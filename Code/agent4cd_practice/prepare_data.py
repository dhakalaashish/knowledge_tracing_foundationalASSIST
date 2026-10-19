"""
Build the Agent4CD inputs for one maca_cd split, so Agent4CD is evaluated on exactly the test
records MACA-CD is evaluated on.

Reads (all produced on the A100 by the maca_cd pipeline):
    ../maca_cd/data/preprocessed/<split>_spilt.pkl   train/test records [student, exercise, y, concept] and Q_matrix
    ../maca_cd/data/cleaned_data.csv                 time order and raw problem_id of every record
    ../maca_cd/data/graph/concept_data.json          concept ids, codes and names
    ../../Data/Problems.csv                          problem text

Writes data/<split>/:
    records.pkl       train / val / test arrays (student, exercise, y) for the tools, and the Q-matrix.
                      val is a seeded val_fraction of maca_cd's training records (70/10/20 overall).
    students.pkl      per student: history (all non-test records) and test records, in time order;
                      the seeded order in which students are simulated; profile statistics (Eq. 1)
    exercises.json    per exercise: problem_id, concept ids, prompt text
    concepts.json     per concept id: node_code and name
    kc_relations.json the KC relation R used to reinforce factual memory (Eq. 4)

Run from Code/agent4cd_practice:
    python3 prepare_data.py --split standard
"""

import argparse
import random
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

from common import (CODE_DIR, MACA_CD_DIR, PROBLEMS_CSV, SPLITS, data_dir, load_config, read_json,
                    read_pickle, write_json, write_pickle)

sys.path.insert(0, str(CODE_DIR))  # clean_utils.py, augment_mathematical_practice.py

from augment_mathematical_practice import format_choices_and_answer, mark_answer_blanks  # noqa: E402
from clean_utils import clean_problem_body  # noqa: E402


def parse_args(config):
    parser = argparse.ArgumentParser(description="Build the Agent4CD inputs for one maca_cd split")
    parser.add_argument("--split", default=config["split"], choices=SPLITS)
    return parser.parse_args()


def load_records(split, code2id):
    """
    maca_cd's split records, with each record's time order and problem_id from cleaned_data.csv.
    The id mapping is rebuilt exactly as maca_cd/data/data_preprocess.py builds it (first-appearance
    order of student_id and question_id), then checked against the pickle record by record.
    """
    cleaned = pd.read_csv(MACA_CD_DIR / "data" / "cleaned_data.csv",
                          dtype={"concept_codes": str, "problem_id": str, "end_time": str})
    assert set(cleaned["score"].unique()) <= {0, 1} and (cleaned["full_score"] == 1).all()
    user_mapping = {sid: i for i, sid in enumerate(cleaned["student_id"].unique())}
    q_mapping = {qid: i for i, qid in enumerate(cleaned["question_id"].unique())}
    students = cleaned["student_id"].map(user_mapping).to_numpy()
    exercises = cleaned["question_id"].map(q_mapping).to_numpy()
    scores = cleaned["score"].to_numpy()

    # cleaned_data.csv is sorted by end_time (then interaction id), so its row number is the time order
    row_of = {(int(s), int(e)): row for row, (s, e) in enumerate(zip(students, exercises))}
    assert len(row_of) == len(cleaned), "a (student, exercise) pair appears twice in cleaned_data.csv"

    split_data = read_pickle(MACA_CD_DIR / "data" / "preprocessed" / f"{split}_spilt.pkl")
    train, test = split_data["train"], split_data["test"]
    assert len(train) + len(test) == len(cleaned), "the split does not cover cleaned_data.csv"
    for record in train + test:
        row = row_of[(int(record[0]), int(record[1]))]
        assert int(scores[row]) == int(record[2]), f"score mismatch for record {record}"

    q_matrix = {int(e): sorted(int(c) for c in cids) for e, cids in split_data["Q_matrix"].items()}
    problem_of = {}
    for e, pid, codes in zip(exercises, cleaned["problem_id"], cleaned["concept_codes"]):
        e = int(e)
        if e not in problem_of:
            problem_of[e] = pid.strip()
            assert q_matrix[e] == sorted(code2id[c] for c in codes.split("|")), f"Q mismatch for exercise {e}"
    student_ids = [int(sid) for sid in user_mapping]  # learner index -> student_id in cleaned_data.csv
    return train, test, row_of, q_matrix, problem_of, student_ids, len(q_mapping)


def exercise_texts(problem_of):
    """Prompt text of each exercise: type, answer type, problem, choices and correct answer."""
    problems = pd.read_csv(PROBLEMS_CSV, dtype=str, keep_default_na=False)
    problems["problem_id"] = problems["problem_id"].str.strip()
    problems = problems.drop_duplicates("problem_id").set_index("problem_id", drop=False)
    texts, missing = {}, 0
    for e, pid in problem_of.items():
        if pid not in problems.index:
            missing += 1
            texts[e] = {"body": "(problem text not available)", "text": "(problem text not available)"}
            continue
        row = problems.loc[pid]
        body = clean_problem_body(mark_answer_blanks(row["Problem Body"]))
        choices, correct = format_choices_and_answer(row)
        text = f"Problem Type: {row['Problem Type']}\nAnswer Type: {row['Answer Types']}\nProblem:\n{body}\n"
        if choices:
            text += f"Answer Choices:\n{choices}\n"
        text += f"Correct Answer:\n{correct or 'Not available'}"
        texts[e] = {"body": body, "text": text}
    return texts, missing


def kc_relations(history, q_matrix, n_concepts, threshold=None):
    """
    Statistical KC relation (Eq. 4, after RCD): for consecutive records of a student that were both
    answered correctly, count transitions concept i -> concept j (i != j). C_ij = n_ij / sum_k n_ik.
    i -> j is an edge when C_ij > threshold (default: mean + std of the non-zero C_ij).
    Two concepts are related when they are equal or an edge joins them in either direction.
    """
    counts = np.zeros((n_concepts + 1, n_concepts + 1))
    for records in history.values():
        for (e1, y1), (e2, y2) in zip(records, records[1:]):
            if y1 == 1 and y2 == 1:
                for i in q_matrix[e1]:
                    for j in q_matrix[e2]:
                        if i != j:
                            counts[i, j] += 1
    totals = counts.sum(axis=1, keepdims=True)
    share = np.divide(counts, totals, out=np.zeros_like(counts), where=totals > 0)
    nonzero = share[share > 0]
    if threshold is None:
        threshold = float(nonzero.mean() + nonzero.std()) if len(nonzero) else 0.0
    edges = [[int(i), int(j), round(float(share[i, j]), 4)] for i, j in zip(*np.nonzero(share > threshold))]
    related = defaultdict(set)
    for i, j, _ in edges:
        related[i].add(j)
        related[j].add(i)
    return {
        "threshold": threshold,
        "num_transition_pairs": int(len(nonzero)),
        "num_edges": len(edges),
        "edges": edges,
        "related": {str(c): sorted(related[c]) for c in range(1, n_concepts + 1)},
    }


def profile_statistics(history, q_matrix, n_exercises, n_concepts):
    """Eq. 1 on each student's history: activity |E_s|/|E|, diversity |K_s|/|KC|, success rate."""
    stats = {}
    for s, records in history.items():
        concept_counts = Counter(c for e, _ in records for c in q_matrix[e])
        stats[s] = {
            "num_records": len(records),
            "activity": len({e for e, _ in records}) / n_exercises,
            "diversity": len(concept_counts) / n_concepts,
            "success": (sum(y for _, y in records) / len(records)) if records else None,
            "preference_concept": concept_counts.most_common(1)[0][0] if concept_counts else None,
        }
    thresholds = {}
    for key in ("activity", "diversity", "success"):
        values = [v[key] for v in stats.values() if v[key] is not None and v["num_records"] > 0]
        thresholds[key] = [float(q) for q in np.quantile(values, [1 / 3, 2 / 3])]
    return stats, thresholds


def main():
    config = load_config()
    args = parse_args(config)
    split = args.split
    concept_data = read_json(MACA_CD_DIR / "data" / "graph" / "concept_data.json")
    code2id = concept_data["code2id"]
    n_concepts = len(code2id)
    concepts = {}
    for code, cid in code2id.items():
        concepts[str(cid)] = {"code": code, "name": concept_data["concept_names"][cid - 1]}

    train, test, row_of, q_matrix, problem_of, student_ids, n_exercises = load_records(split, code2id)
    n_students = len(student_ids)
    print(f"Split {split}: {len(train)} train and {len(test)} test records; "
          f"{n_students} students, {n_exercises} exercises, {n_concepts} concepts")

    # Validation records for picking the tools' epoch (the agent's history keeps them)
    rng = random.Random(config["seed"])
    order = list(range(len(train)))
    rng.shuffle(order)
    val_index = set(order[:round(config["val_fraction"] * len(train))])
    arrays = {"train": [], "val": [], "test": []}
    for idx, record in enumerate(train):
        arrays["val" if idx in val_index else "train"].append(record[:3])
    arrays["test"] = [record[:3] for record in test]
    records = {name: np.array(rows, dtype=np.int64).reshape(-1, 3) for name, rows in arrays.items()}
    records.update({"n_students": n_students, "n_exercises": n_exercises, "n_concepts": n_concepts,
                    "Q": q_matrix})
    print("Tool records: train {}, val {}, test {}".format(*(len(records[k]) for k in ("train", "val", "test"))))

    # Per-student sequences in time order: history = all non-test records, test = test records
    history, test_seq = defaultdict(list), defaultdict(list)
    for target, source in ((history, train), (test_seq, test)):
        for s, e, y, *_ in source:
            target[int(s)].append((row_of[(int(s), int(e))], int(e), int(y)))
    history = {s: [(e, y) for _, e, y in sorted(recs)] for s, recs in history.items()}
    test_seq = {s: [(e, y) for _, e, y in sorted(recs)] for s, recs in test_seq.items()}
    for s in range(n_students):
        history.setdefault(s, [])
    student_order = sorted(test_seq)
    random.Random(config["seed"]).shuffle(student_order)

    stats, thresholds = profile_statistics(history, q_matrix, n_exercises, n_concepts)
    relations = kc_relations(history, q_matrix, n_concepts, config.get("relation_threshold"))
    texts, missing = exercise_texts(problem_of)
    exercises = {str(e): {"problem_id": problem_of[e], "concepts": q_matrix[e], **texts[e]}
                 for e in sorted(problem_of)}

    out = data_dir(split)
    write_pickle(out / "records.pkl", records)
    write_pickle(out / "students.pkl", {
        "history": history, "test": test_seq, "student_order": student_order, "student_ids": student_ids,
        "profile_stats": stats, "profile_thresholds": thresholds,
    })
    write_json(out / "exercises.json", exercises)
    write_json(out / "concepts.json", concepts)
    write_json(out / "kc_relations.json", relations)

    n_test = [len(test_seq[s]) for s in student_order[:config["num_students"]]]
    print(f"Students with test records: {len(student_order)}; the first {config['num_students']} "
          f"have {sum(n_test)} test records (mean {np.mean(n_test):.1f} per student)")
    print(f"Profile tertiles: " + ", ".join(f"{k} {v[0]:.3f}/{v[1]:.3f}" for k, v in thresholds.items()))
    print(f"KC relations: {relations['num_edges']} edges out of {relations['num_transition_pairs']} "
          f"observed transitions (threshold {relations['threshold']:.4f})")
    if missing:
        print(f"WARNING: {missing} exercises have no row in Problems.csv")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
