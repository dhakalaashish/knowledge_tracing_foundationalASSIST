"""
Turn the debate judgements into one practice prediction per item and score it against the
ground truth in problems_naep.csv.

For every debate, the final judge answered A or B, and core/agents/judge_quality.py recorded the
log-probabilities of "A" and "B" ("Logit A: ..., Logit B: ..."). For each debate this script:
  1. normalizes the two log-probabilities over {A, B} (log-softmax), giving log P(A) and log P(B);
  2. maps A and B back to the two practices. Without the swap, A is the first practice of the pair;
     in the swapped debate, A is the second. The mapping is read from each debate's transcript.

Each practice takes part in 10 debates per item (5 opponents x 2 answer orders). Its score is the
mean of its log-probabilities over those debates, and the practice with the highest mean wins.
Mean probability and the number of debates won are also reported, as diagnostics.

ground_truth is read only here, after all debates and judgements are finished.

Run from Code/multi_agent_debate/, e.g.:
    python3 aggregate.py --exp-dir exp/full --data-dir ../../Data
"""

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from practices import PRACTICE_NAMES

GROUND_TRUTH_COLUMN = "ground_truth"
DEBATE_ROOT = "debate_sim_intermediary"  # core/file_handler.Experiment.get_debate_root()
JUDGE_COLUMN = "answer_judge"
COMPLETE_COLUMN = "complete_judge"
LOGIT_PATTERN = re.compile(r"Logit A: (\S+), Logit B: (\S+?),")
ABBREVIATIONS = ["REP", "ABS", "JUS", "MOD", "COL", "PRO"]


def parse_args():
    parser = argparse.ArgumentParser(description="Aggregate debate judgements into practice predictions")
    parser.add_argument("--exp-dir", required=True, help="Experiment directory passed to core.debate / core.judge")
    parser.add_argument("--judge-name", default="qwen3_30b", help="judge_name used by core.judge")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--data-dir", default="../../Data", help="Directory containing problems_naep.csv")
    parser.add_argument("--problems-file", default="problems_naep.csv")
    parser.add_argument("--output-prefix", default="naep_debate",
                        help="Writes <data-dir>/<prefix>_predicted.csv and <prefix>_eval.json")
    return parser.parse_args()


def judgement_files(exp_dir, judge_name, seed):
    folder = Path(exp_dir) / DEBATE_ROOT / judge_name
    return [folder / f"data{seed}_judgement.csv", folder / f"data{seed}_swap_judgement.csv"]


def debate_logprobs(judgement, transcript_json):
    """
    Return {practice: log P(judge picks practice)} for one debate, plus a flag that is True when
    neither "A" nor "B" was among the judge's top tokens (both logits missing, so 50/50).
    """
    match = LOGIT_PATTERN.search(str(judgement))
    if match is None:
        raise ValueError(f"No 'Logit A/B' in judgement: {str(judgement)[:200]!r}")
    logit_a, logit_b = float(match.group(1)), float(match.group(2))
    normalizer = np.logaddexp(logit_a, logit_b)
    logp_a, logp_b = logit_a - normalizer, logit_b - normalizer

    transcript = json.loads(transcript_json)
    answers = transcript["answers"]
    # judge_quality.fill_in_content: ANSWER_A is the "correct" slot unless the transcript is swapped
    practice_a, practice_b = (
        (answers["incorrect"], answers["correct"]) if transcript["swap"]
        else (answers["correct"], answers["incorrect"])
    )
    both_missing = logit_a <= -100 and logit_b <= -100
    return {practice_a: logp_a, practice_b: logp_b}, both_missing


def collect(exp_dir, judge_name, seed):
    """Per item and practice, the list of log-probabilities from every debate it took part in."""
    logprobs = defaultdict(lambda: defaultdict(list))
    pair_winners = defaultdict(dict)  # (problem_id, pair) -> {swap: winner}
    missing_letters, incomplete = 0, []
    for path in judgement_files(exp_dir, judge_name, seed):
        if not path.exists():
            raise FileNotFoundError(f"{path} not found; run core.judge first")
        df = pd.read_csv(path, dtype={"problem_id": str})
        for _, row in df.iterrows():
            if not bool(row.get(COMPLETE_COLUMN, False)):
                incomplete.append(row["id"])
                continue
            scores, both_missing = debate_logprobs(row[JUDGE_COLUMN], row["transcript"])
            missing_letters += both_missing
            problem_id = str(row["problem_id"])
            for practice, logp in scores.items():
                logprobs[problem_id][practice].append(logp)
            pair = tuple(sorted(scores))
            pair_winners[(problem_id, pair)]["swap" in path.name] = max(scores, key=scores.get)
    return logprobs, pair_winners, missing_letters, incomplete


def predict(practice_logprobs):
    """Mean log-probability, mean probability, and wins per practice, plus the predicted practice."""
    mean_logp, mean_p, wins, counts = [], [], [], []
    for name in PRACTICE_NAMES:
        values = np.array(practice_logprobs.get(name, []))
        counts.append(len(values))
        mean_logp.append(float(values.mean()) if len(values) else float("-inf"))
        mean_p.append(float(np.exp(values).mean()) if len(values) else 0.0)
        wins.append(int((values > np.log(0.5)).sum()))
    # Highest mean log-probability; ties broken by mean probability
    best = max(range(len(PRACTICE_NAMES)), key=lambda i: (mean_logp[i], mean_p[i]))
    return PRACTICE_NAMES[best], mean_logp, mean_p, wins, counts


def evaluate(results):
    per_practice = {name: {"n": 0, "top1_correct": 0, "top2_correct": 0} for name in PRACTICE_NAMES}
    confusion = {t: {p: 0 for p in PRACTICE_NAMES} for t in PRACTICE_NAMES}
    misclassified = []
    for item in results:
        truth, predicted = item[GROUND_TRUTH_COLUMN], item["predicted_practice"]
        ranked = np.argsort(-np.array(item["debate_mean_logprob"]), kind="stable")
        in_top2 = PRACTICE_NAMES.index(truth) in ranked[:2]
        stats = per_practice[truth]
        stats["n"] += 1
        stats["top1_correct"] += predicted == truth
        stats["top2_correct"] += bool(in_top2)
        confusion[truth][predicted] += 1
        if predicted != truth:
            misclassified.append(item)
    n = len(results)
    top1 = sum(s["top1_correct"] for s in per_practice.values())
    top2 = sum(s["top2_correct"] for s in per_practice.values())
    for stats in per_practice.values():
        stats["top1_accuracy"] = stats["top1_correct"] / stats["n"] if stats["n"] else None
        stats["top2_accuracy"] = stats["top2_correct"] / stats["n"] if stats["n"] else None
    return {
        "n_evaluated": n,
        "top1_correct": top1,
        "top1_accuracy": top1 / n if n else None,
        "top2_correct": top2,
        "top2_accuracy": top2 / n if n else None,
        "per_practice": per_practice,
        "confusion": confusion,
        "misclassified": [
            {"problem_id": m["problem_id"], GROUND_TRUTH_COLUMN: m[GROUND_TRUTH_COLUMN],
             "predicted_practice": m["predicted_practice"],
             "debate_mean_logprob": dict(zip(PRACTICE_NAMES, m["debate_mean_logprob"]))}
            for m in misclassified
        ],
    }


def print_report(metrics, order_disagreements, n_pairs, missing_letters, incomplete, counts_seen):
    n = metrics["n_evaluated"]
    print(f"\n{'='*80}")
    print(f"MULTI-AGENT DEBATE: EVALUATION AGAINST GROUND TRUTH ({n} items)")
    print(f"{'='*80}")
    if not n:
        print("No items could be evaluated.")
        return
    print(f"Top-1 accuracy: {metrics['top1_correct']}/{n} = {metrics['top1_accuracy']:.1%}  "
          f"(highest mean log-probability)")
    print(f"Top-2 accuracy: {metrics['top2_correct']}/{n} = {metrics['top2_accuracy']:.1%}")
    print(f"Debates per practice per item: {sorted(counts_seen)} (expected 10)")
    print(f"Practice pairs whose winner changed when the answer order was swapped: "
          f"{order_disagreements}/{n_pairs}")
    if missing_letters:
        print(f"Judgements where neither A nor B was in the judge's top tokens (counted 50/50): {missing_letters}")
    if incomplete:
        print(f"Incomplete judgements left out: {len(incomplete)} ({incomplete[:10]}...)")

    print(f"\nPer practice (by ground truth):")
    print(f"  {'Practice':<30} {'n':>3}  {'top-1':>7}  {'top-2':>7}")
    for name, stats in metrics["per_practice"].items():
        if not stats["n"]:
            print(f"  {name:<30} {0:>3}  {'-':>7}  {'-':>7}")
            continue
        print(f"  {name:<30} {stats['n']:>3}  {stats['top1_accuracy']:>7.0%}  {stats['top2_accuracy']:>7.0%}")

    print(f"\nConfusion matrix (rows: ground truth, columns: predicted)")
    print("  " + "  ".join(f"{a}={name}" for a, name in zip(ABBREVIATIONS, PRACTICE_NAMES)))
    print(f"  {'':<6}" + "".join(f"{a:>6}" for a in ABBREVIATIONS))
    for abbreviation, truth in zip(ABBREVIATIONS, PRACTICE_NAMES):
        row = metrics["confusion"][truth]
        print(f"  {abbreviation:<6}" + "".join(f"{row[pred]:>6}" for pred in PRACTICE_NAMES))

    if metrics["misclassified"]:
        print(f"\nMisclassified items (mean log-probability per practice):")
        for item in metrics["misclassified"]:
            scores = ", ".join(f"{a} {s:.2f}" for a, s in zip(ABBREVIATIONS, item["debate_mean_logprob"].values()))
            print(f"  {item['problem_id']}: truth {item[GROUND_TRUTH_COLUMN]}, "
                  f"predicted {item['predicted_practice']}  [{scores}]")


def main():
    args = parse_args()
    logprobs, pair_winners, missing_letters, incomplete = collect(args.exp_dir, args.judge_name, args.seed)

    truth_df = pd.read_csv(os.path.join(args.data_dir, args.problems_file), dtype=str, keep_default_na=False)
    ground_truth = dict(zip(truth_df["problem_id"].str.strip(), truth_df[GROUND_TRUTH_COLUMN].str.strip()))

    results, counts_seen = [], set()
    for problem_id, practice_logprobs in logprobs.items():
        predicted, mean_logp, mean_p, wins, counts = predict(practice_logprobs)
        counts_seen.update(counts)
        results.append({
            "problem_id": problem_id,
            GROUND_TRUTH_COLUMN: ground_truth.get(problem_id, ""),
            "predicted_practice": predicted,
            "debate_mean_logprob": [round(v, 4) for v in mean_logp],
            "debate_mean_prob": [round(v, 4) for v in mean_p],
            "debate_wins": wins,
            "debates_per_practice": counts,
        })
    evaluable = [r for r in results if r[GROUND_TRUTH_COLUMN] in PRACTICE_NAMES]

    both_orders = [w for w in pair_winners.values() if len(w) == 2]
    order_disagreements = sum(w[False] != w[True] for w in both_orders)

    metrics = evaluate(evaluable)
    print_report(metrics, order_disagreements, len(both_orders), missing_letters, incomplete, counts_seen)

    output_csv = os.path.join(args.data_dir, f"{args.output_prefix}_predicted.csv")
    output_json = os.path.join(args.data_dir, f"{args.output_prefix}_eval.json")
    out_df = pd.DataFrame(results)
    for column in ("debate_mean_logprob", "debate_mean_prob", "debate_wins", "debates_per_practice"):
        out_df[column] = out_df[column].apply(json.dumps)
    out_df["correct"] = out_df[GROUND_TRUTH_COLUMN] == out_df["predicted_practice"]
    out_df.to_csv(output_csv, index=False, encoding="utf-8")
    metrics.update({
        "practice_order": PRACTICE_NAMES,
        "order_disagreements": order_disagreements,
        "n_pairs_both_orders": len(both_orders),
        "judgements_missing_both_letters": missing_letters,
        "incomplete_judgements": incomplete,
        "exp_dir": str(args.exp_dir),
        "judge_name": args.judge_name,
    })
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"\nSaved {output_csv} and {output_json}")


if __name__ == "__main__":
    main()
