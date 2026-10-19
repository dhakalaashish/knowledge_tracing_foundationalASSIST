"""
Save a fixed list of learners, so later experiments (e.g. a practice version of the agent) run on
exactly the same learners. The learners are the first --n of prepare_data.py's seeded random order
of the split's learners with test records, so a list of 50 is contained in the default 300.

Run from Code/agent4cd_practice after prepare_data.py:
    python3 make_learner_list.py --split standard --n 50
writes learners/<split>_<n>.json (keep it in git). Use it with
    python3 run_agent.py --split standard --run-name pilot50 --learner-file learners/standard_50.json

Each learner is stored by its index in maca_cd's data (the student id in the pickles) and by its
student_id in maca_cd/data/cleaned_data.csv, which does not depend on the split.
"""

import argparse

import numpy as np

from common import HERE, SPLITS, data_dir, load_config, read_pickle, write_json


def main():
    config = load_config()
    parser = argparse.ArgumentParser(description="Save a fixed list of learners for Agent4CD runs")
    parser.add_argument("--split", default=config["split"], choices=SPLITS)
    parser.add_argument("--n", type=int, default=50)
    args = parser.parse_args()

    data = read_pickle(data_dir(args.split) / "students.pkl")
    learners = data["student_order"][:args.n]
    test_counts = [len(data["test"][s]) for s in learners]
    rows = [{"student": s, "cleaned_student_id": data["student_ids"][s],
             "history_records": len(data["history"][s]), "test_records": len(data["test"][s])}
            for s in learners]
    path = HERE / "learners" / f"{args.split}_{args.n}.json"
    write_json(path, {
        "split": args.split, "seed": config["seed"], "n": len(rows),
        "selection": "first n of prepare_data.py's seeded random order of learners with test records",
        "total_test_records": int(sum(test_counts)),
        "learners": rows,
    })
    print(f"{len(rows)} learners, {sum(test_counts)} test records "
          f"(per learner: median {np.median(test_counts):.0f}, mean {np.mean(test_counts):.1f}, "
          f"max {max(test_counts)})")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
