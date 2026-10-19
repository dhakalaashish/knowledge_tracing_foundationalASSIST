"""
Evaluate Agent4CD runs on one split.

For each run: ACC and F1 (the paper's metrics, from the agent's Yes/No answers) and AUC (from P(Yes),
the probability of the Yes token). The tools are scored on exactly the same test records, so the rows
are comparable: IRT, NCDM (train_tools.py) and MACA-CD (if maca_cd saved its state for the split).
With several runs (e.g. the ablations), all rows use the records every run has finished.

Usage (from Code/agent4cd_practice):
    python3 evaluate.py --split standard --run-name full
    python3 evaluate.py --split standard --run-name full no_affect no_reflection offline

Writes results/<split>/<run>/predictions.csv and metrics.json for each run, and
results/<split>/evaluation_<runs>.md with the table.
"""

import argparse
import json

import numpy as np
import pandas as pd

from common import (SPLITS, binary_metrics, data_dir, load_config, maca_cd_state_file, read_json, read_pickle,
                    run_dir, tool_dir, write_json)


def parse_args(config):
    parser = argparse.ArgumentParser(description="Evaluate Agent4CD runs against the tools on the same records")
    parser.add_argument("--split", default=config["split"], choices=SPLITS)
    parser.add_argument("--run-name", nargs="+", required=True)
    return parser.parse_args()


def load_steps(out):
    steps = {}
    for path in sorted((out / "students").glob("*.jsonl")):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    break
                if entry["type"] == "step":
                    steps[(entry["student"], entry["exercise"])] = entry
    return steps


def tool_predictions(split, records, maca_cd_seed):
    """{name: probabilities aligned with records['test']} for the tools whose outputs exist."""
    tools = {}
    for name, file in (("IRT", "irt.npz"), ("NCDM", "ncdm.npz")):
        path = tool_dir(split) / file
        if path.exists():
            tools[name] = np.load(path)["test_pred"]
    path = maca_cd_state_file(split, maca_cd_seed)
    if path.exists():
        state = np.load(path)
        if np.array_equal(state["test_records"][:, :3], records["test"]):
            tools["MACA-CD"] = state["test_pred"]
        else:
            print(f"Skipping MACA-CD: {path} has other test records")
    return tools


def fmt(value):
    return "nan" if value != value else f"{value:.4f}"


def main():
    config = load_config()
    args = parse_args(config)
    split = args.split
    records = read_pickle(data_dir(split) / "records.pkl")
    index = {(int(s), int(e)): i for i, (s, e, _) in enumerate(records["test"])}

    runs = {}
    for name in args.run_name:
        out = run_dir(split, name)
        settings = read_json(out / "run_config.json")["settings"]
        steps = load_steps(out)
        if not steps:
            raise SystemExit(f"{out} has no finished test records")
        runs[name] = (settings, steps)
    keys = sorted(set.intersection(*(set(steps) for _, steps in runs.values())))
    print(f"Split {split}: {len(keys)} test records finished by every run "
          f"({len({s for s, _ in keys})} learners)")
    rows_idx = np.array([index[k] for k in keys])
    truth = records["test"][rows_idx, 2]

    maca_seed = next((s["maca_cd_seed"] for s, _ in runs.values() if s["knowledge_tool"] == "maca_cd"),
                     config.get("maca_cd_seed"))
    tools = tool_predictions(split, records, maca_seed)

    table = []
    for name, (settings, steps) in runs.items():
        chosen = [steps[k] for k in keys]
        metrics = binary_metrics(truth, probs=[s["p_yes"] for s in chosen], preds=[s["prediction"] for s in chosen])
        agent = settings["agent"]
        label = (f"Agent4CD [{name}] (tool {settings['knowledge_tool']}, "
                 f"{'online' if agent['online_feedback'] else 'offline'}, ablation {agent['ablation']})")
        table.append((label, metrics))

        # Per-run outputs over all of the run's own records
        all_keys = sorted(steps)
        all_rows = np.array([index[k] for k in all_keys])
        frame = pd.DataFrame({
            "student": [k[0] for k in all_keys], "exercise": [k[1] for k in all_keys],
            "truth": [steps[k]["truth"] for k in all_keys],
            "prediction": [steps[k]["prediction"] for k in all_keys],
            "p_yes": [steps[k]["p_yes"] for k in all_keys],
            "affect": [steps[k].get("task2") for k in all_keys],
            "fallback": [steps[k].get("fallback", False) for k in all_keys],
        })
        for tool_name, probs in tools.items():
            frame[tool_name] = probs[all_rows]
        out = run_dir(split, name)
        frame.to_csv(out / "predictions.csv", index=False)

        own = binary_metrics(frame["truth"], probs=frame["p_yes"], preds=frame["prediction"])
        affect = {}
        for state, group in frame.groupby(frame["affect"].fillna("(none)")):
            affect[state] = {"n": int(len(group)), "share": len(group) / len(frame),
                             "actual_correct_rate": float(group["truth"].mean()),
                             "agent_ACC": float((group["prediction"] == group["truth"]).mean())}
        steps_list = list(steps.values())
        summary = {
            "settings": settings, "metrics_all_records": own,
            "tools_all_records": {t: binary_metrics(frame["truth"], probs=frame[t]) for t in tools},
            "fallbacks": int(frame["fallback"].sum()),
            "mean_output_tokens_per_record": float(np.mean([s["completion_tokens"] for s in steps_list])),
            "mean_prompt_tokens_per_record": float(np.mean([s["prompt_tokens"] for s in steps_list])),
            "affect": affect,
        }
        write_json(out / "metrics.json", summary)
        print(f"\n[{name}] {len(frame)} records, {summary['fallbacks']} answered by the tool fallback, "
              f"{summary['mean_prompt_tokens_per_record']:.0f} prompt / "
              f"{summary['mean_output_tokens_per_record']:.0f} output tokens per record")
        print("  affect          n   share  correct  agent ACC")
        for state, a in sorted(affect.items(), key=lambda item: -item[1]["n"]):
            print(f"  {state:<12} {a['n']:>6}  {a['share']:6.1%}  {a['actual_correct_rate']:7.3f}  {a['agent_ACC']:9.4f}")

    for tool_name, probs in tools.items():
        table.append((tool_name, binary_metrics(truth, probs=probs[rows_idx])))

    lines = ["| Method | n | ACC | F1 | AUC |", "|---|---|---|---|---|"]
    lines += [f"| {label} | {m['n']} | {fmt(m['ACC'])} | {fmt(m['F1'])} | {fmt(m['AUC'])} |" for label, m in table]
    print("\nSame test records for every row:\n" + "\n".join(lines))
    md_path = run_dir(split, "evaluation_" + "+".join(args.run_name) + ".md")
    md_path.write_text(f"Split {split}, {len(keys)} test records\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {md_path} and predictions.csv / metrics.json in each run directory")


if __name__ == "__main__":
    main()
