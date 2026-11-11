# Which practice, done wrong, produces the common wrong answer? (rows 1–300, Claude's labels)

**Question.** For a problem, the common wrong answer (a "distractor") often comes from a student who did every step right except one. If that one step is always the same practice, practices are tied to incorrect answers. Is the step that fails the problem's top practice?

**Data**
- The first 300 rows of `Data/Problems.csv`, with Claude's ordering and top practice (`Data/problems_300.csv`).
- Responses are students' first attempts from the cleaned MACA-CD data. Wrong answers count only when the student used no hint and did not view the answer, because otherwise the logged text is not their first answer. A "wrong" answer equal to the correct one is dropped.
- 255 of the 299 distinct problems have 30 or more responses. 166 have 30 or more typed wrong answers.

**Question types.** Rows 1–300 contain no multiple-choice or select-all problems. They have 291 fill-in problems (268 numeric) and 9 ordering problems, and one fill-in is a Yes/No dropdown. The analysis therefore uses:
- **the ordering problems**, where a wrong order is a distractor;
- **numeric fill-ins**, where the most common wrong number works like a distractor, because it is what most failing students wrote.

The multiple-choice problems are all later in Problems.csv, where Claude's labels don't exist yet.

**Method.** For each problem with a dominant wrong answer, I worked out what a student must have done to produce it. I then named the step that went wrong and the steps done right, and compared that step with Claude's top practice. This coding is my own judgment, by a single coder, so treat it as a careful reading, not a measurement.

## Short answer

**Yes: in most of these problems the common wrong answer comes from one practice failing while the others succeed.** The failing step is usually Claude's top practice (20 of the 25 problems examined below).

The kind of wrong answer is typical of the practice:

| Practice that fails | What the student does right | What goes wrong | Typical distractor |
|---|---|---|---|
| **Representing** | the arithmetic | the setup: which quantity is which, which way a ratio or scale goes, what the question asks for | a correct computation on the wrong setup (27 instead of 3; 1.25 instead of 0.8; 15.99 instead of 0.99) |
| **Mathematical Modeling** | each calculation | which event or quantity the model should end with | the answer to a neighbouring question (cookies sold instead of left; spins on A instead of not A) |
| **Abstracting and Generalizing** | the setup and the arithmetic | the rule being extended, e.g. area scales with the square of the scale factor | the linear version (1/5 instead of 1/25; 6 instead of 36) |
| **Procedural Fluency** | the setup | one step of the procedure: sign, decimal point, exponent | a near-miss of the right number (6 for −6; 0.6 for 0.06; 182 for 18.2) |

This shows in the numbers too. On problems whose top practice is **Representing** or **Modeling**, the most common wrong answer takes **36–40%** of all wrong answers, against **27–28%** on Procedural and Abstracting problems. A wrong setup sends many students to the *same* wrong number, while procedural slips scatter. Among the 166 problems with 30 or more typed wrong answers, 46 have one wrong answer that takes at least 40% of the wrong answers.

## The 25 problems examined

"Share" is the share of typed wrong answers (first attempt, no help) that are this distractor.

| Row | Problem (short) | Correct | Common wrong answer (share) | What the student did | Practice that failed | Done right | Claude's top | Match |
|---:|---|---|---|---|---|---|---|:-:|
| 65 | d = 3t: minutes to get 9 inches from the rock | 3 | 27 (72%) | put 9 in for t instead of d | Representing (which variable is which) | multiplying | REP | ✓ |
| 70 | Constant of proportionality, sale dollars per original dollar | 0.8 | 1.25 (62%) | divided original by sale: the ratio upside down | Representing (direction of the rate) | dividing | REP | ✓ |
| 289 | 8 is 32 times what number? | 1/4 | 4 (89%) | 32 ÷ 8 instead of 8 ÷ 32 | Representing (the multiplicative comparison) | dividing | REP | ✓ |
| 258 | For 2n − 3 = 7, what is the variable? | n | 5 (74%) | solved the equation instead of naming the variable | Representing (what is asked) | solving | REP | ✓ |
| 223 | What is the coefficient of the variable? (equation in an earlier part) | 2 | 5 (79%) | solved for the variable instead | Representing (what is asked) | solving | PF | ✗ |
| 260 | Sales tax at 6.6% on a $15 meal | 0.99 | 15.99 (51%) | gave the total cost, not the tax | Representing (what is asked) | percent computation | REP | ✓ |
| 84 | Snail: 10 cm in 4 min; minutes for 24 cm | 9.6 | 60 (47%) | 24 × 10 ÷ 4: used cm per minute where minutes per cm was needed | Representing (rate units) | multiplying, dividing | REP | ✓ |
| 234 | 3 days for 1/2 apple; days for 3 apples | 18 | 6 (52%) | found the 6 half-apples, never multiplied by 3 days | Representing (setting up the rate) | dividing by 1/2 | REP | ✓ |
| 236 | Scale factor from R to T (R→S ×3, S→T ×2) | 6 | 1/6 (54%) | reversed the direction | Representing (direction of scaling) | combining factors | REP | ✓ |
| 242 | Scale factor from S to R | 1/3 | 3 (55%) | reversed the direction | Representing (direction) | — | REP | ✓ |
| 235 | Scale factor from T to S | 1/2 | 2 (56%) | gave the forward factor S→T | Representing (direction) | — | A&G | ✗ |
| 178 | Used 7/8 lb of a 1 3/4 lb box: what fraction? | 1/2 | 2 (43%) | 1 3/4 ÷ 7/8: whole divided by part | Representing (which quantity is the whole) | fraction division | MOD | ✗ |
| 240 | 80 spins: about how many not on A? | 60 | 20 (82%) | expected count for A, not for "not A" | Modeling (the event to count) | probability × trials | MOD | ✓ |
| 244 | 125% of 64 cookies made, 90% sold: how many left? | 8 | 72 (55%) | gave the number sold, not left | Modeling (which quantity answers the question) | both percent steps | PF | ✗ |
| 22 | Order by how many fit in a 1-ft stack: pennies, dollar bills, bread, books | books < bread < pennies < bills | bills, pennies, bread, books (43%) | ordered by how thick the item is, the inverse of how many fit | Modeling (thinner item → more in the stack) | knowing the sizes | MOD | ✓ |
| 241 | Scale factor 5: A's area as a fraction of B's | 1/25 | 1/5 (63%) | scaled area like length | Abstracting (area scales with k²) | direction (A smaller) | A&G | ✓ |
| 115 | Photo enlarged ×6: how many times the area? | 36 | 6 (65%) | scaled area like length | Abstracting (k²) | — | A&G | ✓ |
| 268 | Without calculating, order 426÷70, 42.6÷70, 42.6÷0.7, 42.6÷0.07 | 42.6÷70 < 426÷70 < 42.6÷0.7 < 42.6÷0.07 | 426÷70 first, then 42.6÷70 … (26%); full reverse (21%) | the effect of a 10× larger dividend, or of a smaller divisor, turned around | Abstracting (how quotients change) | ordering the rest | A&G | ✓ |
| 23 | Order states by lowest elevation (−282, −8, 2,842, 3,099, 3,350) | CA, LA, NM, WY, CO | greatest to least (36% with both spellings); LA before CA (13%) | the direction was flipped, or negatives were ordered by size, not by position on the number line | Representing (the meaning of "least" and of negative numbers) | ordering the positives | PF | ✗ |
| 64 | (−1)(−2)(−3) | −6 | 6 (90%) | three negatives treated as positive | Procedural (sign rule) | multiplying | PF | ✓ |
| 291 | −5.7 + (−4.2) | −9.9 | 9.9 (63%) | dropped the sign | Procedural (adding negatives) | adding | PF | ✓ |
| 159 | (−0.2)(−0.3) | 0.06 | 0.6 (67%) | misplaced the decimal point | Procedural (decimal places in a product) | sign | PF | ✓ |
| 122 | 2 · 6² | 72 | 24 (47%) | read 6² as 6 × 2 | Procedural (exponents) | — | PF | ✓ |
| 230 | 109.2 ÷ 6 | 18.2 | 182 (46%) | lost the decimal point | Procedural (decimal division) | dividing | PF | ✓ |
| 290 | 5x + 1/4 = 61/4 | 3 | 12 (53%) | (61 − 1) ÷ 5, ignoring the fourths | Procedural (operating on fractions) | inverse operations | PF | ✓ |

**20 of 25 match Claude's top practice.** In the five that don't, the distractor points to a setup practice (Representing or Modeling) where Claude chose Procedural or another practice:
- **Row 244:** Claude names the 72 "sold instead of left" trap in its own reasoning, but rates it a "close second". The data says it is the main error: 55% of wrong answers.
- **Row 23:** Claude predicted the absolute-value error (13% of wrong answers). The data shows that flipping the direction is more common (36%).
- **Rows 223, 235, 178:** "solve instead of name", "forward instead of reverse scale factor" and "whole divided by part" are setup errors, not computation or generalization errors.

## A few examples in detail

**Row 65: Representing fails, Procedural works.** *"The equation d = 3t represents the distance (d) in inches a snail is from a rock and the time (t) in minutes. How many minutes does it take the snail to get 9 inches from the rock?"* The answer is 3. Of the students who answered wrong without help, 72% wrote **27**: they put 9 in for *t* and multiplied (3 × 9). The multiplication is right; reading 9 as a time instead of a distance is the error. This is Claude's top practice, Representing.

**Row 244: Modeling fails, Procedural works.** *"Noah was assigned to make 64 cookies. He made 125% of that number. 90% of the cookies he made were sold. How many were left?"* The answer is 8. 55% of wrong answers are **72**: 125% of 64 = 80 and 90% of 80 = 72 were both done correctly, but the student reported the cookies sold. Claude rated Procedural Fluency as the top practice and named this trap as a close second. The data says the trap is the main reason for errors.

**Row 241: Abstracting fails, Representing works.** *"Polygon B is a scaled copy of Polygon A with scale factor 5. Polygon A's area is what fraction of Polygon B's area?"* The answer is 1/25. 63% of wrong answers are **1/5**. The student read the direction right (A is the smaller one, so the answer is a fraction), but applied the length factor to area instead of squaring it, which is the generalization the item tests.

**Row 64: Procedural fails, the setup is trivial.** *"Evaluate (−1) · (−2) · (−3)."* 90% of wrong answers are **6**. The multiplication 1 · 2 · 3 is right, and the sign rule for an odd number of negatives is not.

**Row 22 (ordering): Modeling fails.** *"Order from smallest to largest the number of pennies / dollar bills / slices of bread / books in a stack 1 ft high."* 43% of wrong orders are bills, pennies, bread, books. That is the order of how *thin* each item is, the reverse of how many fit. Students know the sizes; they don't turn "thinner" into "more of them fit in a foot".

**Row 23 (ordering): Representing fails.** *"Put the states in order by their lowest elevation, from least to greatest (California −282, Louisiana −8, New Mexico 2,842, Wyoming 3,099, Colorado 3,350)."* The most common wrong order is exactly greatest to least (36% with both spellings), and 13% put Louisiana (−8) before California (−282), ordering the negatives by size. Both errors are about what "least" means for signed numbers, not about comparing 2,842 and 3,099.

## What this means for the labels

- **The top practice predicts the kind of error.** Representing and Modeling problems fail at setup and produce one shared, systematic wrong answer. Procedural problems fail at execution and produce near-misses (sign, decimal point, exponent). Abstracting problems produce the linear version of a non-linear rule.
- **Wrong-answer data can check the labels.** When a problem's dominant distractor is a correct computation on a wrong setup, its top practice is probably Representing or Modeling, even when a labeler said Procedural (rows 223, 244, 23). That gives an automatic way to flag labels for review.
- **This could feed the models.** A distractor-to-practice map can turn a wrong answer into evidence about *which* practice failed, not just that the student got the item wrong.
- **Limits:**
  - The mapping is hand-coded by one coder.
  - Rows 1–300 have no multiple-choice items, so the multiple-choice and select-all problems still need Claude-quality labels before they can be analysed this way.
  - Only first attempts without help are used, and answer texts on multi-part problems may mix parts.
