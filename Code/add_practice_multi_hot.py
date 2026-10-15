"""
Multi-hot practice column computed from the zero-shot practice scores.

mathematical_practice holds six scores per problem, in the order of PRACTICE_NAMES in
augment_mathematical_practice.py (Representing, Abstracting and Generalizing, Justifying and Proving,
Mathematical Modeling, Collaborative Mathematics, Procedural Fluency). practice_multi_hot, placed
right after it in the same format (e.g. "[0, 0, 0, 0, 0, 1]"), marks:
  - every practice scored at or above the threshold (0.7);
  - if no practice reaches the threshold, the highest-scored practice. When several practices share
    the highest score (for example, all six are equal), one of them is chosen at random. The random
    choice is seeded by the seed and the problem_id, so a problem always gets the same choice.
Rows without scores get an empty cell.

augment_mathematical_practice.py and evaluate_mathematical_practice_naep.py call add_multi_hot_column
before every save, so the column always matches the scores they write. Run this script directly to
add or recompute the column in an existing Problems.csv:
    python3 add_practice_multi_hot.py --data-dir ../Data --dry-run   # summary only, writes nothing
    python3 add_practice_multi_hot.py --data-dir ../Data
"""

import argparse
import json
import os
import random

import pandas as pd

PROBLEMS_FILE = "Problems.csv"
SCORE_COLUMN = "mathematical_practice"
MULTI_HOT_COLUMN = "practice_multi_hot"
PRACTICE_NAMES = [
    "Representing",
    "Abstracting and Generalizing",
    "Justifying and Proving",
    "Mathematical Modeling",
    "Collaborative Mathematics",
    "Procedural Fluency",
]
DEFAULT_THRESHOLD = 0.7
DEFAULT_SEED = 2025


def multi_hot(scores, threshold, rng):
    """Returns (multi-hot list, how it was chosen: 'threshold', 'highest' or 'random tie')."""
    hot = [1 if score >= threshold else 0 for score in scores]
    if any(hot):
        return hot, "threshold"
    top = max(scores)
    tied = [i for i, score in enumerate(scores) if score == top]
    hot[rng.choice(tied)] = 1
    return hot, "highest" if len(tied) == 1 else "random tie"


def add_multi_hot_column(problems_df, score_column=SCORE_COLUMN, threshold=DEFAULT_THRESHOLD,
                         seed=DEFAULT_SEED):
    """
    Sets problems_df[MULTI_HOT_COLUMN] (in place) from the scores in score_column. A new column is
    inserted right after score_column; an existing one keeps its position. Rows whose scores are
    empty or not a list of len(PRACTICE_NAMES) numbers get an empty cell (check_output_frame reports
    malformed scores). Returns a summary dict.
    """
    column = []
    stats = {
        "rules": {"threshold": 0, "highest": 0, "random tie": 0, "no scores": 0},
        "practice_counts": [0] * len(PRACTICE_NAMES),
        "hot_counts": {},
        "random_ties": [],
    }
    for problem_id, cell in zip(problems_df["problem_id"], problems_df[score_column]):
        try:
            scores = [float(score) for score in json.loads(cell)]
        except (TypeError, ValueError):
            scores = None
        if not scores or len(scores) != len(PRACTICE_NAMES):
            column.append("")
            stats["rules"]["no scores"] += 1
            continue
        rng = random.Random(f"{seed}-{str(problem_id).strip()}")
        hot, rule = multi_hot(scores, threshold, rng)
        stats["rules"][rule] += 1
        if rule == "random tie":
            stats["random_ties"].append((problem_id, max(scores), PRACTICE_NAMES[hot.index(1)]))
        for i, value in enumerate(hot):
            stats["practice_counts"][i] += value
        stats["hot_counts"][sum(hot)] = stats["hot_counts"].get(sum(hot), 0) + 1
        column.append(json.dumps(hot))

    if MULTI_HOT_COLUMN in problems_df.columns:
        problems_df[MULTI_HOT_COLUMN] = column
    else:
        problems_df.insert(problems_df.columns.get_loc(score_column) + 1, MULTI_HOT_COLUMN, column)
    return stats


def print_multi_hot_summary(stats, threshold=DEFAULT_THRESHOLD):
    rules = stats["rules"]
    for problem_id, top, chosen in stats["random_ties"]:
        print(f"problem {problem_id}: all highest scores tied at {top}, chose {chosen} at random")
    print(f"{MULTI_HOT_COLUMN}:")
    print(f"  at least one practice >= {threshold}: {rules['threshold']}")
    print(f"  none >= {threshold}, single highest:     {rules['highest']}")
    print(f"  none >= {threshold}, random among tied:  {rules['random tie']}")
    print(f"  no scores (left empty):        {rules['no scores']}")
    print("  practices marked per problem: " +
          ", ".join(f"{count}: {n}" for count, n in sorted(stats["hot_counts"].items())))
    print("  problems marked with each practice:")
    for name, count in zip(PRACTICE_NAMES, stats["practice_counts"]):
        print(f"    {name:30s} {count}")


def parse_args():
    parser = argparse.ArgumentParser(description="Add or recompute the multi-hot practice column in Problems.csv")
    parser.add_argument("--data-dir", "-d", default=".",
                        help=f"Directory containing {PROBLEMS_FILE} (default: current directory)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Scores at or above this are 1 (default: {DEFAULT_THRESHOLD})")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help=f"Seed for breaking ties among equal highest scores (default: {DEFAULT_SEED})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the summary without writing Problems.csv")
    return parser.parse_args()


def main():
    args = parse_args()
    problems_csv = os.path.join(args.data_dir, PROBLEMS_FILE)

    # Read every cell as text so the other columns are written back unchanged
    problems_df = pd.read_csv(problems_csv, dtype=str, keep_default_na=False)
    if SCORE_COLUMN not in problems_df.columns:
        raise SystemExit(f"{problems_csv} has no {SCORE_COLUMN} column; run augment_mathematical_practice.py first")

    stats = add_multi_hot_column(problems_df, threshold=args.threshold, seed=args.seed)
    print(f"Problems: {len(problems_df)}")
    print_multi_hot_summary(stats, args.threshold)

    if args.dry_run:
        print("\nDry run: Problems.csv not written")
        return
    # Same writing as augment_mathematical_practice.py: atomic, utf-8, \n line endings
    tmp_path = problems_csv + ".tmp"
    problems_df.to_csv(tmp_path, index=False, encoding="utf-8", lineterminator="\n")
    os.replace(tmp_path, problems_csv)
    print(f"\nWrote {MULTI_HOT_COLUMN} to {problems_csv}")


if __name__ == "__main__":
    main()
