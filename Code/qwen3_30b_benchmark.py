#!/usr/bin/env python3
"""
Run the FoundationalASSIST paper benchmark for Qwen3-30B-A3B-Instruct-2507 and build the
paper's Table 2 (KT accuracy), Table 3 (cognitive accuracy on incorrect answers) and
Table 4 (pedagogical grounding) for it, next to the paper's four models.

No original file is modified. Qwen3-30B goes through the same, unmodified pipeline as the
paper's models (kt_inference_base.py / pedagogical_inference_base.py). Where the released
data differs from what produced the published results, the input data is staged instead of
changing code, so the prompts are identical to the ones the paper's models saw
(check with `check-prompts`):

  1. Same students: the paper's 500 user_ids are read from Results/inference_data_kt_results.zip
     and Interactions.csv is filtered to them (the base then runs with --num-students 0).
  2. Correct answers: the base prints Problems.csv['Fill-in Answers'] as "Correct Answer". In the
     released CSV it is empty for most MC problems (published prompts show letters) and many values
     were altered by Excel ('3/7' -> '7-Mar', '1.40' -> '1.4', '-2/3' -> '-0.666666667', 'False' ->
     'FALSE'). The staged Problems.csv takes each problem's correct answer from the published prompts.
  3. Repeated interactions: the released Interactions.csv repeats an interaction once per duplicate
     row of its problem in Problems.csv; the staged copy keeps each interaction id once.
  4. Skills: every published prompt says "Skill: Undefined", so the staged Skills.csv matches nothing.

Subcommands (run from the Code/ directory):
    extract-users   Write the paper's 500 user_ids to <out>/paper_user_ids.txt
    stage-kt        Build <out>/kt_data/ (Interactions, Problems, Skills) for the KT run (CPU)
    check-prompts   Check that staged data + unmodified base reproduce the published prompts
    infer-kt        Run qwen3_30b_a3b_instruct_vllm.py on the staged data (GPU, timed)
    infer-ped       Run qwen3_30b_a3b_instruct_pedagogical.py once per task (GPU, each timed)
    evaluate        Build Tables 2-4 from the result JSONL files (CPU)
    all             extract-users -> stage-kt -> infer-kt -> infer-ped -> evaluate

Outputs:
    console + <out>/<label>_tables.md   Tables 2-4 next to the paper's models
    Results/qwen_30b_results.csv        one row per result, with the GPU time of the run behind it
    <out>/<label>_metrics.json          all metrics
    <out>/timings.json                  per-run timings (data prep, model load, generation)
KT accuracy and cognitive modeling come from the same inference run (one prompt predicts both),
so their rows carry the same time.

Usage:
    # Test the whole pipeline first: 5 students, 12 items per pedagogical task,
    # written to Results/qwen3_30b_test5/ and Results/qwen_30b_results_test5.csv
    CUDA_VISIBLE_DEVICES=0,1 python qwen3_30b_benchmark.py all --students 5 --num-gpus 2 --cache-dir /data1/

    # Whole pipeline on the GPU server
    CUDA_VISIBLE_DEVICES=0,1 python qwen3_30b_benchmark.py all --num-gpus 2 --cache-dir /data1/

    # Check the evaluator against a published result file (no GPU needed)
    python qwen3_30b_benchmark.py evaluate --no-ped --label GPT-OSS-120B \
        --kt-results ../Results/inference_data_kt_results.zip::inference_data_kt_results/gptoss120b_n500_bin10_hist50.jsonl
"""

import argparse
import csv
import difflib
import hashlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import types
import zipfile

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(REPO_DIR, "Data")
PED_DIR = os.path.join(REPO_DIR, "Results", "pedagogical_grounding")
PAPER_ZIP = os.path.join(REPO_DIR, "Results", "inference_data_kt_results.zip")
PAPER_REF_MEMBER = "inference_data_kt_results/gptoss120b_n500_bin10_hist50.jsonl"
DEFAULT_OUT_DIR = os.path.join(REPO_DIR, "Results", "qwen3_30b")
DEFAULT_CSV = os.path.join(REPO_DIR, "Results", "qwen_30b_results.csv")

sys.path.insert(0, CODE_DIR)
sys.path.insert(0, PED_DIR)
from evaluate_kt import answers_match  # noqa: E402
from evaluate_pedagogical import (  # noqa: E402
    load_results,
    evaluate_comparison_task,
    evaluate_distractor_task,
)

KT_SCRIPT = "qwen3_30b_a3b_instruct_vllm.py"
PED_SCRIPT = "qwen3_30b_a3b_instruct_pedagogical.py"
KT_OUTPUT = "qwen3_30b_a3b_instruct_n500_bin10_hist50.jsonl"
MODEL_LABEL = "Qwen3-30B-A3B-Instruct"

# Settings the paper's KT results were produced with (see result file names in the zip)
BIN_SIZE = 10
MIN_HISTORY = 50

MC_SELECT_1 = "Multiple Choice (select 1)"
MC_SELECT_ALL = "Multiple Choice (select all)"
FILL_IN = "Fill-in-the-blank(s)"
ORDER_SORT = "Order / Sort"
MC_TYPES = (MC_SELECT_1, MC_SELECT_ALL)

PED_TASKS = ["difficulty", "discrimination", "distractor_most", "distractor_least"]

# Reference numbers from the paper (Worden et al., 2026)
# Table 2: FKT Acc., (student correct) FKT Acc., Cog. Acc., (student incorrect) FKT Acc., Cog. Acc.
PAPER_TABLE2 = {
    "GPT-OSS-120B": (56.2, 68.2, 62.9, 43.4, 10.1),
    "Llama-3.3-70B": (52.3, 85.4, 72.6, 12.6, 3.7),
    "Qwen3-80B-Inst.": (54.0, 56.5, 50.3, 51.0, 13.5),
    "Qwen3-80B-Think.": (55.8, 63.6, 57.6, 44.6, 12.9),
}
# Table 3: MC (select 1), MC (select all), Fill-in-blank
PAPER_TABLE3 = {
    "GPT-OSS-120B": (30.3, 7.0, 5.7),
    "Llama-3.3-70B-Instruct": (11.8, 0.9, 1.7),
    "Qwen3-Next-80B-Instruct": (47.5, 3.9, 7.5),
    "Qwen3-Next-80B-Thinking": (34.7, 5.6, 6.7),
    "Random Baseline": (41.3, 2.9, 0.0),
}
# Table 4: Difficulty, Discrimination, Distractor Most, Distractor Least
PAPER_TABLE4 = {
    "GPT-OSS-120B": (68.6, 31.1, 35.5, 31.2),
    "Llama-3.3-70B": (65.7, 40.3, 43.6, 28.2),
    "Qwen3-80B-Instruct": (63.9, 43.5, 47.9, 39.7),
    "Qwen3-80B-Thinking": (63.7, 46.9, 40.2, 20.5),
    "Random Baseline": (50.0, 50.0, 35.8, 35.8),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def import_kt_base():
    """Import the unmodified kt_inference_base, stubbing torch/vllm where they can't load.

    Only data-prep helpers are used from it here, so a CPU-only machine can still stage data
    and check prompts. On the GPU server the real packages are imported.
    """
    def unavailable(*_args, **_kwargs):
        raise RuntimeError("vllm/torch are not available on this machine")

    def stub(name, **attrs):
        module = types.ModuleType(name)
        module.__dict__.update(attrs)
        sys.modules[name] = module

    def drop(prefix):
        for name in [n for n in sys.modules if n == prefix or n.startswith(prefix + ".")]:
            del sys.modules[name]

    try:
        import torch  # noqa: F401
    except (ImportError, OSError):
        drop("torch")
        stub("torch")
    try:
        import vllm.distributed.parallel_state  # noqa: F401
    except (ImportError, OSError):
        drop("vllm")
        stub("vllm", LLM=unavailable, SamplingParams=unavailable)
        stub("vllm.distributed")
        stub("vllm.distributed.parallel_state",
             destroy_model_parallel=unavailable,
             destroy_distributed_environment=unavailable)

    import kt_inference_base
    return kt_inference_base


def iter_lines(path):
    """Yield non-empty lines from a JSONL file, or from 'archive.zip::member'."""
    if "::" in path:
        zip_path, member = path.split("::", 1)
        with zipfile.ZipFile(zip_path) as z, z.open(member) as f:
            for line in io.TextIOWrapper(f, encoding="utf-8"):
                if line.strip():
                    yield line
    else:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield line


PREDICTION_ID_RE = re.compile(r'^\{"prediction_id":\s*"([^"]+)_\d+_(?:correct|incorrect)"')


def line_user_id(line):
    """user_id of a KT result line without parsing the (large) JSON.

    prediction_id = '<user_id>_<bin>_<type>' is the first key in both the base's output
    and the published files (which were re-serialized with other keys reordered).
    """
    return PREDICTION_ID_RE.match(line).group(1)


def is_missing(value):
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return str(value).strip().lower() in ("", "nan", "none")


def pct(value):
    return "N/A" if value is None else f"{100 * value:.1f}%"


def markdown_table(header, rows):
    lines = ["| " + " | ".join(header) + " |",
             "|" + "|".join("---" for _ in header) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def paths(args):
    out_dir = os.path.abspath(args.out_dir)
    return {
        "out": out_dir,
        "user_ids": os.path.join(out_dir, "paper_user_ids.txt"),
        "kt_data": os.path.join(out_dir, "kt_data"),
        "ped_data": os.path.join(out_dir, "ped_data"),
        "kt_results": os.path.abspath(args.kt_results) if args.kt_results and "::" not in args.kt_results
        else (args.kt_results or os.path.join(
            out_dir, f"qwen3_30b_a3b_instruct_n{args.students or 500}_bin{BIN_SIZE}_hist{MIN_HISTORY}.jsonl")),
        # One results file per pedagogical task, so each task's GPU time can be measured
        "ped_results": {
            task: os.path.join(out_dir, f"qwen3_30b_a3b_pedagogical_{task}_n{args.num_samples}_{args.sampling_mode}.jsonl")
            for task in PED_TASKS
        },
        "timings": os.path.join(out_dir, "timings.json"),
    }


def read_user_ids(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def selected_user_ids(p, args):
    """The paper's users, or only the first --students of them for a test run."""
    users = sorted(read_user_ids(p["user_ids"]))
    return users[:args.students] if args.students else users


# ---------------------------------------------------------------------------
# extract-users / stage-kt / infer-kt / infer-ped
# ---------------------------------------------------------------------------

def cmd_extract_users(args):
    p = paths(args)
    if os.path.exists(p["user_ids"]) and not args.force:
        print(f"User ids already extracted: {p['user_ids']}")
        return
    os.makedirs(p["out"], exist_ok=True)

    print(f"Reading user ids from {PAPER_ZIP}::{PAPER_REF_MEMBER} ...")
    users = {line_user_id(line) for line in iter_lines(f"{PAPER_ZIP}::{PAPER_REF_MEMBER}")}

    with open(p["user_ids"], "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(users)) + "\n")
    print(f"Wrote {len(users)} user ids to {p['user_ids']}")


CORRECT_ANSWER_PREFIX = "Correct Answer: "


def correct_answer_values(prompt_section):
    """Values of the 'Correct Answer:' lines in a prompt section, in order, spacing kept."""
    return [line[len(CORRECT_ANSWER_PREFIX):] for line in prompt_section.split("\n")
            if line.startswith(CORRECT_ANSWER_PREFIX)]


def interaction_sequences(interactions_path, problems_path, user_ids):
    """Each user's (problem_id, end_time) in the order kt_inference_base builds `user_records`
    (same sorts and inner merge with the staged problems; no skills)."""
    student_df = pd.read_csv(interactions_path, usecols=["id", "problem_id", "user_id", "end_time"])
    student_df = student_df.sort_values(["user_id", "id"]).reset_index(drop=True)
    student_df = student_df.sort_values("id").reset_index(drop=True)
    problems_df = pd.read_csv(problems_path, usecols=["problem_id"])
    merged_df = student_df.merge(problems_df, on="problem_id", how="inner")
    merged_df = merged_df[merged_df["user_id"].isin(user_ids)]
    return {user_id: list(zip(group["problem_id"].astype(int), group["end_time"].astype(str)))
            for user_id, group in merged_df.groupby("user_id")}


def harvest_paper_answers(sequences):
    """problem_id -> the 'Correct Answer' text the paper's models were shown.

    Targets: each record's new-problem block, keyed by the record's problem_id.
    History: the longest-history prompt of each user, whose entries follow the user's records.
    Entries are used only while their timestamps line up with the staged records: a few users
    have interactions in the paper's data that the released Interactions.csv no longer has.
    """
    answers = {}
    longest = {}
    for line in iter_lines(f"{PAPER_ZIP}::{PAPER_REF_MEMBER}"):
        if line_user_id(line) not in sequences:  # a user not staged (e.g. with --students)
            continue
        r = json.loads(line)
        head, new_block = r["prompt"].rsplit("**New Problem to Predict:**", 1)
        target = correct_answer_values(new_block)
        if len(target) == 1:
            answers.setdefault(int(r["problem_id"]), set()).add(target[0])
        if r["history_size"] > longest.get(r["user_id"], (0, None))[0]:
            longest[r["user_id"]] = (r["history_size"], head)

    diverged_users = []
    for user_id, (size, head) in longest.items():
        history = head.split("**Student's Previous Problems:**", 1)[1]
        timestamps = re.findall(r"^Timestamp: (.*)$", history, re.MULTILINE)
        values = correct_answer_values(history)
        for (problem_id, end_time), timestamp, value in zip(sequences[user_id], timestamps, values):
            if end_time != timestamp:
                diverged_users.append(user_id)
                break
            answers.setdefault(problem_id, set()).add(value)

    # A problem with several differing rows in Problems.csv (e.g. 437233) shows several values;
    # those rows already hold the paper's values, so they are left unchanged.
    conflicts = [pid for pid, v in answers.items() if len(v) > 1]
    print(f"Harvested correct answers for {len(answers) - len(conflicts)} problems "
          f"({len(conflicts)} with several values left as in Problems.csv)")
    if diverged_users:
        print(f"  NOTE: {len(diverged_users)} users have interactions in the paper's data that are missing "
              f"from the released Interactions.csv; their prompts diverge from that point on")
    return {pid: v.pop() for pid, v in answers.items() if len(v) == 1}


def write_staged_problems(dst, answers=None):
    """Copy Data/Problems.csv to dst; with `answers` ({problem_id: text}), set 'Fill-in Answers'
    to the text the paper's prompts showed as "Correct Answer" (letters for MC, pre-Excel values
    for fill-in). Rows are copied with the csv module so no other cell text is re-formatted.
    Duplicate problem rows are kept: the paper's run had them too."""
    src = os.path.join(DATA_DIR, "Problems.csv")
    n_set = 0
    with open(src, newline="", encoding="utf-8") as fin, open(dst, "w", newline="", encoding="utf-8") as fout:
        reader, writer = csv.reader(fin), csv.writer(fout)
        header = next(reader)
        writer.writerow(header)
        fill_col, pid_col = header.index("Fill-in Answers"), header.index("problem_id")
        for row in reader:
            problem_id = int(row[pid_col])
            if answers and problem_id in answers:
                # The base printed a missing answer as 'nan'; an empty cell reads back as NaN
                row[fill_col] = "" if answers[problem_id] == "nan" else answers[problem_id]
                n_set += 1
            writer.writerow(row)
    if answers:
        print(f"Problems: paper correct answers set for {n_set} rows")


STAGED_MARKER = ".staged"


def is_staged(p, marker=STAGED_MARKER):
    """True once stage-kt has finished (an interrupted staging leaves no marker)."""
    return os.path.exists(os.path.join(p["kt_data"], marker))


def cmd_stage_kt(args):
    p = paths(args)
    if os.path.exists(os.path.join(p["kt_data"], STAGED_MARKER)):
        os.remove(os.path.join(p["kt_data"], STAGED_MARKER))
    if not os.path.exists(p["user_ids"]):
        cmd_extract_users(args)
    user_ids = set(selected_user_ids(p, args))
    os.makedirs(p["kt_data"], exist_ok=True)
    interactions_dst = os.path.join(p["kt_data"], "Interactions.csv")
    problems_dst = os.path.join(p["kt_data"], "Problems.csv")

    # Interactions: copy the paper users' rows as-is (csv module, so cell text is not re-formatted).
    # The released file repeats an interaction once per duplicate row of its problem in
    # Problems.csv (same id, same content); the paper's run had each interaction once, so keep
    # the first copy. The base's merge with Problems.csv then re-expands them exactly as before.
    found, seen_ids = set(), set()
    n_rows = n_dups = 0
    with open(os.path.join(DATA_DIR, "Interactions.csv"), newline="", encoding="utf-8") as fin, \
            open(interactions_dst, "w", newline="", encoding="utf-8") as fout:
        reader, writer = csv.reader(fin), csv.writer(fout)
        header = next(reader)
        writer.writerow(header)
        user_col, id_col = header.index("user_id"), header.index("id")
        for row in reader:
            if row[user_col] not in user_ids:
                continue
            if row[id_col] in seen_ids:
                n_dups += 1
                continue
            seen_ids.add(row[id_col])
            writer.writerow(row)
            found.add(row[user_col])
            n_rows += 1
    print(f"Interactions: {len(found)}/{len(user_ids)} paper users found, {n_rows:,} rows "
          f"({n_dups:,} repeated rows dropped)")
    if len(found) != len(user_ids):
        print("  WARNING: some paper users are missing from Data/Interactions.csv")

    # Problems: correct answers as the paper's prompts showed them (cached after the first harvest)
    answers_path = os.path.join(p["out"], "paper_correct_answers.json")
    if os.path.exists(answers_path) and not args.force:
        with open(answers_path, encoding="utf-8") as f:
            answers = {int(pid): value for pid, value in json.load(f).items()}
        print(f"Loaded {len(answers)} paper correct answers from {answers_path}")
    else:
        write_staged_problems(problems_dst)
        print(f"Reading correct answers from the published prompts ({PAPER_REF_MEMBER}) ...")
        answers = harvest_paper_answers(interaction_sequences(interactions_dst, problems_dst, user_ids))
        with open(answers_path, "w", encoding="utf-8") as f:
            json.dump({str(pid): value for pid, value in sorted(answers.items())}, f, indent=0)
    write_staged_problems(problems_dst, answers)

    # Skills: every published prompt says "Skill: Undefined" and has no duplicated interactions,
    # i.e. the skill merge matched nothing in the paper's run. A Skills.csv whose only row matches
    # no problem reproduces that (no node_name column -> "Undefined", no multi-skill duplicates).
    skills_dst = os.path.join(p["kt_data"], "Skills.csv")
    if args.with_skills:
        shutil.copy(os.path.join(DATA_DIR, "Skills.csv"), skills_dst)
        print("Skills: real Skills.csv copied (prompts will differ from the paper's)")
    else:
        pd.DataFrame({"problem_id": [-1]}).to_csv(skills_dst, index=False)
        print("Skills: none, as in the paper's run (use --with-skills to include them)")
    with open(os.path.join(p["kt_data"], STAGED_MARKER), "w") as f:
        f.write("done\n")
    print(f"Staged KT data in {p['kt_data']}")


def vllm_args(args):
    extra = ["--num-gpus", str(args.num_gpus),
             "--gpu-memory-utilization", str(args.gpu_memory_utilization)]
    if args.cache_dir:
        extra += ["--cache-dir", args.cache_dir]
    if args.batch_size:
        extra += ["--batch-size", str(args.batch_size)]
    if args.max_model_len:
        extra += ["--max-model-len", str(args.max_model_len)]
    if args.max_num_seqs:
        extra += ["--max-num-seqs", str(args.max_num_seqs)]
    return extra


def gpu_names():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    visible = os.environ.get("CUDA_VISIBLE_DEVICES")
    names = [n.strip() for n in out.splitlines() if n.strip()]
    if visible:
        names = [names[int(i)] for i in visible.split(",") if i.strip().isdigit() and int(i) < len(names)]
    return ", ".join(names) or None


def run_timed(stage, cmd, cwd, timings_path, env=None):
    """Run an inference script, echo its output, and record how long each phase took.

    Phases are taken from lines the base scripts print: data prep until "Initializing vLLM
    engine", model load until the first "Processing batch", generation until "All batches
    processed successfully!". Each run is appended to timings.json under `stage`, so a resumed
    task keeps the time of its earlier runs.
    """
    print("Running:", " ".join(cmd))
    env = dict(env or os.environ)
    env["PYTHONUNBUFFERED"] = "1"  # so output lines arrive (and are timestamped) as they happen
    start = time.time()
    marks, prompts = {}, None
    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace", bufsize=1)
    for line in proc.stdout:
        sys.stdout.write(line)
        now = time.time()
        if "Initializing vLLM engine" in line:
            marks.setdefault("load_start", now)
        elif line.startswith("Processing batch "):
            marks.setdefault("generation_start", now)
        elif "All batches processed successfully" in line:
            marks["generation_end"] = now
        match = re.match(r"(?:Remaining to process|Total predictions to make): (\d+)", line)
        if match:
            prompts = int(match.group(1))  # the last one printed = prompts actually sent to the model
    returncode = proc.wait()
    end = time.time()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, cmd)
    if "generation_start" not in marks:
        print(f"[timing] {stage}: nothing was generated (already complete?), no timing recorded")
        return

    load_start = marks.get("load_start", start)
    generation_end = marks.get("generation_end", end)
    run = {
        "started": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)),
        "prompts": prompts,
        "wall_seconds": round(end - start, 1),
        "data_prep_seconds": round(load_start - start, 1),
        "model_load_seconds": round(marks["generation_start"] - load_start, 1),
        "generation_seconds": round(generation_end - marks["generation_start"], 1),
        "num_gpus": args_num_gpus(cmd),
        "gpus": gpu_names(),
    }
    timings = {}
    if os.path.exists(timings_path):
        with open(timings_path, encoding="utf-8") as f:
            timings = json.load(f)
    timings.setdefault(stage, []).append(run)
    with open(timings_path, "w", encoding="utf-8") as f:
        json.dump(timings, f, indent=2)
    print(f"[timing] {stage}: {run['wall_seconds']:.0f}s total, {run['generation_seconds']:.0f}s generating "
          f"{prompts} prompts, {run['model_load_seconds']:.0f}s loading the model")


def args_num_gpus(cmd):
    return int(cmd[cmd.index("--num-gpus") + 1]) if "--num-gpus" in cmd else 1


def cmd_infer_kt(args):
    p = paths(args)
    if not is_staged(p):
        cmd_stage_kt(args)
    cmd = [sys.executable, KT_SCRIPT,
           "--data-dir", p["kt_data"],
           "--num-students", "0",  # all users in the staged file = the paper's 500
           "--bin-size", str(BIN_SIZE),
           "--min-history", str(MIN_HISTORY),
           "--output", p["kt_results"]] + vllm_args(args)
    run_timed("kt", cmd, CODE_DIR, p["timings"])


def stage_ped(p):
    """Lay the inputs out the way pedagogical_inference_base.py expects them under --data-dir."""
    output_dir = os.path.join(p["ped_data"], "pedagogical_grounding", "output")
    problems_dir = os.path.join(p["ped_data"], "foundationalktdataset")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(problems_dir, exist_ok=True)
    for name in ("irt_parameters.json", "distractor_stats.json"):
        shutil.copy(os.path.join(PED_DIR, "output", name), os.path.join(output_dir, name))
    shutil.copy(os.path.join(DATA_DIR, "Problems.csv"), os.path.join(problems_dir, "Problems.csv"))


def cmd_infer_ped(args):
    """Run each pedagogical task separately so its GPU time can be measured on its own.

    The base re-seeds before sampling every task, so the items are the same as with --task all.
    """
    p = paths(args)
    stage_ped(p)
    env = dict(os.environ)
    # pedagogical_inference_base imports clean_utils, which lives in Code/
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [CODE_DIR, env.get("PYTHONPATH")]))
    for task in args.ped_tasks:
        cmd = [sys.executable, PED_SCRIPT,
               "--task", task,
               "--num-samples", str(args.num_samples),
               "--sampling-mode", args.sampling_mode,
               "--seed", str(args.seed),
               "--data-dir", p["ped_data"],
               "--output", p["ped_results"][task]] + vllm_args(args)
        run_timed(f"ped_{task}", cmd, PED_DIR, p["timings"], env=env)


# ---------------------------------------------------------------------------
# check-prompts
# ---------------------------------------------------------------------------

def iter_prompts(kt, data_dir, user_ids, system_prompt, legacy_clean=False):
    """Yield (prediction_id, prompt), built with the same data prep as kt_inference_base.run_inference."""
    student_df = pd.read_csv(os.path.join(data_dir, kt.STUDENT_FILE))
    student_df = student_df.sort_values(["user_id", "id"]).reset_index(drop=True)
    problems_df = pd.read_csv(os.path.join(data_dir, kt.PROBLEMS_FILE))
    clean_func = kt.clean_text_legacy if legacy_clean else kt.clean_problem_body
    problems_df["cleaned body"] = problems_df["Problem Body"].apply(clean_func)
    problems_df["answer_options"] = problems_df["Multiple Choice Options"].apply(kt.label_answer_options)
    problems_df["correct_answers"] = problems_df.apply(
        lambda row: kt.get_correct_option_letters(row["answer_options"], row["Multiple Choice Answers"])
        if row["Problem Type"] in MC_TYPES else row["Fill-in Answers"],
        axis=1,
    )
    skill_df = pd.read_csv(os.path.join(data_dir, kt.SKILL_FILE))
    problems_df = pd.merge(problems_df, skill_df, on="problem_id", how="left")
    problems_df["answer_options_formatted"] = problems_df["answer_options"].apply(
        lambda x: kt.format_answer_options_for_prompt(x) if pd.notna(x) else None
    )
    student_df = student_df.sort_values("id").reset_index(drop=True)
    merged_df = student_df.merge(problems_df, on="problem_id", how="inner")
    merged_df["answer_text"] = merged_df.apply(
        lambda row: kt.match_student_answer_to_letters(row["answer_text"], row["answer_options"])
        if row["Problem Type"] in MC_TYPES and pd.notna(row["answer_options"])
        else row["answer_text"],
        axis=1,
    )
    merged_df = merged_df[merged_df["user_id"].isin(user_ids)]

    process_single_user = kt.make_process_single_user(system_prompt)
    for user_id, user_df in merged_df.groupby("user_id"):
        user_prompts, metadata = process_single_user(
            (user_id, user_df.to_dict("records"), MIN_HISTORY, BIN_SIZE))
        for prompt, m in zip(user_prompts, metadata):
            yield m["prediction_id"], prompt


def prompt_hash(prompt):
    return hashlib.sha1(prompt.encode("utf-8")).hexdigest()


def cmd_check_prompts(args, system_suffix="", normalize=None, show_example=None):
    """Compare our prompts with the published ones.

    system_suffix is appended to the system prompt, and normalize(prompt) is applied before
    comparing; together they let a variant (e.g. with practice text) check that it adds only
    what it means to. show_example(prompt) is called with our first prompt.
    """
    p = paths(args)
    if not is_staged(p):
        cmd_stage_kt(args)
    kt = import_kt_base()
    users = selected_user_ids(p, args)
    if args.check_users > 0:
        users = users[:args.check_users]
    wanted = set(users)

    print(f"Hashing published prompts of {len(users)} paper users ({PAPER_REF_MEMBER}) ...")
    published = {}
    for line in iter_lines(f"{PAPER_ZIP}::{PAPER_REF_MEMBER}"):
        if line_user_id(line) in wanted:
            record = json.loads(line)
            published[record["prediction_id"]] = prompt_hash(record["prompt"])

    print(f"Building our prompts from {p['kt_data']} ...")
    # The reference file is GPT-OSS, whose config prepends "Reasoning: medium"
    system_prompt = "Reasoning: medium\n\n" + kt.BASE_SYSTEM_PROMPT + system_suffix
    ours, differing_users = set(), set()
    n_identical = 0
    first_mismatch = None
    for pid, prompt in iter_prompts(kt, p["kt_data"], users, system_prompt, legacy_clean=args.legacy_clean):
        if show_example and not ours:
            show_example(prompt)
        ours.add(pid)
        if normalize:
            prompt = normalize(prompt)
        if published.get(pid) == prompt_hash(prompt):
            n_identical += 1
        else:
            differing_users.add(pid.rsplit("_", 2)[0])
            if first_mismatch is None and pid in published:
                first_mismatch = (pid, prompt)

    only_published = set(published) - ours
    differing_users |= {pid.rsplit("_", 2)[0] for pid in only_published}
    print(f"\nTargets: ours={len(ours):,} published={len(published):,} "
          f"(only ours: {len(ours - set(published))}, only published: {len(only_published)})")
    print(f"Identical prompts: {n_identical:,}/{len(published):,} ({100 * n_identical / len(published):.2f}%)")
    print(f"Users with any difference: {len(differing_users)}/{len(users)}")

    if first_mismatch:
        pid, prompt = first_mismatch
        reference = next(json.loads(line)["prompt"] for line in iter_lines(f"{PAPER_ZIP}::{PAPER_REF_MEMBER}")
                         if line.startswith(f'{{"prediction_id":"{pid}"')
                         or line.startswith(f'{{"prediction_id": "{pid}"'))
        print(f"\nFirst difference ({pid}):")
        diff = difflib.unified_diff(reference.splitlines(), prompt.splitlines(),
                                    "published", "ours", lineterm="", n=1)
        for i, line in enumerate(diff):
            if i >= 40:
                print("  ...")
                break
            print("  " + line)


# ---------------------------------------------------------------------------
# evaluate
# ---------------------------------------------------------------------------

def correct_answer_from_prompt(prompt):
    """The 'Correct Answer:' line of the prompt's new-problem block."""
    block = prompt.rsplit("**New Problem to Predict:**", 1)[-1]
    match = re.search(r"^Correct Answer: (.*)$", block, re.MULTILINE)
    return match.group(1).strip() if match else None


def load_kt_records(path):
    """Load KT predictions, keeping only the fields the tables need."""
    records = []
    for line in iter_lines(path):
        r = json.loads(line)
        correct = r.get("correct_answer")
        if is_missing(correct) and r.get("prompt"):
            correct = correct_answer_from_prompt(r["prompt"])
        records.append({
            "prediction_type": r.get("prediction_type"),
            "problem_id": r.get("problem_id"),
            "problem_type": r.get("problem_type"),
            "actual_score": r.get("actual_score"),
            "actual_answer": r.get("actual_answer"),
            "correct_answer": correct,
            "predicted_question_level": r.get("predicted_question_level"),
            "predicted_student_answer": r.get("predicted_student_answer"),
        })
    return records


def exact_match(a, b):
    return a is not None and b is not None and str(a).strip() == str(b).strip()


def is_truly_incorrect(r, match=answers_match):
    """Scored incorrect AND the first answer is actually wrong.

    discrete_score is 0 whenever a hint or the answer was requested, so some 'incorrect'
    targets hold the correct answer. The paper's incorrect-case cognitive accuracy excludes them.
    """
    if r["prediction_type"] != "incorrect":
        return False
    if is_missing(r["correct_answer"]):
        return True
    return not match(r["actual_answer"], r["correct_answer"])


def cognitive_hit(r, match=answers_match):
    return match(r["predicted_student_answer"], r["actual_answer"])


def kt_table2(records):
    """Table 2 with evaluate_kt.py's metrics; incorrect-case Cog. Acc. uses truly-wrong answers only."""
    n = len(records)
    parsed = [r for r in records
              if r["actual_score"] is not None and r["predicted_question_level"] is not None]
    fkt_acc = sum(r["predicted_question_level"] == r["actual_score"] for r in parsed) / len(parsed)

    y_true, y_pred = [], []
    for r in parsed:
        try:
            y_pred.append(int(r["predicted_question_level"]))
            y_true.append(int(r["actual_score"]))
        except (TypeError, ValueError):
            pass
    try:
        auc = roc_auc_score(y_true, y_pred)
    except ValueError:
        auc = None

    by_gt = {}
    for gt in ("correct", "incorrect"):
        subset = [r for r in records if r["prediction_type"] == gt]
        cog_subset = subset if gt == "correct" else [r for r in subset if is_truly_incorrect(r)]
        by_gt[gt] = {
            "n": len(subset),
            "fkt_acc": sum(r["predicted_question_level"] == r["actual_score"] for r in subset) / len(subset),
            "cog_n": len(cog_subset),
            "cog_acc": sum(cognitive_hit(r) for r in cog_subset) / len(cog_subset),
            "cog_acc_unfiltered": sum(cognitive_hit(r) for r in subset) / len(subset),
        }

    return {
        "n": n,
        "all_correct_baseline": by_gt["correct"]["n"] / n,
        "parse_rate": len(parsed) / n,
        "predicted_correct_rate": sum(r["predicted_question_level"] == 1 for r in records) / n,
        "fkt_acc": fkt_acc,
        "fkt_auc": auc,
        "correct": by_gt["correct"],
        "incorrect": by_gt["incorrect"],
    }


def option_counts():
    problems = pd.read_csv(os.path.join(DATA_DIR, "Problems.csv"),
                           usecols=["problem_id", "Multiple Choice Options"])
    return {
        int(pid): len([o for o in str(opts).split("||") if o.strip()])
        for pid, opts in zip(problems["problem_id"], problems["Multiple Choice Options"])
        if not is_missing(opts)
    }


def kt_table3(records):
    """Cognitive accuracy on truly-wrong answers by problem type.

    Uses exact string matching (no letter-order or numeric tolerance). This reproduces the
    paper's Table 3 for all four published models; evaluate_kt.answers_match does not.
    """
    n_options = option_counts()
    table = {}
    for ptype in (MC_SELECT_1, MC_SELECT_ALL, FILL_IN, ORDER_SORT):
        subset = [r for r in records
                  if r["problem_type"] == ptype and is_truly_incorrect(r, match=exact_match)]
        if not subset:
            continue
        # Random guess: one of n options (select 1), a non-empty subset of n options (select all)
        counts = [n_options.get(int(r["problem_id"])) for r in subset if r["problem_id"] is not None]
        counts = [c for c in counts if c]
        if ptype == MC_SELECT_1 and counts:
            baseline = float(np.mean([1 / c for c in counts]))
        elif ptype == MC_SELECT_ALL and counts:
            baseline = float(np.mean([1 / (2 ** c - 1) for c in counts]))
        else:
            baseline = 0.0
        table[ptype] = {
            "n": len(subset),
            "cog_acc": sum(cognitive_hit(r, match=exact_match) for r in subset) / len(subset),
            "random_baseline": baseline,
        }
    return table


def ped_table4(results):
    table = {}
    for task in PED_TASKS:
        if task in ("difficulty", "discrimination"):
            metrics = evaluate_comparison_task(results, task)
            baseline_key = "baseline_random"
        else:
            metrics = evaluate_distractor_task(results, task)
            baseline_key = "baseline_random_avg"
        if "error" in metrics:
            print(f"  {metrics['error']}")
            continue
        metrics["baseline"] = metrics[baseline_key]
        table[task] = metrics
    return table


def render_tables(label, t2, t3, t4):
    sections = []
    if t2:
        rows = [[name, *(f"{v:.1f}%" for v in vals)] for name, vals in PAPER_TABLE2.items()]
        rows.append([f"**{label}**", pct(t2["fkt_acc"]),
                     pct(t2["correct"]["fkt_acc"]), pct(t2["correct"]["cog_acc"]),
                     pct(t2["incorrect"]["fkt_acc"]), pct(t2["incorrect"]["cog_acc"])])
        sections.append("### Table 2. Knowledge tracing accuracy broken down by correctness\n\n" + markdown_table(
            ["Model", "FKT Acc.", "Correct: FKT Acc.", "Correct: Cog. Acc.",
             "Incorrect: FKT Acc.", "Incorrect: Cog. Acc."], rows))
        sections.append(markdown_table(["Extra (this run)", "Value"], [
            ["Predictions", f"{t2['n']:,}"],
            ["All-correct baseline", pct(t2["all_correct_baseline"])],
            ["FKT AUC-ROC", "N/A" if t2["fkt_auc"] is None else f"{t2['fkt_auc']:.3f}"],
            ["Parsed predictions", pct(t2["parse_rate"])],
            ["Predicted 'correct' rate", pct(t2["predicted_correct_rate"])],
            ["Incorrect: truly-wrong answers used for Cog. Acc.",
             f"{t2['incorrect']['cog_n']:,}/{t2['incorrect']['n']:,}"],
            ["Incorrect: Cog. Acc. without the truly-wrong filter", pct(t2["incorrect"]["cog_acc_unfiltered"])],
        ]))
    if t3:
        columns = (MC_SELECT_1, MC_SELECT_ALL, FILL_IN)
        rows = [[name, *(f"{v:.1f}%" for v in vals)] for name, vals in PAPER_TABLE3.items()]
        rows.append([f"**{label}**", *(pct(t3[c]["cog_acc"]) if c in t3 else "N/A" for c in columns)])
        rows.append(["Random baseline (this run's targets)",
                     *(pct(t3[c]["random_baseline"]) if c in t3 else "N/A" for c in columns)])
        extra = ""
        if ORDER_SORT in t3:
            extra = (f"\n\nOrder / Sort (not in the paper): {pct(t3[ORDER_SORT]['cog_acc'])} "
                     f"(n={t3[ORDER_SORT]['n']})")
        sections.append("### Table 3. Cognitive modeling accuracy by problem type for incorrect answers\n\n"
                        + markdown_table(["Model", "MC (select 1)", "MC (select all)", "Fill-in-blank"], rows)
                        + "\n\n" + "n: " + ", ".join(f"{c}={t3[c]['n']}" for c in columns if c in t3) + extra)
    if t4:
        rows = [[name, *(f"{v:.1f}%" for v in vals)] for name, vals in PAPER_TABLE4.items()]
        rows.append([f"**{label}**", *(pct(t4[t]["accuracy"]) if t in t4 else "N/A" for t in PED_TASKS)])
        rows.append(["Random baseline (this run's items)",
                     *(pct(t4[t]["baseline"]) if t in t4 else "N/A" for t in PED_TASKS)])
        strata = []
        for task in ("difficulty", "discrimination"):
            if task in t4:
                by_stratum = t4[task].get("by_stratum", {})
                strata.append([task, *(pct(by_stratum[s]["accuracy"]) if s in by_stratum else "N/A"
                                       for s in ("small", "medium", "large"))])
        sections.append("### Table 4. Pedagogical Grounding results\n\n" + markdown_table(
            ["Model", "Difficulty", "Discrimination", "Distractor Most", "Distractor Least"], rows)
            + "\n\nn: " + ", ".join(f"{t}={t4[t]['total']}" for t in PED_TASKS if t in t4)
            + ("\n\n" + markdown_table(["Comparison task", "Small (diff 0.2-0.5)", "Medium (0.5-1.0)", "Large (>1.0)"],
                                       strata) if strata else ""))
    return "\n\n".join(sections)


def cmd_evaluate(args):
    p = paths(args)
    t2 = t3 = t4 = None
    if not args.no_kt:
        print(f"Loading KT results: {p['kt_results']}")
        records = load_kt_records(p["kt_results"])
        print(f"  {len(records):,} predictions")
        t2, t3 = kt_table2(records), kt_table3(records)
    if not args.no_ped:
        ped_files = [os.path.abspath(args.ped_results)] if args.ped_results else \
            [path for path in p["ped_results"].values() if os.path.exists(path)]
        results = []
        for path in ped_files:
            print(f"Loading pedagogical results: {path}")
            results += load_results(path)
        t4 = ped_table4(results)

    report = render_tables(args.label, t2, t3, t4)
    print("\n" + report + "\n")

    timings = {}
    if os.path.exists(p["timings"]):
        with open(p["timings"], encoding="utf-8") as f:
            timings = json.load(f)

    os.makedirs(p["out"], exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "_", args.label.lower()).strip("_")
    md_path = os.path.join(p["out"], f"{slug}_tables.md")
    json_path = os.path.join(p["out"], f"{slug}_metrics.json")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {args.label}: FoundationalASSIST benchmark\n\n{report}\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"table2": t2, "table3": t3, "table4": t4, "timings": timings}, f, indent=2)
    csv_path = os.path.abspath(args.csv)
    write_results_csv(csv_path, args.label, t2, t3, t4, timings, compare_csv=getattr(args, "compare_csv", None))
    print(f"Saved {md_path}\nSaved {json_path}\nSaved {csv_path}")


def timing_summary(runs):
    """Sum the runs of one stage (several if it was resumed)."""
    if not runs:
        return None
    total = {key: round(sum(r[key] for r in runs), 1)
             for key in ("wall_seconds", "data_prep_seconds", "model_load_seconds", "generation_seconds")}
    total["prompts"] = sum(r["prompts"] or 0 for r in runs)
    total["runs"] = len(runs)
    total["num_gpus"] = runs[-1]["num_gpus"]
    total["gpus"] = runs[-1]["gpus"]
    return total


CSV_COLUMNS = ["track", "task", "metric", "value", "n", "random_baseline",
               "wall_seconds", "data_prep_seconds", "model_load_seconds", "generation_seconds",
               "prompts", "seconds_per_prompt", "num_gpus", "gpus", "runs", "note"]
COMPARE_COLUMNS = ["baseline_value", "change_vs_baseline"]


def read_csv_values(path):
    """(task, metric) -> value from a results CSV written by write_results_csv."""
    with open(path, newline="", encoding="utf-8") as f:
        return {(row["task"], row["metric"]): float(row["value"])
                for row in csv.DictReader(f) if row.get("value") not in (None, "")}


def write_results_csv(path, label, t2, t3, t4, timings, compare_csv=None):
    """One row per result, with the GPU time of the inference run that produced it.

    With compare_csv (another results CSV), each row also gets that file's value for the same
    task and metric, and the difference in percentage points.
    """
    rows = []

    def add(task, metric, value, n=None, baseline=None, stage=None, note=""):
        track = "Knowledge Tracing" if task.startswith(("Task 1", "Task 2")) else "Pedagogical Grounding"
        row = {"track": track, "task": task, "metric": metric, "n": n, "note": note,
               "value": None if value is None else round(100 * value, 2),
               "random_baseline": baseline}
        summary = timing_summary(timings.get(stage)) if stage else None
        if summary:
            row.update({k: summary[k] for k in ("wall_seconds", "data_prep_seconds", "model_load_seconds",
                                                "generation_seconds", "prompts", "num_gpus", "gpus", "runs")})
            if summary["prompts"]:
                row["seconds_per_prompt"] = round(summary["generation_seconds"] / summary["prompts"], 3)
        rows.append(row)

    shared = "same GPU run as the other task: one KT prompt predicts both correctness and the answer"
    if t2:
        kt = "Task 1: Knowledge tracing"
        add(kt, "FKT accuracy (%)", t2["fkt_acc"], t2["n"], 51.3, "kt", shared)
        add(kt, "FKT accuracy when student correct (%)", t2["correct"]["fkt_acc"], t2["correct"]["n"], None, "kt", shared)
        add(kt, "FKT accuracy when student incorrect (%)", t2["incorrect"]["fkt_acc"], t2["incorrect"]["n"], None, "kt", shared)
        add(kt, "FKT AUC-ROC (x100)", t2["fkt_auc"], t2["n"], 50.0, "kt", shared)
        add(kt, "Predicted 'correct' rate (%)", t2["predicted_correct_rate"], t2["n"], None, "kt", shared)
        add(kt, "Parsed predictions (%)", t2["parse_rate"], t2["n"], None, "kt", shared)

        cog = "Task 2: Cognitive student modeling"
        add(cog, "Cog. accuracy when student correct (%)", t2["correct"]["cog_acc"], t2["correct"]["n"], None, "kt", shared)
        add(cog, "Cog. accuracy when student incorrect (%)", t2["incorrect"]["cog_acc"], t2["incorrect"]["cog_n"],
            None, "kt", shared + "; truly-wrong answers only")
        for ptype, paper_baseline in ((MC_SELECT_1, 41.3), (MC_SELECT_ALL, 2.9), (FILL_IN, 0.0), (ORDER_SORT, None)):
            if t3 and ptype in t3:
                add(cog, f"Cog. accuracy on incorrect answers, {ptype} (%)", t3[ptype]["cog_acc"], t3[ptype]["n"],
                    paper_baseline, "kt", shared + "; exact match, truly-wrong answers only")

    if t4:
        names = {"difficulty": "Task 3: Difficulty comparison",
                 "discrimination": "Task 4: Discrimination comparison",
                 "distractor_most": "Task 5: Most common distractor",
                 "distractor_least": "Task 6: Least common distractor"}
        for task in PED_TASKS:
            if task in t4:
                add(names[task], "Accuracy (%)", t4[task]["accuracy"], t4[task]["total"],
                    round(100 * t4[task]["baseline"], 2), f"ped_{task}")

    columns = ["model"] + CSV_COLUMNS
    if compare_csv:
        columns[columns.index("value") + 1:columns.index("value") + 1] = COMPARE_COLUMNS
        compare = read_csv_values(compare_csv) if os.path.exists(compare_csv) else {}
        print(f"Comparing with {compare_csv}" if compare else f"No comparison file yet: {compare_csv}")
        for row in rows:
            other = compare.get((row["task"], row["metric"]))
            if other is not None and row["value"] is not None:
                row["baseline_value"] = other
                row["change_vs_baseline"] = round(row["value"] - other, 2)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({"model": label, **row})


def cmd_all(args):
    cmd_extract_users(args)
    cmd_stage_kt(args)
    cmd_infer_kt(args)
    cmd_infer_ped(args)
    cmd_evaluate(args)


COMMANDS = {
    "extract-users": cmd_extract_users,
    "stage-kt": cmd_stage_kt,
    "check-prompts": cmd_check_prompts,
    "infer-kt": cmd_infer_kt,
    "infer-ped": cmd_infer_ped,
    "evaluate": cmd_evaluate,
    "all": cmd_all,
}


def build_parser(commands, description=__doc__):
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=commands)
    parser.add_argument("--students", type=int, default=0,
                        help="Test run on only the first N paper students; also uses --num-samples 12 "
                             "and a separate _testN output folder and CSV unless given")
    parser.add_argument("--out-dir", default=None, help="Directory for staged data and results")
    parser.add_argument("--force", action="store_true", help="Re-extract user ids even if the file exists")
    parser.add_argument("--with-skills", action="store_true",
                        help="stage-kt: include skill names (the paper's prompts had none)")

    # vLLM (infer-kt / infer-ped)
    parser.add_argument("--num-gpus", type=int, default=1)
    parser.add_argument("--cache-dir", default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--max-model-len", type=int, default=None)
    parser.add_argument("--max-num-seqs", type=int, default=None)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.9)

    # Pedagogical sampling (infer-ped), pedagogical_inference_base defaults
    parser.add_argument("--num-samples", type=int, default=None,
                        help="Pairs per comparison task / distractor items (default: 1000, or 12 with --students)")
    parser.add_argument("--sampling-mode", choices=["stratified", "random"], default="stratified")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--ped-tasks", nargs="+", choices=PED_TASKS, default=PED_TASKS,
                        help="infer-ped: tasks to run, each timed separately (default: all four)")

    # check-prompts
    parser.add_argument("--check-users", type=int, default=0, help="Paper users to compare (default: 0 = all 500)")
    parser.add_argument("--legacy-clean", action="store_true", help="Build prompts with cleantext.py")

    # evaluate
    parser.add_argument("--kt-results", default=None,
                        help="KT results JSONL, or 'archive.zip::member' (default: <out>/" + KT_OUTPUT + ")")
    parser.add_argument("--ped-results", default=None,
                        help="A single pedagogical results JSONL (default: the per-task files in <out>)")
    parser.add_argument("--csv", default=None, help="Results CSV")
    parser.add_argument("--no-kt", action="store_true", help="Skip Tables 2 and 3")
    parser.add_argument("--no-ped", action="store_true", help="Skip Table 4")
    parser.add_argument("--label", default=MODEL_LABEL, help="Row label for this model")
    return parser


def test_suffix(args):
    return f"_test{args.students}" if args.students else ""


def resolve_defaults(args, out_dir=DEFAULT_OUT_DIR, csv_path=DEFAULT_CSV):
    """Fill in defaults. A test run (--students N) gets its own folder and CSV, so it never
    mixes with the full run: <out_dir>_testN and <csv name>_testN.csv."""
    suffix = test_suffix(args)
    if args.out_dir is None:
        args.out_dir = out_dir + suffix
    if args.csv is None:
        args.csv = csv_path.replace(".csv", f"{suffix}.csv")
    if args.num_samples is None:
        args.num_samples = 12 if args.students else 1000
    return args


def parse_args():
    return resolve_defaults(build_parser(COMMANDS).parse_args())


if __name__ == "__main__":
    args = parse_args()
    COMMANDS[args.command](args)
