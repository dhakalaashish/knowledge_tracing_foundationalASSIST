"""v5 labels: students' common wrong answers first, then the problem's practices per skill (prompts 5 and 6 in
prompts.py). Every prompt is a fresh single-turn conversation; no call sees predicted_practice or an earlier run's
labels.

    Prompt 5, the main incorrect-answer prompt: one call per common wrong answer (given by at least --min-students
    students on their first attempt, without hints or answer views; Results/practice_analysis/common_wrong_answers.csv)
        system: prompts.SYSTEM_PROMPT_V5_WRONG (definitions and descriptors without examples, answer 5 format)
        user:   prompts.Q5_WRONG_TEMPLATE with the item, its correct answer, its skills and the wrong answer
        answer: the model's own solution (step, skill, practice), how the student produced the wrong answer, and
                the error: practice / math_fact / comprehension / stopped_early / unexplained, per skill as well
                when the item has two or more skills
    Prompt 6, the main problem prompt, sent once every wrong answer of the item has a valid answer 5
        system: prompts.SYSTEM_PROMPT_V5_PROBLEM (same definitions and descriptors, answer 6 format)
        user:   prompts.Q6_PROBLEM_EVIDENCE_TEMPLATE with the item, correct answer, skills and one line per diagnosed
                wrong answer (evidence_text), or prompts.Q6_PROBLEM_TEMPLATE when the item has no common wrong answer
        answer: the practices used per skill (one order across the item), the math facts, the practices not used,
                and the top practice (from the evidence, or by judgment)

Each answer is checked with a JSON parser and the format rules (common.check_v5_wrong, common.check_v5_problem). A
failed answer is asked again in a fresh conversation; each wrong answer and the problem prompt get at most
1 + --max-retries-per-problem attempts. A problem whose wrong answers or problem prompt fail every attempt is listed
in runs/<prefix>/failed_problems.csv.

Outputs
    Data/Problems.csv columns (or --problems-csv):
        <prefix>_reasoning               answer 6 as JSON, with a flat "practices_used" list (each practice once, in
                                         order of first use) so tools that read the earlier format keep working
        <prefix>_top_practice            answer 6's top_practice
        <prefix>_top_practice_reasoning  answer 6's top_practice_why
        <prefix>_skill_practices         e.g. "7.NS.A.3: REP > PF | 7.EE.B.4a: MOD > PF"
        <prefix>_math_facts              answer 6's math_facts as JSON
        <prefix>_evidence_used           yes / no: whether prompt 6 had the analysis of common wrong answers
    Data/wrong_answer_diagnosis_<prefix>.csv   one line per diagnosed wrong answer (or --diagnosis-out)
    runs/<prefix>/rows/row_NNNNN.json          every call, attempt and parsed answer of the row
    runs/<prefix>/manifest.json                settings and the full system prompts; other settings stop a later run

There is no separate order prompt and no separate top-practice prompt: prompt 6 gives the practices in order (per
skill, one order across the item) and the top practice in one answer. Both prompts use the descriptors-only
definitions (no example items, no NAEP Chapter 3).

By default only rows 1-300 (the first 300 problems) are run, to be checked before the full run; --rows all runs
every problem. A later --rows all resumes: rows already done are skipped.

Examples (from Code/generate_practice_reasoning):
    python3 label_v5.py --provider local --model Qwen/Qwen3.5-122B-A10B-FP8 --rows 1,65,260,2 --dry-run
    python3 label_v5.py --provider local --model Qwen/Qwen3-30B-A3B-Instruct-2507 --rows 1-15,127 \\
        --column-prefix qwen3_30b_v5_smoke --no-merge
    python3 label_v5.py --provider local --model Qwen/Qwen3.5-122B-A10B-FP8 --column-prefix qwen35_122b_v5 \\
        --max-model-len 131072 --enable-thinking true --max-tokens 32768 --temperature 0.6 --top-p 0.95   # rows 1-300
    python3 label_v5.py --provider local --column-prefix qwen35_122b_v5 --merge-only
"""

import argparse
import csv
import json
import os
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import common
import generate
import prompts as PR

DEFAULT_WRONG = os.path.join(common.REPO_ROOT, "Results", "practice_analysis", "common_wrong_answers.csv")
SUFFIXES = ["reasoning", "top_practice", "top_practice_reasoning", "skill_practices", "math_facts", "evidence_used"]
LOCKED_KEYS = ["provider", "model", "system_prompt_5_sha256", "system_prompt_6_sha256", "q5_template_sha256",
               "q6_template_sha256", "q6_evidence_template_sha256", "params", "min_students"]
SHORT = dict(zip(PR.PRACTICES, ["REP", "A&G", "J&P", "MOD", "COL", "PF"]))
OPEN = ("pending", "pending_retry")


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", required=True, choices=["anthropic", "openai", "gemini", "local"])
    ap.add_argument("--model", help="model id (default depends on --provider)")
    ap.add_argument("--rows", default="1-300",
                    help="data rows of Problems.csv, e.g. '1-300' or '1,65,260', or 'all' (default: 1-300, the "
                         "first 300 problems, to be checked before the full run)")
    ap.add_argument("--column-prefix", help="CSV column prefix and run folder name (default: <provider prefix>_v5)")
    ap.add_argument("--run-dir", help="log directory (default: runs/<prefix>)")
    ap.add_argument("--problems-csv", default=common.DEFAULT_PROBLEMS_CSV)
    ap.add_argument("--wrong-answers", default=DEFAULT_WRONG)
    ap.add_argument("--skills-csv", default=common.DEFAULT_SKILLS_CSV)
    ap.add_argument("--min-students", type=int, default=3,
                    help="a wrong answer is analyzed when at least this many students gave it (default 3)")
    ap.add_argument("--diagnosis-out", help="diagnosis CSV (default: Data/wrong_answer_diagnosis_<prefix>.csv)")
    ap.add_argument("--max-retries-per-problem", type=int, default=3,
                    help="each wrong answer and each problem prompt gets at most 1 + this many attempts")
    ap.add_argument("--retry-failed", action="store_true",
                    help="give the prompts that failed every attempt a fresh set of attempts (history kept)")
    ap.add_argument("--max-tokens", type=int, help="output token limit per call")
    ap.add_argument("--temperature", type=float, help="sampling temperature (OpenAI, Gemini, local)")
    ap.add_argument("--workers", type=int, default=8, help="parallel calls for API providers")
    ap.add_argument("--max-retries", type=int, default=8, help="API-level retries of one call (rate limits etc.)")
    ap.add_argument("--dry-run", action="store_true", help="print the prompts for the first selected rows and stop")
    ap.add_argument("--merge-only", action="store_true", help="skip the LLM; write the CSV outputs from the logs")
    ap.add_argument("--no-merge", action="store_true", help="do not touch the problems CSV after generating")
    ap.add_argument("--force", action="store_true", help="allow settings that differ from the run's manifest")
    generate.add_provider_args(ap)
    args = ap.parse_args()
    args.model = args.model or generate.DEFAULT_MODELS[args.provider]
    if args.rows and args.rows.strip().lower() == "all":
        args.rows = None                     # common.parse_rows: None means every row
    args.column_prefix = args.column_prefix or generate.DEFAULT_PREFIX[args.provider] + "_v5"
    args.run_dir = args.run_dir or os.path.join(common.RUNS_DIR, args.column_prefix)
    return args


# ---------------------------------------------------------------- data

def load_items(args):
    """row -> {row, problem_id, text, type, correct, skills, wrong: [...], wrong_total} for the selected rows."""
    common._raise_field_limit()
    texts = common.load_problems()
    with open(args.problems_csv, encoding="utf-8", newline="") as f:
        table = list(csv.reader(f))
    head, body = table[0], table[1:]
    h = {c: i for i, c in enumerate(head)}
    rows = common.parse_rows(args.rows, len(body))
    skills = common.load_skills(args.skills_csv)
    items = {}
    for row in rows:
        r = body[row - 1]
        pid = r[h["problem_id"]].strip()
        if str(texts[row]["problem_id"]).strip() != pid:
            sys.exit(f"row {row}: problem_id {pid} in {args.problems_csv}, {texts[row]['problem_id']} in problems_rendered.jsonl")
        ptype = r[h["Problem Type"]].strip()
        sk = skills.get(pid) or [{"code": "none", "name": "the item has no skill code"}]
        items[row] = {"row": row, "problem_id": pid, "text": texts[row]["text"], "type": ptype,
                      "correct": common.correct_answer(ptype, r[h["Multiple Choice Answers"]], r[h["Fill-in Answers"]]),
                      "skills": sk, "wrong": [], "wrong_total": 0}
    with open(args.wrong_answers, encoding="utf-8", newline="") as f:
        for w in csv.DictReader(f):
            row = int(w["row"])
            if row not in items or int(w["students"]) < args.min_students:
                continue
            it = items[row]
            if w["problem_id"].strip() != it["problem_id"]:
                sys.exit(f"row {row}: problem_id {it['problem_id']} in {args.problems_csv}, {w['problem_id']} in {args.wrong_answers}")
            it["wrong"].append({"key": f"r{row:05d}_w{int(w['rank']):03d}", "rank": int(w["rank"]),
                                "wrong_answer": w["wrong_answer"], "students": int(w["students"]),
                                "share": float(w["share_of_wrong"])})
            it["wrong_total"] = int(w["wrong_without_help"])
    for it in items.values():
        it["wrong"].sort(key=lambda x: x["rank"])
    return items


def codes(it):
    return [s["code"] for s in it["skills"]]


def build_prompt5(prompts, it, w):
    return common.fill(prompts["q5_template"], PROBLEM=it["text"], CORRECT=it["correct"],
                       SKILLS=common.skills_text(it["skills"]), WRONG=w["wrong_answer"], COUNT=str(w["students"]),
                       SHARE=f"{round(100 * w['share'])}%")


def _failure_text(a, prefix=""):
    et, fp = a.get("error_type") or a.get("outcome"), a.get("failed_practice", "")
    if et == "correct":
        return "correct"
    if et == "practice":
        return f"{prefix}practice error at {fp}"
    if et == "math_fact":
        return f"{prefix}math-fact error at {fp}: {a.get('math_fact', '').rstrip('.')}"
    if et == "comprehension":
        return f"{prefix}comprehension error: {a.get('comprehension', '').rstrip('.')}"
    if et == "stopped_early":
        return f"{prefix}stopped early, before {fp}"
    return f"{prefix}unexplained: no reasonable process gives this answer"


def _sentence(s):
    s = (s or "").strip()
    return s if not s or s[-1] in ".!?" else s + "."


def evidence_text(it, answers):
    """The {COVERAGE} and {EVIDENCE} of prompt 6: one line per diagnosed wrong answer, most students first.
    answers: wrong-answer key -> answer 5 (parsed)."""
    lines = []
    multi = len(it["skills"]) >= 2
    ws = sorted(it["wrong"], key=lambda w: (-w["students"], w["rank"]))
    for i, w in enumerate(ws, 1):
        a = answers[w["key"]]
        what = _failure_text(a)
        parts = [f"w{i}. “{w['wrong_answer']}”: {w['students']} students ({round(100 * w['share'])}% of the item's wrong "
                 f"answers). {what[:1].upper() + what[1:]}."]
        if a["error_type"] != "unexplained":
            parts.append(f"Student's process: {_sentence(a['student_process'])}")
        parts.append(f"Explanation: {_sentence(a['explanation'])}")
        if multi and a.get("by_skill"):
            parts.append("By skill: " + "; ".join(f"{b['skill']}: {_failure_text(b)}" for b in a["by_skill"]) + ".")
        lines.append(" ".join(parts))
    students = sum(w["students"] for w in it["wrong"])
    share = students / it["wrong_total"] if it["wrong_total"] else None
    n = len(it["wrong"])
    coverage = (f"{n} wrong answer{'s' if n != 1 else ''} given by {students} students"
                + (f", {round(100 * share)}% of the item's wrong first attempts without hints" if share is not None else ""))
    return coverage, "\n".join(lines)


def build_prompt6(prompts, it, answers):
    base = dict(PROBLEM=it["text"], CORRECT=it["correct"], SKILLS=common.skills_text(it["skills"]))
    if not it["wrong"]:
        return common.fill(prompts["q6_template"], **base)
    coverage, evidence = evidence_text(it, answers)
    return common.fill(prompts["q6_evidence_template"], COVERAGE=coverage, EVIDENCE=evidence, **base)


# ---------------------------------------------------------------- run settings and logs

def run_config(args, prompts, provider_desc):
    sha = common.sha256
    return {
        "provider": args.provider, "model": args.model, "column_prefix": args.column_prefix, "framework": "v5",
        "system_prompt_5": prompts["system_5"], "system_prompt_5_sha256": sha(prompts["system_5"]),
        "system_prompt_6": prompts["system_6"], "system_prompt_6_sha256": sha(prompts["system_6"]),
        "q5_template": prompts["q5_template"], "q5_template_sha256": sha(prompts["q5_template"]),
        "q6_template": prompts["q6_template"], "q6_template_sha256": sha(prompts["q6_template"]),
        "q6_evidence_template": prompts["q6_evidence_template"],
        "q6_evidence_template_sha256": sha(prompts["q6_evidence_template"]),
        "params": provider_desc["params"], "min_students": args.min_students,
        "max_retries_per_problem": args.max_retries_per_problem,
        "problems_file": os.path.relpath(common.RENDERED_JSONL, common.HERE),
        "problems_file_sha256": sha(common.read_text(common.RENDERED_JSONL)),
        "wrong_answers_file": os.path.relpath(args.wrong_answers, common.REPO_ROOT),
        "wrong_answers_sha256": sha(common.read_text(args.wrong_answers)),
        "skills_file": os.path.relpath(args.skills_csv, common.REPO_ROOT),
        "skills_sha256": sha(common.read_text(args.skills_csv)),
        "answer_check": "each answer must parse as one JSON object (optionally inside one ```json fence) and follow "
                        "prompts.RESPONSE_V5_WRONG / RESPONSE_V5_PROBLEM (common.check_v5_wrong, check_v5_problem); "
                        "prompt 6 is sent only after every wrong answer of the item passed",
        "output_columns": [f"{args.column_prefix}_{s}" for s in SUFFIXES],
    }


def check_manifest(args, config):
    """Record the run settings once; refuse to mix different settings in one run directory."""
    path = os.path.join(args.run_dir, "manifest.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
        diff = [k for k in LOCKED_KEYS if old["config"].get(k) != config.get(k)]
        if diff and not args.force:
            sys.exit(f"Settings differ from {path} in: {', '.join(diff)}.\n"
                     f"Use another --column-prefix (new columns), or --force to continue anyway.")
        if diff:
            old.setdefault("config_changes", []).append({"at": common.now(), "changed": diff, "config": config})
            common.write_json_atomic(path, old)
        return
    common.write_json_atomic(path, {"created_at": common.now(), "config": config,
                                    "environment": common.environment_info()})


def new_part():
    return {"attempts": [], "final": {"status": "pending"}}


def new_record(args, it, prompts, provider_desc):
    rec = {"row": it["row"], "problem_id": it["problem_id"], "problem_text": it["text"], "problem_type": it["type"],
           "correct": it["correct"], "skills": it["skills"], "provider": args.provider, "model": args.model,
           "column_prefix": args.column_prefix, "system_prompt_5_sha256": common.sha256(prompts["system_5"]),
           "system_prompt_6_sha256": common.sha256(prompts["system_6"]), "generation_params": provider_desc["params"],
           "wrong": {}, "problem": new_part(), "final": {"status": "pending"}}
    for w in it["wrong"]:
        rec["wrong"][w["key"]] = {**w, **new_part()}
    return rec


def reopen(part):
    """--retry-failed: a part that failed every attempt gets a fresh budget; its attempts are kept."""
    if part["final"]["status"] == "failed":
        part["earlier_failed_attempts"] = part.get("earlier_failed_attempts", []) + part["attempts"]
        part["attempts"], part["final"] = [], {"status": "pending"}


def add_attempt(part, call, error, invalid, parsed, how, max_retries, ok_extra):
    """Record one attempt of a part (one wrong answer, or the problem prompt) and set its status."""
    reason = error or invalid
    part["attempts"].append({"attempt": len(part["attempts"]) + 1, "call": call,
                             "failure_kind": ("error" if error else "invalid_answer") if reason else None,
                             "failure_reason": reason, "parsed": parsed, "json_extraction": how})
    if reason is None:
        part["final"] = {"status": "ok", "attempt": len(part["attempts"]), "answer": call["response_text"],
                         "answer_json": parsed, **ok_extra}
        return
    n_failed = sum(1 for a in part["attempts"] if a["failure_reason"])
    part["final"] = {"status": "pending_retry" if n_failed <= max_retries else "failed", "failed_attempts": n_failed,
                     "last_failure_kind": part["attempts"][-1]["failure_kind"], "last_failure_reason": reason}


def settle(rec):
    """The row's status from its parts."""
    bad = [k for k, w in rec["wrong"].items() if w["final"]["status"] == "failed"]
    if bad:
        rec["final"] = {"status": "failed", "stage": "wrong answer " + ", ".join(bad),
                        "last_failure_reason": rec["wrong"][bad[0]]["final"]["last_failure_reason"]}
    elif rec["problem"]["final"]["status"] == "failed":
        rec["final"] = {"status": "failed", "stage": "problem prompt",
                        "last_failure_reason": rec["problem"]["final"]["last_failure_reason"]}
    elif rec["problem"]["final"]["status"] == "ok":
        f = rec["problem"]["final"]
        rec["final"] = {"status": "ok", "ordering": f["derived"]["ordering"], "top_practice": f["answer_json"]["top_practice"],
                        "top_practice_basis": f["answer_json"]["top_practice_basis"], "evidence_used": f["evidence_used"]}
    else:
        rec["final"] = {"status": "pending"}


# ---------------------------------------------------------------- calls

def call_batch(args, provider, reqs):
    """reqs: [(key, system, prompt, step)] -> [(key, call record or None, error or None)]."""
    if args.provider == "local":
        return provider.call_many(reqs)

    def one(req):
        key, system, prompt, step = req
        calls = []
        try:
            provider.call(system, prompt, step, calls)
            return key, calls[-1], None
        except Exception as e:
            return key, (calls[-1] if calls else None), f"{type(e).__name__}: {e}\n{traceback.format_exc(limit=3)}"

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        return [fut.result() for fut in as_completed([ex.submit(one, q) for q in reqs])]


def run_chunk(args, provider, prompts, items, records, chunk):
    """All prompt-5 calls of the chunk's rows (rounds until each is ok or failed), then prompt 6 for the rows whose
    wrong answers all passed (rounds again). Row files are written after every round."""
    mr = args.max_retries_per_problem
    where = {}
    while True:   # prompt 5
        todo = [(r, k) for r in chunk for k, w in records[r]["wrong"].items() if w["final"]["status"] in OPEN]
        if not todo:
            break
        if hasattr(provider, "attempt_of"):
            provider.attempt_of = {k: len(records[r]["wrong"][k]["attempts"]) for r, k in todo}
        wdef = {w["key"]: w for r in chunk for w in items[r]["wrong"]}
        where = {k: r for r, k in todo}
        reqs = [(k, prompts["system_5"], build_prompt5(prompts, items[r], wdef[k]), 5) for r, k in todo]
        for key, call, error in call_batch(args, provider, reqs):
            r = where[key]
            part = records[r]["wrong"][key]
            invalid = parsed = how = fp = None
            if not error:
                try:
                    parsed, how = common.parse_json_answer(call["response_text"])
                    fp = common.check_v5_wrong(parsed, codes(items[r]))
                except ValueError as e:
                    invalid, parsed = f"answer 5: {e}", None
            add_attempt(part, call, error, invalid, parsed, how, mr, {"failed_practice": fp})
        for r in sorted({r for r, _ in todo}):
            common.write_json_atomic(common.row_path(args.run_dir, r), records[r])
    while True:   # prompt 6
        ready = [r for r in chunk if records[r]["problem"]["final"]["status"] in OPEN
                 and all(w["final"]["status"] == "ok" for w in records[r]["wrong"].values())]
        if not ready:
            break
        if hasattr(provider, "attempt_of"):
            provider.attempt_of = {f"r{r:05d}_p": len(records[r]["problem"]["attempts"]) for r in ready}
        answers = {r: {k: w["final"]["answer_json"] for k, w in records[r]["wrong"].items()} for r in ready}
        prompt6 = {r: build_prompt6(prompts, items[r], answers[r]) for r in ready}
        reqs = [(f"r{r:05d}_p", prompts["system_6"], prompt6[r], 6) for r in ready]
        for key, call, error in call_batch(args, provider, reqs):
            r = int(key[1:6])
            has_ev = bool(items[r]["wrong"])
            invalid = parsed = how = derived = None
            if not error:
                try:
                    parsed, how = common.parse_json_answer(call["response_text"])
                    derived = common.check_v5_problem(parsed, codes(items[r]), has_ev)
                except ValueError as e:
                    invalid, parsed = f"answer 6: {e}", None
            add_attempt(records[r]["problem"], call, error, invalid, parsed, how, mr,
                        {"derived": derived, "evidence_used": has_ev})
        for r in ready:
            common.write_json_atomic(common.row_path(args.run_dir, r), records[r])


def run(args, provider, prompts, items):
    desc = provider.describe()
    records = {}
    for r, it in items.items():
        old = common.load_row(args.run_dir, r)
        if old:
            for w in it["wrong"]:              # a wrong answer added to the input since the row was started
                old["wrong"].setdefault(w["key"], {**w, **new_part()})
            if args.retry_failed:
                for part in [*old["wrong"].values(), old["problem"]]:
                    reopen(part)
            settle(old)
            if old["final"]["status"] in ("ok", "failed"):
                continue
            records[r] = old
        else:
            records[r] = new_record(args, it, prompts, desc)
    n_wrong = sum(len(items[r]["wrong"]) for r in records)
    print(f"{len(items) - len(records)} of {len(items)} rows already done (ok or failed); {len(records)} to run, "
          f"with {n_wrong} wrong answers to diagnose. Each prompt gets up to {1 + args.max_retries_per_problem} attempts.",
          flush=True)
    counts = {"ok": 0, "failed": 0}
    progress = common.Progress(len(items), len(items) - len(records), len(records), "problems")
    pending = sorted(records)
    size = max(1, getattr(provider, "batch_size", 0) or 4 * args.workers)
    for start in range(0, len(pending), size):
        chunk = pending[start:start + size]
        run_chunk(args, provider, prompts, items, records, chunk)
        for r in chunk:
            rec = records[r]
            settle(rec)
            common.write_json_atomic(common.row_path(args.run_dir, r), rec)
            f = rec["final"]
            if f["status"] == "ok":
                note = (f"{' > '.join(SHORT[p] for p in f['ordering'])} | top: {f['top_practice']} ({f['top_practice_basis']})"
                        f" | evidence: {len(rec['wrong'])} wrong answers")
            else:
                note = f"{f.get('stage')}: {str(f.get('last_failure_reason', '')).splitlines()[0] if f.get('last_failure_reason') else ''}"
            print(f"  row {r}: {f['status']} {note}", flush=True)
            counts[f["status"]] = counts.get(f["status"], 0) + 1
            progress.add()
        progress.report(f" (rows {chunk[0]}-{chunk[-1]} done)")
    progress.stop()
    return counts


# ---------------------------------------------------------------- outputs

def load_records(run_dir):
    rows_dir = os.path.join(run_dir, "rows")
    out = []
    for name in sorted(os.listdir(rows_dir)) if os.path.isdir(rows_dir) else []:
        if name.endswith(".json"):
            with open(os.path.join(rows_dir, name), encoding="utf-8") as f:
                out.append(json.load(f))
    return out


def csv_values(rec):
    f = rec["problem"]["final"]
    a, d = f["answer_json"], f["derived"]
    reasoning = {"practices_used": d["practices_used"], "practices_not_used": a["practices_not_used"],
                 "skills": a["skills"], "math_facts": a.get("math_facts", []),
                 "top_practice_basis": a["top_practice_basis"], "comprehension_note": a.get("comprehension_note", ""),
                 "evidence_used": f["evidence_used"]}
    per_skill = " | ".join(f"{code}: {' > '.join(SHORT[p] for p in names) or '(not exercised)'}"
                           for code, names in d["skill_practices"].items())
    return [json.dumps(reasoning, ensure_ascii=False), a["top_practice"], a["top_practice_why"], per_skill,
            json.dumps(a.get("math_facts", []), ensure_ascii=False), "yes" if f["evidence_used"] else "no"]


def write_outputs(args):
    recs = load_records(args.run_dir)
    # failed list
    failed = [r for r in recs if r["final"].get("status") == "failed"]
    fpath = os.path.join(args.run_dir, "failed_problems.csv")
    os.makedirs(args.run_dir, exist_ok=True)
    with open(fpath, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["row", "problem_id", "stage", "last_failure_reason"])
        for r in failed:
            w.writerow([r["row"], r["problem_id"], r["final"].get("stage", ""),
                        str(r["final"].get("last_failure_reason", "")).splitlines()[0] if r["final"].get("last_failure_reason") else ""])
    print(f"{len(failed)} problems failed all attempts of a prompt; list: {fpath}", flush=True)
    # diagnoses (every wrong answer with a valid answer 5, also on rows whose problem prompt is not done)
    out = args.diagnosis_out or os.path.join(common.REPO_ROOT, "Data", f"wrong_answer_diagnosis_{args.column_prefix}.csv")
    head = ["row", "problem_id", "problem_type", "rank", "wrong_answer", "students", "share_of_wrong", "practice_prefix",
            "error_type", "failed_practice", "math_fact", "comprehension", "reconstruction", "explanation", "confidence",
            "solution", "by_skill", "diagnosis_json", "diagnosed_by"]
    n = 0
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        for rec in sorted(recs, key=lambda r: r["row"]):
            for key in sorted(rec["wrong"]):
                part = rec["wrong"][key]
                if part["final"]["status"] != "ok":
                    continue
                a = part["final"]["answer_json"]
                sol = " > ".join(f"{s['skill']}: {s['practice']}" for s in a["solution"])
                by = " | ".join(f"{b['skill']}: {_failure_text(b)}" for b in a.get("by_skill") or [])
                w.writerow([rec["row"], rec["problem_id"], rec["problem_type"], part["rank"], part["wrong_answer"],
                            part["students"], part["share"], args.column_prefix, a["error_type"],
                            a.get("failed_practice", ""), a.get("math_fact", ""), a.get("comprehension", ""),
                            a["student_process"], a["explanation"], a["confidence"], sol, by,
                            json.dumps(a, ensure_ascii=False), args.column_prefix])
                n += 1
    print(f"Wrote {n} diagnosed wrong answers to {out}", flush=True)
    if args.no_merge:
        return
    values = {r["row"]: (r["problem_id"], csv_values(r)) for r in recs if r["final"].get("status") == "ok"}
    res = common.write_columns(args.problems_csv, os.path.join(common.RUNS_DIR, "_csv_backups"),
                               args.column_prefix, SUFFIXES, values)
    print(f"Wrote {res['written']} rows to {', '.join(res['columns'])} in {args.problems_csv} (backup: {res['backup']})",
          flush=True)


# ---------------------------------------------------------------- main

def main():
    args = parse_args()
    prompts = PR.v5_prompts()
    if args.merge_only:
        write_outputs(args)
        return
    items = load_items(args)
    n_wrong = sum(len(it["wrong"]) for it in items.values())
    print(f"{len(items)} rows; {sum(1 for it in items.values() if it['wrong'])} with common wrong answers "
          f"(>= {args.min_students} students), {n_wrong} wrong answers in all", flush=True)
    if args.dry_run:
        print(f"provider={args.provider} model={args.model} prefix={args.column_prefix} run_dir={args.run_dir}")
        print("=" * 30, "SYSTEM PROMPT 5 (main incorrect-answer prompt)", "=" * 30)
        print(prompts["system_5"])
        print("=" * 30, "SYSTEM PROMPT 6 (main problem prompt)", "=" * 30)
        print(prompts["system_6"])
        for r in sorted(items)[:4]:
            it = items[r]
            if it["wrong"]:
                print("=" * 30, f"ROW {r} USER PROMPT 5 ({it['wrong'][0]['key']}; {len(it['wrong'])} wrong answers in all)", "=" * 30)
                print(build_prompt5(prompts, it, it["wrong"][0]))
                print("=" * 30, f"ROW {r} USER PROMPT 6 (with evidence; one line per diagnosed wrong answer goes where "
                      f"{{EVIDENCE}} is)", "=" * 30)
                coverage, _ = evidence_text(it, {w["key"]: {"error_type": "unexplained", "student_process": "",
                                                            "explanation": "", "by_skill": []} for w in it["wrong"]})
                print(common.fill(prompts["q6_evidence_template"], PROBLEM=it["text"], CORRECT=it["correct"],
                                  SKILLS=common.skills_text(it["skills"]), COVERAGE=coverage, EVIDENCE="{EVIDENCE}"))
            else:
                print("=" * 30, f"ROW {r} USER PROMPT 6 (no common wrong answers)", "=" * 30)
                print(build_prompt6(prompts, it, {}))
        return
    from providers import PROVIDERS
    provider = PROVIDERS[args.provider](args)
    config = run_config(args, prompts, provider.describe())
    check_manifest(args, config)
    generate.log_invocation(args, {"rows": args.rows or "all", "config": config,
                                   "infra": provider.describe().get("infra"), "environment": common.environment_info()})
    counts = run(args, provider, prompts, items)
    print(f"Finished this invocation: {counts}", flush=True)
    write_outputs(args)


if __name__ == "__main__":
    main()
