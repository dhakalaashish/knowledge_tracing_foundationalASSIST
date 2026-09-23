"""
Batch evaluation script for Pedagogical Grounding LLM Benchmark.

Analyzes all result files in a directory and creates aggregate comparison tables.

Usage:
    python pedagogical_grounding/batch_evaluate.py --input-dir pedagogical_grounding/results
    python pedagogical_grounding/batch_evaluate.py --input-dir results --output summary.json
"""

import argparse
import glob
import json
import os
import re
from collections import defaultdict
from typing import Dict, List, Tuple

from evaluate_pedagogical import (
    load_results,
    evaluate_comparison_task,
    evaluate_distractor_task,
)


def extract_model_name(filename: str) -> str:
    """Extract model name from filename."""
    basename = os.path.basename(filename)
    # Pattern: {model}_pedagogical_{task}_...
    match = re.match(r'^(.+?)_pedagogical_', basename)
    if match:
        return match.group(1)
    return basename.replace('.jsonl', '')


def evaluate_file(filepath: str) -> Tuple[str, Dict]:
    """Evaluate a single file and return model name and metrics."""
    model_name = extract_model_name(filepath)
    results = load_results(filepath)

    metrics = {
        'file': os.path.basename(filepath),
        'total_predictions': len(results),
        'tasks': {}
    }

    # Identify and evaluate tasks
    tasks = set(r.get('task') for r in results if r.get('task'))

    for task in tasks:
        if task in ['difficulty', 'discrimination']:
            task_metrics = evaluate_comparison_task(results, task)
        elif task in ['distractor_most', 'distractor_least']:
            task_metrics = evaluate_distractor_task(results, task)
        else:
            continue

        if 'error' not in task_metrics:
            metrics['tasks'][task] = task_metrics

    return model_name, metrics


def print_header(title: str, width: int = 80) -> None:
    """Print a formatted header."""
    print()
    print("=" * width)
    print(f" {title}")
    print("=" * width)


def print_accuracy_table(all_metrics: Dict[str, Dict], task: str) -> None:
    """Print accuracy comparison table for a task."""
    models = sorted(all_metrics.keys())

    # Get baseline
    if task in ['difficulty', 'discrimination']:
        baseline = 0.5
        baseline_label = "50.0%"
    else:
        baseline = None  # Varies by model
        baseline_label = "varies"

    # Header
    print(f"\n{'Model':<35} {'Accuracy':>10} {'Lift':>10} {'N':>8}")
    print("-" * 65)

    # Data rows
    for model in models:
        task_metrics = all_metrics[model]['tasks'].get(task)
        if task_metrics and 'error' not in task_metrics:
            acc = task_metrics['accuracy']
            lift = task_metrics['lift_over_random']
            n = task_metrics['total']
            print(f"{model:<35} {acc:>9.1%} {lift:>+9.1%} {n:>8}")
        else:
            print(f"{model:<35} {'N/A':>10} {'N/A':>10} {'N/A':>8}")

    print("-" * 65)
    print(f"{'Random Baseline':<35} {baseline_label:>10}")


def print_stratum_table(all_metrics: Dict[str, Dict], task: str) -> None:
    """Print stratum breakdown comparison table."""
    models = sorted(all_metrics.keys())
    strata = ['small', 'medium', 'large']

    # Header
    header = f"{'Model':<30}"
    for s in strata:
        header += f" {s:>12}"
    print(f"\n{header}")
    print("-" * (30 + 13 * len(strata)))

    # Data rows
    for model in models:
        task_metrics = all_metrics[model]['tasks'].get(task)
        if task_metrics and 'error' not in task_metrics:
            row = f"{model:<30}"
            by_stratum = task_metrics.get('by_stratum', {})
            for s in strata:
                if s in by_stratum:
                    acc = by_stratum[s]['accuracy']
                    row += f" {acc:>11.1%}"
                else:
                    row += f" {'N/A':>12}"
            print(row)


def print_summary_table(all_metrics: Dict[str, Dict]) -> None:
    """Print overall summary table with all tasks."""
    models = sorted(all_metrics.keys())
    tasks = ['difficulty', 'discrimination', 'distractor_most', 'distractor_least']
    task_abbrev = {
        'difficulty': 'Diff',
        'discrimination': 'Disc',
        'distractor_most': 'D-Most',
        'distractor_least': 'D-Least'
    }

    # Header
    header = f"{'Model':<30}"
    for t in tasks:
        header += f" {task_abbrev[t]:>10}"
    header += f" {'Avg':>10}"
    print(f"\n{header}")
    print("-" * (30 + 11 * (len(tasks) + 1)))

    # Data rows
    for model in models:
        row = f"{model:<30}"
        accs = []
        for t in tasks:
            task_metrics = all_metrics[model]['tasks'].get(t)
            if task_metrics and 'error' not in task_metrics:
                acc = task_metrics['accuracy']
                row += f" {acc:>9.1%}"
                accs.append(acc)
            else:
                row += f" {'N/A':>10}"

        # Average
        if accs:
            avg = sum(accs) / len(accs)
            row += f" {avg:>9.1%}"
        else:
            row += f" {'N/A':>10}"

        print(row)

    # Baseline row
    print("-" * (30 + 11 * (len(tasks) + 1)))
    baseline_row = f"{'Random Baseline':<30}"
    baseline_row += f" {'50.0%':>10}"  # difficulty
    baseline_row += f" {'50.0%':>10}"  # discrimination
    baseline_row += f" {'~35%':>10}"   # distractor_most
    baseline_row += f" {'~35%':>10}"   # distractor_least
    baseline_row += f" {'~43%':>10}"   # avg
    print(baseline_row)


def print_lift_table(all_metrics: Dict[str, Dict]) -> None:
    """Print lift over random baseline table."""
    models = sorted(all_metrics.keys())
    tasks = ['difficulty', 'discrimination', 'distractor_most', 'distractor_least']
    task_abbrev = {
        'difficulty': 'Diff',
        'discrimination': 'Disc',
        'distractor_most': 'D-Most',
        'distractor_least': 'D-Least'
    }

    # Header
    header = f"{'Model':<30}"
    for t in tasks:
        header += f" {task_abbrev[t]:>10}"
    header += f" {'Avg Lift':>10}"
    print(f"\n{header}")
    print("-" * (30 + 11 * (len(tasks) + 1)))

    # Data rows
    for model in models:
        row = f"{model:<30}"
        lifts = []
        for t in tasks:
            task_metrics = all_metrics[model]['tasks'].get(t)
            if task_metrics and 'error' not in task_metrics:
                lift = task_metrics['lift_over_random']
                row += f" {lift:>+9.1%}"
                lifts.append(lift)
            else:
                row += f" {'N/A':>10}"

        # Average lift
        if lifts:
            avg_lift = sum(lifts) / len(lifts)
            row += f" {avg_lift:>+9.1%}"
        else:
            row += f" {'N/A':>10}"

        print(row)


def print_best_model_per_task(all_metrics: Dict[str, Dict]) -> None:
    """Print best model for each task."""
    tasks = ['difficulty', 'discrimination', 'distractor_most', 'distractor_least']

    print(f"\n{'Task':<20} {'Best Model':<30} {'Accuracy':>10} {'Lift':>10}")
    print("-" * 72)

    for task in tasks:
        best_model = None
        best_acc = -1
        best_lift = 0

        for model, metrics in all_metrics.items():
            task_metrics = metrics['tasks'].get(task)
            if task_metrics and 'error' not in task_metrics:
                if task_metrics['accuracy'] > best_acc:
                    best_acc = task_metrics['accuracy']
                    best_lift = task_metrics['lift_over_random']
                    best_model = model

        if best_model:
            print(f"{task:<20} {best_model:<30} {best_acc:>9.1%} {best_lift:>+9.1%}")
        else:
            print(f"{task:<20} {'N/A':<30} {'N/A':>10} {'N/A':>10}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch evaluate Pedagogical Grounding Benchmark results"
    )
    parser.add_argument(
        "--input-dir", "-i",
        type=str,
        required=True,
        help="Directory containing JSONL result files"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output JSON file for aggregate metrics (optional)"
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="*.jsonl",
        help="Glob pattern for result files (default: *.jsonl)"
    )
    args = parser.parse_args()

    # Find all result files
    pattern = os.path.join(args.input_dir, args.pattern)
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"No files found matching: {pattern}")
        return

    print(f"Found {len(files)} result files in {args.input_dir}")

    # Evaluate all files
    all_metrics = {}
    for filepath in files:
        print(f"  Loading: {os.path.basename(filepath)}")
        model_name, metrics = evaluate_file(filepath)
        all_metrics[model_name] = metrics

    # Print aggregate tables
    print_header("PEDAGOGICAL GROUNDING BENCHMARK - AGGREGATE RESULTS")

    # Summary table
    print_header("ACCURACY BY TASK", width=72)
    print_summary_table(all_metrics)

    # Lift table
    print_header("LIFT OVER RANDOM BASELINE", width=72)
    print_lift_table(all_metrics)

    # Best model per task
    print_header("BEST MODEL PER TASK", width=72)
    print_best_model_per_task(all_metrics)

    # Detailed stratum breakdown for comparison tasks
    print_header("DIFFICULTY - ACCURACY BY STRATUM", width=70)
    print_stratum_table(all_metrics, 'difficulty')

    print_header("DISCRIMINATION - ACCURACY BY STRATUM", width=70)
    print_stratum_table(all_metrics, 'discrimination')

    # Individual task tables
    for task in ['difficulty', 'discrimination', 'distractor_most', 'distractor_least']:
        print_header(f"{task.upper()} - DETAILED", width=65)
        print_accuracy_table(all_metrics, task)

    # Save aggregate metrics if output specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(all_metrics, f, indent=2)
        print(f"\nAggregate metrics saved to {args.output}")

    print()


if __name__ == "__main__":
    main()
