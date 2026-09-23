"""
Base module for Pedagogical Grounding LLM Benchmark.

This module benchmarks LLMs on 4 pedagogical reasoning tasks:
1. Difficulty comparison: Which of two questions has higher IRT difficulty?
2. Discrimination comparison: Which of two questions has higher discrimination?
3. Most common distractor: Which wrong answer is most commonly chosen?
4. Least common distractor: Which wrong answer is least commonly chosen?

================================================================================
INPUT FILES (relative to --data-dir):
================================================================================
- pedagogical_grounding/output/irt_parameters.json
    Source: Pre-computed IRT parameters (~2,548 problems)
    Used by: difficulty, discrimination tasks
    Fields: problem_id, difficulty_2pl, discrimination_2pl, percent_correct

- pedagogical_grounding/output/distractor_stats.json
    Source: Pre-computed distractor analysis (~236 MC problems)
    Used by: distractor_most, distractor_least tasks
    Fields: problem_id, most_common_distractor, least_common_distractor, distractors

- foundationalktdataset/Problems.csv
    Source: Problem text and answer options
    Used by: All tasks (merged by problem_id to get question text)

================================================================================
OUTPUT FORMAT (JSONL):
================================================================================
Each line is a JSON object with:
- prediction_id: Unique identifier (e.g., "difficulty_405080_448452")
- task: Task name ("difficulty", "discrimination", "distractor_most", "distractor_least")
- ground_truth: Correct answer from IRT/distractor data
- predicted_answer: LLM's prediction
- is_correct: Boolean indicating if prediction matches ground truth
- full_response: Raw LLM output text

Output filename pattern: {model_prefix}_pedagogical_{task}_n{samples}_{mode}_mindiff_dot{X}.jsonl
Example: gptoss120b_pedagogical_difficulty_n1000_stratified_mindiff_dot2.jsonl

================================================================================
EVALUATION:
================================================================================
Run separately after inference:

    python evaluate_pedagogical.py --input <results.jsonl>
    python evaluate_pedagogical.py --input <results.jsonl> --output metrics.json

Metrics computed:
- Overall accuracy vs random baseline (50% for comparison, ~33% for distractors)
- Accuracy by stratum (small/medium/large difference) for comparison tasks
- Accuracy by number of distractors for distractor tasks

================================================================================
SAMPLING MODES (--sampling-mode):
================================================================================
For comparison tasks (difficulty, discrimination):

- "random": Randomly pair any two questions
    May include trivial pairs with nearly identical values

- "stratified" (default): Ensure meaningful differences between pairs
    Samples equally from 3 strata:
    - Small:  0.2 - 0.5 difference (hard comparisons)
    - Medium: 0.5 - 1.0 difference (moderate comparisons)
    - Large:  > 1.0 difference (easy comparisons)

================================================================================
CLI ARGUMENTS:
================================================================================
Required:
  --task, -t          Task to run (see below)

Sampling:
  --sampling-mode, -s Pair sampling: "random" or "stratified" (default: stratified)
  --num-samples, -n   Number of pairs/problems to sample (default: 1000)
  --min-difference    Min difference for stratified sampling (default: 0.2)
  --seed              Random seed for reproducibility (default: 42)

Output:
  --output, -o        Output JSONL file path (overrides auto-generated name)
  --output-dir        Output directory for results (default: current directory)
  --data-dir, -d      Base directory containing data files (default: .)

vLLM Configuration:
  --batch-size, -b    Batch size for inference (default: 500)
  --num-gpus          GPUs for tensor parallelism (default: 1)
  --cache-dir, -c     Directory for model cache (vLLM download_dir)
  --max-num-seqs      Max sequences per batch
  --max-model-len     Max sequence length in tokens
  --gpu-memory-utilization  Fraction of GPU memory (default: 0.9)
  --reasoning-level   For models that support it: none/low/medium/high

================================================================================
TASK SELECTION (--task, REQUIRED):
================================================================================
- "difficulty": Compare IRT difficulty between question pairs
- "discrimination": Compare IRT discrimination between question pairs
- "distractor_most": Predict most commonly chosen wrong answer
- "distractor_least": Predict least commonly chosen wrong answer
- "all": Run all 4 tasks sequentially

================================================================================
USAGE EXAMPLES:
================================================================================
# Run from project root directory:

# Run difficulty comparison with stratified sampling (1000 pairs)
CUDA_VISIBLE_DEVICES=0,1,2,3 python pedagogical_grounding/gptoss120b_pedagogical.py \\
    --task difficulty \\
    --num-samples 1000 \\
    --sampling-mode stratified \\
    --num-gpus 4

# Run all tasks with 500 samples each
CUDA_VISIBLE_DEVICES=0,1,2,3 python pedagogical_grounding/gptoss120b_pedagogical.py \\
    --task all \\
    --num-samples 500 \\
    --num-gpus 4

# Run distractor task (uses all 236 available MC problems)
CUDA_VISIBLE_DEVICES=0,1,2,3 python pedagogical_grounding/gptoss120b_pedagogical.py \\
    --task distractor_most \\
    --num-gpus 4

================================================================================
CREATING MODEL CONFIGS:
================================================================================
    from pedagogical_inference_base import run_inference

    MODEL_CONFIG = {
        "model_id": "model/name",
        "gen_configs": {
            "temperature": 0.3,
            "max_tokens": 1024,
        },
        "output_prefix": "prefix",
        "system_prompt_prefix": "",  # e.g., "Reasoning: medium\\n\\n" for GPT-OSS
    }

    if __name__ == "__main__":
        run_inference(MODEL_CONFIG)
"""

import argparse
import contextlib
import os
import sys
import json
import re
import gc
from typing import List, Dict, Optional, Tuple, Set

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from vllm import LLM, SamplingParams
from vllm.distributed.parallel_state import (
    destroy_model_parallel,
    destroy_distributed_environment,
)

# Add parent directory to path for clean_utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clean_utils import clean_problem_body


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles numpy types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# Default configuration
DEFAULT_NUM_SAMPLES = 1000
DEFAULT_BATCH_SIZE = 500
DEFAULT_MIN_DIFFERENCE = 0.2

# Input file paths (relative to data_dir)
IRT_PARAMS_FILE = "pedagogical_grounding/output/irt_parameters.json"
DISTRACTOR_STATS_FILE = "pedagogical_grounding/output/distractor_stats.json"
PROBLEMS_FILE = "foundationalktdataset/Problems.csv"

# Task types
TASK_DIFFICULTY = "difficulty"
TASK_DISCRIMINATION = "discrimination"
TASK_DISTRACTOR_MOST = "distractor_most"
TASK_DISTRACTOR_LEAST = "distractor_least"
TASK_ALL = "all"

COMPARISON_TASKS = [TASK_DIFFICULTY, TASK_DISCRIMINATION]
DISTRACTOR_TASKS = [TASK_DISTRACTOR_MOST, TASK_DISTRACTOR_LEAST]

# System prompts
SYSTEM_PROMPT_DIFFICULTY = """You are an expert educator evaluating mathematics problems for instructional design.

Your task is to compare two problems and determine which one is MORE DIFFICULT.

A problem is MORE DIFFICULT if:
- It requires more prerequisite knowledge or skills
- It involves more complex reasoning steps
- It has higher cognitive load
- Students are more likely to make errors
- It requires synthesizing multiple concepts

Instructions:
1. Carefully read both Problem A and Problem B
2. Consider factors like conceptual complexity, prerequisite knowledge, cognitive load, and potential for errors
3. Make your judgment based solely on the problem content
4. Respond with exactly "A" or "B"

Output Format:
Respond with a single JSON object:
{"answer": "A"} or {"answer": "B"}
"""

SYSTEM_PROMPT_DISCRIMINATION = """You are an expert educator evaluating mathematics problems for instructional design.

Your task is to compare two problems and determine which one has HIGHER DISCRIMINATION.

A problem has HIGHER DISCRIMINATION if:
- It better distinguishes between students who understand the material vs. those who don't
- Correct answers strongly indicate mastery
- Incorrect answers are unlikely for knowledgeable students
- The problem tests specific, well-defined skills rather than general guessing
- It avoids ambiguity that could confuse strong students

Instructions:
1. Carefully read both Problem A and Problem B
2. Consider how well each problem separates students by ability level
3. Make your judgment based solely on the problem content
4. Respond with exactly "A" or "B"

Output Format:
Respond with a single JSON object:
{"answer": "A"} or {"answer": "B"}
"""

SYSTEM_PROMPT_DISTRACTOR_MOST = """You are an expert educator analyzing student misconceptions in mathematics.

Your task is to predict which incorrect answer option (distractor) is MOST COMMONLY CHOSEN by students.

The MOST COMMON distractor is the wrong answer that students choose most frequently.
Common reasons include:
- It represents a predictable computational error
- It matches a common misconception
- It seems plausible but contains a subtle flaw
- It results from a partial understanding of the concept
- It's what you get if you make a typical arithmetic mistake

Instructions:
1. Read the problem carefully
2. Identify the correct answer
3. Consider common student misconceptions and errors for this type of problem
4. Analyze each incorrect answer option
5. Predict which distractor students would most often choose
6. Respond with the letter of that distractor (A, B, C, etc.)

Output Format:
Respond with a single JSON object:
{"answer": "X"} where X is the letter of the most common distractor
"""

SYSTEM_PROMPT_DISTRACTOR_LEAST = """You are an expert educator analyzing student misconceptions in mathematics.

Your task is to predict which incorrect answer option (distractor) is LEAST COMMONLY CHOSEN by students.

The LEAST COMMON distractor is the wrong answer that students rarely choose.
Common reasons include:
- It is obviously incorrect to most students
- It doesn't correspond to any common error pattern
- It requires a very unusual misconception
- It is far from the correct answer conceptually
- It looks implausible compared to other options

Instructions:
1. Read the problem carefully
2. Identify the correct answer
3. Consider which wrong answer would seem most obviously incorrect
4. Analyze each incorrect answer option
5. Predict which distractor students would rarely choose
6. Respond with the letter of that distractor (A, B, C, etc.)

Output Format:
Respond with a single JSON object:
{"answer": "X"} where X is the letter of the least common distractor
"""


def parse_args(default_output_jsonl: str) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Pedagogical Grounding LLM Benchmark"
    )

    # Task selection
    parser.add_argument(
        "--task", "-t",
        type=str,
        required=True,
        choices=[TASK_DIFFICULTY, TASK_DISCRIMINATION,
                 TASK_DISTRACTOR_MOST, TASK_DISTRACTOR_LEAST, TASK_ALL],
        help="Task to run: difficulty, discrimination, distractor_most, distractor_least, or all"
    )

    # Sampling configuration
    parser.add_argument(
        "--sampling-mode", "-s",
        type=str,
        default="stratified",
        choices=["random", "stratified"],
        help="Pair sampling mode: random or stratified (default: stratified)"
    )
    parser.add_argument(
        "--num-samples", "-n",
        type=int,
        default=DEFAULT_NUM_SAMPLES,
        help=f"Number of pairs/problems to sample (default: {DEFAULT_NUM_SAMPLES})"
    )
    parser.add_argument(
        "--min-difference",
        type=float,
        default=DEFAULT_MIN_DIFFERENCE,
        help=f"Minimum difference for stratified sampling (default: {DEFAULT_MIN_DIFFERENCE})"
    )

    # Output
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output JSONL file path (overrides auto-generated name)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory for results (default: current directory)"
    )
    parser.add_argument(
        "--data-dir", "-d",
        type=str,
        default=".",
        help="Base directory containing data files (default: current directory)"
    )

    # vLLM configuration
    parser.add_argument(
        "--batch-size", "-b",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Batch size for LLM inference (default: {DEFAULT_BATCH_SIZE})"
    )
    parser.add_argument(
        "--cache-dir", "-c",
        type=str,
        default=None,
        help="Directory for vLLM model cache"
    )
    parser.add_argument(
        "--num-gpus",
        type=int,
        default=1,
        help="Number of GPUs for tensor parallelism (default: 1)"
    )
    parser.add_argument(
        "--max-num-seqs",
        type=int,
        default=None,
        help="Maximum number of sequences to process in a batch"
    )
    parser.add_argument(
        "--max-model-len",
        type=int,
        default=None,
        help="Maximum sequence length in tokens"
    )
    parser.add_argument(
        "--gpu-memory-utilization",
        type=float,
        default=0.9,
        help="Fraction of GPU memory to use (default: 0.9)"
    )
    parser.add_argument(
        "--reasoning-level",
        type=str,
        choices=["none", "low", "medium", "high"],
        default=None,
        help="Reasoning level for models that support it"
    )

    # Reproducibility
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)"
    )

    return parser.parse_args()


def load_irt_parameters(data_dir: str) -> pd.DataFrame:
    """Load IRT parameters and merge with problem text."""
    irt_path = os.path.join(data_dir, IRT_PARAMS_FILE)
    problems_path = os.path.join(data_dir, PROBLEMS_FILE)

    print(f"Loading IRT parameters from {irt_path}...")
    with open(irt_path, 'r') as f:
        irt_data = json.load(f)

    print(f"Loading problem text from {problems_path}...")
    problems_df = pd.read_csv(problems_path)
    problems_df['cleaned_body'] = problems_df['Problem Body'].apply(clean_problem_body)

    # Merge on problem_id
    irt_df = pd.DataFrame(irt_data)
    merged = irt_df.merge(
        problems_df[['problem_id', 'cleaned_body', 'Multiple Choice Options', 'Problem Type']],
        on='problem_id',
        how='inner'
    )

    # Filter to problems with valid 2PL parameters
    merged = merged.dropna(subset=['difficulty_2pl', 'discrimination_2pl'])

    print(f"Loaded {len(merged)} problems with IRT parameters")
    return merged


def load_distractor_stats(data_dir: str) -> pd.DataFrame:
    """Load distractor stats and merge with problem text."""
    distractor_path = os.path.join(data_dir, DISTRACTOR_STATS_FILE)
    problems_path = os.path.join(data_dir, PROBLEMS_FILE)

    print(f"Loading distractor stats from {distractor_path}...")
    with open(distractor_path, 'r') as f:
        distractor_data = json.load(f)

    print(f"Loading problem text from {problems_path}...")
    problems_df = pd.read_csv(problems_path)
    problems_df['cleaned_body'] = problems_df['Problem Body'].apply(clean_problem_body)

    # Convert to DataFrame and merge
    distractor_df = pd.DataFrame(distractor_data)
    merged = distractor_df.merge(
        problems_df[['problem_id', 'cleaned_body', 'Multiple Choice Options',
                     'Multiple Choice Answers']],
        on='problem_id',
        how='inner'
    )

    print(f"Loaded {len(merged)} problems with distractor stats")
    return merged


def sample_pairs_random(
    df: pd.DataFrame,
    param_col: str,
    num_samples: int,
    seed: int = 42
) -> List[Dict]:
    """Random sampling of problem pairs."""
    np.random.seed(seed)

    problem_ids = df['problem_id'].values
    n = len(problem_ids)

    pairs = []
    sampled = set()
    max_attempts = num_samples * 10
    attempts = 0

    while len(pairs) < num_samples and attempts < max_attempts:
        attempts += 1
        i, j = np.random.choice(n, size=2, replace=False)

        # Ensure we don't duplicate pairs
        pair_key = tuple(sorted([problem_ids[i], problem_ids[j]]))
        if pair_key in sampled:
            continue
        sampled.add(pair_key)

        row_a = df.iloc[i]
        row_b = df.iloc[j]

        # Skip if values are too close (tie)
        val_a = row_a[param_col]
        val_b = row_b[param_col]
        if abs(val_a - val_b) < 0.01:
            continue

        # Determine ground truth
        ground_truth = "A" if val_a > val_b else "B"

        pairs.append({
            'problem_id_a': int(row_a['problem_id']),
            'problem_id_b': int(row_b['problem_id']),
            'text_a': row_a['cleaned_body'],
            'text_b': row_b['cleaned_body'],
            'value_a': float(val_a),
            'value_b': float(val_b),
            'difference': float(abs(val_a - val_b)),
            'ground_truth': ground_truth,
            'stratum': 'random'
        })

    print(f"Sampled {len(pairs)} random pairs")
    return pairs


def sample_pairs_stratified(
    df: pd.DataFrame,
    param_col: str,
    num_samples: int,
    min_difference: float = 0.2,
    seed: int = 42
) -> List[Dict]:
    """Stratified sampling to ensure meaningful differences."""
    np.random.seed(seed)

    values = df[param_col].values
    problem_ids = df['problem_id'].values
    n = len(problem_ids)

    # Define strata
    strata = [
        ('small', min_difference, 0.5),
        ('medium', 0.5, 1.0),
        ('large', 1.0, float('inf'))
    ]

    samples_per_stratum = num_samples // len(strata)

    pairs = []
    sampled = set()

    for stratum_name, low, high in strata:
        stratum_pairs = []
        attempts = 0
        max_attempts = samples_per_stratum * 100

        while len(stratum_pairs) < samples_per_stratum and attempts < max_attempts:
            attempts += 1
            i = np.random.randint(0, n)
            j = np.random.randint(0, n)

            if i == j:
                continue

            diff = abs(values[i] - values[j])
            if not (low <= diff < high):
                continue

            pair_key = tuple(sorted([problem_ids[i], problem_ids[j]]))
            if pair_key in sampled:
                continue
            sampled.add(pair_key)

            row_a = df.iloc[i]
            row_b = df.iloc[j]
            ground_truth = "A" if row_a[param_col] > row_b[param_col] else "B"

            stratum_pairs.append({
                'problem_id_a': int(row_a['problem_id']),
                'problem_id_b': int(row_b['problem_id']),
                'text_a': row_a['cleaned_body'],
                'text_b': row_b['cleaned_body'],
                'value_a': float(row_a[param_col]),
                'value_b': float(row_b[param_col]),
                'difference': float(diff),
                'ground_truth': ground_truth,
                'stratum': stratum_name
            })

        pairs.extend(stratum_pairs)
        print(f"  Stratum '{stratum_name}' ({low:.1f}-{high:.1f}): {len(stratum_pairs)} pairs")

    print(f"Total stratified pairs: {len(pairs)}")
    return pairs


def sample_distractor_problems(
    df: pd.DataFrame,
    num_samples: Optional[int] = None,
    seed: int = 42
) -> List[Dict]:
    """Sample distractor problems (or use all if num_samples > available)."""
    np.random.seed(seed)

    if num_samples is None or num_samples >= len(df):
        sampled = df
        print(f"Using all {len(df)} distractor problems")
    else:
        sampled = df.sample(n=num_samples, random_state=seed)
        print(f"Sampled {num_samples} distractor problems from {len(df)}")

    return sampled.to_dict('records')


def format_answer_options(answer_string: str) -> Tuple[str, Dict[str, str]]:
    """Format pipe-delimited answers for display.

    Returns:
        formatted_text: String like "A) Option1\nB) Option2..."
        letter_map: Dict mapping letters to option text
    """
    if pd.isna(answer_string) or answer_string == '':
        return "", {}

    options = [opt.strip() for opt in answer_string.split('||')]
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    letter_map = {}
    lines = []
    for i, opt in enumerate(options):
        if i < len(letters):
            letter_map[letters[i]] = opt
            lines.append(f"{letters[i]}) {opt}")

    return '\n'.join(lines), letter_map


def get_correct_letter(correct_answer: str, letter_map: Dict[str, str]) -> Optional[str]:
    """Find the letter corresponding to the correct answer."""
    if pd.isna(correct_answer):
        return None

    correct_answer = correct_answer.strip()
    for letter, text in letter_map.items():
        if text.strip() == correct_answer:
            return letter
    return None


def get_distractor_letter(distractor_text: str, letter_map: Dict[str, str]) -> Optional[str]:
    """Find the letter corresponding to a distractor."""
    if pd.isna(distractor_text):
        return None

    distractor_text = distractor_text.strip()
    for letter, text in letter_map.items():
        if text.strip() == distractor_text:
            return letter
    return None


def create_comparison_prompt(text_a: str, text_b: str, task_type: str) -> str:
    """Create user prompt for difficulty/discrimination comparison."""
    if task_type == TASK_DIFFICULTY:
        comparison_type = "more difficult"
    else:
        comparison_type = "more discriminating (better at distinguishing student ability levels)"

    return f"""Compare the following two problems and determine which is {comparison_type}.

**Problem A:**
{text_a}

**Problem B:**
{text_b}

Which problem is {comparison_type}? Respond with {{"answer": "A"}} or {{"answer": "B"}}."""


def create_distractor_prompt(
    problem_text: str,
    options_formatted: str,
    correct_letter: str,
    task_type: str
) -> str:
    """Create user prompt for distractor prediction."""
    if task_type == TASK_DISTRACTOR_MOST:
        distractor_type = "MOST COMMONLY"
        behavior = "most often"
    else:
        distractor_type = "LEAST COMMONLY"
        behavior = "least often"

    return f"""Analyze this multiple-choice problem and predict which distractor (wrong answer) is {distractor_type} chosen by students.

**Problem:**
{problem_text}

**Answer Options:**
{options_formatted}

**Correct Answer:** {correct_letter}

Which incorrect answer option do students choose {behavior}? Respond with {{"answer": "X"}} where X is the letter of the distractor."""


def extract_json_prediction(response_text: str) -> Optional[Dict]:
    """Extract the JSON prediction from the model's response."""
    json_matches = re.findall(r'\{[^{}]*\}', response_text)

    if json_matches:
        # Take the last JSON object
        json_str = json_matches[-1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    return None


def extract_answer(response_text: str) -> Optional[str]:
    """Extract answer (A/B or letter) from response."""
    prediction = extract_json_prediction(response_text)
    if prediction and 'answer' in prediction:
        return str(prediction['answer']).strip().upper()

    # Fallback: look for standalone A or B
    match = re.search(r'\b([A-H])\b', response_text)
    if match:
        return match.group(1)

    return None


def load_completed_predictions(output_jsonl: str) -> Set[str]:
    """Load already-completed prediction IDs from JSONL file."""
    completed = set()
    if os.path.exists(output_jsonl):
        with open(output_jsonl, 'r') as f:
            for line in f:
                if line.strip():
                    result = json.loads(line)
                    completed.add(result['prediction_id'])
        print(f"Loaded {len(completed)} completed predictions from {output_jsonl}")
    return completed


def append_results_jsonl(results: List[Dict], output_jsonl: str) -> None:
    """Append batch results to JSONL file."""
    with open(output_jsonl, 'a') as f:
        for result in results:
            f.write(json.dumps(result, cls=NumpyEncoder) + '\n')


def prepare_comparison_batch(
    samples: List[Dict],
    task_type: str,
    system_prompt: str,
    completed_ids: Set[str]
) -> Tuple[List[str], List[Dict]]:
    """Prepare prompts and metadata for comparison task."""
    prompts = []
    metadata = []

    for i, sample in enumerate(samples):
        pred_id = f"{task_type}_{sample['problem_id_a']}_{sample['problem_id_b']}"

        if pred_id in completed_ids:
            continue

        user_prompt = create_comparison_prompt(
            sample['text_a'],
            sample['text_b'],
            task_type
        )
        full_prompt = system_prompt + "\n\n" + user_prompt

        prompts.append(full_prompt)
        metadata.append({
            'prediction_id': pred_id,
            'task': task_type,
            'problem_id_a': sample['problem_id_a'],
            'problem_id_b': sample['problem_id_b'],
            'value_a': sample['value_a'],
            'value_b': sample['value_b'],
            'difference': sample['difference'],
            'ground_truth': sample['ground_truth'],
            'stratum': sample.get('stratum', 'unknown'),
            'prompt': full_prompt
        })

    return prompts, metadata


def prepare_distractor_batch(
    samples: List[Dict],
    task_type: str,
    system_prompt: str,
    completed_ids: Set[str]
) -> Tuple[List[str], List[Dict]]:
    """Prepare prompts and metadata for distractor task."""
    prompts = []
    metadata = []

    for sample in samples:
        pred_id = f"{task_type}_{sample['problem_id']}"

        if pred_id in completed_ids:
            continue

        # Format answer options
        options_formatted, letter_map = format_answer_options(
            sample['Multiple Choice Options']
        )

        if not options_formatted:
            continue

        # Get correct answer letter
        correct_letter = get_correct_letter(
            sample.get('Multiple Choice Answers', ''),
            letter_map
        )

        if not correct_letter:
            # Try to infer from distractor data
            distractors = sample.get('distractors', {})
            all_letters = set(letter_map.keys())
            distractor_letters = set()
            for d_text in distractors.keys():
                d_letter = get_distractor_letter(d_text, letter_map)
                if d_letter:
                    distractor_letters.add(d_letter)
            correct_letters = all_letters - distractor_letters
            if len(correct_letters) == 1:
                correct_letter = list(correct_letters)[0]
            else:
                continue  # Skip if we can't determine correct answer

        # Get ground truth distractor letter
        if task_type == TASK_DISTRACTOR_MOST:
            ground_truth_text = sample.get('most_common_distractor', '')
            ground_truth_freq = sample.get('most_common_distractor_freq', 0)
        else:
            ground_truth_text = sample.get('least_common_distractor', '')
            ground_truth_freq = sample.get('least_common_distractor_freq', 0)

        ground_truth_letter = get_distractor_letter(ground_truth_text, letter_map)
        if not ground_truth_letter:
            continue  # Skip if we can't map ground truth

        user_prompt = create_distractor_prompt(
            sample['cleaned_body'],
            options_formatted,
            correct_letter,
            task_type
        )
        full_prompt = system_prompt + "\n\n" + user_prompt

        prompts.append(full_prompt)
        metadata.append({
            'prediction_id': pred_id,
            'task': task_type,
            'problem_id': sample['problem_id'],
            'n_choices': sample.get('n_choices', len(letter_map)),
            'correct_letter': correct_letter,
            'ground_truth_letter': ground_truth_letter,
            'ground_truth_text': ground_truth_text,
            'ground_truth_freq': ground_truth_freq,
            'distractors': sample.get('distractors', {}),
            'letter_map': letter_map,
            'prompt': full_prompt
        })

    return prompts, metadata


def process_comparison_results(
    metadata: List[Dict],
    responses: List[str]
) -> List[Dict]:
    """Process comparison task results."""
    results = []

    for meta, response in zip(metadata, responses):
        predicted = extract_answer(response)
        is_correct = predicted == meta['ground_truth'] if predicted else False

        results.append({
            'prediction_id': meta['prediction_id'],
            'task': meta['task'],
            'problem_id_a': meta['problem_id_a'],
            'problem_id_b': meta['problem_id_b'],
            'value_a': meta['value_a'],
            'value_b': meta['value_b'],
            'difference': meta['difference'],
            'stratum': meta['stratum'],
            'ground_truth': meta['ground_truth'],
            'predicted_answer': predicted,
            'is_correct': is_correct,
            'full_response': response
        })

    return results


def process_distractor_results(
    metadata: List[Dict],
    responses: List[str]
) -> List[Dict]:
    """Process distractor task results."""
    results = []

    for meta, response in zip(metadata, responses):
        predicted = extract_answer(response)
        is_correct = predicted == meta['ground_truth_letter'] if predicted else False

        results.append({
            'prediction_id': meta['prediction_id'],
            'task': meta['task'],
            'problem_id': meta['problem_id'],
            'n_choices': meta['n_choices'],
            'correct_letter': meta['correct_letter'],
            'ground_truth_letter': meta['ground_truth_letter'],
            'ground_truth_text': meta['ground_truth_text'],
            'ground_truth_freq': meta['ground_truth_freq'],
            'predicted_answer': predicted,
            'is_correct': is_correct,
            'full_response': response
        })

    return results


def get_system_prompt(task_type: str, prefix: str = "") -> str:
    """Get the system prompt for a task type."""
    prompts = {
        TASK_DIFFICULTY: SYSTEM_PROMPT_DIFFICULTY,
        TASK_DISCRIMINATION: SYSTEM_PROMPT_DISCRIMINATION,
        TASK_DISTRACTOR_MOST: SYSTEM_PROMPT_DISTRACTOR_MOST,
        TASK_DISTRACTOR_LEAST: SYSTEM_PROMPT_DISTRACTOR_LEAST,
    }
    return prefix + prompts[task_type]


def run_inference(config: Dict) -> None:
    """Main inference function that runs pedagogical grounding benchmark.

    Args:
        config: Dict with keys:
            - model_id: HuggingFace model ID
            - gen_configs: Dict of generation parameters
            - output_prefix: Prefix for output filename
            - system_prompt_prefix: Optional prefix for system prompt
    """
    model_id = config["model_id"]
    gen_configs = config["gen_configs"]
    output_prefix = config["output_prefix"]

    # Parse arguments
    default_output_jsonl = f"{output_prefix}_pedagogical.jsonl"
    args = parse_args(default_output_jsonl)

    # Determine system prompt prefix
    if args.reasoning_level is not None:
        if args.reasoning_level == "none":
            system_prompt_prefix = ""
        else:
            system_prompt_prefix = f"Reasoning: {args.reasoning_level}\n\n"
    else:
        system_prompt_prefix = config.get("system_prompt_prefix", "")

    # Determine tasks to run
    if args.task == TASK_ALL:
        tasks = COMPARISON_TASKS + DISTRACTOR_TASKS
    else:
        tasks = [args.task]

    # Generate output filename
    task_str = args.task
    # Format min_difference as "dot1" for 0.1, "dot2" for 0.2, etc.
    mindiff_str = f"_mindiff_dot{str(args.min_difference).replace('0.', '')}"
    params_suffix = f"_{task_str}_n{args.num_samples}_{args.sampling_mode}{mindiff_str}"

    if args.output:
        # Use explicit output path
        output_jsonl = args.output
    else:
        # Auto-generate filename in output directory
        filename = f"{output_prefix}_pedagogical{params_suffix}.jsonl"
        output_jsonl = os.path.join(args.output_dir, filename)

    print(f"Model: {model_id}")
    print(f"Tasks: {tasks}")
    print(f"Sampling mode: {args.sampling_mode}")
    print(f"Num samples: {args.num_samples}")
    print(f"Output: {output_jsonl}")
    print(f"Data directory: {args.data_dir}")

    # Load data
    irt_df = None
    distractor_df = None

    if any(t in COMPARISON_TASKS for t in tasks):
        irt_df = load_irt_parameters(args.data_dir)

    if any(t in DISTRACTOR_TASKS for t in tasks):
        distractor_df = load_distractor_stats(args.data_dir)

    # Load completed predictions for resume support
    completed_ids = load_completed_predictions(output_jsonl)

    # Prepare all prompts and metadata
    all_prompts = []
    all_metadata = []
    task_info = []  # Track which task each prompt belongs to

    for task_type in tasks:
        print(f"\nPreparing {task_type} task...")

        if task_type in COMPARISON_TASKS:
            param_col = 'difficulty_2pl' if task_type == TASK_DIFFICULTY else 'discrimination_2pl'

            if args.sampling_mode == 'stratified':
                samples = sample_pairs_stratified(
                    irt_df, param_col, args.num_samples,
                    args.min_difference, args.seed
                )
            else:
                samples = sample_pairs_random(
                    irt_df, param_col, args.num_samples, args.seed
                )

            system_prompt = get_system_prompt(task_type, system_prompt_prefix)
            prompts, metadata = prepare_comparison_batch(
                samples, task_type, system_prompt, completed_ids
            )

            all_prompts.extend(prompts)
            all_metadata.extend(metadata)
            task_info.extend([task_type] * len(prompts))

        else:  # Distractor tasks
            samples = sample_distractor_problems(
                distractor_df, args.num_samples, args.seed
            )

            system_prompt = get_system_prompt(task_type, system_prompt_prefix)
            prompts, metadata = prepare_distractor_batch(
                samples, task_type, system_prompt, completed_ids
            )

            all_prompts.extend(prompts)
            all_metadata.extend(metadata)
            task_info.extend([task_type] * len(prompts))

    print(f"\nTotal predictions to make: {len(all_prompts)}")
    print(f"Already completed: {len(completed_ids)}")

    if not all_prompts:
        print("All predictions already completed!")
        return

    # Initialize vLLM engine
    print("\nInitializing vLLM engine...")
    sampling_params = SamplingParams(**gen_configs)
    llm_kwargs = {
        "model": model_id,
        "tensor_parallel_size": args.num_gpus,
        "trust_remote_code": True,
        "gpu_memory_utilization": args.gpu_memory_utilization,
        "enable_prefix_caching": True,
    }
    if args.max_num_seqs is not None:
        llm_kwargs["max_num_seqs"] = args.max_num_seqs
    if args.max_model_len is not None:
        llm_kwargs["max_model_len"] = args.max_model_len
    if args.cache_dir:
        llm_kwargs["download_dir"] = args.cache_dir

    llm = LLM(**llm_kwargs)

    # Process in batches
    batch_size = args.batch_size
    num_batches = (len(all_prompts) + batch_size - 1) // batch_size
    total_results = 0

    for batch_idx in range(num_batches):
        batch_start = batch_idx * batch_size
        batch_end = min(batch_start + batch_size, len(all_prompts))

        batch_prompts = all_prompts[batch_start:batch_end]
        batch_metadata = all_metadata[batch_start:batch_end]
        batch_tasks = task_info[batch_start:batch_end]

        print(f"\n{'='*80}")
        print(f"Processing batch {batch_idx + 1}/{num_batches}")
        print(f"Items: {batch_start} to {batch_end} ({len(batch_prompts)} prompts)")
        print(f"{'='*80}")

        try:
            outputs = llm.generate(batch_prompts, sampling_params)
            response_texts = [o.outputs[0].text.strip() for o in outputs]

            # Process results based on task type
            batch_results = []
            for meta, response, task_type in zip(batch_metadata, response_texts, batch_tasks):
                if task_type in COMPARISON_TASKS:
                    result = process_comparison_results([meta], [response])[0]
                else:
                    result = process_distractor_results([meta], [response])[0]
                batch_results.append(result)

            # Save results
            append_results_jsonl(batch_results, output_jsonl)
            total_results += len(batch_results)

            # Print batch summary
            correct = sum(1 for r in batch_results if r.get('is_correct', False))
            print(f"Batch accuracy: {correct}/{len(batch_results)} ({100*correct/len(batch_results):.1f}%)")
            print(f"Total results so far: {total_results}")

        except Exception as e:
            print(f"\nERROR processing batch {batch_idx + 1}: {str(e)}")
            print(f"Progress saved in {output_jsonl} - restart to resume")
            raise

    print(f"\n{'='*80}")
    print("All batches processed successfully!")
    print(f"{'='*80}")
    print(f"Results saved to: {output_jsonl}")
    print(f"Total predictions: {total_results}")

    # Cleanup
    print("\nCleaning up...")
    destroy_model_parallel()
    destroy_distributed_environment()
    del llm
    with contextlib.suppress(AssertionError):
        torch.distributed.destroy_process_group()
    gc.collect()
    torch.cuda.empty_cache()

    print("\nDone!")
