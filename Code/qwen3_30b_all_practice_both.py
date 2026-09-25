#!/usr/bin/env python3
"""
Find the students who worked on problems of every chosen mathematical practice, save their
user_ids in a list, and run both qwen3_30b_benchmark.py (baseline) and
qwen3_30b_benchmark_practice.py (with practice information) on exactly those students.

A problem's practice is the one with the highest probability in
Problems.csv['mathematical_practice'] (tied practices all count). A student "did" a practice if
they attempted at least --min-problems different problems of that practice.

Defaults: all six practices, students from the paper's 500 (every prompt can then be checked
against the published prompts), knowledge tracing only (Tasks 1-2; the pedagogical tasks don't
involve students, so their results from the main runs still apply).

Outputs:
    Results/student_lists/<run-name>.txt                   the user_ids, one per line
    Results/student_lists/<run-name>_practice_counts.csv   problems per practice for every student in the pool
    Results/qwen_30b_results_<run-name>.csv                baseline accuracies
    Results/qwen_30b_results_<run-name>_practice.csv       with practice information, plus the change vs baseline
    Results/qwen3_30b_<run-name>/, Results/qwen3_30b_practice_<run-name>/   staged data, predictions, tables

Any other option (--students, --max-model-len, --gpu-memory-utilization, --num-gpus,
--cache-dir, ...) is passed to both scripts.

Usage (from the Code/ directory):
    # Only find and save the students
    python3 qwen3_30b_all_practice_both.py --list-only

    # Find the students and run both benchmarks on them
    VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=0 python3 qwen3_30b_all_practice_both.py \\
        --max-model-len 98304 --gpu-memory-utilization 0.95

    # Other groups: all 5,000 students, or the five practices other than Collaborative
    python3 qwen3_30b_all_practice_both.py --pool all --list-only
    python3 qwen3_30b_all_practice_both.py --practices representing abstracting justifying modeling procedural --list-only
"""

import argparse
import os
import subprocess
import sys

import pandas as pd

import qwen3_30b_benchmark as B
import qwen3_30b_benchmark_practice as PR

PRACTICE_KEYS = {
    "representing": "Representing",
    "abstracting": "Abstracting and Generalizing",
    "justifying": "Justifying and Proving",
    "modeling": "Mathematical Modeling",
    "collaborative": "Collaborative Mathematics",
    "procedural": "Procedural Fluency",
}
LIST_DIR = os.path.join(B.REPO_DIR, "Results", "student_lists")
BASELINE_SCRIPT = os.path.join(B.CODE_DIR, "qwen3_30b_benchmark.py")
PRACTICE_SCRIPT = os.path.join(B.CODE_DIR, "qwen3_30b_benchmark_practice.py")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--practices", nargs="+", choices=PRACTICE_KEYS, default=list(PRACTICE_KEYS),
                        help="Practices a student must have done (default: all six)")
    parser.add_argument("--pool", choices=["paper", "all"], default="paper",
                        help="paper: only the paper's 500 students (default); all: all 5,000")
    parser.add_argument("--min-problems", type=int, default=1,
                        help="Different problems of each practice a student must have attempted (default: 1)")
    parser.add_argument("--run-name", default=None,
                        help="Name for the list, folders and CSVs (default: from the options, e.g. allpractices_paper)")
    parser.add_argument("--with-ped", action="store_true",
                        help="Also run the pedagogical tasks (they don't depend on the students)")
    parser.add_argument("--list-only", action="store_true", help="Only find and save the students")
    parser.add_argument("--dry-run", action="store_true", help="Save the students and print the commands only")
    args, passthrough = parser.parse_known_args()
    for option in ("--out-dir", "--csv", "--user-ids-file", "--compare-csv"):
        if any(arg == option or arg.startswith(option + "=") for arg in passthrough):
            parser.error(f"{option} is set by this script for each run")
    if args.run_name is None:
        chosen = "allpractices" if set(args.practices) == set(PRACTICE_KEYS) else \
            "_".join(key[:3] for key in PRACTICE_KEYS if key in args.practices)
        args.run_name = f"{chosen}_{args.pool}" + (f"_min{args.min_problems}" if args.min_problems > 1 else "")
    return args, passthrough


def paper_user_ids():
    """The paper's 500 user_ids (shared cache; extracted from the results zip on first use)."""
    base_args = B.resolve_defaults(B.build_parser(B.COMMANDS).parse_args(["extract-users"]))
    B.cmd_extract_users(base_args)
    return set(B.read_user_ids(B.paths(base_args)["user_ids"]))


def practice_counts(paper_users, pool):
    """Different problems per practice for every student in the pool."""
    labels = PR.practice_labels()
    interactions = pd.read_csv(os.path.join(B.DATA_DIR, "Interactions.csv"), usecols=["id", "problem_id", "user_id"])
    interactions = interactions.drop_duplicates("id")
    interactions = interactions[interactions["problem_id"].isin(labels.keys())]
    if pool == "paper":
        interactions = interactions[interactions["user_id"].isin(paper_users)]
    attempted = interactions.drop_duplicates(["user_id", "problem_id"]).copy()
    attempted["practice"] = attempted["problem_id"].map(lambda pid: labels[pid].split("; "))
    attempted = attempted.explode("practice")
    counts = pd.crosstab(attempted["user_id"], attempted["practice"])
    counts = counts.reindex(columns=PR.PRACTICE_NAMES, fill_value=0)
    counts.insert(0, "in_paper_500", counts.index.isin(paper_users))
    return counts


def main():
    args, passthrough = parse_args()
    chosen = [PRACTICE_KEYS[key] for key in args.practices]

    paper_users = paper_user_ids()
    counts = practice_counts(paper_users, args.pool)
    selected = counts[(counts[chosen] >= args.min_problems).all(axis=1)]
    counts.insert(1, "selected", counts.index.isin(selected.index))

    os.makedirs(LIST_DIR, exist_ok=True)
    list_path = os.path.join(LIST_DIR, f"{args.run_name}.txt")
    counts_path = os.path.join(LIST_DIR, f"{args.run_name}_practice_counts.csv")
    with open(list_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(selected.index)) + "\n")
    counts.sort_values("selected", ascending=False).to_csv(counts_path, index_label="user_id")

    pool_name = "the paper's" if args.pool == "paper" else "all"
    print(f"\n{len(selected)} of {pool_name} {len(counts):,} students attempted at least "
          f"{args.min_problems} problem(s) of each of: {', '.join(chosen)}")
    if len(selected):
        if args.pool == "all":
            print(f"({selected['in_paper_500'].sum()} of them are among the paper's 500)")
        print("Problems per practice among them (min / median / max):")
        for name in PR.PRACTICE_NAMES:
            column = selected[name]
            print(f"  {name:<30} {column.min():>4} / {int(column.median()):>4} / {column.max():>4}")
        shown = sorted(selected.index)
        print("user_ids:" + "".join(f"\n  {user}" for user in shown[:50])
              + (f"\n  ... ({len(shown) - 50} more)" if len(shown) > 50 else ""))
    print(f"Saved {list_path}\nSaved {counts_path}")
    if args.list_only or not len(selected):
        return

    shared = ["all", "--user-ids-file", list_path, "--run-name", args.run_name] + \
        ([] if args.with_ped else ["--no-ped"]) + passthrough
    commands = [[sys.executable, BASELINE_SCRIPT] + shared, [sys.executable, PRACTICE_SCRIPT] + shared]

    # Resolve the output CSVs the way the two scripts will (also checks the passed-through options)
    baseline_run = B.resolve_defaults(B.build_parser(B.COMMANDS).parse_args(shared))
    sys_argv, sys.argv = sys.argv, [PRACTICE_SCRIPT] + shared
    try:
        practice_run = PR.parse_args()
    finally:
        sys.argv = sys_argv

    for command in commands:
        print("\nRunning:", " ".join(command))
        if not args.dry_run:
            subprocess.run(command, cwd=B.CODE_DIR, check=True)

    print(f"\nBaseline results:       {baseline_run.csv}")
    print(f"With practice results:  {practice_run.csv}  (includes the change vs baseline)")


if __name__ == "__main__":
    # Write each line right away, also when output goes to a log file (nohup ... > log)
    sys.stdout.reconfigure(line_buffering=True)
    main()
