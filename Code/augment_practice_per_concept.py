"""
Per-skill practice scores for problems that have two or more skills.

augment_mathematical_practice.py rates each problem once on the six practices. When a problem has
several skills (distinct node_codes in Skills.csv), that one score vector cannot say which practices
go with which skill. This script runs the same zero-shot prompt once per skill of those problems:
the system prompt (SYSTEM_PROMPT) is unchanged, and the item prompt names the skill to rate and the
item's other skills. The six scores per skill are written to Problems.csv as

    concept_practice: JSON object {"<node_code>": [6 scores], ...}, in the order of the problem's
                      skills; the scores are in the order of PRACTICE_NAMES in
                      augment_mathematical_practice.py. Empty for problems with one skill, which
                      use mathematical_practice.

maca_cd_practice (practice_q = practice_per_concept) normalizes each skill's scores to sum to 1.

Rows that share a problem_id get the same value. A rerun labels only the skills that are still
missing (--overwrite relabels every multi-skill problem). Raw model responses are appended to
concept_practice_raw.jsonl in --output-dir. Before the first update, Problems.csv is backed up to
Problems.csv.bak (if no backup exists yet).

Run from the Code/ directory (it imports augment_mathematical_practice).

Usage:
    VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=0 python3 augment_practice_per_concept.py \
        --data-dir ../Data --output-dir ../Data --dry-run --limit 5
    VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=0 python3 augment_practice_per_concept.py \
        --data-dir ../Data --output-dir ../Data
"""

import argparse
import contextlib
import gc
import json
import os
import shutil

import pandas as pd
import torch
from vllm import LLM, SamplingParams
from vllm.distributed.parallel_state import (
    destroy_model_parallel,
    destroy_distributed_environment,
)

from add_practice_multi_hot import MULTI_HOT_COLUMN
from augment_mathematical_practice import (
    DEFAULT_BATCH_SIZE,
    DEFAULT_MAX_MODEL_LEN,
    DEFAULT_MODEL_ID,
    GREEDY_SAMPLING,
    MAX_NEW_TOKENS,
    OUTPUT_COLUMN,
    PRACTICE_KEYS,
    PRACTICE_NAMES,
    PREDICTED_COLUMN,
    PROBLEMS_FILE,
    SKILL_FILE,
    STOCHASTIC_SAMPLING,
    SYSTEM_PROMPT,
    append_results_jsonl,
    format_choices_and_answer,
    mark_answer_blanks,
    save_problems_csv,
    score_request_output,
)
from clean_utils import clean_problem_body
from output_checks import check_output_frame, print_format_report, structured_output_kwargs

CONCEPT_PRACTICE_COLUMN = "concept_practice"
RAW_OUTPUT_FILE = "concept_practice_raw.jsonl"
DEFAULT_DRY_RUN_LIMIT = 5


def parse_args():
    parser = argparse.ArgumentParser(
        description="Add per-skill practice scores (concept_practice) to Problems.csv for multi-skill problems"
    )
    parser.add_argument("--data-dir", "-d", type=str, default=".",
                        help="Directory containing Problems.csv and Skills.csv (default: current directory)")
    parser.add_argument("--output-dir", type=str, default=".",
                        help=f"Directory for {RAW_OUTPUT_FILE} (default: current directory)")
    parser.add_argument("--model-id", type=str, default=DEFAULT_MODEL_ID,
                        help=f"HuggingFace model ID (default: {DEFAULT_MODEL_ID})")
    parser.add_argument("--cache-dir", "-c", type=str, default=None,
                        help="Directory for vLLM model cache (default: vLLM default)")
    parser.add_argument("--num-gpus", type=int, default=1,
                        help="Number of GPUs for tensor parallelism (default: 1)")
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.9,
                        help="Fraction of GPU memory to use (vLLM, default: 0.9)")
    parser.add_argument("--max-model-len", type=int, default=DEFAULT_MAX_MODEL_LEN,
                        help=f"Maximum sequence length in tokens (vLLM, default: {DEFAULT_MAX_MODEL_LEN})")
    parser.add_argument("--batch-size", "-b", type=int, default=DEFAULT_BATCH_SIZE,
                        help=f"Prompts per batch; Problems.csv is saved after each batch (default: {DEFAULT_BATCH_SIZE})")
    parser.add_argument("--no-structured-output", action="store_true", default=False,
                        help="Do not constrain generation to the JSON schema; rely only on the format checks")
    parser.add_argument("--limit", type=int, default=None,
                        help=f"Only label the first N multi-skill problems that need labels "
                             f"(default: all; {DEFAULT_DRY_RUN_LIMIT} with --dry-run)")
    parser.add_argument("--overwrite", action="store_true", default=False,
                        help="Relabel every multi-skill problem, not only missing skills")
    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="Print prompts and scores without writing Problems.csv or the raw JSONL")
    args = parser.parse_args()
    if args.dry_run and args.limit is None:
        args.limit = DEFAULT_DRY_RUN_LIMIT
    return args


def load_problem_concepts(skills_csv):
    """Map problem_id to its distinct skills [(node_code, node_name), ...], in Skills.csv order.
    Several skill_ids share one node_code and name, so a skill is a node_code (as in maca_cd)."""
    skill_df = pd.read_csv(skills_csv, dtype=str, keep_default_na=False)
    concepts = {}
    for problem_id, code, name in zip(skill_df['problem_id'], skill_df['node_code'], skill_df['node_name']):
        problem_id, code, name = problem_id.strip(), code.strip(), name.strip()
        if not code:
            continue
        problem_concepts = concepts.setdefault(problem_id, [])
        if code not in [c for c, _ in problem_concepts]:
            problem_concepts.append((code, name))
    return concepts


def concept_label(concept):
    code, name = concept
    return f"{name} ({code})"


def create_concept_prompt(row, concept, other_concepts):
    """The item prompt of augment_mathematical_practice.create_user_prompt, rating one skill."""
    choices, correct = format_choices_and_answer(row)

    prompt = "Item to rate:\n\n"
    prompt += f"Problem Type: {row['Problem Type']}\n"
    prompt += f"Answer Type: {row['Answer Types']}\n"
    prompt += f"Skill to rate: {concept_label(concept)}\n"
    prompt += f"Other skills in this item: {'; '.join(concept_label(c) for c in other_concepts)}\n\n"
    prompt += f"Problem:\n{clean_problem_body(mark_answer_blanks(row['Problem Body']))}\n\n"
    if choices:
        prompt += f"Answer Choices:\n{choices}\n\n"
    prompt += f"Correct Answer:\n{correct or 'Not available'}\n\n"
    prompt += (f'Rate the six practices for how the student uses the skill "{concept[1]}" in answering '
               f'this item. Respond with only the JSON object described in the instructions.')
    return prompt


def parse_concept_practice(cell):
    """concept_practice cell -> {node_code: [6 floats]} (empty or malformed cell -> {})."""
    try:
        value = json.loads(cell)
    except (TypeError, ValueError):
        return {}
    if not isinstance(value, dict):
        return {}
    parsed = {}
    for code, scores in value.items():
        if (isinstance(scores, list) and len(scores) == len(PRACTICE_NAMES)
                and all(isinstance(s, (int, float)) and not isinstance(s, bool) and 0 <= s <= 1 for s in scores)):
            parsed[code] = [float(s) for s in scores]
    return parsed


def check_concept_practice_column(problems_df, problem_concepts):
    """Refuse to save a concept_practice cell that is not {node_code of the problem: [6 numbers in 0..1]}."""
    problems = []
    for idx, (problem_id, cell) in enumerate(zip(problems_df['problem_id'], problems_df[CONCEPT_PRACTICE_COLUMN])):
        if not cell.strip():
            continue
        try:
            value = json.loads(cell)
        except ValueError:
            problems.append(f"row {idx}: not valid JSON")
            continue
        codes = [code for code, _ in problem_concepts.get(problem_id.strip(), [])]
        if not isinstance(value, dict) or set(value) - set(codes) or len(parse_concept_practice(cell)) != len(value):
            problems.append(f"row {idx} (problem {problem_id}): malformed {CONCEPT_PRACTICE_COLUMN}: {cell[:80]}")
    if problems:
        shown = '\n  '.join(problems[:10])
        raise ValueError(f"{CONCEPT_PRACTICE_COLUMN} failed the format checks, so nothing was written:\n  {shown}")


def highest_practice(scores):
    return PRACTICE_NAMES[max(range(len(scores)), key=lambda i: scores[i])]


def print_concept_summary(problems_df, problem_concepts, targets):
    """How many multi-skill problems are complete, and how often their skills disagree on the
    highest-scored practice (if they always agreed, per-skill prompting would add little)."""
    complete, differ_between, differ_item = 0, 0, 0
    for problem_id, first_idx in targets.items():
        codes = [code for code, _ in problem_concepts[problem_id]]
        labels = parse_concept_practice(problems_df.at[first_idx, CONCEPT_PRACTICE_COLUMN])
        if not all(code in labels for code in codes):
            continue
        complete += 1
        highest = {highest_practice(labels[code]) for code in codes}
        if len(highest) > 1:
            differ_between += 1
        item_primary = problems_df.at[first_idx, PREDICTED_COLUMN] if PREDICTED_COLUMN in problems_df.columns else ''
        if item_primary and any(h != item_primary for h in highest):
            differ_item += 1
    print(f"\n{'='*80}")
    print(f"{CONCEPT_PRACTICE_COLUMN}: {complete} of {len(targets)} multi-skill problems have scores for every skill")
    if complete:
        print(f"  skills of the same problem with different highest-scored practices: {differ_between} "
              f"({differ_between / complete:.1%})")
        print(f"  problems where some skill's highest-scored practice differs from the item's "
              f"predicted_practice: {differ_item} ({differ_item / complete:.1%})")


def main():
    args = parse_args()

    problems_csv = os.path.join(args.data_dir, PROBLEMS_FILE)
    skill_csv = os.path.join(args.data_dir, SKILL_FILE)
    output_jsonl = os.path.join(args.output_dir, RAW_OUTPUT_FILE)

    print(f"Model: {args.model_id}")
    print(f"Problems file: {problems_csv}")
    print(f"Raw output JSONL: {output_jsonl}")
    print(f"Structured output: {'off (format checks only)' if args.no_structured_output else 'on (JSON schema enforced during generation)'}")
    if args.dry_run:
        print("DRY RUN: nothing will be written")

    # Read every cell as text so the original columns are written back unchanged.
    # original_df is kept untouched so check_output_frame can verify that before each save.
    original_df = pd.read_csv(problems_csv, dtype=str, keep_default_na=False)
    if OUTPUT_COLUMN not in original_df.columns:
        raise SystemExit(f"{problems_csv} has no {OUTPUT_COLUMN} column; run augment_mathematical_practice.py first")
    problems_df = original_df.copy()
    if CONCEPT_PRACTICE_COLUMN not in problems_df.columns:
        after = MULTI_HOT_COLUMN if MULTI_HOT_COLUMN in problems_df.columns else OUTPUT_COLUMN
        problems_df.insert(problems_df.columns.get_loc(after) + 1, CONCEPT_PRACTICE_COLUMN, '')
    problem_concepts = load_problem_concepts(skill_csv)

    # Multi-skill problems: problem_id -> rows with that id (duplicate problem_ids share a value)
    rows_by_problem = {}
    for idx, problem_id in zip(problems_df.index, problems_df['problem_id']):
        problem_id = problem_id.strip()
        if len(problem_concepts.get(problem_id, [])) >= 2:
            rows_by_problem.setdefault(problem_id, []).append(idx)
    targets = {problem_id: rows[0] for problem_id, rows in rows_by_problem.items()}
    by_size = {}
    for problem_id in targets:
        size = len(problem_concepts[problem_id])
        by_size[size] = by_size.get(size, 0) + 1
    print(f"\nProblems: {len(problems_df)} rows; multi-skill problems: {len(targets)} "
          f"({', '.join(f'{n} with {size} skills' for size, n in sorted(by_size.items()))})")

    # Skills still to label (all skills of every multi-skill problem with --overwrite)
    todo_problems = []
    for problem_id, first_idx in targets.items():
        existing = {} if args.overwrite else parse_concept_practice(problems_df.at[first_idx, CONCEPT_PRACTICE_COLUMN])
        missing = [concept for concept in problem_concepts[problem_id] if concept[0] not in existing]
        if missing:
            todo_problems.append((problem_id, missing))
    if args.limit is not None:
        todo_problems = todo_problems[:args.limit]
    if args.overwrite:
        # Clear the old scores of the problems being relabeled, so a skill that fails now is
        # left empty (and retried on the next run) instead of keeping an old value
        for problem_id, _ in todo_problems:
            for row_idx in rows_by_problem[problem_id]:
                problems_df.at[row_idx, CONCEPT_PRACTICE_COLUMN] = ''
    requests = []  # (problem_id, concept, user prompt)
    for problem_id, missing in todo_problems:
        row = problems_df.loc[targets[problem_id]]
        for concept in missing:
            others = [c for c in problem_concepts[problem_id] if c != concept]
            requests.append((problem_id, concept, create_concept_prompt(row, concept, others)))
    print(f"Problems needing per-skill scores: {len(todo_problems)} ({len(requests)} prompts)")
    if not requests:
        print("Nothing to label.")
        print_concept_summary(problems_df, problem_concepts, targets)
        return
    print(f"\nExample user prompt (problem_id {requests[0][0]}, skill {requests[0][1][0]}):\n")
    print(requests[0][2])

    # Initialize vLLM engine (as in augment_mathematical_practice.py)
    print("\nInitializing vLLM engine...")
    llm_kwargs = {
        "model": args.model_id,
        "tensor_parallel_size": args.num_gpus,
        "trust_remote_code": True,
        "gpu_memory_utilization": args.gpu_memory_utilization,
        "enable_prefix_caching": True,
        "max_model_len": args.max_model_len,
    }
    if args.cache_dir:
        llm_kwargs["download_dir"] = args.cache_dir
    llm = LLM(**llm_kwargs)

    # Skip prompts that would not fit in the context window instead of crashing the batch
    tokenizer = llm.get_tokenizer()
    system_tokens = len(tokenizer.encode(SYSTEM_PROMPT))
    chat_template_overhead = 32
    prompt_budget = args.max_model_len - MAX_NEW_TOKENS
    prompt_tokens = [system_tokens + len(tokenizer.encode(prompt)) + chat_template_overhead
                     for _, _, prompt in requests]
    sendable = [i for i, tokens in enumerate(prompt_tokens) if tokens <= prompt_budget]
    too_long = [i for i, tokens in enumerate(prompt_tokens) if tokens > prompt_budget]
    print(f"System prompt: {system_tokens} tokens; longest full prompt: {max(prompt_tokens)} tokens; "
          f"budget: {prompt_budget}")
    if too_long:
        print(f"WARNING: skipping {len(too_long)} prompts over budget (raise --max-model-len to include them): "
              f"{[f'{requests[i][0]}:{requests[i][1][0]}' for i in too_long]}")

    # Greedy decoding constrained to the JSON schema; failed responses are retried once with sampling
    schema_constraint = ({} if args.no_structured_output
                         else structured_output_kwargs(PRACTICE_KEYS, PRACTICE_NAMES))
    sampling_params = SamplingParams(n=1, **GREEDY_SAMPLING, **schema_constraint)
    retry_params = SamplingParams(n=1, **STOCHASTIC_SAMPLING, **schema_constraint)

    if not args.dry_run:
        backup_csv = problems_csv + '.bak'
        if not os.path.exists(backup_csv):
            shutil.copy2(problems_csv, backup_csv)
            print(f"Backed up original to {backup_csv}")

    labeled, failed = 0, 0
    all_records = []
    num_batches = (len(sendable) + args.batch_size - 1) // args.batch_size
    for batch_idx in range(num_batches):
        batch = sendable[batch_idx * args.batch_size:(batch_idx + 1) * args.batch_size]
        conversations = [
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": requests[i][2]},
            ]
            for i in batch
        ]
        print(f"\n{'='*80}")
        print(f"Processing batch {batch_idx + 1}/{num_batches} ({len(batch)} prompts)")
        print(f"{'='*80}")

        outputs = llm.chat(conversations, sampling_params, use_tqdm=True)
        results = [score_request_output(output) for output in outputs]
        retry_positions = [pos for pos, result in enumerate(results) if result['scores'] is None]
        if retry_positions:
            print(f"Retrying {len(retry_positions)} responses that failed the format checks...")
            retry_outputs = llm.chat([conversations[pos] for pos in retry_positions], retry_params, use_tqdm=False)
            for pos, output in zip(retry_positions, retry_outputs):
                retried = score_request_output(output)
                for key in ('responses', 'format_errors', 'format_warnings'):
                    retried[key] = results[pos][key] + retried[key]
                retried['retried'] = True
                results[pos] = retried

        records = []
        for i, result in zip(batch, results):
            problem_id, concept, prompt = requests[i]
            if result['scores'] is not None:
                rows = rows_by_problem[problem_id]
                labels = parse_concept_practice(problems_df.at[rows[0], CONCEPT_PRACTICE_COLUMN])
                labels[concept[0]] = result['scores']
                # Keep the problem's skill order
                ordered = {code: labels[code] for code, _ in problem_concepts[problem_id] if code in labels}
                for row_idx in rows:
                    problems_df.at[row_idx, CONCEPT_PRACTICE_COLUMN] = json.dumps(ordered)
                labeled += 1
            else:
                failed += 1
            records.append({
                'problem_id': f"{problem_id}:{concept[0]}",
                'node_code': concept[0],
                'node_name': concept[1],
                'scores': result['scores'],
                'primary_practice': result['primary'],
                'retried': result['retried'],
                'format_errors': result['format_errors'],
                'format_warnings': result['format_warnings'],
                'reasoning': result['reasoning'],
                'responses': result['responses'],
                'user_prompt': prompt,
                'model_id': args.model_id,
            })
        all_records.extend(records)

        # Refuse to save if any other column changed or a concept_practice cell is malformed
        check_concept_practice_column(problems_df, problem_concepts)
        check_output_frame(original_df, problems_df, OUTPUT_COLUMN, PRACTICE_NAMES,
                           predicted_column=PREDICTED_COLUMN,
                           derived_columns=[MULTI_HOT_COLUMN, CONCEPT_PRACTICE_COLUMN])

        if args.dry_run:
            for record in records:
                print(f"\nproblem {record['problem_id']}  skill: {record['node_name']}")
                if record['scores'] is None:
                    print(f"  FAILED FORMAT CHECKS: {record['format_errors']}")
                    print("  Last raw response:")
                    print(record['responses'][-1])
                    continue
                for name, score in zip(PRACTICE_NAMES, record['scores']):
                    print(f"  {name:<30} {score:.2f}")
                print(f"  Primary practice: {record['primary_practice']}")
                print(f"  Reasoning: {record['reasoning'][0]}")
        else:
            save_problems_csv(problems_df, problems_csv)
            append_results_jsonl(records, output_jsonl)
            print(f"Saved {len(records)} results to {problems_csv} and {output_jsonl}")

    print(f"\n{'='*80}")
    print(f"Labeled: {labeled} skills, failed format checks: {failed}, skipped (too long): {len(too_long)}")
    if failed or too_long:
        print("Re-run the script to retry the skills that are still missing.")
    print_format_report(all_records)
    print_concept_summary(problems_df, problem_concepts, targets)
    if args.dry_run:
        print("(dry run: summary includes unsaved scores)")

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


if __name__ == "__main__":
    main()
