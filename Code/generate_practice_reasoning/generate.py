"""Ask an LLM which practices a problem needs, then their order, then which one is the top practice.

Every prompt is in prompts.py. Each problem goes through three separate LLM calls (three fresh
conversations); all see only the problem text, never predicted_practice or any other label:

    Prompt 1 (practices used and not used)
        system: prompts.SYSTEM_PROMPT_1 (practice definitions and descriptors, answer 1 format)
        user:   prompts.Q1_TEMPLATE with the rendered problem
        answer 1: the practices used, in order, with why and likely errors; the practices not used, with why
    Prompt 2 (order), sent only after answer 1 passed the JSON check
        system: prompts.SYSTEM_PROMPT_2 (same definitions and descriptors, answer 2 format)
        user:   prompts.Q2_TEMPLATE with the problem and the practices answer 1 lists as used (fixed
                order, each with answer 1's why; not answer 1's order)
        answer 2: those practices in the order a student uses them, with each step, and why this order
    Answer 1 is reordered as answer 2 says (common.combine): the combined analysis.
    Prompt 3 (top practice), sent only after answer 2 passed the JSON check
        system: prompts.SYSTEM_PROMPT_3 (same definitions and descriptors, answer 3 format)
        user:   prompts.Q3_TEMPLATE with the problem and the combined analysis (JSON)
        answer 3: the top practice, with why

Each answer is checked with a JSON parser and against the format rules. If an answer fails, the
problem starts again from prompt 1 in fresh conversations; a problem gets at most
1 + --max-retries-per-problem (default 3) attempts. Problems that fail every attempt are listed in
runs/<prefix>/failed_problems.csv.

Output columns in Data/Problems.csv:
    <prefix>_reasoning               the combined analysis as JSON (answer 1 in answer 2's order)
    <prefix>_ordering_reasoning      answer 2 as JSON
    <prefix>_top_practice            answer 3's top_practice
    <prefix>_top_practice_reasoning  answer 3's why
With --replace-columns OLD, the OLD_* columns are renamed to <prefix>_* in place and hold only this run.

Every call is logged in runs/<prefix>/rows/row_NNNNN.json (each call's exact request, full raw
response, reasoning when exposed, usage, timestamps, the JSON check result, every attempt); the
full system prompts are in runs/<prefix>/manifest.json. Runs resume: finished rows are skipped.

Examples:
    python3 generate.py --provider anthropic --rows 1-3 --dry-run              # show prompts, no calls
    python3 generate.py --provider anthropic --rows 1-20
    python3 generate.py --provider openai --model gpt-5 --rows 1-300 --workers 8
    python3 generate.py --provider gemini --model gemini-2.5-pro --rows 1-300
    python3 generate.py --provider local --num-gpus 1 --column-prefix qwen3_30b_v3 --replace-columns qwen3_30b_v2
    python3 generate.py --provider anthropic --merge-only                      # rewrite the CSV columns
"""


import argparse
import csv
import json
import os
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import common

DEFAULT_MODELS = {
    "anthropic": "claude-opus-5-5",
    "openai": "gpt-5",
    "gemini": "gemini-2.5-pro",
    "local": "Qwen/Qwen3-30B-A3B-Instruct-2507",
}
DEFAULT_PREFIX = {"anthropic": "claude_api", "openai": "openAI", "gemini": "gemini", "local": "qwen3_30b"}
# Settings that must match for rows of one run (one set of CSV columns) to be comparable.
LOCKED_KEYS = ["provider", "model", "system_prompt_1_sha256", "system_prompt_2_sha256", "system_prompt_3_sha256",
               "q1_template_sha256", "q2_template_sha256", "q3_template_sha256", "params", "no_ordering"]
LOCK_DEFAULTS = {"no_ordering": False}   # runs recorded before the option existed used the order prompt


def add_provider_args(ap):
    """Options of the four providers (also used by diagnose.py)."""
    g = ap.add_argument_group("anthropic")
    g.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"],
                   help="output_config.effort (Claude Opus 5.5 defaults to medium if unset)")
    g.add_argument("--claude-thinking", default="adaptive_summarized", choices=["adaptive_summarized", "omit"],
                   help="adaptive thinking with summarized display (logged), or leave the parameter out")
    g.add_argument("--no-fallbacks", action="store_true", help="turn off the server-side refusal fallback")
    g = ap.add_argument_group("openai")
    g.add_argument("--reasoning-effort", help="reasoning_effort for reasoning models (e.g. low, medium, high)")
    g.add_argument("--base-url", help="OpenAI-compatible server instead of api.openai.com (e.g. a vLLM server)")
    g = ap.add_argument_group("gemini")
    g.add_argument("--gemini-include-thoughts", action="store_true", help="return and log thought summaries")
    g = ap.add_argument_group("local (offline vLLM)")
    g.add_argument("--num-gpus", type=int, default=1,
                   help="GPUs for tensor parallelism; must not exceed the visible GPUs")
    g.add_argument("--gpu-memory-utilization", type=float, default=0.9)
    g.add_argument("--max-model-len", type=int, default=32768)
    g.add_argument("--cache-dir", help="Hugging Face download directory (e.g. /data1/)")
    g.add_argument("--batch-size", type=int, default=512, help="conversations per vLLM call")
    g.add_argument("--top-p", type=float, default=0.8)
    g.add_argument("--top-k", type=int, default=20)
    g.add_argument("--min-p", type=float, default=0.0)
    g.add_argument("--seed", type=int, default=0)
    g.add_argument("--enable-thinking", type=lambda s: s.lower() in ("1", "true", "yes"), default=None,
                   help="pass enable_thinking to the chat template (for hybrid Qwen3 models)")


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", required=True, choices=["anthropic", "openai", "gemini", "local"])
    ap.add_argument("--model", help="model id (default depends on --provider)")
    ap.add_argument("--rows", help="data rows of Problems.csv, e.g. '1-300' or '301-400,512' (default: all)")
    ap.add_argument("--column-prefix", help="CSV column prefix and run folder name "
                                            "(default: claude_api / openAI / gemini / qwen3_30b)")
    ap.add_argument("--run-dir", help="log directory (default: runs/<prefix>)")
    ap.add_argument("--problems-csv", default=common.DEFAULT_PROBLEMS_CSV)
    ap.add_argument("--framework", default="standard", choices=["standard", "naep_ch3"],
                    help="standard: the prompts in prompts.py; naep_ch3: the same prompts with the text of NAEP "
                         "Chapter 3 in front of every system prompt (needs a new --column-prefix)")
    ap.add_argument("--chapter-file", default=common.DEFAULT_CHAPTER,
                    help="text of NAEP Chapter 3 for --framework naep_ch3 (default naep_chapter3.txt)")
    ap.add_argument("--max-retries-per-problem", type=int, default=3,
                    help="retries of a problem after a failed attempt (an answer that fails the JSON check, "
                         "or a failed call, in prompt 1 or prompt 2); each retry starts again from "
                         "prompt 1. A problem gets at most 1 + this many attempts; after that it is "
                         "listed in failed_problems.csv")
    ap.add_argument("--retry-failed", action="store_true",
                    help="give problems that failed in an earlier invocation a fresh set of attempts")
    ap.add_argument("--max-tokens", type=int, help="output token limit per call")
    ap.add_argument("--temperature", type=float, help="sampling temperature (OpenAI, Gemini, local)")
    ap.add_argument("--workers", type=int, default=8, help="parallel conversations for API providers")
    ap.add_argument("--max-retries", type=int, default=8,
                    help="API providers: HTTP retries inside one call on 429/5xx/connection errors "
                         "(separate from --max-retries-per-problem)")
    ap.add_argument("--dry-run", action="store_true", help="print the prompts for the selected rows and stop")
    ap.add_argument("--merge-only", action="store_true", help="skip generation; write the CSV columns from the logs")
    ap.add_argument("--no-merge", action="store_true", help="do not touch Problems.csv after generating")
    ap.add_argument("--no-ordering", action="store_true",
                    help="skip prompt 2 (the order): prompt 3 gets answer 1 in its own order, as in the two-prompt "
                         "version; <prefix>_ordering_reasoning stays empty (needs its own --column-prefix)")
    ap.add_argument("--replace-columns", metavar="OLD_PREFIX",
                    help="when merging, rename the OLD_PREFIX_* columns of Problems.csv to <prefix>_* in place and "
                         "fill them only from this run (e.g. --replace-columns qwen3_30b_v2)")
    ap.add_argument("--force", action="store_true",
                    help="allow settings that differ from the ones recorded for this run directory")
    add_provider_args(ap)
    args = ap.parse_args()
    args.model = args.model or DEFAULT_MODELS[args.provider]
    if args.provider == "openai" and args.base_url and not args.column_prefix:
        ap.error("--base-url needs --column-prefix (the columns would otherwise be called openAI_*)")
    args.column_prefix = args.column_prefix or DEFAULT_PREFIX[args.provider]
    args.run_dir = args.run_dir or os.path.join(common.RUNS_DIR, args.column_prefix)
    return args


def run_config(args, prompts, provider_desc):
    return {
        "provider": args.provider,
        "model": args.model,
        "column_prefix": args.column_prefix,
        "framework": prompts["framework"],
        "no_ordering": args.no_ordering,
        "chapter_sha256": prompts["chapter_sha256"],
        "system_prompt_1": prompts["system_1"],
        "system_prompt_1_sha256": common.sha256(prompts["system_1"]),
        "system_prompt_2": prompts["system_2"],
        "system_prompt_2_sha256": common.sha256(prompts["system_2"]),
        "q1_template": prompts["q1_template"],
        "q1_template_sha256": common.sha256(prompts["q1_template"]),
        "q2_template": prompts["q2_template"],
        "q2_template_sha256": common.sha256(prompts["q2_template"]),
        "system_prompt_3": prompts["system_3"],
        "system_prompt_3_sha256": common.sha256(prompts["system_3"]),
        "q3_template": prompts["q3_template"],
        "q3_template_sha256": common.sha256(prompts["q3_template"]),
        "params": provider_desc["params"],
        "max_retries_per_problem": args.max_retries_per_problem,
        "problems_file": os.path.relpath(common.RENDERED_JSONL, common.HERE),
        "problems_file_sha256": common.sha256(common.read_text(common.RENDERED_JSONL)),
        "answer_check": "each answer must parse as one JSON object (optionally inside one ```json fence) "
                        "and follow prompts.PROMPT_RESPONSE_1 / _2 / _3; each prompt is sent only after the answer "
                        "before it passes; prompt 3 gets answer 1 reordered as answer 2 says (common.combine); "
                        "a failed answer starts the problem again from prompt 1",
        "output_columns": common.output_columns(args.column_prefix),
    }


def check_manifest(args, config):
    """Record the run settings once; refuse to mix different settings in one run directory."""
    path = os.path.join(args.run_dir, "manifest.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
        diff = [k for k in LOCKED_KEYS if old["config"].get(k, LOCK_DEFAULTS.get(k)) != config.get(k)]
        if diff and not args.force:
            sys.exit(f"Settings differ from {path} in: {', '.join(diff)}.\n"
                     f"Use another --column-prefix (new columns), or --force to continue anyway.")
        if diff:
            old.setdefault("config_changes", []).append({"at": common.now(), "changed": diff, "config": config})
            common.write_json_atomic(path, old)
        return
    common.write_json_atomic(path, {"created_at": common.now(), "config": config,
                                    "environment": common.environment_info()})


def log_invocation(args, extra):
    os.makedirs(args.run_dir, exist_ok=True)
    rec = {"at": common.now(), "argv": sys.argv, **extra}
    with open(os.path.join(args.run_dir, "invocations.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def new_record(args, prob, prompts, provider_desc):
    return {
        "row": prob["row"], "problem_id": prob["problem_id"], "problem_text": prob["text"],
        "provider": args.provider, "model": args.model, "column_prefix": args.column_prefix,
        "system_prompt_1_sha256": common.sha256(prompts["system_1"]),
        "system_prompt_2_sha256": common.sha256(prompts["system_2"]),
        "system_prompt_3_sha256": common.sha256(prompts["system_3"]),
        "generation_params": provider_desc["params"],
        "attempts": [], "final": {"status": "pending"},
    }


def finish_attempt(rec, calls, failed_step, error, invalid, checker, max_retries):
    """Add one attempt (prompt 1, and prompts 2 and 3 if they were reached) to the record.

    An attempt fails if any prompt failed: the model's answer did not pass the JSON check
    (invalid), or the call itself failed (error: API error, refusal, output cut off at the token
    limit, empty answer). A failed attempt is retried from prompt 1 while the row has made at most
    max_retries failed attempts, so a row gets at most 1 + max_retries attempts in all.
    Return True if the row needs another attempt.
    """
    reason = error or invalid
    att = {"attempt": len(rec["attempts"]) + 1, "calls": calls or [],
           "failed_step": failed_step if reason else None,
           "failure_kind": ("error" if error else "invalid_answer") if reason else None,
           "failure_reason": reason, "parsed_answers": checker.parsed, "combined": checker.combined,
           "json_extraction": checker.how}
    rec["attempts"].append(att)
    if reason is None:
        with_order = len(calls) == 3       # without the order prompt (--no-ordering) there are two calls
        rec["final"] = {
            "status": "ok", "attempt": att["attempt"],
            "answer1": calls[0]["response_text"], "answer2": calls[1]["response_text"] if with_order else None,
            "answer3": calls[-1]["response_text"],
            "answer1_json": checker.parsed[0], "answer2_json": checker.parsed[1] if with_order else None,
            "answer3_json": checker.parsed[-1], "combined_json": checker.combined,
            "ordering": [it["practice"] for it in checker.combined["practices_used"]],
            "top_practice": checker.parsed[-1]["top_practice"],
        }
        return False
    n_failed = sum(1 for a in rec["attempts"] if a["failure_reason"])
    status = "pending_retry" if n_failed <= max_retries else "failed"
    rec["final"] = {"status": status, "failed_attempts": n_failed, "last_failed_step": failed_step,
                    "last_failure_kind": att["failure_kind"], "last_failure_reason": reason}
    return status == "pending_retry"


def generate(args, provider, prompts, problems, rows):
    desc = provider.describe()
    records = {}
    for r in rows:
        old = common.load_row(args.run_dir, r)
        status = old["final"]["status"] if old else None
        if status == "ok" or (status == "failed" and not args.retry_failed):
            continue
        if status == "pending_retry":
            records[r] = old  # interrupted mid-row: continue its attempt count
        else:
            records[r] = new_record(args, problems[r], prompts, desc)
            if old:  # failed in an earlier invocation (--retry-failed): fresh budget, history kept
                records[r]["earlier_failed_attempts"] = (old.get("earlier_failed_attempts", [])
                                                         + old["attempts"])
    print(f"{len(rows) - len(records)} of {len(rows)} rows already done (ok or failed); "
          f"{len(records)} to run. Each gets up to {1 + args.max_retries_per_problem} attempts.", flush=True)

    counts = {"ok": 0, "failed": 0}
    pending = sorted(records)
    round_no = 0
    while pending:
        round_no += 1
        print(f"Round {round_no}: {len(pending)} problems", flush=True)
        checkers = {r: common.AnswerChecker(no_ordering=args.no_ordering) for r in pending}
        if hasattr(provider, "attempt_of"):  # local vLLM: seed depends on the attempts already made
            provider.attempt_of = {r: len(records[r]["attempts"]) for r in pending}
        again = []
        for r, calls, failed_step, error, invalid in run_problems(args, provider, prompts, problems,
                                                                   pending, checkers):
            rec = records[r]
            more = finish_attempt(rec, calls, failed_step, error, invalid, checkers[r],
                                  args.max_retries_per_problem)
            common.write_json_atomic(common.row_path(args.run_dir, r), rec)
            f = rec["final"]
            if f["status"] == "ok":
                note = f"{' > '.join(f['ordering'])} | top: {f['top_practice']}"
            else:
                note = (f"prompt {f['last_failed_step']}, {f['last_failure_kind']}: "
                        f"{f['last_failure_reason'].splitlines()[0]}")
            print(f"  row {r}: {f['status']} {note}", flush=True)
            if more:
                again.append(r)
            else:
                counts[f["status"]] += 1
        pending = sorted(again)
    return counts


def write_failed_list(run_dir):
    """Write runs/<prefix>/failed_problems.csv: every row of the run directory whose status is
    "failed" (all its attempts failed), with what failed in each attempt.
    Returns (number of rows, path)."""
    rows_dir = os.path.join(run_dir, "rows")
    out = []
    for name in sorted(os.listdir(rows_dir)) if os.path.isdir(rows_dir) else []:
        if not name.endswith(".json"):
            continue
        with open(os.path.join(rows_dir, name), encoding="utf-8") as f:
            rec = json.load(f)
        if rec["final"]["status"] != "failed":
            continue
        fails = [a for a in rec["attempts"] if a["failure_reason"]]
        out.append({
            "row": rec["row"], "problem_id": rec["problem_id"], "attempts": len(rec["attempts"]),
            "failed_steps": " | ".join(f"prompt {a['failed_step']}" for a in fails),
            "failure_kinds": " | ".join(a["failure_kind"] for a in fails),
            "last_failure_reason": rec["final"]["last_failure_reason"].splitlines()[0],
            "all_failure_reasons": " | ".join(a["failure_reason"].splitlines()[0] for a in fails),
        })
    path = os.path.join(run_dir, "failed_problems.csv")
    os.makedirs(run_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["row", "problem_id", "attempts", "failed_steps", "failure_kinds",
                                          "last_failure_reason", "all_failure_reasons"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    return len(out), path


def error_text(e):
    return f"{type(e).__name__}: {e}\n{traceback.format_exc(limit=3)}"


def run_problems(args, provider, prompts, problems, rows, checkers):
    """Run prompts 1, 2 and 3 for each row (1 and 3 with --no-ordering), each only after the answer before it
    passed. Yield (row, calls, failed_step, error, invalid); failed_step is 1, 2 or 3 when the attempt failed."""
    if args.provider == "local":
        yield from run_problems_local(provider, prompts, problems, rows, checkers,
                                      (1, 3) if args.no_ordering else (1, 2, 3))
        return

    def one(r):
        calls, ck, text = [], checkers[r], problems[r]["text"]
        step = 1
        try:
            rec = provider.call(prompts["system_1"], common.build_prompt1(prompts, text), 1, calls)
            problem = ck.check(1, rec["response_text"])
            if problem:
                return r, calls, 1, None, problem     # prompts 2 and 3 are never sent
            if not args.no_ordering:
                step = 2
                rec = provider.call(prompts["system_2"], common.build_prompt2(prompts, text, ck.parsed[0]), 2, calls)
                problem = ck.check(2, rec["response_text"])
                if problem:
                    return r, calls, 2, None, problem     # prompt 3 is never sent
            step = 3
            rec = provider.call(prompts["system_3"], common.build_prompt3(prompts, text, ck.combined), 3, calls)
            problem = ck.check(3, rec["response_text"])
            return r, calls, (3 if problem else None), None, problem
        except Exception as e:  # logged in the row file with the calls that finished; the run goes on
            return r, calls, step, error_text(e), None

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(one, r) for r in rows]
        for fut in as_completed(futures):
            yield fut.result()


def run_problems_local(provider, prompts, problems, rows, checkers, steps=(1, 2, 3)):
    """Batched version: prompt 1 for all rows, then prompt 2 for the rows whose answer 1 passed, then
    prompt 3 for the rows whose answer 2 passed (steps (1, 3): prompt 3 right after answer 1)."""
    calls = {r: [] for r in rows}
    build = {1: lambda r: common.build_prompt1(prompts, problems[r]["text"]),
             2: lambda r: common.build_prompt2(prompts, problems[r]["text"], checkers[r].parsed[0]),
             3: lambda r: common.build_prompt3(prompts, problems[r]["text"], checkers[r].combined)}
    todo = list(rows)
    for step in steps:
        reqs = [(r, prompts[f"system_{step}"], build[step](r), step) for r in todo]
        passed = []
        for r, rec, error in provider.call_many(reqs):
            calls[r].append(rec)
            if error:
                yield r, calls[r], step, error, None
                continue
            problem = checkers[r].check(step, rec["response_text"])
            if problem:
                yield r, calls[r], step, None, problem
            elif step == 3:
                yield r, calls[r], None, None, None
            else:
                passed.append(r)
        todo = passed


def main():
    args = parse_args()
    prompts = common.load_prompts(args.framework, args.chapter_file)
    problems = common.load_problems()
    rows = common.parse_rows(args.rows, len(problems))

    if args.dry_run:
        print(f"provider={args.provider} model={args.model} prefix={args.column_prefix} run_dir={args.run_dir} "
              f"framework={args.framework}")
        print("=" * 30, "SYSTEM PROMPT 1", "=" * 30)
        print(prompts["system_1"])
        print("=" * 30, "SYSTEM PROMPT 2", "=" * 30)
        print(prompts["system_2"])
        print("=" * 30, "SYSTEM PROMPT 3", "=" * 30)
        print(prompts["system_3"])
        for r in rows[:3]:
            text = problems[r]["text"]
            print("=" * 30, f"ROW {r} (problem_id {problems[r]['problem_id']}) USER PROMPT 1", "=" * 30)
            print(common.build_prompt1(prompts, text))
            print("=" * 30, f"ROW {r} USER PROMPT 2 (answer 1's practices used go where {{PRACTICES}} is)", "=" * 30)
            print(common.fill(prompts["q2_template"], PROBLEM=text, PRACTICES="{PRACTICES}"))
            print("=" * 30, f"ROW {r} USER PROMPT 3 (answer 1 in answer 2's order goes where {{ANALYSIS}} is)", "=" * 30)
            print(common.fill(prompts["q3_template"], PROBLEM=text, ANALYSIS="{ANALYSIS}"))
        return

    if not args.merge_only:
        from providers import PROVIDERS
        provider = PROVIDERS[args.provider](args)
        config = run_config(args, prompts, provider.describe())
        check_manifest(args, config)
        log_invocation(args, {"rows": args.rows or "all", "config": config,
                              "infra": provider.describe().get("infra"),
                              "environment": common.environment_info()})
        counts = generate(args, provider, prompts, problems, rows)
        print(f"Finished this invocation: {counts}", flush=True)

    n_failed, failed_path = write_failed_list(args.run_dir)
    print(f"{n_failed} problems in this run directory failed all their attempts; list: {failed_path}", flush=True)

    if not args.no_merge:
        res = common.merge_into_csv(args.run_dir, args.column_prefix, args.problems_csv,
                                    os.path.join(common.RUNS_DIR, "_csv_backups"), args.replace_columns)
        if res["replaced"]:
            print(f"Replaced {', '.join(res['replaced'])} with the {args.column_prefix}_* columns")
        print(f"Wrote {res['written']} rows to {', '.join(res['columns'])} in {args.problems_csv} "
              f"({res['skipped_unfinished']} rows not ok left out; backup: {res['backup']})")


if __name__ == "__main__":
    main()
