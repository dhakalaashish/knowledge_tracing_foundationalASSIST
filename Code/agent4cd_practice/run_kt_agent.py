#!/usr/bin/env python3
"""
Agent4CD + cognitive student modeling on the FoundationalASSIST KT benchmark (after kt_benchmark.py).

One agent per student (the 100 students of kt_practice_benchmark.py), all students at once; each student's events run
in order:
    memory  <- the first 50 answers (Eq. 4), with the student's answers and hint / answer-view flags
    SR_0    <- initial summary reflection
    for each bin b:
        predict each target of the bin (1 or 2; the same state, as in the paper's benchmark): reasoning, affect,
            the exact answer and Yes/No, with the NCDM mastery fitted on the history before bin b
        reveal the bin's 10 answers one by one (online feedback): each enters the memory and is reflected on
            (kt.reflect_every_answer; false: one reflection after the bin's last answer)
    (after the last bin that has a target, nothing more is revealed)
Each event is appended to results/kt/<run>/students/<user>.jsonl when done; a rerun replays them and continues.
When every student is done, all predictions are written in the benchmark's format to
<out-dir>/agent4cd_qwen3next80b_awq_bin10_hist50.jsonl (kt_practice_benchmark.py evaluate reads it as "agent4cd"):
predicted_question_level = Yes -> 1 / No -> 0, predicted_student_answer = the predicted answer. An answer that does
not parse stays empty (scored as wrong, like the other runs).

Needs the vLLM server (run_kt_gb300.sh starts it). From Code/agent4cd_practice:
    python3 run_kt_agent.py --dry-run          # the prompts of one student, no LLM
    python3 run_kt_agent.py --out-dir ../../Results/kt_practice_main
"""

import argparse
import asyncio
import json
import math
import os
import time
from collections import defaultdict
from types import SimpleNamespace

from common import HERE, load_config, read_json, read_pickle, write_json
from agent.kt_prompts import prediction_prompt, prediction_schema, reflection_prompt
from agent.learner_profile import profile_prompt
from agent.llm import LLMClient, parse_prediction, yes_probability
from agent.memory import Memory

KT_DATA = HERE / "data" / "kt" / "kt_data.pkl"
MIN_HISTORY, BIN_SIZE = 50, 10
DEFAULT_OUT = HERE.parent.parent / "Results" / "kt_practice_main"
RESULT_NAME = f"agent4cd_qwen3next80b_awq_bin{BIN_SIZE}_hist{MIN_HISTORY}.jsonl"


def plain(value):
    """JSON-safe: numpy numbers to Python, NaN to None."""
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


class Progress:
    def __init__(self, total, done):
        self.total, self.done, self.new, self.right, self.calls, self.start = total, done, 0, 0, 0, time.time()

    def call(self):
        self.calls += 1

    def prediction(self, step, truth):
        self.done += 1
        self.new += 1
        self.right += int(step.get("prediction") == truth)
        if self.new % 100 == 0 or self.done == self.total:
            elapsed = time.time() - self.start
            rate = self.new / elapsed * 3600
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.done}/{self.total} predictions  KT ACC (this session) "
                  f"{self.right / self.new:.4f}  {self.calls} LLM calls  {rate:.0f} predictions/h  "
                  f"ETA {(self.total - self.done) / max(rate, 1e-9):.1f} h", flush=True)


class KTAgent:
    def __init__(self, user, ctx, llm, log_path):
        self.user, self.ctx, self.llm, self.log_path = user, ctx, llm, log_path
        self.cfg = ctx.config
        self.records = ctx.records[user]
        self.theta = ctx.theta[user]
        self.by_bin = defaultdict(list)
        for t in ctx.targets[user]:
            self.by_bin[int(t["bin_number"])].append(t)
        self.system = profile_prompt(ctx.profiles[user])
        self.memory = Memory(ctx.related, self.cfg["agent"]["short_term_size"])
        for r in self.records[:MIN_HISTORY]:
            self.add(r)

    def add(self, r):
        pid = r["problem_id"]
        self.memory.add(pid, self.ctx.q.get(pid, []), r["right"], answer=r["answer"], hint=r["hint"], saw=r["saw"])

    def messages(self, prompt):
        return [{"role": "system", "content": self.system}, {"role": "user", "content": prompt}]

    def events(self):
        """('init',), ('predict', bin, target), ('reveal', bin, record index, reflect?) in order."""
        yield ("init",)
        if not self.by_bin:
            return
        last = max(self.by_bin)
        every = self.cfg["kt"]["reflect_every_answer"]
        for b in range(last + 1):
            for t in self.by_bin.get(b, []):
                yield ("predict", b, t)
            if b == last:
                break
            start = MIN_HISTORY + b * BIN_SIZE
            for i in range(start, start + BIN_SIZE):
                yield ("reveal", b, i, every or i == start + BIN_SIZE - 1)

    # ------------------------------------------------------------------ saved events
    def saved_entries(self):
        if not self.log_path or not os.path.exists(self.log_path):
            return []
        entries = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:   # cut off by a crash: drop it and everything after
                        break
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(e, ensure_ascii=False) + "\n" for e in entries)
        return entries

    def save(self, entry):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ------------------------------------------------------------------ LLM calls
    async def reflect(self, theta, event=None):
        prompt = reflection_prompt(self.ctx, self.memory, theta, event)
        result = await self.llm.chat(self.messages(prompt), self.cfg["kt"]["llm"]["max_tokens_reflect"])
        self.ctx.progress.call()
        return result["text"].strip(), result

    async def predict(self, t, previous_reasoning):
        b = int(t["bin_number"])
        pid = int(t["problem_id"])
        prompt = prediction_prompt(pid, self.ctx, self.memory, self.theta[b], previous_reasoning)
        max_tokens = self.cfg["kt"]["llm"]["max_tokens_predict"]
        tokens = [0, 0]
        for attempt in range(2):   # a cut-off answer is retried once with twice the tokens (as run_agent.py)
            result = await self.llm.chat(self.messages(prompt), max_tokens * (attempt + 1), schema=prediction_schema(),
                                         logprobs=True)
            self.ctx.progress.call()
            tokens[0] += result["prompt_tokens"]
            tokens[1] += result["completion_tokens"]
            parsed = parse_prediction(result["text"])
            if parsed is not None and result["finish_reason"] != "length":
                break
        step = {"type": "predict", "prediction_id": t["prediction_id"], "row_index": int(t["row_index"]), "bin": b,
                "prompt_tokens": tokens[0], "completion_tokens": tokens[1], "raw": result["text"],
                "prediction": None, "p_yes": None, "student_answer": None, "task1": None, "task2": None}
        if parsed is not None:
            prediction = 1 if parsed["task3"] == "Yes" else 0
            p_yes = yes_probability(result["logprobs"])
            step.update(prediction=prediction, p_yes=float(prediction) if p_yes is None else p_yes,
                        student_answer=str(parsed.get("student_answer") or ""), task1=parsed.get("task1"),
                        task2=parsed.get("task2"))
        return step

    # ------------------------------------------------------------------ the run
    async def run(self):
        saved = self.saved_entries()
        k = 0
        previous_reasoning = None
        predicted = {}   # record index -> prediction step, for the reflection on that answer

        def take(kind, key=None, field=None):
            nonlocal k
            if k < len(saved) and saved[k]["type"] == kind and (field is None or saved[k][field] == key):
                k += 1
                return saved[k - 1]
            return None

        for ev in self.events():
            if ev[0] == "init":
                entry = take("init")
                if entry is None:
                    status, result = await self.reflect(self.theta[0])
                    entry = {"type": "init", "user": self.user, "reflection": status,
                             "prompt_tokens": result["prompt_tokens"], "completion_tokens": result["completion_tokens"]}
                    self.save(entry)
                self.memory.learning_status.append(entry["reflection"])
            elif ev[0] == "predict":
                _, b, t = ev
                # the agent has seen exactly the paper's history for this target, and not the target itself
                assert len(self.memory.facts) == int(t["history_size"]) == MIN_HISTORY + b * BIN_SIZE
                assert int(t["row_index"]) >= int(t["history_size"])
                step = take("predict", t["prediction_id"], "prediction_id")
                if step is None:
                    step = await self.predict(t, previous_reasoning)
                    self.save(step)
                    self.ctx.progress.prediction(step, self.records[int(t["row_index"])]["right"])
                predicted[int(t["row_index"])] = step
                previous_reasoning = step.get("task1") or previous_reasoning
            else:
                _, b, i, reflect_now = ev
                r = self.records[i]
                self.add(r)
                if reflect_now:
                    entry = take("reflect", i, "index")
                    if entry is None:
                        p = predicted.get(i)
                        event = {"exercise": r["problem_id"], "truth": r["right"], "answer": r["answer"],
                                 "hint": r["hint"], "saw": r["saw"]}
                        if p is not None and p.get("prediction") is not None:
                            event.update(prediction=p["prediction"], predicted_answer=p.get("student_answer"),
                                         task1=p.get("task1"), task2=p.get("task2"))
                        status, result = await self.reflect(self.theta[b], event)
                        entry = {"type": "reflect", "index": i, "bin": b, "reflection": status,
                                 "corrective": (None if p is None or p.get("prediction") in (None, r["right"]) else
                                                "false_negative" if r["right"] == 1 else "false_positive"),
                                 "prompt_tokens": result["prompt_tokens"], "completion_tokens": result["completion_tokens"]}
                        self.save(entry)
                    self.memory.learning_status.append(entry["reflection"])
                if i == MIN_HISTORY + (b + 1) * BIN_SIZE - 1:
                    predicted = {}

    def dry_run(self):
        print("=" * 30, f"student {self.user}", "=" * 30)
        n_pred = sum(len(v) for v in self.by_bin.values())
        n_reflect = sum(1 for ev in self.events() if ev[0] == "reveal" and ev[3])
        print(f"{len(self.records)} records, {n_pred} targets, {n_reflect} reflections after answers, profile "
              f"{self.ctx.profiles[self.user]['levels']}")
        print("\n--- SYSTEM ---\n" + self.system)
        print("\n--- USER (initial reflection SR_0) ---\n" + reflection_prompt(self.ctx, self.memory, self.theta[0]))
        self.memory.learning_status.append("<the initial reflection would appear here>")
        t = self.by_bin[min(self.by_bin)][0]
        b = int(t["bin_number"])
        for i in range(MIN_HISTORY, MIN_HISTORY + b * BIN_SIZE):   # the answers before the first target's bin
            self.add(self.records[i])
        print(f"\n--- USER (prediction, {t['prediction_id']}) ---\n"
              + prediction_prompt(int(t["problem_id"]), self.ctx, self.memory, self.theta[b], None))
        print(f"\n--- JSON schema ---\n{json.dumps(prediction_schema())}")
        r = self.records[int(t["row_index"])]
        self.add(r)
        fake = {"exercise": r["problem_id"], "truth": r["right"], "answer": r["answer"], "hint": r["hint"],
                "saw": r["saw"], "prediction": 1 - r["right"], "predicted_answer": "<predicted answer>",
                "task1": "<reasoning>", "task2": "confident"}
        print("\n--- USER (reflection after that answer, if the prediction had been wrong) ---\n"
              + reflection_prompt(self.ctx, self.memory, self.theta[b], fake))


def build_context(config):
    if not KT_DATA.exists():
        raise SystemExit(f"{KT_DATA} is missing: run python3 kt_benchmark.py first")
    data = read_pickle(KT_DATA)
    ctx = SimpleNamespace(config=config, exercises=data["exercises"], concepts=data["concepts"], q=data["q"],
                          related={int(c): set(r) for c, r in data["related"].items()}, records=data["records"],
                          targets=data["targets"], theta=data["theta"], profiles=data["profiles"], progress=None)
    users = [u for u in data["users"] if data["targets"][u]]
    return ctx, users, data


def write_results(ctx, users, run_dir, out_path, model):
    """Every prediction in the benchmark's format, once every student is done."""
    rows = []
    for u in users:
        steps = {}
        with open(run_dir / "students" / f"{u}.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                e = json.loads(line)
                if e["type"] == "predict":
                    steps[e["prediction_id"]] = e
        for t in ctx.targets[u]:
            s = steps[t["prediction_id"]]
            row = {k: plain(v) for k, v in t.items()}
            row.update(predicted_skill_level=None, predicted_question_level=s["prediction"],
                       predicted_student_answer=s["student_answer"], p_yes=s["p_yes"], task1=s["task1"],
                       task2=s["task2"], full_response=s["raw"], model=model, method="agent4cd")
            rows.append(row)
    tmp = str(out_path) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    os.replace(tmp, out_path)
    print(f"Wrote {len(rows):,} predictions to {out_path}", flush=True)


async def run_all(config, users, ctx, run_dir, out_path):
    llm = LLMClient(config["kt"]["llm"])
    await llm.check_server()
    paths = {u: run_dir / "students" / f"{u}.jsonl" for u in users}
    total = sum(len(ctx.targets[u]) for u in users)
    done = 0
    for p in paths.values():
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                done += sum('"type": "predict"' in line for line in f)
    ctx.progress = Progress(total, done)
    print(f"{len(users)} students, {total:,} predictions ({done:,} already done); reflect after every answer: "
          f"{config['kt']['reflect_every_answer']}", flush=True)
    agents = [KTAgent(u, ctx, llm, paths[u]) for u in users]
    results = await asyncio.gather(*(a.run() for a in agents), return_exceptions=True)
    failed = [(u, r) for u, r in zip(users, results) if isinstance(r, Exception)]
    for u, error in failed[:10]:
        print(f"Student {u} failed: {type(error).__name__}: {error}", flush=True)
    if failed:
        raise SystemExit(f"{len(failed)} students failed; run again to resume them (nothing written to {out_path})")
    write_results(ctx, users, run_dir, out_path, config["kt"]["llm"]["model"])


def main():
    config = load_config()
    ap = argparse.ArgumentParser(description="Agent4CD + cognitive student modeling on the KT benchmark")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT), help="kt_practice_benchmark's folder; the results go there")
    ap.add_argument("--run-name", default=config["kt"]["run_name"])
    ap.add_argument("--dry-run", action="store_true", help="print one student's prompts without calling the LLM")
    args, _ = ap.parse_known_args()
    ctx, users, data = build_context(config)
    total = sum(len(ctx.targets[u]) for u in users)
    print(f"{len(users)} students with targets, {total:,} predictions; NCDM validation AUC {data['ncdm']['val_auc']:.4f}; "
          f"KC relations {data['relations']['num_edges']} edges", flush=True)
    if args.dry_run:
        n_calls = 0
        for u in users:
            agent = KTAgent(u, ctx, None, None)
            n_calls += sum(1 for ev in agent.events() if ev[0] in ("init", "predict") or (ev[0] == "reveal" and ev[3]))
        print(f"LLM calls for the whole run: about {n_calls:,} (plus retries)")
        KTAgent(users[0], ctx, None, None).dry_run()
        return
    run_dir = HERE / "results" / "kt" / args.run_name
    settings = {"agent": config["agent"], "kt": {k: v for k, v in config["kt"].items() if k != "run_name"},
                "users": users}
    saved = run_dir / "run_config.json"
    if saved.exists() and read_json(saved)["settings"] != settings:
        raise SystemExit(f"{run_dir} was run with other settings; use another --run-name or delete it")
    os.makedirs(run_dir / "students", exist_ok=True)
    write_json(saved, {"settings": settings})
    out_path = os.path.join(os.path.abspath(args.out_dir), RESULT_NAME)
    asyncio.run(run_all(config, users, ctx, run_dir, out_path))


if __name__ == "__main__":
    main()
