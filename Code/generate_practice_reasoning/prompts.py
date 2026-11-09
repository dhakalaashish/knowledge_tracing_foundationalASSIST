"""Every prompt used by generate.py: two system prompts and two user prompts.

The practice definitions and descriptors are copied verbatim from SYSTEM_PROMPT in
Code/augment_mathematical_practice.py (only the '(JSON key: ...)' tags after each practice name were
removed, since the answers here use the practice names). Both prompts contain them. The two
questions are the ones used for the claude_practice_reasoning / claude_top_practice columns.

Each problem goes through two separate LLM calls (two fresh conversations, not one chat):

    Prompt 1 (practice order)
        system: SYSTEM_PROMPT_1
        user:   Q1_TEMPLATE with the problem in place of {PROBLEM}
        model:  answer 1, a JSON object: the practices used, in order, with why; the practices not
                used, with why. Checked with a JSON parser and the rules in PROMPT_RESPONSE_1.

    Prompt 2 (top practice), only after answer 1 passed the check
        system: SYSTEM_PROMPT_2
        user:   Q2_TEMPLATE with the problem in place of {PROBLEM} and answer 1 (the checked JSON,
                indented) in place of {ANALYSIS}
        model:  answer 2, a JSON object: the top practice and why. Checked the same way.
"""

PRACTICES = [
    "Representing",
    "Abstracting and Generalizing",
    "Justifying and Proving",
    "Mathematical Modeling",
    "Collaborative Mathematics",
    "Procedural Fluency",
]

INTRO_1 = """You are an expert in mathematics assessment. You have years of experience reviewing test items and deciding which mathematical practices each item assesses.

Your task: read ONE item from an online k-12 mathematics item bank and work out which practices a student needs to use to solve it, in which order, and why; and which practices the item does not use, and why.

"""

INTRO_2 = """You are an expert in mathematics assessment. You have years of experience reviewing test items and deciding which mathematical practices each item assesses.

Your task: you will be given ONE item from an online k-12 mathematics item bank, together with an analysis of it: the practices a student uses to solve the item, in order, with the reason for each, and the practices the item does not use, with the reason for each. Use the item and the analysis to choose the single practice the item mainly assesses (the top practice), and explain why it is the top practice.

"""

PROMPT_CONTEXT = """---

Assess the item's practices using:
    - Practice definition: defines what the practice measures
    - Practice descriptors: non-comprehensive list of descriptions of what the practice could entail
Both the definition and the descriptor are important in identifying which practice the item belongs to

---

About the items

- A student works on each item alone. Practices that involve other people therefore appear through the item itself: the item shows another person's mathematical thinking (a named student's claim, strategy, answer, work, or a dialogue), and the student responds to it.
- Figures appear only as text descriptions such as [Image: ...], or as [image] when no description is available. Judge from what the text shows.
- Answer blanks appear as ____. For multiple-choice items the answer choices are listed; the correct answer is not shown.

---

The six practices:

"""

PROMPT_REPRESENTING = """
===
1. Representing

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
2. Abstracting and Generalizing

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
3. Justifying and Proving

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
4. Mathematical Modeling

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
5. Collaborative Mathematics

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
6. Procedural Fluency

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

PROMPT_RESPONSE_1 = """
---

How to respond

Base the answer on what the student must do to produce the correct answer to this item, not on what a teacher could do with it or on the lesson it came from. Write the practice names exactly as: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, Procedural Fluency.

- Work through how a student solves the item, step by step, and decide which practices the steps require.
- Put each practice the student uses in "practices_used", in the order the student first needs it ("order": 1, 2, 3, ...). If a practice is needed at several points, list it once, at the point where it is first needed. Say why each practice is used: what the student does at that step, and which part of the practice definition or descriptors it matches.
- Put each remaining practice in "practices_not_used", and say why the item does not call for it.
- Each of the six practices must appear exactly once, either in "practices_used" or in "practices_not_used". "practices_used" must contain at least one practice.

Respond with exactly one JSON object in this form, and write nothing before or after it:

{
"practices_used": [
  {"order": 1, "practice": "<practice name>", "why": "<1-3 sentences: what the student does at this step and why that is this practice>"},
  {"order": 2, "practice": "<practice name>", "why": "<...>"}
],
"practices_not_used": [
  {"practice": "<practice name>", "why": "<1-2 sentences: why the item does not call for this practice>"}
]
}"""

PROMPT_RESPONSE_2 = """
---

How to respond

Base the answer on what the student must do to produce the correct answer to this item, not on what a teacher could do with it or on the lesson it came from. Write the practice names exactly as: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, Procedural Fluency.

- Read the item and the analysis. The analysis lists the practices the student uses, in order, and the practices the item does not use, each with a reason.
- Choose the single practice the item mainly assesses: the practice that carries the main demand of the item, the one a student most needs in order to answer it correctly. It must be one of the practices in the analysis's "practices_used" list.
- A practice is not the top practice just because it comes first or last in the order. Weigh what each used practice contributes to solving the item, using the reasons in the analysis and the practice definitions and descriptors. When two practices seem equally strong, choose the one that best matches the practice definitions.
- Explain why this practice is the top practice: what in the item makes it the main demand, and why it outweighs each of the other practices used.

Respond with exactly one JSON object in this form, and write nothing before or after it:

{
"top_practice": "<exactly one of: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, Procedural Fluency>",
"why": "<2-4 sentences: why this practice is the top practice of the item, and why it outweighs the other practices used>"
}"""

PRACTICE_DEFINITIONS = (
    PROMPT_CONTEXT
    + PROMPT_REPRESENTING
    + PROMPT_ABSTRACTING
    + PROMPT_JUSTIFYING
    + PROMPT_MODELING
    + PROMPT_COLLABORATIVE
    + PROMPT_PROCEDURAL
)

# Prompt 1: practice order, with reasons, and the practices not used.
SYSTEM_PROMPT_1 = INTRO_1 + PRACTICE_DEFINITIONS + PROMPT_RESPONSE_1

# Prompt 2: the top practice, from the item and answer 1.
SYSTEM_PROMPT_2 = INTRO_2 + PRACTICE_DEFINITIONS + PROMPT_RESPONSE_2

# User prompt 1: question 1 with the rendered problem text in place of {PROBLEM}.
# Placeholders are filled with str.replace, because problem texts contain braces.
Q1_TEMPLATE = """Look at the Math NAEP practices, and then tell me which practices needs to be used in which order to solve this problem. Also add "procedural fluency" from NRC as one of the practice:

{PROBLEM}"""

# User prompt 2: the problem, answer 1 (the checked JSON object, indented) and question 2.
Q2_TEMPLATE = """Item:

{PROBLEM}

Analysis of the practices this item uses:

{ANALYSIS}

If you had to choose one as the major practice, which one would you choose?"""
