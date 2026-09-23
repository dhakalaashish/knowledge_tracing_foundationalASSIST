#!/usr/bin/env python3
"""
Evaluate KT performance by context length (history size).

Analyzes how KT accuracy changes as student history grows from 50 to 400 interactions.
Plots all models in a single figure for comparison.

Usage:
    python evaluate_kt_by_context.py
"""

import argparse
import json
import math
import os
from glob import glob
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_auc_score

# Set publication-quality font sizes
plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
})

# Model name mapping for display
MODEL_NAMES = {
    'gptoss120b': 'GPT-OSS-120B',
    'llama33_70b_instruct': 'Llama-3.3-70B-Instruct',
    'qwen3next80binstruct': 'Qwen3-80B-Instruct',
    'qwen3next80bthinking': 'Qwen3-80B-Thinking',
}

# Colors for each model
MODEL_COLORS = {
    'gptoss120b': '#1f77b4',  # blue
    'llama33_70b_instruct': '#ff7f0e',  # orange
    'qwen3next80binstruct': '#2ca02c',  # green
    'qwen3next80bthinking': '#d62728',  # red
}


def normalize_mcq_answer(answer_str: str) -> str:
    """Normalize MCQ answer format for consistent comparison."""
    parts = [p.strip().upper() for p in answer_str.split(',')]
    parts = [p for p in parts if p]
    if parts and all(len(p) == 1 and p.isalpha() for p in parts):
        return ', '.join(sorted(set(parts)))
    return answer_str


def numerical_match(answer1: str, answer2: str, atol: float = 0.01, rtol: float = 0.01) -> bool:
    """Check if two answers are numerically close within tolerance."""
    try:
        a = float(answer1.strip())
        b = float(answer2.strip())
        return math.isclose(a, b, abs_tol=atol, rel_tol=rtol)
    except (ValueError, AttributeError):
        return False


def answers_match(pred, actual):
    """Check if predicted answer matches actual answer."""
    if pred is None or actual is None:
        return False

    pred_str = str(pred).strip()
    actual_str = str(actual).strip()

    if pred_str == actual_str:
        return True

    pred_normalized = normalize_mcq_answer(pred_str)
    actual_normalized = normalize_mcq_answer(actual_str)
    if pred_normalized == actual_normalized:
        return True

    return numerical_match(pred_str, actual_str)


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate KT by context length")
    parser.add_argument(
        "--results-dir", "-r",
        type=str,
        default="inference_data_kt_results",
        help="Directory containing JSONL results files"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="dataset_analysis/plots",
        help="Directory to save output plots"
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip generating plots"
    )
    return parser.parse_args()


def extract_model_name(filename):
    """Extract model identifier from filename."""
    basename = os.path.basename(filename)
    # Pattern: modelname_n500_bin10_hist50.jsonl
    for model_key in MODEL_NAMES.keys():
        if basename.startswith(model_key):
            return model_key
    return basename.replace('.jsonl', '')


def load_results(jsonl_path):
    """Load results from JSONL file."""
    results = []
    with open(jsonl_path, 'r') as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results


def compute_metrics_by_bin(results):
    """Compute metrics grouped by history_size."""
    bins = defaultdict(list)

    for r in results:
        history_size = r.get('history_size', 50)
        bins[history_size].append(r)

    metrics = {}
    for history_size in sorted(bins.keys()):
        bin_results = bins[history_size]
        n = len(bin_results)

        # FKT: Collect valid predictions for AUC-ROC
        y_true = []
        y_pred = []
        for r in bin_results:
            actual = r.get('actual_score')
            pred = r.get('predicted_question_level')
            if actual is not None and pred is not None:
                y_true.append(int(actual))
                y_pred.append(int(pred))

        # Compute AUC-ROC (requires both classes present)
        fkt_auc = None
        if len(set(y_true)) == 2 and len(y_true) > 0:
            try:
                fkt_auc = roc_auc_score(y_true, y_pred)
            except ValueError:
                pass

        # FKT accuracy (for reference)
        fkt_correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
        fkt_acc = fkt_correct / len(y_true) if y_true else 0.0

        # Cognitive accuracy (answer match)
        cognitive_correct = sum(
            1 for r in bin_results
            if answers_match(r.get('predicted_student_answer'), r.get('actual_answer'))
        )

        metrics[history_size] = {
            'n': n,
            'fkt_auc': fkt_auc,
            'fkt_acc': fkt_acc,
            'fkt_valid': len(y_true),
            'cognitive_acc': cognitive_correct / n if n > 0 else 0.0,
        }

    return metrics


def print_table(all_metrics):
    """Print metrics table to console."""
    # Get all history sizes across all models
    all_history_sizes = sorted(set(
        hs for model_metrics in all_metrics.values()
        for hs in model_metrics.keys()
    ))

    # Header
    print("\n" + "=" * 100)
    print("KT Performance by Context Length (History Size)")
    print("=" * 100)

    # Print FKT AUC-ROC table
    print("\nFKT AUC-ROC (Question-Level):")
    print("-" * 80)
    header = f"{'History':>8}"
    for model_key in all_metrics.keys():
        header += f"  {MODEL_NAMES.get(model_key, model_key)[:20]:>20}"
    print(header)
    print("-" * 80)

    for hs in all_history_sizes:
        row = f"{hs:>8}"
        for model_key in all_metrics.keys():
            if hs in all_metrics[model_key]:
                auc = all_metrics[model_key][hs]['fkt_auc']
                if auc is not None:
                    row += f"  {auc:>20.3f}"
                else:
                    row += f"  {'N/A':>20}"
            else:
                row += f"  {'N/A':>20}"
        print(row)

    # Print Cognitive accuracy table
    print("\nCognitive Accuracy (Answer Prediction):")
    print("-" * 80)
    print(header)
    print("-" * 80)

    for hs in all_history_sizes:
        row = f"{hs:>8}"
        for model_key in all_metrics.keys():
            if hs in all_metrics[model_key]:
                acc = all_metrics[model_key][hs]['cognitive_acc']
                row += f"  {acc:>20.3f}"
            else:
                row += f"  {'N/A':>20}"
        print(row)


def plot_results(all_metrics, output_dir):
    """Generate plot with all models."""
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: FKT AUC-ROC
    for model_key, metrics in all_metrics.items():
        history_sizes = sorted(metrics.keys())
        # Filter out None values
        valid_hs = [hs for hs in history_sizes if metrics[hs]['fkt_auc'] is not None]
        fkt_aucs = [metrics[hs]['fkt_auc'] for hs in valid_hs]

        if valid_hs:
            axes[0].plot(
                valid_hs, fkt_aucs,
                marker='o', markersize=4,
                color=MODEL_COLORS.get(model_key, 'gray'),
                label=MODEL_NAMES.get(model_key, model_key),
                linewidth=2
            )

    axes[0].set_xlabel('History Size (# prior interactions)')
    axes[0].set_ylabel('AUC-ROC')
    axes[0].set_title('FKT AUC-ROC vs Context Length')
    axes[0].legend(loc='best')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(40, 410)
    axes[0].axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Random')

    # Plot 2: Cognitive Accuracy
    for model_key, metrics in all_metrics.items():
        history_sizes = sorted(metrics.keys())
        cognitive_accs = [metrics[hs]['cognitive_acc'] for hs in history_sizes]

        axes[1].plot(
            history_sizes, cognitive_accs,
            marker='o', markersize=4,
            color=MODEL_COLORS.get(model_key, 'gray'),
            label=MODEL_NAMES.get(model_key, model_key),
            linewidth=2
        )

    axes[1].set_xlabel('History Size (# prior interactions)')
    axes[1].set_ylabel('Accuracy')
    axes[1].set_title('Cognitive Modeling Accuracy vs Context Length')
    axes[1].legend(loc='best')
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(40, 410)

    plt.tight_layout()

    plot_path = os.path.join(output_dir, 'kt_context_scaling.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()

    print(f"\nSaved: {plot_path}")


def main():
    args = parse_args()

    # Find all JSONL files
    jsonl_files = glob(os.path.join(args.results_dir, '*.jsonl'))

    if not jsonl_files:
        print(f"No JSONL files found in {args.results_dir}")
        return

    print(f"Found {len(jsonl_files)} result files:")
    for f in jsonl_files:
        print(f"  - {os.path.basename(f)}")

    # Load and analyze each model
    all_metrics = {}

    for jsonl_path in sorted(jsonl_files):
        model_key = extract_model_name(jsonl_path)
        print(f"\nProcessing {MODEL_NAMES.get(model_key, model_key)}...")

        results = load_results(jsonl_path)
        print(f"  Loaded {len(results):,} predictions")

        metrics = compute_metrics_by_bin(results)
        all_metrics[model_key] = metrics

        # Print quick summary
        history_sizes = sorted(metrics.keys())
        valid_aucs = [metrics[hs]['fkt_auc'] for hs in history_sizes if metrics[hs]['fkt_auc'] is not None]
        avg_auc = np.mean(valid_aucs) if valid_aucs else 0.0
        avg_cognitive = np.mean([metrics[hs]['cognitive_acc'] for hs in history_sizes])
        print(f"  Avg FKT AUC-ROC: {avg_auc:.3f}")
        print(f"  Avg Cognitive accuracy: {avg_cognitive:.3f}")

    # Print detailed table
    print_table(all_metrics)

    # Generate plot
    if not args.no_plots:
        plot_results(all_metrics, args.output_dir)

    print("\nDone!")


if __name__ == "__main__":
    main()
