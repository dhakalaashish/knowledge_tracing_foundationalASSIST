"""
Evaluation script for Pedagogical Grounding LLM Benchmark.

Computes accuracy metrics for:
1. Difficulty comparison task
2. Discrimination comparison task
3. Most common distractor prediction
4. Least common distractor prediction

Usage:
    python evaluate_pedagogical.py --input results.jsonl
    python evaluate_pedagogical.py --input results.jsonl --output metrics.json
"""

import argparse
import json
from collections import defaultdict
from typing import Dict, List, Optional


def load_results(jsonl_path: str) -> List[Dict]:
    """Load results from JSONL file."""
    results = []
    with open(jsonl_path, 'r') as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results


def evaluate_comparison_task(results: List[Dict], task_name: str) -> Dict:
    """Evaluate a comparison task (difficulty or discrimination)."""
    task_results = [r for r in results if r.get('task') == task_name]

    if not task_results:
        return {'error': f'No results found for task: {task_name}'}

    total = len(task_results)
    correct = sum(1 for r in task_results if r.get('is_correct', False))
    accuracy = correct / total if total > 0 else 0

    # Breakdown by stratum
    stratum_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in task_results:
        stratum = r.get('stratum', 'unknown')
        stratum_stats[stratum]['total'] += 1
        if r.get('is_correct', False):
            stratum_stats[stratum]['correct'] += 1

    stratum_accuracy = {}
    for stratum, stats in stratum_stats.items():
        if stats['total'] > 0:
            stratum_accuracy[stratum] = {
                'accuracy': stats['correct'] / stats['total'],
                'correct': stats['correct'],
                'total': stats['total']
            }

    # Breakdown by difficulty difference bins
    diff_bins = [
        ('very_small', 0, 0.2),
        ('small', 0.2, 0.5),
        ('medium', 0.5, 1.0),
        ('large', 1.0, float('inf'))
    ]

    diff_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in task_results:
        diff = r.get('difference', 0)
        for bin_name, low, high in diff_bins:
            if low <= diff < high:
                diff_stats[bin_name]['total'] += 1
                if r.get('is_correct', False):
                    diff_stats[bin_name]['correct'] += 1
                break

    diff_accuracy = {}
    for bin_name, stats in diff_stats.items():
        if stats['total'] > 0:
            diff_accuracy[bin_name] = {
                'accuracy': stats['correct'] / stats['total'],
                'correct': stats['correct'],
                'total': stats['total']
            }

    return {
        'task': task_name,
        'total': total,
        'correct': correct,
        'accuracy': accuracy,
        'baseline_random': 0.5,  # Random guess for binary choice
        'lift_over_random': accuracy - 0.5,
        'by_stratum': dict(stratum_accuracy),
        'by_difference': dict(diff_accuracy)
    }


def evaluate_distractor_task(results: List[Dict], task_name: str) -> Dict:
    """Evaluate a distractor task (most or least common)."""
    task_results = [r for r in results if r.get('task') == task_name]

    if not task_results:
        return {'error': f'No results found for task: {task_name}'}

    total = len(task_results)
    correct = sum(1 for r in task_results if r.get('is_correct', False))
    accuracy = correct / total if total > 0 else 0

    # Breakdown by number of choices
    choices_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in task_results:
        n_choices = r.get('n_choices', 0)
        # Number of distractors = n_choices - 1 (excluding correct answer)
        n_distractors = n_choices - 1 if n_choices > 1 else 1
        choices_stats[n_distractors]['total'] += 1
        if r.get('is_correct', False):
            choices_stats[n_distractors]['correct'] += 1

    choices_accuracy = {}
    baseline_by_choices = {}
    for n_distractors, stats in sorted(choices_stats.items()):
        if stats['total'] > 0:
            acc = stats['correct'] / stats['total']
            baseline = 1.0 / n_distractors if n_distractors > 0 else 0
            choices_accuracy[f'{n_distractors}_distractors'] = {
                'accuracy': acc,
                'correct': stats['correct'],
                'total': stats['total'],
                'baseline_random': baseline,
                'lift_over_random': acc - baseline
            }
            baseline_by_choices[n_distractors] = baseline

    # Compute weighted average baseline
    total_weighted_baseline = 0
    for r in task_results:
        n_choices = r.get('n_choices', 0)
        n_distractors = n_choices - 1 if n_choices > 1 else 1
        if n_distractors > 0:
            total_weighted_baseline += 1.0 / n_distractors
    avg_baseline = total_weighted_baseline / total if total > 0 else 0

    # Breakdown by ground truth frequency
    freq_bins = [
        ('very_rare', 0, 0.05),
        ('rare', 0.05, 0.10),
        ('moderate', 0.10, 0.20),
        ('common', 0.20, 0.30),
        ('very_common', 0.30, 1.0)
    ]

    freq_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in task_results:
        freq = r.get('ground_truth_freq', 0)
        for bin_name, low, high in freq_bins:
            if low <= freq < high:
                freq_stats[bin_name]['total'] += 1
                if r.get('is_correct', False):
                    freq_stats[bin_name]['correct'] += 1
                break

    freq_accuracy = {}
    for bin_name, stats in freq_stats.items():
        if stats['total'] > 0:
            freq_accuracy[bin_name] = {
                'accuracy': stats['correct'] / stats['total'],
                'correct': stats['correct'],
                'total': stats['total']
            }

    return {
        'task': task_name,
        'total': total,
        'correct': correct,
        'accuracy': accuracy,
        'baseline_random_avg': avg_baseline,
        'lift_over_random': accuracy - avg_baseline,
        'by_num_distractors': dict(choices_accuracy),
        'by_ground_truth_freq': dict(freq_accuracy)
    }


def print_comparison_results(metrics: Dict) -> None:
    """Print comparison task results."""
    print(f"\n{'='*60}")
    print(f"Task: {metrics['task'].upper()}")
    print(f"{'='*60}")

    print(f"\nOverall Accuracy: {metrics['accuracy']:.1%} ({metrics['correct']}/{metrics['total']})")
    print(f"Random Baseline:  {metrics['baseline_random']:.1%}")
    print(f"Lift over Random: {metrics['lift_over_random']:+.1%}")

    if metrics.get('by_stratum'):
        print(f"\nBy Sampling Stratum:")
        for stratum, stats in sorted(metrics['by_stratum'].items()):
            print(f"  {stratum:12}: {stats['accuracy']:.1%} ({stats['correct']}/{stats['total']})")

    if metrics.get('by_difference'):
        print(f"\nBy Value Difference:")
        for bin_name, stats in metrics['by_difference'].items():
            print(f"  {bin_name:12}: {stats['accuracy']:.1%} ({stats['correct']}/{stats['total']})")


def print_distractor_results(metrics: Dict) -> None:
    """Print distractor task results."""
    print(f"\n{'='*60}")
    print(f"Task: {metrics['task'].upper()}")
    print(f"{'='*60}")

    print(f"\nOverall Accuracy: {metrics['accuracy']:.1%} ({metrics['correct']}/{metrics['total']})")
    print(f"Random Baseline:  {metrics['baseline_random_avg']:.1%} (weighted avg)")
    print(f"Lift over Random: {metrics['lift_over_random']:+.1%}")

    if metrics.get('by_num_distractors'):
        print(f"\nBy Number of Distractors:")
        for key, stats in sorted(metrics['by_num_distractors'].items()):
            print(f"  {key:15}: {stats['accuracy']:.1%} ({stats['correct']}/{stats['total']}) "
                  f"[baseline: {stats['baseline_random']:.1%}, lift: {stats['lift_over_random']:+.1%}]")

    if metrics.get('by_ground_truth_freq'):
        print(f"\nBy Ground Truth Frequency:")
        for bin_name, stats in metrics['by_ground_truth_freq'].items():
            print(f"  {bin_name:12}: {stats['accuracy']:.1%} ({stats['correct']}/{stats['total']})")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate Pedagogical Grounding Benchmark Results"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        required=True,
        help="Input JSONL file with predictions"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output JSON file for metrics (optional)"
    )
    args = parser.parse_args()

    print(f"Loading results from {args.input}...")
    results = load_results(args.input)
    print(f"Loaded {len(results)} predictions")

    # Identify tasks in results
    tasks = set(r.get('task') for r in results if r.get('task'))
    print(f"Tasks found: {tasks}")

    all_metrics = {}

    # Evaluate each task
    for task in sorted(tasks):
        if task in ['difficulty', 'discrimination']:
            metrics = evaluate_comparison_task(results, task)
            print_comparison_results(metrics)
        elif task in ['distractor_most', 'distractor_least']:
            metrics = evaluate_distractor_task(results, task)
            print_distractor_results(metrics)
        else:
            print(f"Unknown task: {task}")
            continue

        all_metrics[task] = metrics

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for task, metrics in all_metrics.items():
        if 'error' not in metrics:
            print(f"{task:20}: {metrics['accuracy']:.1%} accuracy "
                  f"({metrics['lift_over_random']:+.1%} vs random)")

    # Save metrics if output specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(all_metrics, f, indent=2)
        print(f"\nMetrics saved to {args.output}")


if __name__ == "__main__":
    main()
