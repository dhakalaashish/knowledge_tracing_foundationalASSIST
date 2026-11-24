#!/usr/bin/env python3
"""
Agent4CD on the FoundationalASSIST knowledge-tracing benchmark: the inputs of run_kt_agent.py.

The benchmark is the one of Code/kt_practice_benchmark.py: the same paper students (Results/kt_practice_main/
user_ids.txt), the same records and the same targets (50 answers of history, then bins of 10; in each bin the
first correct and the first incorrect answer), built with the paper's own data prep (qwen3_30b_benchmark.iter_prompts
and kt_inference_base.make_process_single_user), so the predictions are scored exactly like the other runs.

Nothing here uses a test student's answers at or after a prediction:
  concepts       the skills of Data/Skills.csv (node codes), numbered 1..K
  KC relations   Eq. 4's statistical relation (prepare_data.kc_relations), from the students OUTSIDE the paper's 500
  profile        Eq. 1-3 from the student's first 50 answers (the history before the first prediction); tertile cuts
                 from the other students' first 50 answers; ability = IRT theta of those 50 answers with the item
                 parameters of Results/kt_profile/problem_irt.json (fitted on the other students, mean 0 / sd 1)
  NCDM tool      the official NeuralCD network (tools/ncdm.py), trained on the other students' first answers (epoch by
                 validation AUC); then frozen, and each test student's mastery vector is fitted on the history before
                 each bin only (theta[b]: records before 50 + 10 b)

Writes data/kt/kt_data.pkl. Run from Code/agent4cd_practice (the GB300 runs it in the container):
    python3 kt_benchmark.py --out-dir ../../Results/kt_practice_main --n 100
"""

import argparse
import math
import os
import random
import sys
from collections import Counter, defaultdict
from types import SimpleNamespace

import numpy as np

from common import CODE_DIR, HERE, load_config, read_json, read_pickle, write_pickle
from agent.learner_profile import build_profile
from prepare_data import kc_relations, profile_statistics
from tools.ncdm import forward_theta, train_ncdm

sys.path.insert(0, str(CODE_DIR))
import kt_practice_benchmark as KP  # noqa: E402
import kt_student_profile as SP  # noqa: E402

B = KP.B
KT_DIR = HERE / "data" / "kt"
KT_DATA = KT_DIR / "kt_data.pkl"
DEFAULT_OUT = os.path.join(KP.REPO_DIR, "Results", "kt_practice_main")
IRT_PATH = os.path.join(KP.REPO_DIR, "Results", "kt_profile", "problem_irt.json")
ABILITY_CUTS = [-0.4307, 0.4307]   # tertiles of N(0, 1): the IRT abilities of the other students have mean 0, sd 1


def kt_args(out_dir, n):
    """The arguments kt_practice_benchmark's helpers expect (its folder of students and staged data)."""
    out_dir = os.path.abspath(out_dir)
    return SimpleNamespace(base_dir=out_dir, out_dir=out_dir, students=0, n=n, seed=2026, force=False, num_gpus=1,
                           gpu_memory_utilization=0.9, max_model_len=None, batch_size=None, max_num_seqs=None,
                           cache_dir=None)


def is_true(value):
    return str(value).strip().lower() in ("true", "1", "1.0")


def missing(value):
    return B.is_missing(value)


# ---------------------------------------------------------------------------------------------- the benchmark

def benchmark_students(out_dir, n):
    """{user: (rows, targets)}: the paper's merged rows of each student (time order) and the metadata of its
    predictions, from the same data prep as qwen3_30b_benchmark.iter_prompts."""
    import pandas as pd
    args = kt_args(out_dir, n)
    KP.cmd_stage(args)
    data_dir, users = KP.kt_data(args), KP.selected(args)
    sys.modules.pop("kt_inference_base", None)
    kt = B.import_kt_base()
    student_df = pd.read_csv(os.path.join(data_dir, kt.STUDENT_FILE))
    student_df = student_df.sort_values(["user_id", "id"]).reset_index(drop=True)
    problems_df = pd.read_csv(os.path.join(data_dir, kt.PROBLEMS_FILE))
    problems_df["cleaned body"] = problems_df["Problem Body"].apply(kt.clean_problem_body)
    problems_df["answer_options"] = problems_df["Multiple Choice Options"].apply(kt.label_answer_options)
    problems_df["correct_answers"] = problems_df.apply(
        lambda row: kt.get_correct_option_letters(row["answer_options"], row["Multiple Choice Answers"])
        if row["Problem Type"] in B.MC_TYPES else row["Fill-in Answers"], axis=1)
    skill_df = pd.read_csv(os.path.join(data_dir, kt.SKILL_FILE))
    problems_df = pd.merge(problems_df, skill_df, on="problem_id", how="left")
    problems_df["answer_options_formatted"] = problems_df["answer_options"].apply(
        lambda x: kt.format_answer_options_for_prompt(x) if pd.notna(x) else None)
    student_df = student_df.sort_values("id").reset_index(drop=True)
    merged_df = student_df.merge(problems_df, on="problem_id", how="inner")
    merged_df["answer_text"] = merged_df.apply(
        lambda row: kt.match_student_answer_to_letters(row["answer_text"], row["answer_options"])
        if row["Problem Type"] in B.MC_TYPES and pd.notna(row["answer_options"]) else row["answer_text"], axis=1)
    merged_df = merged_df[merged_df["user_id"].isin(users)]
    process = kt.make_process_single_user("")
    out = {}
    for user_id, user_df in merged_df.groupby("user_id"):
        rows = user_df.to_dict("records")
        _, metas = process((user_id, rows, B.MIN_HISTORY, B.BIN_SIZE))
        out[user_id] = (rows, [{k: v for k, v in m.items() if k != "prompt"} for m in metas])
    return out


def record_of(row):
    hint = row.get("hint_count")
    return {"problem_id": int(row["problem_id"]), "end_time": str(row["end_time"]),
            "answer": "" if missing(row.get("answer_text")) else str(row["answer_text"]),
            "right": 1 if row.get("discrete_score") == 1 else 0,
            "hint": (not missing(hint)) and float(hint) > 0, "saw": is_true(row.get("saw_answer"))}


def exercise_of(row):
    text = f"Problem Type: {row['Problem Type']}\nProblem: {row['cleaned body']}\n"
    if not missing(row.get("answer_options_formatted")):
        text += f"Answer Options:\n{row['answer_options_formatted']}\n"
    correct = row.get("correct_answers")
    text += f"Correct Answer: {'Not available' if missing(correct) else correct}"
    return {"problem_type": row["Problem Type"], "body": str(row["cleaned body"]), "text": text}


# ---------------------------------------------------------------------------------------------- other students

def other_students(paper_ids):
    """{user: [(problem_id, right), ...]}: the first answer to each problem of every student outside the paper's 500,
    in time order."""
    import pandas as pd
    df = pd.read_csv(os.path.join(B.DATA_DIR, "Interactions.csv"),
                     usecols=["id", "problem_id", "user_id", "discrete_score", "end_time"])
    df = df[~df["user_id"].isin(paper_ids)].dropna(subset=["discrete_score"])
    df = df.sort_values(["user_id", "end_time", "id"]).drop_duplicates(["user_id", "problem_id"], keep="first")
    df["right"] = (df["discrete_score"] >= 1).astype(int)
    return {u: list(zip(g["problem_id"].astype(int).tolist(), g["right"].tolist()))
            for u, g in df.groupby("user_id", sort=False)}


def load_irt():
    problems = read_json(IRT_PATH)["problems"]
    return {int(pid): (v[0], v[1]) for pid, v in problems.items()}


def irt_ability(history, irt):
    """MAP ability (prior N(0, 1)) of the answers whose problem has IRT parameters; Newton steps."""
    items = [(irt[p][0], irt[p][1], y) for p, y in history if p in irt]
    theta = 0.0
    for _ in range(100):
        grad, hess = -theta, -1.0
        for b, a, y in items:
            p = 1.0 / (1.0 + math.exp(-a * (theta - b)))
            grad += a * (y - p)
            hess -= a * a * p * (1 - p)
        step = grad / hess
        theta -= step
        if abs(step) < 1e-8:
            break
    return theta


# ---------------------------------------------------------------------------------------------- NCDM

def train_tool(seqs, q, n_concepts, config):
    """NCDM on the other students' first answers to problems with a skill; 1/8 held out to pick the epoch."""
    ex_index = {pid: i for i, pid in enumerate(sorted(p for p, cids in q.items() if cids))}
    users = {u: i for i, u in enumerate(seqs)}
    rows = [(users[u], ex_index[p], y) for u, s in seqs.items() for p, y in s if p in ex_index]
    random.Random(config["seed"]).shuffle(rows)
    n_val = round(config["val_fraction"] * len(rows))
    records = {"train": np.array(rows[n_val:], dtype=np.int64), "val": np.array(rows[:n_val], dtype=np.int64),
               "test": np.zeros((0, 3), dtype=np.int64), "n_students": len(users), "n_exercises": len(ex_index),
               "n_concepts": n_concepts, "Q": {i: q[p] for p, i in ex_index.items()}}
    print(f"NCDM: {len(records['train']):,} training and {len(records['val']):,} validation answers of "
          f"{len(users):,} other students, {len(ex_index):,} problems, {n_concepts} skills", flush=True)
    return train_ncdm(records, config["ncdm"], config["seed"]), ex_index


def fit_theta(tool, ex_index, recs, n_bins, n_concepts, steps, lr):
    """theta[b] (n_bins x K, in [0, 1]): the student's mastery fitted on the first answers before bin b
    (records < 50 + 10 b) with NCDM's network and exercise parameters frozen. A skill with no answer yet stays 0.5."""
    import torch
    net, kn, device = tool["net"], tool["kn_matrix"], tool["device"]
    first = {}
    for pos, r in enumerate(recs):
        if r["problem_id"] in ex_index and r["problem_id"] not in first:
            first[r["problem_id"]] = (pos, r["right"])
    bins, ex, ys = [], [], []
    for b in range(n_bins):
        end = B.MIN_HISTORY + b * B.BIN_SIZE
        for pid, (pos, y) in first.items():
            if pos < end:
                bins.append(b)
                ex.append(ex_index[pid])
                ys.append(float(y))
    emb = torch.zeros(n_bins, n_concepts, device=device, requires_grad=True)
    if not bins:
        return torch.sigmoid(emb).detach().cpu().numpy()
    bt = torch.tensor(bins, device=device)
    et = torch.tensor(ex, device=device)
    yt = torch.tensor(ys, device=device)
    count = torch.bincount(bt, minlength=n_bins).clamp(min=1).float()
    optimizer = torch.optim.Adam([emb], lr=lr)
    for _ in range(steps):
        optimizer.zero_grad()
        p = forward_theta(net, torch.sigmoid(emb[bt]), et, kn[et]).clamp(1e-6, 1 - 1e-6)
        loss = (-(yt * torch.log(p) + (1 - yt) * torch.log(1 - p)) / count[bt]).sum()   # each bin's mean, summed
        loss.backward()
        optimizer.step()
    return torch.sigmoid(emb).detach().cpu().numpy()


# ---------------------------------------------------------------------------------------------- main

def prepare(out_dir, n, force=False):
    config = load_config()
    students = benchmark_students(out_dir, n)
    users = sorted(students)
    if KT_DATA.exists() and not force:
        saved = read_pickle(KT_DATA)
        if saved.get("users") == users:
            print(f"Already prepared for these {len(users)} students: {KT_DATA} (--force to rebuild)")
            return saved
    by_pid, names = SP.load_skills()
    codes = sorted({c for cs in by_pid.values() for c in cs})
    cid = {c: i + 1 for i, c in enumerate(codes)}
    n_concepts = len(codes)
    concepts = {str(cid[c]): {"code": c, "name": f"{c} {names.get(c, '')}".strip()} for c in codes}
    q = {pid: [cid[c] for c in cs] for pid, cs in by_pid.items()}

    records, targets, exercises = {}, {}, {}
    for u in users:
        rows, metas = students[u]
        records[u] = [record_of(r) for r in rows]
        targets[u] = metas
        for r in rows:
            exercises.setdefault(int(r["problem_id"]), exercise_of(r))
    for pid in exercises:
        q.setdefault(pid, [])
    n_targets = sum(len(t) for t in targets.values())
    print(f"{len(users)} students, {sum(len(r) for r in records.values()):,} records, {n_targets:,} targets", flush=True)

    paper_ids = set(B.read_user_ids(os.path.join(B.PAPER_REF_DIR, "paper_user_ids.txt")))
    assert not paper_ids.isdisjoint(users) and set(users) <= paper_ids
    seqs = other_students(paper_ids)
    print(f"Other students: {len(seqs):,}, {sum(len(s) for s in seqs.values()):,} first answers", flush=True)
    qd = defaultdict(list, q)

    relations = kc_relations(seqs, qd, n_concepts, config.get("relation_threshold"))
    print(f"KC relations: {relations['num_edges']} edges (threshold {relations['threshold']:.4f})", flush=True)

    n_exercises = len({p for s in seqs.values() for p, _ in s} | set(exercises))
    _, thresholds = profile_statistics({u: s[:B.MIN_HISTORY] for u, s in seqs.items() if s}, qd, n_exercises, n_concepts)
    first50 = {u: [(r["problem_id"], r["right"]) for r in records[u][:B.MIN_HISTORY]] for u in users}
    stats, _ = profile_statistics(first50, qd, n_exercises, n_concepts)
    irt = load_irt()
    profiles = {u: build_profile(stats[u], thresholds, irt_ability(first50[u], irt), ABILITY_CUTS, concepts)
                for u in users}
    print("Profile levels: " + "; ".join(
        f"{key} " + ", ".join(f"{k} {v}" for k, v in sorted(Counter(p["levels"][key] for p in profiles.values()).items(),
                                                             key=lambda kv: str(kv[0])))
        for key in ("activity", "diversity", "success", "ability")), flush=True)

    tool, ex_index = train_tool(seqs, q, n_concepts, config)
    print(f"NCDM: best epoch {tool['best_epoch']}, validation AUC {tool['val_auc']:.4f}, ACC {tool['val_acc']:.4f}",
          flush=True)
    for p in tool["net"].parameters():
        p.requires_grad_(False)
    tool["net"].eval()
    fit = config["kt"]["theta_fit"]
    theta = {}
    for i, u in enumerate(users, 1):
        n_bins = (len(records[u]) - B.MIN_HISTORY) // B.BIN_SIZE
        theta[u] = fit_theta(tool, ex_index, records[u], max(n_bins, 0), n_concepts, fit["steps"], fit["lr"])
        if i % 20 == 0 or i == len(users):
            print(f"  mastery fitted per bin: {i}/{len(users)} students", flush=True)
    for u in users:   # every target's bin has a mastery row
        assert all(t["bin_number"] < len(theta[u]) for t in targets[u])

    data = {"users": users, "records": records, "targets": targets, "exercises": exercises, "concepts": concepts,
            "q": q, "related": relations["related"], "profiles": profiles, "theta": theta,
            "ncdm": {"best_epoch": tool["best_epoch"], "val_auc": tool["val_auc"], "val_acc": tool["val_acc"]},
            "relations": {k: relations[k] for k in ("threshold", "num_edges", "num_transition_pairs")}}
    write_pickle(KT_DATA, data)
    print(f"Wrote {KT_DATA}", flush=True)
    return data


def main():
    ap = argparse.ArgumentParser(description="Agent4CD inputs for the KT benchmark (the 100 paper students)")
    ap.add_argument("--out-dir", default=DEFAULT_OUT, help="kt_practice_benchmark's folder (student list, staged data)")
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--force", action="store_true", help="rebuild even if data/kt/kt_data.pkl is there")
    args, _ = ap.parse_known_args()
    prepare(args.out_dir, args.n, args.force)


if __name__ == "__main__":
    main()
