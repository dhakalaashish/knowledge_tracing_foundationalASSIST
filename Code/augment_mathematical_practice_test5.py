"""
Test version of augment_mathematical_practice.py: labels only the first 5 problems.

Same prompt, model, and parsing as augment_mathematical_practice.py. The difference is the
output: the original Problems.csv is only read, never modified. The first 5 rows, with the new
`mathematical_practice` column, are written to a separate file, Problems_test5.csv, in
--output-dir. Each cell is a JSON array of 6 independent probabilities (0 to 1; they do not
sum to 1), in this order:

    [Representing, Abstracting and Generalizing, Justifying and Proving,
     Mathematical Modeling, Collaborative Mathematics, Procedural Fluency]

Read a cell back with json.loads(cell).

Every run re-labels the 5 problems and overwrites Problems_test5.csv. Raw model responses and
reasoning are written to mathematical_practice_test5_raw.jsonl in --output-dir, and the
scores and reasoning for each problem are printed.

Run from the Code/ directory (it imports clean_utils and kt_inference_base).

Usage:
    CUDA_VISIBLE_DEVICES=0 python augment_mathematical_practice_test5.py \
        --data-dir ../Data \
        --output-dir ../Data \
        --cache-dir /data1/
"""

import argparse
import contextlib
import gc
import json
import os
import re

import numpy as np
import pandas as pd
import torch
from vllm import LLM, SamplingParams
from vllm.distributed.parallel_state import (
    destroy_model_parallel,
    destroy_distributed_environment,
)

from clean_utils import clean_problem_body
from kt_inference_base import (
    label_answer_options,
    get_correct_option_letters,
    format_answer_options_for_prompt,
)


DEFAULT_MODEL_ID = "Qwen/Qwen3-30B-A3B-Instruct-2507"

# Input / output files
PROBLEMS_FILE = "Problems.csv"
SKILL_FILE = "Skills.csv"
TEST_OUTPUT_FILE = "Problems_test5.csv"
RAW_OUTPUT_FILE = "mathematical_practice_test5_raw.jsonl"
OUTPUT_COLUMN = "mathematical_practice"

# Run config defaults
NUM_TEST_PROBLEMS = 5
DEFAULT_BATCH_SIZE = 512
DEFAULT_MAX_MODEL_LEN = 16384
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
# Used when --num-samples > 1 and for retrying unparsable responses.
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

About the items

- The items come from Illustrative Mathematics, a grades 6-8 curriculum, delivered in ASSISTments, an online learning platform.
- Each item is scored automatically from a single response: a typed number or expression, a selected choice, a dropdown selection, or an ordering. Students cannot submit written explanations, and they work alone.
- The problem text was converted from HTML. Images appear only as [image], answer blanks appear as ____, and dropdowns appear as [dropdown].
- Many items are one part of a multi-part problem. The text may refer to a figure, table, or earlier part that you cannot see. Rate what the visible text and answer format require; do not guess at hidden content.
- You also see the item's answer choices (if any), its correct answer, and its skill tag. The correct answer tells you what the student must produce. The skill tag describes the mathematics content, not the practice.

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

Boundary rules for common overlaps:
- Named people. Names in a story ("Jada ran 3 miles") do not make an item collaborative. When a named person's claim, answer, strategy, or work is what the student must evaluate or build on, Collaborative Mathematics is high, and Justifying and Proving is usually moderate because the student is judging a claim.
- Representing vs. Mathematical Modeling. If the student must set up the mathematics to solve a real-world problem, Modeling is high and Representing is moderate. If the student translates or interprets a representation without solving a real-world problem, Representing is high and Modeling is low.
- Mathematical Modeling vs. Procedural Fluency. Context alone is not modeling. If the quantities and the operation are obvious and there is nothing to set up or interpret, Procedural Fluency is high and Modeling is low.
- Abstracting and Generalizing vs. Procedural Fluency. Applying a rule, formula, or property that is given is procedural. Finding a rule, or recognizing a structure or property that holds in general, is Abstracting and Generalizing.
- Skill tags. The skill tag names the mathematics content. Do not infer a practice from the verb in the skill name (for example "Interpret..." or "Represent...").
- Missing context. If the item refers to an image or an earlier part you cannot see, score what the visible text and answer format require. Do not raise a score without visible evidence.

---

Output format

Respond with exactly one JSON object in this form, and write nothing before or after it. Fill in "reasoning" first, then the six numbers:

{
"reasoning": "<2-4 sentences: what the student must do to answer correctly, and which practice(s) that requires>",
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
        description=f"Label the first {NUM_TEST_PROBLEMS} problems with NAEP mathematical "
                    f"practice probabilities and write them to {TEST_OUTPUT_FILE}"
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
        help=f"Directory for {TEST_OUTPUT_FILE} and {RAW_OUTPUT_FILE} (default: current directory)"
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
        help=f"Problems per batch (default: {DEFAULT_BATCH_SIZE})"
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=1,
        help="Samples per problem. 1 uses greedy decoding; >1 samples at temperature 0.7 "
             "and averages the probabilities (default: 1)"
    )
    args = parser.parse_args()
    if args.num_samples < 1:
        parser.error("--num-samples must be at least 1")
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


def _to_number(value):
    """Convert a JSON value to a finite float, or None."""
    if isinstance(value, bool):
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if np.isfinite(value) else None


def parse_practice_scores(response_text):
    """
    Extract the practice scores from the last JSON object in the response.

    Returns (scores in PRACTICES order, reasoning), or (None, None) if no JSON object
    with all six numeric keys is found. Scores are clipped to [0, 1].
    """
    decoder = json.JSONDecoder()
    starts = [match.start() for match in re.finditer(r'\{', response_text)]
    for start in reversed(starts):
        try:
            obj, _ = decoder.raw_decode(response_text, start)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        values = [_to_number(obj.get(key)) for key in PRACTICE_KEYS]
        if any(value is None for value in values):
            continue
        # Model answered in percent (e.g. 80 instead of 0.8)
        if 1 < max(values) <= 100:
            values = [value / 100 for value in values]
        scores = [min(max(value, 0.0), 1.0) for value in values]
        return scores, str(obj.get('reasoning', ''))
    return None, None


def score_request_output(output):
    """Parse every sample of one vLLM output and average the valid score vectors."""
    vectors, reasonings, responses = [], [], []
    for completion in output.outputs:
        text = completion.text.strip()
        responses.append(text)
        scores, reasoning = parse_practice_scores(text)
        if scores is not None:
            vectors.append(scores)
            reasonings.append(reasoning)

    mean_scores = None
    if vectors:
        mean_scores = [round(float(value), 2) for value in np.mean(vectors, axis=0)]
    return {
        'scores': mean_scores,
        'num_valid_samples': len(vectors),
        'reasoning': reasonings,
        'responses': responses,
        'retried': False,
    }


def save_problems_csv(problems_df, output_csv):
    """Write the CSV atomically so an interrupted run never leaves a half-written file."""
    tmp_path = output_csv + '.tmp'
    problems_df.to_csv(tmp_path, index=False, encoding='utf-8', lineterminator='\n')
    os.replace(tmp_path, output_csv)


def append_results_jsonl(records, output_jsonl):
    """Append batch records to the raw output JSONL."""
    with open(output_jsonl, 'a', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')


def print_summary(problems_df):
    """Print how many rows have scores, the mean per practice, and the top-practice counts."""
    vectors = [json.loads(cell) for cell in problems_df[OUTPUT_COLUMN] if cell.strip()]
    print(f"Rows with scores: {len(vectors)} / {len(problems_df)}")
    if not vectors:
        return
    scores = np.array(vectors)
    top_counts = np.bincount(scores.argmax(axis=1), minlength=len(PRACTICES))
    for name, mean, count in zip(PRACTICE_NAMES, scores.mean(axis=0), top_counts):
        print(f"  {name:<30} mean {mean:.2f}   highest score in {count} rows")


def main():
    args = parse_args()

    problems_csv = os.path.join(args.data_dir, PROBLEMS_FILE)
    skill_csv = os.path.join(args.data_dir, SKILL_FILE)
    output_csv = os.path.join(args.output_dir, TEST_OUTPUT_FILE)
    output_jsonl = os.path.join(args.output_dir, RAW_OUTPUT_FILE)
    if os.path.abspath(output_csv) == os.path.abspath(problems_csv):
        raise ValueError(f"Output file would overwrite {problems_csv}")

    print(f"Model: {args.model_id}")
    print(f"Problems file (read only): {problems_csv}")
    print(f"Output CSV: {output_csv}")
    print(f"Raw output JSONL: {output_jsonl}")
    print(f"Samples per problem: {args.num_samples} ({'greedy' if args.num_samples == 1 else 'sampled, averaged'})")

    # Read every cell as text so the original columns are written back unchanged.
    # Only the first NUM_TEST_PROBLEMS rows are kept, and all of them are (re-)labeled.
    problems_df = pd.read_csv(problems_csv, dtype=str, keep_default_na=False)
    problems_df = problems_df.head(NUM_TEST_PROBLEMS).copy()
    problems_df[OUTPUT_COLUMN] = ''
    skill_names = load_skill_names(skill_csv)

    todo = list(problems_df.index)
    print(f"\nProblems to label: {len(todo)} "
          f"(problem_ids: {', '.join(problems_df['problem_id'])})")

    # Start a fresh raw output file for this run
    os.makedirs(args.output_dir, exist_ok=True)
    open(output_jsonl, 'w', encoding='utf-8').close()

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

    if args.num_samples == 1:
        sampling_params = SamplingParams(n=1, **GREEDY_SAMPLING)
    else:
        sampling_params = SamplingParams(n=args.num_samples, **STOCHASTIC_SAMPLING)
    retry_params = SamplingParams(n=1, **STOCHASTIC_SAMPLING)

    # Process in batches, saving after each one
    labeled = 0
    failed = 0
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

        # Retry unparsable responses once with sampling (greedy would repeat the same output)
        retry_positions = [pos for pos, result in enumerate(results) if result['scores'] is None]
        if retry_positions:
            print(f"Retrying {len(retry_positions)} unparsable responses...")
            retry_outputs = llm.chat(
                [conversations[pos] for pos in retry_positions], retry_params, use_tqdm=False
            )
            for pos, output in zip(retry_positions, retry_outputs):
                retried = score_request_output(output)
                retried['responses'] = results[pos]['responses'] + retried['responses']
                retried['retried'] = True
                results[pos] = retried

        records = []
        for idx, result in zip(batch, results):
            if result['scores'] is not None:
                problems_df.at[idx, OUTPUT_COLUMN] = json.dumps(result['scores'])
                labeled += 1
            else:
                failed += 1
            records.append({
                'problem_id': problems_df.at[idx, 'problem_id'],
                OUTPUT_COLUMN: result['scores'],
                'num_valid_samples': result['num_valid_samples'],
                'retried': result['retried'],
                'reasoning': result['reasoning'],
                'responses': result['responses'],
                'user_prompt': user_prompts[idx],
                'model_id': args.model_id,
            })

        for record in records:
            scores = record[OUTPUT_COLUMN]
            print(f"\nproblem_id {record['problem_id']}")
            if scores is None:
                print("  UNPARSED. Raw response:")
                print(record['responses'][-1])
                continue
            for name, score in zip(PRACTICE_NAMES, scores):
                print(f"  {name:<30} {score:.2f}")
            print(f"  Reasoning: {record['reasoning'][0]}")

        save_problems_csv(problems_df, output_csv)
        append_results_jsonl(records, output_jsonl)
        print(f"\nSaved {len(records)} results to {output_csv} and {output_jsonl}")

    # Also write the CSV when nothing was sendable, so the output always exists
    if not sendable:
        save_problems_csv(problems_df, output_csv)

    print(f"\n{'='*80}")
    print(f"Labeled: {labeled}, failed to parse: {failed}, skipped (too long): {len(too_long)}")
    if failed or too_long:
        print("Re-run the script to retry; the rows that failed are empty in the output CSV.")
    print_summary(problems_df)

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
