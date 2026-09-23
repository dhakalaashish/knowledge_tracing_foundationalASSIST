#!/usr/bin/env python3
"""
Evaluate LLM knowledge tracing predictions against FKT benchmark tasks.

Tasks evaluated:
  - Task 1 (FKT): Foundational Knowledge Tracing - predict if student answers correctly (question-level)
  - Task 1 Variant 2: Cognitive Student Modeling - predict the actual student response

Usage:
    python evaluate_kt.py results.jsonl
"""

import argparse
import json
import math
from sklearn.metrics import roc_auc_score


def normalize_mcq_answer(answer_str: str) -> str:
    """
    Normalize MCQ answer format for consistent comparison.

    Handles variations like:
    - 'C, A' -> 'A, C' (order normalization)
    - 'A,C' -> 'A, C' (spacing normalization)
    - 'a, c' -> 'A, C' (case normalization)

    Args:
        answer_str: Answer string to normalize

    Returns:
        Normalized answer string, or original if not MCQ format
    """
    # Split by comma, strip whitespace, uppercase, sort, rejoin
    parts = [p.strip().upper() for p in answer_str.split(',')]
    # Filter out empty parts
    parts = [p for p in parts if p]
    # Only normalize if all parts are single letters (MCQ format)
    if parts and all(len(p) == 1 and p.isalpha() for p in parts):
        return ', '.join(sorted(set(parts)))
    return answer_str


def numerical_match(answer1: str, answer2: str, atol: float = 0.01, rtol: float = 0.01) -> bool:
    """
    Check if two answers are numerically close within tolerance.

    Uses math.isclose for robust comparison that handles both absolute
    and relative tolerance.

    Args:
        answer1: First answer string
        answer2: Second answer string
        atol: Absolute tolerance (default: 0.01)
        rtol: Relative tolerance (default: 0.01)

    Returns:
        True if answers are numerically close, False otherwise
    """
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

    # Exact string match
    if pred_str == actual_str:
        return True

    # Normalize MCQ answers (handles case, order, spacing)
    pred_normalized = normalize_mcq_answer(pred_str)
    actual_normalized = normalize_mcq_answer(actual_str)
    if pred_normalized == actual_normalized:
        return True

    # Numeric match with tolerance
    return numerical_match(pred_str, actual_str)


def load_results(jsonl_path):
    """Load results from JSONL file."""
    results = []
    with open(jsonl_path, 'r') as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results


def evaluate(results):
    """Compute evaluation metrics aligned with FKT benchmark tasks."""
    total = len(results)

    if total == 0:
        print("No results to evaluate.")
        return

    # Compute class distribution
    n_correct = sum(1 for r in results if r.get('actual_score') == 1)
    n_incorrect = total - n_correct

    # Task 1: FKT - Question-level accuracy
    valid_q = [(r.get('actual_score'), r.get('predicted_question_level'))
               for r in results
               if r.get('actual_score') is not None and r.get('predicted_question_level') is not None]

    if valid_q:
        y_true, y_pred = zip(*valid_q)
        question_correct = sum(1 for t, p in valid_q if t == p)
        question_acc = question_correct / len(valid_q)
        # AUC-ROC (note: with binary predictions, this is limited)
        try:
            auc_roc = roc_auc_score(y_true, y_pred)
        except ValueError:
            auc_roc = None  # Only one class present
    else:
        question_correct = 0
        question_acc = 0.0
        auc_roc = None

    # Task 1 Variant 2: Cognitive Modeling - Answer prediction accuracy
    answer_correct = sum(
        1 for r in results
        if answers_match(r.get('predicted_student_answer'), r.get('actual_answer'))
    )

    # Baselines
    prior_baseline = 0.615  # True correctness rate from Interactions.csv
    majority_baseline = max(n_correct, n_incorrect) / total

    # Print results
    print(f"{'='*60}")
    print(f"Evaluation Results ({total} predictions)")
    print(f"{'='*60}")
    print()
    print(f"Class distribution: {n_correct} correct, {n_incorrect} incorrect")
    print()

    # Task 1: Foundational Knowledge Tracing (FKT) - question-level prediction
    print("Task 1: Foundational Knowledge Tracing (FKT) - Question-Level")
    print(f"  Accuracy:  {question_correct}/{len(valid_q)} = {question_acc:.3f}")
    if auc_roc is not None:
        print(f"  AUC-ROC:   {auc_roc:.3f}")
    else:
        print(f"  AUC-ROC:   N/A (single class)")
    print(f"  Baselines: Prior={prior_baseline:.3f}, Majority={majority_baseline:.3f}")
    print()

    # Task 1 Variant 2: Cognitive Student Modeling
    print("Task 1 Variant 2: Cognitive Student Modeling")
    print(f"  Overall Accuracy: {answer_correct}/{total} = {answer_correct/total:.3f}")

    # Breakdown by problem type
    problem_types = ['Multiple Choice (select 1)', 'Multiple Choice (select all)', 'Fill-in-the-blank(s)']
    has_problem_type = any(r.get('problem_type') for r in results)
    if has_problem_type:
        print("  By problem type:")
        for ptype in problem_types:
            subset = [r for r in results if r.get('problem_type') == ptype]
            if subset:
                n = len(subset)
                a_acc = sum(1 for r in subset if answers_match(r.get('predicted_student_answer'), r.get('actual_answer'))) / n
                label = ptype.replace('Multiple Choice ', 'MC ')
                print(f"    {label:20s}: n={n:4d}, acc={a_acc:.3f}")
                # Breakdown by ground truth within problem type
                for gt in ['correct', 'incorrect']:
                    gt_subset = [r for r in subset if r.get('prediction_type') == gt]
                    if gt_subset:
                        gt_n = len(gt_subset)
                        gt_acc = sum(1 for r in gt_subset if answers_match(r.get('predicted_student_answer'), r.get('actual_answer'))) / gt_n
                        print(f"      {gt:18s}: n={gt_n:4d}, acc={gt_acc:.3f}")
    print()

    # Breakdown by prediction type (correct/incorrect ground truth)
    print("By ground truth (prediction_type):")
    for ptype in ['correct', 'incorrect']:
        subset = [r for r in results if r.get('prediction_type') == ptype]
        if subset:
            n = len(subset)
            q_acc = sum(1 for r in subset if r.get('predicted_question_level') == r.get('actual_score')) / n
            a_acc = sum(1 for r in subset if answers_match(r.get('predicted_student_answer'), r.get('actual_answer'))) / n
            print(f"  {ptype:10s}: n={n:4d}, FKT_acc={q_acc:.3f}, cognitive_acc={a_acc:.3f}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate LLM knowledge tracing predictions")
    parser.add_argument("jsonl_file", help="Path to JSONL results file")
    args = parser.parse_args()

    results = load_results(args.jsonl_file)
    evaluate(results)


if __name__ == "__main__":
    main()
