"""Diagnose students' common wrong answers: for each (problem, wrong answer), ask an LLM which practice steps the
student did correctly, where the student went wrong, and which steps the student never got to (prompt 4 in
prompts.py). One call per wrong answer.

Inputs
    Results/practice_analysis/common_wrong_answers.csv   wrong answers given by >= 2 students on their first attempt
                                                         without hints or answer views (Code/practice_analysis/wrong_answers.js)
    Data/Problems.csv                                    the item's correct answer, and the practice analysis in
                                                         <practice prefix>_reasoning (answer 1 in the order of answer 2)
    problems_rendered.jsonl                              the item text the labeling prompts used

Each answer is checked with a JSON parser and the rules of prompts.PROMPT_RESPONSE_4 (common.check_diagnosis): the
steps must be the analysis's practices in order, each with a status (correct / failed / not_reached / cannot_tell),
and error_type practice / math_fact / guess must agree with the statuses. A failed check is retried in a fresh
conversation, at most 1 + --max-retries-per-problem attempts.

Output
    runs/<name>/items/<key>.json       every call, attempt and parsed answer (key = r<row>_w<rank>)
    runs/<name>/manifest.json          settings, full system prompt; a later invocation with other settings stops
    runs/<name>/failed_items.csv       wrong answers that failed every attempt
    Data/wrong_answer_diagnosis_<name>.csv   one line per diagnosed wrong answer

Examples
    python3 diagnose.py --provider local --model Qwen/Qwen3.5-122B-A10B-FP8 --practice-prefix qwen35_122b \\
        --name qwen35_122b_diag --rows 1-300 --dry-run
    python3 diagnose.py --provider local --model Qwen/Qwen3.5-122B-A10B-FP8 --practice-prefix qwen35_122b \\
        --name qwen35_122b_diag --max-model-len 65536
"""

import argparse
import csv
import json
import os
import re
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import common
import generate
import prompts as PR

DEFAULT_WRONG = os.path.join(common.REPO_ROOT, "Results", "practice_analysis", "common_wrong_answers.csv")
TYPE_ALIASES = {"fill": "Fill-in-the-blank(s)", "mc": "Multiple Choice (select 1)",
                "all": "Multiple Choice (select all)", "order": "Order / Sort"}
LOCKED_KEYS = ["provider", "model", "framework", "system_prompt_4_sha256", "q4_template_sha256", "params",
               "practice_prefix", "min_students"]


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", required=True, choices=["anthropic", "openai", "gemini", "local"])
    ap.add_argument("--model", help="model id (default depends on --provider)")
    ap.add_argument("--practice-prefix", required=True,
                    help="column prefix in Problems.csv whose <prefix>_reasoning gives each item's practices "
                         "(e.g. qwen35_122b, or qwen3_30b_v3)")
    ap.add_argument("--name", help="run name: folder runs/<name> and Data/wrong_answer_diagnosis_<name>.csv "
                                   "(default <practice prefix>_diag)")
    ap.add_argument("--wrong-answers", default=DEFAULT_WRONG)
    ap.add_argument("--min-students", type=int, default=2, help="diagnose wrong answers given by at least this many students")
    ap.add_argument("--types", default="fill,mc,all,order",
                    help="question types, comma-separated: fill, mc (select 1), all (select all), order")
    ap.add_argument("--rows", help="data rows of Problems.csv, e.g. '1-300' (default: all)")
    ap.add_argument("--max-items", type=int, help="stop after this many wrong answers (for a quick test)")
    ap.add_argument("--problems-csv", default=common.DEFAULT_PROBLEMS_CSV)
    ap.add_argument("--framework", default="standard", choices=["standard", "naep_ch3"])
    ap.add_argument("--chapter-file", default=common.DEFAULT_CHAPTER)
    ap.add_argument("--max-retries-per-problem", type=int, default=3)
    ap.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--max-tokens", type=int, help="output token limit per call")
    ap.add_argument("--temperature", type=float)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-retries", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true", help="print the system prompt and two user prompts, then stop")
    ap.add_argument("--write-only", action="store_true", help="skip the LLM; write the output CSV from the logs")
    ap.add_argument("--force", action="store_true", help="allow settings that differ from the run's manifest")
    generate.add_provider_args(ap)
    args = ap.parse_args()
    args.model = args.model or generate.DEFAULT_MODELS[args.provider]
    args.name = args.name or f"{args.practice_prefix}_diag"
    args.column_prefix = args.name            # providers and logs use this field
    args.run_dir = os.path.join(common.RUNS_DIR, args.name)
    return args


# ---------------------------------------------------------------- data

MONTHS = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}


def clean_answer(text):
    """Correct answer from Problems.csv as plain text (HTML removed; spreadsheet dates such as 4-Jan back to 1/4)."""
    t = re.sub(r"<[^>]+>", " ", text or "")
    t = t.replace("&nbsp;", " ").replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
    t = re.sub(r"\b(\d{1,2})-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b",
               lambda m: f"{MONTHS[m.group(2).lower()]}/{m.group(1)}", t, flags=re.I)
    return re.sub(r"\s+", " ", t).strip()


def load_items(args):
    common._raise_field_limit()
    with open(args.problems_csv, encoding="utf-8", newline="") as f:
        table = list(csv.reader(f))
    head, body = table[0], table[1:]
    h = {c: i for i, c in enumerate(head)}
    col = f"{args.practice_prefix}_reasoning"
    if col not in h:
        sys.exit(f"{args.problems_csv} has no column {col}; run generate.py for that prefix first")
    texts = common.load_problems()
    types = [TYPE_ALIASES.get(t.strip(), t.strip()) for t in args.types.split(",") if t.strip()]
    rows = set(common.parse_rows(args.rows, len(body))) if args.rows else None
    items, skipped = [], {"no_analysis": 0}
    with open(args.wrong_answers, encoding="utf-8", newline="") as f:
        for w in csv.DictReader(f):
            row = int(w["row"])
            if int(w["students"]) < args.min_students or w["problem_type"] not in types or (rows and row not in rows):
                continue
            r = body[row - 1]
            if r[h["problem_id"]].strip() != w["problem_id"].strip():
                sys.exit(f"row {row}: problem_id {r[h['problem_id']]} in Problems.csv, {w['problem_id']} in {args.wrong_answers}")
            try:
                analysis = json.loads(r[h[col]])
                assert analysis["practices_used"]
            except Exception:
                skipped["no_analysis"] += 1
                continue
            ptype = w["problem_type"]
            if ptype == "Order / Sort":
                correct = "(not given: work out the correct order from the item)"
            elif ptype.startswith("Multiple Choice"):
                correct = clean_answer(r[h["Multiple Choice Answers"]]).replace(" || ", "; ")
            else:
                correct = clean_answer(r[h["Fill-in Answers"]]).replace(" || ", " or ")
            items.append({"key": f"r{row:05d}_w{int(w['rank']):03d}", "row": row, "problem_id": w["problem_id"],
                          "problem_type": ptype, "wrong_answer": w["wrong_answer"], "students": int(w["students"]),
                          "share": float(w["share_of_wrong"]), "rank": int(w["rank"]), "correct": correct or "(not given)",
                          "text": texts[row]["text"], "analysis": analysis})
    if args.max_items:
        items = items[:args.max_items]
    return items, skipped


def build_prompt4(prompts, it):
    return common.fill(prompts["q4_template"], PROBLEM=it["text"], CORRECT=it["correct"],
                       ANALYSIS=json.dumps(it["analysis"], ensure_ascii=False, indent=2), WRONG=it["wrong_answer"],
                       COUNT=str(it["students"]), SHARE=f"{round(100 * it['share'])}%")


# ---------------------------------------------------------------- run

def item_path(args, key):
    return os.path.join(args.run_dir, "items", f"{key}.json")


def load_item(args, key):
    p = item_path(args, key)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def check_manifest(args, config):
    path = os.path.join(args.run_dir, "manifest.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
        diff = [k for k in LOCKED_KEYS if old["config"].get(k) != config.get(k)]
        if diff and not args.force:
            sys.exit(f"Settings differ from {path} in: {', '.join(diff)}. Use another --name, or --force.")
        if diff:
            old.setdefault("config_changes", []).append({"at": common.now(), "changed": diff, "config": config})
            common.write_json_atomic(path, old)
        return
    common.write_json_atomic(path, {"created_at": common.now(), "config": config, "environment": common.environment_info()})


def finish(rec, call, error, invalid, checker, max_retries):
    reason = error or invalid
    att = {"attempt": len(rec["attempts"]) + 1, "calls": [call] if call else [],
           "failure_kind": ("error" if error else "invalid_answer") if reason else None, "failure_reason": reason,
           "parsed_answers": checker.parsed, "json_extraction": checker.how}
    rec["attempts"].append(att)
    if reason is None:
        ans = checker.parsed[0]
        rec["final"] = {"status": "ok", "attempt": att["attempt"], "answer": call["response_text"], "answer_json": ans,
                        "error_type": ans["error_type"], "failed_practice": checker.failed_practice}
        return False
    n_failed = sum(1 for a in rec["attempts"] if a["failure_reason"])
    status = "pending_retry" if n_failed <= max_retries else "failed"
    rec["final"] = {"status": status, "failed_attempts": n_failed, "last_failure_kind": att["failure_kind"],
                    "last_failure_reason": reason}
    return status == "pending_retry"


def run(args, provider, prompts, items):
    desc = provider.describe()
    records, by_key = {}, {it["key"]: it for it in items}
    for it in items:
        old = load_item(args, it["key"])
        st = old["final"]["status"] if old else None
        if st == "ok" or (st == "failed" and not args.retry_failed):
            continue
        if st == "pending_retry":
            records[it["key"]] = old
            continue
        rec = {k: it[k] for k in ("key", "row", "problem_id", "problem_type", "wrong_answer", "students", "share", "rank", "correct")}
        rec.update({"practice_prefix": args.practice_prefix, "analysis": it["analysis"], "provider": args.provider,
                    "model": args.model, "generation_params": desc["params"], "attempts": [], "final": {"status": "pending"}})
        if old:
            rec["earlier_failed_attempts"] = old.get("earlier_failed_attempts", []) + old["attempts"]
        records[it["key"]] = rec
    print(f"{len(items) - len(records)} of {len(items)} wrong answers already done; {len(records)} to run, "
          f"up to {1 + args.max_retries_per_problem} attempts each.", flush=True)
    counts = {"ok": 0, "failed": 0}
    pending, round_no = sorted(records), 0
    while pending:
        round_no += 1
        print(f"Round {round_no}: {len(pending)} wrong answers", flush=True)
        checkers = {k: common.DiagnosisChecker(by_key[k]["analysis"]) for k in pending}
        if hasattr(provider, "attempt_of"):
            provider.attempt_of = {k: len(records[k]["attempts"]) for k in pending}
        again = []
        for k, call, error in call_all(args, provider, prompts, [by_key[k] for k in pending]):
            invalid = None if error else checkers[k].check(4, call["response_text"])
            more = finish(records[k], call, error, invalid, checkers[k], args.max_retries_per_problem)
            common.write_json_atomic(item_path(args, k), records[k])
            f = records[k]["final"]
            note = (f"{f['error_type']}" + (f", failed at {f['failed_practice']}" if f["failed_practice"] else "")) if f["status"] == "ok" \
                else f"{f['last_failure_kind']}: {f['last_failure_reason'].splitlines()[0]}"
            print(f"  {k} [{by_key[k]['wrong_answer'][:30]}]: {f['status']} {note}", flush=True)
            if more:
                again.append(k)
            else:
                counts[f["status"]] += 1
        pending = sorted(again)
    return counts


def call_all(args, provider, prompts, items):
    """Yield (key, call record, error) for prompt 4 of each item."""
    if args.provider == "local":
        reqs = [(it["key"], prompts["system_4"], build_prompt4(prompts, it), 4) for it in items]
        for k, rec, error in provider.call_many(reqs):
            yield k, rec, error
        return

    def one(it):
        calls = []
        try:
            provider.call(prompts["system_4"], build_prompt4(prompts, it), 4, calls)
            return it["key"], calls[-1], None
        except Exception as e:
            return it["key"], (calls[-1] if calls else None), f"{type(e).__name__}: {e}\n{traceback.format_exc(limit=3)}"

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for fut in as_completed([ex.submit(one, it) for it in items]):
            yield fut.result()


# ---------------------------------------------------------------- outputs

def write_outputs(args):
    items_dir = os.path.join(args.run_dir, "items")
    recs = []
    for name in sorted(os.listdir(items_dir)) if os.path.isdir(items_dir) else []:
        if name.endswith(".json"):
            with open(os.path.join(items_dir, name), encoding="utf-8") as f:
                recs.append(json.load(f))
    out = os.path.join(common.REPO_ROOT, "Data", f"wrong_answer_diagnosis_{args.name}.csv")
    head = ["row", "problem_id", "problem_type", "rank", "wrong_answer", "students", "share_of_wrong", "practice_prefix",
            "error_type", "failed_practice", "math_fact", "reconstruction", "explanation", "confidence", "steps",
            *[f"status_{p.replace(' ', '_').lower()}" for p in PR.PRACTICES], "diagnosis_json"]
    n = 0
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        for r in sorted(recs, key=lambda r: (r["row"], r["rank"])):
            if r["final"].get("status") != "ok":
                continue
            a = r["final"]["answer_json"]
            status = {s["practice"]: s["status"] for s in a["steps"]}
            w.writerow([r["row"], r["problem_id"], r["problem_type"], r["rank"], r["wrong_answer"], r["students"],
                        r["share"], r["practice_prefix"], a["error_type"], r["final"]["failed_practice"] or "",
                        a.get("math_fact", ""), a["reconstruction"], a["explanation"], a["confidence"],
                        " > ".join(f"{s['practice']}: {s['status']}" for s in a["steps"]),
                        *[status.get(p, "") for p in PR.PRACTICES], json.dumps(a, ensure_ascii=False)])
            n += 1
    failed = [r for r in recs if r["final"].get("status") == "failed"]
    fpath = os.path.join(args.run_dir, "failed_items.csv")
    with open(fpath, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["key", "row", "problem_id", "wrong_answer", "attempts", "last_failure_reason"])
        for r in failed:
            w.writerow([r["key"], r["row"], r["problem_id"], r["wrong_answer"], len(r["attempts"]),
                        r["final"]["last_failure_reason"].splitlines()[0]])
    print(f"Wrote {n} diagnoses to {out}; {len(failed)} wrong answers failed every attempt ({fpath})")


def main():
    args = parse_args()
    prompts = common.load_prompts(args.framework, args.chapter_file)
    if args.write_only:
        write_outputs(args)
        return
    items, skipped = load_items(args)
    print(f"{len(items)} wrong answers to diagnose (min students {args.min_students}, types {args.types}); "
          f"skipped {skipped['no_analysis']} without a {args.practice_prefix} analysis", flush=True)
    if args.dry_run:
        print("=" * 30, f"SYSTEM PROMPT 4 ({args.framework})", "=" * 30)
        print(prompts["system_4"])
        for it in items[:2]:
            print("=" * 30, f"USER PROMPT 4: {it['key']}", "=" * 30)
            print(build_prompt4(prompts, it))
        return
    from providers import PROVIDERS
    provider = PROVIDERS[args.provider](args)
    config = {"provider": args.provider, "model": args.model, "name": args.name, "framework": args.framework,
              "chapter_sha256": prompts["chapter_sha256"], "practice_prefix": args.practice_prefix,
              "min_students": args.min_students, "types": args.types,
              "wrong_answers_file": os.path.relpath(args.wrong_answers, common.REPO_ROOT),
              "wrong_answers_sha256": common.sha256(common.read_text(args.wrong_answers)),
              "system_prompt_4": prompts["system_4"], "system_prompt_4_sha256": common.sha256(prompts["system_4"]),
              "q4_template": prompts["q4_template"], "q4_template_sha256": common.sha256(prompts["q4_template"]),
              "params": provider.describe()["params"], "max_retries_per_problem": args.max_retries_per_problem}
    check_manifest(args, config)
    with open(os.path.join(args.run_dir, "invocations.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"at": common.now(), "argv": sys.argv, "items": len(items),
                            "infra": provider.describe().get("infra")}, ensure_ascii=False) + "\n")
    counts = run(args, provider, prompts, items)
    print(f"Finished this invocation: {counts}", flush=True)
    write_outputs(args)


if __name__ == "__main__":
    main()
