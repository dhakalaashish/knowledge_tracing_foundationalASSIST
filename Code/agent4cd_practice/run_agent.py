"""
Run Agent4CD on one split: one LLM agent per learner, the first num_students learners of the seeded
order from prepare_data.py. Learners run concurrently; each learner predicts its test records one
after another (the agent's memory and learning status change from one record to the next).

Needs: prepare_data.py and train_tools.py for the split (and maca_cd's state file with
knowledge_tool maca_cd), and the vLLM server:
    VLLM_USE_FLASHINFER_SAMPLER=0 vllm serve Qwen/Qwen3-30B-A3B-Instruct-2507 --port 8000 \
        --max-model-len 32768 --enable-prefix-caching

Usage (from Code/agent4cd_practice):
    python3 run_agent.py --split standard --run-name full --dry-run          # print the prompts of 2 learners
    PYTHONUNBUFFERED=1 nohup python3 run_agent.py --split standard --run-name full > logs/standard_full.log 2>&1 &

Settings come from config.json; --num-students, --knowledge-tool, --ablation and --online-feedback
override them for one run. Each run directory (results/<split>/<run-name>/) keeps its settings in
run_config.json and one JSONL file per learner; rerunning the same command resumes, and a larger
--num-students adds learners to a finished run.
"""

import argparse
import asyncio
import os
import time
from types import SimpleNamespace

import numpy as np

from agent.agent import LearnerAgent
from agent.learner_profile import ability_thresholds, build_profile
from agent.llm import LLMClient
from common import (ABLATIONS, SPLITS, TOOLS, data_dir, load_config, read_json, read_pickle, run_dir, tool_dir,
                    write_json)
from tools.knowledge_state import load_knowledge_tool


def parse_args(config):
    parser = argparse.ArgumentParser(description="Run the Agent4CD learner agents on one split")
    parser.add_argument("--split", default=config["split"], choices=SPLITS)
    parser.add_argument("--run-name", required=True, help="Results go to results/<split>/<run-name>/")
    parser.add_argument("--num-students", type=int, default=None, help="Override config num_students")
    parser.add_argument("--learner-file", default=None,
                        help="Run exactly the learners of this list (from make_learner_list.py) "
                             "instead of the first num_students")
    parser.add_argument("--knowledge-tool", choices=TOOLS, default=None, help="Override config knowledge_tool")
    parser.add_argument("--ablation", choices=ABLATIONS, default=None, help="Override config agent.ablation")
    parser.add_argument("--online-feedback", choices=["true", "false"], default=None,
                        help="Override config agent.online_feedback")
    parser.add_argument("--dry-run", action="store_true", help="Print the prompts without calling the LLM")
    parser.add_argument("--limit", type=int, default=2, help="With --dry-run: number of learners to show")
    return parser.parse_args()


def apply_overrides(config, args):
    if args.num_students is not None:
        config["num_students"] = args.num_students
    if args.knowledge_tool is not None:
        config["knowledge_tool"] = args.knowledge_tool
    if args.ablation is not None:
        config["agent"]["ablation"] = args.ablation
    if args.online_feedback is not None:
        config["agent"]["online_feedback"] = args.online_feedback == "true"
    if config["agent"]["ablation"] not in ABLATIONS:
        raise ValueError(f"agent.ablation must be one of {ABLATIONS}")


def run_settings(config, split):
    """The settings a run's results depend on (everything but the number of learners)."""
    return {
        "split": split,
        "knowledge_tool": config["knowledge_tool"],
        "maca_cd_seed": config.get("maca_cd_seed") if config["knowledge_tool"] == "maca_cd" else None,
        "agent": config["agent"],
        "model": config["llm"]["model"],
        "temperature": config["llm"]["temperature"],
    }


class Progress:
    """Prints the number of finished test records, running agent ACC, tokens and an ETA."""

    def __init__(self, total, already_done, every=200):
        self.total, self.done, self.every = total, already_done, every
        self.new = self.correct = self.tokens = 0
        self.start = time.time()

    def update(self, step):
        self.done += 1
        self.new += 1
        self.correct += int(step["prediction"] == step["truth"])
        self.tokens += step["completion_tokens"]
        if self.new % self.every == 0 or self.done == self.total:
            elapsed = time.time() - self.start
            rate = self.new / elapsed * 3600
            eta = (self.total - self.done) / max(rate, 1e-9)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.done}/{self.total} test records  "
                  f"ACC (this session) {self.correct / self.new:.4f}  {rate:.0f} records/h  "
                  f"{self.tokens / elapsed:.0f} output tokens/s  ETA {eta:.1f} h", flush=True)


def select_learners(data, config, split, learner_file):
    """The learners of --learner-file, or else the first num_students of the seeded order."""
    if learner_file is None:
        return data["student_order"][:config["num_students"]]
    listing = read_json(learner_file)
    if listing["split"] != split:
        raise SystemExit(f"{learner_file} lists learners of the {listing['split']} split, not {split}")
    learners = []
    for row in listing["learners"]:
        s = row["student"]
        if data["student_ids"][s] != row["cleaned_student_id"] or s not in data["test"]:
            raise SystemExit(f"{learner_file}: learner {s} does not match data/{split} (rerun make_learner_list.py)")
        learners.append(s)
    return learners


def build_context(config, split, learner_file=None):
    """Everything the agents share; the selected learners get a profile."""
    data = read_pickle(data_dir(split) / "students.pkl")
    records = read_pickle(data_dir(split) / "records.pkl")
    exercises = read_json(data_dir(split) / "exercises.json")
    concepts = read_json(data_dir(split) / "concepts.json")
    relations = read_json(data_dir(split) / "kc_relations.json")
    irt_path = tool_dir(split) / "irt.npz"
    if not irt_path.exists():
        raise FileNotFoundError(f"{irt_path} is missing: run python3 train_tools.py --split {split}")
    ability = np.load(irt_path)["ability"]
    tool = load_knowledge_tool(split, config, records)
    tool_pred = {(int(s), int(e)): float(p) for (s, e, _), p in zip(records["test"], tool["test_pred"])}
    students = select_learners(data, config, split, learner_file)
    cuts = ability_thresholds(ability, data["history"])
    profiles = {s: build_profile(data["profile_stats"][s], data["profile_thresholds"], ability[s], cuts, concepts)
                for s in students}
    print(f"Knowledge-state tool: {tool['name']} ({tool['path']})")
    ctx = SimpleNamespace(
        config=config, exercises=exercises, concepts=concepts,
        related={int(c): set(r) for c, r in relations["related"].items()},
        proficiency=tool["proficiency"], tool_name=tool["name"], tool_pred=tool_pred,
        history=data["history"], test=data["test"], profiles=profiles, progress=None,
    )
    return ctx, students


def count_saved_steps(path):
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        return sum('"type": "step"' in line for line in f)


async def run(config, split, out, students, ctx):
    llm = LLMClient(config["llm"])
    await llm.check_server()
    paths = {s: out / "students" / f"{s}.jsonl" for s in students}
    total = sum(len(ctx.test[s]) for s in students)
    already = sum(count_saved_steps(p) for p in paths.values())
    ctx.progress = Progress(total, already)
    print(f"{len(students)} learners, {total} test records ({already} already done); "
          f"online_feedback={config['agent']['online_feedback']}, ablation={config['agent']['ablation']}", flush=True)
    agents = [LearnerAgent(s, ctx, llm, paths[s]) for s in students]
    results = await asyncio.gather(*(agent.run() for agent in agents), return_exceptions=True)
    failed = [(s, r) for s, r in zip(students, results) if isinstance(r, Exception)]
    for s, error in failed[:10]:
        print(f"Learner {s} failed: {type(error).__name__}: {error}")
    if failed:
        print(f"{len(failed)} learners failed; rerun the same command to resume them.")
    else:
        print(f"All learners done. Next: python3 evaluate.py --split {split} --run-name {out.name}")


def main():
    config = load_config()
    args = parse_args(config)
    apply_overrides(config, args)
    split = args.split
    out = run_dir(split, args.run_name)

    settings = run_settings(config, split)
    saved_path = out / "run_config.json"
    if saved_path.exists() and not args.dry_run:
        saved = read_json(saved_path)
        if saved["settings"] != settings:
            raise SystemExit(f"{out} was run with other settings:\n  saved: {saved['settings']}\n  now:   {settings}\n"
                             f"Use another --run-name, or delete {out}.")
        if args.learner_file is None and saved.get("learner_file") is None:
            config["num_students"] = max(config["num_students"], saved["num_students"])

    ctx, students = build_context(config, split, args.learner_file)

    if args.dry_run:
        for s in students[:args.limit]:
            LearnerAgent(s, ctx, None, None).dry_run()
        return
    os.makedirs(out / "students", exist_ok=True)
    write_json(saved_path, {"settings": settings, "num_students": len(students),
                            "learner_file": args.learner_file, "students": students})
    asyncio.run(run(config, split, out, students, ctx))


if __name__ == "__main__":
    main()
