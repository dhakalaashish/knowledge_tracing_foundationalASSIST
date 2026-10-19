"""
Train the agent's external tools on one split (after prepare_data.py):
    IRT 2PL  -> the learner's ability P^ab_s for the profile (Eq. 2)     tool_outputs/<split>/irt.npz
    NCDM     -> the knowledge state theta (students x concepts)          tool_outputs/<split>/ncdm.npz
Both train on the train records, pick their epoch on the validation records, and store their
probability for every test record (the same-record baselines of evaluate.py).
NCDM is skipped with --skip-ncdm (e.g. when knowledge_tool is maca_cd).

Run from Code/agent4cd_practice, before starting the vLLM server (or with --device cpu):
    python3 train_tools.py --split standard
"""

import argparse

import numpy as np

from common import SPLITS, binary_metrics, data_dir, load_config, read_pickle, tool_dir
from tools.irt import train_irt
from tools.ncdm import train_ncdm


def parse_args(config):
    parser = argparse.ArgumentParser(description="Train the IRT and NCDM tools of Agent4CD")
    parser.add_argument("--split", default=config["split"], choices=SPLITS)
    parser.add_argument("--skip-ncdm", action="store_true", help="Only train IRT")
    parser.add_argument("--device", default=None, help="Override the device of both tools, e.g. cpu")
    return parser.parse_args()


def report(name, result, records):
    test = binary_metrics(records["test"][:, 2], probs=result["test_pred"])
    print(f"{name}: best epoch {result['best_epoch']}  val AUC {result['val_auc']:.4f}  "
          f"test ACC {test['ACC']:.4f}  F1 {test['F1']:.4f}  AUC {test['AUC']:.4f}")


def main():
    config = load_config()
    args = parse_args(config)
    if args.device:
        config["irt"]["device"] = config["ncdm"]["device"] = args.device
    records = read_pickle(data_dir(args.split) / "records.pkl")
    out = tool_dir(args.split)
    out.mkdir(parents=True, exist_ok=True)

    irt = train_irt(records, config["irt"], config["seed"])
    np.savez(out / "irt.npz", ability=irt["ability"], discrimination=irt["discrimination"],
             difficulty=irt["difficulty"], test_pred=irt["test_pred"],
             best_epoch=irt["best_epoch"], val_auc=irt["val_auc"])
    report("IRT", irt, records)

    # IRT ability should rise with the success rate on the training records
    train = records["train"]
    counts = np.bincount(train[:, 0], minlength=records["n_students"])
    correct = np.bincount(train[:, 0], weights=train[:, 2], minlength=records["n_students"])
    seen = counts > 0
    print(f"IRT ability vs training success rate: Pearson r = "
          f"{np.corrcoef(irt['ability'][seen], correct[seen] / counts[seen])[0, 1]:.3f}")

    if not args.skip_ncdm:
        ncdm = train_ncdm(records, config["ncdm"], config["seed"])
        np.savez(out / "ncdm.npz", proficiency=ncdm["proficiency"], test_pred=ncdm["test_pred"],
                 best_epoch=ncdm["best_epoch"], val_auc=ncdm["val_auc"])
        report("NCDM", ncdm, records)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
