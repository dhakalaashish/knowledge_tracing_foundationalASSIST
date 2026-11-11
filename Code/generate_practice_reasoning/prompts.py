"""Every prompt used by generate.py: three system prompts and three user prompts.

The practice definitions and descriptors are copied verbatim from SYSTEM_PROMPT in
Code/augment_mathematical_practice.py (only the '(JSON key: ...)' tags after each practice name were
removed, since the answers here use the practice names). All three system prompts contain them, and every
user prompt asks the model to use them.

Each problem goes through three separate LLM calls (three fresh conversations, not one chat):

    Prompt 1 (practices used and not used)
        system: SYSTEM_PROMPT_1
        user:   Q1_TEMPLATE with the problem in place of {PROBLEM}
        model:  answer 1, a JSON object: the practices used, in order, with why and likely errors; the
                practices not used, with why. Checked with a JSON parser and the rules in PROMPT_RESPONSE_1.

    Prompt 2 (practice order), only after answer 1 passed the check
        system: SYSTEM_PROMPT_2
        user:   Q2_TEMPLATE with the problem in place of {PROBLEM} and the practices answer 1 lists as
                used, in the fixed order of PRACTICES (not answer 1's order), each with answer 1's "why",
                in place of {PRACTICES}
        model:  answer 2, a JSON object: the same practices in the order a student uses them, with what
                the student does at each step, and why the steps come in this order. Checked the same way.

    Answer 1 is then reordered as answer 2 says ("combined analysis": answer 1's practices_used in
    answer 2's order, renumbered, with answer 1's why and likely_errors; practices_not_used unchanged).

    Prompt 3 (top practice), only after answer 2 passed the check
        system: SYSTEM_PROMPT_3
        user:   Q3_TEMPLATE with the problem in place of {PROBLEM} and the combined analysis (JSON,
                indented) in place of {ANALYSIS}
        model:  answer 3, a JSON object: the top practice and why. Checked the same way.

Example items: below each practice's descriptors are example items from Data/problems_naep_predicted.csv
(its ground_truth column), rendered like the problems (tools/render_problems.awk; no answers): all 4 / 4 / 7 /
3 / 4 items of Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling and
Collaborative Mathematics, and 4 of the 14 Procedural Fluency items (data rows 23, 30, 25, 26: whole-number
subtraction across zeros, multi-digit multiplication, a signed decimal division, a linear equation).
The NAEP items are not in Problems.csv.

Apart from the example items, prompt 1 and prompt 3 are the same text as prompt 1 and prompt 2 of the
two-prompt version (run qwen3_30b_v2), and run qwen3_30b_v3 used these prompts without the examples.
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

Your task: read ONE item from an online k-12 mathematics item bank and work out which practices a student needs to use to solve it, in which order, how the student uses each one, and what a student could get wrong at each step; and which practices the item does not use, and why.

"""

INTRO_2 = """You are an expert in mathematics assessment. You have years of experience reviewing test items and deciding which mathematical practices each item assesses.

Your task: you will be given ONE item from an online k-12 mathematics item bank, together with the practices a student uses to solve it, each with how the student uses it. Put these practices in the order in which a student working on the item uses them, from the first step to the last, say what the student does at each step, and explain why the steps come in this order.

"""

INTRO_3 = """You are an expert in mathematics assessment. You have years of experience reviewing test items and deciding which mathematical practices each item assesses.

Your task: you will be given ONE item from an online k-12 mathematics item bank, together with an analysis of it: the practices a student uses to solve the item, in order, with how each is used and what a student could get wrong at that step, and the practices the item does not use, with the reason for each. Use the item and the analysis to choose the top practice: the practice where the item's difficulty lies, the one a student who answers incorrectly most likely failed at. Explain why it is the top practice.

"""

PROMPT_CONTEXT = """---

Assess the item's practices using:
    - Practice definition: defines what the practice measures
    - Practice descriptors: non-comprehensive list of descriptions of what the practice could entail
    - Example items: items from the NAEP mathematics framework whose main practice is this practice (shown without their answers)
Both the definition and the descriptor are important in identifying which practice the item belongs to. The example items show what an item that mainly assesses the practice looks like; an item can still use other practices along the way.

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

Example items:

Example 1:
    [Image: base ten blocks: 3 large cubes (each made of 10 × 10 × 10 small cubes), 2 rods (each made of 10 small cubes), and 5 single small cubes. Key: one small cube = 1]
    Which of the following numbers is represented by the base ten blocks?

    Answer choices:
    A. 325
    B. 370
    C. 3,025
    D. 3,205

Example 2:
    [Graph: MARISA’S BICYCLE TRIP. Horizontal axis: Time (minutes), 0 to 80. Vertical axis: Speed (miles per hour), 0 to 10. The speed rises steadily from 0 mph at 0 minutes to 6 mph at 20 minutes, stays at 6 mph from 20 to 60 minutes, drops to 0 mph at about 65 minutes, and stays at 0 mph after that.]
    The graph above represents Marisa’s riding speed throughout her 80-minute bicycle trip. Use the information in the graph to describe what could have happened on the trip, including her speed throughout the trip.
    During the first 20 minutes, Marisa ____
    From 20 minutes to 60 minutes Marisa ____
    From 60 minutes to 80 minutes Marisa ____

Example 3:
    Chris and Ben each walked home from school. The distance Chris walked, in miles, is represented by point C on the number line.
    [Image: a number line from 0 to 1 divided into 8 equal parts; point C is at the 6th tick mark after 0.]
    Ben walked 1/4 mile less than Chris.
    Enter the distance, in miles, that Ben walked.
    ____

Example 4:
    Which situation can be represented by this equation?
    4 ÷ (1/8) = ☐

    Answer choices:
    A. Jack has 4 pieces of fabric. Each piece is 1/8 of a yard long. How many yards of fabric does Jack have?
    B. Jack has 4 pieces of fabric. He gets 1/8 more yards of fabric. How many yards of fabric does Jack have now?
    C. Jack has 4 yards of fabric. He gives away 1/8 of his pieces of fabric. How many pieces of fabric does Jack have left?
    D. Jack has 4 yards of fabric. He cuts the fabric into 1/8 pieces of a yard long. How many pieces of fabric does Jack have?
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

Example items:

Example 1:
    Point O is the center of the regular hexagon shown. The shaded triangle is formed by O and two adjacent vertices of the hexagon and has an area of T.
    [Image: a regular hexagon with center O; the triangle formed by O and the two bottom vertices is shaded.]
    What is the area of the hexagon in terms of T?
    Area = ____

Example 2:
    Point P is the center of a regular polygon with 10 sides. A triangle is formed by P and two adjacent vertices of the polygon and has an area of V.
    What is the area of the polygon in terms of V?
    Area = ____

Example 3:
    Sequence I: 3, 5, 9, 17, 33, ...
    Sequence I, shown above, is an increasing sequence. Each term in the sequence is greater than the previous term.
    a. Make a list of numbers that consists of the positive differences between each pair of adjacent terms in Sequence I. Label the list Sequence II.
    b. If this same pattern of differences continues for the terms in Sequence I, what are the next two terms after 33 in Sequence I?
    6th term ____
    7th term ____
    c. Write an algebraic expression (rule) that can be used to determine the nth term of Sequence II, which is the difference between the (n + 1)st term and the nth term of Sequence I.

Example 4:
    Three students each have a coin, one has a nickel, one has a dime, and the third student has a quarter. They flip their coins at the same time. Each coin can land either heads up (H) or tails up (T). List all the different possible outcomes for how the coins could land in the chart below. The list has been started for you.
    [Table:
    Nickel | Dime | Quarter
    H | H | H
    H | H | T]
    What if a 4th student joins the group with a half-dollar coin? How many different ways could the 4 coins land? What if a 5th student joined with a penny, how many different ways could the 5 coins land?

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

Example items:

Example 1:
    Elise claims that if you multiply any whole number by 6, you will always get an even number for the answer. Provide an argument for why Elise is correct.

Example 2:
    [Figure: segment BE is horizontal, with point C on it between B and E. Segment AD crosses BE at C. Point A is below B, and AB is perpendicular to BE (right angle at B). Point D is above E, and DE is perpendicular to BE (right angle at E).]
    Given: C is the midpoint of segment BE. ∠B and ∠E are right angles.
    Prove that segment AC ≅ segment DC and give a reason for each statement in your proof.

Example 3:
    Question A: If x is a real number, what are all values of x for which x > −3 and x < 5?
    Question B: If x is a real number, what are all values of x for which x > −3 or x < 5?
    Barbara said that the answers to the two questions above are different.
    Dave said that the answers to the two questions above are the same.
    Which student is correct?
    Explain why this student is correct. You may use words, symbols, or graphs in your explanation.

    Answer choices:
    A. Barbara
    B. Dave

Example 4:
    Tracy said, “I can multiply 6 by another number and get an answer that is smaller than 6.”
    Pat said, “No, you can’t. Multiplying 6 by another number always makes the answer 6 or larger.”
    Who is correct? Give a reason for your answer.

Example 5:
    A student was asked to use mathematical induction to prove the following statement.
    1/2 + 1/4 + 1/8 + ... + (1/2)^n = 1 − (1/2)^n for all positive integers n
    The beginning of the student’s proof is shown below.
    First, show that the statement is true for n = 1: If n = 1, (1/2)^1 = 1 − (1/2)^1, so 1/2 = 1/2.
    Next, show that if the statement is true when n is equal to a given positive integer k, then it is also true when n is equal to the next integer, k + 1: Assume that the statement is true when n = k, so 1/2 + 1/4 + 1/8 + ... + (1/2)^k = 1 − (1/2)^k. Show that the statement is also true when n is equal to the next integer, k + 1.
    Complete the student’s proof by showing that if the statement is true when n = k, then it is also true when n = k + 1, where k is any positive integer.

Example 6:
    [Image: two spinners. Spinner A is divided into 6 equal sections that alternate blue and white (3 blue, 3 white). Spinner B is divided into 3 equal sections: 1 blue and 2 white.]
    Lori has a choice of two spinners. She wants the one that gives her a greater probability of landing on blue.
    Which spinner should she choose?
    Explain why the spinner you chose gives Lori the greater probability of landing on blue.

    Answer choices:
    A. Spinner A
    B. Spinner B

Example 7:
    From any vertex of a 4-sided polygon, 1 diagonal can be drawn.
    From any vertex of a 5-sided polygon, 2 diagonals can be drawn.
    From any vertex of a 6-sided polygon, 3 diagonals can be drawn.
    From any vertex of a 7-sided polygon, 4 diagonals can be drawn.
    How many diagonals can be drawn from any vertex of a 20-sided polygon?
    Answer: ____

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

Example items:

Example 1:
    [Task is introduced through video: A school food service director states during the morning announcements that the school is planning a “Garden Bar” as an option for school lunch <video/image of a garden bar with a variety of fruits and vegetables>. The director says, “The cafeteria staff and I would like your input, so we know that the fruits and vegetables included will be eaten. To assist us in our decision-making process, we are establishing a task force to help us gather your suggestions and will take your suggestions into account when making our decision.”]
    You volunteer for the task force.
    At the first meeting, the team works to determine what they need to know and how to go about gathering that information. Some of the questions your team identifies are:
    “How many students are in the school? Do students like some of these choices more than others? Do some of these choices cost more than others? If so, which ones might we have some left over, which might we run out of? Should the school’s cost of these items be considered?”

Example 2:
    A state’s tax model is described below.
    - Individuals with an income of $10,000 or less per year pay no income tax.
    - Individuals with income greater than $10,000 per year pay a 6% tax on all income over $10,000.
    (1) What would a resident who made $40,000 pay in tax? What percent of this resident’s total income is paid in tax?
    (2) What would a resident who made $50,000 pay in tax? What percent of this resident’s total income is paid in tax?
    (3) Determine a method for calculating the percent of any resident’s total income that is paid in tax.
    (4) Is there a highest percent of total income that a resident could pay in tax? Defend your position on this percent.
    (5) The state is considering the new tax model described below:
    - Individuals with an income of $10,000 or less per year pay no income tax.
    - Individuals with an income greater than $10,000 per year pay 5% on all income over $10,000 up to $50,000, and pay 7% on all income over $50,000.
    Explain whether or not the new tax model benefits individuals in the state who pay income tax. As part of your response, compare the new tax model to the existing tax model.

Example 3:
    The student council at a large middle school must recommend one activity to add to physical education classes next year. They plan to survey 100 students and ask each to pick a favorite among kickball, tennis, yoga, and dance.
    (a) Write the question you would put on the survey, exactly as it would appear.
    (b) Explain how you would choose the 100 students who answer your question.
    (c) Make a table or graph of survey responses that would be reasonable for this situation.
    (d) Which activity should the student council recommend adding to physical education classes next year? Use your answer to part (c) to justify your choice.

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

Example items:

Example 1:
    Chat members: You, George, Rachel, Brad. The team is choosing a place to take visitors from three options suggested by Ms. Cosmo: the museum of local history, the community market, and the electric car factory. The team’s notepad lists two goals: it gives a sense of life in our town; travel time is manageable.
    Chat so far:
    You: Brad, I agree we want the visitors to enjoy themselves, but let’s go over Ms. Cosmo’s options first.
    George: Not sure. Probably any of the sites would be fine.
    Rachel: The museum of local history would really show what life in our town is like.
    Brad: It’s sort of boring. Also, I think it’s closed.
    [Museum information: Location: 101 Main Street, in the center of town. Hours: Saturday 10 a.m. to 5 p.m., Sunday noon to 5 p.m. On display: clothing, furniture, and room decorations from different periods; antiques donated by local families; maps showing how the town and surrounding areas grew.]
    Choose your next message in the chat.

    Answer choices:
    A. Does this mean we only have two options?
    B. I don’t think it’s closed. I’ve seen ads for the museum all over town.
    C. Rachel, the museum is only open on weekends. Let’s look at the other options.
    D. I don’t see how we can go to the museum if it’s closed.

Example 2:
    You, George, Rachel, and Brad are choosing between the museum of local history, the community market, and the electric car factory for a visit.
    Turn 1. George: OK, where should we begin?
    Choose your message:
    A) Let’s ask Ms. Cosmo what we should do.
    B) There are three choices. Let’s just vote.
    C) Maybe we should think about it for a while and check back later?
    D) Let’s talk about what makes a good visit.
    Turn 2. Brad: We’re supposed to visit someplace local.
    Choose your message:
    A) How does that help? Lots of places are local.
    B) If it’s local, it could show what life is like around here.
    C) OK, but we need to hurry and decide.
    D) Too bad we can’t take them anywhere we want.

Example 3:
    Together, you and Connor are finding 8 × 16.
    Connor says, “We can find the product if we multiply 8 and 15 and then add 8.”
    Which sentence could you say to Connor to best explain that his statement is correct or incorrect?

    Answer choices:
    A. I think you are incorrect, because we should add 16 instead of 8.
    B. I think you are correct, because 15 is an easier number to multiply by than 16.
    C. I think you are correct, because 8 × 16 is the same as 15 groups of 8, plus 1 group of 8.
    D. I think you are incorrect, because 8 × 16 is the same as 4 groups of 8, plus 4 groups of 8.

Example 4:
    You and Jose talk about the number of factors all whole numbers have.
    Jose says that all whole numbers except 1 have an even number of factors because factors always come in pairs.
    Jose’s statement is incorrect.
    Complete the sentences to help Jose see that his statement is not always correct. Drag numbers into the empty boxes to complete the sentences.
    Numbers to drag: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    What about the number ____?
    It has ____ factors.

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

Example items:

Example 1:
    3,020 − 687
    ____

Example 2:
    49 × 975 = ____

Example 3:
    Compute.
    −0.4 ÷ 8 = ____

Example 4:
    Solve each equation or write that there are no solutions or infinitely many solutions. Show your work.
    8(2x + 9) = 56
    x = ____

"""

PROMPT_RESPONSE_1 = """
---

How to respond

Base the answer on what the student must do to produce the correct answer to this item, not on what a teacher could do with it or on the lesson it came from. Write the practice names exactly as: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, Procedural Fluency.

- Work through how a student solves the item, step by step, and decide which practices the steps require.
- Order the steps as the student actually does them. Turning words, a diagram, a table or a graph into a mathematical form (an expression, an equation, a number sentence, a model) comes before computing with that form.
- Put each practice the student uses in "practices_used", in the order the student first needs it ("order": 1, 2, 3, ...). If a practice is needed at several points, list it once, at the point where it is first needed. Say why each practice is used: what the student does at that step, and which part of the practice definition or descriptors it matches.
- For each practice used, say in "likely_errors" what a student could get wrong at that step, and how likely that is for a student. If the step is routine for a fluent student, say so.
- Put each remaining practice in "practices_not_used", and say why the item does not call for it.
- Each of the six practices must appear exactly once, either in "practices_used" or in "practices_not_used". "practices_used" must contain at least one practice.

Respond with exactly one JSON object in this form, and write nothing before or after it:

{
"practices_used": [
  {"order": 1, "practice": "<practice name>", "why": "<1-3 sentences: what the student does at this step and why that is this practice>", "likely_errors": "<1-2 sentences: what a student could get wrong at this step, and how likely that is>"},
  {"order": 2, "practice": "<practice name>", "why": "<...>", "likely_errors": "<...>"}
],
"practices_not_used": [
  {"practice": "<practice name>", "why": "<1-2 sentences: why the item does not call for this practice>"}
]
}"""

PROMPT_RESPONSE_2 = """
---

How to respond

Base the answer on what the student must do to produce the correct answer to this item, not on what a teacher could do with it or on the lesson it came from. Write the practice names exactly as: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, Procedural Fluency.

- The practices are given in a fixed order (the order of the six practices above). That order says nothing about the order of the steps.
- Work through how a student solves the item from start to finish, and put the practices in the order the student first uses them: "order": 1 is the practice the student uses first, "order": 2 the next one, and so on.
- The order is the order in time, not the order of importance or difficulty. The practice the item is mostly about, or the hardest step, can come late.
- A student first has to make sense of the item. Turning words, a diagram, a table or a graph into a mathematical form (an expression, an equation, a number sentence, a model) comes before computing with that form, and checking or defending a result comes after the result is found. Follow the item itself when it works differently.
- If a practice is used at several points, place it where it is first needed.
- Use exactly the practices you are given, each once. Do not add or drop a practice.
- For each practice, say in "step" what the student does at that step. In "why", explain why the steps come in this order.

Respond with exactly one JSON object in this form, and write nothing before or after it:

{
"ordering": [
  {"order": 1, "practice": "<practice name>", "step": "<1 sentence: what the student does at this step>"},
  {"order": 2, "practice": "<practice name>", "step": "<...>"}
],
"why": "<1-3 sentences: why the steps come in this order>"
}"""

PROMPT_RESPONSE_3 = """
---

How to respond

Base the answer on what the student must do to produce the correct answer to this item, not on what a teacher could do with it or on the lesson it came from. Write the practice names exactly as: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, Procedural Fluency.

- Read the item and the analysis. The analysis lists the practices the student uses, in order, with how each is used ("why") and what a student could get wrong at that step ("likely_errors"), and the practices the item does not use, each with a reason.
- The top practice is the step where the item's difficulty lies: the practice a student who answers the item incorrectly most likely failed at. Compare the "likely_errors" of the practices used, check them against the item, and choose the practice whose step is hardest for a student. It must be one of the practices in the analysis's "practices_used" list.
- A practice is not the top practice just because it comes first or last in the order, or because the analysis says the most about it. When two practices seem equally hard, choose the one that best matches the practice definitions.
- Explain why this practice is the top practice: what a student is likely to get wrong at this step, and why the other practices used are less likely to cause an incorrect answer.

Respond with exactly one JSON object in this form, and write nothing before or after it:

{
"top_practice": "<exactly one of: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, Procedural Fluency>",
"why": "<2-4 sentences: where a student is most likely to go wrong in this item, why that step is this practice, and why the other practices used are less likely to cause an incorrect answer>"
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

# Prompt 1: the practices used (in order, with reasons and likely errors) and the practices not used.
SYSTEM_PROMPT_1 = INTRO_1 + PRACTICE_DEFINITIONS + PROMPT_RESPONSE_1

# Prompt 2: the order of the practices used, from the item and the practices answer 1 lists as used.
SYSTEM_PROMPT_2 = INTRO_2 + PRACTICE_DEFINITIONS + PROMPT_RESPONSE_2

# Prompt 3: the top practice, from the item and answer 1 reordered as answer 2 says.
SYSTEM_PROMPT_3 = INTRO_3 + PRACTICE_DEFINITIONS + PROMPT_RESPONSE_3

# Placeholders are filled in one pass by common.fill (not str.format: problem texts contain braces).

# User prompt 1: the question, then the rendered problem text in place of {PROBLEM}.
Q1_TEMPLATE = """Using the practice definitions and descriptors, tell me which practices a student needs to use to solve this item, in the order the student uses them, how the student uses each one, and what a student could get wrong at each step. Then tell me which practices the student does not use, and why.

Item:

{PROBLEM}"""

# User prompt 2: the problem, the practices answer 1 lists as used in place of {PRACTICES} (one line each,
# "- <practice>: <answer 1's why>", in the fixed order of PRACTICES), then the question.
Q2_TEMPLATE = """Item:

{PROBLEM}

Practices a student uses to solve this item, each with how the student uses it (listed in a fixed order, not in the order of the steps):

{PRACTICES}

Using the practice definitions and descriptors, put these practices in the order in which a student working on this item uses them, from the first step to the last. Say what the student does at each step, and explain why the steps come in this order."""

# User prompt 3: the problem, the combined analysis (answer 1 reordered as answer 2 says; JSON, indented)
# in place of {ANALYSIS}, then the question.
Q3_TEMPLATE = """Item:

{PROBLEM}

Analysis of the practices a student uses to solve this item:

{ANALYSIS}

Using the practice definitions and descriptors and this analysis, tell me which single practice is the top practice of this item: the step where the item's difficulty lies, the one a student who answers incorrectly most likely failed at. Explain why it is the top practice and why the other practices the student uses are less likely to cause an incorrect answer."""


# =====================================================================================================================
# Prompt 4: diagnosis of one wrong answer (used by diagnose.py)
# =====================================================================================================================

INTRO_4 = """You are an expert in mathematics assessment. You have years of experience reviewing test items, deciding which mathematical practices each item assesses, and reading students' wrong answers to work out where their thinking went wrong.

Your task: you will be given ONE item from an online k-12 mathematics item bank, its correct answer, an analysis of the practices a student uses to solve it (in order, with how each is used and what could go wrong), and ONE wrong answer that several students gave on their first attempt. Work out how a student most likely arrived at this wrong answer: which practice steps the student carried out correctly, at which step the student went wrong, and which steps the student never got to.

"""

PROMPT_RESPONSE_4 = """
---

How to respond

Base the answer on what a student would have to do to produce exactly this wrong answer. Write the practice names exactly as: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, Procedural Fluency.

- First find a "reconstruction": the calculation or line of reasoning that turns the item into this wrong answer (for example "3 × 9 = 27: used 9 as the time instead of the distance"). Prefer the simplest process that produces exactly this answer. If no reasonable process produces it, write "none".
- Then give a status for every practice in the analysis's "practices_used", in the same order:
  - "correct": the student carried out this step correctly. A step done correctly on a wrong earlier result is still "correct" (for example, multiplying correctly after setting up the wrong equation).
  - "failed": the student went wrong at this step.
  - "not_reached": the answer shows the student stopped before doing this step (for example, an intermediate result was given as the final answer).
  - "cannot_tell": the wrong answer gives no evidence about this step.
- Choose the "error_type":
  - "practice": the student went wrong in a practice itself: for example set up the wrong representation, modeled the wrong quantity, applied a rule to the wrong cases, or slipped in carrying out a procedure. At least one step is "failed".
  - "math_fact": the error comes from a wrong or missing mathematical fact: a definition or term (coefficient, variable, radius), notation (reading 6^2 as 6 × 2), a convention (order of operations), a number fact, a unit or conversion, a constant or a formula. Name the fact in "math_fact". Mark the step where the wrong fact was used as "failed".
  - "guess": no reasonable process produces this answer from the item (a random or unrelated answer, or a guess among the choices). No step is "failed"; use "cannot_tell" or "not_reached".
- Wrong answers are written as the student entered them, in lower case. For multiple-choice items the answer is the text of the chosen option(s); for ordering items it is the items in the student's order, separated by commas. An item with several blanks may have its answers joined by commas.

Respond with exactly one JSON object in this form, and write nothing before or after it:

{
"reconstruction": "<the calculation or reasoning that produces this wrong answer, or \\"none\\">",
"steps": [
  {"practice": "<practice name>", "status": "<correct | failed | not_reached | cannot_tell>", "why": "<1 sentence>"}
],
"error_type": "<practice | math_fact | guess>",
"math_fact": "<for math_fact: the fact the student got wrong, e.g. \\"6^2 means 6 × 6, not 6 × 2\\"; otherwise an empty string>",
"explanation": "<1-3 sentences: how the student most likely arrived at this answer>",
"confidence": "<high | medium | low>"
}"""

SYSTEM_PROMPT_4 = INTRO_4 + PRACTICE_DEFINITIONS + PROMPT_RESPONSE_4

# User prompt 4: the problem, its correct answer, the analysis (answer 1 in the order of answer 2, JSON), the wrong answer.
Q4_TEMPLATE = """Item:

{PROBLEM}

Correct answer: {CORRECT}

Analysis of the practices a student uses to solve this item:

{ANALYSIS}

Wrong answer: {WRONG}
({COUNT} students gave this answer on their first attempt, {SHARE} of the item's wrong answers.)

Using the practice definitions and descriptors and this analysis, tell me how a student most likely arrived at this wrong answer: which practice steps the student did correctly, at which step the student went wrong, and which steps the student did not get to."""


# =====================================================================================================================
# NAEP Chapter 3 version (--framework naep_ch3)
# =====================================================================================================================
# The full text of Chapter 3 of the NAEP 2026 Mathematics Framework ("NAEP Mathematical Practices", made with
# tools/naep_chapter_text.js into naep_chapter3.txt) is put in front of every system prompt. The rest of each system
# prompt is unchanged, so the answers use the same six practices and formats. Putting the chapter first gives all
# prompts the same long prefix, which vLLM's prefix cache reuses across every call.

CHAPTER_INTRO = """Background reading: below is the full text of Chapter 3, "NAEP Mathematical Practices", of the Mathematics Framework for the 2026 National Assessment of Educational Progress (NAEP). It explains in depth what each NAEP mathematical practice means, how the practices differ from each other and from conceptual understanding and computational fluency, and gives example items with the practices they assess. The text was extracted from the PDF: figures are missing, tables are flattened into lines, and some item text from images may be garbled.

Use the chapter to understand each practice in depth. For your answer, use the six practices, definitions and descriptors given after the chapter. Five of them are the NAEP practices; the sixth, Procedural Fluency, is not a NAEP practice: it comes from the strands of mathematical proficiency of the National Research Council (Adding It Up, 2001) and covers the computational and procedural work that the chapter calls computational or procedural fluency.

<naep_chapter_3>
"""

CHAPTER_OUTRO = """
</naep_chapter_3>

---

"""

FRAMEWORKS = ("standard", "naep_ch3")


def system_prompts(framework="standard", chapter_text=None):
    """The four system prompts for a framework: {1: ..., 2: ..., 3: ..., 4: ...}."""
    base = {1: SYSTEM_PROMPT_1, 2: SYSTEM_PROMPT_2, 3: SYSTEM_PROMPT_3, 4: SYSTEM_PROMPT_4}
    if framework == "standard":
        return base
    if framework != "naep_ch3":
        raise ValueError(f"unknown framework {framework!r}; use one of {FRAMEWORKS}")
    if not chapter_text or len(chapter_text) < 10000:
        raise ValueError("the naep_ch3 framework needs the chapter text (naep_chapter3.txt)")
    prefix = CHAPTER_INTRO + chapter_text.strip() + CHAPTER_OUTRO
    return {k: prefix + v for k, v in base.items()}
