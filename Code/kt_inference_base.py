"""
Base module for Knowledge Tracing LLM inference.

This module contains all shared logic for running KT inference with different models.
Each model script imports this and provides model-specific configuration.

Usage in model scripts:
    from kt_inference_base import run_inference

    MODEL_CONFIG = {
        "model_id": "model/name",
        "gen_configs": {...},
        "output_prefix": "prefix",
        "system_prompt_prefix": "",  # e.g., "Reasoning: medium\n\n"
    }

    if __name__ == "__main__":
        run_inference(MODEL_CONFIG)
"""

import argparse
import contextlib
import os
from vllm import LLM, SamplingParams
import pandas as pd
import gc
import torch
from vllm.distributed.parallel_state import (
    destroy_model_parallel,
    destroy_distributed_environment,
)
import json
import re
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from clean_utils import clean_problem_body
from cleantext import clean_text as clean_text_legacy


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


# Batch processing config defaults
DEFAULT_BATCH_SIZE = 10000
DEFAULT_NUM_STUDENTS = 500
DEFAULT_BIN_SIZE = 50
DEFAULT_MIN_HISTORY = 50

# Input file names
STUDENT_FILE = "Interactions.csv"
PROBLEMS_FILE = "Problems.csv"
SKILL_FILE = "Skills.csv"

# Base system prompt (without any prefix like "Reasoning: medium")
BASE_SYSTEM_PROMPT = """You are a reasoning model trained to simulate a student's evolving knowledge and response behavior in mathematics.

Your goal is to infer, from past problem–answer pairs, how this same student is likely to perform on a new problem — at multiple levels of granularity.

You must reason about the student's learning progression, skill mastery, and recurring misconceptions, then produce structured predictions for the new item.

---

Your Task:

Generate three coordinated predictions for this student:

1) **Skill-level knowledge tracing (0 or 1):** Whether the student has mastered the underlying skill involved in the new problem.
2) **Question-level knowledge tracing (0 or 1):** Whether the student will answer this specific problem correctly.
3) **Cognitive-level prediction (string):** The exact answer text or option the student would most likely produce, written in their own response style.

---

Reasoning Guidelines:

- Use the student's historical data (problems, answers, hints, timestamps) to infer learning and forgetting patterns.
- Consider recency and exposure: later timestamps often indicate updated knowledge.
- Treat `UsedHint=True` or `SawAnswer=True` as evidence that the student's recorded answer may not reflect true mastery — they might have seen or been helped toward the solution.
- Attend to how the student's accuracy, style, and misconceptions evolve over time.
- You may think step-by-step internally, but your final output must follow the format below.
---

Output Format:

When you are done reasoning, **finish your response with** the JSON object in this exact structure:

For Multiple Choice (select 1) problems:
{
"skill_level": 0 or 1,
"question_level": 0 or 1,
"student_answer": "A" (single letter only)
}

For Multiple Choice (select all) problems:
{
"skill_level": 0 or 1,
"question_level": 0 or 1,
"student_answer": "A, C" (comma-separated letters if multiple selections)
}

For Fill-in problems:
{
"skill_level": 0 or 1,
"question_level": 0 or 1,
"student_answer": "<string exactly as this student would write (e.g., 'x=3', '3/5', '12')>"
}

Predictions must be consistent. If you predict question_level to be 1, then student_answer must match the correct answer. If you predict question_level to be 0, student_answer must not match the correct answer."""


def parse_args(default_output_jsonl):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Knowledge Tracing with LLM")
    parser.add_argument(
        "--batch-size", "-b",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Batch size for LLM inference (default: {DEFAULT_BATCH_SIZE})"
    )
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
        help="Directory containing input CSV files (default: current directory)"
    )
    parser.add_argument(
        "--cache-dir", "-c",
        type=str,
        default=None,
        help="Directory for vLLM model cache (default: vLLM default)"
    )
    parser.add_argument(
        "--num-students", "-n",
        type=int,
        default=DEFAULT_NUM_STUDENTS,
        help=f"Number of students to sample (default: {DEFAULT_NUM_STUDENTS}, use 0 or -1 for all students)"
    )
    parser.add_argument(
        "--bin-size",
        type=int,
        default=DEFAULT_BIN_SIZE,
        help=f"Size of each prediction bin (default: {DEFAULT_BIN_SIZE})"
    )
    parser.add_argument(
        "--min-history",
        type=int,
        default=DEFAULT_MIN_HISTORY,
        help=f"Minimum history size before making predictions (default: {DEFAULT_MIN_HISTORY})"
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
        help="Maximum number of sequences to process in a batch (vLLM, default: 256)"
    )
    parser.add_argument(
        "--reasoning-level",
        type=str,
        choices=["none", "low", "medium", "high"],
        default=None,
        help="Reasoning level for GPT-OSS models only. Default: uses model config (medium for GPT-OSS, none for Qwen)"
    )
    parser.add_argument(
        "--max-model-len",
        type=int,
        default=None,
        help="Maximum sequence length in tokens (vLLM, default: model's context length)"
    )
    parser.add_argument(
        "--gpu-memory-utilization",
        type=float,
        default=0.9,
        help="Fraction of GPU memory to use (vLLM, default: 0.9, range: 0.0-1.0)"
    )
    parser.add_argument(
        "--legacy-clean",
        action="store_true",
        default=False,
        help="Use legacy text cleaner (cleantext.py) instead of clean_utils.py"
    )
    return parser.parse_args()


def label_answer_options(answer_string):
    """
    Convert pipe-delimited answers to lettered format.
    Input: "Han is correct || Elena is correct || Both are correct"
    Output: {"A": "Han is correct", "B": "Elena is correct", "C": "Both are correct"}
    """
    if pd.isna(answer_string) or answer_string == '':
        return None

    options = [opt.strip() for opt in answer_string.split('||')]
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    return {letters[i]: opt for i, opt in enumerate(options) if i < len(letters)}


def clean_html_and_normalize(text):
    """
    Remove HTML tags and normalize text for comparison.
    """
    if pd.isna(text):
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', str(text))
    # Normalize whitespace
    text = ' '.join(text.split())
    # Remove extra spaces around colons
    text = re.sub(r'\s*:\s*', ':', text)
    return text.strip()


def match_student_answer_to_letters(student_answer_text, answer_options_dict):
    """
    Match student's comma-delineated answers to letter options.

    Args:
        student_answer_text: String like "Answer A text , Answer C text , Answer B text"
        answer_options_dict: Dict like {"A": "Answer A text", "B": "Answer B text", ...}

    Returns:
        String like "A, B, C" or original text if no match
    """
    if pd.isna(student_answer_text) or not answer_options_dict:
        return student_answer_text

    # Split by " , " (comma with spaces, which is the delimiter used in the actual_answer)
    student_answers = [ans.strip() for ans in str(student_answer_text).split(' , ')]

    # Clean and normalize all options for comparison
    normalized_options = {
        letter: clean_html_and_normalize(text)
        for letter, text in answer_options_dict.items()
    }

    matched_letters = []
    for student_ans in student_answers:
        normalized_student = clean_html_and_normalize(student_ans)

        # Try to find exact match first
        for letter, normalized_option in normalized_options.items():
            if normalized_student == normalized_option:
                matched_letters.append(letter)
                break
        else:
            # If no exact match, try substring match (student answer contained in option or vice versa)
            for letter, normalized_option in normalized_options.items():
                if (normalized_student in normalized_option or
                    normalized_option in normalized_student):
                    matched_letters.append(letter)
                    break

    # Return comma-separated letters if we found matches, otherwise return original
    if matched_letters:
        return ', '.join(sorted(set(matched_letters)))  # Remove duplicates and sort
    return student_answer_text


def get_correct_option_letters(answer_options, correct_answers):
    """
    Determine which letter(s) correspond to correct answer(s).

    Args:
        answer_options: Dict like {"A": "Han is correct", "B": "Elena is correct", ...}
        correct_answers: String like "Both are correct" or "Han is correct || Elena is correct"

    Returns:
        String like "C" or "A, B" depending on how many correct options
    """
    if not answer_options or pd.isna(correct_answers):
        return correct_answers

    # Split correct answers if multiple
    correct_list = [ans.strip() for ans in correct_answers.split('||')]

    # Find matching letters
    correct_letters = []
    for letter, text in answer_options.items():
        if text in correct_list:
            correct_letters.append(letter)

    return ', '.join(sorted(correct_letters)) if correct_letters else correct_answers


def format_answer_options_for_prompt(answer_options):
    """
    Format answer options dictionary for display in prompt.
    Input: {"A": "Han is correct", "B": "Elena is correct", ...}
    Output: "A) Han is correct\nB) Elena is correct\n..."
    """
    if not answer_options:
        return None

    return '\n'.join([f"{letter}) {text}" for letter, text in answer_options.items()])


def create_user_prompt(student_history, new_problem, problem_df):
    """
    Creates a user prompt with student history and new problem.

    Args:
        student_history: List of dicts with keys: problem_id, timestamp, problem_text,
                        correct_answer, student_answer, used_hint, saw_answer
        new_problem: Dict with keys: problem_text, correct_answer, used_hint, saw_answer,
                     answer_options (optional)
    """
    prompt = "Task Description:\n\n"
    prompt += "Your task is to model a single student's learning process and predict how they will respond to a new mathematics problem based on their prior work.\n\n"

    prompt += """You will produce three coordinated predictions:

    1) **Skill-level knowledge tracing (0 or 1):** Predict whether this student has mastered the underlying skill involved in the new problem.
    2) **Question-level knowledge tracing (0 or 1):** Predict whether this student will answer this specific problem correctly.
    3) **Cognitive-level prediction (string):** Generate the exact answer the student would most likely produce.
       - For Multiple Choice (select 1): Predict a single letter (e.g., "A" or "B")
       - For Multiple Choice (select all): Predict comma-separated letters (e.g., "A, C" or "B, D")
       - For Fill-in problems: Predict the exact text the student would write
    """

    prompt += """---

    Provided Data:

    You will receive:
    - ProblemID: <id>
    - Timestamp: <timestamp>
    - Problem: <problem text>
    - Problem Type: Multiple Choice (select 1) / Multiple Choice (select all) / Fill-in Problem
    - Options: Answer choices in format "A) ...\nB) ...\nC) ..."
    - Correct Answer(s): The letter(s) or text of correct answer(s)
    - Student's First Answer: Letter(s) or fill-in text
    - UsedHint: <True/False>
    - SawAnswer: <True/False>
    - Skill: <skill_name_or_id>
    - A new problem (with optional answer choices), skill metadata, and context flags (`UsedHint`, `SawAnswer`).

    # About the context flags:
    - **UsedHint = True** → The student viewed or used a hint while solving this problem.
    - **SawAnswer = True** → The student saw the correct answer before or during the attempt.
    When either of these flags is True, treat the corresponding response as *less reliable evidence of mastery* — it indicates that the student has not fully learned the concept and required help solving the problem.
"""

    prompt += "**Student's Previous Problems:**\n\n"
    for item in student_history:
        prompt += f"Timestamp: {item['timestamp']}\n"
        prompt += f"Problem: {item['problem_text']}\n"
        prompt += f"Problem Type: {item['problem_type']}\n"
        if item.get('answer_options_formatted'):
            prompt += f"Options:\n{item['answer_options_formatted']}\n"
        prompt += f"Correct Answer: {item['correct_answer']}\n"
        prompt += f"Student's First Answer: {item['student_answer']}\n"
        prompt += f"UsedHint: {item['used_hint']}\n"
        prompt += f"SawAnswer: {item['saw_answer']}\n"
        if item.get('node_name'):
            prompt += f"Skill: {item['node_name']}\n"
        else:
            prompt += f"Skill: Undefined\n"
        prompt += "---\n\n"

    prompt += "**New Problem to Predict:**\n\n"
    prompt += f"Timestamp: {new_problem['timestamp']}\n"
    prompt += f"Problem: {new_problem['problem_text']}\n"
    prompt += f"Problem Type: {new_problem['problem_type']}\n"
    if new_problem.get('answer_options_formatted'):
        prompt += f"Answer Options:\n{new_problem['answer_options_formatted']}\n"
    prompt += f"Correct Answer: {new_problem['correct_answer']}\n"
    if new_problem.get('node_name'):
        prompt += f"Skill: {new_problem['node_name']}\n"
    else:
        prompt += f"Skill: Undefined\n"

    return prompt


def extract_json_prediction(response_text):
    """Extract the final JSON prediction from the model's response."""
    # Find all JSON objects in the response
    json_matches = re.findall(r'\{[\s\S]*?\}', response_text)

    if json_matches:
        # Take the last JSON object
        json_str = json_matches[-1]
        try:
            # Decode escape sequences (like \n) before parsing
            json_str = json_str.encode().decode('unicode_escape')
            json_str = json_str.strip()
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Attempted to parse:\n{json_str}")
        except Exception as e:
            print(f"Error processing JSON: {e}")
    return None


def get_prediction_id(meta):
    """Generate unique ID for a prediction"""
    return f"{meta['user_id']}_{meta['bin_number']}_{meta['prediction_type']}"


def load_completed_predictions(output_jsonl):
    """Load already-completed prediction IDs from JSONL file"""
    completed = set()
    if os.path.exists(output_jsonl):
        with open(output_jsonl, 'r') as f:
            for line in f:
                if line.strip():
                    result = json.loads(line)
                    completed.add(result['prediction_id'])
        print(f"Loaded {len(completed)} completed predictions from {output_jsonl}")
    return completed


def make_process_single_user(system_prompt):
    """Create a process_single_user function with the given system prompt."""
    def process_single_user(args):
        """Process a single user's data and return prompts and metadata."""
        user_id, user_records, min_history, bin_size = args

        prompts = []
        metadata = []

        # Check if user has at least min_history + 1 rows
        if len(user_records) < min_history + 1:
            return prompts, metadata

        num_bins = (len(user_records) - min_history) // bin_size

        # Build initial history
        student_history = []
        for hist_idx in range(min_history):
            row = user_records[hist_idx]
            student_history.append({
                'problem_id': row['problem_id'],
                'timestamp': row['end_time'],
                'problem_text': row['cleaned body'],
                'correct_answer': row['Fill-in Answers'],
                'answer_options': row['answer_options'] if pd.notna(row['answer_options']) else None,
                'answer_options_formatted': row['answer_options_formatted'] if pd.notna(row.get('answer_options_formatted')) else None,
                'student_answer': row['answer_text'],
                'used_hint': row['hint_count'] > 0,
                'saw_answer': row['saw_answer'],
                'problem_type': row['Problem Type'],
                'node_name': row.get('node_name')
            })

        for bin_idx in range(num_bins):
            # Extend history with previous bin's items
            if bin_idx > 0:
                prev_bin_start = min_history + ((bin_idx - 1) * bin_size)
                prev_bin_end = min_history + (bin_idx * bin_size)
                for hist_idx in range(prev_bin_start, prev_bin_end):
                    row = user_records[hist_idx]
                    student_history.append({
                        'problem_id': row['problem_id'],
                        'timestamp': row['end_time'],
                        'problem_text': row['cleaned body'],
                        'correct_answer': row['Fill-in Answers'],
                        'answer_options': row['answer_options'] if pd.notna(row['answer_options']) else None,
                        'answer_options_formatted': row['answer_options_formatted'] if pd.notna(row.get('answer_options_formatted')) else None,
                        'student_answer': row['answer_text'],
                        'used_hint': row['hint_count'] > 0,
                        'saw_answer': row['saw_answer'],
                        'problem_type': row['Problem Type'],
                        'node_name': row.get('node_name')
                    })

            history_end = min_history + (bin_idx * bin_size)
            bin_start = history_end
            bin_end = bin_start + bin_size
            current_bin = user_records[bin_start:bin_end]

            # Find first correct and first incorrect in this bin
            first_correct_idx = None
            first_incorrect_idx = None

            for idx, row in enumerate(current_bin):
                actual_idx = bin_start + idx
                score = row['discrete_score']

                if score == 1 and first_correct_idx is None:
                    first_correct_idx = actual_idx
                if score == 0 and first_incorrect_idx is None:
                    first_incorrect_idx = actual_idx

                if first_correct_idx is not None and first_incorrect_idx is not None:
                    break

            # Create predictions for found cases
            for target_idx, prediction_type in [
                (first_correct_idx, 'correct'),
                (first_incorrect_idx, 'incorrect')
            ]:
                if target_idx is None:
                    continue

                target_row = user_records[target_idx]
                new_problem = {
                    'problem_text': target_row['cleaned body'],
                    'correct_answer': target_row['Fill-in Answers'],
                    'answer_options': target_row['answer_options'] if pd.notna(target_row['answer_options']) else None,
                    'answer_options_formatted': target_row['answer_options_formatted'] if pd.notna(target_row.get('answer_options_formatted')) else None,
                    'problem_type': target_row['Problem Type'],
                    'timestamp': target_row['end_time'],
                    'node_name': target_row.get('node_name')
                }

                user_prompt = create_user_prompt(student_history, new_problem, None)
                full_prompt = system_prompt + "\n\n" + user_prompt

                prompts.append(full_prompt)
                metadata.append({
                    'prediction_id': f"{user_id}_{bin_idx}_{prediction_type}",
                    'row_index': target_idx,
                    'user_id': user_id,
                    'history_size': len(student_history),
                    'bin_number': bin_idx,
                    'prediction_type': prediction_type,
                    'id': target_row.get('id_x', None),
                    'problem_id': target_row.get('problem_id', None),
                    'problem_type': target_row['Problem Type'],
                    'actual_answer': target_row['answer_text'],
                    'correct_answer': target_row['Fill-in Answers'],
                    'actual_score': target_row['discrete_score'],
                    'prompt': full_prompt
                })

        return prompts, metadata

    return process_single_user


def append_results_jsonl(results, output_jsonl):
    """Append batch results to JSONL file"""
    with open(output_jsonl, 'a') as f:
        for result in results:
            f.write(json.dumps(result, cls=NumpyEncoder) + '\n')


def process_batch(batch_metadata, batch_response_texts):
    """Process a batch of responses and return results."""
    batch_results = []

    for metadata, response_text in zip(batch_metadata, batch_response_texts):
        # Extract prediction
        prediction = extract_json_prediction(response_text)

        if prediction:
            batch_results.append({
                **metadata,
                'predicted_skill_level': prediction.get('skill_level'),
                'predicted_question_level': prediction.get('question_level'),
                'predicted_student_answer': prediction.get('student_answer'),
                'full_response': response_text
            })
        else:
            batch_results.append({
                **metadata,
                'predicted_skill_level': None,
                'predicted_question_level': None,
                'predicted_student_answer': None,
                'full_response': response_text
            })

    return batch_results


# Global variable to hold process_single_user function for multiprocessing
_process_single_user_func = None


def _process_single_user_wrapper(args):
    """Wrapper for multiprocessing that uses the global function."""
    return _process_single_user_func(args)


def run_inference(config):
    """
    Main inference function that runs KT prediction with the given model config.

    Args:
        config: Dict with keys:
            - model_id: HuggingFace model ID
            - gen_configs: Dict of generation parameters
            - output_prefix: Prefix for output filename
            - system_prompt_prefix: Optional prefix for system prompt (e.g., "Reasoning: medium\n\n")
    """
    global _process_single_user_func

    model_id = config["model_id"]
    gen_configs = config["gen_configs"]
    output_prefix = config["output_prefix"]

    # Parse arguments first (needed for reasoning level)
    default_output_jsonl = f"{output_prefix}.jsonl"
    args = parse_args(default_output_jsonl)

    # Determine system prompt prefix
    # CLI --reasoning-level overrides model config if provided
    if args.reasoning_level is not None:
        if args.reasoning_level == "none":
            system_prompt_prefix = ""
        else:
            system_prompt_prefix = f"Reasoning: {args.reasoning_level}\n\n"
    else:
        system_prompt_prefix = config.get("system_prompt_prefix", "")

    # Build full system prompt
    system_prompt = system_prompt_prefix + BASE_SYSTEM_PROMPT

    # Create the process_single_user function with this system prompt
    _process_single_user_func = make_process_single_user(system_prompt)

    batch_size = args.batch_size
    data_dir = args.data_dir
    cache_dir = args.cache_dir
    num_students = args.num_students
    bin_size = args.bin_size
    min_history = args.min_history

    # Generate output filename with params
    n_str = "all" if num_students <= 0 else str(num_students)
    params_suffix = f"_n{n_str}_bin{bin_size}_hist{min_history}"

    if args.output:
        # Use explicit output path
        output_jsonl = args.output
    else:
        # Auto-generate filename in output directory
        filename = f"{output_prefix}{params_suffix}.jsonl"
        output_jsonl = os.path.join(args.output_dir, filename)

    # Build input file paths
    student_csv = os.path.join(data_dir, STUDENT_FILE)
    problems_csv = os.path.join(data_dir, PROBLEMS_FILE)
    skill_csv = os.path.join(data_dir, SKILL_FILE)

    print(f"Model: {model_id}")
    print(f"Data directory: {data_dir}")
    print(f"Batch size: {batch_size}")
    print(f"Output JSONL: {output_jsonl}")
    print(f"Num students: {num_students if num_students > 0 else 'all'}")
    print(f"Bin size: {bin_size}")
    print(f"Min history: {min_history}")
    if cache_dir:
        print(f"Model cache: {cache_dir}")
    print(f"Text cleaner: {'legacy (cleantext.py)' if args.legacy_clean else 'default (clean_utils.py)'}")

    # Load the data
    print("\nLoading data...")
    student_df = pd.read_csv(student_csv)
    student_df = student_df.sort_values(['user_id', 'id']).reset_index(drop=True)
    problems_df = pd.read_csv(problems_csv)
    clean_func = clean_text_legacy if args.legacy_clean else clean_problem_body
    problems_df['cleaned body'] = problems_df['Problem Body'].apply(clean_func)

    # Label answer options for multiple-choice items
    problems_df['answer_options'] = problems_df['Multiple Choice Options'].apply(label_answer_options)

    # Get correct answer letters for multiple-choice, keep original for fill-in
    problems_df['correct_answers'] = problems_df.apply(
        lambda row: get_correct_option_letters(row['answer_options'], row['Multiple Choice Answers'])
        if row['Problem Type'] in ['Multiple Choice (select 1)', 'Multiple Choice (select all)']
        else row['Fill-in Answers'],
        axis=1
    )

    skill_df = pd.read_csv(skill_csv)
    problems_df = pd.merge(problems_df, skill_df, on='problem_id', how='left')

    # Pre-compute formatted answer options once per problem
    problems_df['answer_options_formatted'] = problems_df['answer_options'].apply(
        lambda x: format_answer_options_for_prompt(x) if pd.notna(x) else None
    )

    # Sort student data by id (chronological order)
    student_df = student_df.sort_values('id').reset_index(drop=True)

    # Merge with problems data
    merged_df = student_df.merge(problems_df, on='problem_id', how='inner')

    # Convert student answers to letter format for multiple-choice problems
    merged_df['answer_text'] = merged_df.apply(
        lambda row: match_student_answer_to_letters(row['answer_text'], row['answer_options'])
        if row['Problem Type'] in ['Multiple Choice (select 1)', 'Multiple Choice (select all)'] and pd.notna(row['answer_options'])
        else row['answer_text'],
        axis=1
    )

    # Select users (all or random sample)
    all_users = merged_df['user_id'].unique()
    if num_students <= 0:
        # Use all students
        selected_users = all_users
        print(f"\nUsing all {len(all_users)} users")
    else:
        # Random sample
        np.random.seed(42)  # For reproducibility
        selected_users = np.random.choice(all_users, size=min(num_students, len(all_users)), replace=False)
        merged_df = merged_df[merged_df['user_id'].isin(selected_users)]
        print(f"\nSelected {len(selected_users)} random users from {len(all_users)} total users")
    print(f"Filtered data: {len(merged_df)} rows")

    # Prepare data for batch processing
    print("\nPreparing prompts in parallel...")

    # Prepare user groups for parallel processing
    print("Grouping user data...")
    user_groups = [
        (user_id, user_df.to_dict('records'), min_history, bin_size)
        for user_id, user_df in merged_df.groupby('user_id')
    ]
    print(f"Processing {len(user_groups)} users with {cpu_count()} CPU cores...")

    # Process users in parallel
    all_prompts = []
    all_metadata = []

    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(
            pool.imap(_process_single_user_wrapper, user_groups),
            total=len(user_groups),
            desc="Preparing prompts"
        ))

    # Merge results
    for prompts, metadata in results:
        all_prompts.extend(prompts)
        all_metadata.extend(metadata)

    print(f"\nTotal predictions to make: {len(all_prompts)}")

    # Filter out already-completed predictions (resume support)
    completed_ids = load_completed_predictions(output_jsonl)
    remaining = [(p, m) for p, m in zip(all_prompts, all_metadata)
                 if m['prediction_id'] not in completed_ids]

    if not remaining:
        print("All predictions already completed!")
        return

    all_prompts, all_metadata = zip(*remaining)
    all_prompts = list(all_prompts)
    all_metadata = list(all_metadata)

    print(f"Already completed: {len(completed_ids)}")
    print(f"Remaining to process: {len(all_prompts)}")
    print(f"Processing in batches of {batch_size}")

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
    if cache_dir:
        llm_kwargs["download_dir"] = cache_dir
    llm = LLM(**llm_kwargs)

    # Process in batches
    results = []
    num_batches = (len(all_prompts) + batch_size - 1) // batch_size

    for batch_idx in range(num_batches):
        batch_start = batch_idx * batch_size
        batch_end = min(batch_start + batch_size, len(all_prompts))

        batch_prompts = all_prompts[batch_start:batch_end]
        batch_metadata = all_metadata[batch_start:batch_end]

        print(f"\n{'='*80}")
        print(f"Processing batch {batch_idx + 1}/{num_batches}")
        print(f"Items: {batch_start} to {batch_end} ({len(batch_prompts)} prompts)")
        print(f"{'='*80}")

        # Generate predictions for this batch
        try:
            outputs = llm.generate(batch_prompts, sampling_params)
            response_texts = [o.outputs[0].text.strip() for o in outputs]

            # Process results for this batch
            batch_results = process_batch(batch_metadata, response_texts)
            results.extend(batch_results)

            print(f"Successfully processed batch {batch_idx + 1}")
            print(f"Total results so far: {len(results)}")

            # Append results immediately after each batch
            append_results_jsonl(batch_results, output_jsonl)
            print(f"Saved {len(batch_results)} results to {output_jsonl}")

        except Exception as e:
            print(f"\nERROR processing batch {batch_idx + 1}: {str(e)}")
            print(f"Progress saved in {output_jsonl} - restart to resume")
            raise

    print(f"\n{'='*80}")
    print("All batches processed successfully!")
    print(f"{'='*80}")
    print(f"\nAll results saved to {output_jsonl}")
    print(f"Total predictions processed: {len(results)}")

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
    exit(0)
