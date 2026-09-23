"""
IRT Parameter Estimation for Pedagogical Grounding

Computes Item Response Theory parameters (1PL, 2PL) from student response data
using py-irt (Bayesian inference with Pyro, native sparse data support).
"""

import argparse
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import pyro

from py_irt.models.one_param_logistic import OneParamLog
from py_irt.models.two_param_logistic import TwoParamLog

# Configuration
DEFAULT_DATA_DIR = "foundationalktdataset"
STUDENT_FILE = "Interactions.csv"
PROBLEMS_FILE = "Problems.csv"


def parse_args():
    parser = argparse.ArgumentParser(description="Compute IRT parameters using py-irt")
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
        "--min-responses",
        type=int,
        default=50,
        help="Minimum responses per problem to include (default: 50)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=500,
        help="Number of training epochs (default: 500)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "gpu"],
        help="Device for training (default: cpu)"
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


def prepare_sparse_data(student_df, min_responses=50):
    """Prepare data in sparse format for py-irt (no imputation needed)."""
    print("\nPreparing sparse data for IRT...")

    # Use discrete_score as binary response (0/1)
    responses = student_df[['user_id', 'problem_id', 'discrete_score']].copy()

    # Remove NaN responses
    responses = responses.dropna(subset=['discrete_score'])

    # Handle duplicate (student, problem) pairs - take first attempt
    responses = responses.drop_duplicates(subset=['user_id', 'problem_id'], keep='first')
    print(f"  Unique (student, problem) pairs: {len(responses):,}")

    # Filter problems with enough responses
    problem_counts = responses.groupby('problem_id').size()
    valid_problems = problem_counts[problem_counts >= min_responses].index
    responses = responses[responses['problem_id'].isin(valid_problems)]
    print(f"  Problems with >= {min_responses} responses: {len(valid_problems):,}")

    # Create mappings
    unique_students = responses['user_id'].unique()
    unique_problems = responses['problem_id'].unique()

    student_to_idx = {s: i for i, s in enumerate(unique_students)}
    problem_to_idx = {p: i for i, p in enumerate(unique_problems)}
    idx_to_problem = {i: p for p, i in problem_to_idx.items()}

    # Convert to indices
    student_indices = responses['user_id'].map(student_to_idx).values
    problem_indices = responses['problem_id'].map(problem_to_idx).values
    response_values = responses['discrete_score'].values

    print(f"  Students: {len(unique_students):,}")
    print(f"  Problems: {len(unique_problems):,}")
    print(f"  Observations: {len(responses):,}")

    return (student_indices, problem_indices, response_values,
            len(unique_students), len(unique_problems), idx_to_problem)


def compute_simple_difficulty(student_df, min_responses=50):
    """Compute simple difficulty as -logit(percent_correct) for all problems."""
    print("\nComputing simple difficulty estimates...")

    responses = student_df[['problem_id', 'discrete_score']].copy()

    # Compute percent correct per problem
    problem_stats = responses.groupby('problem_id').agg(
        n_responses=('discrete_score', 'count'),
        percent_correct=('discrete_score', 'mean')
    ).reset_index()

    # Filter by min responses
    problem_stats = problem_stats[problem_stats['n_responses'] >= min_responses]

    # Compute IRT-scale difficulty: -logit(p) = log((1-p)/p)
    # Clamp to avoid log(0)
    p = problem_stats['percent_correct'].clip(0.001, 0.999)
    problem_stats['difficulty_simple'] = np.log((1 - p) / p)

    print(f"  Problems with simple difficulty: {len(problem_stats):,}")

    return problem_stats


def fit_irt_models(student_indices, problem_indices, response_values,
                   num_students, num_problems, epochs, device):
    """Fit 1PL and 2PL IRT models using py-irt."""
    print(f"\nFitting IRT models ({epochs} epochs, device={device})...")

    # Convert to tensors
    device_torch = torch.device('cuda' if device == 'gpu' else 'cpu')
    models = torch.tensor(student_indices, dtype=torch.long, device=device_torch)
    items = torch.tensor(problem_indices, dtype=torch.long, device=device_torch)
    # Ensure responses are 0/1 integers, then convert to float for Bernoulli
    response_int = np.round(response_values).astype(int).clip(0, 1)
    obs = torch.tensor(response_int, dtype=torch.float, device=device_torch)

    results = {}

    # Fit 1PL
    print("  Fitting 1PL (Rasch)...")
    try:
        pyro.clear_param_store()
        model_1pl = OneParamLog(
            priors='vague',
            device=device,
            num_items=num_problems,
            num_models=num_students,
            verbose=False
        )
        model_1pl.fit(models, items, obs, num_epochs=epochs)

        # Extract parameters
        difficulty_1pl = pyro.param('loc_diff').detach().cpu().numpy()
        results['1PL'] = {
            'difficulty': difficulty_1pl.tolist()
        }
        print(f"    Difficulty range: [{difficulty_1pl.min():.2f}, {difficulty_1pl.max():.2f}]")
    except Exception as e:
        print(f"    1PL failed: {e}")
        results['1PL'] = None

    # Fit 2PL
    print("  Fitting 2PL...")
    try:
        pyro.clear_param_store()
        model_2pl = TwoParamLog(
            priors='vague',
            device=device,
            num_items=num_problems,
            num_models=num_students,
            verbose=False
        )
        model_2pl.fit(models, items, obs, num_epochs=epochs)

        # Extract parameters
        difficulty_2pl = pyro.param('loc_diff').detach().cpu().numpy()
        discrimination_2pl = pyro.param('loc_slope').detach().cpu().numpy()

        results['2PL'] = {
            'difficulty': difficulty_2pl.tolist(),
            'discrimination': discrimination_2pl.tolist()
        }
        print(f"    Difficulty range: [{difficulty_2pl.min():.2f}, {difficulty_2pl.max():.2f}]")
        print(f"    Discrimination range: [{discrimination_2pl.min():.2f}, {discrimination_2pl.max():.2f}]")
    except Exception as e:
        print(f"    2PL failed: {e}")
        results['2PL'] = None

    return results


def format_results(irt_results, idx_to_problem, simple_stats):
    """Format results as per-problem dictionary."""
    formatted = []

    # Get IRT problems
    irt_problem_ids = set(idx_to_problem.values())

    # Process IRT results
    for idx, problem_id in idx_to_problem.items():
        item = {'problem_id': int(problem_id)}

        if irt_results['1PL']:
            item['difficulty_1pl'] = float(irt_results['1PL']['difficulty'][idx])

        if irt_results['2PL']:
            item['difficulty_2pl'] = float(irt_results['2PL']['difficulty'][idx])
            item['discrimination_2pl'] = float(irt_results['2PL']['discrimination'][idx])

        # Add simple difficulty
        simple_row = simple_stats[simple_stats['problem_id'] == problem_id]
        if len(simple_row) > 0:
            item['difficulty_simple'] = float(simple_row['difficulty_simple'].iloc[0])
            item['percent_correct'] = float(simple_row['percent_correct'].iloc[0])
            item['n_responses'] = int(simple_row['n_responses'].iloc[0])

        formatted.append(item)

    # Add problems not in IRT but in simple stats
    for _, row in simple_stats.iterrows():
        if row['problem_id'] not in irt_problem_ids:
            formatted.append({
                'problem_id': int(row['problem_id']),
                'difficulty_simple': float(row['difficulty_simple']),
                'percent_correct': float(row['percent_correct']),
                'n_responses': int(row['n_responses'])
            })

    return formatted


def print_summary(irt_results, simple_stats):
    """Print summary statistics."""
    print("\n--- Summary Statistics ---")

    print(f"\nSimple Difficulty (all {len(simple_stats)} problems):")
    print(f"  Mean: {simple_stats['difficulty_simple'].mean():.2f}")
    print(f"  Std: {simple_stats['difficulty_simple'].std():.2f}")
    print(f"  Range: [{simple_stats['difficulty_simple'].min():.2f}, {simple_stats['difficulty_simple'].max():.2f}]")

    if irt_results['2PL']:
        difficulties = irt_results['2PL']['difficulty']
        discriminations = irt_results['2PL']['discrimination']

        print(f"\n2PL Difficulty (b):")
        print(f"  Mean: {np.mean(difficulties):.2f}")
        print(f"  Std: {np.std(difficulties):.2f}")
        print(f"  Range: [{np.min(difficulties):.2f}, {np.max(difficulties):.2f}]")

        print(f"\n2PL Discrimination (a):")
        print(f"  Mean: {np.mean(discriminations):.2f}")
        print(f"  Std: {np.std(discriminations):.2f}")
        print(f"  Range: [{np.min(discriminations):.2f}, {np.max(discriminations):.2f}]")

        # Categorize difficulty
        easy = sum(1 for d in difficulties if d < -1)
        medium = sum(1 for d in difficulties if -1 <= d <= 1)
        hard = sum(1 for d in difficulties if d > 1)
        print(f"\nDifficulty Categories:")
        print(f"  Easy (b < -1): {easy} ({100*easy/len(difficulties):.1f}%)")
        print(f"  Medium (-1 <= b <= 1): {medium} ({100*medium/len(difficulties):.1f}%)")
        print(f"  Hard (b > 1): {hard} ({100*hard/len(difficulties):.1f}%)")


def save_results(formatted_results, output_dir):
    """Save results to JSON."""
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'irt_parameters.json')
    with open(output_path, 'w') as f:
        json.dump(formatted_results, f, indent=2)
    print(f"\nSaved: {output_path}")
    print(f"  Total problems: {len(formatted_results)}")


def plot_results(irt_results, simple_stats, output_dir):
    """Generate plots."""
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Simple difficulty distribution (all problems)
    axes[0, 0].hist(simple_stats['difficulty_simple'], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
    axes[0, 0].set_xlabel('Difficulty (logit scale)')
    axes[0, 0].set_ylabel('Number of Problems')
    axes[0, 0].set_title(f'Simple Difficulty Distribution (n={len(simple_stats)})')
    axes[0, 0].axvline(0, color='red', linestyle='--', alpha=0.5)

    if irt_results['2PL']:
        difficulties = irt_results['2PL']['difficulty']
        discriminations = irt_results['2PL']['discrimination']

        # Plot 2: 2PL Difficulty
        axes[0, 1].hist(difficulties, bins=30, edgecolor='black', alpha=0.7, color='orange')
        axes[0, 1].set_xlabel('Difficulty (b)')
        axes[0, 1].set_ylabel('Number of Problems')
        axes[0, 1].set_title(f'2PL Difficulty Distribution (n={len(difficulties)})')
        axes[0, 1].axvline(0, color='red', linestyle='--', alpha=0.5)

        # Plot 3: 2PL Discrimination
        axes[1, 0].hist(discriminations, bins=30, edgecolor='black', alpha=0.7, color='green')
        axes[1, 0].set_xlabel('Discrimination (a)')
        axes[1, 0].set_ylabel('Number of Problems')
        axes[1, 0].set_title('2PL Discrimination Distribution')
        axes[1, 0].axvline(1, color='red', linestyle='--', alpha=0.5)

        # Plot 4: Difficulty vs Discrimination scatter
        axes[1, 1].scatter(difficulties, discriminations, alpha=0.5)
        axes[1, 1].set_xlabel('Difficulty (b)')
        axes[1, 1].set_ylabel('Discrimination (a)')
        axes[1, 1].set_title('Difficulty vs Discrimination')
        axes[1, 1].axhline(1, color='red', linestyle='--', alpha=0.3)
        axes[1, 1].axvline(0, color='red', linestyle='--', alpha=0.3)
    else:
        for ax in [axes[0, 1], axes[1, 0], axes[1, 1]]:
            ax.text(0.5, 0.5, '2PL not fitted', ha='center', va='center', transform=ax.transAxes)

    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'irt_parameters.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()

    print(f"Saved: {plot_path}")


def main():
    args = parse_args()

    # Load data
    student_df, problems_df = load_data(args.data_dir)

    # Compute simple difficulty for ALL problems
    simple_stats = compute_simple_difficulty(student_df, args.min_responses)

    # Prepare sparse data for IRT (no imputation!)
    (student_indices, problem_indices, response_values,
     num_students, num_problems, idx_to_problem) = prepare_sparse_data(
        student_df, args.min_responses
    )

    # Fit IRT models
    irt_results = fit_irt_models(
        student_indices, problem_indices, response_values,
        num_students, num_problems, args.epochs, args.device
    )

    # Print summary
    print_summary(irt_results, simple_stats)

    # Format and save results
    formatted = format_results(irt_results, idx_to_problem, simple_stats)
    save_results(formatted, args.output_dir)

    # Plot
    if not args.no_plots:
        plot_results(irt_results, simple_stats, args.output_dir)

    print("\nDone!")


if __name__ == "__main__":
    main()
