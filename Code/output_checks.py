"""
Output format enforcement and checks for the mathematical practice LLM output.

Used by augment_mathematical_practice.py and augment_mathematical_practice_test5.py.

Enforcement during generation (structured_output_kwargs):
    vLLM's structured outputs constrain decoding to practice_json_schema: a JSON object with
    "reasoning" (non-empty string) followed by the six practice keys, each a number from 0 to 1,
    with no other keys and no text outside the object. A response can still be cut off by
    max_tokens, which check_response reports as "truncated".

Checks after generation (a backstop, and the only checks when structured output is off):
1. check_response: one model response.
   - Errors make the response unusable: the script retries it once, and leaves the row
     empty if the retry also fails. Nothing is silently fixed (no clipping, no rescaling).
   - Warnings keep the scores but are recorded and reported at the end of the run.
2. check_output_frame: the table about to be written. Any problem raises ValueError,
   so a malformed CSV is never written.

Error codes:
    truncated       response hit the max_tokens limit before finishing
    no_json         no JSON object with practice keys was found
    missing_keys    one or more practice keys are missing
    not_a_number    a practice value is not a number (e.g. "high", null, true)
    not_finite      a practice value is NaN or infinite
    out_of_range    a practice value is below 0 or above 1 (e.g. 80 instead of 0.8)

Warning codes:
    extra_text        text before or after the JSON object (e.g. markdown code fences)
    extra_keys        keys other than the six practices and "reasoning"
    empty_reasoning   "reasoning" is missing or empty
    number_as_string  a value was given as a string, e.g. "0.8"
    all_zero          every practice scored 0
    tied_top_score    two or more practices share the highest score
"""

import json
import re

import numpy as np

REASONING_KEY = 'reasoning'


def practice_json_schema(practice_keys):
    """
    JSON schema for one response: "reasoning" first (so the model explains before scoring),
    then each practice key as a number from 0 to 1. No other keys are allowed.
    """
    properties = {REASONING_KEY: {"type": "string", "minLength": 1}}
    for key in practice_keys:
        properties[key] = {"type": "number", "minimum": 0, "maximum": 1}
    return {
        "type": "object",
        "properties": properties,
        "required": [REASONING_KEY, *practice_keys],
        "additionalProperties": False,
    }


def structured_output_kwargs(practice_keys):
    """
    Keyword arguments for vllm.SamplingParams that force every response to match
    practice_json_schema during generation.

    Newer vLLM uses structured_outputs=StructuredOutputsParams(json=...); older versions
    (0.10.x and earlier) use guided_decoding=GuidedDecodingParams(json=...).
    vLLM is imported here, not at module level, so the checks below work without vLLM.
    """
    schema = practice_json_schema(practice_keys)
    try:
        from vllm.sampling_params import StructuredOutputsParams
        return {"structured_outputs": StructuredOutputsParams(json=schema)}
    except ImportError:
        from vllm.sampling_params import GuidedDecodingParams
        return {"guided_decoding": GuidedDecodingParams(json=schema)}


def _find_json_object(text, practice_keys):
    """
    Return (obj, start, end) for the last JSON object in text that contains at least one
    practice key, or (None, None, None) if there is none.
    """
    decoder = json.JSONDecoder()
    for match in reversed(list(re.finditer(r'\{', text))):
        try:
            obj, end = decoder.raw_decode(text, match.start())
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and any(key in obj for key in practice_keys):
            return obj, match.start(), end
    return None, None, None


def check_response(text, finish_reason, practice_keys):
    """
    Check one model response against the expected output format.

    Args:
        text: the response text
        finish_reason: vLLM's finish reason for the response ('stop', 'length', ...)
        practice_keys: the JSON keys of the practices, in output order

    Returns a dict:
        scores:    list of floats in practice_keys order, or None if there is any error
        reasoning: the reasoning string ('' if missing)
        errors:    list of 'code: detail' strings that make the response unusable
        warnings:  list of 'code: detail' strings that are reported but keep the scores
    """
    errors, warnings = [], []
    if finish_reason == 'length':
        errors.append('truncated: response hit the max_tokens limit before finishing')

    obj, start, end = _find_json_object(text, practice_keys)
    if obj is None:
        errors.append('no_json: no JSON object with practice keys found')
        return {'scores': None, 'reasoning': '', 'errors': errors, 'warnings': warnings}

    if text[:start].strip() or text[end:].strip():
        warnings.append('extra_text: text before or after the JSON object')

    missing = [key for key in practice_keys if key not in obj]
    extra = sorted(set(obj) - set(practice_keys) - {REASONING_KEY})
    if missing:
        errors.append(f"missing_keys: {missing}")
    if extra:
        warnings.append(f"extra_keys: {extra}")

    reasoning = obj.get(REASONING_KEY)
    if not isinstance(reasoning, str) or not reasoning.strip():
        warnings.append('empty_reasoning: "reasoning" is missing or empty')
        reasoning = reasoning if isinstance(reasoning, str) else ''

    scores = []
    for key in [key for key in practice_keys if key in obj]:
        value = obj[key]
        if isinstance(value, str):
            try:
                number = float(value)
            except ValueError:
                errors.append(f"not_a_number: {key} = {value!r}")
                continue
            warnings.append(f"number_as_string: {key} = {value!r}")
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            number = float(value)
        else:
            errors.append(f"not_a_number: {key} = {value!r}")
            continue
        if not np.isfinite(number):
            errors.append(f"not_finite: {key} = {value!r}")
        elif not 0.0 <= number <= 1.0:
            errors.append(f"out_of_range: {key} = {number:g} (must be 0 to 1)")
        else:
            scores.append(number)

    if errors:
        return {'scores': None, 'reasoning': reasoning, 'errors': errors, 'warnings': warnings}

    top = max(scores)
    if top == 0:
        warnings.append('all_zero: every practice scored 0')
    elif scores.count(top) > 1:
        tied = [key for key, score in zip(practice_keys, scores) if score == top]
        warnings.append(f"tied_top_score: {tied} all scored {top:g}")
    return {'scores': scores, 'reasoning': reasoning, 'errors': errors, 'warnings': warnings}


def check_output_frame(original_df, output_df, score_column, practice_names, predicted_column=None):
    """
    Check the table before it is written to disk.

    Raises ValueError listing the problems if:
    - the row count or row order changed, or any original column (other than score_column
      and predicted_column) is missing, moved, or has a changed value;
    - a score cell is neither empty nor a JSON list of len(practice_names) numbers from 0 to 1;
    - predicted_column (if given) is not the name of the highest score in its row, or is
      filled in a row that has no scores.
    """
    problems = []
    skip = {score_column, predicted_column}

    if len(output_df) != len(original_df):
        problems.append(f"row count changed: {len(original_df)} -> {len(output_df)}")
    elif not output_df.index.equals(original_df.index):
        problems.append("row order or index changed")
    else:
        kept = [column for column in output_df.columns if column in original_df.columns]
        if kept != list(original_df.columns):
            problems.append("original columns are missing or in a different order")
        for column in original_df.columns:
            if column in skip or column not in output_df.columns:
                continue
            changed = output_df[column] != original_df[column]
            if changed.any():
                problems.append(f"column {column!r} changed in {int(changed.sum())} rows")

    for idx, cell in output_df[score_column].items():
        predicted = output_df.at[idx, predicted_column] if predicted_column else None
        if not isinstance(cell, str):
            problems.append(f"row {idx}: {score_column} is not text: {cell!r}")
            continue
        if not cell.strip():
            if predicted:
                problems.append(f"row {idx}: {predicted_column} is {predicted!r} but there are no scores")
            continue
        try:
            scores = json.loads(cell)
        except json.JSONDecodeError:
            problems.append(f"row {idx}: {score_column} is not valid JSON: {cell[:60]!r}")
            continue
        valid = (
            isinstance(scores, list)
            and len(scores) == len(practice_names)
            and all(isinstance(s, (int, float)) and not isinstance(s, bool) and 0 <= s <= 1
                    for s in scores)
        )
        if not valid:
            problems.append(f"row {idx}: {score_column} is not a list of {len(practice_names)} "
                            f"numbers from 0 to 1: {cell[:60]!r}")
            continue
        if predicted_column:
            expected = practice_names[int(np.argmax(scores))]
            if predicted != expected:
                problems.append(f"row {idx}: {predicted_column} is {predicted!r}, "
                                f"but the highest score is {expected!r}")

    if problems:
        shown = '\n  '.join(problems[:10])
        more = f"\n  ... and {len(problems) - 10} more" if len(problems) > 10 else ''
        raise ValueError(f"Output failed the format checks, so nothing was written:\n  {shown}{more}")


def print_format_report(records):
    """
    Print how many responses had each kind of format error or warning, with their problem ids.

    Each record needs 'problem_id', 'format_errors', and 'format_warnings', where the last two
    are lists with one list of issue strings per response (including retries).
    """
    by_code = {}
    responses = 0
    for record in records:
        responses += len(record['format_errors'])
        for kind in ('format_errors', 'format_warnings'):
            for response_issues in record[kind]:
                for issue in response_issues:
                    code = issue.split(':', 1)[0]
                    by_code.setdefault((kind, code), []).append(record['problem_id'])

    print(f"\nFormat check report ({len(records)} items, {responses} responses including retries)")
    if not by_code:
        print("  All responses passed every format check.")
        return
    for (kind, code), problem_ids in sorted(by_code.items()):
        label = 'ERROR  ' if kind == 'format_errors' else 'warning'
        unique = list(dict.fromkeys(problem_ids))
        shown = ', '.join(unique[:10])
        if len(unique) > 10:
            shown += f", ... ({len(unique) - 10} more)"
        print(f"  {label} {code:<17} {len(problem_ids):>5} responses   problem_ids: {shown}")
    print("  Errors reject a response (it is retried once); warnings keep its scores.")
    print("  Details for each response are in the raw JSONL (format_errors, format_warnings).")
