#!/usr/bin/env python3
"""
FoundationalASSIST knowledge tracing (Task 1) and cognitive student modeling (Task 2) on N random paper
students, run two ways with the same model, so the only difference is the practice information:

  baseline  the paper's prompts, unchanged (kt_inference_base.py, data staged by qwen3_30b_benchmark.py so the
            prompts equal the published ones; check with `check-prompts`)
  practice  the same prompts, plus
              - for every past problem: the practices a student needs, in order, each with its reason, and the top
                practice (Qwen3.5-122B, descriptors-only prompts: Problems.csv qwen35_122b_noex_*), and an analysis
                of the student's answer:
                  correct                       -> the student carried out every practice step correctly
                  wrong, a common wrong answer   -> its diagnosis (step 6, Chapter 3 run: kind of error, failed
                                                    practice, math fact, how students most likely got it)
                  wrong, any other answer        -> an uncommon answer, no diagnosis
                  wrong after a hint / answer view -> said so, no diagnosis (the logged text is unreliable)
              - for the problem to predict: only the practices it needs, in order
              - in the system prompt: the six practices' definitions and descriptors (as in the labeling prompts)
            The added text sits right after each problem's "Skill: Undefined" line; everything else is the
            paper's prompt.
  profile   the history replaced by a student profile that rules update after every answer, plus the last 10
            answers in full and the new problem with its skill, prerequisites, practices and difficulty
            (kt_student_profile.py; deck step 3)

Both use Qwen3-Next-80B-A3B-Instruct in 4-bit AWQ (qwen3next80b_awq_instruct_vllm.py; fits one A100 80 GB)
with the paper's generation settings. `evaluate` also scores the paper's own published Qwen3-Next-80B-Instruct
(BF16) predictions for the same students, as a reference.

Subcommands (from the Code/ directory):
    pick-users      Choose --n random paper students (seed --seed) whose released data reproduces the paper's
                    prompts; writes <out>/user_ids.txt
    stage           Stage their data (as qwen3_30b_benchmark.py stage-kt)
    check-prompts   Baseline: identical to the published prompts? Practice: identical once the added lines are
                    removed?
    show-prompt     Print one prompt (--condition practice|profile, --which first|longest) to read it
    check-length    Longest prompt of --condition in tokens, against --max-model-len
    infer-baseline  Run the baseline (GPU, timed)
    infer-practice  Run the practice version (GPU, timed)
    infer-profile   Run the profile version (GPU, timed)
    evaluate        Tables for paper reference / baseline / practice / profile, and the paired comparisons
    all             pick-users -> stage -> check-length -> infer-baseline -> infer-practice -> evaluate
    profile-all     stage -> check-length (profile) -> infer-profile -> evaluate

Usage:
    # quick test: 3 of the 50 students, both conditions
    VLLM_USE_FLASHINFER_SAMPLER=0 python3 kt_practice_benchmark.py all --students 3 --max-model-len 196608
    # the 50 students
    VLLM_USE_FLASHINFER_SAMPLER=0 nohup python3 kt_practice_benchmark.py all --max-model-len 196608 > kt50.log 2>&1 &
"""

import argparse
import csv
import json
import math
import os
import random
import re
import sys

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(CODE_DIR)
sys.path.insert(0, CODE_DIR)
sys.path.insert(0, os.path.join(CODE_DIR, "generate_practice_reasoning"))

import qwen3_30b_benchmark as B  # noqa: E402
import prompts as PR  # noqa: E402  (generate_practice_reasoning/prompts.py: the practice definitions and descriptors)

THIS_FILE = os.path.abspath(__file__)
MODEL_SCRIPT = "qwen3next80b_awq_instruct_vllm.py"
DEFAULT_OUT = os.path.join(REPO_DIR, "Results", "kt_practice_random50")
LABEL_PREFIX = "qwen35_122b_noex"
DIAG_CSV = os.path.join(REPO_DIR, "Data", "wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv")
PAPER_MEMBER = "inference_data_kt_results/qwen3next80binstruct_n500_bin10_hist50.jsonl"
OUTPUT_HEADROOM_TOKENS = 4096
ADDED_PREFIXES = ("Practices (in order", "  ", "Top practice: ", "Answer analysis: ", "Practices required")

# ---------------------------------------------------------------------------------------------- practice text

PRACTICE_DEFINITIONS = "".join(PR._without_examples(block, blank_line=True) for block in (
    PR.PROMPT_REPRESENTING, PR.PROMPT_ABSTRACTING, PR.PROMPT_JUSTIFYING, PR.PROMPT_MODELING,
    PR.PROMPT_COLLABORATIVE, PR.PROMPT_PROCEDURAL)).rstrip()

PRACTICE_SECTION = (
    "\n\n---\n\nMathematical Practices:\n\n"
    "Every problem below also lists the mathematical practices a student needs to solve it, in the order a student "
    "uses them, each with the reason, and its top practice (the step where the problem's difficulty lies). Each past "
    "problem also has an \"Answer analysis\" of this student's first answer: correct (every practice step done "
    "correctly); a common wrong answer, with the step or math fact that went wrong and how students most likely "
    "arrived at it; an uncommon wrong answer with no diagnosis; or a wrong answer given after a hint or after seeing "
    "the answer. The new problem lists only the practices it needs. Use this information about the practices, "
    "together with the rest of the student's record, to predict how the student will do. The six practices, with "
    "their definitions and descriptors:\n"
    + PRACTICE_DEFINITIONS
)


def one_line(text):
    return " ".join(str(text or "").split())


# Normalization of answers, as Code/practice_analysis/wrong_answers.js built the common wrong answers
def norm_answer(a):
    a = re.sub(r"<[^>]+>", " ", str(a or ""))
    for old, new in (("&nbsp;", " "), ("&gt;", ">"), ("&lt;", "<"), ("&amp;", "&"), ("&#39;", "'"), ("&quot;", '"')):
        a = a.replace(old, new)
    return re.sub(r"\s+", " ", a).strip().lower()


def num_val(t):
    t = re.sub(r"\s+", " ", t.replace(",", "")).strip()
    m = re.match(r"^(-?)(\d+) (\d+)/(\d+)$", t)
    if m:
        return (-1 if m.group(1) else 1) * (int(m.group(2)) + int(m.group(3)) / int(m.group(4))) if int(m.group(4)) else None
    m = re.match(r"^(-?\d*\.?\d+)/(-?\d*\.?\d+)$", t)
    if m:
        return float(m.group(1)) / float(m.group(2)) if float(m.group(2)) else None
    if re.match(r"^-?\d*\.?\d+$", t):
        return float(t)
    return None


def answer_key(a):
    v = num_val(a)
    return "t:" + re.sub(r"\s+", "", a) if v is None else "n:" + repr(round(v * 1e9) / 1e9)


def used_help(rec):
    """The student asked for a hint or saw the answer on this interaction."""
    hint = rec.get("hint_count")
    saw = str(rec.get("saw_answer")).strip().lower() in ("true", "1", "1.0")
    return saw or (hint is not None and str(hint) not in ("", "nan") and float(hint) > 0)


class PracticeInfo:
    """The labels, diagnoses and original answers the practice prompts need."""

    def __init__(self, kt_data_dir):
        B.csv.field_size_limit(sys.maxsize)
        self.practices, self.top = {}, {}
        with open(os.path.join(B.DATA_DIR, "Problems.csv"), newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                pid = int(r["problem_id"])
                if pid in self.practices:
                    continue
                try:
                    used = json.loads(r[f"{LABEL_PREFIX}_reasoning"])["practices_used"]
                except (KeyError, ValueError, TypeError):
                    continue
                self.practices[pid] = [(u["practice"], one_line(u.get("why"))) for u in sorted(used, key=lambda u: u["order"])]
                self.top[pid] = (r.get(f"{LABEL_PREFIX}_top_practice") or "").strip()
        self.diag = {}
        with open(DIAG_CSV, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                self.diag[(int(r["problem_id"]), answer_key(norm_answer(r["wrong_answer"])))] = r
        self.answer = {}   # interaction id -> the answer as the student entered it (MC: option text, not a letter)
        with open(os.path.join(kt_data_dir, "Interactions.csv"), newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                self.answer[str(r["id"])] = r.get("answer_text") or ""
        self.counts = {"correct": 0, "help": 0, "common": 0, "uncommon": 0, "unlabeled": 0}

    def block(self, pid):
        if pid not in self.practices:
            self.counts["unlabeled"] += 1
            return "Practices (in order, with why): not labeled"
        lines = ["Practices (in order, with why):"]
        lines += [f"  {i}. {p}: {why}" for i, (p, why) in enumerate(self.practices[pid], 1)]
        if self.top.get(pid):
            lines.append(f"Top practice: {self.top[pid]}")
        return "\n".join(lines)

    def required(self, pid):
        if pid not in self.practices:
            return "Practices required (in order): not labeled"
        return "Practices required (in order): " + " > ".join(p for p, _ in self.practices[pid])

    def classify(self, rec):
        """(kind, diagnosis row): kind is correct | help (wrong after a hint or the answer) | common (a diagnosed
        common wrong answer; the row is its diagnosis) | uncommon."""
        if float(rec.get("discrete_score") or 0) >= 1:
            return "correct", None
        if used_help(rec):
            return "help", None
        pid = int(rec["problem_id"])
        d = self.diag.get((pid, answer_key(norm_answer(self.answer.get(str(rec.get("id")), "")))))
        return ("uncommon", None) if d is None else ("common", d)

    def analysis(self, rec):
        kind, d = self.classify(rec)
        self.counts[kind] += 1
        if kind == "correct":
            return "Answer analysis: Correct: the student carried out every practice step correctly."
        if kind == "help":
            return ("Answer analysis: Incorrect, given after asking for a hint or seeing the answer "
                    "(no diagnosis: the recorded answer may not be the student's own).")
        if kind == "uncommon":
            return "Answer analysis: Incorrect: an uncommon answer (no diagnosis available)."
        et, fp, fact = d["error_type"], d["failed_practice"], one_line(d["math_fact"])
        if et == "practice":
            what = f"the {fp} step went wrong"
        elif et == "math_fact":
            what = f"a wrong or missing math fact at the {fp} step: {fact.rstrip('.')}"
        else:
            what = "no reasonable process gives this answer (a guess)"
        return (f"Answer analysis: Incorrect: a common wrong answer (given by {d['students']} students). Error: {what}. "
                f"How students most likely got it: {one_line(d['reconstruction'])}. {one_line(d['explanation'])}")


# The paper's code builds each student's prompts in make_process_single_user, which calls the module-level
# create_user_prompt. The practice version wraps both: the wrapper keeps the student's records, and the new
# create_user_prompt appends the practice text to each problem's skill name (printed as "Skill: <name>"), so the
# paper's function writes it right after "Skill: Undefined". History item i is the student's record i.
INFO = None
CURRENT_RECORDS = None


def install_practice(kt, kt_data_dir):
    global INFO
    INFO = PracticeInfo(kt_data_dir)
    if getattr(kt, "_practice_installed", False):   # wrap the paper's functions only once per process
        return
    kt._practice_installed = True
    original_create, original_make = kt.create_user_prompt, kt.make_process_single_user

    def find_target(new_problem, start):
        for rec in CURRENT_RECORDS[start:]:
            if str(rec.get("end_time")) == str(new_problem.get("timestamp")) and rec.get("cleaned body") == new_problem.get("problem_text"):
                return rec
        raise RuntimeError(f"target problem not found in the student's records: {new_problem.get('timestamp')}")

    def create_with_practice(student_history, new_problem, problem_df):
        history = []
        for i, item in enumerate(student_history):
            rec = CURRENT_RECORDS[i]
            if str(rec.get("end_time")) != str(item.get("timestamp")):
                raise RuntimeError("history and records out of step")
            pid = int(rec["problem_id"])
            history.append({**item, "node_name": f"{item.get('node_name') or 'Undefined'}\n{INFO.block(pid)}\n{INFO.analysis(rec)}"})
        target = find_target(new_problem, len(student_history))
        new = {**new_problem, "node_name": f"{new_problem.get('node_name') or 'Undefined'}\n{INFO.required(int(target['problem_id']))}"}
        return original_create(history, new, problem_df)

    def make_with_practice(system_prompt):
        inner = original_make(system_prompt)

        def process(args):
            global CURRENT_RECORDS
            CURRENT_RECORDS = args[1]
            return inner(args)
        return process

    kt.create_user_prompt = create_with_practice
    kt.make_process_single_user = make_with_practice
    kt.BASE_SYSTEM_PROMPT = kt.BASE_SYSTEM_PROMPT + PRACTICE_SECTION


def strip_added(prompt):
    """The practice prompt without the added text: equal to the paper's prompt if nothing else changed."""
    prompt = prompt.replace(PRACTICE_SECTION, "")
    out, in_added = [], False
    for line in prompt.split("\n"):
        if line.startswith("Skill: "):
            out.append(line)
            in_added = True
            continue
        if in_added and line.startswith(ADDED_PREFIXES):
            continue
        in_added = False
        out.append(line)
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------- setup

def b_args(args, command="stage-kt"):
    """Arguments for qwen3_30b_benchmark's functions: this run's students and folder."""
    argv = [command, "--user-ids-file", user_file(args), "--out-dir", args.out_dir, "--num-gpus", str(args.num_gpus),
            "--gpu-memory-utilization", str(args.gpu_memory_utilization), "--no-ped"]
    for flag, value in (("--max-model-len", args.max_model_len), ("--batch-size", args.batch_size),
                        ("--max-num-seqs", args.max_num_seqs), ("--cache-dir", args.cache_dir)):
        if value:
            argv += [flag, str(value)]
    if args.students:
        argv += ["--students", str(args.students)]
    return B.resolve_defaults(B.build_parser(B.COMMANDS).parse_args(argv), out_dir=args.out_dir)


def user_file(args):
    """The picked students, kept in the main folder (a --students test uses the first N of the same list)."""
    return os.path.join(args.base_dir, "user_ids.txt")


def diverged_users(users):
    """Paper users whose released interactions no longer line up with their published prompts."""
    seqs = B.interaction_sequences(os.path.join(B.DATA_DIR, "Interactions.csv"), os.path.join(B.DATA_DIR, "Problems.csv"), users)
    longest = {}
    for line in B.iter_lines(f"{B.PAPER_ZIP}::{B.PAPER_REF_MEMBER}"):
        u = B.line_user_id(line)
        if u not in seqs:
            continue
        r = json.loads(line)
        if r["history_size"] > longest.get(u, (0, None))[0]:
            longest[u] = (r["history_size"], r["prompt"].rsplit("**New Problem to Predict:**", 1)[0])
    bad = set(users) - set(longest)
    for u, (_, head) in longest.items():
        stamps = re.findall(r"^Timestamp: (.*)$", head.split("**Student's Previous Problems:**", 1)[1], re.MULTILINE)
        if any(end != ts for (_, end), ts in zip(seqs[u], stamps)):
            bad.add(u)
    return bad


def cmd_pick_users(args):
    """The first --n students of one fixed random order of the eligible paper students (seed --seed). The picks are
    nested: a larger --n in the same folder keeps the students already there and adds the next ones, so the
    results already computed are kept and only the new students are run (e.g. 170 now, all 490 later)."""
    existing = B.read_user_ids(user_file(args)) if os.path.exists(user_file(args)) else []
    if existing and len(existing) >= args.n and not args.force:
        if len(existing) > args.n:
            print(f"NOTE: {user_file(args)} has {len(existing)} students, more than --n {args.n}; all are used "
                  f"(--force to pick a new, smaller list)")
        print(f"Using the {len(existing)} students in {user_file(args)}")
        return
    # the paper's 500 users (cached in Results/paper_reference); our own list may not exist yet, so the
    # benchmark's arguments here carry no --user-ids-file
    paper_ids = os.path.join(B.PAPER_REF_DIR, "paper_user_ids.txt")
    if not os.path.exists(paper_ids):
        B.cmd_extract_users(B.resolve_defaults(B.build_parser(B.COMMANDS).parse_args(
            ["extract-users", "--out-dir", args.out_dir, "--no-ped"]), out_dir=args.out_dir))
    users = B.read_user_ids(paper_ids)
    print(f"Checking which of the paper's {len(users)} students still match their published prompts ...")
    bad = diverged_users(users)
    order = sorted(set(users) - bad)
    random.Random(args.seed).shuffle(order)
    n = min(args.n, len(order))
    if n < args.n:
        print(f"Only {len(order)} students are eligible: using all of them")
    if existing and not args.force:
        have = set(existing)
        chosen = existing + [u for u in order if u not in have][:n - len(existing)]
        print(f"Adding {len(chosen) - len(existing)} students to the {len(existing)} already in the list")
    else:
        chosen = order[:n]
    os.makedirs(args.base_dir, exist_ok=True)
    with open(user_file(args), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(chosen)) + "\n")
    # the staged data must be rebuilt to hold the new students (results already computed are kept)
    marker = os.path.join(args.out_dir, "kt_data", B.STAGED_MARKER)
    if os.path.exists(marker):
        os.remove(marker)
    print(f"{len(bad)} students left out (data no longer matches); {len(chosen)} of {len(order)} picked "
          f"with seed {args.seed}: {user_file(args)}")


def cmd_stage(args):
    cmd_pick_users(args)
    ba = b_args(args)
    if not B.is_staged(B.paths(ba)):
        B.cmd_stage_kt(ba)
    else:
        print(f"Already staged: {B.paths(ba)['kt_data']}")


def kt_data(args):
    return B.paths(b_args(args))["kt_data"]


def selected(args):
    return B.selected_user_ids(B.paths(b_args(args)), b_args(args))


def install_condition(kt, condition, data_dir):
    """Install the practice or profile prompts into the paper's module; returns the PracticeInfo whose answer-analysis
    counts the prompts update."""
    if condition == "profile":
        import kt_student_profile as SP
        SP.install_profile(kt, data_dir)
        return SP.DATA.info
    install_practice(kt, data_dir)
    return INFO


def practice_prompts(args, condition="practice"):
    """Yields (prediction_id, prompt) for the practice or profile condition; sets args.info for the counts."""
    kt = B.import_kt_base()
    args.info = install_condition(kt, condition, kt_data(args))
    return B.iter_prompts(kt, kt_data(args), selected(args), kt.BASE_SYSTEM_PROMPT)


def cmd_check_prompts(args):
    cmd_stage(args)
    print("=== baseline: our prompts vs the published ones ===")
    B.cmd_check_prompts(b_args(args, "check-prompts"))
    print("\n=== practice: our prompts with the added text removed vs the published ones ===")
    kt = B.import_kt_base()
    install_practice(kt, kt_data(args))
    B.cmd_check_prompts(b_args(args, "check-prompts"), system_suffix="", normalize=strip_added)
    print(f"Answer analyses written while checking: {INFO.counts}")


def cmd_show_prompt(args):
    cmd_stage(args)
    best = None
    for pid, prompt in practice_prompts(args, args.condition):
        if args.which == "first":
            best = (pid, prompt)
            break
        if best is None or len(prompt) > len(best[1]):
            best = (pid, prompt)
    print(f"===== {best[0]} ({len(best[1]):,} characters) =====\n{best[1]}")


def count_tokens_fn(model_id):
    try:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        return lambda text: len(tok(text).input_ids)
    except Exception as e:  # no transformers, or no network: estimate
        print(f"(tokenizer not available: {type(e).__name__}; estimating tokens as characters / 3)")
        return lambda text: len(text) // 3


def cmd_check_length(args):
    cmd_stage(args)
    longest, total, n = {}, 0, 0
    for pid, prompt in practice_prompts(args, args.condition):
        user = pid.rsplit("_", 2)[0]
        total += len(prompt)
        n += 1
        if len(prompt) > len(longest.get(user, "")):
            longest[user] = prompt
    count = count_tokens_fn(model_id())
    lengths = sorted(count(p) for p in longest.values())
    print(f"{n:,} {args.condition} prompts, {total / max(n, 1):,.0f} characters on average; "
          f"answer analyses: {args.info.counts}")
    print(f"Longest {args.condition} prompt: {lengths[-1]:,} tokens (median of the students' longest: {lengths[len(lengths) // 2]:,})")
    need = lengths[-1] + OUTPUT_HEADROOM_TOKENS
    if args.max_model_len and need > args.max_model_len:
        raise SystemExit(f"Needs --max-model-len >= {need:,} (now {args.max_model_len:,}).")
    print(f"OK for --max-model-len {args.max_model_len or '(model default)'} (needs >= {need:,})")


def model_id():
    return os.environ.get("KT_MODEL_ID", "cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit")


def results_path(args, which):
    """One file per condition, whatever the number of students: adding students later continues the same file
    (kt_inference_base skips the predictions already in it)."""
    return os.path.join(args.out_dir, f"{which}_qwen3next80b_awq_bin{B.BIN_SIZE}_hist{B.MIN_HISTORY}.jsonl")


def kt_cmd(args, which):
    ba = b_args(args, "infer-kt")
    head = [sys.executable, MODEL_SCRIPT] if which == "baseline" else [sys.executable, THIS_FILE, f"_{which}-worker"]
    return head + ["--data-dir", kt_data(args), "--num-students", "0", "--bin-size", str(B.BIN_SIZE),
                   "--min-history", str(B.MIN_HISTORY), "--output", results_path(args, which)] + B.vllm_args(ba)


def cmd_infer(args, which):
    cmd_stage(args)
    timings = os.path.join(args.out_dir, "timings.json")
    B.run_timed(f"kt_{which}", kt_cmd(args, which), CODE_DIR, timings)


def condition_worker(condition):
    """Started by infer-practice / infer-profile: the paper's run_inference with that condition's prompts installed."""
    argv = sys.argv[2:]
    data_dir = argv[argv.index("--data-dir") + 1]
    sys.argv = [MODEL_SCRIPT] + argv
    kt = B.import_kt_base()
    install_condition(kt, condition, data_dir)
    import qwen3next80b_awq_instruct_vllm as M
    kt.run_inference(M.MODEL_CONFIG)


# ---------------------------------------------------------------------------------------------- evaluate

def paper_subset(args):
    users = set(selected(args))
    path = os.path.join(args.out_dir, f"paper_qwen3next80b_instruct_bf16_n{len(users)}.jsonl")
    if not os.path.exists(path):
        n = 0
        with open(path, "w", encoding="utf-8") as f:
            for line in B.iter_lines(f"{B.PAPER_ZIP}::{PAPER_MEMBER}"):
                if B.line_user_id(line) in users:
                    f.write(line if line.endswith("\n") else line + "\n")
                    n += 1
        print(f"Wrote the paper's {n:,} published predictions for these students to {path}")
    return path


def mcnemar(b, c):
    """Exact two-sided McNemar test p-value for b and c discordant pairs."""
    n = b + c
    if n == 0:
        return None
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def paired_table(ra, rb, na, nb):
    """McNemar tests of run b against run a on the targets both parsed: KT, and cognitive on truly wrong answers."""
    a = {x["prediction_id"]: x for x in ra}
    b = {x["prediction_id"]: x for x in rb}
    both = [k for k in a if k in b and a[k]["predicted_question_level"] is not None
            and b[k]["predicted_question_level"] is not None]
    hit = lambda x: x["predicted_question_level"] == x["actual_score"]
    only_a = sum(1 for k in both if hit(a[k]) and not hit(b[k]))
    only_b = sum(1 for k in both if hit(b[k]) and not hit(a[k]))
    wrong_targets = [k for k in both if B.is_truly_incorrect(a[k])]
    cog_a = sum(1 for k in wrong_targets if B.cognitive_hit(a[k]) and not B.cognitive_hit(b[k]))
    cog_b = sum(1 for k in wrong_targets if B.cognitive_hit(b[k]) and not B.cognitive_hit(a[k]))
    p1, p2 = mcnemar(only_a, only_b), mcnemar(cog_a, cog_b)
    return (f"\n## {nb.capitalize()} vs {na} on the same {len(both):,} targets (paired)\n\n"
            + B.markdown_table(["", f"only {na} right", f"only {nb} right", "McNemar p"], [
                ["KT (question level)", only_a, only_b, "N/A" if p1 is None else f"{p1:.3g}"],
                [f"Cognitive, incorrect answers ({len(wrong_targets)} targets)", cog_a, cog_b,
                 "N/A" if p2 is None else f"{p2:.3g}"]]))


def cmd_evaluate(args):
    runs = [("Paper: Qwen3-Next-80B-Instruct (BF16, published)", paper_subset(args)),
            ("Baseline: Qwen3-Next-80B-Instruct AWQ, paper prompts", results_path(args, "baseline")),
            ("Practice: Qwen3-Next-80B-Instruct AWQ, + practices", results_path(args, "practice")),
            ("Profile: Qwen3-Next-80B-Instruct AWQ, student profile + last 10", results_path(args, "profile"))]
    tables, recs = [], {}
    for label, path in runs:
        if not os.path.exists(path):
            print(f"missing (not run yet): {path}")
            continue
        r = B.load_kt_records(path)
        for line, x in zip(B.iter_lines(path), r):   # keep the prediction ids for the paired comparison
            x["prediction_id"] = json.loads(line)["prediction_id"]
        recs[label] = r
    if not recs:
        return
    # Every column counts the same predictions: those present in all the runs found (while a run is still going,
    # or after students were added, the files can hold different students)
    common = set.intersection(*({x["prediction_id"] for x in r} for r in recs.values()))
    for label in recs:
        n_all = len(recs[label])
        recs[label] = [x for x in recs[label] if x["prediction_id"] in common]
        if len(recs[label]) < n_all:
            print(f"{label}: {len(recs[label]):,} of its {n_all:,} predictions are in every run; the tables use those")
    tables = [(label, B.kt_table2(r), B.kt_table3(r)) for label, r in recs.items()]
    metrics = [
        ("Predictions", lambda t2, t3: f"{t2['n']:,}"),
        ("Parsed predictions", lambda t2, t3: B.pct(t2["parse_rate"])),
        ("KT accuracy (question level)", lambda t2, t3: B.pct(t2["fkt_acc"])),
        ("KT AUC", lambda t2, t3: "N/A" if t2["fkt_auc"] is None else f"{t2['fkt_auc']:.3f}"),
        ("KT accuracy when the student was correct", lambda t2, t3: B.pct(t2["correct"]["fkt_acc"])),
        ("KT accuracy when the student was incorrect", lambda t2, t3: B.pct(t2["incorrect"]["fkt_acc"])),
        ("Predicted 'correct' rate", lambda t2, t3: B.pct(t2["predicted_correct_rate"])),
        ("All-correct baseline", lambda t2, t3: B.pct(t2["all_correct_baseline"])),
        ("Cognitive accuracy, correct answers", lambda t2, t3: B.pct(t2["correct"]["cog_acc"])),
        ("Cognitive accuracy, incorrect answers", lambda t2, t3: B.pct(t2["incorrect"]["cog_acc"])),
        ("  MC (select 1)", lambda t2, t3: B.pct(t3[B.MC_SELECT_1]["cog_acc"]) if B.MC_SELECT_1 in t3 else "N/A"),
        ("  MC (select all)", lambda t2, t3: B.pct(t3[B.MC_SELECT_ALL]["cog_acc"]) if B.MC_SELECT_ALL in t3 else "N/A"),
        ("  Fill-in", lambda t2, t3: B.pct(t3[B.FILL_IN]["cog_acc"]) if B.FILL_IN in t3 else "N/A"),
    ]
    header = ["Metric"] + [label for label, _, _ in tables]
    rows = [[name] + [fn(t2, t3) for _, t2, t3 in tables] for name, fn in metrics]
    n_students = len({pid.rsplit("_", 2)[0] for pid in common})
    report = [f"# KT and cognitive student modeling, {n_students} random paper students "
              f"({len(common):,} predictions in every run)\n",
              B.markdown_table(header, rows)]
    # paired comparisons on the same targets
    names = {runs[1][0]: "baseline", runs[2][0]: "practice", runs[3][0]: "profile"}
    for la, lb in ((runs[1][0], runs[2][0]), (runs[1][0], runs[3][0]), (runs[2][0], runs[3][0])):
        if la in recs and lb in recs:
            report.append(paired_table(recs[la], recs[lb], names[la], names[lb]))
    text = "\n".join(report)
    print("\n" + text)
    out = os.path.join(args.out_dir, "comparison.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(f"\nSaved {out}")


def cmd_all(args):
    cmd_stage(args)
    cmd_check_length(args)
    cmd_infer(args, "baseline")
    cmd_infer(args, "practice")
    cmd_evaluate(args)


def cmd_profile_all(args):
    """The profile condition only (the baseline and practice runs are reused from the same folder)."""
    args.condition = "profile"
    cmd_stage(args)
    cmd_check_length(args)
    cmd_infer(args, "profile")
    cmd_evaluate(args)


COMMANDS = {"pick-users": cmd_pick_users, "stage": cmd_stage, "check-prompts": cmd_check_prompts,
            "show-prompt": cmd_show_prompt, "check-length": cmd_check_length,
            "infer-baseline": lambda a: cmd_infer(a, "baseline"), "infer-practice": lambda a: cmd_infer(a, "practice"),
            "infer-profile": lambda a: cmd_infer(a, "profile"),
            "evaluate": cmd_evaluate, "all": cmd_all, "profile-all": cmd_profile_all}


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=list(COMMANDS))
    ap.add_argument("--n", type=int, default=50,
                    help="students to use (default 50); a larger --n later in the same folder adds students")
    ap.add_argument("--seed", type=int, default=2026, help="seed for picking the students")
    ap.add_argument("--students", type=int, default=0,
                    help="test run on only the first N of the picked students (separate output folder)")
    ap.add_argument("--out-dir", default=None, help=f"default {DEFAULT_OUT} (+ _testN with --students)")
    ap.add_argument("--force", action="store_true", help="pick the students again")
    ap.add_argument("--which", choices=["first", "longest"], default="first", help="show-prompt: which prompt")
    ap.add_argument("--condition", choices=["practice", "profile"], default="practice",
                    help="show-prompt / check-length: which condition's prompts (default practice)")
    ap.add_argument("--num-gpus", type=int, default=1)
    ap.add_argument("--gpu-memory-utilization", type=float, default=0.9)
    ap.add_argument("--max-model-len", type=int, default=None)
    ap.add_argument("--batch-size", type=int, default=None)
    ap.add_argument("--max-num-seqs", type=int, default=None)
    ap.add_argument("--cache-dir", default=None)
    args = ap.parse_args()
    # base_dir holds the student list; a test run (--students N) writes everything else to <base>_testN
    args.base_dir = os.path.abspath(args.out_dir or DEFAULT_OUT)
    args.out_dir = args.base_dir + (f"_test{args.students}" if args.students else "")
    return args


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("_practice-worker", "_profile-worker"):
        condition_worker(sys.argv[1][1:].split("-")[0])
    else:
        sys.stdout.reconfigure(line_buffering=True)
        a = parse_args()
        COMMANDS[a.command](a)
