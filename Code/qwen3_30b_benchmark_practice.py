#!/usr/bin/env python3
"""
The qwen3_30b_benchmark.py pipeline with mathematical-practice information added to the prompts.

Everything is identical to the baseline (same students, staged data, model, generation settings,
pedagogical items and evaluation) except for the practice text, so the two result CSVs can be
compared directly. The evaluate step does this: each row also shows the baseline's value and the
change in percentage points.

Practice information comes from Problems.csv['mathematical_practice'] (6 probabilities per
problem, see augment_mathematical_practice.py). A problem's practice is the one with the highest
probability; tied practices are all listed ("Representing; Procedural Fluency").

What is added to the prompts:
  - KT (Tasks 1-2): every problem in the history and the new problem get a
    "Mathematical Practice: <practice>" line after their "Skill:" line, and the system prompt
    gets the official definitions of all six practices.
  - Difficulty / discrimination (Tasks 3-4): both problems get the practice line, and the system
    prompt gets the definitions of all six practices.
  - Distractor tasks (Tasks 5-6): the single problem gets the practice line and the definition
    of its own practice.
Only the short "Official definition" of each practice is used (about 300 tokens for all six),
so the longest KT prompt stays around 65k tokens. `check-length` measures it exactly.

How it works without changing the paper's code:
  - KT: the staged Skills.csv has one row per problem whose node_name is
    "Undefined\\nMathematical Practice: <practice>". The unchanged kt_inference_base prints
    "Skill: Undefined" (as in the paper's prompts) followed by the practice line. The worker also
    appends the definitions to kt_inference_base.BASE_SYSTEM_PROMPT before calling run_inference.
  - Pedagogical: the worker appends the definitions to the difficulty/discrimination system
    prompts and wraps prepare_comparison_batch / prepare_distractor_batch to add the practice
    lines, then calls the unchanged run_inference. Items are sampled exactly as in the baseline.

Subcommands and flags are the same as qwen3_30b_benchmark.py, plus `check-length`.
    extract-users   Write the paper's 500 user_ids (copied from the baseline's folder if there)
    stage-kt        Build <out>/kt_data/ like the baseline, with practice labels in Skills.csv
    check-prompts   Check that the prompts equal the paper's apart from the practice text
    check-length    Measure the longest KT prompt in tokens against --max-model-len
    infer-kt        Run the KT inference with practice information (GPU, timed)
    infer-ped       Run each pedagogical task with practice information (GPU, each timed)
    evaluate        Build the tables and Results/qwen_30b_results[_testN]_practice.csv
    all             extract-users -> stage-kt -> check-length -> infer-kt -> infer-ped -> evaluate

Usage (from the Code/ directory):
    # Test run: 5 students, 12 items per pedagogical task
    VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=0 python3 qwen3_30b_benchmark_practice.py all \\
        --students 5 --max-model-len 98304 --gpu-memory-utilization 0.95

    # Full run
    VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=0 python3 qwen3_30b_benchmark_practice.py all \\
        --max-model-len 98304 --gpu-memory-utilization 0.95
"""

import json
import os
import re
import shutil
import sys

import pandas as pd

import qwen3_30b_benchmark as B

MODEL_ID = "Qwen/Qwen3-30B-A3B-Instruct-2507"
MODEL_LABEL = "Qwen3-30B-A3B-Instruct + practice"
DEFAULT_OUT_DIR = os.path.join(os.path.dirname(B.DEFAULT_OUT_DIR), "qwen3_30b_practice")
THIS_FILE = os.path.abspath(__file__)

# Room left for the model's answer when checking prompt lengths against --max-model-len
OUTPUT_HEADROOM_TOKENS = 4096

# Same order as the probability arrays in Problems.csv['mathematical_practice']
PRACTICE_NAMES = [
    "Representing",
    "Abstracting and Generalizing",
    "Justifying and Proving",
    "Mathematical Modeling",
    "Collaborative Mathematics",
    "Procedural Fluency",
]
PRACTICE_LINE = "Mathematical Practice: "


def load_official_definitions():
    """The "Official definition" of each practice, read from augment_mathematical_practice.py.

    That file imports vLLM at module level, so it is parsed as text instead of imported.
    """
    with open(os.path.join(B.CODE_DIR, "augment_mathematical_practice.py"), encoding="utf-8") as f:
        source = f.read()
    definitions = re.findall(r"^Official [Dd]efinition:\n(.+?)\n\n", source, re.MULTILINE | re.DOTALL)
    if len(definitions) != len(PRACTICE_NAMES):
        raise RuntimeError(f"Expected {len(PRACTICE_NAMES)} official definitions in "
                           f"augment_mathematical_practice.py, found {len(definitions)}")
    return dict(zip(PRACTICE_NAMES, (d.strip() for d in definitions)))


DEFINITIONS = load_official_definitions()

# Appended to the system prompt of every prompt that shows more than one problem
PRACTICE_SECTION = (
    "\n\n---\n\n"
    "Mathematical Practices:\n\n"
    f'Every problem below includes a line "{PRACTICE_LINE}<practice>". It names the mathematical '
    "practice the problem most strongly assesses, out of the six practices defined here "
    "(several are listed, separated by semicolons, when they are equally strong).\n\n"
    + "\n".join(f"{i}. {name}: {DEFINITIONS[name]}" for i, name in enumerate(PRACTICE_NAMES, 1))
)


def practice_labels():
    """problem_id -> label: the practice(s) with the highest probability, ties joined by '; '.

    Uses the first row of a problem_id that appears more than once, like the KT merge does.
    """
    problems = pd.read_csv(os.path.join(B.DATA_DIR, "Problems.csv"), dtype=str, keep_default_na=False,
                           usecols=["problem_id", "mathematical_practice"])
    labels = {}
    for problem_id, cell in zip(problems["problem_id"], problems["mathematical_practice"]):
        problem_id = int(problem_id)
        if problem_id in labels or not cell.strip():
            continue
        scores = json.loads(cell)
        top = max(scores)
        labels[problem_id] = "; ".join(name for name, score in zip(PRACTICE_NAMES, scores) if score == top)
    return labels


def label_line(label):
    return f"\n\n{PRACTICE_LINE}{label}" if label else ""


def label_with_definitions(label):
    """Practice line plus the definition of each practice in it (for single-problem prompts)."""
    if not label:
        return ""
    definitions = "\n".join(f"Definition of {name}: {DEFINITIONS[name]}" for name in label.split("; "))
    return f"{label_line(label)}\n{definitions}"


def strip_practice(prompt):
    """Remove the added practice text, leaving the prompt the baseline would have built."""
    prompt = prompt.replace(PRACTICE_SECTION, "", 1)
    return re.sub(rf"\n{PRACTICE_LINE}[^\n]*", "", prompt)


# ---------------------------------------------------------------------------
# Workers: run inside the inference subprocess, patch the base module, run it unchanged
# ---------------------------------------------------------------------------

def kt_worker(argv):
    kt = B.import_kt_base()
    from qwen3_30b_a3b_instruct_vllm import MODEL_CONFIG
    # run_inference builds its system prompt from this module global when it is called
    kt.BASE_SYSTEM_PROMPT = kt.BASE_SYSTEM_PROMPT + PRACTICE_SECTION
    sys.argv = [sys.argv[0]] + argv
    kt.run_inference(MODEL_CONFIG)


def ped_worker(argv):
    B.import_kt_base()  # stubs vllm/torch where they can't load; a no-op on the GPU server
    import pedagogical_inference_base as ped
    from qwen3_30b_a3b_instruct_pedagogical import MODEL_CONFIG
    add_practice_to_pedagogical(ped)
    sys.argv = [sys.argv[0]] + argv
    ped.run_inference(MODEL_CONFIG)


def add_practice_to_pedagogical(ped):
    """Patch pedagogical_inference_base so its prompts carry the practice information."""
    labels = practice_labels()

    # get_system_prompt reads these module globals when it is called
    ped.SYSTEM_PROMPT_DIFFICULTY += PRACTICE_SECTION
    ped.SYSTEM_PROMPT_DISCRIMINATION += PRACTICE_SECTION

    prepare_comparison_batch = ped.prepare_comparison_batch
    prepare_distractor_batch = ped.prepare_distractor_batch

    def prepare_comparison_with_practice(samples, *args, **kwargs):
        samples = [{**s,
                    "text_a": s["text_a"] + label_line(labels.get(s["problem_id_a"])),
                    "text_b": s["text_b"] + label_line(labels.get(s["problem_id_b"]))}
                   for s in samples]
        return prepare_comparison_batch(samples, *args, **kwargs)

    def prepare_distractor_with_practice(samples, *args, **kwargs):
        samples = [{**s, "cleaned_body": s["cleaned_body"] + label_with_definitions(labels.get(int(s["problem_id"])))}
                   for s in samples]
        return prepare_distractor_batch(samples, *args, **kwargs)

    ped.prepare_comparison_batch = prepare_comparison_with_practice
    ped.prepare_distractor_batch = prepare_distractor_with_practice


WORKERS = {"_kt-worker": kt_worker, "_ped-worker": ped_worker}


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def baseline_args(args):
    """The baseline's folder and CSV for the same --students, to reuse its caches and compare."""
    suffix = B.test_suffix(args)
    return B.DEFAULT_OUT_DIR + suffix, B.DEFAULT_CSV.replace(".csv", f"{suffix}.csv")


def cmd_extract_users(args):
    p = B.paths(args)
    baseline_dir, _ = baseline_args(args)
    # The paper's user list and correct answers don't depend on the prompts: reuse the baseline's
    os.makedirs(p["out"], exist_ok=True)
    for name in ("paper_user_ids.txt", "paper_correct_answers.json"):
        source, target = os.path.join(baseline_dir, name), os.path.join(p["out"], name)
        if os.path.exists(source) and not os.path.exists(target) and not args.force:
            shutil.copy(source, target)
            print(f"Copied {name} from {baseline_dir}")
    B.cmd_extract_users(args)


def write_practice_skills(dst):
    """Skills.csv with one row per problem: 'Undefined' plus the practice line.

    kt_inference_base prints 'Skill: {node_name}', so every problem shows 'Skill: Undefined'
    (as in the paper's prompts) followed by 'Mathematical Practice: <practice>'.
    """
    labels = practice_labels()
    problem_ids = pd.read_csv(os.path.join(B.DATA_DIR, "Problems.csv"), usecols=["problem_id"])["problem_id"]
    node_names = {int(pid): "Undefined" + (f"\n{PRACTICE_LINE}{labels[int(pid)]}" if int(pid) in labels else "")
                  for pid in problem_ids}
    pd.DataFrame({"problem_id": list(node_names), "node_name": list(node_names.values())}).to_csv(dst, index=False)
    print(f"Skills: practice labels for {sum(pid in labels for pid in node_names)}/{len(node_names)} problems")


PRACTICE_STAGED_MARKER = ".staged_practice"


def cmd_stage_kt(args):
    if args.with_skills:
        raise SystemExit("--with-skills is not supported with practice labels")
    marker = os.path.join(B.paths(args)["kt_data"], PRACTICE_STAGED_MARKER)
    if os.path.exists(marker):
        os.remove(marker)
    cmd_extract_users(args)
    B.cmd_stage_kt(args)
    write_practice_skills(os.path.join(B.paths(args)["kt_data"], "Skills.csv"))
    with open(marker, "w") as f:
        f.write("done\n")


def ensure_staged(args):
    # The practice marker is written only after the practice Skills.csv, so a run never
    # uses staged data without practice labels
    if not B.is_staged(B.paths(args), PRACTICE_STAGED_MARKER):
        cmd_stage_kt(args)


def show_example(prompt):
    """Print the practice section and the last history problem + new problem of a prompt."""
    tail = prompt.rsplit("**Student's Previous Problems:**", 1)[1]
    last_entries = tail.split("---\n\n")[-2:]
    print("\n" + "=" * 80 + "\nExample prompt (practice section, last history problem, new problem):\n")
    print(PRACTICE_SECTION.strip())
    print("\n[...]\n")
    print("---\n\n".join(last_entries).strip())
    print("=" * 80 + "\n")


def cmd_check_prompts(args):
    ensure_staged(args)
    B.cmd_check_prompts(args, system_suffix=PRACTICE_SECTION, normalize=strip_practice, show_example=show_example)
    print("(Compared after removing the practice text: identical prompts mean nothing else changed.)")


def load_tokenizer():
    """Qwen tokenizer as a function text -> number of tokens, or None if it can't be loaded."""
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    except Exception as error:  # transformers missing or broken
        print(f"transformers tokenizer unavailable ({type(error).__name__}), trying tokenizers ...")
    try:
        from tokenizers import Tokenizer
        tokenizer = Tokenizer.from_pretrained(MODEL_ID)
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False).ids)
    except Exception as error:
        print(f"tokenizers unavailable ({type(error).__name__})")
    return None


def cmd_check_length(args):
    """Token length of the longest KT prompt (the practice text makes prompts longer)."""
    ensure_staged(args)
    kt = B.import_kt_base()
    p = B.paths(args)
    users = B.selected_user_ids(p, args)
    print(f"Building the KT prompts of {len(users)} students to find the longest ...")
    longest = {}  # user -> longest prompt; a user's prompts grow with their history
    for pid, prompt in B.iter_prompts(kt, p["kt_data"], users, kt.BASE_SYSTEM_PROMPT + PRACTICE_SECTION):
        user = pid.rsplit("_", 2)[0]
        if len(prompt) > len(longest.get(user, "")):
            longest[user] = prompt

    count_tokens = load_tokenizer()
    if count_tokens:
        lengths = [count_tokens(prompt) for prompt in longest.values()]
        how = "tokens (Qwen tokenizer)"
    else:
        # About 3.5 characters per token for this text; dividing by 3 overestimates, to be safe
        lengths = [len(prompt) // 3 for prompt in longest.values()]
        how = "tokens (estimated as characters / 3)"
    max_tokens = max(lengths)
    print(f"Longest KT prompt: {max_tokens:,} {how}; longest in characters: "
          f"{max(len(prompt) for prompt in longest.values()):,}")

    if args.max_model_len is None:
        print(f"--max-model-len not set: vLLM uses the model's full context. On one 80GB A100 "
              f"use e.g. --max-model-len 98304 (needs >= {max_tokens + OUTPUT_HEADROOM_TOKENS:,}).")
        return
    needed = max_tokens + OUTPUT_HEADROOM_TOKENS
    if needed > args.max_model_len:
        raise SystemExit(f"Longest prompt + {OUTPUT_HEADROOM_TOKENS} tokens for the answer = {needed:,} "
                         f"> --max-model-len {args.max_model_len:,}. Raise --max-model-len.")
    print(f"OK: fits in --max-model-len {args.max_model_len:,} with "
          f"{args.max_model_len - max_tokens:,} tokens left for the answer.")


def cmd_infer_kt(args):
    ensure_staged(args)
    p = B.paths(args)
    cmd = [sys.executable, THIS_FILE, "_kt-worker",
           "--data-dir", p["kt_data"],
           "--num-students", "0",  # all users in the staged file
           "--bin-size", str(B.BIN_SIZE),
           "--min-history", str(B.MIN_HISTORY),
           "--output", p["kt_results"]] + B.vllm_args(args)
    B.run_timed("kt", cmd, B.CODE_DIR, p["timings"])


def cmd_infer_ped(args):
    p = B.paths(args)
    B.stage_ped(p)
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [B.CODE_DIR, B.PED_DIR, env.get("PYTHONPATH")]))
    for task in args.ped_tasks:
        cmd = [sys.executable, THIS_FILE, "_ped-worker",
               "--task", task,
               "--num-samples", str(args.num_samples),
               "--sampling-mode", args.sampling_mode,
               "--seed", str(args.seed),
               "--data-dir", p["ped_data"],
               "--output", p["ped_results"][task]] + B.vllm_args(args)
        B.run_timed(f"ped_{task}", cmd, B.PED_DIR, p["timings"], env=env)


def cmd_evaluate(args):
    B.cmd_evaluate(args)


def cmd_all(args):
    cmd_stage_kt(args)  # includes extract-users
    cmd_check_length(args)
    cmd_infer_kt(args)
    cmd_infer_ped(args)
    cmd_evaluate(args)


COMMANDS = {
    "extract-users": cmd_extract_users,
    "stage-kt": cmd_stage_kt,
    "check-prompts": cmd_check_prompts,
    "check-length": cmd_check_length,
    "infer-kt": cmd_infer_kt,
    "infer-ped": cmd_infer_ped,
    "evaluate": cmd_evaluate,
    "all": cmd_all,
}


def parse_args():
    parser = B.build_parser(COMMANDS, description=__doc__)
    parser.add_argument("--compare-csv", default=None,
                        help="Baseline results CSV to compare with (default: the baseline CSV for the same --students)")
    parser.set_defaults(label=MODEL_LABEL)
    args = parser.parse_args()
    # Default CSV: Results/qwen_30b_results[_testN]_practice.csv
    B.resolve_defaults(args, out_dir=DEFAULT_OUT_DIR, csv_path=B.DEFAULT_CSV)
    if args.csv == B.DEFAULT_CSV.replace(".csv", f"{B.test_suffix(args)}.csv"):
        args.csv = args.csv.replace(".csv", "_practice.csv")
    if args.compare_csv is None:
        args.compare_csv = baseline_args(args)[1]
    return args


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in WORKERS:
        WORKERS[sys.argv[1]](sys.argv[2:])
    else:
        args = parse_args()
        COMMANDS[args.command](args)
