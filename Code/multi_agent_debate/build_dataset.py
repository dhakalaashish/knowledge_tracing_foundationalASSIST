"""
Build the pairwise debate dataset for the multi-agent debate from problems_naep.csv.

Mapping to the debate setup of Khan et al. (2024), which debates reading-comprehension questions
about a story:
    story     -> the practice framework (definition and descriptors of the six practices, the
                 same text as in augment_mathematical_practice_test5.py) followed by the item.
                 Debaters and critics read it; the judge does not. Quotes are verified against it.
    question  -> "Which mathematical practice does this item mainly assess?"
    item      -> the item text, formatted as in the single-prompt evaluation. Every agent,
                 including the judge, sees it.
    answers   -> two practice names. The paper has two answers per question; with six practices,
                 every pair of practices is debated: 15 rows per item. core/debate.py runs each row
                 twice (answer order swapped), so each item gets 30 debates and each practice 10.

The columns "correct answer" and "negative answer" are the original code's names for the two
debate slots; here they only mean "practice 1" and "practice 2". ground_truth is never written
to the output.

Run from Code/ (it imports augment_mathematical_practice_test5.py), e.g.:
    python3 multi_agent_debate/build_dataset.py --data-dir ../Data --output multi_agent_debate/data/naep_pairs.csv
"""

import argparse
import itertools
import os
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))         # practices.py
sys.path.insert(0, str(HERE.parent))  # Code/: augment_mathematical_practice_test5.py, clean_utils.py

import augment_mathematical_practice_test5 as single_prompt  # noqa: E402
from practices import PRACTICE_NAMES, QUESTION  # noqa: E402

GROUND_TRUTH_COLUMN = "ground_truth"
PAIRS_PER_ITEM = len(PRACTICE_NAMES) * (len(PRACTICE_NAMES) - 1) // 2


def build_framework_text():
    """The six practice sections of the evaluated prompt, without the JSON-key annotations."""
    sections = [
        single_prompt.PROMPT_REPRESENTING,
        single_prompt.PROMPT_ABSTRACTING,
        single_prompt.PROMPT_JUSTIFYING,
        single_prompt.PROMPT_MODELING,
        single_prompt.PROMPT_COLLABORATIVE,
        single_prompt.PROMPT_PROCEDURAL,
    ]
    cleaned = []
    for section in sections:
        text = re.sub(r'\s*\(JSON key: "[^"]*"\)', "", section)
        text = "\n".join(line for line in text.splitlines() if line.strip() != "===")
        cleaned.append(text.strip())
    header = "Practice framework: six mathematical practices, each with a definition and descriptors."
    return header + "\n\n" + "\n\n".join(cleaned)


def build_item_text(row):
    """
    The item exactly as the single-prompt evaluation shows it (problem type, answer type, problem,
    answer choices, correct answer), without its "Item to rate" header and closing instruction.
    """
    prompt = single_prompt.create_user_prompt(row)
    prompt = re.sub(r"^Item to rate:\s*", "", prompt)
    prompt = prompt.split("\n\nRate this item")[0]
    return prompt.strip()


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--data-dir", default="../Data", help="Directory containing problems_naep.csv")
    parser.add_argument("--problems-file", default="problems_naep.csv")
    parser.add_argument("--output", default=str(HERE / "data" / "naep_pairs.csv"),
                        help="Where to write the pairwise debate CSV")
    parser.add_argument("--limit-problems", type=int, default=None,
                        help="Only use the first N items (for a pilot run)")
    return parser.parse_args()


def main():
    args = parse_args()
    if PRACTICE_NAMES != single_prompt.PRACTICE_NAMES:
        raise ValueError("practices.py is out of sync with augment_mathematical_practice_test5.PRACTICE_NAMES")

    problems_csv = os.path.join(args.data_dir, args.problems_file)
    problems_df = pd.read_csv(problems_csv, dtype=str, keep_default_na=False)
    if args.limit_problems is not None:
        problems_df = problems_df.head(args.limit_problems)
    # The ground truth must never reach a prompt: drop it (and any earlier predictions) first
    prompt_df = problems_df.drop(
        columns=[c for c in (GROUND_TRUTH_COLUMN, "mathematical_practice", "predicted_practice")
                 if c in problems_df.columns]
    )

    framework = build_framework_text()
    rows = []
    for _, row in prompt_df.iterrows():
        problem_id = row["problem_id"].strip()
        item = build_item_text(row)
        story = f"{framework}\n\nThe item being classified:\n{item}"
        for practice_1, practice_2 in itertools.combinations(PRACTICE_NAMES, 2):
            rows.append({
                "id": f"{problem_id}_{PRACTICE_NAMES.index(practice_1)}{PRACTICE_NAMES.index(practice_2)}",
                "problem_id": problem_id,
                "question": QUESTION,
                "item": item,
                "story": story,
                "story_title": problem_id,
                "question_set_id": problem_id,
                "correct answer": practice_1,   # slot 1 (not "correct" in this task)
                "negative answer": practice_2,  # slot 2
            })
    pairs_df = pd.DataFrame(rows)

    # Checks
    assert GROUND_TRUTH_COLUMN not in pairs_df.columns
    per_item = pairs_df.groupby("problem_id").size()
    assert (per_item == PAIRS_PER_ITEM).all(), f"expected {PAIRS_PER_ITEM} pairs per item"
    assert set(pairs_df["correct answer"]) | set(pairs_df["negative answer"]) <= set(PRACTICE_NAMES)
    assert pairs_df["id"].is_unique

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    pairs_df.to_csv(args.output, index=False, encoding="utf-8")

    print(f"Items: {len(per_item)}   pairs per item: {PAIRS_PER_ITEM}   rows: {len(pairs_df)}")
    print(f"Debates (both answer orders): {2 * len(pairs_df)}")
    print(f"Framework: {len(framework)} characters (~{len(framework) // 4} tokens)")
    print(f"Wrote {args.output}")
    sample = pairs_df.iloc[0]
    print(f"\nSample row {sample['id']}: {sample['correct answer']!r} vs {sample['negative answer']!r}")
    print(f"Question: {sample['question']}")
    print(f"Item:\n{sample['item']}")


if __name__ == "__main__":
    main()
