"""Paths, config and metrics shared by the Agent4CD scripts."""

import json
import os
import pickle
from pathlib import Path

import numpy as np
from sklearn.metrics import f1_score, roc_auc_score

HERE = Path(__file__).resolve().parent              # Code/agent4cd_practice
CODE_DIR = HERE.parent                              # Code/
MACA_CD_DIR = CODE_DIR / "maca_cd"
PROBLEMS_CSV = CODE_DIR.parent / "Data" / "Problems.csv"
SPLITS = ("standard", "cold", "zeroshot", "colditem")
ABLATIONS = ("none", "no_profile", "no_reasoning", "no_affect", "no_reflection")
TOOLS = ("ncdm", "maca_cd")


def load_config(path=None):
    with open(path or HERE / "config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def data_dir(split):
    """prepare_data.py output for one split."""
    return HERE / "data" / split


def tool_dir(split):
    """train_tools.py output (IRT and NCDM) for one split."""
    return HERE / "tool_outputs" / split


def run_dir(split, run_name):
    """run_agent.py and evaluate.py output for one run."""
    return HERE / "results" / split / run_name


def maca_cd_state_file(split, seed=None):
    """Proficiency and test predictions saved by maca_cd/model/train.py at its best epoch."""
    name = "state_" + split + ("" if seed is None else "_seed%d" % seed) + ".npz"
    return MACA_CD_DIR / "model" / "results" / "OurModel" / name


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def read_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def write_pickle(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def tier(value):
    """Mastery tier of a tool's proficiency value (Agent4Edu's knowledge_proficiency.tier)."""
    if value is None:
        return "unknown"
    if value > 0.66:
        return "good"
    if value > 0.33:
        return "common"
    return "poor"


def binary_metrics(labels, probs=None, preds=None):
    """
    ACC and F1 (the paper's metrics) and AUC. preds are 0/1 decisions (default: probs >= 0.5);
    AUC needs probs and both classes.
    """
    labels = np.asarray(labels, dtype=int)
    if preds is None:
        preds = (np.asarray(probs, dtype=float) >= 0.5).astype(int)
    preds = np.asarray(preds, dtype=int)
    result = {
        "n": int(len(labels)),
        "ACC": float((preds == labels).mean()) if len(labels) else float("nan"),
        "F1": float(f1_score(labels, preds, zero_division=0)) if len(labels) else float("nan"),
        "AUC": float("nan"),
    }
    if probs is not None and len(set(labels.tolist())) == 2:
        result["AUC"] = float(roc_auc_score(labels, np.asarray(probs, dtype=float)))
    return result
