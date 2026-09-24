"""
Augment Problems.csv with NAEP mathematical practice probabilities.

For each problem, an LLM (Qwen3-30B-A3B-Instruct-2507 by default) reads the problem type,
answer type, problem body, answer choices, correct answer, and skill name. It then estimates
how likely it is that the item assesses each of six practices: the five NAEP 2026
Mathematical Practices plus Procedural Fluency (National Research Council, 2001).

The result is written to Problems.csv as a new column, `mathematical_practice`. Each cell is
a JSON array of 6 independent probabilities (0 to 1; they do not sum to 1), in this order:

    [Representing, Abstracting and Generalizing, Justifying and Proving,
     Mathematical Modeling, Collaborative Mathematics, Procedural Fluency]

Read a cell back with json.loads(cell).

Rows that already have a value are skipped, so an interrupted run resumes where it stopped.
Raw model responses and reasoning are appended to mathematical_practice_raw.jsonl in
--output-dir. Before the first update, Problems.csv is backed up to Problems.csv.bak.

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

PROMPT_INTRO = """You are an expert in mathematics assessment. You have years of experience reviewing test items against the NAEP 2026 Mathematics Framework and deciding which mathematical practices each item assesses.

Your task: read ONE item from an online middle-school mathematics item bank and estimate, for each of six practices, the probability that an expert NAEP item reviewer would say the item assesses that practice.

---

About the items

- The items come from Illustrative Mathematics, a grades 6-8 curriculum, delivered in ASSISTments, an online learning platform.
- Each item is scored automatically from a single response: a typed number or expression, a selected choice, a dropdown selection, or an ordering. Students cannot submit written explanations, and they work alone.
- The problem text was converted from HTML. Images appear only as [image], answer blanks appear as ____, and dropdowns appear as [dropdown].
- Many items are one part of a multi-part problem. The text may refer to a figure, table, or earlier part that you cannot see. Rate what the visible text and answer format require; do not guess at hidden content.
- You also see the item's answer choices (if any), its correct answer, and its skill tag. The correct answer tells you what the student must produce. The skill tag describes the mathematics content, not the practice.

---

The six practices

The first five are the NAEP Mathematical Practices. For each one you get the official NAEP definition, the Framework's description of it, and rater guidance written for this item bank. The sixth, Procedural Fluency, is not a NAEP practice; it is a strand of mathematical proficiency from the National Research Council's "Adding It Up" (2001). It is included so that items that mainly require carrying out procedures, and that feature none of the NAEP practices, are rated too.
"""

PROMPT_REPRESENTING = """
===
1. Representing   (JSON key: "representing")

Official NAEP definition:
Representing: Recognizing, using, creating, interpreting, or translating among representations appropriate for the grade level and the mathematics being assessed.

From the NAEP Framework:
Representing mathematical ideas and using mathematical representations to make sense of and solve problems is central to mathematics. Students create representations themselves, or in collaboration with other students, and they reason from or translate between standard representations (e.g., graphs, tables, geometric drawings). Variety in representations "is like examining a concept through a variety of lenses, with each lens providing a different perspective that makes the picture (concept) richer and deeper."

Students, especially young ones, benefit from using physical objects or acting out processes during problem solving. Base 10 blocks (or blocks/tiles representing other bases), fraction strips/bars, red-black integer tiles, and algebra tiles are all examples of physical representations of number and operation that are used to enhance students' understanding of concepts in elementary and middle grades. These visual and physical representations connect, eventually, to symbolic representations as well. Visual representations also play a particularly powerful role in helping students make sense of problems and understand mathematical concepts and procedures. For instance, arrays of squares in a grid can be used to represent area models for mathematical operations such as multiplication and division in early elementary grades, then later for multiplication of algebraic expressions. Additionally, students create, use, and reason about multiple representations for a given mathematical idea or relationship in contextually relevant ways.

Rater guidance for this item bank:
- High when the student must read meaning from, create, complete, choose, or translate between representations: graphs, tables, number lines, double number lines, tape diagrams, geometric drawings, coordinate points, equations, expressions, or verbal descriptions.
- Typical items: "Which graph represents y = 2x + 1?"; "The point (4, 12) is on the graph of hours worked and dollars earned. What does it mean?"; "Write an equation that matches the tape diagram."; "Complete the table."
- Low (0.1-0.3) when a table or diagram only supplies numbers for a routine calculation.
"""

PROMPT_ABSTRACTING = """
===
2. Abstracting and Generalizing   (JSON key: "abstracting_and_generalizing")

Official NAEP definition:
Abstracting and Generalizing: Decontextualizing, identifying commonality across cases, items, problems, or representations, and extending one's reasoning to a broader domain appropriate for the grade level and the mathematics being assessed.

From the NAEP Framework:
Abstracting. Students learning and doing mathematics also engage in the practice of abstracting and generalizing. An essential element of mathematical learning and problem solving is the ability to reason abstractly and to develop, test, and refine generalizations. In reasoning abstractly, students engage in the process of decontextualizing: Students abstract ideas in a given problem or context and express and manipulate them in a manner independent of their contextual references. Decontextualizing can foster an understanding of the relationships among problem contexts and written or symbolic forms, as well as an understanding of how mathematical expressions might be transformed to facilitate a solution strategy. Abstracting is also a critical activity for fostering generalizing; it enables a consideration of concepts and relationships decontextualized from specific examples or cases, which can support the formation of a more general rule or relationship.

Young students, for instance, can notice patterns of additive commutativity, such as 3 + 7 yielding the same sum as 7 + 3. In this instance, decontextualization would include finding a way to represent this relation independent of particular numbers, as a more general identity. Younger students might express this general identity verbally or with pictures, or with the use of a generic example. Older students might express this identity algebraically as a + b = b + a. Reasoning abstractly can also support recognizing similar mathematical structures across different problems or domains. For example, one could see the multiplication of two binomials (2x + 7)(3x + 2) as a more general version of multiplying 27 by 32.

Abstracting can occur across different domains. It can be addressed in reasoning about figures and their relationships in geometry, about number theory in number properties and operations, or about equivalence or functional relationships in algebra. How one decontextualizes or reasons with structure will differ across the domains, but these are processes students can employ in all five content areas included in the NAEP Mathematics Assessment.

Generalizing. Historically, generalization has been defined as an individual, cognitive construct, where generalization is the act of identifying a property that holds for a larger set of mathematical objects or conditions than the number of individually verified cases. It has been described as the process of "applying a given argument in a broader context," and as identifying a commonality based on particulars and then extending it to all terms. More recently, researchers have begun to address generalizing as a construct that is both social and cognitive; that is, it can occur either individually or collectively. Therefore, for NAEP, generalizing is an individual or collective practice of (a) identifying commonality across cases, (b) extending reasoning beyond the domain in which it originated, and/or (c) deriving broader results from particular cases.

Several aspects of mathematical reasoning can foster generalizing. Abstracting and decontextualizing are important mental actions that support generalizing. Other actions that support generalizing include visualizing, focusing, reflecting, connecting, and expressing. Visualizing involves seeing patterns or structural relationships, as well as imagining a set of relationships beyond what is perceptually available. Focusing is attending to particular details, characteristics, properties, or relationships above others. This can include examining a particular case in a pattern or attending to figural or numerical cues. Reflecting involves actions such as thinking back on the operations one has carried out, observing one's method in solving problems, or examining the rules that govern a given pattern. Connecting is the identification of relationships among tasks, representations, or properties. Making connections between representations or identifying and operating on structural similarities can foster the development of generalizations. Finally, expressing involves depicting a generalization verbally or in writing. Describing generalizations in words can support the subsequent development of algebraically represented generalizations.

Like abstracting, generalizing can occur across the content areas and grade bands. Existing NAEP Mathematics Assessment items contain a number of generalization tasks in which students are asked to determine a rule guiding the pattern of number terms in a sequence. In some items, potential rules are provided for students who are prompted only to attend to the action required to move from one term in the sequence to the next. In other items, students must determine a rule themselves. Students can also be challenged to engage in the processes of generalizing in items that do not rely on pattern sequences. One aspect of generalizing is identifying commonality across cases.

Rater guidance for this item bank:
- High when the student must find or recognize a rule, pattern, or structure that holds for every case: the n-th term of a pattern, an expression with a variable that works for any value, equivalent expressions, properties of operations (distributive, commutative), or a relationship shared by several situations once the context is removed.
- Typical items: "Which expressions are equivalent to 6x + 9? Select all that apply."; "Each figure has 3 more tiles than the one before. Write an expression for the number of tiles in figure n."; "Which of these relationships are proportional?"
- Low when the student only substitutes numbers into a rule or formula that is given; that is Procedural Fluency.
"""

PROMPT_JUSTIFYING = """
===
3. Justifying and Proving   (JSON key: "justifying_and_proving")

Official NAEP definition:
Justifying and Proving: Creating, evaluating, showing, or refuting mathematical claims in developmentally and mathematically appropriate ways.

From the NAEP Framework:
Justifying and proving are essential in all content areas and grade levels. State standards highlight the activities students engage in as they learn to create valid mathematical arguments: making and investigating conjectures, developing particular forms of argument (e.g., deductive), and using a variety of proof methods (e.g., direct, counterexample). These are all considered components of the practice of justifying and proving.

Mathematical justification includes creating arguments, explaining why conjectures must be true or demonstrating that they are false, exploring special cases or searching for counterexamples, understanding the role of definitions and counterexamples, and evaluating arguments. A valid justification should show why a statement or conjecture is true or not true generally (i.e., for all cases) and, especially by grades 8 and 12, should do so by providing a logical sequence of statements, each building on already established statements, ideas, or relationships.

A justification is not based on authority, perception, popular consensus, or examples alone. As students engage in justifying, they may be tempted to rely on external sources to verify their ideas, such as their teacher or a textbook. Students may also want to use examples to support their claims, concluding that a conjecture must be true because it holds for several different cases. Examples can and do play an important role in justifying and proving, particularly in terms of helping students make sense of statements, gain a sense of conviction, or revealing an underlying structure that could lead to a proof. But they do not suffice as a mathematical justification or proof except for proofs by exhaustion or counterexample.

A proof can have many different forms, including narrative, pictorial, diagram, two-column, or algebraic forms. The form used to represent a mathematical proof is valid as long as it communicates the proof's essential features, namely, that it contains logically connected mathematical statements that are based on valid definitions and theorems.

In addition to the various formats one can use to develop or present proofs, there are other ways of mathematically proving, disproving, or justifying a mathematical answer. These include developing deductive arguments, finding counterexamples, proving by exhaustion (i.e., verifying every possible case), and employing mathematical induction. Often, it may be easier to use a particular mode of argumentation based on the nature of the claim.

The process of refuting (demonstrating that a statement is false) is a key element of justification because conjecturing can produce both true and false statements. Students must understand that a single counterexample disproves a conjectured generalization. Understanding that a single counterexample undermines a general claim is an important but difficult aspect of justification. Learning to search for counterexamples and explaining why they are justifications is only one aspect of refutation. Attempting to prove that a conjecture is false can also lead to the development of new insights or ideas, as well as to the formation of different conjectures that can then be explored, refuted, or proved. Knowing a variety of approaches to generating a proof and knowing which one to select for a particular circumstance is an important aspect of justifying and proving.

Another element of justifying and proving is evaluating the validity of a purported proof. This involves not only deciding whether a proof is valid in terms of its conclusion, but also deciding whether a given proof relies on correct assumptions, makes use of merited conclusions and logic, and explains the entire statement or conclusion. These skills can be fostered by challenging students to judge the appropriateness of a given argument (e.g., a formal or informal proof).

Engaging in justifying and proving is a way for students to explore why a particular assertion must be true. While investigating the reasons a conjecture might be true, students attend to particular features and consider relationships, examine multiple factors that are relevant to the problem statement, return to the meanings of terms and operations, or notice similarity or difference across cases. By exploring these factors, students gain new insight into the conjecture or deepen their understanding of fundamental mathematical ideas.

Rater guidance for this item bank:
- Because answers are scored automatically, this practice usually appears as choosing: whether a claim is always, sometimes, or never true; a counterexample; the reason that shows why something is true; or whether a given argument or solution is valid.
- Typical items: "Is the sum of two odd numbers always even?"; "Which value of x shows that x^2 > x is not always true?"; "Which statement explains why the two triangles must be similar?"
- Low when the student only states a result and nothing about why it is true is asked or checked.
"""

PROMPT_MODELING = """
===
4. Mathematical Modeling   (JSON key: "mathematical_modeling")

Official NAEP definition:
Mathematical Modeling: Making sense of a scenario, identifying a problem to be solved, mathematizing it, applying the mathematization to reach a solution, and checking the viability of the solution in developmentally and mathematically appropriate ways.

From the NAEP Framework:
Mathematical modeling involves student choice, including the assumptions made in the posing of answerable questions in an open-ended situation. The practice of modeling requires students to make sense of a scenario, identify a problem to be solved, mathematize it, and apply the mathematization to reach a solution and check the viability of the solution. Mathematical modeling also requires discussions and decisions about what is valuable.

At an introductory level, modeling involves steps such as selecting and applying mathematical processes or expressing mathematical concepts and processes (such as mathematical operations) using visual, physical, or symbolic representations. At a more advanced level, a series of processes may be needed to mathematize a messy real-world situation prior to selecting and applying the mathematics. Follow-up work can involve analyzing and evaluating the results obtained from doing the mathematics. A full cycle in the mathematical modeling process includes: (a) identifying the problem; (b) making assumptions that often simplify the problem and then identifying variables; (c) mathematizing the situation; (d) analyzing and assessing solutions; and (e) translating the solution(s) back into the real world and examining their feasibility, and, if not feasible, changing the simplifying assumptions and iterating the process. Finally, if there seems to be a feasible real-world solution, there are two additional steps: (f) implementing the model; and (g) reporting out results.

It is important to distinguish between the process of mathematical modeling and the noun "model," which is an object and a term sometimes used as a synonym for a mathematical representation. For example, when a line or other function is fitted to a bivariate scatterplot, the function is referred to as a model for the data, meaning a representation of the data. However, the practice of mathematical modeling involves far more than just using a representation. As previously described, mathematical modeling is a multistep process, which may involve aspects of representing, particularly building or interpreting a representation. However, the NAEP Mathematical Practice of Mathematical Modeling is distinct from that of Representing in that the use of representations in modeling is necessarily in service of the overarching purpose of identifying and finding solutions for problems in real-world situations. Items assessing the NAEP Mathematical Practice of Mathematical Modeling focus on multiple steps of the cycle of mathematical modeling driven by that overarching purpose. For example, given an open-ended situation, students could generate questions they would need to explore or identify some assumptions as they begin the modeling process. In such scenarios, students would engage in the first two steps of the modeling process.

Scenario-based tasks are particularly useful in assessing student achievement in the practice of mathematical modeling.

Rater guidance for this item bank:
- High when the item gives a real-world situation and the student must turn it into mathematics themselves (decide which quantities and relationships matter, choose the operations, or set up an equation, table, or expression) to answer a question about the situation, and ideally interpret or check the answer in context.
- Typical items: "Diego has $11 and saves $5 each week. Lin has $60 and spends $2 each week. Is there a week when they have the same amount of money?"; "A family needs 10 liters of paint and each can holds 3 liters. How many cans should they buy?"
- Low (0-0.3) when the context is only a wrapper around one obvious computation, e.g. "There are 5,280 feet in a mile. Jada ran 3 1/4 miles. How many feet is that?" That item is mostly Procedural Fluency.
"""

PROMPT_COLLABORATIVE = """
===
5. Collaborative Mathematics   (JSON key: "collaborative_mathematics")

Official NAEP definition:
Collaborative Mathematics: The social enterprise of doing mathematics with others through discussion and collaborative problem solving whereby ideas are offered, debated, connected, and built-upon toward solution and shared understanding. Collaborative mathematics involves joint thinking among individuals toward the construction of a problem solution in developmentally and mathematically appropriate ways.

From the NAEP Framework:
As a practice, collaborative mathematics exists alongside other mathematical practices. That is, as students work together toward a shared goal, they may also engage in representing, abstracting and generalizing, justifying and proving, and mathematical modeling. Assessing collaborative mathematics requires developing items that foreground and require the doing of mathematics collaboratively, engaging processes that are fundamentally about joint thinking. Collectively, these processes include sharing ideas with others; attending to and making sense of the mathematical contributions of others; evaluating the merit of others' ideas through agreement or disagreement; and productively responding to others' ideas through building on or extending ideas and connecting or generalizing across ideas.

Collaborative mathematics processes are largely understood as discursive in nature and occurring through social interaction during mathematical activity. Given the discursive nature of collaborative mathematics, NAEP Mathematics Assessment items that measure collaborative processes should likewise be discursive in nature, offering students examples of social interaction or imagined utterances around mathematics to which they are tasked to respond in key ways. These include being asked to make sense of others' thinking, express and defend agreement or disagreement, and extend an idea.

Three measurable skills are involved in collaborative mathematics: attending to and making sense of the mathematical contributions of others, evaluating the mathematical merit of the contributions of others, and responding productively to others' mathematical ideas.

Attending to and making sense of the mathematical contributions of others. Collaborative mathematics begins with the sharing of ideas in the form of a conjecture or other contribution that is meant to be communicated to others. A first joint act is made up of both this sharing and how others attend to the conjecture and make sense of it. To do so, students must establish a shared understanding about what the problem is and how the problem is being interpreted. People elicit and probe ideas. Individuals then express and check personal understanding of another's thinking by repeating or revoicing the idea. From an assessment perspective, students can be asked to revoice (or put into their own words) the expressed mathematical ideas of another student/an avatar, or to justify its mathematical appropriateness.

Evaluating the mathematical merit of the contributions of others. Once students attend to and make sense of the thinking of others, they must evaluate the mathematical reasonableness of their peers' mathematical contributions. Generally, students express their evaluation of the mathematical reasonableness of an idea through agreement or disagreement, including some explanation or justification. Agreeing or disagreeing emerges out of shared understanding. This skill is critical to the development of productive mathematical argumentation.

Responding productively to others' mathematical ideas. Students learn to build on, extend, and connect across mathematical ideas. These discursive acts depend and build on the acts of making sense of and evaluating others' mathematical thinking. Once a shared mathematical idea is understood, students can further contribute to the mathematical discussion by acting upon those shared ideas. Connecting across students' mathematical ideas is a core discursive component of productive collaborative mathematics. By connecting ideas, students are able to notice and explain how two seemingly different strategies hold the same mathematical ideas. Students also build on or extend an idea through new examples, next steps, or logical deductions.

Rater guidance for this item bank:
- Students work alone here, so this practice appears only in its "imagined utterance" form: the item presents another person's mathematical thinking (a named student's claim, answer, strategy, or work, or two people who disagree), and the student must make sense of it, judge whether it is correct, find the error, or build on it.
- Typical items: "Noah says 0.3 x 0.2 = 0.6. Is Noah correct?"; "Han says the ratios are equivalent. Elena says they are not. Who is correct?"; "Priya's work is shown. In which step did she make a mistake?"
- 0 when named people only appear as characters in a story and no one's thinking is being evaluated, e.g. "Jada ran 3 miles."
"""

PROMPT_PROCEDURAL = """
===
6. Procedural Fluency   (JSON key: "procedural_fluency")

Definition (National Research Council, "Adding It Up", 2001):
Procedural fluency refers to knowledge of procedures, knowledge of when and how to use them appropriately, and skill in performing them flexibly, accurately, and efficiently.

From "Adding It Up":
In the domain of number, procedural fluency is especially needed to support conceptual understanding of place value and the meanings of rational numbers. It also supports the analysis of similarities and differences between methods of calculating. These methods include, in addition to written procedures, mental methods for finding certain sums, differences, products, or quotients, as well as methods that use calculators, computers, or manipulative materials such as blocks, counters, or beads.

Students need to be efficient and accurate in performing basic computations with whole numbers (6+7, 17-9, 8x4, and so on) without always having to refer to tables or other aids. They also need to know reasonably efficient and accurate ways to add, subtract, multiply, and divide multidigit numbers, both mentally and with pencil and paper. A good conceptual understanding of place value in the base-10 system supports the development of fluency in multidigit computation. Such understanding also supports simplified but accurate mental arithmetic and more flexible ways of dealing with numbers than many students ultimately achieve.

Connected with procedural fluency is knowledge of ways to estimate the result of a procedure. Many tasks involving mathematics in everyday life require facility with algorithms for performing computations either mentally or in writing.

In addition to providing tools for computing, some algorithms are important as concepts in their own right, which again illustrates the link between conceptual understanding and procedural fluency. Students need to see that procedures can be developed that will solve entire classes of problems, not just individual problems. By studying algorithms as "general procedures," students can gain insight into the fact that mathematics is well structured (highly organized, filled with patterns, predictable) and that a carefully developed procedure can be a powerful tool for completing routine tasks.

It is important for computational procedures to be efficient, to be used accurately, and to result in correct answers. Both accuracy and efficiency can be improved with practice, which can also help students maintain fluency. Students also need to be able to apply procedures flexibly. Not all computational situations are alike. For example, applying a standard pencil-and-paper algorithm to find the result of every multiplication problem is neither necessary nor efficient. Students should be able to use a variety of mental strategies to multiply by 10, 20, or 300 (or any power of 10 or multiple of 10). Also, students should be able to perform such operations as finding the sum of 199 and 67 or the product of 4 and 26 by using quick mental strategies rather than relying on paper and pencil. Further, situations vary in their need for exact answers. Sometimes an estimate is good enough, as in calculating a tip on a bill at a restaurant. Sometimes using a calculator or computer is more appropriate than using paper and pencil, as in completing a complicated tax form. Hence, students need facility with a variety of computational tools, and they need to know how to select the appropriate tool for a given situation.

Rater guidance for this item bank:
- High when the student must carry out a known procedure accurately on numbers, expressions, or equations that are fully given: compute, evaluate, simplify, convert units with given rates, solve a given equation, apply a formula the item points to, round, or estimate.
- This includes word problems where the operation is obvious and nothing needs to be set up or interpreted.
- Typical items: "Evaluate 5^3 * 2^3."; "Divide: (4/9) ÷ (8/15)."; "Solve 3x + 7 = 22."; "What is 15% of 80?"
- Use this practice for items that feature none of the five NAEP practices.
"""

PROMPT_SCORING = """
---

How to score

For each of the six practices, give a number from 0 to 1: the probability that an expert NAEP item reviewer would say this item assesses that practice.

- Score each practice on its own. The six numbers do not need to add up to 1, and an item can score high on two practices.
- Scale:
  - 0: no evidence; the practice is not involved.
  - 0.1-0.3: incidental; it plays a minor role (e.g. reading one value from a table).
  - 0.4-0.6: substantial, but shared with another practice or only part of what is needed.
  - 0.7-0.9: clearly required to answer the item correctly.
  - 1.0: the item is a textbook example of the practice.
- Most items have one main practice that scores 0.7 or higher, with the others at 0 or low. Some items genuinely combine two practices. Use 0 when there is no evidence; do not spread small scores over every practice because you are unsure.
- At least one practice should normally score 0.5 or higher. If none of the five NAEP practices is clearly involved, the item is almost always Procedural Fluency.
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
        description="Add NAEP mathematical practice probabilities to Problems.csv"
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
    output_jsonl = os.path.join(args.output_dir, RAW_OUTPUT_FILE)

    print(f"Model: {args.model_id}")
    print(f"Problems file: {problems_csv}")
    print(f"Raw output JSONL: {output_jsonl}")
    print(f"Samples per problem: {args.num_samples} ({'greedy' if args.num_samples == 1 else 'sampled, averaged'})")
    if args.dry_run:
        print("DRY RUN: nothing will be written")

    # Read every cell as text so the original columns are written back unchanged
    problems_df = pd.read_csv(problems_csv, dtype=str, keep_default_na=False)
    if OUTPUT_COLUMN not in problems_df.columns:
        problems_df[OUTPUT_COLUMN] = ''
    skill_names = load_skill_names(skill_csv)

    if args.overwrite:
        todo = list(problems_df.index)
    else:
        todo = list(problems_df.index[problems_df[OUTPUT_COLUMN].str.strip() == ''])
    print(f"\nProblems: {len(problems_df)}, needing labels: {len(todo)}")
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

    if args.num_samples == 1:
        sampling_params = SamplingParams(n=1, **GREEDY_SAMPLING)
    else:
        sampling_params = SamplingParams(n=args.num_samples, **STOCHASTIC_SAMPLING)
    retry_params = SamplingParams(n=1, **STOCHASTIC_SAMPLING)

    if not args.dry_run:
        backup_csv = problems_csv + '.bak'
        if not os.path.exists(backup_csv):
            shutil.copy2(problems_csv, backup_csv)
            print(f"Backed up original to {backup_csv}")

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

        if args.dry_run:
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
        else:
            save_problems_csv(problems_df, problems_csv)
            append_results_jsonl(records, output_jsonl)
            print(f"Saved {len(records)} results to {problems_csv} and {output_jsonl}")

    print(f"\n{'='*80}")
    print(f"Labeled: {labeled}, failed to parse: {failed}, skipped (too long): {len(too_long)}")
    if failed or too_long:
        print("Re-run the script to retry the rows that are still empty.")
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
