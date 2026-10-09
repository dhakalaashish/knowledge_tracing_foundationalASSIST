"""
Augment Problems.csv with NAEP mathematical practice probabilities.

For each problem, an LLM (Qwen3-30B-A3B-Instruct-2507 by default) reads the problem type,
answer type, problem body, answer choices, correct answer, and skill name. It then estimates
how likely it is that the item assesses each of six practices: the five NAEP 2026
Mathematical Practices plus Procedural Fluency (National Research Council, 2001).

The prompt (SYSTEM_PROMPT) is the one evaluated against the NAEP ground-truth items in
augment_mathematical_practice_test5.py; keep the two in sync.

The result is written to Problems.csv as two columns:
    mathematical_practice: JSON array of 6 independent probabilities (0 to 1; they do not
                           sum to 1), in this order:
        [Representing, Abstracting and Generalizing, Justifying and Proving,
         Mathematical Modeling, Collaborative Mathematics, Procedural Fluency]
                           Read a cell back with json.loads(cell).
    predicted_practice:    the model's primary_practice, the single practice the problem
                           mainly assesses (with --num-samples > 1, the one most samples chose)

A row counts as labeled only when predicted_practice is filled. Rows without it (including
rows scored by the earlier six-score prompt) are labeled on the next run, and their old
scores are cleared first, so an interrupted run resumes where it stopped without mixing
prompts. Raw model responses and reasoning are appended to mathematical_practice_raw.jsonl
in --output-dir. Before the first update, Problems.csv is backed up to Problems.csv.bak.

At the end, the script prints how many problems have each predicted_practice.

Run from the Code/ directory (it imports clean_utils and kt_inference_base).

Usage:
    CUDA_VISIBLE_DEVICES=0,1 python augment_mathematical_practice.py \
        --data-dir foundationalktdataset/ \
        --num-gpus 2 \
        --cache-dir /data1/

    # Print prompts and scores for 20 problems without writing anything
    python augment_mathematical_practice.py --data-dir foundationalktdataset/ --limit 20 --dry-run
"""

import argparse
import contextlib
import gc
import json
import os
import re
import shutil

import numpy as np
import pandas as pd
import torch
from vllm import LLM, SamplingParams
from vllm.distributed.parallel_state import (
    destroy_model_parallel,
    destroy_distributed_environment,
)

from clean_utils import clean_problem_body
from output_checks import (
    check_response,
    check_output_frame,
    print_format_report,
    structured_output_kwargs,
)
from kt_inference_base import (
    label_answer_options,
    get_correct_option_letters,
    format_answer_options_for_prompt,
)


DEFAULT_MODEL_ID = "Qwen/Qwen3-30B-A3B-Instruct-2507"

# Input / output files
PROBLEMS_FILE = "Problems.csv"
SKILL_FILE = "Skills.csv"
RAW_OUTPUT_FILE = "mathematical_practice_raw.jsonl"
OUTPUT_COLUMN = "mathematical_practice"
PREDICTED_COLUMN = "predicted_practice"

# Run config defaults
DEFAULT_BATCH_SIZE = 512
DEFAULT_MAX_MODEL_LEN = 16384
DEFAULT_DRY_RUN_LIMIT = 20
MAX_NEW_TOKENS = 1024

# Order of the probability array stored in OUTPUT_COLUMN.
# The first element of each pair is the JSON key the model returns.
PRACTICES = [
    ("representing", "Representing"),
    ("abstracting_and_generalizing", "Abstracting and Generalizing"),
    ("justifying_and_proving", "Justifying and Proving"),
    ("mathematical_modeling", "Mathematical Modeling"),
    ("collaborative_mathematics", "Collaborative Mathematics"),
    ("procedural_fluency", "Procedural Fluency"),
]
PRACTICE_KEYS = [key for key, _ in PRACTICES]
PRACTICE_NAMES = [name for _, name in PRACTICES]

# Greedy decoding: deterministic, used when --num-samples is 1
GREEDY_SAMPLING = {
    "temperature": 0.0,
    "max_tokens": MAX_NEW_TOKENS,
}
# Qwen's recommended settings for Qwen3 Instruct-2507 models.
# Used when --num-samples > 1 and for retrying responses that fail the format checks.
STOCHASTIC_SAMPLING = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "min_p": 0.0,
    "max_tokens": MAX_NEW_TOKENS,
}


# ---------------------------------------------------------------------------
# Prompts
#
# The "From the NAEP Framework" and "From Adding It Up" passages are the source
# text, verbatim except that in-text citations, page numbers, exhibit references,
# and paragraphs about assessment logistics were removed. The "Rater guidance"
# passages are written for this item bank and are not part of either source.
# ---------------------------------------------------------------------------

PROMPT_INTRO = """You are an expert in mathematics assessment. You have years of experience reviewing test items and deciding which mathematical practices each item assesses.

Your task: read ONE item from an online k-12 mathematics item bank and estimate, for each of six practices, the probability that an expert reviewer would say the item assesses that practice.

---

Assess the item's practice probability using:
    - Practice definition: defines what the practice measures 
    - Practice descriptors: non-comprehensive list of descriptions of what the practice could entail
Both the definition and the descriptor are important in identifying which practice the item belongs to

---

About the items

- A student works on each item alone. Practices that involve other people therefore appear through the item itself: the item shows another person's mathematical thinking (a named student's claim, strategy, answer, work, or a dialogue), and the student responds to it.
- Figures appear only as text descriptions such as [Image: ...], or as [image] when no description is available. Judge from what the text shows.

---

The six practices:

"""

PROMPT_REPRESENTING = """
===
1. Representing   (JSON key: "representing")

Practice definition:
Recognizing, using, creating, interpreting, or translating among representations appropriate for the grade level and the mathematics being assessed.

Practice descriptors:
    - Represent numbers, operations, or word problems using visual models (e.g., base 10, number lines, fraction strips).
    - Recognize, translate between, interpret, and compare written, numerical, and visual representations of large numbers (e.g., thousands).
    - Recognize, apply, create, or translate across multiple representations of fractions (e.g., visual models of equivalent fractions) and rational numbers (decimals, fractions, percents).
    - Create and justify solutions to word problems through numeric representations and operations.
    - Represent, interpret, or compare expressions or problem situations involving absolute values.
    - Select or use appropriate units or measurement instruments to represent or determine the attributes of an object.
    - Create visual representation of measurements or relationships between measurements.
    - Draw or sketch figures from a written description.
    - Represent, describe, or visualize figures from different views, including using 2-D representations of 3-D objects to solve problems.
    - Represent problem situations with geometric models to draw conclusions or solve mathematical or real-world problems.
    - Create a visual, graphical, or tabular representation of a given data set.
    - Compare and contrast different visual and graphical representations of univariate and bivariate data.
    - Justify the use of a particular representation of data over another.
    - Interpret visual representations to compare data sets, to draw inferences, or to make conclusions across two or more distinct data sets.
    - Create and use scatterplots to represent the relationship between two variables and to estimate the strength of the relationship (strong, weak, none).
    - Recognize, describe, or extend numerical and geometric patterns using tables, graphs, words, or symbols.
    - Express linear and exponential sequences in recursive or explicit forms given a table.
    - Translate between different representations of expressions using symbols, graphs, tables, diagrams, or written descriptions.
    - Use or create a graphical representation of a situation to draw conclusions.
"""

PROMPT_ABSTRACTING = """
===
2. Abstracting and Generalizing   (JSON key: "abstracting_and_generalizing")

Practice definition:
Decontextualizing, identifying commonality across cases, items, problems, or representations, and extending one's reasoning to a broader domain appropriate for the grade level and the mathematics being assessed.

Practice descriptors:
    - Identify patterns in numbers, figures, sequences, tables, or graphs and generalize them using words, pictures, or symbols.
    - Describe or extend a pattern, sequence, or relationship to a larger set of numbers, including from a given description.
    - Determine a generalized expression for a recursive pattern.
    - Find and generate structural relationships among sets of numbers.
    - Generalize understanding of place value.
    - Generalize findings about rational and irrational numbers.
    - Generalize, describe, compare, or extend numerical properties and operations across different domains or number systems (e.g., extend the properties of exponents to rational exponents).
    - Make generalizations about areas of squares or rectangles.
    - Generalize the effect of proportions and scaling for area and volume.
    - Extend quantified attributes to a larger set.
    - Make connections between representations of different measurement systems.
    - Extend trigonometric formulas to determine triangle unknowns.
    - Identify common elements and generalize geometric properties across different figures and families of figures (e.g., triangles, quadrilaterals, polygons, polyhedra).
    - Extend a geometric relationship from one or more figures to a family of figures.
    - Describe and generalize the effects of transformations (e.g., dilations, translations, rotations) and the relationships (e.g., congruence, similarity, orientation) between figures and their images.
    - Develop generalizations about transformations that preserve the area or volume of figures.
    - Make general conclusions from graphical or tabular representations of data (e.g., pictographs, bar graphs, dot plots) in terms of generalized phenomena (e.g., median, mode, range, shape, center, spread, clusters).
    - Organize and display data, and generalize patterns or trends in the data to suggest interpretations or infer conclusions.
    - Notice patterns of outcomes in a probability situation.
    - Develop generalizations about how linear transformations of one-variable data affect mean, median, mode, range, interquartile range, and standard deviation.
    - Extend and generalize numerical patterns, including arithmetic and geometric progressions.
    - Identify commonalities and compare and generalize properties within and across function families (e.g., linear, quadratic, rational, and exponential functions).
    - Develop general rules for translating functions and graphs.
    - Create connections across representations.

"""

PROMPT_JUSTIFYING = """
===
3. Justifying and Proving   (JSON key: "justifying_and_proving")

Practice definition:
Creating, evaluating, showing, or refuting mathematical claims in developmentally and mathematically appropriate ways.

Practice descriptors:
    - Make, justify, or defend conclusions and generalizations about numerical relationships or patterns, including why they are valid or will always hold.
    - Find a counterexample to refute a claim about number properties or operations.
    - Evaluate the appropriateness or validity of a provided argument about properties or operations.
    - Prove numerical or algebraic relationships through developing deductive arguments, finding counterexamples, engaging in proof by exhaustion, or employing mathematical induction.
    - Analyze or interpret a proof by mathematical induction about the properties of numbers.
    - Justify relationships between properties of number systems, including natural numbers, integers, rational numbers, real numbers, and complex numbers.
    - Defend, justify, or prove a claim about physical attributes, comparisons, or measurement properties.
    - Find or choose a counterexample to disprove a claim about properties such as area, length, or volume.
    - Evaluate the validity of a provided argument making use of measurement.
    - Explain why a given attribute can be appropriately measured by the chosen quantity and unit.
    - Prove conjectures about trigonometric identities.
    - Create, test, and validate geometric conjectures (e.g., distinguish which objects in a collection satisfy a given geometric property or definition and defend choices).
    - Verify properties of rotations, reflections, or translations.
    - Justify relationships of congruence and similarity of two-dimensional figures; apply these relationships using scaling and proportional reasoning.
    - Analyze a provided argument about geometric attributes or relationships.
    - Use given definitions and theorems to prove geometric conjectures.
    - Develop justifications and proofs that rely on a variety of representational modes (e.g., two-column, paragraph).
    - Discuss the implications that a definition of a type of figure has on the figure properties.
    - Evaluate the characteristics of a good survey or well-designed experiment, and justify or critique the validity of surveys or experiments.
    - Defend or counter conjectures offered based on a data set, including conjectures about bivariate data.
    - Justify or prove conjectures about probability.
    - Create and explore counting arguments in order to develop and justify conjectures.
    - Given a pattern or sequence, construct, explain, or justify a rule to generate the terms of the pattern or sequence.
    - Develop a valid mathematical argument based on properties of slope and intercept for linear functions.
    - Justify functional relationships across different representational forms, such as tables, equations, verbal descriptions, or graphs.
    - Create, validate, and justify conclusions and generalizations about functional relationships.
    - Verify a conclusion using algebraic properties.

"""

PROMPT_MODELING = """
===
4. Mathematical Modeling   (JSON key: "mathematical_modeling")

Practice Definition:
Making sense of a scenario, identifying a problem to be solved, mathematizing it, applying the mathematization to reach a solution, and checking the viability of the solution in developmentally and mathematically appropriate ways.

Practice descriptors:
    - Use physical or virtual materials to build a model of a number pattern or to predict or estimate results of a continued pattern.
    - Build a model of a situation for an estimation problem, and select and defend an appropriate method of estimation.
    - Select appropriate properties or operations that can be used to build a model of a situation or solve a problem.
    - Identify a mathematical problem from a given situation that could be modeled numerically or algebraically.
    - Create a physical or virtual model involving number and/or operation, and communicate and defend decisions about the model to an audience for feedback.
    - Identify the attribute(s) appropriate to measure in a given situation.
    - Mathematize a contextual measurement situation to lead to a solution.
    - Select, use, or evaluate the reasonableness of a model unit for an attribute in a real context, and defend the use of that unit.
    - Create a model to convert between two measurement systems.
    - Construct scale drawings to be used as measurement models of objects in problem situations.
    - Use existing geometric models to solve mathematical or real-world problems.
    - Create or construct geometric models of physical objects or situations, using physical or virtual materials, to solve mathematical or real-world problems.
    - Visually model the effects of successive (or composite) transformations of figures in the plane.
    - Predict the results of combining, subdividing, and transforming geometric figures.
    - Discuss differences in solutions caused by having used a simplified model.
    - Identify a statistical question to investigate in a given, open-ended or data-rich situation.
    - Create or use a statistical model to answer a statistical question or make a prediction about a data set.
    - Create or use a statistical model to assess the validity of a statistical claim.
    - Create a probability model to calculate or estimate the probability of an event.
    - Compare and contrast theoretical probabilities with results from experimental probabilities in a simulation.
    - Identify the variables needed to create an algebraic model of a situation.
    - Write algebraic relationships, expressions, equations, or inequalities to model real-world situations.
    - Revise an existing algebraic model based on introducing new variables or parameters.
    - Build or apply a mathematical model of a financial situation (e.g., a monthly family budget, or a car loan).

"""

PROMPT_COLLABORATIVE = """
===
5. Collaborative Mathematics   (JSON key: "collaborative_mathematics")

Practice definition:
The social enterprise of doing mathematics with others through discussion and collaborative problem solving whereby ideas are offered, debated, connected, and built-upon toward solution and shared understanding. Collaborative mathematics involves joint thinking among individuals toward the construction of a problem solution in developmentally and mathematically appropriate ways.

Practice descriptors:
    - Add to or build on a numerical model provided by others to complete a mathematical task.
    - Evaluate others' interpretations of numbers from real-life contexts.
    - Analyze the effect of another's estimation method on the accuracy of results.
    - Reflect on the work of others to extend a numerical pattern.
    - Evaluate the mathematical reasonableness of a peer's mathematical contribution.
    - Evaluate the validity of a measurement claim posed by others.
    - Analyze others' solutions and suggest a critique of their solutions in a situation involving measurement.
    - Attend to and make sense of the mathematical contributions of others in a situation involving measurement (e.g., revoice the work of others to clarify meaning of choice of measurement units).
    - Engage in joint thinking to reach consensus about a measurement situation.
    - Express and justify agreement or disagreement with a claim made by others in a geometric problem situation.
    - Build on the work of others to geometrically model a situation.
    - Evaluate the merit of others' geometric ideas.
    - Connect and generalize across geometric ideas contributed by others in a problem-solving situation.
    - Attend to the contributions of others in collaboratively generating a geometric proof.
    - Choose a worthwhile statistical question from a set offered by others about a problem situation or context involving data.
    - Recognize and critique misleading arguments from data (e.g., from media or other people).
    - Revoice/restate the work of others in addressing a statistical or probabilistic situation.
    - Analyze the models constructed by others to evaluate a new data set.
    - Verify the conclusions of others using algebraic or numerical properties.

"""

PROMPT_PROCEDURAL = """
===
6. Procedural Fluency   (JSON key: "procedural_fluency")

Practice Definition:
Procedural fluency refers to knowledge of procedures, knowledge of when and how to use them appropriately, and skill in performing them flexibly, accurately, and efficiently.

Practice descriptors:
    - Recall basic number combinations quickly and accurately, or derive them efficiently from known facts.
    - Carry out algorithms for addition, subtraction, multiplication, and division accurately and efficiently with whole numbers, fractions, decimals, and integers.
    - Perform mental computations flexibly, adapting procedures to the numbers involved (e.g., compensating, using benchmark numbers, multiplying by powers of 10).
    - Estimate the results of computations and use the estimates to check accuracy and order of magnitude.
    - Select an appropriate and efficient computational method (mental, written, calculator, or other tools) for a given task.
    - Convert accurately among equivalent forms of numbers (e.g., fractions, decimals, percents, scientific notation).
    - Apply procedures for operations with signed numbers, exponents, and roots accurately.
    - Carry out proportional, rate, and percent computations efficiently (e.g., unit rates, scaling, solving proportions).
    - Use measuring tools and read scales accurately and with appropriate precision.
    - Apply formulas for perimeter, area, surface area, and volume accurately and efficiently.
    - Convert units within and between measurement systems accurately.
    - Carry out geometric transformations (translations, reflections, rotations, dilations) accurately and determine the resulting images.
    - Perform geometric constructions and measurements accurately with tools or technology (e.g., ruler, protractor, compass, dynamic geometry software).
    - Apply known geometric relationships and formulas to compute unknown lengths, angles, or measures efficiently.
    - Compute statistical measures (e.g., mean, median, mode, range, interquartile range, standard deviation) accurately and efficiently.
    - Carry out the steps of constructing data displays accurately (e.g., setting scales and intervals, plotting values).
    - Use systematic counting procedures (e.g., organized lists, tree diagrams, tables, counting principles) to determine sample spaces.
    - Compute probabilities of simple, compound, and conditional events accurately.
    - Apply properties of operations to rewrite expressions in equivalent forms (e.g., combining like terms, expanding, factoring).
    - Evaluate expressions and functions accurately by substitution.
    - Solve equations, inequalities, and systems using appropriate and efficient procedures, from informal methods to formal symbolic manipulation.
    - Check results for accuracy (e.g., by substitution, estimation, or inverse operations) and correct procedural errors.

"""

PROMPT_SCORING = """
---

How to score

For each of the six practices, give a number from 0 to 1: the probability that an expert would say this item assesses that practice.

- Score each practice on its own. The six numbers do not need to add up to 1, however, one practice has to be the highest.
- Scale:
  - 0: no evidence; the practice is not involved.
  - 0.1-0.3: incidental; it plays a minor role (e.g. reading one value from a table).
  - 0.4-0.6: substantial, but shared with another practice or only part of what is needed.
  - 0.7-0.9: clearly required to answer the item correctly.
  - 1.0: the item is a textbook example of the practice from the practice descriptors.
- Base every score on what the student must do to produce the correct answer to this item, not on what a teacher could do with it or on the lesson it came from.
- Name the primary practice: the single practice the item mainly assesses. Give it the highest score. 

---

Output format

Respond with exactly one JSON object in this form, and write nothing before or after it. Fill in "reasoning" first, then "primary_practice", then the six numbers:

{
"reasoning": "<2-4 sentences: what the student must do to answer correctly, and which practice(s) that requires>",
"primary_practice": "<exactly one of: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, Procedural Fluency>",
"representing": <number from 0 to 1>,
"abstracting_and_generalizing": <number from 0 to 1>,
"justifying_and_proving": <number from 0 to 1>,
"mathematical_modeling": <number from 0 to 1>,
"collaborative_mathematics": <number from 0 to 1>,
"procedural_fluency": <number from 0 to 1>
}"""

SYSTEM_PROMPT = (
    PROMPT_INTRO
    + PROMPT_REPRESENTING
    + PROMPT_ABSTRACTING
    + PROMPT_JUSTIFYING
    + PROMPT_MODELING
    + PROMPT_COLLABORATIVE
    + PROMPT_PROCEDURAL
    + PROMPT_SCORING
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Add mathematical practice probabilities to Problems.csv"
    )
    parser.add_argument(
        "--data-dir", "-d",
        type=str,
        default=".",
        help="Directory containing Problems.csv and Skills.csv (default: current directory)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help=f"Directory for {RAW_OUTPUT_FILE} (default: current directory)"
    )
    parser.add_argument(
        "--model-id",
        type=str,
        default=DEFAULT_MODEL_ID,
        help=f"HuggingFace model ID (default: {DEFAULT_MODEL_ID})"
    )
    parser.add_argument(
        "--cache-dir", "-c",
        type=str,
        default=None,
        help="Directory for vLLM model cache (default: vLLM default)"
    )
    parser.add_argument(
        "--num-gpus",
        type=int,
        default=1,
        help="Number of GPUs for tensor parallelism (default: 1)"
    )
    parser.add_argument(
        "--gpu-memory-utilization",
        type=float,
        default=0.9,
        help="Fraction of GPU memory to use (vLLM, default: 0.9, range: 0.0-1.0)"
    )
    parser.add_argument(
        "--max-model-len",
        type=int,
        default=DEFAULT_MAX_MODEL_LEN,
        help=f"Maximum sequence length in tokens (vLLM, default: {DEFAULT_MAX_MODEL_LEN})"
    )
    parser.add_argument(
        "--batch-size", "-b",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Problems per batch; Problems.csv is saved after each batch (default: {DEFAULT_BATCH_SIZE})"
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=1,
        help="Samples per problem. 1 uses greedy decoding; >1 samples at temperature 0.7 "
             "and averages the probabilities (default: 1)"
    )
    parser.add_argument(
        "--no-structured-output",
        action="store_true",
        default=False,
        help="Do not constrain generation to the JSON schema; rely only on the format checks"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=f"Only label the first N problems that need labels "
             f"(default: all; {DEFAULT_DRY_RUN_LIMIT} with --dry-run)"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Re-label problems that already have a value"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print prompts and scores without writing Problems.csv or the raw JSONL"
    )
    args = parser.parse_args()
    if args.num_samples < 1:
        parser.error("--num-samples must be at least 1")
    if args.dry_run and args.limit is None:
        args.limit = DEFAULT_DRY_RUN_LIMIT
    return args


def load_skill_names(skills_csv):
    """Map problem_id to its skill names, e.g. "Interpret Products of Whole Numbers (3.OA.A.1)"."""
    skill_df = pd.read_csv(skills_csv, dtype=str, keep_default_na=False)
    skill_names = {}
    for problem_id, group in skill_df.groupby('problem_id', sort=False):
        labels = []
        for name, code in zip(group['node_name'], group['node_code']):
            name, code = name.strip(), code.strip()
            label = f"{name} ({code})" if code else name
            if label and label not in labels:
                labels.append(label)
        skill_names[problem_id.strip()] = '; '.join(labels)
    return skill_names


def mark_answer_blanks(body_html):
    """
    Replace ASSISTments answer-blank tags with visible markers.
    clean_problem_body would otherwise drop them, hiding where the student answers.
    """
    body_html = re.sub(
        r'<ast-r\b[^>]*\btype=["\']dropdown["\'][^>]*>(\s*</ast-r>)?', ' [dropdown] ', body_html
    )
    body_html = re.sub(r'<ast-r\b[^>]*>(\s*</ast-r>)?', ' ____ ', body_html)
    return body_html


def format_choices_and_answer(row):
    """
    Return (answer choices for the prompt or None, correct answer for the prompt).
    Multiple choice gets lettered options; dropdowns get their option list.
    """
    mc_options = row['Multiple Choice Options']
    if mc_options.strip():
        raw_options = label_answer_options(mc_options)
        options = {letter: clean_problem_body(text) for letter, text in raw_options.items()}
        letters = get_correct_option_letters(raw_options, row['Multiple Choice Answers'])
        correct_letters = [letter.strip() for letter in letters.split(',')]
        if letters and all(letter in options for letter in correct_letters):
            correct = '\n'.join(f"{letter}) {options[letter]}" for letter in correct_letters)
        else:
            correct = clean_problem_body(row['Multiple Choice Answers'])
        return format_answer_options_for_prompt(options), correct

    correct = clean_problem_body(row['Fill-in Answers'])
    if 'Drop Down' in row['Answer Types'] and row['Fill-in Options'].strip():
        choices = [clean_problem_body(opt) for opt in row['Fill-in Options'].split('</p>,')]
        return '\n'.join(f"- {choice}" for choice in choices if choice), correct
    if row['Problem Type'] == 'Order / Sort':
        correct = f"{correct}  (items listed in the correct order)"
    return None, correct


def create_user_prompt(row, skill_names):
    """Creates the per-problem user prompt."""
    choices, correct = format_choices_and_answer(row)
    skills = skill_names.get(row['problem_id'].strip()) or 'Undefined'

    prompt = "Item to rate:\n\n"
    prompt += f"Problem Type: {row['Problem Type']}\n"
    prompt += f"Answer Type: {row['Answer Types']}\n"
    prompt += f"Skill(s): {skills}\n\n"
    prompt += f"Problem:\n{clean_problem_body(mark_answer_blanks(row['Problem Body']))}\n\n"
    if choices:
        prompt += f"Answer Choices:\n{choices}\n\n"
    prompt += f"Correct Answer:\n{correct or 'Not available'}\n\n"
    prompt += "Rate this item on the six practices. Respond with only the JSON object described in the instructions."
    return prompt


def score_request_output(output):
    """
    Run the format checks (output_checks.check_response) on every sample of one vLLM output,
    average the scores of the samples that pass, and combine their primary_practice answers.
    Samples with format errors are left out.

    With several samples, the primary practice is the one most samples chose; a tied vote
    goes to the tied practice with the highest mean score.
    """
    vectors, primaries, reasonings, responses, errors, warnings = [], [], [], [], [], []
    for completion in output.outputs:
        text = completion.text.strip()
        responses.append(text)
        check = check_response(text, completion.finish_reason, PRACTICE_KEYS, PRACTICE_NAMES)
        errors.append(check['errors'])
        warnings.append(check['warnings'])
        if check['scores'] is not None:
            vectors.append(check['scores'])
            primaries.append(check['primary'])
            reasonings.append(check['reasoning'])

    mean_scores = None
    primary = None
    if vectors:
        mean_scores = [round(float(value), 2) for value in np.mean(vectors, axis=0)]
        votes = {name: primaries.count(name) for name in PRACTICE_NAMES}
        most = max(votes.values())
        tied = [name for name in PRACTICE_NAMES if votes[name] == most]
        primary = max(tied, key=lambda name: mean_scores[PRACTICE_NAMES.index(name)])
    return {
        'scores': mean_scores,
        'primary': primary,
        'primary_votes': primaries,
        'num_valid_samples': len(vectors),
        'reasoning': reasonings,
        'responses': responses,
        'format_errors': errors,
        'format_warnings': warnings,
        'retried': False,
    }


def save_problems_csv(problems_df, problems_csv):
    """Write Problems.csv atomically so an interrupted run never leaves a half-written file."""
    tmp_path = problems_csv + '.tmp'
    problems_df.to_csv(tmp_path, index=False, encoding='utf-8', lineterminator='\n')
    os.replace(tmp_path, problems_csv)


def append_results_jsonl(records, output_jsonl):
    """Append batch records to the raw output JSONL."""
    with open(output_jsonl, 'a', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')


def print_summary(problems_df):
    """
    Print how the labeled problems are spread over the practices. There is no ground truth
    for these problems, so the counts are the main way to see what the model decided:
      primary        problems whose predicted_practice is this practice (each counted once)
      highest score  problems where this practice has the highest probability
      score >= 0.7   problems where this practice is "clearly required" (can overlap)
      mean score     mean probability of this practice over all labeled problems
    """
    labeled = problems_df[problems_df[PREDICTED_COLUMN].str.strip() != '']
    print(f"\n{'='*80}")
    print(f"PRACTICE COUNTS ({len(labeled)} of {len(problems_df)} problems labeled)")
    print(f"{'='*80}")
    if labeled.empty:
        return

    scores = np.array([json.loads(cell) for cell in labeled[OUTPUT_COLUMN]])
    primary_counts = labeled[PREDICTED_COLUMN].value_counts()
    highest_counts = np.bincount(scores.argmax(axis=1), minlength=len(PRACTICES))
    strong_counts = (scores >= 0.7).sum(axis=0)

    print(f"  {'Practice':<30} {'primary':>15} {'highest score':>14} {'score >= 0.7':>13} {'mean score':>11}")
    for i, name in enumerate(PRACTICE_NAMES):
        count = int(primary_counts.get(name, 0))
        print(f"  {name:<30} {count:>6} ({count / len(labeled):>6.1%}) {int(highest_counts[i]):>14} "
              f"{int(strong_counts[i]):>13} {scores[:, i].mean():>11.2f}")
    print(f"  {'Total':<30} {len(labeled):>6} ({1:>6.1%})")

    highest_names = [PRACTICE_NAMES[i] for i in scores.argmax(axis=1)]
    differ = sum(p != h for p, h in zip(labeled[PREDICTED_COLUMN], highest_names))
    multi = int(((scores >= 0.7).sum(axis=1) >= 2).sum())
    print(f"\n  primary: the model's primary_practice (predicted_practice), each problem counted once")
    print(f"  highest score: this practice has the highest probability (ties go to the first practice)")
    print(f"  score >= 0.7: this practice is clearly required; a problem can count for several")
    print(f"  Problems whose primary_practice is not their highest score: {differ}")
    print(f"  Problems with two or more practices scored 0.7 or higher: {multi}")


def main():
    args = parse_args()

    problems_csv = os.path.join(args.data_dir, PROBLEMS_FILE)
    skill_csv = os.path.join(args.data_dir, SKILL_FILE)
    output_jsonl = os.path.join(args.output_dir, RAW_OUTPUT_FILE)

    print(f"Model: {args.model_id}")
    print(f"Problems file: {problems_csv}")
    print(f"Raw output JSONL: {output_jsonl}")
    print(f"Samples per problem: {args.num_samples} ({'greedy' if args.num_samples == 1 else 'sampled, averaged'})")
    print(f"Structured output: {'off (format checks only)' if args.no_structured_output else 'on (JSON schema enforced during generation)'}")
    if args.dry_run:
        print("DRY RUN: nothing will be written")

    # Read every cell as text so the original columns are written back unchanged.
    # original_df is kept untouched so check_output_frame can verify that before each save.
    original_df = pd.read_csv(problems_csv, dtype=str, keep_default_na=False)
    problems_df = original_df.copy()
    for column in (OUTPUT_COLUMN, PREDICTED_COLUMN):
        if column not in problems_df.columns:
            problems_df[column] = ''
    skill_names = load_skill_names(skill_csv)

    # A row is labeled only when predicted_practice is filled. Rows without it (for example,
    # scored by the earlier six-score prompt) are relabeled, and their old scores are cleared
    # so scores and predicted_practice always come from the same prompt.
    if args.overwrite:
        needs_label = problems_df.index
    else:
        needs_label = problems_df.index[problems_df[PREDICTED_COLUMN].str.strip() == '']
    stale = int((problems_df.loc[needs_label, OUTPUT_COLUMN].str.strip() != '').sum())
    problems_df.loc[needs_label, [OUTPUT_COLUMN, PREDICTED_COLUMN]] = ''
    todo = list(needs_label)
    print(f"\nProblems: {len(problems_df)}, needing labels: {len(todo)}")
    if stale:
        print(f"Cleared {stale} old scores (from an earlier prompt) that will be replaced. "
              f"Before the first save, {PROBLEMS_FILE} is copied to {PROBLEMS_FILE}.bak "
              f"if no backup exists yet.")
    if args.limit is not None:
        todo = todo[:args.limit]
        print(f"Limited to: {len(todo)}")
    if not todo:
        print("Nothing to label.")
        print_summary(problems_df)
        return

    user_prompts = {idx: create_user_prompt(problems_df.loc[idx], skill_names) for idx in todo}
    print(f"\nExample user prompt (problem_id {problems_df.at[todo[0], 'problem_id']}):\n")
    print(user_prompts[todo[0]])

    # Initialize vLLM engine
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
    prompt_tokens = {
        idx: system_tokens + len(tokenizer.encode(user_prompts[idx])) + chat_template_overhead
        for idx in todo
    }
    sendable = [idx for idx in todo if prompt_tokens[idx] <= prompt_budget]
    too_long = [idx for idx in todo if prompt_tokens[idx] > prompt_budget]
    print(f"System prompt: {system_tokens} tokens; "
          f"longest full prompt: {max(prompt_tokens.values())} tokens; budget: {prompt_budget}")
    if too_long:
        too_long_ids = [problems_df.at[idx, 'problem_id'] for idx in too_long]
        print(f"WARNING: skipping {len(too_long)} prompts over budget "
              f"(raise --max-model-len to include them): {too_long_ids}")

    # Constrain every response, including retries, to the JSON schema in output_checks
    schema_constraint = ({} if args.no_structured_output
                         else structured_output_kwargs(PRACTICE_KEYS, PRACTICE_NAMES))
    if args.num_samples == 1:
        sampling_params = SamplingParams(n=1, **GREEDY_SAMPLING, **schema_constraint)
    else:
        sampling_params = SamplingParams(n=args.num_samples, **STOCHASTIC_SAMPLING, **schema_constraint)
    retry_params = SamplingParams(n=1, **STOCHASTIC_SAMPLING, **schema_constraint)

    if not args.dry_run:
        backup_csv = problems_csv + '.bak'
        if not os.path.exists(backup_csv):
            shutil.copy2(problems_csv, backup_csv)
            print(f"Backed up original to {backup_csv}")

    # Process in batches, saving after each one
    labeled = 0
    failed = 0
    all_records = []
    num_batches = (len(sendable) + args.batch_size - 1) // args.batch_size

    for batch_idx in range(num_batches):
        batch = sendable[batch_idx * args.batch_size:(batch_idx + 1) * args.batch_size]
        conversations = [
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompts[idx]},
            ]
            for idx in batch
        ]

        print(f"\n{'='*80}")
        print(f"Processing batch {batch_idx + 1}/{num_batches} ({len(batch)} problems)")
        print(f"{'='*80}")

        outputs = llm.chat(conversations, sampling_params, use_tqdm=True)
        results = [score_request_output(output) for output in outputs]

        # Retry responses that failed the format checks once with sampling
        # (greedy would repeat the same output)
        retry_positions = [pos for pos, result in enumerate(results) if result['scores'] is None]
        if retry_positions:
            print(f"Retrying {len(retry_positions)} responses that failed the format checks...")
            retry_outputs = llm.chat(
                [conversations[pos] for pos in retry_positions], retry_params, use_tqdm=False
            )
            for pos, output in zip(retry_positions, retry_outputs):
                retried = score_request_output(output)
                for key in ('responses', 'format_errors', 'format_warnings'):
                    retried[key] = results[pos][key] + retried[key]
                retried['retried'] = True
                results[pos] = retried

        records = []
        for idx, result in zip(batch, results):
            if result['scores'] is not None:
                problems_df.at[idx, OUTPUT_COLUMN] = json.dumps(result['scores'])
                problems_df.at[idx, PREDICTED_COLUMN] = result['primary']
                labeled += 1
            else:
                failed += 1
            records.append({
                'problem_id': problems_df.at[idx, 'problem_id'],
                OUTPUT_COLUMN: result['scores'],
                PREDICTED_COLUMN: result['primary'],
                'primary_votes': result['primary_votes'],
                'num_valid_samples': result['num_valid_samples'],
                'retried': result['retried'],
                'format_errors': result['format_errors'],
                'format_warnings': result['format_warnings'],
                'reasoning': result['reasoning'],
                'responses': result['responses'],
                'user_prompt': user_prompts[idx],
                'model_id': args.model_id,
            })
        all_records.extend(records)

        # Refuse to save if any original column changed, a score cell is malformed, or
        # predicted_practice is not a practice name
        check_output_frame(original_df, problems_df, OUTPUT_COLUMN, PRACTICE_NAMES,
                           predicted_column=PREDICTED_COLUMN)

        if args.dry_run:
            for record in records:
                scores = record[OUTPUT_COLUMN]
                print(f"\nproblem_id {record['problem_id']}")
                if scores is None:
                    print(f"  FAILED FORMAT CHECKS: {record['format_errors']}")
                    print("  Last raw response:")
                    print(record['responses'][-1])
                    continue
                for name, score in zip(PRACTICE_NAMES, scores):
                    print(f"  {name:<30} {score:.2f}")
                print(f"  Primary practice: {record[PREDICTED_COLUMN]}")
                print(f"  Reasoning: {record['reasoning'][0]}")
                if any(record['format_warnings']):
                    print(f"  Format warnings: {record['format_warnings']}")
        else:
            save_problems_csv(problems_df, problems_csv)
            append_results_jsonl(records, output_jsonl)
            print(f"Saved {len(records)} results to {problems_csv} and {output_jsonl}")

    print(f"\n{'='*80}")
    print(f"Labeled: {labeled}, failed format checks: {failed}, skipped (too long): {len(too_long)}")
    if failed or too_long:
        print("Re-run the script to retry the rows that are still empty.")
    print_format_report(all_records)
    print_summary(problems_df)
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
