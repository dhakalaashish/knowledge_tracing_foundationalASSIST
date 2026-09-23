"""
Distractor Analysis for Pedagogical Grounding

Computes distractor effectiveness for Multiple Choice (select 1) questions
with more than 2 choices. Identifies most/least common wrong answers.
"""

import argparse
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Configuration
DEFAULT_DATA_DIR = "foundationalktdataset"
STUDENT_FILE = "Interactions.csv"
PROBLEMS_FILE = "Problems.csv"


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze distractor effectiveness")
    parser.add_argument(
        "--data-dir", "-d",
        type=str,
        default=DEFAULT_DATA_DIR,
        help=f"Directory containing input CSV files (default: {DEFAULT_DATA_DIR})"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="pedagogical_grounding/output",
        help="Directory to save output (default: pedagogical_grounding/output)"
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip generating plots"
    )
    return parser.parse_args()


def load_data(data_dir):
    """Load student and problem data."""
    print(f"Loading data from {data_dir}...")

    student_df = pd.read_csv(os.path.join(data_dir, STUDENT_FILE))
    problems_df = pd.read_csv(os.path.join(data_dir, PROBLEMS_FILE))

    print(f"  Loaded {len(student_df):,} student interactions")
    print(f"  Loaded {len(problems_df):,} problems")

    return student_df, problems_df


def get_answer_options(answer_string):
    """Parse pipe-delimited answer options."""
    if pd.isna(answer_string) or answer_string == '':
        return []
    return [opt.strip() for opt in answer_string.split('||') if opt.strip()]


def get_correct_answers(correct_string):
    """Parse pipe-delimited correct answers."""
    if pd.isna(correct_string) or correct_string == '':
        return []
    return [ans.strip() for ans in correct_string.split('||') if ans.strip()]


def normalize_answer(text):
    """Normalize answer text for comparison."""
    if pd.isna(text):
        return ""
    import re
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', str(text))
    # Normalize whitespace
    text = ' '.join(text.split())
    return text.strip().lower()


def analyze_distractors(student_df, problems_df):
    """Analyze distractor effectiveness for MC (select 1) with >2 choices."""
    print("\n" + "=" * 60)
    print(" DISTRACTOR ANALYSIS")
    print("=" * 60)

    # Filter to MC (select 1) problems
    mc_problems = problems_df[problems_df['Problem Type'] == 'Multiple Choice (select 1)'].copy()

    # Count choices
    mc_problems['answer_options'] = mc_problems['Multiple Choice Options'].apply(get_answer_options)
    mc_problems['n_choices'] = mc_problems['answer_options'].apply(len)

    # Filter to >2 choices
    mc_problems = mc_problems[mc_problems['n_choices'] > 2].copy()
    print(f"\nMC (select 1) problems with >2 choices: {len(mc_problems)}")

    # Get correct answers
    mc_problems['correct_answers'] = mc_problems['Multiple Choice Answers'].apply(get_correct_answers)

    # Filter student data to these problems
    problem_ids = set(mc_problems['problem_id'])
    mc_interactions = student_df[student_df['problem_id'].isin(problem_ids)].copy()
    print(f"Student interactions for these problems: {len(mc_interactions):,}")

    # Merge to get answer options
    mc_interactions = mc_interactions.merge(
        mc_problems[['problem_id', 'answer_options', 'correct_answers', 'n_choices']],
        on='problem_id',
        how='left'
    )

    # Analyze each problem
    results = []

    for problem_id in mc_problems['problem_id'].unique():
        problem_data = mc_interactions[mc_interactions['problem_id'] == problem_id]

        if len(problem_data) < 10:  # Skip problems with too few responses
            continue

        problem_info = mc_problems[mc_problems['problem_id'] == problem_id].iloc[0]
        answer_options = problem_info['answer_options']
        correct_answers = problem_info['Fill-in Answers']

        # Normalize correct answers for comparison
        correct_normalized = set(normalize_answer(a) for a in correct_answers)

        # Count responses for each option
        option_counts = Counter()
        total_responses = 0

        for _, row in problem_data.iterrows():
            student_answer = row['answer_text']
            if pd.isna(student_answer):
                continue

            # Normalize student answer
            student_normalized = normalize_answer(student_answer)

            # Match to options
            for opt in answer_options:
                opt_normalized = normalize_answer(opt)
                if student_normalized == opt_normalized or student_normalized in opt_normalized or opt_normalized in student_normalized:
                    option_counts[opt] += 1
                    total_responses += 1
                    break

        if total_responses < 10:
            continue

        # Separate correct and incorrect options
        distractors = {}
        correct_count = 0

        for opt in answer_options:
            opt_normalized = normalize_answer(opt)
            count = option_counts.get(opt, 0)

            if opt_normalized in correct_normalized or any(normalize_answer(c) in opt_normalized or opt_normalized in normalize_answer(c) for c in correct_answers):
                correct_count = count
            else:
                distractors[opt] = count

        if not distractors:
            continue

        # Find most/least common distractor
        sorted_distractors = sorted(distractors.items(), key=lambda x: x[1], reverse=True)
        most_common = sorted_distractors[0]
        least_common = sorted_distractors[-1]

        # Compute frequencies
        distractor_freqs = {opt: count / total_responses for opt, count in distractors.items()}

        results.append({
            'problem_id': int(problem_id),
            'n_choices': int(problem_info['n_choices']),
            'total_responses': int(total_responses),
            'correct_count': int(correct_count),
            'correct_rate': correct_count / total_responses,
            'distractors': {opt: int(count) for opt, count in distractors.items()},
            'distractor_frequencies': distractor_freqs,
            'most_common_distractor': most_common[0],
            'most_common_distractor_freq': most_common[1] / total_responses,
            'least_common_distractor': least_common[0],
            'least_common_distractor_freq': least_common[1] / total_responses,
        })

    print(f"Problems with sufficient data: {len(results)}")

    return results


def print_summary(results):
    """Print summary statistics."""
    print("\n--- Summary Statistics ---")

    correct_rates = [r['correct_rate'] for r in results]
    most_common_freqs = [r['most_common_distractor_freq'] for r in results]
    least_common_freqs = [r['least_common_distractor_freq'] for r in results]

    print(f"\nCorrect Answer Rate:")
    print(f"  Mean: {np.mean(correct_rates):.1%}")
    print(f"  Median: {np.median(correct_rates):.1%}")
    print(f"  Min: {np.min(correct_rates):.1%}")
    print(f"  Max: {np.max(correct_rates):.1%}")

    print(f"\nMost Common Distractor Frequency:")
    print(f"  Mean: {np.mean(most_common_freqs):.1%}")
    print(f"  Median: {np.median(most_common_freqs):.1%}")

    print(f"\nLeast Common Distractor Frequency:")
    print(f"  Mean: {np.mean(least_common_freqs):.1%}")
    print(f"  Median: {np.median(least_common_freqs):.1%}")

    # Count problems where least common distractor is never chosen
    never_chosen = sum(1 for r in results if r['least_common_distractor_freq'] == 0)
    print(f"\nProblems with ineffective distractor (0 selections): {never_chosen} ({100*never_chosen/len(results):.1f}%)")


def save_results(results, output_dir):
    """Save results to JSON."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'distractor_stats.json')

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved: {output_path}")


def plot_results(results, output_dir):
    """Generate plots."""
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Plot 1: Correct rate distribution
    correct_rates = [r['correct_rate'] for r in results]
    axes[0].hist(correct_rates, bins=20, edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Correct Answer Rate')
    axes[0].set_ylabel('Number of Problems')
    axes[0].set_title('Distribution of Correct Answer Rates')
    axes[0].axvline(np.mean(correct_rates), color='red', linestyle='--', label=f'Mean: {np.mean(correct_rates):.1%}')
    axes[0].legend()

    # Plot 2: Most common distractor frequency
    most_common_freqs = [r['most_common_distractor_freq'] for r in results]
    axes[1].hist(most_common_freqs, bins=20, edgecolor='black', alpha=0.7, color='orange')
    axes[1].set_xlabel('Most Common Distractor Frequency')
    axes[1].set_ylabel('Number of Problems')
    axes[1].set_title('Distribution of Most Common Distractor')
    axes[1].axvline(np.mean(most_common_freqs), color='red', linestyle='--', label=f'Mean: {np.mean(most_common_freqs):.1%}')
    axes[1].legend()

    # Plot 3: Least common distractor frequency
    least_common_freqs = [r['least_common_distractor_freq'] for r in results]
    axes[2].hist(least_common_freqs, bins=20, edgecolor='black', alpha=0.7, color='green')
    axes[2].set_xlabel('Least Common Distractor Frequency')
    axes[2].set_ylabel('Number of Problems')
    axes[2].set_title('Distribution of Least Common Distractor')
    axes[2].axvline(np.mean(least_common_freqs), color='red', linestyle='--', label=f'Mean: {np.mean(least_common_freqs):.1%}')
    axes[2].legend()

    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'distractor_analysis.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()

    print(f"Saved: {plot_path}")


def main():
    args = parse_args()

    # Load data
    student_df, problems_df = load_data(args.data_dir)

    # Analyze distractors
    results = analyze_distractors(student_df, problems_df)

    # Print summary
    print_summary(results)

    # Save results
    save_results(results, args.output_dir)

    # Plot
    if not args.no_plots:
        plot_results(results, args.output_dir)

    print("\nDone!")


if __name__ == "__main__":
    main()
