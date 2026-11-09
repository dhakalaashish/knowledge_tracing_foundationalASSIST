# Agreements: predicted_practice vs claude_top_practice (rows 1–300)

Rows where `claude_top_practice` equals `predicted_practice`: 187 of 300 (62%). Each problem was answered by a fresh agent that saw only the problem text. **Answer 1** is the reply to the first question; it is stored in `claude_practice_reasoning`. **Answer 2** is the reply to the follow-up; `claude_top_practice` is the first practice it names.

| Practice | Rows |
|---|---|
| Procedural Fluency | 159 |
| Representing | 19 |
| Abstracting and Generalizing | 8 |
| Mathematical Modeling | 1 |

---

## Row 2 (problem_id 58180)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate 10^3.
____
```

### Answer 1: practices in order

**Answer: 10^3 = 1000.** You need two practices, used in this order: **Representing, then Procedural Fluency.**

**The practice set I'm using:**
- From the NAEP Mathematics Framework (2026), the five mathematical practices:
  1. Representing
  2. Abstracting and Generalizing
  3. Justifying and Proving
  4. Mathematical Modeling
  5. Collaborative Mathematics
- Added from the NRC "Adding It Up" strands: Procedural Fluency, meaning carrying out procedures flexibly, accurately and efficiently.

**Order of practices for "Evaluate 10^3":**

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Turns the exponent notation into repeated multiplication: 10^3 means 10 × 10 × 10. This is a move from one symbolic form to an equivalent one. |
| 2 | **Procedural Fluency (NRC)** | Does the multiplication accurately: 10 × 10 = 100, then 100 × 10 = 1000. |

**Practices not needed:**
- **Abstracting and Generalizing:** The item asks for one value, not a pattern. The "1 followed by n zeros" rule is a generalization, but a student using it here is only recalling and applying a known rule. That counts as procedural fluency, not generalizing in the moment.
- **Justifying and Proving:** The student doesn't have to give an argument or explain why.
- **Mathematical Modeling:** There's no real-world context to turn into math.
- **Collaborative Mathematics:** It's an individual item with nothing to communicate or critique.

**Caveat for coding:** For a student who already knows that 10^3 = 1000, the Representing step is close to automatic, and the item is almost purely Procedural Fluency. If your scheme needs a single primary practice, tag it **Procedural Fluency**, with Representing as a minor secondary practice.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC).** Representing stays as a minor secondary practice.

**Why:**
- **What the item tests is the calculation.** The only thing it asks for is the value, 1000. Getting there correctly means multiplying 10 × 10 × 10 accurately, or recalling and applying the rule that 10^n is 1 followed by n zeros.
- **The Representing step is too small to be the main one.** Reading 10^3 as 10 × 10 × 10 is just decoding standard notation. The student doesn't choose between representations, translate between forms or build one, which is what NAEP's Representing practice is about. For any student past the basic exponent lesson, this step is automatic.
- **None of the other NAEP practices apply.** The item doesn't involve Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling or Collaborative Mathematics.

**Coding for "Evaluate 10^3" (answer: 1000):** Procedural Fluency as primary, Representing as minor secondary. The order stays Representing, then Procedural Fluency.

---

## Row 3 (problem_id 58041)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate 5^3 ⋅ 2^3.
____
```

### Answer 1: practices in order

**Answer:** 5³ · 2³ = 125 · 8 = **1000**. You can also get it as (5·2)³ = 10³ = 1000.

**Practices available.** The NAEP 2026 Mathematics Framework lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I added **Procedural Fluency** from the NRC's *Adding It Up* strands. I named the NAEP practices from memory, not from your files.

**Practices used, in order:**

1. **Representing.** The student reads the notation: 5³ means 5·5·5, 2³ means 2·2·2, and the "·" means multiply. On the faster route, the student also rewrites the expression as (5·2)³.
2. **Abstracting and Generalizing** (only on the faster route). The student notices that both bases have the same exponent and uses the rule aⁿ·bⁿ = (ab)ⁿ to get 10³. A student who multiplies the powers out directly skips this step.
3. **Procedural Fluency (NRC).** The student does the arithmetic correctly: 5³ = 125, 2³ = 8, and 125 × 8 = 1000. On the faster route, 10³ = 1000.

**So there are two valid orders:**
- **Direct route:** Representing → Procedural Fluency
- **Structural route:** Representing → Abstracting and Generalizing → Procedural Fluency

**Practices not used:**
- **Justifying and Proving:** the student fills in a blank and gives no argument.
- **Mathematical Modeling:** the problem has no real-world context.
- **Collaborative Mathematics:** there is no one else's reasoning to evaluate or build on.

**Possible weights for Problems.csv** (my judgment, not taken from NAEP): Procedural Fluency about 0.6, Representing about 0.25, Abstracting and Generalizing about 0.15, and 0 for the other three. Procedural Fluency gets the most weight because this is mainly a computation item.

### Answer 2: major practice

**Major practice:** if I had to choose one, it would be **Procedural Fluency (NRC)**.
- **It's what the item measures.** The task is "evaluate," the answer is a single number, and success depends on getting 5³ = 125, 2³ = 8 and 125 × 8 = 1000 right.
- **It's used on both routes.** Whether a student multiplies directly or rewrites it as (5·2)³ = 10³, they still have to compute. Abstracting and Generalizing only shows up on the shortcut route.
- **Representing is too small a step to be the main practice.** Reading exponent notation is basic for a student at this level.

If you have to pick only from the five NAEP practices, I'd choose **Representing**, since the item is mostly about reading and working with exponent notation. I'd put Abstracting and Generalizing second, because the shortcut is optional.

---

## Row 4 (problem_id 95)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
There are 12 inches in 1 foot and 5,280 feet in 1 mile. Jada ran 3 1/4 miles.
How many feet is that?
____ feet
```

### Answer 1: practices in order

I used the five mathematical practices from the NAEP 2026 Mathematics Framework: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I also added Procedural Fluency from the NRC's *Adding It Up* strands. I listed the NAEP practices from memory and did not check them against the framework document.

**Answer: 17,160 feet**

**Practices in order**

1. **Representing.** Turn the word problem into a math expression.
   - Pick out the fact that matters: 1 mile = 5,280 feet. The fact that 12 inches = 1 foot is a distractor and isn't needed.
   - Rewrite the mixed number 3 1/4 as 13/4 or 3.25.
   - Set up the conversion: 3 1/4 × 5,280.

2. **Procedural Fluency (NRC).** Do the multiplication accurately.
   - 3 × 5,280 = 15,840
   - 1/4 × 5,280 = 1,320
   - 15,840 + 1,320 = **17,160**
   - Another way: 13/4 × 5,280 = 13 × 1,320 = 17,160

So the sequence is **Representing → Procedural Fluency**.

**Practices not used**
- **Abstracting and Generalizing:** there is no pattern to find and no general rule to state.
- **Justifying and Proving:** the item asks for a number, not an explanation.
- **Mathematical Modeling:** the context is fully set up, so there are no assumptions to make or models to choose. At most, a student might check that the answer is reasonable, since it should fall between 3 × 5,280 and 4 × 5,280. That check is too small to count as this practice.
- **Collaborative Mathematics:** this is a task done alone.

If you label items with weights, Procedural Fluency should get the most, because the main challenge is multiplying a mixed number by a four-digit number. Representing gets less, because the only hard part is ignoring the inches distractor.

### Answer 2: major practice

I'd pick **Procedural Fluency** as the major practice.

Getting the right answer depends mostly on multiplying 5,280 by the mixed number 3 1/4 correctly: 3 × 5,280 = 15,840, plus 1/4 × 5,280 = 1,320, for **17,160 feet**. Setting up the problem takes little work. The problem gives the conversion fact directly, and the only trap is ignoring the 12-inches-per-foot information. Students are much more likely to miss this item because of an arithmetic or fraction mistake than because they set it up wrong.

If the label has to be one of the five NAEP 2026 practices, which don't include Procedural Fluency, I'd pick **Representing**. Turning the words into 3 1/4 × 5,280 is the only NAEP practice the problem really uses. Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling and Collaborative Mathematics don't come into it.

Order of practices if you label more than one: **Representing, then Procedural Fluency**. Give Procedural Fluency the higher weight.

---

## Row 5 (problem_id 93)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Given the equation y = ‐3x + 2.5:
When x is 1, what value of y makes the equation true?
y = ____
```

### Answer 1: practices in order

**Answer:** y = −3(1) + 2.5 = **−0.5**

**Which practices are used, and in what order**

The practices available are the five in the NAEP 2026 Mathematics Framework (Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics), plus Procedural Fluency from the NRC's *Adding It Up*. This item uses two of them, in this order:

1. **Representing (NAEP)**
   - The student reads y = −3x + 2.5 as a rule that pairs each x with a y.
   - They understand that "what value of y makes the equation true" means finding the y that goes with x = 1, the point (1, y).
   - They see that the 1 has to replace x in the expression.
   - This step is light. There is no switch to a graph or table and no real-world context. It is reading and working within one symbolic form.

2. **Procedural Fluency (NRC)**
   - The student carries out the substitution and the arithmetic: −3 · 1 = −3, then −3 + 2.5 = −0.5.
   - This is where the item gets hard: multiplying by a negative, then adding a positive decimal to a negative whole number. A common wrong answer is 0.5 from a sign error, or 5.5 from treating −3 + 2.5 as 3 + 2.5.
   - An optional check, putting −0.5 back in to see that it works, is also procedural fluency.

**Practices not used**

- **Abstracting and Generalizing:** The student goes from a general rule to one specific value. Nothing is generalized.
- **Justifying and Proving:** No explanation or argument is asked for.
- **Mathematical Modeling:** There is no real-world context to turn into math.
- **Collaborative Mathematics:** This is a single-student item.

**Summary:** Representing → Procedural Fluency. Procedural Fluency carries most of the difficulty, so it should get the most weight. If your coding scheme counts Representing only when the student moves between forms (for example equation to graph or table), code this item as Procedural Fluency only.

### Answer 2: major practice

**Answer to the follow-up:** If I had to pick one, it would be **Procedural Fluency (NRC)**.

**Why:**
- The student only needs to see that x = 1 replaces x, and that takes almost no thought. That is the Representing step, and it is short.
- Where students actually fail is the arithmetic: −3 · 1 = −3, then −3 + 2.5 = −0.5.
- The usual wrong answers come from sign mistakes: 0.5 from dropping the negative, or 5.5 from adding 3 + 2.5.
- So Procedural Fluency decides whether a student gets the item right. Representing is a short first step before it.

---

## Row 6 (problem_id 253)

- **predicted_practice:** Mathematical Modeling
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
Diego has $11 and begins saving $5 each week toward buying a new phone. At the same time that Diego begins saving, Lin has $60 and begins spending $2 per week on supplies for her art class.
Is there a week when they have the same amount of money?
[dropdown: No / Yes]
```

### Answer 1: practices in order

**Answer: Yes.** In week 7, Diego and Lin both have $46.

- Diego's money after w weeks: 11 + 5w
- Lin's money after w weeks: 60 − 2w
- Setting them equal: 11 + 5w = 60 − 2w, so 7w = 49 and w = 7

The NAEP 2026 Mathematics Framework names five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Here is the order for this problem, with NRC procedural fluency added:

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (set up) | Identifies the quantities (dollars and weeks) and that each person's money changes by a fixed amount each week. Turns the question into: is there a whole number of weeks w at which the two amounts are equal? |
| 2 | **Representing** | Writes the situation in math form: D = 11 + 5w, L = 60 − 2w, and sets them equal. A week-by-week table or a graph of two lines also works. |
| 3 | **Procedural Fluency** (NRC) | Solves the linear equation: 11 + 5w = 60 − 2w, so 7w = 49 and w = 7. Checks it: 11 + 35 = 46 and 60 − 14 = 46. |
| 4 | **Mathematical Modeling** (interpret and check) | Puts w = 7 back into the story. It is a whole, positive number of weeks, and Lin still has money at that point ($46). So the answer in the dropdown is **Yes**. |
| 5 | **Justifying and Proving** (minor) | Supports the claim "there is such a week" by naming the week (week 7, $46 each). The dropdown doesn't ask for a written reason, so this practice plays only a small role here. |

**Why step 4 matters most for a Yes/No item.** They only have equal money in a particular week because the $49 gap is a multiple of the $7 it shrinks each week. If Lin had started with $61, the equation would give w = 7 1/7. The answer would then be **No**, even though the two lines still cross. Checking that the answer is a whole number of weeks is what the item really tests.

**Practices that are optional or not used:**
- **Abstracting and Generalizing** depends on how the student solves it. It is used if the student turns "each week" into a rule for any week w (step 2). It is also used if the student sees the shortcut "a $49 gap closing by $7 per week." A student who just lists the weeks in a table (11, 16, 21, … vs. 60, 58, 56, …) doesn't need it.
- **Collaborative Mathematics** is not used, because there is no other person's reasoning to judge or build on.

**One tag set for this item:**
- Core: Mathematical Modeling, Representing, Procedural Fluency
- Minor: Justifying and Proving
- Optional: Abstracting and Generalizing

### Answer 2: major practice

**Mathematical Modeling.** That is the one I'd choose as the major practice.

Why it beats the others:

- **It covers both ends of the problem.** The student starts by turning a story about saving and spending into a math question: is there a whole number of weeks w where 11 + 5w = 60 − 2w? The student ends by putting the result back into the story. Those are the formulate and interpret steps of the modeling cycle. Representing and procedural fluency only handle the middle.
- **It is what decides Yes or No.** Solving gives w = 7, but the dropdown answer depends on reading that result in context. It is a whole, positive number of weeks, and Lin still has money then, so the answer is Yes. If the gap had been $50 instead of $49, the algebra would be just as easy, but w = 50/7 would make the answer No. The item really tests the modeling judgment, not the calculation.
- **The other practices are interchangeable or small.** A student can skip symbols entirely and just list the weeks in a table, so Representing (in its symbolic form) isn't required. The arithmetic for procedural fluency is light (7w = 49). Justifying is not asked for in a dropdown.

If you need a second tag, add **Representing**. The student has to put the two changing amounts into some comparable form (expressions, a table, or a graph) before anything can be compared.

---

## Row 7 (problem_id 320140)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Divide.
4/9 ÷ 8/15
____
```

### Answer 1: practices in order

**Answer: 4/9 ÷ 8/15 = 5/6**

The NAEP mathematics practices are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added Procedural Fluency from the NRC's *Adding It Up* as a sixth.

This item is a plain calculation. It has no context, no picture or graph, and it doesn't ask the student to explain anything. So it mainly tests procedural fluency. Representing plays a small part, and only if you count rewriting the expression as using that practice.

### Practices in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | Representing (minor) + Procedural Fluency | Recognizes this as dividing one fraction by another and rewrites it as an equivalent multiplication: 4/9 × 15/8 (multiply by the reciprocal). |
| 2 | Procedural Fluency | Cancels common factors across the fractions: 4 and 8 share 4, giving 1 and 2. 15 and 9 share 3, giving 5 and 3. The expression becomes 1/3 × 5/2. |
| 3 | Procedural Fluency | Multiplies the numerators and the denominators to get 5/6, which is already in lowest terms. Without canceling first, the student gets 60/72 and must reduce it to 5/6. |
| (optional) | Self-check (not required) | Checks the answer by multiplying back: 5/6 × 8/15 = 40/90 = 4/9. This is good habit, but the item doesn't require it, so I wouldn't tag it as Justifying and Proving. |

### Practices not used

- **Abstracting and Generalizing:** The student uses a known rule ("invert and multiply") but doesn't find a pattern or build a general rule.
- **Justifying and Proving:** The item doesn't ask the student to explain or defend the method.
- **Mathematical Modeling:** There's no real-world situation to turn into math.
- **Collaborative Mathematics:** There's no other student's work to read or critique.

### Summary for tagging

- **Primary:** Procedural Fluency (steps 1-3)
- **Secondary (weak):** Representing (step 1 only)
- **Order:** Representing, then Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

I'd pick it for three reasons:

- **It covers the whole solution.** Rewriting as multiplication by the reciprocal (4/9 × 15/8), canceling common factors (1/3 × 5/2), and multiplying to get 5/6 are all steps of a standard procedure, done correctly.
- **It's what the item tests.** The prompt only says "Divide." There's no context to model, no representation to read or build, and no reasoning to explain or defend.
- **Representing is too small to count as the major one.** Its only role is rewriting the division as multiplication. That's a symbolic rewrite inside the procedure, not real work with representations. A student can solve the whole problem just by knowing the "invert and multiply" rule.

If you must use a NAEP practice, choose **Representing**, but it's a weak fit. NAEP's practices are meant for items that require more reasoning or context than this one does.

---

## Row 9 (problem_id 3056)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Factor to write an equivalent expression: 26a - 10
If you get stuck, use a diagram to organize your work.
____
```

### Answer 1: practices in order

**Problem:** Factor 26a − 10 to write an equivalent expression (a diagram is suggested if the student gets stuck).
**Answer:** 2(13a − 5)

**Practices available** (NAEP 2026 framework, plus one from NRC): Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, and Procedural Fluency.

### Practices needed, in order

**1. Procedural Fluency (the main practice)**
- Find the greatest common factor of the coefficients: 26 = 2·13 and 10 = 2·5, so the GCF is 2. The variable *a* is only in the first term, so it can't be factored out.
- Divide each term by 2: 26a ÷ 2 = 13a and 10 ÷ 2 = 5.
- Write the result as 2(13a − 5).

Most of the work is carrying out this routine procedure correctly and quickly.

**2. Representing (used if the student gets stuck)**
- The prompt says to "use a diagram to organize your work." This usually means an area or box model. Write 26a and −10 inside the boxes. Put the common factor 2 on the side. Then fill in 13a and −5 along the top.
- The answer itself is also a change of representation, from expanded form (a sum of terms) to factored form (a product).
- For a student who goes straight to the diagram, Representing would come first and support step 1. For a fluent student, it may not be used at all. That's why it comes second.

**3. Justifying and Proving (a light check)**
- Confirm the two expressions are equivalent by distributing: 2(13a − 5) = 26a − 10. You could also check that 13 and 5 have no common factor left, so the factoring is complete.
- The problem doesn't ask for this, so it's a self-check rather than a formal justification. Count it as a minor or optional practice.

### Practices not needed
- **Abstracting and Generalizing:** Spotting a common factor and using the distributive property in reverse is part of the routine procedure. Nothing is being generalized. You could argue for a very light tag, but I wouldn't include it.
- **Mathematical Modeling:** There is no real-world context to model.
- **Collaborative Mathematics:** This is an individual task, with no communicating or critiquing someone else's reasoning.

### Summary
**Procedural Fluency → Representing (only if stuck) → Justifying and Proving (check)**

Procedural Fluency is the main practice. Representing is the backup strategy the prompt suggests. Justifying and Proving is optional.

### Answer 2: major practice

**Major practice: Procedural Fluency**

**Why:**
- **The task is a procedure.** The question tells the student what to do: "Factor to write an equivalent expression." To answer it, you find the GCF of 26 and 10 (which is 2), divide each term by it, and write 2(13a − 5). This is a standard skill that is either done correctly or not.
- **Representing is only a backup.** The diagram appears only under "if you get stuck." A student can get the answer without drawing anything, so Representing isn't needed to solve the problem.
- **Justifying and Proving is never asked for.** Checking the answer by distributing is good practice, but the problem doesn't require it and doesn't grade it.
- **What the item measures.** If a student gets it wrong, the likely cause is a procedural error: missing the GCF, factoring only part of it (2 instead of a larger factor, though here 2 is the GCF), dividing incorrectly, or dropping the minus sign. Those are fluency errors, not errors in representing or reasoning.

So if the item gets one label, it should be **Procedural Fluency**. If your coding allows a secondary tag, use Representing because the item suggests a diagram.

---

## Row 10 (problem_id 319193)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Lin’s second pan has a length of 8/3 inches, a width of 15/4 inches, and a height of 3/2 inches. What is the volume of the second pan?
____ cubic inches
```

### Answer 1: practices in order

**Problem:** Lin's second pan is 8/3 in. long, 15/4 in. wide and 3/2 in. high. What is its volume?

**Practices to choose from**

- **NAEP 2026 Mathematics Framework practices:** Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics.
- **Added from the NRC (*Adding It Up*):** Procedural Fluency.

---

## Practices needed, in order

### 1. Representing
Turn the word description into a mathematical expression.
- A pan with a length, width and height is a rectangular prism, so its volume is V = l × w × h.
- Put the given values into the formula: **V = 8/3 × 15/4 × 3/2**.
- The answer must be in cubic inches.

This is the key step. The student has to see that "volume of a box-shaped pan" means multiplying the three dimensions. They also need to keep the measurements as fractions rather than converting them.

### 2. Procedural Fluency (NRC)
Carry out the fraction multiplication accurately and efficiently.
- Cancel common factors before multiplying:
  - 8/3 × 3/2 → the 3s cancel, giving 8/2 = 4
  - 4 × 15/4 → the 4s cancel, giving **15**
- Another route is to multiply straight across: (8 × 15 × 3)/(3 × 4 × 2) = 360/24 = 15.
- A quick estimate confirms the answer is reasonable: about 2.7 × 3.75 × 1.5 ≈ 15.

**Answer: 15 cubic inches**

---

## Practices not needed

| Practice | Why it isn't used |
|---|---|
| Mathematical Modeling | The situation is already fully defined. There are no assumptions to make, no model to build or refine, and no answer to interpret back in context beyond stating the units. Recognizing the pan as a prism is part of Representing. |
| Abstracting and Generalizing | The student finds one specific value and does not need to find a pattern or general rule. |
| Justifying and Proving | The student only gives a number and is not asked to explain or defend it. |
| Collaborative Mathematics | This is an individual item with no group work. |

**Order:** Representing → Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

In my last answer I called Representing "the key step." That is true in one sense: the student has to take that step first. But if I have to pick the practice that drives this item, it's Procedural Fluency. Here's why:

- **The Representing step is routine.** The problem gives length, width and height, and asks for volume in cubic inches. That points straight to V = l × w × h. There is nothing to decide about which quantities matter or how they relate. Any student who knows the volume formula sets up 8/3 × 15/4 × 3/2 almost immediately.
- **The real work is the fraction calculation.** The student has to multiply three fractions and simplify, ideally by cancelling (8/3 × 3/2 = 4, then 4 × 15/4 = 15). This is where the item gets its difficulty.
- **Most errors would come from the arithmetic.** Typical mistakes include:
  - adding the fractions instead of multiplying them
  - multiplying incorrectly or not simplifying 360/24
  - converting to mixed numbers or decimals and making a mistake
  - stopping after two of the three factors

  Students who know the formula but are shaky with fractions would get this wrong. Students who are fluent with fractions would almost always get it right.
- **It looks like a fraction-multiplication item set in a volume context.** The neat answer (15) and the factors that cancel cleanly suggest the item was written to reward efficient computation with fractions.

**Summary:** Representing is a short, necessary first step. Procedural Fluency is the main practice.

---

## Row 11 (problem_id 195315)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
How many days of the week is Noah considering?
____ days of the week
[Image: The image is a decision tree diagram with three main branches labeled "space," "safari," and "comics." Each branch splits into two sub-branches: "skating rink" and "park." From each sub-branch, there are three additional branches pointing to the days "Fri," "Sat," and "Sun."]
```

### Answer 1: practices in order

**Answer: 3 days (Fri, Sat, Sun)**

**The practices available.** The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added **Procedural Fluency**, one of the NRC's five strands of mathematical proficiency.

**Practices needed, in order:**

| Step | Practice | What the student does in this problem |
|---|---|---|
| 1 | **Representing** | Reads the tree diagram and works out what each level stands for. The first level is the activity (space, safari, comics), the second is the place (skating rink, park), and the third is the day (Fri, Sat, Sun). The student then picks out the day level as the one the question is about. |
| 2 | **Abstracting and Generalizing** | Sees that the day branches repeat the same way under every place branch. The 18 day branches at the end of the tree are just the same 3 days repeated 6 times. So the number of different days is not the same as the number of branches or paths. This is the main trap in the problem: a student who misses it may answer 18 (all the day branches) or 6. |
| 3 | **Procedural Fluency** (NRC) | Counts the different day labels (Fri, Sat, Sun) correctly and gets **3**. |

**Practices not needed:**
- **Justifying and Proving**: the student doesn't have to explain or defend the answer.
- **Mathematical Modeling**: the model (the tree) is already given, so the student doesn't build one from the real situation.
- **Collaborative Mathematics**: the student works alone.

**Note on how much each practice matters:** Most of the work here is **Representing**, meaning reading the diagram. The Procedural Fluency step is small, since it's only counting to 3. If a later part of the same item asked for the total number of choices (3 × 2 × 3 = 18), Procedural Fluency would matter more because that uses multiplication, and Abstracting and Generalizing would also matter more because it needs the counting principle.

### Answer 2: major practice

**Major practice: Representing**

Most of this problem is about reading the tree diagram correctly:

- **The answer is right there in the diagram.** Nothing needs to be calculated or built. The student only has to see which level of the tree shows the days and read off its labels.
- **The usual mistakes are reading mistakes.** A wrong answer like 18 (all the day branches) or 6 (the branches one level up) comes from misreading how the tree is laid out. It doesn't come from a counting error or a gap in reasoning.
- **The other two practices are small.** Abstracting and Generalizing here just means noticing that the same three days show up under every branch, which is really part of understanding how a tree diagram works. Procedural Fluency is only counting to 3.

So if I had to tag this item with one practice, it would be **Representing**. Abstracting and Generalizing would come second, and Procedural Fluency would play only a small role.

---

## Row 12 (problem_id 3036)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression.
6.08 + 2.02
____
```

### Answer 1: practices in order

**Answer:** 6.08 + 2.02 = **8.10**, which is the same as **8.1**.

**Practices considered**
- From the NAEP 2026 Mathematics Framework: Representing, Abstracting & Generalizing, Justifying & Proving, Mathematical Modeling, and Collaborative Mathematics.
- From the NRC: Procedural Fluency.

---

## Practice order for this problem

### 1. Procedural Fluency (NRC): the only practice this problem needs

This is a plain computation with no context. Solving it means running the decimal-addition steps correctly:

1. **Line up the decimal points** so digits with the same place value sit in the same column:
   ```
     6.08
   + 2.02
   ```
2. **Hundredths:** 8 + 2 = 10 hundredths. Write 0 and carry 1 tenth.
3. **Tenths:** 0 + 0 + 1 (carried) = 1.
4. **Ones:** 6 + 2 = 8.
5. **Result:** 8.10, which simplifies to 8.1.

A quicker mental route also counts as fluency: (6 + 2) + (0.08 + 0.02) = 8 + 0.10 = 8.1.

**Check:** 6 + 2 = 8, and the answer is just over 8, so it makes sense.

**Likely mistake:** writing 8.010. This happens when a student adds "08 + 02 = 010" and sticks it after the decimal point, instead of regrouping 10 hundredths as 1 tenth.

---

## Why the NAEP practices aren't needed

| NAEP practice | Used? | Reason |
|---|---|---|
| Representing | No | The problem is given and answered in the same symbolic form. Nothing gets turned into a table, graph, number line, or words. Lining up the decimals is part of the steps, not a new representation. |
| Abstracting & Generalizing | No | There is no pattern or general rule to find. |
| Justifying & Proving | No | The problem doesn't ask for an argument or explanation. |
| Mathematical Modeling | No | There is no real-world situation to turn into math. |
| Collaborative Mathematics | No | There is no work with others or reasoning about someone else's solution. |

**Final sequence:** Procedural Fluency only.

If your tagging scheme needs at least one NAEP practice on every item, the closest weak match is **Representing**, because the student has to read decimals as place-value amounts. I'd still mark it as not truly required.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:** 6.08 + 2.02 is a bare calculation. There is no context, no change of representation, nothing to generalize or justify, and no one to work with. Getting it right depends only on carrying out the decimal-addition steps accurately:
1. Line up the decimal points.
2. Add the hundredths: 8 + 2 = 10, so write 0 and carry 1 to the tenths.
3. Add the tenths and the ones to get 8.10, which is 8.1.

The one place students go wrong is that regrouping step, which is a fluency error, not a reasoning error.

**If it has to be a NAEP practice:** I'd pick **Representing**. It is only a weak fit: the student has to read 6.08 and 2.02 as place-value amounts so the right digits line up. The problem never asks them to move between representations, though, so this tag would be much less accurate than Procedural Fluency.

---

## Row 13 (problem_id 3201)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression.
35 - 0.02
____
```

### Answer 1: practices in order

**Problem:** Evaluate 35 − 0.02  →  **Answer: 34.98**

### The practice set

The 2026 NAEP Mathematics Framework names five mathematical practices:

1. **Representing**: making, interpreting and moving between representations (symbolic, numeric, visual).
2. **Abstracting and Generalizing**
3. **Justifying and Proving**
4. **Mathematical Modeling**
5. **Collaborative Mathematics**

Added from the NRC strands (*Adding It Up*, 2001):

6. **Procedural Fluency**: carrying out procedures such as computation flexibly, accurately and efficiently.

### Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Rewrite the whole number 35 as an equivalent decimal, **35.00**, so both numbers have the same place values (tenths and hundredths) and the decimal points line up: `35.00 − 0.02`. This step catches the most common error, which is treating 35 as if it had no decimal places and lining up the digits wrongly. Students who get 33 or 34.02 have usually skipped it. |
| 2 | **Procedural Fluency** (NRC) | Subtract column by column with regrouping: borrow from the ones place across the zeros (5 ones → 4 ones, 9 tenths, 10 hundredths), then compute 10 − 2 = 8 hundredths and 9 − 0 = 9 tenths, giving **34.98**. A fluent student can also do it mentally: "0.02 less than 35 is 34.98." |

**Optional check (still procedural fluency):** add back, 34.98 + 0.02 = 35.00. This is a routine self-check, not the NAEP *Justifying and Proving* practice, because no argument or proof is being built.

### Practices not used

- **Abstracting and Generalizing**: the student only computes one value and forms no pattern or general rule.
- **Justifying and Proving**: the item asks for no explanation or argument.
- **Mathematical Modeling**: there is no real-world context to translate into math.
- **Collaborative Mathematics**: this is an individual computation item.

### Summary

**Representing → Procedural Fluency**

The item is mainly a **procedural fluency** item, and NAEP would rate it low complexity. *Representing* plays a small but important role at the start: writing 35 as 35.00 so the place values line up before subtracting. If you need to tag one primary practice, use **Procedural Fluency**, with **Representing** as secondary.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**

- **It is what the item tests.** "Evaluate 35 − 0.02" asks for a single computed value. The main work, and where most of the difficulty lies, is subtracting decimals with regrouping across zeros (35.00 → 34 ones, 9 tenths, 10 hundredths) and getting 34.98.
- **Representing is only a setup step.** Writing 35 as 35.00 to line up place values is part of the standard decimal-subtraction procedure. It is not a separate act of creating or interpreting a representation. Fluent students often skip writing it down and just reason "0.02 less than 35 is 34.98."
- **None of the other NAEP practices apply.** The item has no pattern to generalize, no argument to make, no real-world context to model, and no group work.
- **The common errors are procedural.** Answers like 33, 34.02 or 35.02 come from misaligning place values or borrowing wrongly. Those are failures in carrying out the procedure accurately, which is exactly what procedural fluency covers.

So if you need a single label for this item, tag it **Procedural Fluency**. Treat Representing as a minor secondary practice, if you tag one at all.

---

## Row 14 (problem_id 2812)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression.
7 - 0.18
____
```

### Answer 1: practices in order

**Problem:** Evaluate 7 - 0.18
**Answer:** 6.82

## Practices available

The NAEP 2026 Mathematics Framework lists five mathematical practices. I'm working from memory of the framework, so check these names against your copy.
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC (*Adding It Up*): **Procedural Fluency**

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Writes the whole number 7 in a different but equal form, 7.00, so that it has the same number of decimal places as 0.18. Then lines the two numbers up by place value (ones under ones, tenths under tenths, hundredths under hundredths). |
| 2 | **Procedural Fluency (NRC)** | Does the subtraction 7.00 - 0.18 with regrouping. 7 ones becomes 6 ones + 9 tenths + 10 hundredths. Then 10 - 8 = 2 hundredths, 9 - 1 = 8 tenths, 6 - 0 = 6 ones. The result is **6.82**. |

**Main practice:** Procedural Fluency. This is a direct calculation and most of the work is carrying out the algorithm correctly. Representing is a short setup step before it, but it matters. The usual mistake on this item comes from skipping it: the student lines up the last digits (7 under the 8) instead of the decimal points and gets an answer like 0.11. Rewriting 7 as 7.00 prevents that.

## Practices not used

- **Abstracting and Generalizing:** The student doesn't need to find a pattern or a general rule. It's one specific calculation.
- **Justifying and Proving:** The problem doesn't ask for an argument or explanation. A quick check (6.82 + 0.18 = 7) is part of being fluent with the procedure, not a justification.
- **Mathematical Modeling:** There is no real-world context to turn into math. The expression is already given.
- **Collaborative Mathematics:** This is a single student answering a single item.

**Sequence:** Representing -> Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- **The task:** "Evaluate the expression" with no context. The student just has to carry out a calculation correctly, and that is what procedural fluency means.
- **Where the work is:** Almost all of it is the decimal subtraction algorithm. The student has to regroup across the decimal point (7.00 -> 6 ones, 9 tenths, 10 hundredths) and then subtract each place.
- **Why not Representing:** Rewriting 7 as 7.00 is a short setup move that is part of the standard decimal subtraction procedure. Representing isn't the main skill being tested. The item doesn't ask the student to choose or move between representations such as number lines, models, or fractions.

If I had to pick only from the five NAEP practices, I would choose **Representing**, since it's the only NAEP practice the item really uses. Still, it is a weak fit, and Procedural Fluency describes this item much better.

---

## Row 15 (problem_id 2930)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression.
13.23 + 2.67
____
```

### Answer 1: practices in order

**Problem:** Evaluate 13.23 + 2.67
**Answer:** 15.90 (= 15.9)

## Practices available

**NAEP Mathematics Framework (2026) practices:**
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

**Added from NRC (*Adding It Up*):** Procedural Fluency, which means carrying out procedures flexibly, accurately and efficiently.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (minor) | Rewrites the horizontal expression in column form with the decimal points lined up, so hundredths sit under hundredths, tenths under tenths, and so on. This turns the item into a place-value layout. |
| 2 | **Procedural Fluency** (NRC), the main practice | Runs the decimal addition algorithm. Hundredths: 3 + 7 = 10, so write 0 and carry 1. Tenths: 2 + 6 + 1 = 9. Ones: 3 + 2 = 5. Tens: 1. The result is **15.90**. |
| 3 | **Representing** (optional, minor) | Writes the result as an equivalent value, 15.90 = 15.9, if the answer format calls for it. |

```
  13.23
+  2.67
-------
  15.90
```

**Short version:** Representing (align by place value), then Procedural Fluency (add and regroup), then optionally Representing again (simplify 15.90 to 15.9).

## Practices that don't apply

- **Abstracting and Generalizing:** The student doesn't need to find a pattern or a general rule.
- **Justifying and Proving:** The item asks for no argument or explanation. A quick check like 13 + 3 ≈ 16 is self-monitoring, not justification.
- **Mathematical Modeling:** The problem has no real-world context to turn into math.
- **Collaborative Mathematics:** This is a solo item.

## Note

This is basically a **content-only computation item**. The NAEP framework allows items that assess content without targeting any practice, and this is one of them. If you tag only one practice, use **Procedural Fluency**. Representing is light here: it is just the place-value alignment, not a real move between different representations like a graph, table or equation. You could reasonably leave it out if you want to tag only strong practice demands.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:** The item is a bare computation, 13.23 + 2.67. It has no context, no pattern to generalize, nothing to justify or model, and no real switch between representations. A student who gets it right shows one thing: they can run the decimal addition algorithm accurately. That means lining up place values, adding 3 + 7 = 10 in the hundredths and carrying 1, then getting 9 in the tenths and 5 in the ones, for 15.90. That's procedural fluency.

Lining up the decimal points is part of the procedure itself, not a separate Representing demand. So none of the NAEP practices has a strong claim here. If you had to pick only from the NAEP list, you'd pick **Representing**, but it would be a weak fit. The better call is Procedural Fluency, or "content only, no practice."

---

## Row 16 (problem_id 2695)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression.
11 - 4.9
____
```

### Answer 1: practices in order

**Problem:** Evaluate 11 - 4.9  **Answer: 6.1**

**Practices used.** The NAEP 2026 Mathematics Framework has five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I added NRC's Procedural Fluency as a sixth.

This item is a plain computation with no context, so it relies mostly on Procedural Fluency. Only one NAEP practice plays a real part, and it is a small one.

### Order of practices

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Rewrites the whole number 11 as the decimal 11.0 so the place values line up with 4.9 (ones under ones, tenths under tenths). Writing the same quantity in an equivalent decimal form is a small change of representation. |
| 2 | **Procedural Fluency** (NRC) | Does the subtraction with regrouping. In the tenths place, 0 - 9 can't be done, so the student borrows 1 one, which gives 10 tenths - 9 tenths = 1 tenth. In the ones place, 11 becomes 10, and 10 - 4 = 6. Result: **6.1**. A fluent student can also compensate instead: 11 - 5 = 6, then add back 0.1 to get 6.1. This is the main practice for the item. |
| 3 | *(Optional)* **Justifying and Proving** (NAEP) | Checks that the answer is reasonable, either by addition (6.1 + 4.9 = 11) or by estimation (11 - 5 = 6, so the answer should be just over 6). The item doesn't require this. It is a weak, self-check form of the practice. |

**Sequence:** Representing -> Procedural Fluency -> (Justifying and Proving, optional)

### Practices not used
- **Abstracting and Generalizing:** no pattern or general rule is asked for.
- **Mathematical Modeling:** there is no real-world situation to turn into mathematics.
- **Collaborative Mathematics:** this is a single-student item with nothing to communicate or critique.

**Coding suggestion:** For a single practice label, use **Procedural Fluency**. For a multi-label code, use **Procedural Fluency** as primary and **Representing** as secondary (weak).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item asks for nothing except a correct computation: 11 - 4.9 = 6.1. There is no context to model, no pattern to generalize, and no argument to write. What separates a right answer from a wrong one is whether the student can subtract decimals accurately, regrouping across the decimal point.

The usual errors on this item are all procedural. One is misaligning the place values: 11 - 4.9 treated as 1.1 - 4.9 or 11 - 49. Another is skipping the regrouping and writing 0 - 9 as 9, which gives 7.9. A third is borrowing incorrectly, which gives answers like 7.1 or 6.9.

Representing (rewriting 11 as 11.0) is only a small setup step inside that procedure, so it isn't the practice the item actually tests.

---

## Row 18 (problem_id 3705)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
For how many outcomes are the x-coordinate and the y-coordinate the same number?
____
```

### Answer 1: practices in order

## Practices for this problem, in order

The problem text only gives the question: *"For how many outcomes are the x-coordinate and the y-coordinate the same number?"* It is missing the setup that defines the outcomes, which is probably two number cubes, two spinners, or a grid or list of ordered pairs (x, y). The practice sequence below holds for any of those setups. The final count depends on the number set. For two standard number cubes (1–6), the answer is **6**.

**Practices used:** the four NAEP Mathematics Framework practices that apply (Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling), plus Procedural Fluency from the NRC.

---

### Step 1: Representing
Turn the outcomes into ordered pairs (x, y) and lay out the sample space. You can use a 6 × 6 table, a list, or points on a coordinate grid. This means reading "x-coordinate" and "y-coordinate" as the first and second parts of each outcome. Everything else depends on getting this step right.

### Step 2: Abstracting and Generalizing
Turn "the x-coordinate and the y-coordinate are the same number" into the condition **x = y**. Then see that these outcomes make a clear pattern: the main diagonal of the table, or the line y = x on the grid. There is exactly one such pair for each possible value of x: (1,1), (2,2), …, (n,n).

### Step 3: Procedural Fluency (NRC)
Count the outcomes that meet the condition, accurately and in order: (1,1), (2,2), (3,3), (4,4), (5,5), (6,6) gives **6**. This is a routine counting step once the structure is clear, so this is where Procedural Fluency comes in.

### Step 4: Justifying and Proving (light, optional)
Check that the count is complete and correct. x and y must be equal, and each can take each value only once, so the number of matching outcomes equals the number of possible values. No other pair works. A short-answer item does not ask for written justification, so this is only a check the student does mentally.

---

### Practices not used
- **Mathematical Modeling:** not used. There is no real-world situation to simplify or model. The task is about a sample space that is already defined.
- **Collaborative Mathematics:** not used. This is an individual assessment item.

### Summary order
**Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving as a check)**

The main load is on **Representing** and **Abstracting and Generalizing**, meaning setting up the ordered pairs and seeing that "same number" means x = y. Once that is done, **Procedural Fluency** gives the count. Answer (two standard number cubes): **6**.

### Answer 2: major practice

## Major practice: Representing

If I had to pick one, it would be **Representing**.

**Why:**
- **The hard part is reading the representation.** The student has to see each outcome as an ordered pair (x, y) and read its first and second numbers as the x- and y-coordinates. Then they have to find those outcomes in a table, list, or coordinate grid. A student who can't link the outcomes to the coordinate representation can't start the problem.
- **After that, the rest is easy.** Once the outcomes are set out as (x, y) pairs, "same number" just means pairs like (1,1), (2,2), and so on. These sit on the diagonal of the table or the line y = x. Spotting them takes only a little Abstracting and Generalizing, so that practice comes second, not first.
- **Procedural Fluency plays a small role.** Counting six pairs (with two standard number cubes) is a trivial step. It isn't where students go wrong.
- **Justifying and Proving isn't really needed.** The item asks only for a number, with no explanation.

**Ranking:** Representing (major) > Abstracting and Generalizing > Procedural Fluency > Justifying and Proving (just a check).

---

## Row 19 (problem_id 2894)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Expand to write an equivalent expression: -1/2(-2x + 4y)
If you get stuck, use a diagram to organize your work.
____
```

### Answer 1: practices in order

**Problem:** Expand to write an equivalent expression: -1/2(-2x + 4y). (Hint: if you get stuck, use a diagram to organize your work.)

**Answer:** x - 2y

I used the five practices in the NAEP 2026 Mathematics Framework (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics) and added **Procedural Fluency** from the NRC's *Adding It Up* strands. I'm working from memory of the framework here.

### Practices in order

| Step | Practice | What the student does | Required? |
|---|---|---|---|
| 1 | **Abstracting and Generalizing** | Sees that the expression has the form a(b + c), with a = -1/2, b = -2x, c = 4y. So the distributive property applies: a(b + c) = ab + ac. The rule still works when a is a negative fraction. | Yes |
| 2 | **Representing** | Turns the symbolic expression into a diagram, as the hint suggests. This is usually an area or box model with -1/2 on the side and -2x and 4y across the top, one cell for each partial product. | Only if stuck (the item offers it as a scaffold) |
| 3 | **Procedural Fluency (NRC)** | Does the arithmetic correctly: (-1/2)(-2x) = x, because a negative times a negative is positive and 1/2 of 2 is 1. Then (-1/2)(4y) = -2y. Adds the partial products to get x - 2y. | Yes. This is where most of the difficulty is. |
| 4 | **Justifying and Proving** | Checks that the result is equivalent, for example by substituting values. With x = 1 and y = 1, the original is -1/2(-2 + 4) = -1, and x - 2y = 1 - 2 = -1. | Optional |

### Practices not used
- **Mathematical Modeling:** the problem has no real-world situation to model. It is purely symbolic.
- **Collaborative Mathematics:** this is an individual item with no exchange of ideas.

### Summary sequence
**Abstracting and Generalizing → (Representing, if stuck) → Procedural Fluency → (Justifying and Proving, optional check)**

The essential pair is **Abstracting and Generalizing → Procedural Fluency**. Most mistakes on this item are sign or fraction errors in the fluency step, such as -x - 2y, x + 2y, or forgetting to distribute to the second term. That means a wrong answer usually points to a fluency gap more than to failing to recognize the distributive structure.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- **The item is a routine procedure.** The word "Expand" already tells the student to distribute. Recognizing the a(b + c) structure takes little effort, so Abstracting and Generalizing plays only a small part.
- **This step carries the difficulty.** The main demand is multiplying correctly by a negative fraction: (-1/2)(-2x) = x and (-1/2)(4y) = -2y. That means applying sign rules, multiplying a fraction by an integer, and distributing to both terms. Most wrong answers come from this step, such as -x - 2y, x + 2y, or x + 4y.
- **The other practices are optional.** The diagram (Representing) is offered only "if you get stuck," and checking equivalence (Justifying and Proving) isn't required to get the answer.

**If you are limited to the NAEP practices:** choose **Abstracting and Generalizing**. Applying the general distributive rule a(b + c) = ab + ac to this specific case is the only NAEP practice the solution actually requires. Representing is only a fallback.

---

## Row 20 (problem_id 194852)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
How many locations is Noah considering?
____ locations
[Image: The image is a decision tree diagram with three main branches labeled "space," "safari," and "comics." Each branch splits into two sub-branches: "skating rink" and "park." From each sub-branch, there are three additional branches pointing to the days "Fri," "Sat," and "Sun."]
```

### Answer 1: practices in order

**Answer: 2 locations** (skating rink and park).

## Practices to choose from

The NAEP 2026 Mathematics Framework lists five mathematical practices. You asked me to add Procedural Fluency from the NRC strands as a sixth:

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics
6. Procedural Fluency (NRC)

## Practices needed, in order

### 1. Representing (main practice)
The tree diagram gives all the information, so the work is mostly reading it correctly:
- Each level of the tree is one decision. The first level is the theme (space, safari, comics). The second level is the **location** (skating rink, park). The third level is the day (Fri, Sat, Sun).
- The student has to match the word "locations" to the second level. Themes and days are not locations.
- The student also has to know how tree diagrams work. "Skating rink" and "park" are drawn three times, once under each theme, but they are the same two places. The repetition only shows that each location can go with each theme.

The common mistakes come from this step:
- Counting all six second-level branches gives 6.
- Counting every path through the tree gives 3 × 2 × 3 = 18.
- Counting the wrong level gives 3 (themes or days).

### 2. Procedural Fluency (NRC)
Once the location level is found, the student counts the different options: skating rink and park, so **2**. The counting is trivial. Its only demand is counting distinct labels rather than branches.

## Practices not needed
- **Abstracting and Generalizing:** The question doesn't ask for the total number of combinations, so the student doesn't need the multiplication rule for counting. The repeated subtrees can be understood as part of reading the diagram (Representing).
- **Justifying and Proving:** There is no argument or explanation to give.
- **Mathematical Modeling:** The model (the tree) is already given. The student doesn't build one from a real situation.
- **Collaborative Mathematics:** This is an individual item.

## Summary
**Representing → Procedural Fluency.** Almost all of the difficulty is in Representing. Procedural Fluency is a very small final step.

### Answer 2: major practice

**Major practice: Representing.**

Almost all of the work is reading the tree diagram correctly. The student has to see that each level is one decision (theme, then location, then day) and match "locations" to the second level. They also have to understand that the "skating rink" and "park" branches repeated under each theme are the same two places.

All the likely wrong answers come from misreading the diagram:
- 3: counting the themes or the days instead of the locations
- 6: counting every location branch
- 18: counting every full path

Once the right level is found, the count itself is trivial. It is just "skating rink, park" = 2, so Procedural Fluency adds almost nothing to the difficulty.

---

## Row 21 (problem_id 131506)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Divide 4 1/2 by the following unit fraction.
1/6
____
```

### Answer 1: practices in order

**Problem:** Divide 4 1/2 by the unit fraction 1/6. **Answer: 27**

## Practices to choose from

From the NAEP 2026 Mathematics Framework:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC's *Adding It Up* strands:
6. Procedural Fluency

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Rewrites the mixed number 4 1/2 as the improper fraction 9/2. Rewrites "÷ 1/6" as "× 6/1" (multiply by the reciprocal). This only changes the form of the numbers, not their value. |
| 2 | **Procedural Fluency (NRC)** | Does the calculation correctly: 9/2 × 6 = 54/2 = 27, then simplifies to a whole number. |

**Order: Representing → Procedural Fluency**

## Optional practice (another way to solve it)

- **Abstracting and Generalizing:** A student who knows the general rule "dividing by a unit fraction 1/n is the same as multiplying by n" can skip the reciprocal step. They count how many sixths are in 4 1/2: 4 × 6 + 3 = 27. The words "unit fraction" in the problem point toward this structure. Still, a student can solve the problem without it, so I would tag it as secondary, not required.

## Practices not used

- **Justifying and Proving:** The problem doesn't ask students to explain or defend the answer.
- **Mathematical Modeling:** There is no real-world context to turn into math.
- **Collaborative Mathematics:** This is a single-student item.

**Tags for this item:** Representing (primary, first), Procedural Fluency (primary, second). Abstracting and Generalizing is an optional secondary tag.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- **The item is a bare computation.** "Divide 4 1/2 by 1/6" has no context, asks for no explanation, and has no pattern to find. It checks whether the student can carry out fraction division accurately.
- **Representing is only a setup step.** Changing 4 1/2 to 9/2 and ÷ 1/6 to × 6 is the standard first move of the division procedure. The item doesn't ask students to pick or interpret a representation, so it isn't really testing Representing.
- **Most wrong answers would be procedural errors.** Typical mistakes are multiplying by 1/6 instead of 6 (getting 3/4), mishandling the mixed number (for example, 4 × 6 + 1/2 = 24 1/2), or making an arithmetic slip. These are fluency errors, not representation errors.

**So the tags would be:** Procedural Fluency (major), Representing (minor, supporting step).

---

## Row 23 (problem_id 5669)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
The table shows five states and the lowest point in each state.
[Table:
State | Lowest Elevation (feet)
California | -282
Colorado | 3,350
Louisiana | -8
New Mexico | 2,842
Wyoming | 3,099]
Put the states in order by their lowest elevation, from least (1) to greatest (5).

Items to put in order:
- California
- Louisiana
- Wyoming
- Colorado
- New Mexico
```

### Answer 1: practices in order

## Practices for the state-elevation ordering problem

**The practice set I'm using:** the five mathematical practices in the 2026 NAEP Mathematics Framework, plus the NRC strand you asked for:

| Source | Practice |
|---|---|
| NAEP | Representing |
| NAEP | Abstracting and Generalizing |
| NAEP | Justifying and Proving |
| NAEP | Mathematical Modeling |
| NAEP | Collaborative Mathematics |
| NRC (*Adding It Up*) | Procedural Fluency: carrying out procedures accurately, efficiently and flexibly |

### Practices needed, in order

**1. Representing (NAEP)**
- Read the table and turn each elevation into a signed number. A negative elevation means the point is below sea level. California's -282 is 282 ft below sea level and Louisiana's -8 is 8 ft below. The other three are above sea level.
- Place these values on a vertical number line, with sea level at 0. "Least to greatest" then means "lowest to highest." This step is where students usually go wrong. A student who looks only at the digits will put -8 before -282, or will treat -282 as larger than 2,842 because it has a 2 and an 8 in it.

**2. Procedural Fluency (NRC)**
- Compare the integers using the standard procedure:
  - Every negative is less than every positive, so California and Louisiana come first.
  - For two negatives, the one with the larger absolute value is smaller, so -282 < -8.
  - For the positives, compare by place value. All three have 4 digits, so compare the thousands digit first (2 < 3), then the hundreds digit (0 < 3). This gives 2,842 < 3,099 < 3,350.
- Write the ordered list.

**Answer:**
1. California (-282)
2. Louisiana (-8)
3. New Mexico (2,842)
4. Wyoming (3,099)
5. Colorado (3,350)

### Practices not needed

- **Abstracting and Generalizing:** You could argue a student uses the general rule "larger absolute value means smaller negative number." But here the rule is only applied, not formed or extended, so it belongs under Procedural Fluency.
- **Justifying and Proving:** The item asks for no explanation or argument.
- **Mathematical Modeling:** The real-world quantities already come as numbers in a table. Nothing has to be built, assumed or checked against the context.
- **Collaborative Mathematics:** This is a task done alone.

**Summary sequence:** Representing → Procedural Fluency

### Answer 2: major practice

## Major practice: Procedural Fluency (NRC)

**Why this one:**
- **It is what the item mainly tests.** The task is to order five integers, two of them negative. Getting the right answer depends on doing the comparison correctly: every negative is less than every positive, -282 < -8, and 2,842 < 3,099 < 3,350.
- **Representing is light here.** The elevations are already given as signed numbers in a table. The student doesn't have to build a representation or switch from one to another, such as from words to symbols or from a table to a graph. The student only has to read the numbers and know that a negative sign means "below sea level." That small step supports the comparison rather than standing alone as a practice.
- **The likely errors are procedural.** Typical wrong answers come from mistakes in the comparison procedure. One is ordering negatives by absolute value, which puts -8 before -282. Another is ignoring the sign. These are not errors of interpretation.

**When I would pick Representing instead:** if the item showed the elevations on a number line or a diagram, or described them in words such as "282 feet below sea level." Then the main work would be turning the context into signed numbers.

---

## Row 24 (problem_id 199749)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of 24/25 ÷ 4/5.
____
```

### Answer 1: practices in order

**Problem:** Find the value of 24/25 ÷ 4/5.
**Answer:** 6/5 (also 1 1/5 or 1.2)

The practice list below combines the five mathematical practices in the 2026 NAEP Mathematics Framework with Procedural Fluency from the NRC's *Adding It Up* strands, as you asked:

- **NAEP:** Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics
- **NRC:** Procedural Fluency

This is a short, symbol-only computation, so it needs only two of these practices.

### Practices used, in order

**1. Representing**
- Read the symbolic expression: two fractions joined by the division operator.
- Turn it into an equivalent form that can be computed. This means rewriting division as multiplication by the reciprocal: 24/25 ÷ 4/5 = 24/25 × 5/4.
- This step changes the representation without computing anything, so it fits Representing rather than fluency.

**2. Procedural Fluency (NRC)**
- Carry out the algorithm accurately: (24 × 5)/(25 × 4) = 120/100.
  - A more fluent route is to cross-cancel first: (24/4) × (5/25) = 6 × 1/5 = 6/5.
- Simplify to lowest terms: 120/100 = 6/5.
- This is where the main work happens. The student needs to know the fraction-division procedure, multiply correctly, and reduce the result.

The final answer can be written as 6/5, 1 1/5 or 1.2. All three are correct because the item doesn't ask for a particular form.

**Sequence:** Representing → Procedural Fluency

### Optional (depends on strategy)

- **Abstracting and Generalizing:** This applies only if the student notices the structure: 4 divides 24 and 5 divides 25.
  - They could then use the general rule a/b ÷ c/d = (a÷c)/(b÷d) to get 6/5 directly.
  - This would replace the reciprocal step in Step 1, but the item doesn't require it.

### Not used

- **Justifying and Proving:** The item doesn't ask for an explanation or argument.
- **Mathematical Modeling:** There's no real-world context to turn into math.
- **Collaborative Mathematics:** It's an item a student solves alone.

**Summary for tagging:** Primary = Procedural Fluency; Secondary = Representing; Order = Representing → Procedural Fluency.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:

- **It's a bare computation.** "Find the value of 24/25 ÷ 4/5" has no context, no request for an explanation, no pattern to generalize and no choice of representation.
- **The calculation is the task.** The student has to know the fraction-division procedure (invert and multiply, or cross-cancel), carry it out correctly and reduce the result to 6/5.
- **Representing plays only a small part.** Rewriting ÷ 4/5 as × 5/4 is the first step of the standard procedure. A fluent student does it automatically, without consciously changing representations. So it fits better under Procedural Fluency than as a separate major practice.
- **It matches the likely errors.** Students who miss this item usually get the procedure wrong. For example, they divide without taking the reciprocal, flip the wrong fraction, make an arithmetic slip, or don't simplify. These are fluency errors, not representation or reasoning errors.

**Tag:** Procedural Fluency (major). If you allow a secondary tag, use Representing.

---

## Row 25 (problem_id 76591)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the quotient.
5 ÷ 3/10
____
```

### Answer 1: practices in order

**Problem:** Find the quotient. 5 ÷ 3/10

**Answer:** 50/3 = 16 2/3

## The practices available

The NAEP 2026 Mathematics Framework lists five mathematical practices:

1. **Representing**: moving between and working within forms such as symbols, numbers, pictures, number lines and words.
2. **Abstracting and Generalizing**: spotting structure or patterns and extending them to a general rule.
3. **Justifying and Proving**: building or checking a mathematical argument.
4. **Mathematical Modeling**: turning a real-world situation into math, solving it, and interpreting the result.
5. **Collaborative Mathematical Discourse**: building on, questioning or critiquing other people's reasoning.

As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands. It means carrying out procedures flexibly, accurately and efficiently.

## Practices this problem uses, in order

This is a bare computation item. It has no context, asks for no explanation, and shows no pattern to extend. So it uses only a few practices, and most of the work is procedural.

**Step 1: Representing**
- Read the symbolic expression and recode it into a form that can be computed. Write the whole number as a fraction, 5 = 5/1. Recognize that "÷ 3/10" means multiplying by the reciprocal, 10/3.
- Another approach that also counts as Representing is to write both numbers in tenths: 5 = 50/10. Then 50/10 ÷ 3/10 asks "how many 3-tenths fit in 50-tenths?", which is 50 ÷ 3.
- This step sets up the computation, so it comes first.

**Step 2: Procedural Fluency (NRC)**
- Carry out the algorithm correctly: 5 × 10/3 = 50/3.
- Convert to a mixed number if needed: 50 ÷ 3 = 16 remainder 2, so the answer is **16 2/3**.
- A fluent student also does a quick reasonableness check. Since 3/10 is a little less than 1/3, the answer should be a little more than 5 × 3 = 15, and 16 2/3 fits. This check is part of fluency, not a separate argument.

**Sequence: Representing → Procedural Fluency**

## Practices this problem doesn't use

- **Abstracting and Generalizing**: the student recalls the invert-and-multiply rule rather than deriving or generalizing it. No pattern or structure has to be found or extended.
- **Justifying and Proving**: the item asks for no explanation or argument.
- **Mathematical Modeling**: the item has no real-world context to translate.
- **Collaborative Mathematical Discourse**: the item gives no one else's reasoning to respond to.

## Summary

| Order | Practice | Role in this problem |
|---|---|---|
| 1 | Representing (NAEP) | Rewrite 5 ÷ 3/10 as 5/1 × 10/3, or as 50/10 ÷ 3/10 |
| 2 | Procedural Fluency (NRC) | Compute 50/3, convert to 16 2/3, and check that it is reasonable |

Under the NAEP 2026 framework, some coders could reasonably tag this item as **content-only**, with no practice beyond fluency. That is because the representation change is a routine part of the standard algorithm. If you need a single primary label, use **Procedural Fluency**, with **Representing** as a light secondary practice.

### Answer 2: major practice

**The major practice is Procedural Fluency (NRC).**

Why:

- **The item asks for one thing: compute the answer.** "Find the quotient" with a bare expression, 5 ÷ 3/10, tests whether a student can run the fraction-division procedure correctly: 5 × 10/3 = 50/3 = 16 2/3.
- **The Representing step is part of the standard algorithm.** Writing 5 as 5/1 and flipping 3/10 to 10/3 are built-in steps of invert-and-multiply. Students don't choose or interpret a representation, so Representing isn't really what's being measured.
- **Errors here are almost always procedural.** Common mistakes include inverting the wrong number (5/1 × 3/10 = 3/2, or 1/5 × 3/10), multiplying instead of dividing (15/10 = 3/2), or converting 50/3 to a mixed number wrong. All of these are fluency failures, not representation failures.
- **None of the other NAEP practices applies.** No context means no Modeling. No argument means no Justifying and Proving. No pattern to extend means no Abstracting and Generalizing.

If you need a tag from the five NAEP practices only, **Representing** is the closest fit, and it's a weak one. Under the NAEP 2026 framework, I'd mark this item as content-only, with no NAEP practice.

---

## Row 26 (problem_id 76716)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the quotient.
5 ÷ 9/10
____
```

### Answer 1: practices in order

**Problem:** Find the quotient. 5 ÷ 9/10

**Answer:** 50/9 = 5 5/9 (about 5.56)

### Practices I considered

From the 2026 NAEP Mathematics Framework:
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics

From the NRC's *Adding It Up* strands:
- Procedural Fluency

### Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Rewrites the problem in a form the division algorithm can use. The whole number 5 becomes 5/1, and "÷ 9/10" becomes "× 10/9" (multiply by the reciprocal). This is a change of symbolic form. The numbers stay the same. |
| 2 | **Procedural Fluency (NRC)** | Carries out the computation correctly: 5/1 × 10/9 = 50/9. Checks for common factors and finds none. Converts the improper fraction to a mixed number: 50 ÷ 9 = 5 remainder 5, so 5 5/9. This is the core of the item. |

The full sequence is **Representing → Procedural Fluency**.

### Practices not needed

- **Abstracting and Generalizing:** The student applies a rule they already know (invert and multiply). They don't build or extend a generalization.
- **Justifying and Proving:** The item asks for no argument or explanation. A strong student may do a quick check: dividing by a number less than 1 gives a result larger than 5, so 5 5/9 makes sense. That check is good habit, but the item doesn't require it.
- **Mathematical Modeling:** There is no real-world context to turn into math.
- **Collaborative Mathematics:** This is an individual computation item.

### Note

This is mainly a **Procedural Fluency** item. Representing plays a small supporting role at the start, where the student rewrites the whole number as a fraction and the division as multiplication. If you want only one practice tag for this item, use Procedural Fluency.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:

- **The item asks for a computation and nothing else.** It says "Find the quotient." There's no context to model, no argument to make, and no representation to choose or interpret.
- **Most of the work is procedural.** The student has to recall and run the fraction-division algorithm. They rewrite 5 ÷ 9/10 as 5 × 10/9, multiply to get 50/9, check whether it simplifies, and may convert it to 5 5/9. Each of these is a procedure done correctly and efficiently.
- **The Representing step is minor.** Writing 5 as 5/1 and turning division into multiplication by the reciprocal are routine parts of the algorithm. A fluent student does them without thinking about them as choices.
- **Errors here are procedural.** Typical mistakes include inverting the wrong number (5/1 × 9/10 = 9/2), inverting both numbers, or making a mistake in the mixed-number conversion. Students don't usually fail this item because they misread a representation.

If you tag the item with one practice, use **Procedural Fluency**.

---

## Row 28 (problem_id 36911)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A rectangular bathroom floor is covered with square tiles that are 1 1/2 feet by 1 1/2 feet. The length of the bathroom floor is 10 1/2 feet and the width is 6 1/2 feet.
How many tiles does it take to cover the width of the floor?
____ tiles
Express your answer in fraction form.
```

### Answer 1: practices in order

**Answer: 13/3 tiles** (6 1/2 ÷ 1 1/2 = 13/2 ÷ 3/2 = 13/3, which is 4 1/3 tiles)

The practices I'm drawing from:

- **NAEP 2026 Mathematics Framework practices:** Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics.
- **From NRC's *Adding It Up*:** Procedural Fluency.

### Practices needed, in order

| Step | Practice | What the student does in this problem |
|---|---|---|
| 1 | **Mathematical Modeling** (formulating) | Turns the tiling situation into a math question. The tiles go along one side, so the question is "how many 1 1/2 ft pieces fit in 6 1/2 ft?", which is a division (measurement or quotative division). The student has to see that only the **width** matters and ignore the length of 10 1/2 ft, which is a distractor. |
| 2 | **Representing** | Rewrites the quantities and the relationship in symbols. The mixed numbers become improper fractions (6 1/2 = 13/2, 1 1/2 = 3/2), giving the expression **13/2 ÷ 3/2**. Representing also comes back at the end, when the answer has to be written "in fraction form." |
| 3 | **Procedural Fluency** (NRC) | Divides the fractions correctly and efficiently by multiplying by the reciprocal: 13/2 × 2/3 = 26/6 = **13/3**, simplified to lowest terms. |
| 4 | **Mathematical Modeling** (interpreting and validating) | Reads the result back into the situation. 13/3 = 4 1/3 means 4 full tiles plus 1/3 of a tile. A quick check confirms it: 4 tiles cover 6 ft, and the leftover 1/2 ft is 1/3 of a 1 1/2 ft tile. The student then reports it in the requested form, **13/3**, rather than rounding to 5 tiles. |

**Sequence:** Mathematical Modeling (formulate) → Representing → Procedural Fluency → Mathematical Modeling (interpret/validate, with Representing used for the final fraction form)

### Practices that are not needed
- **Abstracting and Generalizing:** The problem doesn't ask for a pattern, a general rule, or a move from specific cases to a general one.
- **Justifying and Proving:** No argument or explanation is required. The step 4 check is self-monitoring, not a formal justification.
- **Collaborative Mathematics:** This is an individual item.

**Note:** This is a fairly routine context problem, so the modeling here is "light." It is a single-step translation, not a full open-ended modeling cycle. If you want to tag only the dominant practices, use **Representing** and **Procedural Fluency**, with **Mathematical Modeling** as the secondary one.

### Answer 2: major practice

**My pick for the major practice: Procedural Fluency (NRC).**

- **The setup is quick.** "How many 1 1/2 ft tiles fit across 6 1/2 ft" leads almost straight to dividing the width by the tile size. The only modeling decision is to ignore the 10 1/2 ft length. That is a single, familiar step, not a real modeling cycle.
- **The computation is most of the work.** The student has to:
  - rewrite both mixed numbers as improper fractions (13/2 and 3/2)
  - divide them by multiplying by the reciprocal (13/2 × 2/3 = 26/6)
  - simplify to 13/3

  Students are most likely to slip in these steps. For example, they may divide only the whole parts (6 ÷ 1 = 6), or forget to flip the divisor.
- **The required format points to the procedure.** "Express your answer in fraction form" asks for the exact result of the fraction calculation. A rounded count like 5 tiles would not be accepted, so the item is mainly checking the computation.

**Runner-up: Representing.** Rewriting the mixed numbers and writing 13/2 ÷ 3/2 is a real step. If you only want to use NAEP's own practices and leave out the NRC strand, I would pick **Representing** as the major practice.

---

## Row 29 (problem_id 469563)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the correct quotient.
____
```

### Answer 1: practices in order

**Note:** The problem you pasted only says "Find the correct quotient. ____". It doesn't include the dividend or divisor. They were probably in an image or in an earlier part of the problem. "Correct quotient" also suggests an earlier part showed a wrong answer for you to fix. So my answer below is for this kind of problem in general. If you send the actual numbers, I can make it specific.

## Practices available

**NAEP mathematical practices (2026 framework):** Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics.

**Added from NRC (*Adding It Up*):** Procedural Fluency, which means carrying out procedures accurately, efficiently and flexibly.

## Practices needed, in order

| Order | Practice | What the student does in this problem | Weight |
|---|---|---|---|
| 1 | **Representing** | Reads the division expression and sets it up in a form they can compute: names the dividend and divisor and writes the long-division layout. For decimals, they shift both decimal points by the same power of ten. For fractions, they rewrite the problem as multiplying by the reciprocal. | Secondary |
| 2 | **Procedural Fluency (NRC)** | Runs the division algorithm correctly: divide, multiply, subtract, bring down. They place the quotient digits and the decimal point correctly and handle any remainder. | **Primary** |
| 3 | **Justifying and Proving** | Checks the result with quotient × divisor (+ remainder) = dividend. If the problem showed someone's mistake, they also confirm the new answer fixes it. | Minor or optional |

## Practices not needed

- **Abstracting and Generalizing:** The student isn't asked to find a pattern or a general rule. It's a single calculation.
- **Mathematical Modeling:** There's no real-world situation to turn into math. The division is already given.
- **Collaborative Mathematics:** It's an individual fill-in-the-blank item, so there's no group reasoning involved.

## Summary

**Representing → Procedural Fluency → Justifying and Proving**

Procedural Fluency carries most of the weight. This is a routine, low-complexity computation item. Representing matters more if the numbers are decimals or fractions, because rewriting the problem is then a real step. If the item doesn't show an earlier wrong answer, the final checking step can be dropped. The problem then reduces to **Representing → Procedural Fluency**, or just **Procedural Fluency** for plain whole-number division.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item asks for one numeric answer, the quotient, and the only way to get it is to carry out the division algorithm correctly. That is what decides whether a student gets the item right or wrong.

The other two practices play smaller roles:
- **Representing** is a short setup step: identifying the dividend and divisor and writing the problem in a form you can compute. Once that's done, computing is the actual work.
- **Justifying and Proving** is only an optional check, such as multiplying the quotient by the divisor. The item doesn't ask for it and isn't scored on it.

Students who miss this item are most likely to have made a computation mistake: a wrong quotient digit, a misplaced decimal point, or a mishandled remainder. Those are all procedural fluency errors.

---

## Row 30 (problem_id 130932)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of 15/4 ÷ 5/8.
____
```

### Answer 1: practices in order

**Problem:** Find the value of 15/4 ÷ 5/8. **Answer: 6**

**Practices available** (the five NAEP 2026 Mathematical Practices, plus the one you added from NRC):
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics
- Procedural Fluency (NRC, *Adding It Up*)

## Practices needed, in order

**1. Representing (light use)**
The student first rewrites the division in a form they can compute. The usual choice is multiplying by the reciprocal:
15/4 ÷ 5/8 → 15/4 × 8/5
Another way is to use a common denominator: 30/8 ÷ 5/8 → 30 ÷ 5.
Both are symbolic-to-symbolic rewrites, so this is a small use of Representing. No translation to a picture, table, or context is needed.

**2. Procedural Fluency (main practice)**
Next the student carries out the procedure accurately:
- Cancel common factors: 15 and 5 become 3 and 1; 8 and 4 become 2 and 1
- Multiply: 3 × 2 = 6
- Simplify the result to a whole number: 6. (Without cancelling, it is 120/20 = 6.)

This is where nearly all of the work happens.

## Practices not needed
- **Abstracting and Generalizing:** The student applies a known rule but does not find a pattern or form a generalization.
- **Justifying and Proving:** The answer is a fill-in, so no explanation or argument is asked for. A student may check the answer (6 × 5/8 = 30/8 = 15/4), but the item does not require it.
- **Mathematical Modeling:** There is no real-world situation to turn into math. The item is a bare expression.
- **Collaborative Mathematics:** It is an individual task.

## Summary
**Representing → Procedural Fluency**

This is a low-complexity computation item. If you want one tag only, use **Procedural Fluency**. Rewriting division as "invert and multiply" is often taught as part of the procedure itself, so Step 1 can also be counted under Procedural Fluency.

### Answer 2: major practice

**Major practice: Procedural Fluency**

The item is a bare expression, 15/4 ÷ 5/8, with no context, no picture, and no request to explain the answer. To get it right, the student has to carry out the fraction-division procedure accurately: rewrite it as 15/4 × 8/5, cancel common factors, multiply, and simplify to 6.

The Representing step (rewriting the division as multiplication by the reciprocal) is minor and is usually taught as part of the procedure. A student can get the item wrong only by making a procedural error, such as flipping the wrong fraction or simplifying incorrectly. They do not need to choose a representation, form a generalization, build a model, or give a justification. So Procedural Fluency is the main practice.

---

## Row 31 (problem_id 131258)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Divide 4 1/2 by the following unit fraction.
1/8
____
```

### Answer 1: practices in order

**Problem:** Divide 4 1/2 by the unit fraction 1/8.
**Answer:** 4 1/2 ÷ 1/8 = **36**

### Practices available

The 2026 NAEP Mathematics Framework lists five mathematical practices:
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics

You asked me to add **Procedural Fluency** from the NRC strands (*Adding It Up*, 2001). It means carrying out procedures flexibly, accurately and efficiently.

### Practices in solving order

| Step | Practice | What the student does here |
|---|---|---|
| 1 | **Representing** | Rewrite the mixed number 4 1/2 as the improper fraction 9/2. The student can also picture the division as a quotitive question: "How many eighths fit in 4 1/2?" |
| 2 | **Abstracting and Generalizing** | Use the general rule that dividing by a unit fraction 1/n is the same as multiplying by n (that is, multiply by the reciprocal). Here, ÷ 1/8 becomes × 8. |
| 3 | **Procedural Fluency (NRC)** | Do the calculation: 9/2 × 8 = 72/2 = 36. Another route is 4 × 8 + (1/2) × 8 = 32 + 4 = 36. |
| 4 | **Justifying and Proving** (optional check) | Check the answer with the inverse operation: 36 × 1/8 = 36/8 = 4 1/2. Or reason that each whole holds 8 eighths, so 4 wholes hold 32 and the half holds 4, which gives 36. |

**Order:** Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving)

### Practices not used
- **Mathematical Modeling:** The problem is purely symbolic and has no real-world situation to model.
- **Collaborative Mathematics:** The problem is solved by one student, so it does not apply.

### Notes
- Steps 1 to 3 are required. Step 4 is a verification step that a careful student may do, but the item does not require it.
- Procedural Fluency carries most of the weight. Once the student has converted to 9/2 and applied the reciprocal rule, the rest is routine arithmetic.
- You could argue that step 2 is just part of Procedural Fluency, because many students apply "multiply by the reciprocal" as a memorized procedure. If you want a tighter tagging, use two practices: **Representing → Procedural Fluency**.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why this one:**
- **The item tests a procedure.** It gives a bare computation, 4 1/2 ÷ 1/8, with no context, no request for an explanation and no choice of representation. The student is graded only on the final number, 36.
- **The other steps are routine parts of that procedure.**
  - Changing 4 1/2 to 9/2 is technically Representing. But for a student at this level it is a standard first step of fraction division, not a real choice between representations.
  - "Dividing by 1/8 means multiplying by 8" is technically Abstracting and Generalizing. Most students, though, use it as a memorized rule (multiply by the reciprocal) rather than working the generalization out.
- **Most errors here are procedural.** Typical mistakes are:
  - multiplying by 1/8 instead of 8, which gives 9/16
  - working only with the whole number, which gives 4 × 8 = 32
  - converting the mixed number wrongly, for example 4 1/2 → 5/2

  All of these are slips in carrying out the procedure, not conceptual or reasoning failures.

**Runner-up:** Representing. If the item had been framed as "How many 1/8-cup servings are in 4 1/2 cups?", or if it asked students to use a model, Representing (or Mathematical Modeling) would become the major practice. In its current symbolic form, though, it is mainly a fluency item.

---

## Row 32 (problem_id 131386)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Divide 4 1/2 by the following unit fraction.
1/4
____
```

### Answer 1: practices in order

**Problem:** Divide 4 1/2 by the unit fraction 1/4. **Answer: 18**

**Practices to draw from**
- NAEP 2026 mathematical practices: Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics.
- From the NRC strands in *Adding It Up*: Procedural Fluency, which you asked me to add.

**Practices needed, in order**

1. **Representing (NAEP).** First, rewrite the problem in a form you can compute with:
   - Change the mixed number to an improper fraction: 4 1/2 = 9/2.
   - Rewrite the division as multiplication by the reciprocal: 9/2 ÷ 1/4 = 9/2 × 4/1. (You can also read it as "how many fourths fit in 4 1/2?")

2. **Procedural Fluency (NRC).** Then do the calculation accurately:
   - 9/2 × 4 = 36/2 = 18.
   - Check: 18 × 1/4 = 18/4 = 4 1/2. ✓

**Practices not needed**
- **Abstracting and Generalizing:** The student uses the rule "dividing by 1/n is the same as multiplying by n" but doesn't have to come up with it. Using a known rule counts as procedural fluency, not generalizing.
- **Justifying and Proving:** The problem asks only for a number, not an explanation or argument.
- **Mathematical Modeling:** The problem is purely numeric, with no real-world situation to turn into math.
- **Collaborative Mathematics:** There is no task that involves working with others or judging someone else's reasoning.

**Order:** Representing → Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The problem is a bare calculation: 4 1/2 ÷ 1/4. There's no context, no explanation to give, and no choice of method. It mainly tests whether the student can carry out the standard fraction-division steps correctly.
- The Representing step (4 1/2 → 9/2, and ÷ 1/4 → × 4) is itself part of that routine. It's a standard symbolic rewrite, not a translation between kinds of representations, like a picture, number line, or table.
- The likely errors are procedural: multiplying by 1/4 instead of 4, mishandling the mixed number (for example, getting 4 × 4 + 1/2), or making an arithmetic slip. A student who gets this wrong has usually broken the procedure, not misunderstood how to represent the problem.

**Secondary practice:** Representing (NAEP), for the mixed-number-to-improper-fraction conversion.

---

## Row 35 (problem_id 36501)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A zookeeper is 6 1/4 feet tall. A young giraffe in his care is 9 3/8 feet tall.
What fraction of the giraffe’s height is the zookeeper’s height?
____
Express your answer in fraction form.
```

### Answer 1: practices in order

**Answer:** (6 1/4) ÷ (9 3/8) = 25/4 ÷ 75/8 = 25/4 × 8/75 = 200/300 = **2/3**

## Practices available

**NAEP 2026 Mathematics Framework practices:**
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

**Added from NRC (*Adding It Up*):** Procedural Fluency, which means carrying out procedures flexibly, accurately, and efficiently.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (formulating) | Turns the word problem into math. "What fraction of the giraffe's height is the zookeeper's height" means zookeeper ÷ giraffe, so the expression is (6 1/4) ÷ (9 3/8). This is the key step. Students often get it backwards and compute 9 3/8 ÷ 6 1/4 = 3/2. |
| 2 | **Representing** | Rewrites the mixed numbers in a form you can compute with: improper fractions (25/4 and 75/8), or a common denominator (50/8 and 75/8). |
| 3 | **Procedural Fluency** (NRC) | Divides the fractions by multiplying by the reciprocal (25/4 × 8/75 = 200/300), or, with common denominators, takes 50/75. Then simplifies to lowest terms: **2/3**. |
| 4 | **Mathematical Modeling** (interpreting/validating) | Checks the result against the situation. The zookeeper is shorter than the giraffe, so the answer must be less than 1, and 2/3 is. Also 2/3 × 9 3/8 = 6 1/4 ✓. Writes the answer as a fraction, as the question asks. |

**Sequence:** Modeling → Representing → Procedural Fluency → (Modeling: interpret and check)

## Practices not needed
- **Abstracting and Generalizing:** no pattern or general rule is asked for. This is one specific calculation.
- **Justifying and Proving:** the student isn't asked to explain or defend the answer.
- **Collaborative Mathematics:** no other person's reasoning has to be evaluated or built on.

**Core practices for tagging:** Mathematical Modeling, Representing, Procedural Fluency. Modeling is the main thinking step. Representing and Procedural Fluency are where most computation errors happen.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

I called Modeling "the key step" earlier. I'd still pick Procedural Fluency as the major practice, for these reasons:

- **The modeling here is light.** It's one translation of a standard phrase: "what fraction of A is B" becomes B ÷ A. The student doesn't make assumptions, choose variables, or iterate. The NAEP Mathematical Modeling practice is about that full cycle, and this item uses only a sliver of it.
- **Most of the work is computation.** The student converts two mixed numbers (6 1/4 = 25/4, 9 3/8 = 75/8), divides by multiplying by the reciprocal, and simplifies 200/300 to 2/3. That's three or four steps where arithmetic slips can happen. The modeling step is just one.
- **The item points at the procedure.** "Express your answer in fraction form" tells you the item cares about a correctly computed and simplified fraction. The context is just a light story around a mixed-number division problem.
- **It's where students separate.** A student who sets up the problem correctly but can't divide mixed numbers reliably will get it wrong. Once the phrase is read correctly, everything else depends on fluency.

**Runner-up: Mathematical Modeling.** Choose it instead if your tagging is meant to capture the most common *conceptual* error. That error is reversing the ratio and getting 3/2. It's a formulation mistake, not a computation mistake.

Representing (rewriting the mixed numbers) is a step within the procedure here. It isn't a separate demand, so I wouldn't make it the major practice.

---

## Row 36 (problem_id 577269)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Here is a right triangle. What is its area?
____ cm^2
[Image: A right triangle. ]
```

### Answer 1: practices in order

The problem only needs two practices: **Representing** (NAEP), then **Procedural Fluency** (NRC).

The 2026 NAEP Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Procedural fluency comes from the NRC's *Adding It Up* strands.

## Order of practices

**1. Representing (NAEP)**
- Read the picture: find the right-angle mark and pick out the two legs. The legs are perpendicular, so they serve as the base and the height.
- If the hypotenuse is labeled, it is a distractor and isn't used.
- Link the picture to the formula A = ½ × base × height. The lengths are in cm, so the answer is in cm².
- If the triangle is drawn on a grid instead of labeled, counting the leg lengths also belongs to this step.

**2. Procedural Fluency (NRC)**
- Compute ½ × leg₁ × leg₂ correctly. Multiplying first and then halving, or halving one leg first, gives the same result.
- Write the result in cm² in the blank.
- If the picture gives only the hypotenuse and one leg, there is an extra step first: find the missing leg with the Pythagorean theorem. That step is also procedural fluency.

## Practices not needed

| Practice | Why it isn't used |
|---|---|
| Abstracting and Generalizing | The student only applies a known formula. There's no pattern to find or rule to generalize. It would apply only if the student worked out the formula by treating the triangle as half a rectangle. |
| Justifying and Proving | The item asks for a number, not an argument or explanation. |
| Mathematical Modeling | It is a plain geometric figure with no real-world situation to turn into math. |
| Collaborative Mathematics | It is an individual item with no shared reasoning. |

**Summary:** Representing → Procedural Fluency. Most of the difficulty is in Representing: choosing the two perpendicular sides and ignoring the hypotenuse. That is the most common mistake on this type of item.

I can't give the number because the side lengths are only in the image, which isn't included in the text.

### Answer 2: major practice

I'd choose **Procedural Fluency** as the major practice.

- **It's what the item asks for.** "What is its area?" with a cm² blank is a routine task: apply A = ½ × base × height and compute it. There's no argument, model or pattern to find. The student just has to carry out a known procedure correctly.
- **Representing is a smaller step here.** The right angle is given ("here is a right triangle"), and the student only has to read two lengths off the picture. That step comes first, but it's short.
- **It's where the answer succeeds or fails.** Typical mistakes are forgetting the ½, multiplying all three sides, or writing the wrong units. These are all errors in using the procedure.

**One exception:** if the picture labels the hypotenuse as a distractor, or the triangle is drawn on a grid so the student has to count lengths, then choosing the right sides matters more. In that case Representing could be the major practice. My earlier answer said most of the difficulty is in Representing, but that's only true in this case. Since I can't see the image, Procedural Fluency is the safer single label. Representing is a close second.

---

## Row 39 (problem_id 9946)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
If you are standing on a beach right next to the ocean, what is your elevation?
____
```

### Answer 1: practices in order

**Answer to the problem:** 0. You are at sea level, so your elevation is 0 feet (or 0 meters). Strictly speaking a beach sits a little above mean sea level, but the expected answer is 0.

## Practices considered

The five practices in the NAEP Mathematics Framework (2026), plus the one you asked me to add from the NRC's *Adding It Up*:

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematical Discourse
6. Procedural Fluency (NRC)

## Practices used, in order

**1. Mathematical Modeling (a light version)**
First the student reads the real-world situation and works out what is being measured. Elevation is height measured from a reference level, and that reference level is sea level. Standing right next to the ocean puts you at that reference level. This is the step that turns the beach scene into a math question. It's a small piece of modeling: there are no assumptions to make and no model to test.

**2. Representing**
Next the student puts that position on the number scale used for elevation. Points above sea level are positive, points below are negative, and sea level is **0**. This is the main skill the item tests: using signed numbers in a real-world context, with zero as the reference point (about the level of CCSS 6.NS.C.5).

**3. Procedural Fluency (NRC): barely used, if at all**
The problem involves no calculation, algorithm, or rule. The only "procedure" is writing down the value 0, maybe with units. If you have to tag it, put it last and give it very little weight. I would leave it untagged. What the student actually needs to know is that sea level is the zero point. In NRC terms that is **conceptual understanding**, not procedural fluency.

**Sequence:** Mathematical Modeling → Representing → (Procedural Fluency, trivial)

## Practices not used

- **Abstracting and Generalizing:** there is no pattern, structure, or general rule to find.
- **Justifying and Proving:** the item asks only for a value, not a reason.
- **Collaborative Mathematical Discourse:** it is a short-answer item done alone.

Overall, this is a low-complexity recall item. Representing does most of the work, with a small amount of interpreting the context (Modeling) before it.

### Answer 2: major practice

**Major practice: Representing.**

The item mainly checks whether the student knows how elevation is shown with numbers: sea level is the zero point, heights above it are positive and depths below it are negative. Once the student places "right next to the ocean" at sea level, the answer is just 0 on that scale.

The other two practices play a smaller role:
- **Mathematical Modeling** is only a quick reading of the context. There are no assumptions to choose, no model to build and no result to check against the situation.
- **Procedural Fluency** has almost nothing to work on because the problem has no computation or procedure.

So if the item gets one tag, it should be **Representing**.

---

## Row 40 (problem_id 242315)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
The area of a rectangle is 17 1/2 in^2 and its shorter side is 3 1/2 in.
What is the length of the longer side?
____ in
```

### Answer 1: practices in order

**Answer: 5 in** (17 1/2 ÷ 3 1/2 = 35/2 ÷ 7/2 = 35/7 = 5)

I used the five practices in the 2026 NAEP Mathematics Framework: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I added **Procedural Fluency** from the NRC's *Adding It Up* strands.

### Practices in the order they are used

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the words into math. The student sees that the area of a rectangle is length × width and writes the unknown side as 3 1/2 × L = 17 1/2, so L = 17 1/2 ÷ 3 1/2. A quick sketch of the rectangle with the short side labeled 3 1/2 also fits here. This is the step that sets up the problem. |
| 2 | **Procedural Fluency** (NRC) | Divides the mixed numbers correctly and efficiently. The student changes them to improper fractions (35/2 ÷ 7/2), multiplies by the reciprocal (35/2 × 2/7), and simplifies to 5. Converting to decimals (17.5 ÷ 3.5 = 5) also works. This is the main computation in the problem. |
| 3 | **Justifying and Proving** (NAEP), light use, optional | Checks the answer: 3 1/2 × 5 = 17 1/2, and 5 > 3 1/2, so 5 really is the *longer* side. This is a quick reasonableness check, not a full argument, so it is a minor or optional step. |

**Sequence:** Representing → Procedural Fluency → (Justifying and Proving, as a check)

### Practices that are not needed
- **Mathematical Modeling:** There is no real-world situation to simplify, no assumptions to make and no model to test. The rectangle and the area formula are given directly.
- **Abstracting and Generalizing:** The student only applies a known formula to one case. They don't find a pattern or extend a rule to a general class.
- **Collaborative Mathematics:** This is a single-student item with no group work.

### Notes for coding
- **Main practices:** Representing and Procedural Fluency. Both are needed to get the answer.
- **Hardest step:** Probably the fraction division in step 2. Common mistakes are dividing the whole numbers and fractions separately (17 ÷ 3 and 1/2 ÷ 1/2) or multiplying instead of dividing. Some students also misread step 1 and compute the perimeter instead of the area.
- **Complexity:** The item is low complexity. It is a familiar one-step inverse use of a formula, made harder only by the mixed-number arithmetic.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Here is why I'd pick it over Representing:

- **The difficulty is in the computation.** Setting up the problem is short and standard: area = length × width, so length = area ÷ width. Most students who know the area formula get this right away. The hard part is dividing mixed numbers: 17 1/2 ÷ 3 1/2 = 35/2 × 2/7 = 5.
- **Most errors come from the computation.** Students often divide the whole numbers and fractions separately, flip the wrong fraction, or make mistakes converting to improper fractions. Students who miss this item most likely miss it in this step.
- **The item seems built to test it.** A rectangle with a whole-number side would make the problem trivial. Using mixed numbers like 17 1/2 and 3 1/2 suggests the item is mainly checking fluency with fraction or decimal division in a measurement setting.

Representing is still needed, but only as a small first step. If you code only one practice for this item, use **Procedural Fluency**.

---

## Row 41 (problem_id 243107)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of 5/32 ÷ 25/4.
____
```

### Answer 1: practices in order

**Problem:** Find the value of 5/32 ÷ 25/4.
**Answer:** 1/40

**The practices I'm choosing from**

- NAEP Mathematics Framework (2026) has five practices: Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics.
- You asked me to add one from the NRC's *Adding It Up*: **Procedural Fluency**. This means carrying out procedures flexibly, accurately, efficiently and appropriately.

**Practices needed, in order**

This is a short symbolic computation, so only one practice is really needed.

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Procedural Fluency** (NRC) | Turns the division into multiplication by the reciprocal: 5/32 × 4/25. |
| 1 (cont.) | **Procedural Fluency** | Cancels common factors: 5 and 25 become 1 and 5, and 4 and 32 become 1 and 8. |
| 1 (cont.) | **Procedural Fluency** | Multiplies to get 1/40. |

An optional check, not needed for the answer: 5/32 ≈ 0.16 and 25/4 = 6.25, so the quotient should be about 0.025, which is 1/40. This is a reasonableness check. It is closer to NRC's adaptive reasoning than to any NAEP practice.

**Why the NAEP practices don't apply**

- **Representing:** The problem is given in symbols and answered in symbols. Nothing is translated between forms such as a diagram, number line, area model or story. Rewriting ÷ as × with the reciprocal is a step in the procedure, not a change of representation.
- **Abstracting and Generalizing:** The student uses a rule they already know. They don't find a pattern or extend one.
- **Justifying and Proving:** The problem asks for no explanation or argument.
- **Mathematical Modeling:** There is no real-world situation to model.
- **Collaborative Mathematics:** This is an individual item.

**For labeling:** Procedural Fluency only. In NAEP terms this is a low-complexity item. If your tagging scheme requires at least one NAEP practice per item, the closest fit is Representing, because the work is manipulating symbols. I would give it a low weight, because the item doesn't really test that practice.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item asks only for 5/32 ÷ 25/4 in symbols. Answering it means carrying out a known algorithm accurately:

1. Rewrite it as multiplication by the reciprocal.
2. Cancel common factors.
3. Multiply to get 1/40.

That is exactly what procedural fluency describes. The item has no context to model, no representation to translate, no pattern to generalize and no argument to make.

If you have to pick from the five NAEP practices only, I would choose **Representing**, because the work is manipulating symbols. It is a weak fit, though, and I would give it a low weight.

---

## Row 42 (problem_id 10585)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Use Priya’s method to calculate (0.0015) · (0.024).
____
```

### Answer 1: practices in order

**Problem:** Use Priya's method to calculate (0.0015) · (0.024).
**Answer:** 0.000036

**One assumption:** The problem doesn't say what Priya's method is, so it was probably shown in an earlier part. I'm assuming it's the usual one for this kind of problem:
1. Write each decimal as a whole number times a power-of-ten fraction.
2. Multiply the whole numbers.
3. Multiply the fractions.
4. Convert the result back to a decimal.

If her method is "multiply as whole numbers, then count the decimal places," the practices and their order below stay the same.

**The practices I chose from**
- **NAEP 2026 Mathematics Framework:** Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics.
- **Added from the NRC's *Adding It Up* (2001):** Procedural Fluency, which means carrying out procedures flexibly, accurately, efficiently and appropriately.

**Order of practices**

| Step | Practice | What the student does |
|---|---|---|
| 1 | Abstracting and Generalizing | Sees the general structure behind Priya's worked example: split each number into a whole number and a power of ten, then multiply the parts. Recognizes that the same structure works for these new numbers. |
| 2 | Representing | Rewrites the decimals in place-value form: 0.0015 = 15 × 1/10,000 and 0.024 = 24 × 1/1,000. |
| 3 | Procedural Fluency | Calculates 15 × 24 = 360 and (1/10,000) × (1/1,000) = 1/10,000,000. |
| 4 | Representing | Converts 360/10,000,000 back to decimal form: 0.000036. |
| 5 (optional) | Justifying and Proving | Checks that the answer is reasonable. Since 0.0015 × 0.02 = 0.00003, an answer of 0.000036 is the right size. |

**Short form:** Abstracting and Generalizing → Representing → Procedural Fluency → Representing → (Justifying and Proving, optional)

**How much each practice matters**
- **Representing and Procedural Fluency do most of the work.** The main tasks are switching between decimal and place-value or fraction forms and carrying out the multiplication correctly.
- **Abstracting and Generalizing plays only a small part.** The method is already given, so the student only has to apply it to new numbers rather than come up with it.
- **Justifying and Proving isn't required.** The problem asks only for the result, not an explanation, so the check in step 5 is extra.
- **Not used:**
  - Mathematical Modeling, because there is no real-world context.
  - Collaborative Mathematics, because the student works alone.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The problem gives the student a method and asks them to "calculate" with it. That makes it mainly a test of carrying out a known procedure accurately: split the decimals, multiply 15 × 24 = 360, multiply the powers of ten to get 1/10,000,000, and turn the result back into 0.000036. The student doesn't need to invent a strategy, explain why it works, or model a real situation.

**Close second: Representing.** Rewriting between decimal form and place-value form is part of the method. Here, though, the method already tells the student what to rewrite and how, so that step works as part of the procedure rather than as a separate representing decision.

---

## Row 47 (problem_id 102028)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A sixth-grade science club needs $180 to pay for the tickets to a science museum. All tickets cost the same amount.
Find the quotient.
____
```

### Answer 1: practices in order

## Practices for this problem, in order

The 2026 NAEP Mathematics Framework names five mathematical practices: **Representing**, **Abstracting and Generalizing**, **Justifying and Proving**, **Mathematical Modeling**, and **Collaborative Mathematics**. You asked me to add **Procedural Fluency** from the NRC's *Adding It Up*, so I've included it below.

**First, a note on the problem.** As written, it is missing a number. We know the club needs $180 in total and that every ticket costs the same. To "find the quotient," we also need the number of tickets (or students), or the price of one ticket. The original item probably had a table, an image, or another sentence that was lost. The practice sequence below holds for any number you fill in. For example, with 12 tickets the answer is 180 ÷ 12 = 15, or $15 per ticket.

### 1. Mathematical Modeling (formulate)
The student turns the real situation into a math problem. "A total cost shared equally among tickets" becomes an equal-groups (partitive) division: total cost ÷ number of tickets = cost per ticket. This step is about deciding which operation fits the situation.

### 2. Representing
The student writes the model down as a symbol expression, such as **180 ÷ n** (for example 180 ÷ 12). They might also use a tape diagram or a bar split into equal parts. The word "quotient" tells them that a division expression is the representation they need.

### 3. Procedural Fluency (NRC)
The student carries out the division accurately and efficiently. They might use long division, a fact they already know (18 ÷ 12 → 180 ÷ 12 = 15), or a partial-quotients method. **For this item, this is the main skill being tested.**

### 4. Mathematical Modeling (interpret and validate)
The student puts the result back into the situation: "Each ticket costs $15." Then they check that it makes sense. It should be a positive dollar amount below $180, and 15 × 12 = 180 should check out. This step finishes the modeling cycle that began in Step 1.

### Practices not needed here
- **Abstracting and Generalizing:** Not used. The problem asks for one specific quotient, not a general rule.
- **Justifying and Proving:** Only the light self-check in Step 4. The student isn't asked to explain or argue for the answer.
- **Collaborative Mathematics:** Not used. It's an individual task with one answer.

### Summary
**Mathematical Modeling (formulate) → Representing → Procedural Fluency → Mathematical Modeling (interpret/check)**

If you need one main practice for each step:
- Representing is the main practice for setting up the problem.
- Procedural Fluency is the main practice for finding the quotient.

### Answer 2: major practice

## Major practice: Procedural Fluency

If I had to choose one, I'd choose **Procedural Fluency** (the NRC practice).

**Why:**
- **The prompt asks for a calculation.** "Find the quotient" asks the student to compute an answer. It doesn't ask them to model, explain, or generalize. The question already says the operation is division, so the student doesn't have to work out which operation to use.
- **The modeling and representing steps are small.** Turning "shared equally among the tickets" into "total ÷ number of tickets" is a routine sixth-grade step, and the word "quotient" all but tells the student to divide. Most of the difficulty is in dividing correctly, for example 180 ÷ 12 = 15.
- **Errors would mostly come from the arithmetic.** A wrong answer most likely means a slip in long division or a misplaced digit or zero, not a misunderstanding of the situation. That is what procedural fluency covers.

**If you need a NAEP practice instead:** use **Representing**, because writing the situation as 180 ÷ n is the main thinking step before the calculation. Mathematical Modeling would be second. I'd still rate Procedural Fluency as the main practice for this item overall.

Caveat: the problem text is missing the number of tickets. If the full item added steps, such as working out the number of tickets from a table first, Representing or Modeling would become more important.

---

## Row 48 (problem_id 196019)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
How many different possible outcomes are in the sample space?
____ possible outcomes
[Image: The image is a decision tree diagram with three main branches labeled "space," "safari," and "comics." Each branch splits into two sub-branches: "skating rink" and "park." From each sub-branch, there are three additional branches pointing to the days "Fri," "Sat," and "Sun."]
```

### Answer 1: practices in order

**Answer: 18 possible outcomes** (3 themes x 2 places x 3 days = 18)

The NAEP 2026 Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. The list below also includes **Procedural Fluency** from the NRC's *Adding It Up* strands.

### Practices needed, in order

**1. Representing (NAEP)**
The student reads the tree diagram and works out what each level stands for:
- Level 1 is the theme: space, safari, comics (3 choices)
- Level 2 is the place: skating rink, park (2 choices for each theme)
- Level 3 is the day: Fri, Sat, Sun (3 choices for each place)

They also need to see that each outcome in the sample space is one complete path from the root to a leaf (for example, *space - park - Sat*). Without this, they might count the labeled nodes (3 + 2 + 3 = 8) by mistake.

**2. Abstracting and Generalizing (NAEP)**
The student sees that the tree has a repeating structure: every branch splits the same way. That means the number of outcomes is the product of the choices at each stage, which is the Fundamental Counting Principle. They no longer have to trace every path one by one.

**3. Procedural Fluency (NRC)**
The student carries out the calculation correctly and quickly: 3 x 2 = 6, then 6 x 3 = 18. They could also count the 18 leaves at the end of the tree. They enter **18**.

### Practices not needed
- **Justifying and Proving:** the item asks only for a number, not an explanation.
- **Mathematical Modeling:** the situation is already modeled for the student, because the tree is given. They don't have to build a model from a real-world context.
- **Collaborative Mathematics:** this is an individual item.

**Sequence:** Representing -> Abstracting and Generalizing -> Procedural Fluency

### Answer 2: major practice

**Major practice: Representing (NAEP)**

**Why Representing is the main practice:**
- **The question is mostly about reading the tree diagram.** The student has to understand that each outcome is one full path from the root to a leaf, combining a theme, a place and a day. Once they see that, the answer is close at hand.
- **It is the step students are most likely to get wrong.** Typical mistakes are adding the labels at each level (3 + 2 + 3 = 8), counting only the first branches (3), or counting the labels shown in the picture instead of the paths. All of these come from misreading the representation, not from doing the arithmetic badly.
- **The other two practices are optional here.** A student can skip the multiplication rule (Abstracting and Generalizing) and just count the 18 leaves, which works because the whole tree is drawn. The arithmetic (Procedural Fluency) is only 3 x 2 x 3, which is easy.

**One caveat:** Abstracting and Generalizing would become the main practice if the question took away the full diagram. Examples are a tree with "..." where branches are left out, or a question that asks for the count with a 4th day or another theme added. Then the student would have to use the counting principle instead of reading the answer off the picture. As the problem is written now, Representing is the main practice.

---

## Row 49 (problem_id 103383)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find a value for a that makes the statement true.
a ÷ 6 is equal to 1
____
```

### Answer 1: practices in order

**Problem:** Find a value for *a* that makes the statement true: *a* ÷ 6 = 1.
**Answer:** *a* = 6

**The practices to work with**

The NAEP 2026 Mathematics Framework lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematical Discourse

You asked me to add one practice from the NRC (*Adding It Up*) strands:
6. **Procedural Fluency**: carrying out procedures flexibly, accurately and efficiently.

**Practices used, in order**

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the symbolic statement "*a* ÷ 6 = 1" and understands that *a* is an unknown number. The student then rewrites the division as the related multiplication fact: *a* = 1 × 6. This could also be shown as "*a* split into 6 equal groups gives 1 in each group." |
| 2 | **Procedural Fluency (NRC)** | Uses the inverse relationship between division and multiplication to work out 1 × 6 = 6, so *a* = 6. A student who knows the fact "any number divided by itself is 1" can recall the answer directly. |
| 3 | **Justifying and Proving** | Substitutes the answer back into the statement to check it: 6 ÷ 6 = 1 is true, so *a* = 6 is correct. |

**Order:** Representing → Procedural Fluency → Justifying and Proving

**Practices not used**
- **Abstracting and Generalizing:** a single numeric case doesn't require the student to generalize. A student who does use the rule "*n* ÷ *n* = 1" is recalling a known fact, which counts as fluency here.
- **Mathematical Modeling:** there is no real-world context to model.
- **Collaborative Mathematical Discourse:** this is an individual task.

**Main practice:** Procedural Fluency. The item is basically a fact-recall or inverse-operation item. Representing is a light first step, and Justifying is an optional check.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why this one:**
- **It is where the item does most of its work.** To get *a* = 6, the student has to undo the division with the inverse operation (1 × 6 = 6) or recall the fact *n* ÷ *n* = 1. Both are quick, routine procedures, and the main thing the item checks is whether the student can do that accurately.
- **Representing is only a small step here.** The statement already comes in standard symbolic form, so the student just has to read it. There is no need to translate between forms or build a representation of their own.
- **Justifying is optional.** Checking that 6 ÷ 6 = 1 confirms the answer, but the item doesn't ask for it and the student can get the right answer without it.

If you have to pick from the five NAEP practices only, I would choose **Representing**. The student has to read *a* ÷ 6 = 1 as a statement about an unknown and connect it to the related multiplication fact. Among the NAEP practices, that is the closest match to what the item asks for.

---

## Row 50 (problem_id 12381)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate:
(1/2)^(-3)
____
```

### Answer 1: practices in order

**Problem:** Evaluate (1/2)^(-3)

**Answer:** 8

### Practices available
The NAEP Mathematics Framework (2026) lists these mathematical practices: **Representing**, **Abstracting and Generalizing**, **Justifying and Proving**, **Mathematical Modeling**, and **Collaborative Mathematics**. You asked me to add **Procedural Fluency** from the NRC's *Adding It Up* strands, so I've included it.

### Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Abstracting and Generalizing** | Sees that the expression is a case of the general rule for negative exponents: a^(-n) = 1/a^n, which gives (a/b)^(-n) = (b/a)^n. The student has to spot the structure (a fraction raised to a negative power) and connect it to that rule. |
| 2 | **Representing** | Changes the expression into an equivalent form: (1/2)^(-3) becomes 1/(1/2)^3, or (2/1)^3 = 2^3. Writing the same quantity a different way is the central move in this problem. |
| 3 | **Procedural Fluency (NRC)** | Does the arithmetic accurately: 2^3 = 2 × 2 × 2 = **8**. If they took the other path, (1/2)^3 = 1/8 and 1/(1/8) = 8. |

### Practices not used
- **Justifying and Proving**: The student doesn't have to explain why the rule works. They only need to apply it.
- **Mathematical Modeling**: There is no real-world context.
- **Collaborative Mathematics**: This is an individual item, and NAEP does not assess this practice directly.

**Summary order:** Abstracting and Generalizing → Representing → Procedural Fluency

*Note:* Many students who know this rule well apply it automatically. For them, steps 1 and 2 merge into one routine step, and the item becomes mostly **Representing + Procedural Fluency**. If you want only the main practices, use **Representing → Procedural Fluency**.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item says only "Evaluate." It has no context, does not ask for an explanation, and does not ask for a representation. All it checks is whether the student can apply a known rule correctly and get the right number.
- The key step, (1/2)^(-3) = 2^3, applies the negative-exponent rule a^(-n) = 1/a^n, a standard procedure. A student who knows the rule doesn't have to think about it; they just apply it and then compute 2^3 = 8.
- Wrong answers usually come from procedural mistakes, not conceptual ones. The common ones are -1/8, -8, 1/8, and -3/2, which come from treating the negative exponent as a negative sign, forgetting to take the reciprocal, or multiplying the base by the exponent. These are the errors a fluency item is meant to catch.

**Runner-up: Representing.** Rewriting the expression as a reciprocal is technically a change of representation. Here, though, the rewrite is a memorized rule, not a choice the student has to reason about. So it belongs under procedural fluency rather than being the main thing the item tests.

---

## Row 52 (problem_id 15627)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A gas company’s delivery truck has a cylindrical tank that is 14 feet in diameter and 40 feet long.
How much gas can fit in the tank?
____ cubic feet
Use 3.14 as an approximation for pi. Round your answer to the nearest whole.
```

### Answer 1: practices in order

## Practices to use for this problem

**The practices to choose from.** The NAEP 2026 Mathematics Framework names five mathematical practices:

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

From the NRC strands of mathematical proficiency (*Adding It Up*), I've added **Procedural Fluency**.

**The problem.** A cylindrical tank is 14 ft in diameter and 40 ft long. How much gas fits in it? Use pi = 3.14 and round to the nearest whole number.

### Practices in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** | Sees the real situation as a geometry problem. "How much gas can fit" means the tank's **volume**, and the tank is a **cylinder** whose "length" is its height. The answer must be in cubic feet. |
| 2 | **Representing** | Turns the words into math. They pick the formula V = πr²h, change the diameter into a radius (r = 14 / 2 = 7 ft), set h = 40 ft and π ≈ 3.14. |
| 3 | **Procedural Fluency (NRC)** | Does the arithmetic correctly and efficiently: r² = 49; 49 × 40 = 1,960; 1,960 × 3.14 = 6,154.4; rounded to the nearest whole, that is **6,154**. |
| 4 | **Mathematical Modeling** (check back in context) | Checks that the answer makes sense for the situation. It should be a volume in cubic feet, and it should be about the right size (about 3 × 50 × 40 ≈ 6,000). They also confirm the diameter was halved, since using 14 as the radius would give a value about 4 times too large. |

**Answer: about 6,154 cubic feet** (6,154.4 before rounding).

### Practices that are not really used

- **Abstracting and Generalizing:** Not needed. The student applies a known formula and does not build or extend a general pattern or rule.
- **Justifying and Proving:** Not needed. The item asks for a number, not an argument. The sense check in step 4 is light reasoning, but it is not justification in the framework's sense.
- **Collaborative Mathematics:** Not needed. This is an individual item.

**Summary sequence:** Mathematical Modeling, then Representing, then Procedural Fluency, then Mathematical Modeling again to interpret and check the answer. Representing and Procedural Fluency carry most of the load. The main mistake to watch for is diameter versus radius, which is a Representing error.

### Answer 2: major practice

## Major practice: Procedural Fluency (NRC)

If I had to pick one, it would be **Procedural Fluency**.

**Why:**

- **The problem mostly asks for a standard procedure.** It tells the student the shape (a cylinder) and gives both dimensions. It also says which value of π to use and how to round. What remains is to recall V = πr²h, halve the diameter, and compute 3.14 × 7² × 40 = 6,154.4, which rounds to 6,154. This is the core of procedural fluency: carrying out a known procedure accurately and efficiently.
- **Most errors happen during the procedure.** The likely mistakes are using 14 as the radius, squaring wrong, multiplying wrong, or rounding wrong. These are all slips in carrying out the procedure, not in understanding the situation.
- **Mathematical Modeling is light here.** The real-world setting is thin. "How much gas can fit" maps straight onto "volume of a cylinder," with no assumptions to make and no choices about the model. A full NAEP modeling task would make the student set up and interpret the model themselves.
- **Representing is a close second.** Turning "14 feet in diameter, 40 feet long" into r = 7 and h = 40 in the formula is a real step, and it is where the diameter-versus-radius trap sits. Still, it is a small translation step in a problem whose main demand is the calculation.

**In short:** Procedural Fluency is the main practice, Representing is secondary, and Mathematical Modeling plays only a minor role.

---

## Row 54 (problem_id 14749)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the product. If you get stuck, draw an area diagram to help.
(5.6) ⋅ (1.8)
____
```

### Answer 1: practices in order

**Problem:** Calculate (5.6) · (1.8). If you get stuck, draw an area diagram to help.

**Practices available.** The NAEP Mathematics Framework (2026) lists five mathematical practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling and (5) Collaborative Mathematics. The sixth one here is **Procedural Fluency** from the NRC's *Adding It Up* strands.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Procedural Fluency** (NRC) | Use the standard algorithm for multiplying decimals. Multiply the numbers as whole numbers: 56 × 18 = 1008. Then count the decimal places in the factors (1 + 1 = 2) and place the decimal point: **10.08**. |
| 2 | **Representing** (NAEP), used if the student gets stuck | Change the expression into an area model. Split each factor by place value: 5.6 = 5 + 0.6 and 1.8 = 1 + 0.8. Draw a rectangle with these side lengths, divided into 4 smaller rectangles. |
| 3 | **Procedural Fluency** (NRC), applied again to the diagram | Find each partial product and add them: 5 × 1 = 5, 5 × 0.8 = 4, 0.6 × 1 = 0.6, 0.6 × 0.8 = 0.48. The total is 5 + 4 + 0.6 + 0.48 = **10.08**. |
| 4 | **Justifying and Proving** (NAEP), light or optional | Check that the answer is reasonable. The product should be between 5 × 1.8 = 9 and 6 × 1.8 = 10.8, and 10.08 is in that range. The area model also shows *why* the decimal goes where it does. |

**Main path:** Procedural Fluency alone is enough for a student who knows the algorithm.
**Path the prompt suggests when stuck:** Representing → Procedural Fluency → (Justifying).

## Practices not needed
- **Abstracting and Generalizing:** the student does not have to state or extend a general rule.
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** this is an individual computation task.

**Answer:** (5.6)(1.8) = **10.08**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- **The task is to compute.** The prompt says "Calculate the product." Success means getting 10.08 correctly and efficiently: multiply 56 × 18 = 1008, then place the decimal point.
- **The diagram is optional.** It is offered only "if you get stuck," so Representing is a fallback, not the main demand. Even with the diagram, the student still has to calculate and add the partial products (5 + 4 + 0.6 + 0.48), and that is procedural work again.
- **There is nothing else to explain or model.** There is no context to turn into math, no generalization to make and no argument to write. The other NAEP practices play at most a minor role.

**Secondary practice:** Representing (NAEP), through the area diagram the prompt suggests.

---

## Row 55 (problem_id 15038)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the product. If you get stuck, draw an area diagram to help.
(0.008) ⋅ (7.2)
____
```

### Answer 1: practices in order

**Problem:** Calculate (0.008) · (7.2). If you get stuck, draw an area diagram to help.

**Answer:** 0.0576

## Practices available

The 2026 NAEP Mathematics Framework lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

As you asked, I've added a sixth: **Procedural Fluency** from the NRC's *Adding It Up*. It means carrying out procedures flexibly, accurately and efficiently.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Procedural Fluency** (main practice) | Ignore the decimal points and multiply the whole numbers: 8 × 72 = 576. Count the decimal places in the factors: 3 in 0.008 and 1 in 7.2, so 4 in total. Place the decimal point: **0.0576**. |
| 2 | **Representing** (optional, only if stuck) | Draw an area diagram as the problem suggests. Split 7.2 into 7 + 0.2 and find each part: 0.008 × 7 = 0.056 and 0.008 × 0.2 = 0.0016. Add them: 0.056 + 0.0016 = 0.0576. This moves the multiplication into a picture that shows the distributive property. |
| 3 | **Justifying** (light, as a check) | Check the answer by estimating: 0.008 is about 0.01, and 0.01 × 7.2 = 0.072. The answer should be slightly smaller than that, and 0.0576 is. This confirms the decimal point is in the right place. |

## Practices not needed
- **Abstracting and Generalizing:** the student doesn't have to state a general rule. Using the decimal-place rule is part of procedural fluency.
- **Mathematical Modeling:** there is no real-world situation in the problem.
- **Collaborative Mathematics:** the student works alone.

## Summary
**Procedural Fluency → (Representing, only if stuck) → Justifying (reasonableness check)**

Procedural fluency is the main practice. The problem offers Representing through the area diagram as a fallback, not as a required step. A student who multiplies fluently can solve it using only Procedural Fluency.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- **The task:** the problem says "Calculate the product." It is a bare computation, 0.008 × 7.2, with no context, no explanation and no proof required.
- **The skills:** to answer it, a student must carry out decimal multiplication accurately. That means multiplying 8 × 72 = 576, counting the 4 decimal places and writing 0.0576. Each of these is a procedural skill.
- **The area diagram is optional.** "If you get stuck" offers the diagram as a scaffold, not as a required step. Many students will never draw it, so Representing is a secondary practice at most.
- **Mistakes come from the procedure.** The usual wrong answers are about where the decimal point goes, such as 0.576 or 0.00576. Those are procedural errors.

Representing would be the major practice only if the problem required students to draw or interpret the area model. It doesn't, so Procedural Fluency is the major practice.

---

## Row 56 (problem_id 15760)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A salesperson sold a car for $18,250 and their commission is $693.50. What percentage of the sale price is their commission?
____ %
```

### Answer 1: practices in order

**Answer: 3.8%** (693.50 ÷ 18,250 = 0.038)

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Below are the ones this problem uses, plus NRC Procedural Fluency, in the order a student would use them.

1. **Mathematical Modeling**: turn the sales situation into a percent relationship. Commission is a part of the sale price, so commission = p% × sale price. The student has to see that $18,250 is the whole, $693.50 is the part, and the unknown is the rate.

2. **Representing**: write that relationship in symbols, either as the fraction 693.50 / 18,250 or as the equation (p/100) × 18,250 = 693.50.

3. **Procedural Fluency (NRC)**: do the arithmetic correctly and efficiently.
   - 693.50 ÷ 18,250 = 0.038
   - Convert the decimal to a percent: 0.038 × 100 = **3.8**

4. **Justifying and Proving** (a light check, often skipped): confirm the answer makes sense. For example, 1% of 18,250 is 182.50, so 4% is 730. Since 693.50 is a little under 730, an answer a little under 4% is reasonable. You can also check directly: 0.038 × 18,250 = 693.50.

**Not used:** Abstracting and Generalizing (the problem asks for no general rule or pattern) and Collaborative Mathematics (it is an individual item).

**Order:** Mathematical Modeling → Representing → Procedural Fluency → (Justifying and Proving)

The main step is the first one: modeling the context as a part ÷ whole percent problem. After that, the work is mostly procedural fluency (dividing decimals and converting to a percent).

### Answer 2: major practice

**My pick: Procedural Fluency (NRC).**

This changes what I said before. Earlier I called modeling the "main step." But for one major practice, I would pick Procedural Fluency, for these reasons:

- **The setup is routine.** "What percentage of the sale price is the commission?" is the standard *part ÷ whole* percent question. The words "percentage of the sale price" tell you which number is the whole. The student builds no real model: no assumptions, no choice of variables, nothing to interpret in the context. That makes Mathematical Modeling a small step, not the main one.
- **The work and the likely mistakes are in the computation.** Students get this wrong by:
  - dividing 693.50 by 18,250 incorrectly (with this decimal and these sizes, it is easy to misplace the decimal point and get 0.38 or 0.0038)
  - forgetting to multiply by 100 and answering 0.038 instead of 3.8
  - dividing the wrong way (18,250 ÷ 693.50)

  The first two are plainly procedural. The third is a setup error, but it is the simple part/whole convention, not modeling.
- **The answer blank is labeled "____ %".** So the item checks whether the student can carry out the percent procedure and the decimal-to-percent conversion correctly. It does not check whether they can formulate a model.

**Runner-up:** Mathematical Modeling, if you want to credit turning the sales context into a part/whole relationship. Representing and Justifying and Proving play only a minor role here.

---

## Row 57 (problem_id 15234)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Three cylinders have a volume of 2826 cm^3.
Cylinder A has a height of 900 cm.
Cylinder B has a height of 225 cm.
Cylinder C has a height of 100 cm.
Find the radius of the cylinder. Use 3.14 as an approximation for π.
Cylinder C has a radius of ____ cm
```

### Answer 1: practices in order

## Solution

V = πr²h, so 2826 = 3.14 · r² · 100
→ 2826 = 314 · r²
→ r² = 9
→ **r = 3 cm**

(Cylinders A and B are not needed to answer the question about Cylinder C.)

## Practices used, in order

The NAEP mathematical practices (2026 framework) are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. This problem calls for two of them, plus NRC Procedural Fluency:

| Order | Practice | What the student does in this problem |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the word problem into symbols. The student picks out what applies to Cylinder C (V = 2826, h = 100), ignores A and B, and writes the volume formula V = πr²h with π ≈ 3.14: **2826 = 3.14 · r² · 100**. |
| 2 | **Procedural Fluency** (NRC) | Solves the equation correctly and efficiently: 3.14 × 100 = 314, then 2826 ÷ 314 = 9, then √9 = 3. |
| 3 | **Justifying and Proving** (NAEP), *light / optional* | Checks the answer by substituting it back: 3.14 × 3² × 100 = 2826. ✓ This step isn't needed to get the answer, but it confirms it. |

**Not really used:**
- **Mathematical Modeling**: the problem is already a mathematical object, not a real-world situation that has to be modeled.
- **Abstracting and Generalizing**: you would need it only to see the general pattern across all three cylinders (same volume, so r² ∝ 1/h, giving radii of 1, 2 and 3 cm). The question asks only about C.
- **Collaborative Mathematics**: this is an individual item.

**Core sequence:** Representing → Procedural Fluency (→ optional Justifying check).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- **The representing step is small.** The problem gives every value directly (V = 2826, h = 100, π ≈ 3.14). Setting up the equation is just recalling the standard formula V = πr²h and filling in the numbers. No unusual translation or choice of representation is needed.
- **The procedure is where students get it right or wrong.** The answer depends on running the procedure accurately: multiply 3.14 × 100 = 314, divide 2826 ÷ 314 = 9, and then take the square root to get r = 3. Students most often make one of two slips. They stop at r² = 9 and answer 9, or they make an arithmetic error in the decimal division.
- **It is a routine item.** Solving the volume formula backward for r is a standard, well-practiced procedure. That is exactly what procedural fluency describes.

Representing is the secondary practice. It is needed to start the problem, but it is not where the difficulty lies.

---

## Row 59 (problem_id 21711)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Write the expression with fewer terms.
10x − 2x
____
```

### Answer 1: practices in order

**Problem:** Write the expression with fewer terms: 10x − 2x
**Answer:** 8x

## Practices available

The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

You asked me to add a sixth from the NRC's *Adding It Up* strands:
6. **Procedural Fluency**: carrying out procedures flexibly, accurately and efficiently.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Abstracting and Generalizing** | The student sees that 10x and 2x are like terms because they share the variable x. That means they can be combined with the general rule ax − bx = (a − b)x, which is the distributive property. |
| 2 | **Procedural Fluency** (NRC) | The student applies the rule correctly: (10 − 2)x = 8x. They subtract the coefficients and keep the variable. |

So the sequence is **Abstracting and Generalizing → Procedural Fluency**.

## Practices not needed

- **Representing**: The expression is already given in symbols. The student doesn't have to translate between representations such as words, tables, graphs or symbols.
- **Justifying and Proving**: The student only has to write the simplified expression, not explain or defend why it is equivalent.
- **Mathematical Modeling**: There's no real-world situation to turn into math.
- **Collaborative Mathematics**: This is a single-student item, so there's no communication or teamwork involved.

**Note:** Procedural Fluency carries most of the load in this item. A student who has practiced combining like terms will often do Step 1 automatically. Students who write answers like "8" (dropping the x) or "8x²" are usually failing on Step 1 (what like terms are and what combining means), not on the arithmetic 10 − 2.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Here's why it beats Abstracting and Generalizing for this item:

- **The item is a routine skill exercise.** "Write the expression with fewer terms" with 10x − 2x tests one standard procedure: combining like terms. Nothing about it is new or unfamiliar to the student.
- **The structural step is very small.** Both terms have exactly the same variable part (x), and there are no distractors. There are no unlike terms, constants, exponents or negative coefficients to sort out, so spotting the like terms takes almost no generalizing. For a student who has learned the procedure, that recognition is simply part of it.
- **What the item measures is accurate execution.** Getting it right means correctly producing (10 − 2)x = 8x and keeping the variable. That is accurate, efficient application of a learned procedure, which is how the NRC defines procedural fluency.

Abstracting and Generalizing would be the major practice in a related item. Examples are an expression with mixed terms such as 10x + 3 − 2x + y, or a question asking why ax − bx = (a − b)x works for any a and b. Here it plays only a minor, supporting role.

---

## Row 61 (problem_id 22023)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression:
(-1) · 2 · 3
____
```

### Answer 1: practices in order

**Problem:** Evaluate (-1) · 2 · 3

**Answer:** -6

## Practices available

NAEP 2026 Mathematics Framework, Mathematical Practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC strands of proficiency (*Adding It Up*, 2001):
6. Procedural Fluency

## Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (light) | Reads the symbolic expression correctly. The student has to see that "·" means multiplication and that (-1) is a negative factor in a product of three numbers, not a subtraction. |
| 2 | **Procedural Fluency** (main) | Carries out the computation accurately: multiplies left to right, (-1)·2 = -2, then -2·3 = -6. Or multiplies 2·3 = 6 and applies the sign rule (one negative factor gives a negative product) to get -6. |

**Order:** Representing → Procedural Fluency

## Practices not needed

- **Abstracting and Generalizing:** no pattern or general rule has to be found. The sign rule is only applied, not derived.
- **Justifying and Proving:** the student isn't asked to explain or justify the result.
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** this is an individual computation.

## Summary

This is mostly a **Procedural Fluency** item. Its only extra demand is a small Representing step: reading the notation and the negative sign correctly before computing. In practice, the most likely mistake is getting the sign wrong (answering 6), which is a procedural fluency error.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The main thing this problem tests is whether the student can carry out a known procedure accurately: multiply the integers and apply the sign rule (one negative factor gives a negative product), so (-1) · 2 · 3 = -6.

There is a Representing step, but it's very small. Reading the "·" as multiplication and (-1) as a negative factor is routine notation, not a task of translating between representations. Nothing in the problem asks for modeling, generalizing, or justifying. The likely error is a wrong sign (answering 6), and that is a procedural mistake.

---

## Row 62 (problem_id 22103)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Here are some scenarios:
- According to market research, a business has a 75% chance of making money in the first 3 years.
- According to lab testing, 5/6 of a certain kind of experimental light bulb will work after 3 years.
- According to experts, the likelihood of a car needing major repairs in the first 3 years is 0.7.
Order the scenarios in order of likelihood from least (1) to greatest (3) after three years.

Items to put in order:
- the light bulb still works
- the car needs major repairs
- the business makes money
```

### Answer 1: practices in order

## Practices available

**NAEP Mathematics Framework (2026) mathematical practices:**
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

**Added from NRC (*Adding It Up*):**
6. Procedural Fluency: carrying out procedures such as conversions and calculations accurately and efficiently

## The problem in short

Three probabilities are given in three different forms:
- Business makes money: **75%** (percent)
- Light bulb still works: **5/6** (fraction)
- Car needs major repairs: **0.7** (decimal)

You have to order them from least to most likely.

## Practices to use, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (light use) | Reads each real-world statement as a probability of the named event. For example, "5/6 of the bulbs will work after 3 years" becomes P(bulb still works) = 5/6, and "likelihood of a car needing major repairs is 0.7" becomes P(car needs repairs) = 0.7. The events to order match the events stated, so no complement is needed. That step is easy, but it is the bridge from the context to the math. |
| 2 | **Representing** (central practice) | Notices that the three values are in different representations (percent, fraction, decimal) and picks one common form to compare them in, e.g. all decimals: 75% → 0.75, 5/6 → 0.833..., 0.7 → 0.70. Moving flexibly between equivalent representations is the main idea of this item. |
| 3 | **Procedural Fluency** (NRC) | Does the actual conversions correctly: 75% ÷ 100 = 0.75, and 5 ÷ 6 = 0.8333... (or knows the benchmark that 5/6 is about 83%). Then compares the decimals: 0.70 < 0.75 < 0.833. |
| 4 | **Justifying and Proving** (light, optional) | Checks the order and could explain it: "0.7 = 70%, which is less than 75%, and 5/6 ≈ 83%, so the order is car, business, bulb." On a selected-response or ordering item this justification is implicit rather than written out. |

**Not really needed:** *Abstracting and Generalizing* (the student doesn't generalize a pattern or structure) and *Collaborative Mathematics* (it's an individual item).

## Answer

1. (least likely) **the car needs major repairs**: 0.7 = 70%
2. **the business makes money**: 0.75 = 75%
3. (most likely) **the light bulb still works**: 5/6 ≈ 83.3%

## Summary of the order

**Mathematical Modeling → Representing → Procedural Fluency → (Justifying and Proving)**

The two practices that do the real work are Representing and Procedural Fluency. Modeling is a short interpretation step at the start, and justifying is a brief check at the end.

### Answer 2: major practice

## Major practice: **Representing**

The whole problem is built around the fact that the three probabilities come in three different representations: a percent (75%), a fraction (5/6), and a decimal (0.7). To solve it, the student has to see that these forms can't be compared as written and then put them into one common form, such as 0.75, 0.833..., and 0.70. Once that's done, ordering them is easy.

Why not the others:
- **Procedural Fluency** is needed to carry out the conversions, mainly 5 ÷ 6 ≈ 0.833. But it only serves the representational move. The arithmetic is routine, and the item doesn't test computational skill for its own sake.
- **Mathematical Modeling** is minimal. Each statement already gives the probability of the event to be ordered, so the student doesn't build a model.
- **Justifying and Proving** is at most an implicit check. The student isn't asked to explain anything.

So if I have to pick one, it's **Representing**: translating between equivalent percent, fraction, and decimal forms to compare likelihoods. That's the core of this item. Procedural Fluency would be my second choice.

**Answer (least → greatest):** car needs major repairs (0.7) → business makes money (0.75) → light bulb still works (5/6 ≈ 0.833).

---

## Row 63 (problem_id 22322)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression:
(-1) · (-2) · 3
____
```

### Answer 1: practices in order

**Problem:** Evaluate (-1) · (-2) · 3

**Practices available:** the NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands.

## Practices needed, in order

**1. Abstracting and Generalizing (NAEP)**
Before doing any arithmetic, the student has to recognize the structure: this is a product of signed integers. The general sign rule applies. A product with an even number of negative factors is positive. Here there are two negative factors, (-1) and (-2), so the result will be positive. Using the general rule here is what makes this practice the right one, rather than just recalling a fact.

**2. Procedural Fluency (NRC)**
Next the student carries out the multiplication accurately and efficiently:
- (-1) · (-2) = 2
- 2 · 3 = **6**

You can also multiply the absolute values (1 · 2 · 3 = 6) and attach the sign from step 1.

**Answer: 6**

## Practices not needed
- **Representing:** the expression is already in symbolic form, and there's nothing to translate between representations.
- **Justifying and Proving:** the item doesn't ask for any explanation or argument.
- **Mathematical Modeling:** there's no real-world situation to model.
- **Collaborative Mathematics:** this is a task done alone.

**Summary sequence:** Abstracting and Generalizing → Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Evaluating (-1) · (-2) · 3 is mostly a matter of carrying out a familiar procedure: multiply integers correctly and apply the sign rule. The sign rule (two negatives make a positive) is something a student at this level should know automatically as part of the procedure. It isn't a new generalization they work out during the problem. Getting the item right depends on doing the computation accurately and efficiently, and that is what procedural fluency means.

Abstracting and Generalizing plays a small supporting role at most. If I could tag only one practice, I'd tag Procedural Fluency.

---

## Row 64 (problem_id 22552)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression:
(-1) · (-2) · (-3)
____
```

### Answer 1: practices in order

**Problem:** Evaluate (-1) · (-2) · (-3)
**Answer:** -6

**Practices available.** The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. You asked me to add one more, NRC's Procedural Fluency.

**Practices needed, in order**

1. **Representing (minor).** Read the notation correctly. The "·" means multiplication, and the parentheses mark each number as a negative factor rather than a subtraction. This is a quick translation step, so it carries little weight.

2. **Abstracting and Generalizing (moderate).** Use the general sign rule for products. A negative times a negative is positive. More generally, a product with an odd number of negative factors is negative. Here there are three negative factors, so the result must be negative. A student can also apply the rule step by step: (-1)(-2) = +2, and then 2 · (-3) = -6.

3. **Procedural Fluency (NRC, primary).** Carry out the multiplication accurately: 1 · 2 · 3 = 6. Then attach the sign from step 2 to get **-6**. This is the main practice in the problem. It is a routine one-step computation with integers, and it rests on knowing the integer multiplication rules well.

**Not needed.** Mathematical Modeling has no real-world context to model. Justifying and Proving is not needed because the item asks for no explanation. Collaborative Mathematical Discourse does not apply to a single-answer item.

**Summary of order:** Representing → Abstracting and Generalizing (sign rule) → Procedural Fluency. Procedural Fluency is the main practice, and the item has low mathematical complexity.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

This item asks for a routine computation and nothing else: evaluate (-1) · (-2) · (-3) = -6. It has no context to model, nothing to justify, and no new representation to build. To succeed, a student needs to know the integer sign rules and apply them accurately and efficiently. That is exactly what procedural fluency covers.

The other practices only play a small part:
- **Representing** is just reading "·" as multiplication.
- **Abstracting and Generalizing** (the sign rule) shows up here as a rule the student recalls and applies. The student is not generalizing anything new, so it fits better as part of procedural fluency than as a separate practice.

If you are limited to the five NAEP practices, I would pick **Abstracting and Generalizing**, because applying the sign rule is the key step. With Procedural Fluency available, though, it is clearly the best fit.

---

## Row 66 (problem_id 25949)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the area of the rectangle with the following side lengths.
7/6 in and 6/7 in
____ square inch
```

### Answer 1: practices in order

**Problem:** Find the area of a rectangle with side lengths 7/6 in and 6/7 in.

**Answer:** 7/6 × 6/7 = 42/42 = **1 square inch**

## Practices used, in order

The NAEP 2026 mathematical practices are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Procedural Fluency comes from the NRC strands of mathematical proficiency.

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the geometric description (a rectangle with two given side lengths) into a symbolic expression with the area formula: A = length × width = 7/6 × 6/7. |
| 2 | **Procedural Fluency** (NRC) | Multiplies the fractions correctly and efficiently: numerators 7 × 6 = 42, denominators 6 × 7 = 42. Simplifies 42/42 to 1, or cross-cancels first. Writes the answer as 1 square inch. |

## Practices not needed
- **Abstracting and Generalizing:** This is optional. A student who notices that 7/6 and 6/7 are reciprocals, so their product must be 1, uses this practice as a shortcut. The problem doesn't require it, because direct computation gets the same answer.
- **Justifying and Proving:** Not used. The problem asks for no argument or explanation.
- **Mathematical Modeling:** Not used. There's no real-world situation to model. The problem is a direct geometric calculation.
- **Collaborative Mathematics:** Not used. This is an individual task.

**Final sequence:** Representing → Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Most of the work in this problem is computation. The Representing step is small. Writing A = l × w for a rectangle is a recalled, routine formula, and the problem hands over both side lengths directly.

The real demand is multiplying two fractions, 7/6 × 6/7, and simplifying 42/42 to 1. A student who fails here almost always fails on the procedure. For example, they might multiply incorrectly, add the fractions instead, or forget to simplify. Knowing what area means is rarely the problem.

If I had to pick from the NAEP practices only, I would choose **Representing**. Without Procedural Fluency on the list, though, it is only a weak fit for where this problem actually challenges students.

---

## Row 67 (problem_id 24873)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A random sample of people were asked which hand they prefer to write with.
l means they prefer to use their left hand.
r means they prefer to use their right hand.
l r r r r r r r r r l r r r r
Based on this sample, estimate the proportion of the population that prefers to write with their left hand.
____
```

### Answer 1: practices in order

## The practices

The 2026 NAEP Mathematics Framework has five mathematical practices:

1. **Representing.** Moving between representations of the same mathematical idea, such as a list, a count, a fraction, a decimal or a percent.
2. **Abstracting and Generalizing.** Pulling out the general structure of a situation and extending it beyond the case at hand.
3. **Justifying and Proving.** Building or judging an argument for why a result holds.
4. **Mathematical Modeling.** Using math to describe and reason about a real-world situation, then reading the result back in context.
5. **Collaborative Mathematics.** Working on math with others.

From the NRC (*Adding It Up*, 2001):

6. **Procedural Fluency.** Carrying out procedures (counting, computing, converting) flexibly, accurately and efficiently.

## The problem

The sample is `l r r r r r r r r r l r r r r`. That is 15 people, 2 of them `l`.

Estimated proportion who prefer their left hand = **2/15 ≈ 0.13 (about 13%)**.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (setting up the model) | Sees the sample as a stand-in for the population. The sample proportion is used as the estimate of the population proportion. |
| 2 | **Representing** | Turns the string of symbols into counts: total = 15, left (`l`) = 2. Then writes "proportion" as the fraction left/total, which is 2/15. |
| 3 | **Procedural Fluency** (NRC) | Counts the entries accurately; it is easy to miss an `l` or miscount the 15. Then writes 2/15 and, if needed, converts it to a decimal or percent (≈ 0.133, or 13.3%). |
| 4 | **Representing** (again, light) | Gives the answer in the form the answer box expects: fraction, decimal or percent. |
| 5 | **Mathematical Modeling** (interpreting) | Reads 2/15 back as an *estimate* for the whole population, not an exact value. |

**Short order:** Mathematical Modeling, then Representing, then Procedural Fluency, then (Representing, then Modeling to interpret).

## Practices not really involved

- **Abstracting and Generalizing:** not needed. The problem asks for one direct estimate, with no pattern to generalize. The one exception is the weak sense of carrying the sample result over to the population, which the Modeling step already covers.
- **Justifying and Proving:** not needed. The student is not asked to explain or defend the estimate.
- **Collaborative Mathematics:** not involved. This is an individual assessment item.

## Main practices

The problem rests mostly on **Procedural Fluency** (counting and forming the fraction correctly) and **Representing** (turning raw data into a proportion). **Mathematical Modeling** plays a lighter part, framing the sample as an estimate for the population.

### Answer 2: major practice

## Major practice: **Procedural Fluency** (NRC)

The main thing the problem asks for is to count the data and form a proportion. That makes it a procedural task: count the `l`s (2), count all the entries (15), and write 2/15 (≈ 0.13).

The other practices play smaller parts:

- **Modeling** (sample → population) is built into the problem. The question itself says "based on this sample, estimate," so the student does not have to decide to use the sample proportion as the estimate.
- **Representing** (data → fraction) is simple here. "Proportion = part/whole" is a routine step, not a real change of representation.

Students who get this wrong usually miscount the entries or swap the part and the whole, for example writing 2/13 (left to right) instead of 2/15. Both are fluency errors, not conceptual ones. If I could tag only one practice, it would be **Procedural Fluency**. **Representing** would be a close second.

---

## Row 68 (problem_id 26005)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of the expression.
-2/5 · (-3/4)
____
```

### Answer 1: practices in order

**Problem:** Find the value of (-2/5) · (-3/4)

**Answer:** 3/10

### Practices available
The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I'm adding **Procedural Fluency** from the NRC's *Adding It Up* strands.

### Practices used, in order

**1. Representing (NAEP)**
The student first has to read the symbols correctly. Here, "·" means multiplication, each factor is a negative fraction, and the parentheses tie the second sign to its fraction. Reading the problem as two negative rational numbers being multiplied is what sets up every later step.

**2. Abstracting and Generalizing (NAEP)** *(light use)*
Next the student applies two general rules to this case:
- The sign rule: a negative times a negative is positive.
- The fraction rule: (a/b)(c/d) = ac/bd.

This step is about recognizing which general structure applies, not about computing yet. You could also fold it into Step 3, because fluent students apply these rules automatically.

**3. Procedural Fluency (NRC)** *(main practice)*
Then the student carries out the procedure accurately:
- Sign: (−)(−) → positive
- Numerators: 2 × 3 = 6
- Denominators: 5 × 4 = 20
- Simplify: 6/20 = **3/10** (an alternative is to cross-cancel the 2 and the 4 first, which gives 1/5 · 3/2 = 3/10)

### Practices not used
- **Justifying and Proving:** The problem doesn't ask for any explanation or argument. At most, a student might do a quick informal check that the answer should be positive.
- **Mathematical Modeling:** There is no real-world context.
- **Collaborative Mathematics:** This is an individual computation item.

### Summary
**Representing → (Abstracting and Generalizing) → Procedural Fluency**

Procedural Fluency is the main practice. Representing is needed briefly at the start, and Abstracting and Generalizing is optional or minor.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why I'd pick it**
- **It's what the item tests.** The prompt is just "find the value of" a bare symbolic expression. There's no context to model and nothing to justify, and the representation is already given as plain symbols.
- **It's where the work and the mistakes happen.** Solving it means applying the sign rule, multiplying numerators and denominators, and simplifying 6/20 to 3/10 (or cross-cancelling first). Students who miss this item usually do so in this step. Typical errors are getting the sign wrong (−3/10), not simplifying (6/20), or using a wrong rule such as cross-multiplying or finding a common denominator.
- **The other practices play a small role.** Representing is only reading standard notation, which takes little effort for any student ready for this item. Abstracting and Generalizing is just recalling familiar rules, and fluency already covers that.

So if you're tagging one practice for this problem, it's **Procedural Fluency**.

---

## Row 71 (problem_id 26296)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of the expression.
8/3 · -42
____
```

### Answer 1: practices in order

**Problem:** Find the value of the expression 8/3 · (−42).

**Answer:** −112

## Practices available
NAEP Mathematics Framework (2026) mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from NRC (*Adding It Up*, 2001):
6. Procedural Fluency

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the symbols correctly: `8/3` is a fraction, `·` means multiply, `−42` is a negative integer. Rewrites the problem as a fraction times a whole number, (8/3) × (−42/1), and sees that a positive times a negative gives a negative. |
| 2 | **Procedural Fluency** (NRC) | Does the arithmetic quickly and correctly. Cancels the common factor of 3 first (42 ÷ 3 = 14), then multiplies 8 × 14 = 112, and puts the negative sign on the result: **−112**. |
| 3 | **Justifying and Proving** (optional, light) | Checks the result: the sign rule (+ × − = −) holds, and the size is reasonable (about 2.67 × 42 ≈ 112). |

**Core sequence:** Representing → Procedural Fluency (→ a quick Justifying check if you count verification).

## Practices not needed
- **Abstracting and Generalizing:** the student doesn't need to find a pattern or general rule. It's one computation.
- **Mathematical Modeling:** there's no real-world context to turn into math.
- **Collaborative Mathematics:** it's an individual computation item.

**Note:** if "−42" was meant to be −4² (a superscript lost when the text was copied), the same practices apply in the same order. Representing then also covers reading the exponent and the order of operations (−4² = −16), and the answer becomes 8/3 · (−16) = −128/3.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item is a bare computation, 8/3 · (−42), with no context, pattern or argument involved. Its whole demand is carrying out a known procedure accurately and efficiently: multiply a fraction by an integer, simplify (42 ÷ 3 = 14, then 8 × 14 = 112), and apply the sign rule to get **−112**. That is exactly what procedural fluency means.
- Representing matters only a little here. Reading `8/3`, `·` and `−42` is routine notation, and the student doesn't have to translate between representations.
- Most errors on this item will be procedural slips: a wrong sign, multiplying 8 × 42 without simplifying and then dividing wrong, or treating 8/3 incorrectly. These are fluency errors, not errors of representing or reasoning.

If you have to choose a NAEP practice only, without the NRC addition, pick **Representing** as the closest fit, because it covers interpreting the symbolic expression. But the item mainly measures procedural fluency.

---

## Row 74 (problem_id 517656)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is 5/6 ÷ 1/12?
____
```

### Answer 1: practices in order

**Problem:** What is 5/6 ÷ 1/12?  **Answer: 10**

**The practices available.** The NAEP Mathematics Framework (2026) names five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

To these I've added **Procedural Fluency** from the NRC's *Adding It Up* strands. It means carrying out procedures flexibly, accurately and efficiently.

**Practices used, in order**

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (light) | Reads the symbols. "5/6 ÷ 1/12" is a division of two fractions, and the student sees it as the question "how many twelfths are in 5/6?" Or the student rewrites it in an equivalent form, such as 5/6 × 12/1, or 10/12 ÷ 1/12 using a common denominator. This step is a move between equivalent symbolic forms. |
| 2 | **Procedural Fluency** (main) | Runs the division procedure correctly. One way is to invert and multiply: 5/6 × 12 = 60/6 = 10. Another is to use a common denominator: 10/12 ÷ 1/12 = 10 ÷ 1 = 10. Then the student simplifies to 10. |

**Practices not needed**
- **Abstracting and Generalizing:** the student applies a known rule and doesn't build or extend a general pattern.
- **Justifying and Proving:** the item asks for no explanation or argument.
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** this is an individual item.

**Summary:** Representing (minor, used to set up the problem), then Procedural Fluency (main). This is mostly a procedural fluency item. Representing matters only as far as the student turns the division into an equivalent form they can compute.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item is a bare computation: "What is 5/6 ÷ 1/12?" It has no context, asks for no explanation, and offers no choice of representation. The student only needs to carry out the fraction-division procedure accurately and get 10. One way is invert and multiply: 5/6 × 12 = 10. Another is a common denominator: 10/12 ÷ 1/12 = 10.

Representing appears only in a small way, when the student rewrites the division in an equivalent form they can compute. That rewrite is itself part of the standard procedure. Whether a student gets this item right depends on procedural fluency.

---

## Row 77 (problem_id 27930)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A cone has volume 12π cubic inches. Its height is 4 inches. What is its radius?
____ inches
```

### Answer 1: practices in order

**Problem:** A cone has volume 12π cubic inches and height 4 inches. Find the radius.

**Practices available.** The NAEP 2026 Mathematics Framework lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands.

## Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Turns the words into symbols: V = 12π, h = 4, r unknown. Writes the cone formula V = (1/3)πr²h and substitutes: 12π = (1/3)π·r²·4. |
| 2 | **Procedural Fluency (NRC)** | Solves the equation correctly and efficiently: divide both sides by π to get 12 = (4/3)r². Multiply by 3/4 to get r² = 9. Take the square root to get r = 3, keeping only the positive root because r is a length. |
| 3 | **Justifying and Proving** *(light, optional)* | Checks the answer: (1/3)π(3²)(4) = 12π. Also explains why r = −3 is thrown out. |

**Answer:** **3** inches

## Practices not really used
- **Abstracting and Generalizing:** The student uses a known formula and doesn't build a general rule or pattern.
- **Mathematical Modeling:** There's no real-world situation to simplify or assumptions to make. This is a pure geometry problem.
- **Collaborative Mathematics:** This is a single-student item, so there's no shared reasoning.

## Summary
**Representing → Procedural Fluency → (Justifying and Proving, as a check)**

The two main practices are Representing and Procedural Fluency. The core of the problem is recalling and setting up the cone volume formula, then solving for r. Justifying and Proving only comes in as a short check of the answer.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why this one:**
- **The problem is mostly a known procedure.** You recall the cone volume formula V = (1/3)πr²h, substitute the given values, and solve for the unknown: 12π = (1/3)π·r²·4, so r² = 9 and r = 3. Every step is a standard routine you either carry out correctly or don't.
- **The hard part is working the formula backward.** Plugging r into V would be routine. Here the student has to rearrange and solve for r: cancel π, clear the 1/3, isolate r², take the square root, and drop the negative root. That flexible, accurate use of procedures is exactly what procedural fluency means.
- **Representing is a smaller part.** The words map directly onto symbols (volume becomes V, height becomes h, radius becomes r). There's no diagram to read, no switch between representations, and no choice of how to model the problem. The setup takes one line. The solving is where the work is.
- **Justifying and Proving is optional.** It's just a quick check at the end.

**Answer:** 3 inches. **Major practice:** Procedural Fluency. Representing is secondary.

---

## Row 79 (problem_id 30779)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Elena bought 8 tokens for $4.40. At this rate:
How much do 19 tokens cost?
$ ____
```

### Answer 1: practices in order

**Problem:** Elena bought 8 tokens for $4.40. At this rate, how much do 19 tokens cost?

**Answer: $10.45**

## Practices available

The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

You asked me to add one from the NRC's *Adding It Up* strands:
6. **Procedural Fluency**: carrying out procedures flexibly, accurately and efficiently.

## Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Turns the words "8 tokens for $4.40, at this rate" into a math form: a ratio or proportion (8 : 4.40 = 19 : x), a unit-rate setup (cost per token = 4.40 ÷ 8), or a ratio table. |
| 2 | **Abstracting and Generalizing** | Sees that "at this rate" means the cost per token stays the same, so the cost is proportional: cost = (price per token) × (number of tokens). This rule works for any number of tokens, including 19. |
| 3 | **Procedural Fluency** (NRC) | Does the decimal arithmetic correctly: 4.40 ÷ 8 = 0.55, then 0.55 × 19 = 10.45. Another route is to cross-multiply 4.40 × 19 = 83.60, then 83.60 ÷ 8 = 10.45. |

Optional step 4, a light use of **Justifying**: checking that the answer makes sense. 19 is a bit more than twice 8, and $10.45 is a bit more than twice $4.40 ($8.80), so the answer is reasonable. The item only asks for a number, so this step is not required.

## Practices not used

- **Mathematical Modeling**: not really used. The rate model is handed to the student ("at this rate"). The student does not have to choose assumptions or build a model from a messy real situation. At most it is a very simple proportional model, which Steps 1–2 already cover.
- **Justifying and Proving**: not required. The item asks for no explanation or argument.
- **Collaborative Mathematics**: not applicable to a single-student item.

## Summary

**Representing → Abstracting and Generalizing → Procedural Fluency**

The main demand is Representing plus Procedural Fluency. Abstracting and Generalizing is a smaller step, because the item states the constant rate outright.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The problem gives the structure away. "At this rate" tells the student the relationship is a constant unit rate. The setup (cost per token = 4.40 ÷ 8, then multiply by 19) is a standard, well-practiced routine for this grade level, so Representing and Abstracting take little thought.
- Most of the work, and most of the chances for error, is in the computation. The student divides a decimal (4.40 ÷ 8 = 0.55), multiplies a decimal (0.55 × 19 = 10.45), and keeps the place value right in a money answer. Typical mistakes are 0.5 or 0.6 instead of 0.55, and slips like 10.40 or 1.045. These are procedural errors, not representation errors.
- The answer is a single number with no explanation, so the item mainly checks whether the student can carry out the procedure correctly.

**Runner-up: Representing.** A student who doesn't see this as a unit-rate or proportion problem can't get started; some might try 19 − 8 or 4.40 + 19. If the item were written in less routine words, or if the numbers made the arithmetic trivial, I would choose Representing. With these numbers and this wording, Procedural Fluency is the main demand.

---

## Row 80 (problem_id 30604)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Elena bought 8 tokens for $4.40. At this rate:
How many tokens could she buy with $6.05?
____ tokens
```

### Answer 1: practices in order

## Practices for the token problem

**Problem:** Elena bought 8 tokens for $4.40. At this rate, how many tokens could she buy with $6.05?

**Answer: 11 tokens**

### Practices available
- **NAEP Mathematics Framework practices:** Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics.
- **Added from the NRC strands (*Adding It Up*):** Procedural Fluency.

### Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** | Reads "at this rate" as a constant rate, so cost is proportional to the number of tokens. The real-world situation becomes a math model: same price per token. |
| 2 | **Representing** | Writes the model in math form, either as a unit rate ($4.40 ÷ 8 per token) or as a proportion: 8 / 4.40 = x / 6.05. |
| 3 | **Procedural Fluency** (NRC) | Does the decimal arithmetic correctly and efficiently: 4.40 ÷ 8 = 0.55 dollars per token, then 6.05 ÷ 0.55 = 11. Using cross-multiplication gives the same result: x = 8 × 6.05 / 4.40 = 48.40 / 4.40 = 11. |
| 4 | **Justifying and Proving** (light use) | Checks that the answer makes sense: 11 × $0.55 = $6.05. Also, $6.05 is more than $4.40, so the answer should be more than 8 tokens, and it is a whole number. |

### Practices not needed
- **Abstracting and Generalizing:** The problem asks for one specific value. It does not ask for a general rule or pattern beyond the single unit rate.
- **Collaborative Mathematics:** This is a single-student item with no communication or group work.

### Short sequence
**Mathematical Modeling → Representing → Procedural Fluency → Justifying and Proving (check)**

Procedural Fluency is the main practice. Most of the difficulty is in the decimal division (4.40 ÷ 8 and 6.05 ÷ 0.55). Modeling and Representing are the setup steps before that.

### Answer 2: major practice

## Major practice: Procedural Fluency (NRC)

If I had to pick one, I would choose **Procedural Fluency**.

**Why:**
- **Setting up the problem is easy.** "At this rate" tells the student directly that this is a constant-rate (proportional) situation. The student does not have to work out a model, so Mathematical Modeling and Representing don't take much effort.
- **The hard part is the arithmetic.** The work is decimal division: 4.40 ÷ 8 = 0.55, then 6.05 ÷ 0.55 = 11. Using cross-multiplication instead means computing 8 × 6.05 = 48.40 and then 48.40 ÷ 4.40 = 11. Students most likely get this item wrong through slips such as misplacing the decimal point or dividing in the wrong direction. These are procedural errors.
- **The checking step is optional.** Verifying 11 × 0.55 = 6.05 is good practice, but the answer doesn't depend on it.

**Runner-up:** Representing. A student who sets up the ratio upside down (dollars per token versus tokens per dollar) fails for a reason that isn't about computing. This makes Representing a reasonable second choice. But for most students the main challenge is executing the decimal computation, so Procedural Fluency is the major practice.

---

## Row 81 (problem_id 587537)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is 3/4 ÷ 1/8?
____
```

### Answer 1: practices in order

**Problem:** What is 3/4 ÷ 1/8?  **Answer: 6**

**Practices available.** The 2026 NAEP Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've also included NRC's *Procedural Fluency* (one of the five strands of mathematical proficiency in *Adding It Up*).

**Practices needed, in order:**

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) — light/optional | Reads the symbolic expression as a fraction division and understands what it means, for example "how many 1/8s fit in 3/4?" (3/4 = 6/8, so six eighths). A student who already has the procedure automatized may skip this step or barely use it. |
| 2 | **Procedural Fluency** (NRC) — primary | Carries out the division algorithm correctly and efficiently: keep, change, flip, so 3/4 × 8/1 = 24/4 = 6. Another route is a common denominator: 6/8 ÷ 1/8 = 6. Either way, the student simplifies to the final answer, 6. |

**Practices not needed:**
- **Abstracting and Generalizing**: there is no pattern to generalize and no general rule to build. The student only applies a rule they already know.
- **Justifying and Proving**: the item asks for no explanation or argument.
- **Mathematical Modeling**: the item has no real-world context to translate into math.
- **Collaborative Mathematics**: this is an individual, short-answer item.

**Summary:** Representing (minor, for interpreting the expression), then **Procedural Fluency** (dominant). This is basically a pure procedural-fluency item. Representing helps only if the student reasons about the division conceptually instead of using the algorithm directly.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item is a bare symbolic computation, 3/4 ÷ 1/8, with no context and no request for an explanation. Success depends almost entirely on carrying out the fraction-division algorithm accurately: keep, change, flip, so 3/4 × 8 = 6. You could also rewrite both fractions with a common denominator: 6/8 ÷ 1/8 = 6.

Representing plays at most a minor role. A student might interpret the expression as "how many eighths are in 3/4," but solving the problem doesn't require it. None of the NAEP practices captures the core demand of this item as well as Procedural Fluency does.

---

## Row 82 (problem_id 284725)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Compute (4,803) · 95.
____
```

### Answer 1: practices in order

**Problem:** Compute (4,803) · 95

**Answer:** 456,285

**Practices used, in order**

The NAEP mathematical practices are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Procedural fluency from the NRC strands is added to that list.

1. **Representing (NAEP)**: a small role, at the start.
   - Read the notation: the parentheses and the centered dot "·" both mean multiplication. The comma in 4,803 is a thousands separator, not a decimal or list separator.
   - Turn the expression into a form you can calculate with. That can be the standard vertical multiplication layout, or a decomposition such as 95 = 100 − 5 (or 4,803 = 4,800 + 3).

2. **Procedural Fluency (NRC)**: the main practice, and most of the work.
   - Carry out the multi-digit multiplication accurately and efficiently:
     - 4,803 × 100 = 480,300
     - 4,803 × 5 = 24,015
     - 480,300 − 24,015 = **456,285**
   - Or use the standard algorithm with place values (4,803 × 90 = 432,270; 4,803 × 5 = 24,015; sum = 456,285).
   - This depends on knowing the basic facts, handling place value and carrying, and choosing a sensible method.

3. **Justifying (NAEP Justifying and Proving)**: optional and light, at the end.
   - Check that the answer is reasonable with an estimate: 4,800 × 100 ≈ 480,000, and the product should be a bit less than that. Or check it a second way: 4,800 × 95 + 3 × 95 = 456,000 + 285 = 456,285.

**Practices not needed:** Abstracting and Generalizing, Mathematical Modeling, and Collaborative Mathematics. The problem has no context, no pattern and no generalization, and it is a single-person computation.

**Order:** Representing → Procedural Fluency → (optional) Justifying. Procedural fluency is the main practice.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Computing (4,803) · 95 is a straight multi-digit multiplication with no context, no pattern and nothing to prove. Almost all of the work is doing the multiplication accurately and efficiently: place value, regrouping, partial products, and possibly the shortcut 95 = 100 − 5. The answer is 456,285.

Representing is involved only in a small way, when you read "·" and the parentheses as multiplication. Justifying is just an optional check with an estimate. A student who knows what the notation means but cannot do the multiplication fluently will get this wrong. That makes procedural fluency the practice that decides success on this item.

---

## Row 83 (problem_id 32069)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the problem below.
What is 25% of 160?
____
```

### Answer 1: practices in order

**Problem:** What is 25% of 160?  **Answer: 40**

**Practices available.** The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands.

**Practices needed, in order:**

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Turns "25% of 160" into a form you can compute with. "25%" becomes 25/100 = 1/4 (or 0.25), and "of" means multiply. So the problem becomes 1/4 × 160 (or 0.25 × 160). |
| 2 | **Procedural Fluency (NRC)** | Does the calculation accurately and efficiently: 160 ÷ 4 = 40 (or 0.25 × 160 = 40). |

**Practices not needed:**
- **Abstracting and Generalizing:** the student doesn't have to find a general pattern or rule. Using the known fact that 25% = 1/4 counts as representing, not generalizing.
- **Justifying and Proving:** the item doesn't ask for an argument or explanation.
- **Mathematical Modeling:** there's no real-world situation to model. It's a bare computation.
- **Collaborative Mathematics:** this is a task done alone.

**Order:** Representing → Procedural Fluency.

(Optional check: 10% of 160 is 16, so 25% should be a bit more than 2 × 16 = 32. 40 fits. This is a quick sense check, not a required Justifying step.)

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- **It's a bare computation.** "What is 25% of 160?" has no context, nothing to model, and nothing to explain or justify. It checks whether the student can carry out a standard percent-of-a-number procedure accurately and efficiently.
- **The Representing step is routine.** Turning 25% into 1/4 or 0.25 is a memorized equivalence, and it's really the first step of the standard procedure ("convert the percent, then multiply"). The student doesn't have to choose between representations or build a new one, so it adds little beyond the procedure.
- **Most of the difficulty is in doing the steps.** Students who get it wrong usually misapply the procedure. They might compute 160 × 25 = 4000 or 160 ÷ 25 = 6.4, or slip on the arithmetic. They rarely misunderstand what the question is asking.

**Representing** would be the secondary practice. It's needed to get started, but here it's minor.

---

## Row 85 (problem_id 32696)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the problem below.
What is 150% of 32?
____
```

### Answer 1: practices in order

**Problem:** What is 150% of 32?  **Answer: 48**

**Practices available.** The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematical Discourse

You also asked me to include **Procedural Fluency** from the NRC's strands of mathematical proficiency (*Adding It Up*, 2001).

---

### Practices needed, in order

**Step 1: Representing**
The student has to change "150% of 32" into a form they can compute with. Two things happen here:
- "150%" becomes 1.5 (or 3/2, or 100% + 50%).
- "of" becomes multiplication: 1.5 × 32.

This is a change from one representation to another (percent → decimal or fraction, words → expression), so it's the Representing practice. It's also the step where students most often go wrong, for example by writing 150 × 32 or 0.15 × 32.

**Step 2: Procedural Fluency (NRC)**
Next the student does the arithmetic correctly and quickly:
- 1.5 × 32 = 48, or
- 32 + ½(32) = 32 + 16 = 48, or
- (3/2) × 32 = 96/2 = 48.

This is routine work: a known procedure applied accurately, which is Procedural Fluency.

**Step 3 (optional, light): Justifying and Proving, as a reasonableness check**
A quick check: 150% is more than 100%, so the answer has to be bigger than 32 (and 48 is). It's also halfway between 100% (32) and 200% (64), and 48 is the midpoint. This is a small, informal use of the practice. The problem doesn't require it, and many students will skip it.

---

### Practices not needed
- **Abstracting and Generalizing:** no pattern or general rule is asked for.
- **Mathematical Modeling:** the problem is purely numerical, with no real-world situation to model.
- **Collaborative Mathematical Discourse:** this is a single-answer item done alone.

### Summary

| Order | Practice | Role in this problem |
|---|---|---|
| 1 | Representing (NAEP) | 150% of 32 → 1.5 × 32 (or 3/2 × 32) |
| 2 | Procedural Fluency (NRC) | Work out 1.5 × 32 = 48 |
| 3 (optional) | Justifying and Proving (NAEP) | Check that 48 > 32 makes sense because 150% > 100% |

The main sequence is **Representing → Procedural Fluency**. Representing is the harder part for students, and Procedural Fluency is what produces the answer.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why this one:**
- **The problem is a bare computation.** "What is 150% of 32?" has no context, no wording to interpret and no choice of method. It asks for one number from a standard procedure: percent to decimal, then multiply.
- **The Representing step is part of the procedure.** Writing 150% as 1.5 and "of" as × is the first step of the usual "percent of a number" routine that students learn. It's an automatic translation, not a real choice between representations like tables, graphs or equations.
- **It decides whether the answer is right.** A student who knows the percent-of procedure and can carry it out (1.5 × 32, or 32 + 16) gets 48. A student who doesn't usually makes a procedural mistake (150 × 32, 0.15 × 32, or finding only 50%). Those are gaps in fluency with percents.
- **The other practices barely appear.** The reasonableness check (Justifying) is optional. Abstracting, Modeling and Discourse don't come up at all.

**About my earlier answer:** I said Representing is the step where students most often go wrong. That's still true, but here it's a routine step inside the procedure rather than a separate representational task. So if I can name only one, it's **Procedural Fluency**, with Representing as a secondary practice.

---

## Row 86 (problem_id 32378)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the problem below.
What is 39% of 200?
____
```

### Answer 1: practices in order

**Problem:** What is 39% of 200?  **Answer: 78**

**Practices available.** The NAEP Mathematics framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands.

**Practices used, in order:**

1. **Representing (NAEP).** Rewrite the words as a math expression. "39% of 200" means 39% × 200, and 39% can be written as 39/100 or 0.39. So the expression is 0.39 × 200 (or 39/100 × 200). This step turns the language of percent into a form you can compute.

2. **Procedural Fluency (NRC).** Do the arithmetic accurately and efficiently: 39/100 × 200 = 39 × 2 = 78. A fluent student sees that 200/100 = 2, which makes the multiplication easy. Another efficient route is 40% of 200 = 80, then subtract 1% of 200 (which is 2) to get 78.

3. **Justifying and Proving (NAEP), optional and light.** Check that the answer makes sense. 39% is a little less than 40%, and 40% of 200 is 80, so 78 is reasonable. On a short-answer item this check is usually done silently, so it plays a minor role here.

**Practices not needed:** Abstracting and Generalizing (no pattern or general rule is involved), Mathematical Modeling (there is no real-world situation to model, only a bare computation), and Collaborative Mathematics (this is a solo item).

**Summary:** Representing → Procedural Fluency → (optional) Justifying. Procedural Fluency is the main practice for this item, and Representing is a short first step that sets it up.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Most of the work in this item is computation. Writing "39% of 200" as 0.39 × 200 (or 39/100 × 200) is the standard, almost automatic translation for a percent-of problem, so Representing takes very little effort. What separates students who get it right from those who don't is whether they can do the computation accurately and efficiently: 39 × 2 = 78, or 80 − 2 = 78. Common errors, like misplacing the decimal (getting 7.8 or 780) or making mistakes when multiplying 0.39 × 200, are fluency errors, not representation errors.

So Procedural Fluency is the major practice. Representing is a minor first step, and Justifying is an optional check.

---

## Row 87 (problem_id 33021)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the problem below.
13 is 50% of what number?
____
```

### Answer 1: practices in order

**Problem:** 13 is 50% of what number?  **Answer: 26**

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. You asked me to add one more, Procedural Fluency from the NRC's *Adding It Up*.

This is a short, one-step percent problem. Only two practices are really needed:

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the words into math: "13 is 50% of what number" becomes 0.5 × n = 13, or 13/n = 50/100. The key is seeing that 13 is the part and the unknown is the whole. |
| 2 | **Procedural Fluency** (NRC) | Solves it: n = 13 ÷ 0.5 = 26. A faster route is knowing that 50% means half, so the whole is 13 × 2 = 26. |

**Not needed:**
- **Abstracting and Generalizing:** The student only solves this one case and doesn't look for a general pattern.
- **Justifying and Proving:** No argument is asked for. A quick check (half of 26 is 13) is just routine checking, not justification.
- **Mathematical Modeling:** There's no real-world situation to model. The problem is already pure math.
- **Collaborative Mathematics:** It's a problem for one student working alone.

**Sequence:** Representing → Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The problem is a short, standard percent question: "13 is 50% of what number?" The student mostly needs to know a procedure and carry it out, either 13 ÷ 0.5 = 26 or "50% means half, so double 13 to get 26."

Representing still matters, because the student has to see that 13 is the part and the unknown is the whole. But the wording is a familiar textbook pattern, so that step is light and almost automatic. Most of the difficulty is in doing the calculation correctly. A common mistake is taking 50% of 13 and answering 6.5. That is a gap in procedural or conceptual percent knowledge, not a representing problem.

**Secondary practice:** Representing (NAEP).

---

## Row 88 (problem_id 33513)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
What is the slope of the line you graphed?
____
```

### Answer 1: practices in order

## Practices for: "What is the slope of the line you graphed?"

**Practices to choose from.** The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I also added **Procedural Fluency** from the NRC's *Adding It Up* strands.

**Note on context:** This is a follow-up question. It depends on a line the student graphed in an earlier part, probably from an equation, a table, or two given points. The student has to work from that graph or from the information behind it.

### Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the graphed line and turns it into usable numbers. That means picking two clear points on the line, ideally lattice points, and reading their coordinates. It also means connecting the visual steepness and direction of the line to the idea of slope. |
| 2 | **Procedural Fluency (NRC)** | Uses the slope procedure correctly: rise/run = (y2 - y1)/(x2 - x1). That includes subtracting signed numbers, getting the sign right (rising or falling line), and simplifying the fraction. |
| 3 | **Representing** (check, optional) | Compares the computed value with the graph. If the line rises, the slope should be positive. A steeper line should give a larger absolute value. If the line came from an equation y = mx + b, the result should match m. |

### Practices that are not needed
- **Abstracting and Generalizing:** The student isn't asked to find a pattern or general rule. Slope is computed for this one line.
- **Justifying and Proving:** No explanation or argument is required. The answer is just a number in a blank.
- **Mathematical Modeling:** As written, there is no real-world context to turn into math or interpret. If the earlier part used a context, such as a rate, it would come in only if the student had to interpret the slope, and this question doesn't ask for that.
- **Collaborative Mathematics:** This is an individual item.

### Summary order
**Representing -> Procedural Fluency** (with a quick optional Representing check at the end).

Representing is the main practice, since the student has to pull information from the graph. Procedural Fluency is the main computing step.

### Answer 2: major practice

## Major practice: **Representing**

If I had to choose one, I'd choose **Representing**.

**Why:**
- **The question is built around the graph.** It asks for the slope of "the line you graphed." To answer, the student has to treat the line as something that carries numbers: pick two points on it, read their coordinates, and see its rise and run. Going from the picture to numbers is the core of Representing.
- **It's the step most likely to cause errors.** Common mistakes are misreading coordinates, using points that aren't on the grid lines, mixing up rise and run, or missing that a falling line has a negative slope. All of these are representation errors, not calculation errors.
- **The calculation is simple.** Once the student has two points, (y2 - y1)/(x2 - x1) is basic arithmetic with signed numbers. Procedural Fluency is used, but it's a small step that supports the main one.

**Caveat:** If the student's line came from an equation written in slope-intercept form, they might just read m off the equation without using the graph. That would shift the weight toward Procedural Fluency. The question points the student to the graph, though, so Representing is the best single label.

---

## Row 90 (problem_id 457114)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Compute (3,902) · 85.
____
```

### Answer 1: practices in order

**Problem:** Compute (3,902) · 85.

**The practices to choose from.** The NAEP Mathematics Framework (2026 edition) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

You asked me to add a sixth from the NRC's *Adding It Up* strands:
6. **Procedural Fluency**: carrying out procedures flexibly, accurately and efficiently.

**Practices this problem uses, in order**

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the notation. The dot "·" means multiplication, the parentheses only group the number, and the comma in 3,902 separates thousands; it is not a decimal point. The student turns this into a multiplication to work out, such as 3,902 × 85 written in vertical form with place values lined up. |
| 2 | **Procedural Fluency** (NRC) | Runs the multi-digit multiplication algorithm with correct regrouping: 3,902 × 5 = 19,510; 3,902 × 80 = 312,160; 19,510 + 312,160 = **331,670**. This is the main practice in the problem. |

Optional step 3 (Procedural Fluency again, used as a check): estimate 3,900 × 85 ≈ 4,000 × 85 = 340,000, so 331,670 is a reasonable answer.

**Practices this problem does not use**
- **Abstracting and Generalizing**: there is no pattern or general rule to find.
- **Justifying and Proving**: the student doesn't have to give an argument or explanation.
- **Mathematical Modeling**: there is no real-world context to turn into math.
- **Collaborative Mathematics**: this is an individual computation.

**Final sequence:** Representing → Procedural Fluency

**Answer:** 331,670

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

This is a bare computation with no context: (3,902) · 85. Representing only covers reading the notation, and for a student at this level that is close to automatic. The real thinking work is running the multi-digit multiplication algorithm correctly. That means getting the partial products right (3,902 × 5 = 19,510 and 3,902 × 80 = 312,160), handling the regrouping, and adding them to get **331,670**.

The zero in the tens place of 3,902 is a common place for students to slip, which also makes this a test of accurate procedure. If a student gets this item wrong, the cause is almost always a procedural error, not a misreading of the problem. So Procedural Fluency is the practice the item really measures.

---

## Row 91 (problem_id 36673)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is the volume of the cone? Express your answer in terms of π.
____ cubic units
Use pi to represent the π symbol. For example: 32π would be typed as 32pi
```

### Answer 1: practices in order

**Note:** The problem text doesn't include the cone's dimensions. They are probably in a figure that wasn't attached. So the practice sequence below is general, and I haven't worked out a numeric answer.

### Practices available
NAEP Mathematics Framework (2026) mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics (in the framework but not assessed on NAEP)

Added from the NRC (*Adding It Up*) strands: **Procedural Fluency**.

### Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the cone diagram and picks out the needed measurements: the radius *r* and the perpendicular height *h*. This includes converting a diameter to a radius, or noticing when a labeled length is the slant height rather than the height. |
| 2 | **Abstracting and Generalizing** *(light use)* | Treats the figure as one case of the general cone-volume relationship, V = (1/3)πr²h (a cone is one-third of a cylinder with the same base and height), and matches the diagram's values to the variables. |
| 3 | **Procedural Fluency** (NRC) | Substitutes the values and computes accurately: squares *r*, multiplies by *h*, divides by 3, and keeps π as a symbol instead of approximating it. If the slant height *l* is given, first finds h = √(l² − r²). |
| 4 | **Representing** | Writes the result in the required form: an exact multiple of π, typed with the keyword `pi` (for example, `32pi`), in cubic units. |

### Practices not needed
- **Mathematical Modeling**: there is no real-world context to turn into math. It is a direct geometry calculation.
- **Justifying and Proving**: the student doesn't have to explain or prove anything, only give the number.
- **Collaborative Mathematics**: this is an individual item.

**Short answer:** Representing → (Abstracting and Generalizing) → Procedural Fluency → Representing. Procedural Fluency and Representing are the main practices. Abstracting and Generalizing plays only a small part, because recalling the cone formula is mostly knowing a fact.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- **The problem is a calculation at its core.** The student recalls V = (1/3)πr²h, puts in the values and works out the result. Squaring the radius, multiplying by the height, dividing by 3 and keeping π exact are all procedural steps.
- **Most errors happen here.** Common mistakes are forgetting the 1/3, using the diameter instead of the radius, squaring the wrong value, or turning π into 3.14 when the answer should stay in terms of π. All of these are failures of accurate, flexible use of a procedure.
- **Representing plays a supporting role.** Reading the diagram and typing the answer as `__pi` are needed, but they mostly frame the task. A student who reads the figure correctly can still get it wrong if they can't carry out the procedure.
- **The other practices barely appear.** There is no context to model, nothing to justify, and only a little generalizing, since recalling the formula is mostly knowing a fact.

If you have to use only the NAEP practices (without the NRC addition), choose **Representing**. It is the only NAEP practice that clearly applies, because the student has to read the measurements from the diagram and write the answer in symbolic form.

---

## Row 94 (problem_id 132337)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A line contains the points (-3, -2) and (7, 2).
Calculate the slope of the line.
____
```

### Answer 1: practices in order

**Problem:** A line goes through the points (-3, -2) and (7, 2). Find the slope of the line.

**Practices available.** The NAEP Mathematics Framework (2026) names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling and Collaborative Mathematics. As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands.

## Practices in order

**1. Representing**
- Read each ordered pair as an (x, y) location on the coordinate plane.
- Treat slope as the ratio of the change in y to the change in x ("rise over run").
- This connects the points given in words to the slope formula: m = (y2 - y1) / (x2 - x1).

**2. Procedural Fluency (NRC)**
- Use the formula correctly, keeping the same order of points in the top and bottom of the fraction.
- Handle the negative numbers carefully:
  - Change in y: 2 - (-2) = 4
  - Change in x: 7 - (-3) = 10
- Simplify the fraction: m = 4/10 = **2/5** (0.4).

**3. Abstracting and Generalizing** (minor, optional)
- This practice only applies if the student sees slope as a general property of the line rather than just plugging into a formula.
- The idea is that any two points on the line give the same ratio.
- Example: swapping the order of the points gives (-2 - 2) / (-3 - 7) = -4/-10, which is still 2/5.

## Practices not needed
- **Justifying and Proving:** the student isn't asked to explain or argue for the answer.
- **Mathematical Modeling:** there's no real-world situation to turn into math.
- **Collaborative Mathematics:** it's a single-student item with no group work.

## Summary order
**Representing → Procedural Fluency** (→ Abstracting and Generalizing, optional)

**Answer:** slope = **2/5** (0.4)

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why it's the main one:**
- Most of the work is carrying out a standard procedure: put the two points into m = (y2 - y1) / (x2 - x1) and simplify.
- The hard parts are procedural:
  - subtracting negative numbers correctly: 2 - (-2) = 4 and 7 - (-3) = 10
  - using the points in the same order on the top and bottom of the fraction
  - reducing 4/10 to 2/5
- Most errors on this kind of item come from these steps, such as sign mistakes or flipping the fraction to change in x over change in y. They rarely come from misunderstanding the problem.

**Why Representing comes second:**
- Representing is needed only briefly, to read the ordered pairs as coordinates and recall that slope is rise over run.
- The problem gives the points directly and asks for "the slope," so it already points to the method.
- There's no graph, table or context to translate, which keeps the Representing demand small.

**Answer:** slope = 2/5 (0.4)

---

## Row 96 (problem_id 277925)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A stack of 500 pieces of paper is 1.875 inches tall.
Compute the thickness of each piece of paper.
____ inches
```

### Answer 1: practices in order

**Answer:** 1.875 ÷ 500 = **0.00375 inches**

The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Adding **Procedural Fluency** (NRC, *Adding It Up*) gives six candidates. This problem needs three of them, used in this order:

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** | Turns the real situation into math. The student assumes every sheet is equally thick, so the total height is the thickness of one sheet times 500. That means the question is a division problem. |
| 2 | **Representing** | Writes the model as an expression or equation: 500 × t = 1.875, so t = 1.875 ÷ 500. |
| 3 | **Procedural Fluency (NRC)** | Divides the decimal correctly, for example 1.875 ÷ 5 = 0.375, then ÷ 100 = 0.00375. This step also needs correct place value with the small result. |

**Optional step 4: Justifying and Proving.** The student can check the answer by working backward: 0.00375 × 500 = 1.875. Many students do this, but the item doesn't require it, so it is a minor or optional practice here.

**Not used:**
- **Abstracting and Generalizing:** The student finds one numerical answer and doesn't need to extend the result to a general rule or a family of cases.
- **Collaborative Mathematics:** This is an individual item with no part that involves sharing or critiquing someone else's reasoning.

**Summary of the order:** Mathematical Modeling → Representing → Procedural Fluency (→ optional check with Justifying and Proving).

Procedural Fluency carries most of the difficulty. The model is a simple equal-sharing division, so most errors come from decimal division and place value, such as writing 0.0375 or 0.375.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- **The modeling step is small.** "500 equal sheets make 1.875 inches, so how thick is one sheet?" is a standard equal-sharing situation, and students see right away that it calls for division. Turning it into math takes little real modeling.
- **The representation is one line.** Writing 1.875 ÷ 500 is immediate, and the student doesn't need to choose or move between representations.
- **The computation is the hard part.** The student has to divide a three-place decimal by 500 and get a result with several leading zeros (0.00375). Typical errors are place-value mistakes such as 0.0375 or 0.375, decimal-point slips, and setting up the division backwards (500 ÷ 1.875). The last of these is a small modeling error, but the first two are mostly procedural. So whether a student gets this item right depends mainly on fluency with decimal division.

If the choice had to come from the five NAEP practices only, I would pick **Mathematical Modeling**. It is the only NAEP practice the item truly needs, because the student must link the real situation to the division. With Procedural Fluency available, though, it is the clear major practice.

---

## Row 98 (problem_id 38766)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression. If the answer is not a whole number, write your answer as a fraction.
4/3 ÷ -24
____
```

### Answer 1: practices in order

**Problem:** Evaluate 4/3 ÷ (−24). If the answer is not a whole number, write it as a fraction.

**Answer: −1/18**

## Practices I used

The 2026 NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I also added **Procedural Fluency** from the NRC's *Adding It Up* strands.

This is a short computation with no context, so only two practices are really needed.

### 1. Representing (NAEP)
Rewrite the problem so a standard method applies:
- Write the whole number as a fraction: −24 = −24/1.
- Turn division into multiplication by the reciprocal: 4/3 ÷ (−24/1) = 4/3 × (−1/24).

### 2. Procedural Fluency (NRC)
Carry out the steps correctly:
- Sign rule: a positive divided by a negative is negative.
- Multiply: 4/3 × 1/24 = 4/72.
- Simplify: 4/72 = 1/18. You could also cancel the 4 against the 24 first: (1/3)(1/6) = 1/18.
- Final answer: **−1/18**. It is not a whole number, so it stays a fraction, as the problem asks.

### Practices not needed
- **Abstracting and Generalizing:** no pattern or general rule to find.
- **Justifying and Proving:** the problem doesn't ask for an argument. At most, a student might quickly check the answer: −1/18 × (−24) = 24/18 = 4/3. That check is part of fluent procedure, not a separate practice.
- **Mathematical Modeling:** no real-world situation.
- **Collaborative Mathematics:** not part of this task, and NAEP doesn't assess it on individual items.

**Order:** Representing → Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

This item mostly tests whether a student can carry out the standard fraction-division procedure accurately:
- Multiply by the reciprocal.
- Apply the sign rule (positive ÷ negative gives a negative).
- Multiply and simplify to −1/18.

The Representing step (writing −24 as −24/1 and turning ÷ into × by the reciprocal) is the first move of that same procedure. It isn't a separate choice between representations. Students don't interpret, model, generalize or justify anything. A wrong answer will almost always come from a procedural slip, such as a dropped negative sign, not using the reciprocal, or not simplifying, rather than from a conceptual or representational misunderstanding.

So if I had to label this item with one practice, it would be **Procedural Fluency**.

---

## Row 101 (problem_id 39959)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Strawberries cost $3.00 per pound.
How many pounds of strawberries can you buy for $11.00?
____ pounds of strawberries
```

### Answer 1: practices in order

## The practices to draw on

The 2026 NAEP Mathematics Framework lists five mathematical practices:

1. **Representing**: moving between words, symbols, tables, diagrams and numbers.
2. **Abstracting and Generalizing**: finding structure and patterns that go beyond one case.
3. **Justifying and Proving**: building and judging mathematical arguments.
4. **Mathematical Modeling**: turning a real situation into mathematics, solving it, and reading the result back in context.
5. **Collaborative Mathematics**: working with others to solve problems.

As you asked, I'm adding **Procedural Fluency** from the NRC's *Adding It Up* (1998, 2001): carrying out procedures accurately, efficiently and flexibly.

## The problem

> Strawberries cost $3.00 per pound. How many pounds can you buy for $11.00?

**Answer:** 11 ÷ 3 = **3 2/3 pounds (about 3.67 pounds)**

## Which practices, in what order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (formulate) | Sees this as a unit-rate situation. The $3.00 per pound rate and the $11.00 total give the unknown as total ÷ rate. Pounds × $3 = $11, so pounds = 11 ÷ 3. |
| 2 | **Representing** | Turns the words into symbols, for example 3 × p = 11 or p = 11/3. Writes the answer as a mixed number (3 2/3) or a decimal (3.67) to fill the blank. |
| 3 | **Procedural Fluency** | Does the division correctly: 11 ÷ 3 = 3 remainder 2, which is 3 2/3 or 3.666... ≈ 3.67. This is the main computation step. |
| 4 | **Mathematical Modeling** (interpret and validate) | Reads the result back in context. Strawberries are sold by weight, so a fractional amount makes sense and the answer is not rounded down to 3. Checks that 3 2/3 × $3 = $11. |

**Order:** Mathematical Modeling, then Representing, then Procedural Fluency, then Mathematical Modeling again (interpret and check).

## Practices not needed

- **Abstracting and Generalizing**: the problem is one concrete case and asks for no general rule.
- **Justifying and Proving**: no argument or explanation is requested. Only the number goes in the blank.
- **Collaborative Mathematics**: it is a single-student item.

## Most important practices

The task is mostly **Procedural Fluency**, since the work is one division with a remainder. **Mathematical Modeling** is the second most important: the student must pick division rather than multiplication, and must see that a fractional answer is fine here.

### Answer 2: major practice

## Major practice: Procedural Fluency

If I had to pick one, it would be **Procedural Fluency**.

**Why:**

- **Most of the work is the computation.** Turning the problem into math is short and familiar. "$3 per pound, $11 total, how many pounds" is a textbook unit-rate setup, and it points straight to 11 ÷ 3. Most of the student's effort goes into carrying out that division.
- **Most errors happen in the division.** 11 ÷ 3 doesn't come out even. The student has to deal with the remainder (3 R2) and write it correctly as 3 2/3 or 3.67. Common wrong answers include "3," "3 R2," "3.2," "3.3," and 33 (from multiplying). Most of these are procedural mistakes, not modeling mistakes.
- **The answer format checks procedure.** The item asks for a number in a blank, not an explanation or a model. So what gets scored is mainly whether the computation and its written form are right.

**Runner-up: Mathematical Modeling.** It matters at two points: choosing division over multiplication, and seeing that a fractional number of pounds makes sense. Both steps are short and routine for a student at this level, so I'd call Modeling secondary here.

---

## Row 104 (problem_id 43887)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Add the new set of cards to the first set so that all of the cards are ordered from least likely to most likely.

Items to put in order:
- The weather report says there is a 20% chance of rain tomorrow. The chance of rain tomorrow.
- 2 out of every 5 dentists recommend a certain brand of toothpaste. The chance that a random dentist recommends the toothpaste.
- The probability that a certain medical test gives the right result is 0.95. The chance that this medical test is correct for a random patient.
- A fishbowl contains 5 balls where each one has an even number from 2 to 10 written on it and you choose one. The chance that you draw out of ball with the number 3 on it.
- In general English usage, 4/5 of words begin with the letter T. The chance that a randomly chosen word in a novel begins with the letter T.
- A pile contains 6 square pattern blocks and you choose one. The chance that the block you choose has 4 sides of the same length.
- Half of the cards in a deck are red and half are black. Shuffle the cards and select the first card. The chance that the card is red.
- The offspring of two fruit flies in a science experiment have a 75% chance of having redeyes. The chance that the first fly to hatch has red eyes.
- The chance that your opponent will play rock first in a game of paper, rock, scissors.
- 10% of people are left handed. The chance that a randomly chosen person is left handed.
```

### Answer 1: practices in order

## Practices available

The NAEP Mathematics Framework (2026) names five mathematical practices:

1. **Representing**: moving between forms of a quantity (words, percents, fractions, decimals, number lines, likelihood scales).
2. **Abstracting and Generalizing**: finding the underlying mathematical structure in a situation.
3. **Justifying and Proving**: giving reasons why a result is true.
4. **Mathematical Modeling**: turning a real-world situation into a mathematical one, making assumptions, and reading the result back in context.
5. **Collaborative Problem Solving**: working with others on a problem.

Added from the NRC's *Adding It Up*: **Procedural Fluency**, meaning carrying out procedures (here, converting and comparing numbers) accurately and efficiently.

## What the problem needs

Each card describes a chance in a different way. Some give it as a percent, some as a fraction, some as a decimal, and some only as a situation. The student has to turn every card into one comparable number and then sort the cards.

| Card | Probability |
|---|---|
| Ball numbered 3 (only even numbers 2–10 in the bowl) | 0 (impossible) |
| Left-handed person (10%) | 0.10 |
| Rain tomorrow (20%) | 0.20 |
| Opponent plays rock first | 1/3 ≈ 0.33 |
| Dentist recommends (2 out of 5) | 0.40 |
| Red card (half red) | 0.50 |
| Red-eyed fly (75%) | 0.75 |
| Word begins with T (4/5, as stated) | 0.80 |
| Medical test correct (0.95) | 0.95 |
| Square block has 4 equal sides (all blocks are squares) | 1 (certain) |

**Order, least to most likely:** ball with 3 → left-handed → rain → rock → dentist → red card → red-eyed fly → word begins with T → medical test correct → square block with 4 equal sides.

## Practices needed, in order

1. **Mathematical Modeling**: Three cards give no number, so the student must build one from the situation:
   - **Rock:** assume the opponent picks among 3 moves with equal chance, so the probability is 1/3.
   - **Fishbowl:** every ball is even, so drawing a 3 is impossible, giving 0.
   - **Pattern blocks:** every square has 4 equal sides, so the event is certain, giving 1.

   The student must also take each card's stated rate as the probability for one random case. For example, "10% of people" becomes the chance that one randomly chosen person is left-handed.
2. **Representing**: Turn every card into the same form (a decimal or percent from 0 to 1) so the cards can be compared. This means reading "2 out of every 5", "half", "4/5", "75%", and "0.95" as numbers on one probability scale.
3. **Procedural Fluency (NRC)**: Do the conversions accurately (2/5 = 0.4, 4/5 = 0.8, 1/3 ≈ 0.33, 20% = 0.2, and so on). Then compare and sort the ten values from smallest to largest.
4. **Representing (again)**: Place the sorted values on the likelihood scale from impossible (0) to certain (1). Then merge the new cards into the first set of cards at the right spots.
5. **Justifying and Proving (light)**: Check the placements that need a reason rather than a calculation. The 3-ball sits at 0 because no ball has an odd number. The square block sits at 1 because every square has four equal sides. Rock (1/3) goes just below the dentist card (0.4).

**Not needed:** Abstracting and Generalizing is only marginal, and Collaborative Problem Solving does not apply to an individual item.

**Core sequence:** Mathematical Modeling → Representing → Procedural Fluency → Representing → (Justifying)

### Answer 2: major practice

**Major practice: Representing**

The main challenge in this problem is that the ten chances come in different forms:

- percents (20%, 75%, 10%)
- fractions or ratios (2 out of 5, 4/5, half)
- a decimal (0.95)
- plain situations with no number at all (rock-paper-scissors, the fishbowl, the pattern blocks)

To order the cards, the student has to put every one of them into a single common form and place it on one likelihood scale from 0 (impossible) to 1 (certain). Moving between forms like this is what the Representing practice describes.

The other practices play supporting roles:

- **Mathematical Modeling** is needed for only three cards: rock (1/3), the 3-ball (0) and the square block (1). The modeling in each case is simple.
- **Procedural Fluency** covers the arithmetic: converting 2/5 to 0.4 and 1/3 to about 0.33, then sorting. That arithmetic only matters after each card has been represented as a comparable number.
- **Justifying** is a light final check.

If the student cannot see "2 out of every 5", "40%" and "0.4" as the same point on the probability scale, the task fails, so Representing is the practice that decides the item.

---

## Row 106 (problem_id 275212)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
How many 1/5 -liter glasses can Lin fill with a 1 1/2 -liter bottle of water?
____ glasses
```

### Answer 1: practices in order

**Problem:** How many 1/5-liter glasses can Lin fill with a 1 1/2-liter bottle of water?

**Answer:** 7 1/2 glasses. Lin can fill **7 glasses completely**, and the water left over fills half of another glass. (If the question means full glasses only, the answer is 7.)

---

### The practices available

From the NAEP Mathematics Framework (mathematical practices / complexity processes):
1. **Representing**: moving between words, symbols, diagrams and number lines.
2. **Reasoning**: drawing logical conclusions and justifying steps.
3. **Communicating**: stating a result clearly in the context of the problem.
4. **Mathematical Modeling**: turning a real-world situation into a mathematical model and reading the result back in that context.
5. **Procedural fluency** (NRC, *Adding It Up*): doing procedures accurately, efficiently and flexibly.

### Order of practices to solve this problem

**1. Mathematical Modeling (turn the situation into math)**
The student has to see that "how many 1/5-liter glasses fit in 1 1/2 liters" is a measurement (quotative) division question: how many groups of 1/5 are in 1 1/2?
→ Model: 1 1/2 ÷ 1/5

**2. Representing (turn it into a form you can work with)**
Rewrite the mixed number as an improper fraction, 1 1/2 = 3/2. Another way is to put both amounts in the same unit, fifths or tenths: 1 1/2 = 15/10 and 1/5 = 2/10. A number line or tape diagram marked in fifths also works and makes the question concrete.
→ 3/2 ÷ 1/5, or 15 tenths ÷ 2 tenths

**3. Procedural fluency (carry out the calculation)**
Divide the fractions accurately: 3/2 ÷ 1/5 = 3/2 × 5/1 = 15/2 = 7 1/2.
Another way: 15 tenths ÷ 2 tenths = 7.5. Or count by fifths, since 1 liter = 5 glasses and 1/2 liter = 2.5 glasses, so 7.5 in total.
This is the core step, where most errors happen (for example, multiplying instead of dividing to get 3/10, or flipping the wrong fraction).

**4. Reasoning (check that the result makes sense)**
Check: each glass is smaller than 1 liter, so the answer has to be larger than 1 1/2. Since 7.5 > 1.5, that holds. Check back: 7 1/2 × 1/5 = 15/10 = 1 1/2 liters ✓. The student also decides what the "1/2" means: half a glass, i.e. 7 full glasses plus one half-full glass.

**5. Communicating (state the answer in context)**
Write the answer in the blank as a number of glasses: **7 1/2** (or 7.5). If the item wants full glasses only, say "7 full glasses, with 1/10 liter left over."

### Summary

| Order | Practice | Role in this problem |
|---|---|---|
| 1 | Mathematical Modeling | See the situation as 1 1/2 ÷ 1/5 (how many 1/5s in 1 1/2) |
| 2 | Representing | Convert 1 1/2 to 3/2 (or both amounts to tenths), or use a number line or tape diagram |
| 3 | Procedural fluency (NRC) | Compute 3/2 × 5 = 15/2 = 7 1/2 |
| 4 | Reasoning | Check: answer > 1 1/2 because the divisor < 1; check back with 7 1/2 × 1/5 = 1 1/2 |
| 5 | Communicating | Report "7 1/2 glasses" (7 full glasses, plus half a glass) |

**Most essential practices:** Mathematical Modeling (choosing division) and Procedural fluency (fraction division) do the main work. Representing is an important link between them. Reasoning and Communicating are lighter checks at the end.

### Answer 2: major practice

**Major practice: Procedural fluency (NRC)**

**Why this one:**
- **The setup is easy to see.** "How many 1/5-liter glasses can you fill from 1 1/2 liters" is a standard one-step "how many groups" situation. There is only one quantity to divide by and nothing extra in the context, so turning it into 1 1/2 ÷ 1/5 takes little modeling.
- **The difficulty is in the calculation.** To get the answer, the student has to compute accurately with a mixed number and a unit fraction:
  - convert 1 1/2 to 3/2,
  - divide by 1/5, which means multiplying by 5,
  - get 15/2 and write it as 7 1/2.
  The usual mistakes are all procedural: multiplying instead of dividing (3/10), flipping the wrong fraction (2/15), mishandling the mixed number, or dropping the half glass.
- **A wrong answer usually comes from this step.** Most students who miss this item know it is division but get the fraction calculation wrong.

**Runner-up: Mathematical Modeling.** Seeing the situation as "how many 1/5s are in 1 1/2" is the step that has to come first. For a student who is still learning what fraction division means, this step may be the real hurdle. But the context here is simple and direct, so the step is light. Once it is done, the problem comes down to carrying out the procedure.

---

## Row 107 (problem_id 9184)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the sum.
0.401 + 9.28
____
```

### Answer 1: practices in order

**Problem:** Calculate the sum 0.401 + 9.28

**Practices available**
- NAEP 2026 Mathematics Framework practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics
- Added from NRC (*Adding It Up*): Procedural Fluency

This is a one-step decimal addition with no context. Most of the practices don't apply, so the solution uses only two of them.

**Practices used, in order**

1. **Representing.** Rewrite the horizontal expression in vertical form, lining up the decimal points so each digit sits in its place-value column. Writing 9.28 as 9.280 makes the place values easy to compare:
   ```
     0.401
   + 9.280
   -------
   ```
   This is the step where students usually go wrong. If they right-align the digits (as with whole numbers), the decimal points don't line up and they get the wrong answer.

2. **Procedural Fluency (NRC).** Add column by column from right to left, carrying where needed, and bring the decimal point straight down:
   - Thousandths: 1 + 0 = 1
   - Hundredths: 0 + 8 = 8
   - Tenths: 4 + 2 = 6
   - Ones: 0 + 9 = 9

   Result: **9.681**

3. **(Optional) Justifying, a light estimation check.** 0.4 + 9.3 ≈ 9.7, which agrees with 9.681. This step isn't required for the answer, so it is a minor, optional practice here.

**Practices not used:** Abstracting and Generalizing, Mathematical Modeling, and Collaborative Mathematics. There is no pattern to generalize, no real-world situation to model, and no group work.

**Summary order:** Representing → Procedural Fluency → (optional) Justifying

**Answer:** 9.681

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:** The problem asks for a sum with no context: "Calculate the sum 0.401 + 9.28." It tests whether a student can carry out the standard decimal-addition procedure accurately. Lining up the decimal points (the Representing step) is itself part of that standard procedure. It isn't a separate act of building a representation. So the whole solution comes down to running a known algorithm correctly.

**Where Representing fits:** The most common error, misaligning place values (for example, getting 9.689 or 1.329), happens in the alignment step. Representing therefore matters as a supporting practice. But the student isn't choosing or building a new representation. They are using the vertical format that the procedure already prescribes. That makes it secondary.

**Answer:** 0.401 + 9.28 = **9.681**

---

## Row 108 (problem_id 275405)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
How many 1 1/2 -liter bottles of water does it take to fill a 16-liter jug?
____ bottles of water
Express your answer in fraction form.
```

### Answer 1: practices in order

**Problem:** How many 1 1/2-liter bottles of water does it take to fill a 16-liter jug? Give the answer as a fraction.

**Practices I'm drawing on**

From the NAEP 2026 Mathematics Framework:
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematical Discourse

From the NRC's *Adding It Up* (one of the five strands of mathematical proficiency):
- Procedural Fluency: carrying out procedures accurately, efficiently and flexibly.

---

**Practices used, in order**

**1. Mathematical Modeling (setting up the problem)**
Turn the real-world question into a math operation. The question "how many 1 1/2-liter bottles fill 16 liters?" asks how many groups of 1 1/2 fit into 16. That makes it a division problem: 16 ÷ 1 1/2.

**2. Representing**
Rewrite the numbers in a form you can compute with. Change the mixed number 1 1/2 into the improper fraction 3/2, and write 16 as 16/1. The expression becomes 16/1 ÷ 3/2. This step also prepares for the required answer format, a fraction.

**3. Procedural Fluency (NRC)**
Do the fraction division correctly:
- Multiply by the reciprocal: 16/1 × 2/3 = 32/3
- Check that 32/3 is in lowest terms. It is, because 32 and 3 share no common factor.

**4. Mathematical Modeling (interpreting the result)**
Go back to the context to check that the answer makes sense. 32/3 = 10 2/3 bottles, which means 10 full bottles plus 2/3 of another. Check: 10 × 1.5 = 15 liters, so 1 more liter is needed, and 1 ÷ 1.5 = 2/3. The answer is reasonable. Give it in the requested form.

**Answer:** **32/3** bottles of water (equal to 10 2/3).

---

**Summary of the sequence**

Mathematical Modeling (set up) → Representing → Procedural Fluency → Mathematical Modeling (interpret and check)

**Practices not used:** Abstracting and Generalizing (no pattern or general rule is needed), Justifying and Proving (no argument is asked for), and Collaborative Mathematical Discourse (this is a solo task).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why this one:**
- **Most of the work is computing.** You turn 1 1/2 into 3/2, divide 16 by it by multiplying by the reciprocal (16 × 2/3), and get 32/3. That is the step where students are most likely to go wrong. Typical mistakes are multiplying instead of dividing, dividing by 1 and then by 1/2 separately, or failing to convert the mixed number.
- **The modeling step is small.** "How many 1 1/2-liter bottles fill 16 liters" is a standard "how many groups fit" division setup, and the context gives it away. It takes very little modeling.
- **The answer format points the same way.** The problem asks for the answer "in fraction form," so it is testing whether students can carry out and express a fraction computation, not whether they can make sense of a complicated situation.

**Runner-up:** Mathematical Modeling. Recognizing that the situation calls for division is necessary, but it is the easier part of this item.

---

## Row 111 (problem_id 273269)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Tickets to a show cost $5.50 for adults and $4.25 for students. A family is purchasing 2 adult tickets and 3 student tickets.
If the family pays $25, what is the exact amount of change they should receive?
$ ____
```

### Answer 1: practices in order

**Answer: $1.25**

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added Procedural Fluency from the NRC's *Adding It Up* strands.

This problem needs three of them, used in this order:

### 1. Mathematical Modeling
The first step is to turn the word problem into a math model. You have to see that:
- the total cost is (number of adult tickets × adult price) + (number of student tickets × student price), and
- the change is the amount paid minus the total cost.

This gives the expression: Change = 25 − (2 × 5.50 + 3 × 4.25)

### 2. Representing
Next, write that plan as a clear expression or set of steps, keeping track of which number belongs to which quantity. It's easy to swap the prices or the ticket counts here. This practice is closely tied to Step 1 and helps it along.

### 3. Procedural Fluency (NRC)
Then do the decimal arithmetic accurately:
- 2 × $5.50 = $11.00
- 3 × $4.25 = $12.75
- Total = $11.00 + $12.75 = $23.75
- Change = $25.00 − $23.75 = **$1.25**

The words "exact amount" put the weight on getting the decimal multiplication, addition, and subtraction right, including regrouping across the decimal point.

### Practices not really used
- **Abstracting and Generalizing:** there is no pattern or general rule to find.
- **Justifying and Proving:** the answer is a single number with no argument required. At most, you might check that $23.75 + $1.25 = $25.
- **Collaborative Mathematics:** this is a task done alone.

### Summary order
**Mathematical Modeling → Representing → Procedural Fluency**

Procedural Fluency is the main practice here, since most of the difficulty is in the multi-step decimal arithmetic. Modeling comes second: it involves setting up the "total cost, then change" structure.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- **The setup is simple.** Adult tickets cost $5.50 and student tickets cost $4.25. You buy 2 and 3 of them, then take the total away from $25. That is a familiar "total cost, then change" situation, so the modeling step asks very little of the student.
- **The arithmetic is where the work is.** You need two decimal multiplications (2 × 5.50 and 3 × 4.25), one decimal addition ($23.75), and a subtraction with regrouping (25.00 − 23.75 = $1.25).
- **The question asks for an exact answer.** That rules out estimating, so the main thing being tested is whether the decimal calculations are carried out correctly.
- **Errors will mostly be arithmetic slips.** Students who get this wrong will usually miscalculate 3 × 4.25 or regroup wrongly in the subtraction. Very few will misunderstand what the problem is asking.

If you limit the choice to the NAEP framework practices, the main one would be **Mathematical Modeling**, because turning the story into 25 − (2 × 5.50 + 3 × 4.25) is the only non-procedural reasoning needed. Once Procedural Fluency is an option, though, it is the better fit.

---

## Row 114 (problem_id 44015)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Tyler needs some extra calories each day during his sports season. He wants to know how many servings he can have each day if all the extra calories come from the fruit snack. Write an equation that shows the number of servings, n, in terms of the number of calories, c.
n = ____
Use c as your variable.
```

### Answer 1: practices in order

**Practices available (NAEP 2026 Mathematics Framework + NRC):**
Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics (NAEP), plus Procedural Fluency (NRC).

**Note on the problem:** The item depends on a nutrition label (calories per serving of the fruit snack) that is not in the text. Call that number k. The answer has the form **n = c / k** (e.g., if one serving is 90 calories, n = c/90).

**Practices needed, in order:**

1. **Mathematical Modeling** – Read the real-world situation and work out the relationship: all of Tyler's extra calories (c) come from the snack, and each serving gives a fixed number of calories (k). So the number of servings is the total calories divided by the calories per serving. This step turns the story into a mathematical relationship.

2. **Abstracting and Generalizing** – The relationship has to hold for *any* calorie amount, not one specific number. The student has to move from "if he needs 180 calories, that's 2 servings" to a general rule that uses c as a variable.

3. **Representing** – Write the relationship as a symbolic equation in the required form, with n alone on one side and expressed in terms of c: n = c / k. The student also has to choose the right direction (c divided by k, not k divided by c, and not n = kc, which is the most common mistake).

4. **Procedural Fluency (NRC)** – Carry out the symbol work correctly: write the division (or the equivalent multiplication by 1/k) properly, use the given variable c, and enter the expression in the required format. This step is short but needed to give an answer that can be scored.

**Not needed:** Justifying and Proving (no argument or explanation is asked for) and Collaborative Mathematics (an individual task).

**Summary order:** Mathematical Modeling -> Abstracting and Generalizing -> Representing -> Procedural Fluency

### Answer 2: major practice

**Major practice: Representing**

Why:

- **What the task asks for is a representation.** The student has to turn a verbal situation (and the snack's nutrition information) into a symbolic equation, n = c / k. In the NAEP framework, translating from words or context into symbols is the central case of Representing.
- **The main difficulty is there.** Most errors come from writing the relationship the wrong way: n = kc, n = k/c, or swapping the variables. Choosing the correct symbolic form is the step that decides whether the answer is right.
- **The other practices play smaller roles:**
  - *Mathematical Modeling* is light here. The situation is already simplified, so there are no assumptions to make, no model to refine, and no result to interpret back in context. It is a simple translation, not a full modeling cycle.
  - *Abstracting and Generalizing* only means using a variable instead of a specific number, and the item hands the student the variable ("Use c as your variable").
  - *Procedural Fluency* is minimal, because nothing needs to be computed or simplified.

If a second practice were allowed, it would be Mathematical Modeling, because the student has to understand the context first ("all extra calories come from the snack" means total calories divided by calories per serving). Still, the skill this item mainly measures is building the right symbolic representation.

---

## Row 119 (problem_id 45802)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
How many of the values in this data set are between the first quartile and the median?
____
```

### Answer 1: practices in order

**Note:** The problem text doesn't include the data set itself. It was probably a list, dot plot, stem-and-leaf plot, or table that didn't come through. So I can't give the number, but I can lay out the practices and their order.

**The practice set (NAEP 2026 Mathematics Framework practices, plus one from NRC)**
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics
- *Procedural Fluency* (NRC, *Adding It Up*): carrying out procedures flexibly, accurately, and efficiently

**Practices needed, in order**

1. **Representing (first)**
   - Read the data set from the form it's given in (list, plot, or table).
   - Turn it into an ordered list of values, smallest to largest.
   - This also means understanding what "first quartile" and "median" mean as positions in that ordered data. The question is about where values sit in the distribution, which is a representational idea.

2. **Procedural Fluency (second)**
   - Find the median: the middle value, or the mean of the two middle values if the count is even.
   - Find Q1: the median of the lower half. Use the convention the course teaches, usually leaving out the overall median when n is odd.
   - These are routine steps. Doing them accurately is the core work of the problem.

3. **Representing again, with a light check (third)**
   - Go back to the ordered list and count the values strictly between Q1 and the median.
   - Watch the boundaries: are Q1 or the median themselves data values? Are there repeated values at either end?
   - About 25% of the data should fall in this range. That gives a quick sanity check on the count.

**Not needed:** Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. The problem asks for a single computed count. It doesn't ask for a general rule, an argument, a real-world model, or group work.

**Summary order:** Representing, then Procedural Fluency, then Representing (count and check). Procedural Fluency carries the most weight.

### Answer 2: major practice

**Major practice: Procedural Fluency**

Why this one:
- The core of the problem is two standard procedures: putting the data in order, then finding the median and the first quartile (the median of the lower half). After that, the student counts the values between them.
- Most errors happen in these steps. Students order the values wrong, pick the wrong middle when there's an even count, or use the wrong Q1 convention (including or leaving out the median). They also miscount at the boundaries.
- Representing matters too, since the student has to read the data and understand quartiles as positions. But that part is a lighter setup. It isn't where the work of this problem is.

So if I have to pick one, it's **Procedural Fluency**. Representing is a secondary practice that supports it.

---

## Row 120 (problem_id 46539)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression when x is 4 and y is 6.
2^x - 2y
____
```

### Answer 1: practices in order

**Problem:** Evaluate 2^x − 2y when x = 4 and y = 6.
**Answer:** 2^4 − 2(6) = 16 − 12 = **4**

## Practices available

The 2026 NAEP Mathematics Framework names five mathematical practices. I've added Procedural Fluency from the NRC's *Adding It Up* as a sixth:

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics
6. Procedural Fluency (NRC)

## Practices needed, in order

### Step 1: Representing
The student first has to read the symbolic expression correctly and swap in the given values:
- Read the notation correctly. 2^x is an exponent (2 multiplied by itself x times), not 2·x. 2y means 2 times y, not the two-digit number "2y".
- Replace each variable with its value: 2^x − 2y becomes 2^4 − 2(6).

This step is about understanding and translating between symbolic forms, which is the core of Representing. Most errors on this kind of item happen here: reading 2^4 as 8, or reading 2y as "26".

### Step 2: Procedural Fluency (NRC)
Next the student carries out the arithmetic accurately and in the right order:
- Exponent first: 2^4 = 16
- Then multiplication: 2 × 6 = 12
- Then subtraction: 16 − 12 = 4

This is routine work done in a fixed order (order of operations, powers, multiplication facts). That makes it Procedural Fluency.

## Practices not needed
- **Abstracting and Generalizing:** no pattern or general rule has to be found. The values are given.
- **Justifying and Proving:** the student doesn't have to explain or argue anything.
- **Mathematical Modeling:** there is no real-world situation to turn into math. The expression is already given.
- **Collaborative Mathematics:** this is a task done alone.

## Summary

| Order | Practice | Role in this problem |
|---|---|---|
| 1 | Representing | Read 2^x and 2y correctly and substitute x = 4, y = 6 |
| 2 | Procedural Fluency (NRC) | Compute 16 − 12 = 4 using the order of operations |

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:

- **The item is a direct evaluation task.** It hands the student the expression and the values. All that's left is to carry out a known procedure: substitute, apply the exponent, multiply, and subtract (16 − 12 = 4). Getting that procedure right, in order and without mistakes, is what Procedural Fluency means.
- **The Representing step is small.** Reading 2^x as a power and 2y as 2 × y, then plugging in the numbers, is part of the procedure for evaluating an expression. The student doesn't have to switch between representations (such as a table, graph, or words) or build one. They only need to read standard notation.
- **Where students go wrong points the same way.** The usual errors are computing 2^4 as 8, treating 2y as 26, or getting the order of operations wrong. These are slips in carrying out the procedure or in a notation convention, which are fluency problems, not problems understanding a representation.

Representing still matters as the first step. But if I had to pick one practice for this item, it's **Procedural Fluency**.

---

## Row 121 (problem_id 46338)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression below.
7 + 2^3
____
```

### Answer 1: practices in order

**Problem:** Evaluate 7 + 2^3

**Answer:** 7 + 2^3 = 7 + 8 = **15**

## Practices available

The NAEP Mathematics Framework lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

For this problem I'm also counting **Procedural Fluency** from the NRC's *Adding It Up* strands. It means carrying out procedures flexibly, accurately, and efficiently.

## Which practices are used, and in what order

This is a short computation item, so most of the NAEP practices barely come into play. The order is:

**1. Representing (interpreting the symbolic notation)**
- The student has to read the expression correctly. "2^3" is an exponent, meaning 2 x 2 x 2. It is not 2 x 3, and it is not "23."
- This means turning the written notation into the operations it stands for. It's a light, receptive use of Representing: the student reads one representation and doesn't have to build or switch between representations.

**2. Procedural Fluency (NRC), the main practice**
- Use the order of operations: work out the exponent before the addition.
  - 2^3 = 2 x 2 x 2 = 8
  - 7 + 8 = 15
- Most of the work, and most of the likely errors, happen in this step. Typical mistakes:
  - Adding first: (7 + 2)^3 = 729
  - Treating the exponent as multiplication: 2 x 3 = 6, giving 13
  - Arithmetic slips

**3. (Optional, minor) Justifying, as a self-check**
- A careful student might quickly check that the exponent was done before the addition, or that 2^3 really is 8. The item doesn't ask for this, so it's an implicit check at most and not an assessed practice.

## Practices not used
- **Abstracting and Generalizing:** no pattern or general rule has to be found.
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** this is an individual item.
- **Justifying and Proving:** no argument is asked for. At most it's the informal self-check above.

## Summary

| Order | Practice | Role | Weight |
|---|---|---|---|
| 1 | Representing | Read the exponent notation 2^3 as repeated multiplication | Low to moderate |
| 2 | Procedural Fluency (NRC) | Apply order of operations, compute 8, then 7 + 8 = 15 | **Primary** |
| 3 | Justifying (optional) | Quick self-check of the order of operations | Minimal |

**Main practice:** Procedural Fluency. **Sequence:** Representing, then Procedural Fluency, with an optional brief self-check at the end.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:
- The item is a bare computation. It has no context to model, no pattern to generalize, and no argument to make. What it tests is whether the student can carry out the procedure correctly: work out the exponent first (2^3 = 8), then add (7 + 8 = 15).
- The likely errors are procedural: adding before applying the exponent, which gives 729, or reading 2^3 as 2 x 3, which gives 13. Whether the student gets the right answer depends on doing the procedure correctly.
- Representing, which here means reading the exponent notation, is only a quick first step. It feeds into the procedure and isn't what the item is mainly assessing.

So if only one practice can be chosen, it is **Procedural Fluency**.

---

## Row 122 (problem_id 46909)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression below.
2 · 6^2
____
```

### Answer 1: practices in order

**Problem:** Evaluate 2 · 6^2

**Practice set:** The NAEP Mathematics Framework (2026) names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added a sixth from the NRC (*Adding It Up*): Procedural Fluency.

## Practices to use, in order

### 1. Representing
Read the symbols correctly before doing any arithmetic:
- 6^2 means 6 × 6. It does not mean 6 × 2.
- The dot "·" means multiply.
- The exponent applies only to the 6, not to 2 · 6. So the expression is 2 × (6 × 6), not (2 × 6)^2.

This is the step that decides whether the answer is right. The two common mistakes both happen here: reading 6^2 as 6 × 2, or squaring 2 · 6 to get 144.

### 2. Procedural Fluency (NRC)
Use order of operations: exponents before multiplication.
- 6^2 = 36
- 2 × 36 = **72**

## Practices not needed
- **Abstracting and Generalizing:** Nothing needs generalizing. It's a single numeric expression.
- **Justifying and Proving:** The question asks for a value, not an argument.
- **Mathematical Modeling:** There's no real-world context to turn into math.
- **Collaborative Mathematics:** This is a solo item.

## Summary
**Representing → Procedural Fluency.** Answer: **72**

Representing does most of the thinking (reading what the notation means). Procedural fluency does the rest (exponent first, then multiply).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The task is "Evaluate 2 · 6^2". It asks for a value and nothing else. To get it, you carry out a standard procedure: exponent first, then multiply (6^2 = 36, then 2 × 36 = 72).
- Reading 6^2 as 6 × 6 and applying the exponent only to the 6 are themselves part of the procedure. Knowing that exponents bind tighter than multiplication *is* the order-of-operations rule. So the step I called "Representing" earlier really belongs to procedural knowledge here.
- No representation needs to be built or translated. There is no table, graph, diagram, or context. The expression comes already written in standard symbols.
- A wrong answer like 24 (6 × 2 × 2) or 144 ((2 · 6)^2) shows a gap in procedural knowledge: exponent meaning or order of operations. It doesn't show a failure to represent.

**A correction to my earlier answer:** I said Representing "does most of the thinking." On reflection, that overstated it. Reading the notation is a small step, and in a pure evaluate-the-expression item it falls under procedural knowledge. Representing is at most a minor practice here.

**Answer:** 72

---

## Row 123 (problem_id 46425)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression when x is 4 and y is 6.
2 + x^3
____
```

### Answer 1: practices in order

**Problem:** Evaluate 2 + x³ when x = 4 and y = 6.

**Practices available:** The NAEP 2026 framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. You asked me to add one more, **Procedural Fluency** from the NRC's *Adding It Up* strands.

## Practices needed, in order

**1. Representing (read and set up the symbols)**
- Read the symbolic expression 2 + x³. The superscript means x is multiplied by itself three times, not x × 3.
- Notice that the expression contains only x. The value y = 6 is extra information and is not used.
- Replace x with 4 to get the numeric expression 2 + 4³.

**2. Procedural Fluency (NRC) (do the calculation)**
- Follow the order of operations: work out the exponent before adding.
- 4³ = 4 × 4 × 4 = 64
- 2 + 64 = **66**

## Practices not needed
- **Abstracting and Generalizing:** there is no pattern or general rule to find. It is a single substitution.
- **Justifying and Proving:** the problem doesn't ask for an argument or proof.
- **Mathematical Modeling:** there is no real-world situation to turn into math.
- **Collaborative Mathematics:** the problem is solved alone.

**Order:** Representing → Procedural Fluency

**Answer: 66**

Common mistakes:
- Computing 4 × 3 = 12 instead of 4³. This is a Representing error.
- Adding before raising to the power, giving (2 + 4)³ = 216. This is a Procedural Fluency error.
- Trying to use y = 6 somewhere. This is a Representing error.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:
- Most of the work is computation: put 4 in for x, follow the order of operations (exponent first), work out 4³ = 64, then add 2 to get 66.
- Representing does play a part, but it is a small one. It only means reading x³ as a power and seeing that y = 6 isn't used. The expression is already written in symbols, so nothing has to be translated between forms.
- Most wrong answers come from mistakes in procedure, such as computing 4 × 3 = 12 instead of 4³, or adding before taking the power to get (2 + 4)³ = 216. Getting this item right mostly shows that a student can carry out the evaluation procedure correctly.

So Procedural Fluency is the major practice, and Representing is a minor supporting practice.

---

## Row 124 (problem_id 46711)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression below.
20 - 2^4
____
```

### Answer 1: practices in order

**Problem:** Evaluate 20 − 2^4

**Answer: 4** (2^4 = 16, and 20 − 16 = 4)

### Practices used, in order

The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Modeling, and Collaborative Mathematics. I have added **Procedural Fluency** from the NRC's *Adding It Up* strands, as you asked.

This is a short, purely symbolic computation. Only two practices really apply.

1. **Representing (NAEP).** First, read the symbolic notation correctly. The student has to see that "2^4" is an exponent (2 · 2 · 2 · 2), not 2 × 4 or 24. They also have to see that the expression has two parts: a subtraction, and an exponent inside it. This parsing decides which operation comes first. The classic mistakes (computing 20 − 2 = 18 and then 18^4, or treating 2^4 as 8) are failures at this step.

2. **Procedural Fluency (NRC).** Next, carry out the procedure correctly and efficiently:
   - Apply the order of operations: the exponent before the subtraction.
   - Compute 2^4 = 16.
   - Compute 20 − 16 = 4.

   This is the main practice for the item. Most of the work is recalling and running the order-of-operations rule and basic arithmetic accurately.

### Practices not needed

- **Abstracting and Generalizing:** no pattern or general rule has to be found. The student only applies a known convention.
- **Justifying and Proving:** the item asks only for a value, with no explanation or argument.
- **Modeling:** there is no real-world situation to turn into math.
- **Collaborative Mathematics:** this is a single-student item.

**Order:** Representing → Procedural Fluency. Procedural fluency is the main practice and representing plays a supporting role.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

For 20 − 2^4, most of the work is carrying out a known procedure correctly:
- apply the order of operations (exponent before subtraction),
- compute 2^4 = 16,
- compute 20 − 16 = 4.

Representing is needed too, but it plays a small, supporting role. Recognizing standard exponent notation is quick, and it is really part of knowing the procedure. There is nothing to model, generalize, or justify. Whether a student gets this item right mostly depends on applying the order-of-operations rule and doing the arithmetic accurately, which is procedural fluency.

---

## Row 125 (problem_id 46924)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression when x is 4 and y is 6.
(2^x)/(x^2)
____
```

### Answer 1: practices in order

## Practices for this problem

**Problem:** Evaluate (2^x)/(x^2) when x = 4 and y = 6.

**The NAEP mathematical practices (2026 framework):** Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Added from the NRC strands: **Procedural Fluency**.

### Practices used, in order

1. **Representing.** Read the symbolic expression correctly and turn it into numbers. That means seeing 2^x as "2 raised to the x power" and x^2 as "x squared". It also means noticing that the expression has no y in it, so y = 6 is extra information. Substituting x = 4 gives (2^4)/(4^2).

2. **Procedural Fluency (NRC).** Do the arithmetic accurately and in the right order. Work out the exponents first: 2^4 = 16 and 4^2 = 16. Then divide: 16/16 = **1**. Most of the work is here, and the most likely mistakes happen here too, such as computing 2·4 = 8 or 4·2 = 8, or mixing up base and exponent.

3. **Justifying and Proving (minor, optional).** Check the result quickly. The numerator and denominator are both 16, which makes sense because 2^4 = (2^2)^2 = 4^2. So the answer of 1 is reasonable.

### Practices not used
- **Abstracting and Generalizing:** no pattern or general rule is needed.
- **Mathematical Modeling:** there is no real-world situation to model.
- **Collaborative Mathematics:** this is a task done alone.

**Order:** Representing → Procedural Fluency → (Justifying and Proving as a check)

**Answer:** 1

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Most of the problem comes down to carrying out a known procedure correctly: substitute x = 4, compute 2^4 = 16 and 4^2 = 16, then divide to get 1. Representing does play a part, since you have to read the notation and see that y is extra information. That step is small and routine, though. Whether a student gets this item right depends mostly on computing the exponents correctly (for example, not writing 2·4 or 4·2) and following the order of operations. Those are procedural fluency skills.

---

## Row 126 (problem_id 46527)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression below.
9 · 3^1
____
```

### Answer 1: practices in order

**Problem:** Evaluate 9 · 3^1

**Answer: 27**

**Practices available.** The NAEP 2026 Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added the NRC's *Procedural Fluency* (from *Adding It Up*).

This is a one-step symbolic computation, so only two practices are needed:

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Reads the symbolic notation correctly. "3^1" is an exponent, meaning 3 raised to the first power (one factor of 3), and "·" means multiplication. By order of operations, the exponent is evaluated before the multiplication. |
| 2 | **Procedural Fluency** (NRC) | Carries out the steps accurately: 3^1 = 3, then 9 · 3 = 27. |

**Practices not needed:**
- **Abstracting and Generalizing:** no pattern or general rule has to be found. The student only applies the fact that a^1 = a.
- **Justifying and Proving:** the problem doesn't ask for an argument or explanation.
- **Mathematical Modeling:** there is no real-world situation to turn into math.
- **Collaborative Mathematics:** this is a task done alone.

**Order: Representing, then Procedural Fluency.** Most of the load is on Procedural Fluency. The main chance for error is in Representing: misreading 3^1 as 3 · 1 (which gives the same answer here by luck) or as 3 + 1, or misapplying the exponent as (9 · 3)^1 (which also gives 27, so this item can't tell the two readings apart).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item is a direct "evaluate the expression" task. Its main demand is carrying out a known procedure accurately: compute 3^1 = 3, then 9 · 3 = 27. Representing is only a brief first step. The student just has to recognize exponent notation and apply order of operations, and that reading is simple here. Because a^1 = a, the most common misreadings still give 27, so the item can't really tell whether a student read the notation correctly. What it does measure is whether the student can run the computation fluently. That makes Procedural Fluency the major practice and Representing a minor one.

---

## Row 127 (problem_id 46811)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression when x is 4 and y is 6.
1^x + 2^x
____
```

### Answer 1: practices in order

**Problem:** Evaluate 1^x + 2^x when x = 4 and y = 6.

**Answer:** 1^4 + 2^4 = 1 + 16 = **17**. (The value y = 6 isn't used, because y does not appear in the expression.)

---

### Available practices
The NAEP 2026 Mathematics Framework names five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

The NRC strand you asked to include:

6. **Procedural Fluency**: carrying out procedures flexibly, accurately and efficiently.

### Practices needed, in order

**Step 1: Representing**
- Read the symbols: x is a variable, and in 1^x and 2^x it is the exponent.
- Substitute: replace each x with 4, so the expression becomes 1^4 + 2^4.
- Notice that y is given but does not appear in the expression, so it is a distractor and is ignored.
- This is Representing because the work is turning symbols and given values into a specific numeric expression.

**Step 2: Procedural Fluency**
- Use exponents as repeated multiplication:
  - 1^4 = 1 x 1 x 1 x 1 = 1
  - 2^4 = 2 x 2 x 2 x 2 = 16
- Follow the order of operations: work out the powers first, then add. 1 + 16 = 17.
- This is the routine calculation, and it has to be accurate. A common mistake is 2^4 = 8 (computing 2 x 4 instead of the power) or 1^4 = 4.

### Practices not needed
- **Abstracting and Generalizing:** no pattern or general rule has to be found. It is a single substitution.
- **Justifying and Proving:** no argument or proof is asked for.
- **Mathematical Modeling:** there is no real-world situation to model.
- **Collaborative Mathematics:** this is an individual item.

### Summary
**Representing -> Procedural Fluency**

| Order | Practice | Role in this problem |
|---|---|---|
| 1 | Representing | Read the symbols, substitute x = 4, ignore the unused y |
| 2 | Procedural Fluency | Work out 1^4 = 1 and 2^4 = 16, then add to get 17 |

### Answer 2: major practice

**Major practice: Procedural Fluency**

**Why:**
- **Most of the work is calculation.** Substituting x = 4 is quick. The real task is working out the powers correctly (1^4 = 1, 2^4 = 16), following the order of operations, and adding to get 17.
- **Most wrong answers come from it.** Typical mistakes are treating 2^4 as 2 x 4 = 8, writing 1^4 = 4, or adding before working out the powers. These are all errors in carrying out the procedure.
- **Representing plays a small role.** It is needed for reading the symbols, substituting x = 4 and ignoring y. But the expression is short and the substitution is direct, so this part is unlikely to be what separates students who get it right from those who don't. (The unused y adds a little Representing difficulty, but only a little.)

**In short:** Representing gets the student started, but Procedural Fluency decides whether they get the right answer, so it is the major practice.

---

## Row 128 (problem_id 46683)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression when x is 4 and y is 6.
(1/2)^x
____
```

### Answer 1: practices in order

**Problem:** Evaluate (1/2)^x when x = 4 and y = 6.

**Practices available:** the five NAEP mathematical practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus **Procedural Fluency** from the NRC strands of mathematical proficiency.

### Practices used, in order

**1. Representing (NAEP)**
- Read the symbols correctly. The expression is the base 1/2 raised to the exponent x, and it means multiplying 1/2 by itself x times.
- Note that the expression has only x in it. The value y = 6 is extra information and plays no part.
- Put the given value in for the variable: (1/2)^x becomes (1/2)^4. This step moves from a symbolic expression with a variable to a specific numeric expression.

**2. Procedural Fluency (NRC)**
- Work out the power the standard way, accurately and efficiently:
  (1/2)^4 = (1/2)(1/2)(1/2)(1/2) = 1^4 / 2^4 = 1/16
- Equivalently, apply the exponent to the numerator and the denominator separately: 1/16 (or 0.0625).

**Answer: 1/16**

### Practices not needed
- **Abstracting and Generalizing:** you don't have to find a pattern or make a general rule. You just evaluate one case.
- **Justifying and Proving:** the problem doesn't ask for an argument or justification.
- **Mathematical Modeling:** there is no real-world situation to model.
- **Collaborative Mathematics:** this is an individual computation.

**Order:** Representing → Procedural Fluency. Representing comes first: you read the notation, ignore the extra y, and substitute x = 4. Procedural Fluency then carries out the exponent computation.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Most of the problem is the computation itself: evaluating (1/2)^4 = 1/16. To get it right, a student has to carry out the exponent procedure correctly. That means multiplying 1/2 by itself four times, or raising the numerator and the denominator to the 4th power. Common mistakes are procedural ones, such as computing 1/2 × 4 = 2 or 1/8.

Representing comes before it, but it's a small step. You read the notation, ignore the extra y = 6, and substitute x = 4. Once that substitution is done, success depends almost entirely on doing the exponent computation fluently, so Procedural Fluency is the major practice.

---

## Row 129 (problem_id 47289)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression below.
1/3 · 3^3
____
```

### Answer 1: practices in order

**Problem:** Evaluate 1/3 · 3^3

**Answer: 9**

**Practices available**

- NAEP 2026 Mathematical Practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics
- Added from the NRC strands: Procedural Fluency

**Which practices to use, in order**

1. **Representing (to read the notation).** First you have to understand what the symbols mean. 3^3 is shorthand for 3 · 3 · 3, and "1/3 ·" means multiply by one-third, which is the same as dividing by 3. Moving from the compact exponent form to repeated multiplication is the representational step. Everything after it depends on reading the exponent correctly, for example not mistaking 3^3 for 3 · 3 = 9.

2. **Procedural Fluency (to calculate).** Next comes the arithmetic, done correctly and in the right order:
   - Apply the exponent first: 3^3 = 27
   - Then multiply: 1/3 · 27 = 27/3 = 9

   An equally quick route is to cancel one factor of 3: (1/3) · 3 · 3 · 3 = 3 · 3 = 9. Choosing the more efficient route is also part of fluency.

**Practices not really needed**

- **Abstracting and Generalizing:** You could treat this as the rule (1/a) · a^n = a^(n-1). That is optional, though, because the plain calculation is enough.
- **Justifying and Proving, Mathematical Modeling, Collaborative Mathematics:** These don't apply. Nothing has to be argued or proved, there is no real-world situation to model, and the item is a single-step task done alone.

**Summary:** Representing, then Procedural Fluency. Procedural Fluency is the main practice here, and Representing is a quick first step to read the exponent.

### Answer 2: major practice

**Major practice: Procedural Fluency**

This item is mostly about carrying out a known procedure correctly:

- apply the exponent first: 3^3 = 27
- then multiply by one-third: 27 / 3 = 9

There's no situation to model and nothing to justify or generalize. The representing step, reading 3^3 as 3 · 3 · 3, is small and basic, and it's really part of knowing the procedure anyway.

A student who gets this wrong has almost always made a procedural slip, not a conceptual or representational one. Typical slips are:

- computing 3^3 as 9 (3 · 3) instead of 27
- taking 3^3 to mean 3 · 3 = 9
- doing the operations in the wrong order

So Procedural Fluency is the practice that best explains whether a student gets this right.

---

## Row 130 (problem_id 47479)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression below.
(1/5 · 5)^5
____
```

### Answer 1: practices in order

**Problem:** Evaluate (1/5 · 5)^5

**Solution:** 1/5 · 5 = 1, and 1^5 = 1. **Answer: 1**

---

### Practices available

The NAEP Mathematics Framework (2026) has five practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands. It means carrying out procedures flexibly, accurately and efficiently.

### Practices needed, in order

**1. Representing (interpret the notation)**
First, read the symbolic expression correctly. The parentheses group 1/5 · 5 into one quantity, and the exponent 5 applies to that whole quantity, not just to the last 5. So the order of operations says: simplify inside the parentheses first, then apply the power. This step is the main place students go wrong, for example by computing 1/5 · 5^5.

**2. Abstracting and Generalizing (spot the structure)** *(small but useful role)*
Next, notice two general properties:
- A number times its reciprocal is 1: (1/a) · a = 1.
- 1 raised to any power is 1: 1^n = 1.

Seeing this structure turns the problem into a short shortcut. Without it, a student might work out 5^5 = 3125 and then divide.

**3. Procedural Fluency (NRC) (do the computation)**
Finally, do the arithmetic accurately: 1/5 · 5 = 1, then 1^5 = 1.

### Practices not needed
- **Justifying and Proving:** the item asks only for a value, not an argument.
- **Mathematical Modeling:** there is no real-world context.
- **Collaborative Mathematics:** this is an individual task.

### Summary
**Representing → Abstracting and Generalizing → Procedural Fluency**

Procedural Fluency carries most of the load. Representing (reading the parentheses and exponent correctly) is the step most likely to cause errors.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item says "Evaluate the expression." It is a pure computation task with no context, no argument to build and no model to construct.
- Most of the work is running a known procedure correctly: follow the order of operations (parentheses first, then the exponent), multiply 1/5 · 5 = 1, then compute 1^5 = 1.
- Representing and Abstracting and Generalizing do help, but only in small ways. Reading the parentheses correctly and noticing the reciprocal shortcut are both part of using the procedure fluently: knowing when and how to apply order of operations and spotting an efficient route. Neither is a separate main demand of the problem.

So if only one practice can be chosen, it is **Procedural Fluency**.

---

## Row 132 (problem_id 47109)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression below.
8 · (1/2)^2
____
```

### Answer 1: practices in order

**Problem:** Evaluate 8 · (1/2)^2

**Answer:** 8 · (1/2)^2 = 8 · 1/4 = **2**

## NAEP Mathematical Practices (plus NRC Procedural Fluency)

The NAEP 2026 Mathematics Framework lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Modeling
5. Collaborative Mathematics

Added from the NRC (*Adding It Up*) strands:
6. **Procedural Fluency**: carrying out procedures flexibly, accurately, efficiently, and appropriately.

## Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (minor, light use) | Reads the symbolic expression and interprets the notation: the raised dot means multiplication, and the exponent 2 applies only to the fraction (1/2). Knowing what the symbols mean sets up the order of operations: exponent first, then multiply. |
| 2 | **Procedural Fluency** (primary) | Does the computation: (1/2)^2 = 1/2 · 1/2 = 1/4 (square the numerator and the denominator), then 8 · 1/4 = 8/4 = 2. |

**Order:** Representing → Procedural Fluency

## Practices not needed
- **Abstracting and Generalizing:** there is no pattern or general rule to find. It is a single concrete expression.
- **Justifying and Proving:** the problem asks for a value, not an argument.
- **Modeling:** there is no real-world situation to turn into math.
- **Collaborative Mathematics:** this is an individual computation task.

**Summary:** This is essentially a procedural fluency item about order of operations, exponents on fractions, and multiplying a whole number by a fraction. Representing only matters in the small sense of reading the notation correctly.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Nearly all of the work in this problem is procedural:
- Applying the order of operations, so the exponent is done before the multiplication
- Squaring a fraction: (1/2)^2 = 1/4
- Multiplying a whole number by a fraction and simplifying: 8 · 1/4 = 2

Representing only shows up in the small sense of reading standard notation correctly. The student doesn't have to build, choose, or translate between representations. So if one practice has to carry the item, it's Procedural Fluency.

---

## Row 133 (problem_id 92124)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Use long division to find the quotient. Write your answer as a decimal.
99 ÷ 12
____
```

### Answer 1: practices in order

## Problem
Use long division to find the quotient. Write your answer as a decimal: **99 ÷ 12**

**Answer: 8.25**

## Practices available
I used the five NAEP mathematical practices (2026 framework) and added the NRC strand you asked for:

1. **Representing**: moving between forms of a mathematical idea (symbols, diagrams, tables, number forms)
2. **Abstracting and Generalizing**: spotting structure and stating general patterns or rules
3. **Justifying and Proving**: building and checking arguments for why something is true
4. **Mathematical Modeling**: using math to represent and solve real-world situations
5. **Collaborative Mathematical Discourse**: talking through and refining math ideas with others
6. **Procedural Fluency (NRC)**: carrying out procedures flexibly, accurately, efficiently and appropriately

## Practices needed, in order

### Step 1: Representing
Rewrite the horizontal expression 99 ÷ 12 in the long-division layout, with 12 as the divisor outside and 99 as the dividend inside. Because the answer must be a decimal, also write the dividend as **99.00** (a decimal point plus placeholder zeros). The problem tells you to change the format here. Seeing that 99 and 99.00 are the same number is a representation move.

### Step 2: Procedural Fluency (NRC), the main practice
Run the long-division steps (divide, multiply, subtract, bring down) correctly:
- 12 goes into 99 **8** times: 8 × 12 = 96, and 99 − 96 = **3**
- Put the decimal point in the quotient straight above the one in the dividend. Bring down a 0 to get 30.
- 12 goes into 30 **2** times: 2 × 12 = 24, and 30 − 24 = **6**
- Bring down another 0 to get 60. 12 goes into 60 **5** times: 5 × 12 = 60, and 60 − 60 = **0**
- The remainder is 0, so the division ends: **8.25**

Most of the work, and most of the ways to go wrong, sit in this step. Common errors are a misplaced decimal point, stopping at "8 R3", or a subtraction or multiplication fact error.

### Step 3: Justifying and Proving (light, as a check)
Confirm the result makes sense:
- Check by multiplying back: 12 × 8.25 = 96 + 3 = 99 ✓
- Or estimate: 12 × 8 = 96, which is just under 99, so the answer should be a little more than 8 ✓
- The leftover 3/12 = 1/4 = 0.25 matches the decimal part ✓

## Practices not needed
- **Abstracting and Generalizing**: you don't need to find a pattern or general rule
- **Mathematical Modeling**: there is no real-world context to turn into math
- **Collaborative Mathematical Discourse**: the problem is solved alone, with no discussion or critique of others' reasoning

## Summary
**Representing → Procedural Fluency → Justifying and Proving (check)**

Procedural Fluency is the main practice. This is mostly a test of whether the student can carry out long division correctly past the decimal point. Representing sets up the problem, and Justifying is an optional but useful final check.

### Answer 2: major practice

## Major practice: Procedural Fluency (NRC)

If I had to pick just one, it would be **Procedural Fluency**.

**Why:**
- **The problem names the procedure.** "Use long division" tells the student which method to use. They don't have to choose a strategy, model a situation, or interpret anything.
- **Most of the work happens here.** Solving it means running the divide, multiply, subtract, bring down cycle three times (99 → 30 → 60) and correctly carrying the work past the decimal point to get **8.25**.
- **Most errors come from here.** The usual mistakes are all procedural: stopping at "8 R3" instead of continuing into decimals, putting the decimal point in the wrong place in the quotient, or making a slip in a multiplication or subtraction fact.
- **The other practices are small.** Representing only means writing 99 as 99.00 in the division layout, which is a quick setup step. Justifying is an optional check (12 × 8.25 = 99). Neither one decides whether the student gets the right answer.

**In short:** the item checks whether a student can carry out long division accurately into the decimal places. That is procedural fluency.

---

## Row 134 (problem_id 48612)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What value of d makes the equation true?
12 + d = -4.8
d = ____
```

### Answer 1: practices in order

**Problem:** Find the value of d that makes 12 + d = -4.8 true.

The NAEP Mathematics Framework lists five mathematical practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics). I've added **Procedural Fluency** from the NRC's *Adding It Up* strands as a sixth.

The problem is short and purely symbolic, so only a few practices are really needed. In the order they are used:

| Order | Practice | How it is used in this problem |
|---|---|---|
| 1 | **Representing** (NAEP) | Read the equation as a balance or relationship. "12 plus an unknown number gives -4.8" means d is the number that moves you from 12 to -4.8 on a number line. Seeing it this way tells you d has to be **negative**, because the total is less than 12. It also shows that the inverse operation, subtracting 12, will isolate d. |
| 2 | **Procedural Fluency** (NRC) | Carry out the steps correctly and efficiently: subtract 12 from both sides, giving d = -4.8 - 12. Then do signed-decimal arithmetic: -4.8 - 12 = -(4.8 + 12) = **-16.8**. This is the main practice for the problem. Most errors happen here, such as getting 7.2 or -7.2 by mixing up the signs, or misplacing the decimal point. |
| 3 | **Justifying and Proving** (NAEP), light use | Check the answer by substituting it back: 12 + (-16.8) = -4.8 ✓. This confirms the value really makes the equation true, which is what the question asks for. |

**Practices not needed:**
- **Abstracting and Generalizing:** no pattern or general rule is asked for. The equation is already written in symbols.
- **Mathematical Modeling:** there is no real-world situation to turn into math.
- **Collaborative Mathematics:** this is an individual item with nothing to communicate or critique.

**Order:** Representing → Procedural Fluency → Justifying and Proving (check)

**Answer:** d = **-16.8**

The main practice is **Procedural Fluency**: solving a one-step equation with an inverse operation, plus adding and subtracting signed decimals. Representing plays a small supporting role by showing which way to go and that the answer must be negative.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:

- **The problem is a pure procedure.** It is already written in symbols, has no context, and asks for no explanation. To solve 12 + d = -4.8 you apply the inverse operation (subtract 12 from both sides) and then compute -4.8 - 12 = -16.8.
- **This is where students succeed or fail.** The usual wrong answers are 7.2, -7.2 and 16.8. All of them come from sign mistakes with negative decimals or from using the wrong operation, which are fluency errors. They don't come from misreading the problem.
- **The other practices only play small parts.** Representing (seeing that d must be negative) helps, but you can skip it and still get the right answer. Justifying by substituting the answer back is an optional check.

So if only one practice is chosen, **Procedural Fluency** is the main one this item tests. **Answer: d = -16.8**

---

## Row 135 (problem_id 48762)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A cube has side length of 10 inches. What is its volume?
____ cubic inches
```

### Answer 1: practices in order

**Problem:** A cube has side length of 10 inches. What is its volume? ____ cubic inches

**Answer:** 1,000 cubic inches

The NAEP mathematics framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. You asked me to add NRC Procedural Fluency as a sixth.

This is a direct, one-step item, so only a few practices are used. Here they are in order:

1. **Representing** (NAEP). The student turns the words into a mathematical object. They picture a cube whose length, width and height are all 10 inches. They also see that "volume" and "cubic inches" mean a three-dimensional measure, so the answer is a count of unit cubes. The task here is to recognize what the question is asking.

2. **Abstracting and Generalizing** (NAEP), a light role. The student recalls the general rule for a cube, V = s^3 (a special case of V = l × w × h), and applies it to this cube with s = 10. This is mostly recall of a known formula, so this practice plays only a small part.

3. **Procedural Fluency** (NRC). The student carries out the arithmetic correctly and efficiently: 10 × 10 × 10 = 10^3 = 1,000. A fluent student sees this at once by place value (each factor of 10 adds a zero) and does not confuse it with 3 × 10 = 30 or 10^2 = 100. They also give the answer in cubic inches, the correct unit. This is the main step where the answer is produced.

**Not needed:** Justifying and Proving (no argument is asked for), Mathematical Modeling (there is no real-world situation to simplify or interpret; the geometric setup is already given), and Collaborative Mathematical Discourse (this is a single-answer item done alone).

**Summary sequence:** Representing → Abstracting and Generalizing (light) → Procedural Fluency

Procedural Fluency is the main practice for this item. Representing is a necessary first step. The main ways to get it wrong are procedural: answering 30 (3 × 10) or 100 (10^2, the area of one face) instead of 1,000.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:

- **It is where the answer gets produced.** Once the student knows to use V = s^3, the item comes down to working out 10 × 10 × 10 = 1,000 correctly and giving the answer in cubic inches.
- **Representing takes very little here.** The cube and its side length are stated outright, and "cubic inches" already signals volume. Little interpretation or translation is needed, so Representing is a minimal entry step and not the main demand.
- **Typical errors are procedural.** Wrong answers like 30 (3 × 10) or 100 (10^2, the area of one face) come from applying the formula or the exponent incorrectly. They are not failures of modeling, representation or reasoning.
- **It is a routine, single-step item.** Recalling and correctly carrying out a standard formula is exactly what procedural fluency describes.

If you have to stay within the five NAEP practices, I would pick **Representing** as the next best choice. Even so, it plays only a small role in this item.

---

## Row 137 (problem_id 50865)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the equation.
1/5 = 2/3x
x = ____
If necessary, express your answer in fraction form.
```

### Answer 1: practices in order

**Problem:** Solve 1/5 = 2/3x. Give x, as a fraction if needed.

**Practices to draw from**
- NAEP 2026 Mathematics Framework practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics
- Added from the NRC strands of proficiency: Procedural Fluency

**Practices needed, in order**

1. **Representing (NAEP).** Read the symbols as an equation. "2/3x" means the coefficient 2/3 times the unknown x, so the problem is 1/5 = (2/3)·x. To get x alone you need the inverse of "multiply by 2/3," which is "multiply by 3/2." This translation step comes first. If you misread it as 2/(3x), you get a different answer.

2. **Procedural Fluency (NRC).** Do the algebra and fraction steps correctly and quickly:
   - Multiply both sides by 3/2: x = (1/5)·(3/2)
   - Multiply the fractions: x = 3/10, which is already in lowest terms

3. **Justifying and Proving (NAEP), a short final check.** Put the answer back in: (2/3)·(3/10) = 6/30 = 1/5. ✓ This confirms the answer, but it plays a small role here.

**Not used:** Abstracting and Generalizing, Mathematical Modeling, and Collaborative Mathematics. The task is a one-step linear equation with no real-world context, no pattern to generalize, and no group work.

**Main practices:** Representing → Procedural Fluency, with Procedural Fluency doing most of the work.

**Answer:** x = 3/10

(If the expression is read as 2/(3x), then 3x = 10 and x = 10/3. In this kind of item, the usual reading is (2/3)x.)

### Answer 2: major practice

**Main practice: Procedural Fluency (NRC)**

Here's why:
- The problem gives a ready-made equation with no context, so almost no translating or modeling is needed. The "Representing" step is just reading the notation as (2/3)·x.
- Most of the work, and most of the ways to go wrong, are in the procedure. You have to pick the inverse operation (multiply by 3/2, the reciprocal of 2/3), multiply the fractions (1/5 · 3/2 = 3/10), and check that the answer is in lowest terms.
- A student who misses this item usually slips on the fraction steps, for example multiplying by 2/3 instead of 3/2, or flipping the wrong fraction. Misreading what is being asked is a less likely cause.

**Answer:** x = 3/10

---

## Row 138 (problem_id 81261)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A roll of ribbon was 12 meters long. Diego cut 9 pieces of ribbon that were 0.4 meter each to tie some presents. He then used the remaining ribbon to make some wreaths. Each wreath required 0.6 meter.
How many meters of ribbon were available for making wreaths?
____ meters
```

### Answer 1: practices in order

**Answer: 8.4 meters**

**Practices to draw from**

The NAEP Mathematics Framework (2026) names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. You asked me to add **Procedural Fluency**, one of the NRC's strands of mathematical proficiency.

**Practices used, in order**

1. **Mathematical Modeling (formulating the model)**
   - Read the real-world situation and decide what the question asks for: the ribbon left *after* the gift pieces are cut.
   - Find the quantities that matter (12 m total, 9 pieces, 0.4 m each). Notice that the wreath information (0.6 m per wreath) doesn't affect this question. It looks like it sets up a follow-up question.

2. **Representing**
   - Turn the words into a math expression: remaining ribbon = 12 − 9 × 0.4.

3. **Procedural Fluency (NRC)**
   - Multiply the decimal: 9 × 0.4 = 3.6.
   - Subtract: 12 − 3.6 = 8.4.
   - This step needs correct decimal place value (writing 12 as 12.0 when subtracting) and the right order of operations.

4. **Mathematical Modeling (interpreting and validating)**
   - Put the result back into the story: 8.4 meters of ribbon are left for wreaths.
   - Check that it makes sense: it's less than 12 m and more than half of the roll, which fits cutting 3.6 m away.

**Practices not used:** Abstracting and Generalizing, Justifying and Proving, and Collaborative Mathematics. The item doesn't ask for a general pattern, an argument, or group work.

**Summary order:** Mathematical Modeling (formulate) → Representing → Procedural Fluency → Mathematical Modeling (interpret/validate)

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- **The modeling here is simple.** The story turns directly into 12 − 9 × 0.4. It's a familiar "total minus the pieces used" setup. The extra wreath information is a small distractor, but the question clearly asks only about what's left after cutting the gift pieces.
- **The real difficulty is the decimal arithmetic.** Students must:
  - multiply a whole number by a decimal: 9 × 0.4 = 3.6, not 36 or 0.36
  - subtract a decimal from a whole number: 12 − 3.6 = 8.4, which means lining up place values and writing 12 as 12.0
  - follow the right order: multiply first, then subtract
- **Most wrong answers would come from these steps.** Likely errors include misplacing the decimal point, misaligning digits when subtracting, or computing (12 − 9) × 0.4. Few would come from setting the problem up wrong.

**Runner-up:** Mathematical Modeling. It would become the major practice if the item asked the follow-up question (how many wreaths could be made, 8.4 ÷ 0.6 = 14). That version needs more reasoning about the situation, chaining the steps together, and interpreting the result.

---

## Row 141 (problem_id 54008)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Use any method to find the value for y that makes the equation true.
y = ____
```

### Answer 1: practices in order

**Note:** The problem text doesn't include the equation itself. It was probably an image that didn't come through. The analysis below assumes a typical one-variable linear equation in y, such as `3y + 5 = 20` or `2(y - 4) = 10`. If you share the equation, I can make this more specific.

**Practices available** (the five practices in the NAEP 2026 Mathematics Framework, plus the NRC strand you asked for):
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics
6. Procedural Fluency (NRC, *Adding It Up*)

**Practices needed, in order:**

1. **Representing.** Read the equation as a statement that two expressions are equal, with y as the unknown. Choose a way to work with it: a balance model, inverse operations, or guess-and-check. "Use any method" asks the student to pick a representation, so this comes first.

2. **Procedural Fluency (NRC).** This is the main step. Carry out the solving steps accurately and efficiently: distribute or combine like terms if needed, then undo operations in reverse order. Subtract or add constants on both sides, then divide or multiply to isolate y. Most of the difficulty is here, and most errors happen here too (sign mistakes, applying an operation to only one side).

3. **Justifying and Proving (light use).** Check the answer by substituting y back into the original equation to confirm both sides are equal. Inverse operations keep the equation balanced, and that is the justification for each step. The item doesn't ask for a written justification, so this practice plays a small role.

**Not needed:**
- **Mathematical Modeling.** There is no real-world context to turn into math.
- **Abstracting and Generalizing.** The student solves one specific equation and doesn't need to find a general pattern or rule.
- **Collaborative Mathematics.** This is an individual, short-answer item.

**Summary:** Representing → Procedural Fluency → Justifying and Proving (check). Procedural Fluency is the main practice.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- **The item is about doing the steps.** "Find the value for y that makes the equation true" asks the student to carry out a known procedure: undo the operations in order and keep both sides balanced. The answer is just a number.
- **Most success or failure comes from this practice.** Students can read the equation correctly and still get it wrong because of a sign error, a mistake in distributing, or applying an operation to only one side. That makes the item a test of executing the procedure accurately.
- **The other practices play a small role here.** Choosing a representation is simple, since the equation is given and the student just picks a method. Checking the answer by substitution is a good habit, but the item doesn't require it and doesn't score it.

**Caveat:** The equation didn't come through in the problem text. If it turns out to be unusual (for example, y appears on both sides in a form that calls for a strategic rearrangement, or the item mainly tests understanding of what "makes the equation true" means), Representing could matter more. For a typical linear equation, though, Procedural Fluency is the clear choice.

---

## Row 143 (problem_id 7369)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the difference.
13.2 − 1.78
____
```

### Answer 1: practices in order

**Answer: 13.2 − 1.78 = 11.42**

## Practices available

The 2026 NAEP Mathematics Framework lists these mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

You asked me to add a sixth:
6. **Procedural Fluency**, from the NRC's *Adding It Up* strands. It means carrying out procedures flexibly, accurately and efficiently.

## Practices needed, in order

This is a bare computation item. It has no context, no pattern and no claim to defend, so only two practices really apply.

**Step 1: Representing.** Rewrite the problem in a form the subtraction algorithm can use:
- Line the numbers up by place value, with the decimal points directly above each other.
- Write 13.2 as the equivalent **13.20**, so both numbers have digits to the hundredths place.

```
  13.20
−  1.78
```

Most errors on this item come from skipping this step. The usual one is right-aligning the digits, as if computing 132 − 178, or 13.2 − 17.8.

**Step 2: Procedural Fluency (NRC).** Run the column subtraction with regrouping:
- Hundredths: you can't take 8 from 0, so borrow from the tenths. That gives 10 − 8 = 2, and the tenths digit becomes 1.
- Tenths: you can't take 7 from 1, so borrow from the ones. That gives 11 − 7 = 4, and the ones digit becomes 2.
- Ones: 2 − 1 = 1.
- Tens: 1 − 0 = 1.
- Put the decimal point straight down in the answer: **11.42**.

Most of the item's difficulty is here: the student has to borrow twice in a row, across the decimal point.

**Optional quick check (still Procedural Fluency).** Estimate 13 − 2 ≈ 11, which agrees with 11.42. Or add back: 11.42 + 1.78 = 13.20. This is a routine check, not a formal argument, so it doesn't count as Justifying and Proving.

## Practices not needed

- **Abstracting and Generalizing**: the item asks for no pattern or general rule.
- **Justifying and Proving**: the item asks for no explanation or argument.
- **Mathematical Modeling**: there is no real-world situation to turn into math.
- **Collaborative Mathematics**: this is an individual computation.

**Summary order:** Representing (align place values, 13.2 → 13.20) → Procedural Fluency (subtract with two regroupings; optional estimate check). Procedural Fluency is the main practice.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Here's why:

- **The item asks for a computation and nothing else.** "Calculate the difference" asks only for the result of running an algorithm. It has no context to model, no representation to read or build, no pattern to generalize and no argument to make.
- **Most of the difficulty sits here.** The student has to borrow twice in a row: hundredths from tenths, then tenths from ones, across the decimal point. Then they have to put the decimal point in the right place in the answer. That is the accurate, efficient use of a procedure that Procedural Fluency describes.
- **Representing is only a setup step.** Lining up the decimal points and writing 13.2 as 13.20 matters, and it is the source of a common error. But it is a standard first step of the decimal subtraction procedure, so it's best seen as part of the procedure rather than a separate practice.

**In one line:** this item mainly tests Procedural Fluency. Representing is a minor supporting step.

---

## Row 146 (problem_id 8064)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the difference.
0.9 − 0.245
____
```

### Answer 1: practices in order

**Problem:** 0.9 − 0.245 = ?  **Answer: 0.655**

**Practices used.** These are the NAEP 2026 Mathematical Practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus NRC Procedural Fluency as you asked:

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Rewrites 0.9 as **0.900** so both numbers have three decimal places. This is the same value in a form that lines the digits up by place value (tenths, hundredths, thousandths), so it can be written as a vertical subtraction: 0.900 − 0.245. |
| 2 | **Procedural Fluency** (NRC) | Does the column subtraction with regrouping. 0 thousandths − 5 needs a borrow, so regroup 9 tenths into 8 tenths + 9 hundredths + 10 thousandths. Then 10 − 5 = 5, 9 − 4 = 5, 8 − 2 = 6, which gives **0.655**. |
| 3 (optional) | **Justifying and Proving** (light) | Checks the result: 0.655 + 0.245 = 0.900, or estimates 0.9 − 0.25 ≈ 0.65. This confirms the answer and the decimal-point placement. |

**Practices not needed:** Mathematical Modeling (there is no real-world context), Abstracting and Generalizing (it is one concrete calculation with no pattern or general rule), and Collaborative Mathematics (an individual item).

**Core sequence:** Representing → Procedural Fluency (→ an optional Justifying check).

The key step is Representing. The most common mistake on this item is lining up the digits on the right instead of at the decimal point. Another is treating 0.9 as "smaller" than 0.245 because 9 < 245. Writing 0.9 as 0.900 removes both mistakes before the procedure starts.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- **It's a bare calculation.** The item just says "Calculate the difference" and gives 0.9 − 0.245. It has no context, no pattern to generalize and no argument to make. What it tests is whether the student can carry out decimal subtraction correctly.
- **Most of the work is the procedure.** The student lines the numbers up at the decimal point and then subtracts with regrouping across places (borrowing from the tenths to cover the thousandths). That is the main source of difficulty, and it is a standard algorithm.
- **Representing helps, but it isn't the main practice.** Writing 0.9 as 0.900 matters, but it is a quick setup step. Fluent students often do it automatically as part of the decimal-subtraction procedure. Representing would be the main practice only if the item asked students to show the subtraction with a model, number line or grid, or to change between representations.

**Ranking:** Procedural Fluency (major) > Representing (supporting) > Justifying (optional check).

---

## Row 147 (problem_id 249867)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the sum vertically.
0.137 + 0.284.
____
```

### Answer 1: practices in order

**Problem:** Add 0.137 + 0.284 vertically.

**Answer:** 0.421

```
   0.137
 + 0.284
 -------
   0.421
```

## Practices available

The NAEP Mathematics Framework lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

I have added **Procedural Fluency** from the NRC's *Adding It Up* strands. It means carrying out procedures flexibly, accurately, and efficiently.

## Practices in the order they're used

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Rewrites the horizontal expression 0.137 + 0.284 in vertical (column) form. The decimal points and place values must line up: tenths over tenths, hundredths over hundredths, thousandths over thousandths. The problem asks for this step directly ("vertically"). |
| 2 | **Procedural Fluency (NRC)** | Runs the standard addition algorithm from right to left, carrying where needed: <br>- Thousandths: 7 + 4 = 11 → write 1, carry 1 <br>- Hundredths: 3 + 8 + 1 = 12 → write 2, carry 1 <br>- Tenths: 1 + 2 + 1 = 4 → write 4 <br>- Ones: 0 + 0 = 0 <br>- Bring the decimal point straight down → **0.421** |

**Main practice:** Procedural Fluency. Most of the work is carrying out the column-addition procedure correctly, including two carries. Representing is the setup step that comes first.

## Practices not needed

- **Abstracting and Generalizing:** no pattern or general rule has to be found.
- **Justifying and Proving:** the problem doesn't ask the student to explain or justify anything. A student might do a quick estimate (about 0.14 + 0.28 ≈ 0.42) to check the answer, but that is optional.
- **Mathematical Modeling:** there is no real-world situation to turn into math.
- **Collaborative Mathematics:** this is a task done alone.

**Final order:** Representing → Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:

- **It's where most of the work is.** Solving the problem mostly means carrying out the column-addition algorithm correctly. That includes two carries: thousandths 7 + 4 = 11 and hundredths 3 + 8 + 1 = 12. It also means bringing the decimal point straight down to get **0.421**.
- **It's where students usually go wrong.** Typical mistakes are procedural: forgetting a carry (which gives 0.411 or 0.311, for example) or putting the decimal point in the wrong place.
- **Representing only plays a small part here.** The numbers already have the same number of decimal places (three each), so lining them up vertically is simple. Representing would matter more if the place values were different, as in 0.137 + 2.8.

So Representing is a short setup step. The skill this problem mainly tests is **Procedural Fluency**: doing multi-digit decimal addition with regrouping accurately and efficiently.

---

## Row 148 (problem_id 278504)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A rectangular prism measures 7 1/2 cm by 12 cm by 15 1/2 cm.
Calculate the number of cubes with edge length 1/2 cm that fit in this prism.
____ cubes
```

### Answer 1: practices in order

## Practices to use (NAEP 2026 Mathematical Practices + NRC Procedural Fluency)

The NAEP 2026 framework lists five mathematical practices: **Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics**. I've added **Procedural Fluency** from the NRC strands, as you asked.

Three practices do the main work on this problem, with a fourth used to check the answer. Here is the order:

### 1. Representing (first)
Picture the prism filled with small cubes, stacked in rows, columns and layers. Because each edge is 1/2 cm, each centimeter of edge holds 2 cubes. This changes the problem from "volume with fractions" into "count the cubes along each edge, then multiply."

### 2. Abstracting and Generalizing (second)
Use the general rule: **cubes along an edge = edge length ÷ cube edge**, and **total cubes = product of the three counts**. This is the same as prism volume ÷ cube volume. Seeing that "how many fit" means division by the unit cube, using the same structure as V = l × w × h, is the key abstraction.

### 3. Procedural Fluency (NRC) (third)
Do the fraction and whole-number arithmetic correctly and efficiently:
- 7 1/2 ÷ 1/2 = 15/2 × 2 = **15**
- 12 ÷ 1/2 = **24**
- 15 1/2 ÷ 1/2 = 31/2 × 2 = **31**
- 15 × 24 × 31 = 360 × 31 = **11,160**

### 4. Justifying and Proving (last, lighter role)
Check the answer another way. Prism volume = 15/2 × 12 × 31/2 = 5580/4 = 1395 cm³. One cube's volume = 1/8 cm³. 1395 ÷ 1/8 = 1395 × 8 = 11,160. ✔ Each dimension divides evenly by 1/2, so whole cubes fill the prism with no gaps or leftover space. That justifies counting exactly rather than rounding down.

**Not used:** Mathematical Modeling (the problem is already purely mathematical, with no real-world situation to model) and Collaborative Mathematics (this is a solo task).

### Summary order
**Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving**

**Answer: 11,160 cubes**

### Answer 2: major practice

## Major practice: **Procedural Fluency (NRC)**

Here's why:

- **The problem says "Calculate."** The setup is a standard, familiar one: find how many unit cubes fill a prism. The method (divide each edge by 1/2, then multiply, or divide the volume by 1/8) is a routine grade 5–6 procedure. It doesn't take much representing or abstracting to see it.
- **Most of the work, and most of the errors, are in the computation.** Students have to:
  - turn mixed numbers into fractions (7 1/2 = 15/2, 15 1/2 = 31/2),
  - divide by a fraction correctly (÷ 1/2 means × 2, not ÷ 2),
  - multiply multi-digit numbers accurately (15 × 24 × 31 = 11,160, or 1395 × 8).
  
  A student who understands the idea can still miss the answer by halving instead of doubling, mishandling a mixed number, or making a multiplication slip.
- **The other practices play a smaller role.** Representing and Abstracting/Generalizing are needed only briefly, to pick the method. Justifying is an optional check.

**Runner-up:** Abstracting and Generalizing. Seeing that "how many cubes fit" means dividing by the unit cube's edge or volume is the one conceptual step. Students who miss it may just report the volume (1395) as the answer. Still, that step is quick for most students compared with the arithmetic, so Procedural Fluency is the major practice.

---

## Row 149 (problem_id 278648)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A rectangular prism measures 7 1/2 cm by 12 cm by 15 1/2 cm.
What is the volume of the prism in cm^3? If you are stuck, think about how many cubes with 1/2 -cm edge lengths fit into 1 cm^3.
____ cm^3
```

### Answer 1: practices in order

## Practices available

The NAEP 2026 Mathematics Framework names five mathematical practices. I've added Procedural Fluency from the NRC's *Adding It Up*:

| # | Practice | Source |
|---|----------|--------|
| P1 | Representing | NAEP |
| P2 | Abstracting and Generalizing | NAEP |
| P3 | Justifying and Proving | NAEP |
| P4 | Mathematical Modeling | NAEP |
| P5 | Collaborative Mathematics | NAEP |
| P6 | Procedural Fluency | NRC |

## Practices needed, in order

**1. Representing (P1)**
Read the problem as a rectangular prism with edges 7 1/2 cm, 12 cm and 15 1/2 cm, and picture the volume as unit cubes filling it. The hint asks the student to switch to a new unit, the 1/2-cm cube. Seeing that one 1 cm³ cube holds 2 x 2 x 2 = 8 of these small cubes is a change of representation.

**2. Abstracting and Generalizing (P2)**
The student must see that V = l x w x h, which they learned by counting whole cubes, still works when the edges are fractions. With the hint, the student builds that argument. In half-cm units every edge is a whole number: 15, 24 and 31 half-cm. So the whole-number cube-counting idea carries over, and the result is scaled by 1/8.

**3. Procedural Fluency (P6, NRC)**
Do the arithmetic accurately and efficiently:
- Direct route: 7.5 x 12 = 90, then 90 x 15.5 = 1,395.
- Hint route: 15 x 24 x 31 = 11,160 half-cm cubes, then 11,160 / 8 = 1,395.
Changing mixed numbers to decimals or improper fractions (15/2, 31/2) and multiplying in a smart order (7.5 x 12 first) are both part of fluency here.

**4. Justifying and Proving (P3)** (light, optional)
Check that the answer makes sense: the two routes agree, and 1,395 falls between 7 x 12 x 15 = 1,260 and 8 x 12 x 16 = 1,536. The units are cm³. The item does not ask for a written argument, so this is only a self-check.

## Practices not used
- **Mathematical Modeling (P4):** there is no real-world situation to turn into math. The problem is already given in math terms.
- **Collaborative Mathematics (P5):** this is a single-student item with no shared work.

## Summary
**Representing -> Abstracting and Generalizing -> Procedural Fluency -> (Justifying and Proving)**

**Answer: 1,395 cm³**

### Answer 2: major practice

## Major practice: Procedural Fluency (NRC)

If I had to pick one, I would pick **Procedural Fluency**.

**Why**
- The item asks only for a number (____ cm³). There is no explanation, model or representation to produce.
- Most students at this level already know V = l x w x h. For them, the real work is multiplying 7 1/2 x 12 x 15 1/2 correctly. That means changing mixed numbers to decimals or improper fractions, multiplying in a smart order (7.5 x 12 = 90, then 90 x 15.5 = 1,395), and not dropping the fractional parts.
- Computation is where most wrong answers would come from. Typical mistakes are multiplying only the whole-number parts (7 x 12 x 15 = 1,260) or handling the halves badly. So fluency is what most separates students who get it right from those who don't.

**Runner-up: Abstracting and Generalizing**
The hint about 1/2-cm cubes is there to help students who don't yet trust that V = l x w x h works for fractional edges (CCSS 6.G.A.2). For those students, the key step is extending the whole-number cube-counting idea to fractions, so Abstracting and Generalizing would be the main practice. But the hint is optional ("If you are stuck"). The core task is still the calculation, so Procedural Fluency stays the main one.

**Answer: 1,395 cm³**

---

## Row 150 (problem_id 58258)

- **predicted_practice:** Abstracting and Generalizing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
2^12 = 4096. How many other whole numbers can you raise to a power and get 4,096?
____
```

### Answer 1: practices in order

**Problem:** 2^12 = 4096. How many other whole numbers can you raise to a power and get 4,096?

**Answer:** 4. The bases are 4, 8, 16 and 64:
- 4^6 = 4096
- 8^4 = 4096
- 16^3 = 4096
- 64^2 = 4096

If you also count the trivial 4096^1, the answer is 5. Most versions of this item expect 4, because they mean a non-trivial power.

---

### Practices used, in order

The NAEP mathematics framework lists these mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Procedural Fluency from the NRC's *Adding It Up* strands is added below, as you asked.

**1. Representing**
First, write 4096 in a form that shows its structure: its prime factorization, 4096 = 2^12. Any base that works must itself be a power of 2, written as 2^k. Then (2^k)^m = 2^(km), so we need km = 12. This turns a guess-and-check search into a question about the exponents.

**2. Abstracting and Generalizing**
Next, see the general rule. b^m = 4096 has a whole-number solution exactly when b = 2^k and k divides 12. The divisors of 12 are 1, 2, 3, 4, 6 and 12, which give one candidate base for each divisor. The problem asks for "other" whole numbers, so drop k = 1 (base 2). If you treat exponent 1 as trivial, drop k = 12 (base 4096) as well.

**3. Procedural Fluency (NRC)**
Then do the calculations correctly and quickly. Work out the bases: 2^2 = 4, 2^3 = 8, 2^4 = 16, 2^6 = 64 (and 2^12 = 4096). Work out the matching exponents: 12/2 = 6, 12/3 = 4, 12/4 = 3, 12/6 = 2. Check a couple of them, for example 16^3 = 256 × 16 = 4096 and 64^2 = 4096. This step relies on the laws of exponents and quick multiplication.

**4. Justifying and Proving**
Finally, argue that the list is complete. Prime factorization is unique, so no base that contains another prime factor (3, 5, 6, 10, ...) can give 4096. Every power-of-2 base corresponds to a divisor of 12, so the four bases (five, counting 4096^1) are all there is.

**Not really used:** Mathematical Modeling (there is no real-world situation to model) and Collaborative Mathematics (this is a task done alone).

**Summary order:** Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

This is the step that actually solves the problem. Writing 4096 = 2^12 is given in the question, so Representing takes little effort. The real work is seeing the general rule: b^m = 4096 only when b = 2^k and k divides 12. With that rule, the question becomes "count the divisors of 12, other than the trivial ones." A student who misses this ends up guessing bases one by one and can easily skip one (such as 8 or 64) or not know when to stop.

The other practices play a supporting role:
- **Representing** sets up the structure, but most of it is handed to the student.
- **Procedural Fluency** is just checking a few powers (4^6, 8^4, 16^3, 64^2), which is routine arithmetic.
- **Justifying and Proving** (showing the list is complete) is needed for a full argument. But a fill-in-the-blank item only asks for the count.

So if I had to pick one, it would be **Abstracting and Generalizing**.

---

## Row 152 (problem_id 60862)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of the expression below.
(-22)(-5)
____
```

### Answer 1: practices in order

**Problem:** Find the value of (-22)(-5).

**Answer:** 110

---

### Practices available

The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Problem Solving

Added from the NRC's *Adding It Up* strands:
6. **Procedural Fluency**: carrying out procedures flexibly, accurately, and efficiently.

### Practices needed, in order

**1. Representing (minor, first)**
The student has to read the notation correctly. Two parenthesized numbers written side by side, (-22)(-5), with no operator between them mean multiplication. The parentheses also show that each minus sign belongs to its number. This is not subtraction. Turning the symbols into "multiply negative 22 by negative 5" is a small act of interpreting a representation. For most students at this level it is quick and nearly automatic.

**2. Procedural Fluency (primary)**
This is where the work happens. The student:
- applies the sign rule for multiplying integers: negative × negative = positive
- multiplies the absolute values: 22 × 5 = 110 (for example, 20 × 5 + 2 × 5 = 100 + 10)
- puts the two together to get **+110**

The task tests whether the student can run a known procedure accurately. The usual mistakes are procedural: giving −110 by misapplying the sign rule, or treating the expression as subtraction or addition.

### Practices not needed
- **Abstracting and Generalizing:** The student only *uses* the rule that a negative times a negative is positive. They do not have to derive or generalize it.
- **Justifying and Proving:** No explanation or argument is asked for.
- **Mathematical Modeling:** There is no real-world context to model.
- **Collaborative Problem Solving:** This is an individual item.

### Summary

| Order | Practice | Role |
|---|---|---|
| 1 | Representing | Minor: read (a)(b) as multiplication of two negative integers |
| 2 | Procedural Fluency (NRC) | Primary: apply the integer sign rule and compute 22 × 5 = 110 |

**Final answer: 110**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item asks for one thing: compute (-22)(-5). To get it right, the student has to:
- apply the integer sign rule (negative × negative = positive)
- multiply 22 × 5 = 110 accurately

Both steps carry out a known procedure. Neither calls for interpreting a new representation, generalizing, justifying, or modeling.

The likely mistakes are also procedural. A student who writes −110 has misapplied the sign rule. A student who adds or subtracts the numbers has run the wrong operation.

Reading (a)(b) as multiplication does involve Representing, but it is a quick first step and not where the item's difficulty lies.

**Answer: 110**

---

## Row 153 (problem_id 9017)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the sum.
1.075 + 27.105
____
```

### Answer 1: practices in order

**Problem:** Calculate the sum 1.075 + 27.105

**Practices available**
- NAEP 2026 Mathematical Practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics
- NRC strand you added: Procedural Fluency

**Practices needed, in order**

1. **Representing (NAEP).** Set the sum up vertically so the decimal points line up and each digit sits in its place-value column (ones, tenths, hundredths, thousandths). Both numbers already go to the thousandths place, so you don't need to pad with zeros.
   ```
      1.075
   + 27.105
   --------
   ```
   This step matters. The most common error on decimal addition is misaligning the digits, which is a representation error and not an arithmetic one.

2. **Procedural Fluency (NRC).** Run the standard column-addition algorithm from right to left and carry where needed:
   - Thousandths: 5 + 5 = 10, write 0, carry 1
   - Hundredths: 7 + 0 + 1 = 8
   - Tenths: 0 + 1 = 1
   - Ones: 1 + 7 = 8
   - Tens: 0 + 2 = 2
   - Result: **28.180 = 28.18**

   This is the core of the problem. The task is almost entirely a test of carrying out the algorithm accurately.

3. **Justifying (NAEP, optional and light).** A quick estimation check: about 1 + 27 = 28, so 28.18 is reasonable. This is a sanity check, not a formal proof. Most students skip it, and the problem doesn't require it.

**Not needed:** Abstracting and Generalizing, Mathematical Modeling, and Collaborative Mathematics. There's no pattern to generalize, no real-world context to model, and no collaboration.

**Summary:** Representing, then Procedural Fluency (with an optional Justifying check). Procedural Fluency is the main practice. Representing is a short setup step that comes before it.

**Answer: 28.18**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- The problem is a bare computation, "Calculate the sum," with no context, no pattern and nothing to explain. Getting it right depends almost entirely on carrying out decimal column addition correctly, including the carry from the thousandths place (5 + 5 = 10).
- Representing (lining up the decimal points) is a real step, but it's small here. Both numbers already have three decimal places, so they line up naturally and there's little room for a place-value mistake.
- Justifying (the estimation check) is optional, and the problem doesn't ask for it.

So if a student gets this item wrong, the most likely cause is a slip in the algorithm, such as a dropped carry. That makes Procedural Fluency the practice this item mainly measures.

**Answer: 28.18**

---

## Row 154 (problem_id 61160)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of the expression below.
-22 ÷ 5
____
```

### Answer 1: practices in order

## Practices for: Find the value of -22 ÷ 5

**Answer:** -22 ÷ 5 = **-4.4** (or -4 2/5, or -22/5)

### Available practices

The NAEP Mathematics Framework (2026) names five mathematical practices:

1. **Representing**: moving between and working with different forms of a number (fraction, mixed number, decimal, symbol).
2. **Abstracting and Generalizing**: noticing structure and applying general rules.
3. **Justifying and Proving**: giving reasons why a result holds.
4. **Mathematical Modeling**: turning a real-world situation into math and reading the result back.
5. **Collaborative Mathematics**: working on math together with others.

You asked me to add one more:

6. **Procedural Fluency (NRC, *Adding It Up*)**: carrying out procedures flexibly, accurately, and efficiently.

### Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Abstracting and Generalizing** (small role) | Uses the sign rule for division: a negative divided by a positive is negative. So the answer is −(22 ÷ 5). |
| 2 | **Procedural Fluency** (main practice) | Does the division: 22 ÷ 5 = 4 remainder 2, so 4 2/5. As a decimal, 2/5 = 0.4, which gives 4.4. Then attaches the sign: −4.4. |
| 3 | **Representing** (small role) | Writes the result in the form the blank expects: −4.4, −4 2/5, or −22/5. These are all the same value. Converting the remainder 2/5 to 0.4 is also a representation step. |

### Practices not used

- **Mathematical Modeling**: there is no real-world context.
- **Justifying and Proving**: the student only gives a value, not an explanation.
- **Collaborative Mathematics**: this is an individual item.

### Summary

**Abstracting and Generalizing (sign rule) → Procedural Fluency (dividing 22 by 5) → Representing (writing −4.4 or −4 2/5)**

Procedural Fluency carries most of the work. This is a one-step computation. The main ways students get it wrong are procedural: losing the negative sign, or writing the remainder as ".2" (giving −4.2) instead of 2/5 = 0.4.

### Answer 2: major practice

## Major practice: **Procedural Fluency** (NRC)

-22 ÷ 5 is a bare computation, so the work is mostly procedural:

- **Division:** 22 ÷ 5 = 4 remainder 2, and the remainder means 2/5 = 0.4.
- **Sign rule:** a negative divided by a positive gives a negative result, so the answer is **−4.4** (or −4 2/5).

The other practices play only small roles. Using the sign rule is routine recall. It isn't real abstracting or generalizing. Writing the result as a decimal or mixed number is a small representing step. The item has no context to model, asks for no justification, and involves no collaboration.

The likely errors are also procedural: dropping the negative sign, or writing the remainder 2 as ".2" to get −4.2. That points the same way. Whether a student gets this item right depends on Procedural Fluency.

---

## Row 156 (problem_id 8869)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the sum.
33.1 + 1.95
____
```

### Answer 1: practices in order

**Problem:** Calculate the sum 33.1 + 1.95

This is a one-step computation. The NAEP mathematical practices are Representing, Abstracting, Reasoning, Generalizing, Justifying, and Modeling. Very few of them really apply here. Most of the work is **procedural fluency** (NRC), with a little help from NAEP practices at the start and end.

### Practices in order

1. **Representing (NAEP).** Rewrite the horizontal sum as a vertical addition with the decimal points lined up. Use place value to pad 33.1 to 33.10, so both numbers have digits in the tenths and hundredths places:
   ```
     33.10
   +  1.95
   -------
   ```
   This is the step where students most often go wrong. A common mistake is lining up the last digits and getting 33.1 + 1.95 = 5.26.

2. **Procedural fluency (NRC).** Do the standard addition algorithm column by column, from right to left, regrouping as needed:
   - Hundredths: 0 + 5 = 5
   - Tenths: 1 + 9 = 10, so write 0 and carry 1
   - Ones: 3 + 1 + 1 = 5
   - Tens: 3
   - Bring the decimal point straight down.

   Result: **35.05**

3. **Reasoning (NAEP), as a quick check.** Estimate to confirm the answer makes sense: 33 + 2 = 35, so 35.05 is reasonable. A result like 5.26 or 352.6 would fail this check.

### Summary

| Order | Practice | Role |
|---|---|---|
| 1 | Representing (NAEP) | Line up the numbers by place value (33.10 + 1.95) |
| 2 | Procedural fluency (NRC) | Add the columns with regrouping (main step) |
| 3 | Reasoning (NAEP) | Check the answer by estimation (about 35) |

**Answer:** 33.1 + 1.95 = **35.05**

Procedural fluency is the main practice here. Abstracting, Generalizing, Justifying, and Modeling are not needed for this problem.

### Answer 2: major practice

**Major practice: Procedural fluency (NRC)**

The problem only asks for a sum: 33.1 + 1.95 = 35.05. Almost all of the work is running the standard decimal addition algorithm correctly and efficiently. That means lining up the decimal points, adding column by column, and carrying from the tenths to the ones.

The NAEP practices play smaller roles. Representing is only the setup step (writing 33.1 as 33.10 and lining up the decimal points). Reasoning is an optional estimation check (about 33 + 2 = 35). There is nothing to model, generalize, or justify. So procedural fluency is the one practice that decides whether a student gets the problem right.

---

## Row 157 (problem_id 7710)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the difference.
23.11 − 0.376
____
```

### Answer 1: practices in order

**Answer:** 23.11 − 0.376 = **22.734**

**Practices available:** the five NAEP mathematical practices (2026 framework): Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Added to these is **Procedural Fluency** from the NRC (*Adding It Up*).

This is a bare computation item, so it needs only two practices. Neither is a major reasoning step.

### Order of practices

**1. Representing** (setup)
- Write the problem vertically with the decimal points lined up, so each digit sits in its correct place-value column (ones, tenths, hundredths, thousandths).
- Rewrite 23.11 as **23.110**, adding a placeholder zero so both numbers have three decimal places.

```
  23.110
-  0.376
--------
```

The usual mistake here is lining up the digits from the right (putting the 6 under the 1 in 23.11). This step is what prevents it.

**2. Procedural Fluency (NRC)** (the main step)
Run the standard subtraction algorithm with regrouping:
- Thousandths: 0 − 6 can't be done, so borrow from the hundredths: 10 − 6 = **4**
- Hundredths: (1 − 1) = 0, and 0 − 7 can't be done, so borrow from the tenths: 10 − 7 = **3**
- Tenths: (1 − 1) = 0, and 0 − 3 can't be done, so borrow from the ones: 10 − 3 = **7**
- Ones: (3 − 1) − 0 = **2**
- Tens: 2 − 0 = **2**
- Bring down the decimal point: **22.734**

A quick estimate (23.11 − 0.4 ≈ 22.7) confirms the answer is reasonable. This check is part of fluent procedure use, not a separate practice.

### Practices not needed
- **Abstracting and Generalizing:** there is no pattern or general rule to find.
- **Justifying and Proving:** the item asks for no explanation or argument.
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** this is an individual computation item.

**Summary sequence:** Representing (align place values, add the placeholder zero) → Procedural Fluency (subtract with regrouping across three places) → 22.734

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- **The item is a bare computation.** "Calculate the difference" has no context, no explanation to give, and no pattern to find. What it measures is whether the student can carry out decimal subtraction correctly.
- **Most of the difficulty is in the procedure.** The student has to regroup across three places in a row (thousandths, hundredths, tenths), borrowing from places that have already been reduced. Most errors on this item will come from mistakes in that borrowing chain.
- **Representing comes before it but is smaller.** Lining up the decimal points and writing 23.11 as 23.110 is a necessary setup step, and it is where the classic misalignment error happens. But it takes one quick move and only supports the procedure. In standard decimal-subtraction instruction, this alignment is usually taught as the first step of the algorithm itself.

So **Procedural Fluency** is the major practice. **Representing** is a minor supporting practice that comes first.

---

## Row 158 (problem_id 64354)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the equation to find their starting altitude.
____ feet
```

### Answer 1: practices in order

**Note on the problem:** The text given is only the last step of a multi-part item: "Solve the equation to find their starting altitude. ____ feet." The equation itself, and the story behind it, came from an earlier part that isn't shown. So I'm assuming the usual setup for this kind of item: a linear equation such as `a + r·t = final altitude` (or `a − r·t = …`), where `a` is the unknown starting altitude, `r` is a rate of climb or descent, and `t` is time.

**Practices used:** the five NAEP mathematical practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus NRC Procedural Fluency.

### Practices in order

1. **Representing (NAEP)**
   - Read the equation as a description of the situation: the variable is the starting altitude, the rate × time term is the change in altitude, and the constant is the final altitude.
   - Watch the signs: going down subtracts, going up adds.
   - This step links the symbols to the context, so you know which value you're solving for.

2. **Procedural Fluency (NRC)**
   - This is the main practice for this problem. Solve the linear equation correctly and efficiently with inverse operations.
   - Simplify any product first (for example, compute `r·t`).
   - Then add or subtract that amount on both sides to isolate the starting altitude.
   - Work accurately with signed numbers, especially for a descent or negative rates.

3. **Mathematical Modeling (NAEP), the interpret/validate step**
   - Read the number back into the situation as an altitude in feet.
   - Check that it makes sense. For example, for a descent the starting altitude should be higher than the final altitude.
   - Optionally, put the value back into the equation or the story to confirm it.

### Practices not needed
- **Abstracting and Generalizing:** you aren't asked to find a general pattern or rule.
- **Justifying and Proving:** you aren't asked to give an argument or explanation.
- **Collaborative Mathematics:** this is an individual, single-answer item.

**Summary order:** Representing → Procedural Fluency → Mathematical Modeling (interpret/check). Procedural Fluency is the main practice here.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The problem says "Solve the equation." It doesn't ask students to build the equation, so the modeling and representing work happened in an earlier part. What's left here is carrying out a procedure correctly:
- simplify any rate × time term
- use inverse operations to isolate the starting altitude
- handle the signs accurately

Representing and the interpret/check step from Modeling are still involved, but only in small ways: you match the variable to "starting altitude" and write the answer in feet. Whether a student gets this right or wrong depends mostly on whether they can solve the linear equation accurately, and that is Procedural Fluency.

---

## Row 159 (problem_id 65369)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the product.
(-0.2) • (-0.3)
____
```

### Answer 1: practices in order

**Problem:** Find the product (-0.2) • (-0.3)
**Answer:** 0.06

The NAEP 2026 Mathematics Framework lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added Procedural Fluency from the NRC's *Adding It Up* strands.

This is a short computation with no context, so only some of the practices apply.

### Practices, in the order you'd use them

**1. Representing**
- Read the notation correctly: "•" means multiply, and the parentheses show that each factor is negative.
- Read -0.2 as "negative two tenths" and -0.3 as "negative three tenths." This sets up both the sign question and the decimal question.

**2. Abstracting and Generalizing**
- Apply the general sign rule: a negative times a negative is positive. So the product is positive.
- Treat the problem as two separate parts: the sign, then the size of the answer, which is 0.2 × 0.3.

**3. Procedural Fluency (NRC)** *(the main practice for this problem)*
- Multiply the digits as whole numbers: 2 × 3 = 6.
- Place the decimal point. Each factor has one decimal place, so the product has 1 + 1 = 2 decimal places. That gives 0.06, not 0.6.
- Attach the sign from step 2: +0.06.

**4. Justifying and Proving** *(light, as a check)*
- Check that the size makes sense. A tenth of a tenth is a hundredth, so (2 tenths) × (3 tenths) = 6 hundredths = 0.06.
- Or check with fractions: (-2/10)(-3/10) = 6/100 = 0.06.

### Not used
- **Mathematical Modeling:** there is no real-world situation to model.
- **Collaborative Mathematics:** this is a solo task with nothing to communicate or critique.

### Summary of the order
Representing → Abstracting and Generalizing (sign rule) → **Procedural Fluency** (multiply and place the decimal) → Justifying and Proving (reasonableness check)

**Main practice:** Procedural Fluency. The most common mistakes on this item are procedural ones: writing 0.6 instead of 0.06, or giving the answer a negative sign.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The problem is a bare calculation, (-0.2) • (-0.3) = 0.06. There is no context to model, no claim to justify, and no choice of representation to make.
- Nearly all the work is carrying out a known procedure correctly and quickly: multiply 2 × 3, count the decimal places (1 + 1 = 2) to get 0.06, and apply the sign rule (negative × negative = positive).
- Students mostly get this item wrong through procedural slips: writing 0.6 instead of 0.06, or giving a negative answer. These are fluency errors, not conceptual or reasoning errors.

The other practices play small supporting roles. Representing covers reading the notation, Abstracting and Generalizing covers recalling the sign rule, and Justifying covers the optional reasonableness check. Procedural Fluency is the one the problem actually measures.

---

## Row 160 (problem_id 64054)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the equation.
3a = 12
a = ____
```

### Answer 1: practices in order

**Problem:** Solve the equation 3a = 12. a = ____

**Answer:** a = 4

## Practices available

The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

You asked me to add one more, from the NRC's *Adding It Up* strands of proficiency:
6. Procedural Fluency

## Which practices this problem uses, in order

**1. Representing (light use)**
The student has to read the symbols correctly. "3a" means 3 times a, and the equals sign means both sides have the same value. In words: "what number times 3 gives 12?" The representation is already given, so the student only has to interpret it, not build it.

**2. Procedural Fluency (main practice)**
The student uses the standard step for solving a one-step equation: undo multiplication by dividing both sides by 3.
- 3a / 3 = 12 / 3
- a = 4

A student who knows the basic fact 3 x 4 = 12 can also find the answer straight away from fact recall. Either way, the work is a routine procedure done accurately and efficiently, and that is the core of procedural fluency.

**3. Justifying and Proving (optional, light)**
A careful student checks the answer by putting it back in: 3 x 4 = 12, which is true. This is a small piece of informal justification. It confirms the answer but the problem does not ask for it.

## Practices not used
- **Abstracting and Generalizing:** no pattern or general rule is required. The student solves one specific equation.
- **Mathematical Modeling:** there is no real-world situation to turn into math, because the equation is given directly.
- **Collaborative Mathematics:** this is a task done alone.

## Summary

| Order | Practice | Role |
|---|---|---|
| 1 | Representing | Read 3a = 12 as "3 times a number equals 12" |
| 2 | **Procedural Fluency** | Divide both sides by 3 (or recall 3 x 4 = 12) to get a = 4 (**dominant**) |
| 3 | Justifying and Proving | Optional check: 3 x 4 = 12 |

Procedural Fluency is the main practice in this problem. Representing plays a small supporting role before it, and the check afterwards is optional.

### Answer 2: major practice

**Major practice: Procedural Fluency**

All the real work in 3a = 12 is one routine step: divide both sides by 3, or recall the fact 3 x 4 = 12, to get a = 4. That is a standard procedure done accurately and efficiently, which is exactly what procedural fluency means.

The other practices play only small roles:
- **Representing:** the student just reads an equation that is already written in symbols. Nothing has to be translated or built.
- **Justifying:** the substitution check (3 x 4 = 12) is optional, and the problem does not ask for it.

If the student can't carry out the procedure, they can't solve the problem. If they can, the problem is basically done. So Procedural Fluency is the one to pick.

---

## Row 162 (problem_id 403777)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the product.
(0.64) ⋅ (0.81)
____
```

### Answer 1: practices in order

**Problem:** Find the product (0.64) · (0.81)

**Answer:** 0.64 × 0.81 = **0.5184**

---

### Practices available
NAEP 2026 Mathematics Framework practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, (5) Collaborative Mathematics. Added from NRC *Adding It Up*: **Procedural Fluency**.

### Practices needed, in order

**1. Procedural Fluency (NRC): the main practice, used throughout**
This is a bare computation with no context, so most of the work is carrying out the standard decimal multiplication algorithm accurately and efficiently:
- Ignore the decimal points and multiply the whole numbers: 64 × 81 = 64 × 80 + 64 × 1 = 5120 + 64 = 5184.
- Count the decimal places: 0.64 has 2 and 0.81 has 2, so the product has 2 + 2 = 4.
- Place the decimal point: 0.5184.

**2. Representing (NAEP): small, supporting role**
The student may switch representations to make the step easier or to see why the decimal rule works, for example rewriting the decimals as fractions, 64/100 × 81/100 = 5184/10000 = 0.5184. Many students skip this and just apply the rule mechanically, so it is optional.

**3. Justifying and Proving (NAEP): light, optional check at the end**
A quick reasonableness check: both factors are less than 1, so the product must be smaller than each factor. Estimating 0.6 × 0.8 = 0.48 confirms that 0.5184 is about the right size and that the decimal point is in the right place. This is a sense-making check, not a formal proof.

### Practices not needed
- **Mathematical Modeling:** there is no real-world situation to turn into math.
- **Abstracting and Generalizing:** no pattern or general rule has to be found. The student applies a known rule rather than deriving one.
- **Collaborative Mathematics:** this is an individual computation.

### Summary order
**Procedural Fluency → (optional) Representing → (optional) Justifying/estimating check**

Procedural Fluency is by far the dominant practice for this item.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- The item is a bare computation, (0.64) · (0.81). There is no context to model, no pattern to generalize, and nothing to justify.
- Solving it comes down to running the standard decimal multiplication procedure correctly: multiply 64 × 81 = 5184, count the 4 decimal places, and write 0.5184.
- Most errors on this item are procedural ones, such as putting the decimal point in the wrong place (writing 5.184 or 51.84) or making an arithmetic slip in 64 × 81. Those are failures of procedural fluency, not of any NAEP practice.

Representing and Justifying (the estimation check) can support the work, but they are optional. Procedural Fluency is the one practice the problem actually requires.

---

## Row 164 (problem_id 70629)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the difference.
2.1 − 0.4
____
```

### Answer 1: practices in order

**Problem:** Find the difference. 2.1 − 0.4

**Answer:** 1.7

The NAEP mathematical practices are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Procedural Fluency comes from the NRC strands. This is a bare computation, so it doesn't need many practices. Here is the order I'd use them in:

**1. Representing (NAEP), a light, supporting role**
- Line up the decimals by place value (ones and tenths):
  ```
    2.1
  − 0.4
  -----
  ```
- You can also think of it as 21 tenths − 4 tenths, or picture it on a number line. Either way, the problem now has a form you can compute with.

**2. Procedural Fluency (NRC), the main practice**
- Do the subtraction accurately and efficiently:
  - Tenths: 1 − 4 won't work, so regroup 1 one into 10 tenths. That gives 11 − 4 = 7 tenths.
  - Ones: 2 − 1 (after regrouping) − 0 = 1.
  - Result: **1.7**
- Another way: 21 tenths − 4 tenths = 17 tenths = 1.7.

**3. Justifying (NAEP Justifying and Proving), optional, for checking**
- Check by addition: 1.7 + 0.4 = 2.1 ✓
- Estimate: 2 − 0.5 ≈ 1.5, which is close to 1.7. The answer is reasonable.

**Practices not needed:** Mathematical Modeling (there's no real-world situation), Abstracting and Generalizing (you don't need a general pattern), and Collaborative Mathematics.

**Summary of order:** Representing (place-value alignment) → **Procedural Fluency** (regroup and subtract, the main one) → Justifying (inverse-operation check). Procedural Fluency carries most of this problem.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The problem is "2.1 − 0.4", a bare computation. It has no context to model, nothing to generalize, and it doesn't ask for a justification.
- Solving it comes down to carrying out decimal subtraction correctly. The key step is regrouping 1 one into 10 tenths, so 11 tenths − 4 tenths = 7 tenths, which gives **1.7**.
- Representing (lining up the place values) and Justifying (checking with 1.7 + 0.4 = 2.1) help, but they're minor. The usual mistake on this item is a procedural one, such as writing 2.3 because the student subtracted 1 from 4 instead of regrouping. That is a fluency error, not a representation or reasoning error.

So if I had to pick one, it's **Procedural Fluency**.

---

## Row 165 (problem_id 70299)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the difference.
0.3 − 0.05
____
```

### Answer 1: practices in order

**Problem:** Find the difference. 0.3 − 0.05

**Practices available** (2026 NAEP Mathematics Framework, plus one from the NRC):
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics
6. Procedural Fluency (NRC, *Adding It Up*)

**Practices to use, in order:**

**Step 1: Representing.** The two numbers don't have the same number of decimal places, and that is where students usually go wrong (a common error answer is 0.02, from doing "5 − 3"). First rewrite 0.3 as the equivalent decimal 0.30 (3 tenths = 30 hundredths). Then line the numbers up by place value:
```
  0.30
− 0.05
```
This is the key step in the problem. You change the representation so both numbers are in hundredths, and then the subtraction is easy.

**Step 2: Procedural Fluency.** Run the standard subtraction algorithm. In the hundredths column, 0 − 5 needs regrouping: borrow 1 tenth, so you have 10 hundredths, and 10 − 5 = 5. The tenths column is now 2 − 0 = 2. Result: **0.25**. (Or in place-value terms: 30 hundredths − 5 hundredths = 25 hundredths.)

**Step 3 (optional, light): Justifying.** Check the answer by adding back: 0.25 + 0.05 = 0.30 = 0.3. This is a quick check of reasonableness, not a formal proof.

**Not used:** Abstracting and Generalizing, Mathematical Modeling (there's no real-world context), and Collaborative Mathematics.

**Answer:** 0.3 − 0.05 = **0.25**

**Summary order:** Representing → Procedural Fluency → (Justifying, optional check)

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item is just a computation, "Find the difference," with no context, no explanation asked for, and no model to build. It checks whether the student can subtract decimals correctly and efficiently.
- The "representing" step, rewriting 0.3 as 0.30 and lining up the decimal points, is really part of the standard decimal-subtraction procedure. A fluent student does it automatically, without treating it as a separate act of choosing a representation.
- Most errors on this item are procedural: misaligning the place values (getting 0.02 or 0.2) or not regrouping correctly in the hundredths column. Those are breakdowns in procedural fluency.

**Runner-up: Representing.** If the item were scored for place-value understanding (seeing 0.3 as 30 hundredths), Representing would be a reasonable second choice. But as written, the main demand is carrying out the procedure correctly, so Procedural Fluency is the major practice.

---

## Row 166 (problem_id 71223)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the difference.
0.02 − 0.007
____
```

### Answer 1: practices in order

**Problem:** Find the difference. 0.02 − 0.007

**Answer:** 0.013

**Practices to use**

The NAEP 2026 Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. Procedural Fluency comes from the NRC strands of proficiency. This problem needs only two of these practices, plus an optional check.

**1. Representing (rewrite the problem so place values line up)**
- Write the subtraction vertically with the decimal points lined up.
- Add a trailing zero so both numbers have the same number of decimal places: 0.02 becomes 0.020.
- Now the problem reads 0.020 − 0.007. Seen as thousandths, it is 20 thousandths − 7 thousandths.

**2. Procedural Fluency (NRC): carry out the subtraction correctly**
- Thousandths place: 0 − 7 can't be done, so regroup. Take 1 hundredth from the 2 hundredths to get 10 thousandths. Then 10 − 7 = 3.
- Hundredths place: 1 hundredth is left, and 1 − 0 = 1.
- Tenths and ones places: 0.
- Result: **0.013**. In whole numbers, this is the same as 20 − 7 = 13 thousandths.

**3. Justifying and Proving (optional, brief): check the result**
- Check with addition: 0.013 + 0.007 = 0.020 = 0.02. ✓
- Check the size: 0.007 is less than 0.02, so the answer must be positive and a bit less than 0.02. 0.013 fits.

**Order:** Representing → Procedural Fluency → (Justifying, as a check)

**Practices not used:**
- Abstracting and Generalizing: the problem asks for no general rule or pattern.
- Mathematical Modeling: there is no real-world situation to model.
- Collaborative Mathematical Discourse: this is a single-answer item for one student.

Procedural Fluency does most of the work. Representing matters because the most common mistake here comes from lining up the digits wrongly. A student who lines up the last digits instead of the decimal points might compute 0.02 − 0.007 as 0.005 or 0.007 − 0.02.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item is a straight computation: "Find the difference. 0.02 − 0.007." It has no context to model, no pattern to generalize, and asks for no justification. What it tests is whether the student can run the decimal subtraction algorithm correctly. That means lining up the decimal points, adding the trailing zero (0.020), regrouping across the hundredths and thousandths places, and placing the decimal point in the answer, 0.013.

Representing, through lining up place values, is a necessary step inside the procedure. But it's the standard first step of the algorithm, not a separate representational task. So Procedural Fluency is the main practice, and Representing plays a supporting role.

---

## Row 167 (problem_id 70912)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the difference.
1.03 − 0.06
____
```

### Answer 1: practices in order

**Problem:** Find the difference. 1.03 − 0.06

**Answer:** 0.97

## Practices used to solve it, in order

The NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. You asked me to add **Procedural Fluency** from the NRC's *Adding It Up* strands. With that addition, these are the practices this problem uses, in order:

### 1. Representing
The student has to read the horizontal expression "1.03 − 0.06" and change it into a form they can work with. Usually that means writing it vertically with the decimal points lined up (1.03 over 0.06). They also need to understand the place values: 1 one and 3 hundredths, minus 6 hundredths. Getting this alignment right is the step where mistakes like subtracting 6 from the wrong place happen.

### 2. Procedural Fluency (NRC)
This is the main practice. The student carries out the subtraction algorithm accurately:
- Hundredths: 3 − 6 can't be done, so regroup. The tenths place is 0, so borrow from the ones: 1 one becomes 10 tenths, then 1 tenth becomes 10 hundredths. That leaves 0 ones, 9 tenths and 13 hundredths.
- 13 − 6 = 7 hundredths. 9 − 0 = 9 tenths. 0 − 0 = 0 ones.
- Result: **0.97**

The hard part is regrouping across the zero in the tenths place, which is a classic fluency skill.

### 3. Justifying (light, optional)
A careful student checks that the answer makes sense. For example, 1.03 is a little more than 1 and 0.06 is small, so the answer should be a little less than 1. Or they add back: 0.97 + 0.06 = 1.03. This is a quick check, not a formal proof.

### Not used
- **Abstracting and Generalizing:** the problem asks for no pattern or general rule.
- **Mathematical Modeling:** there is no real-world situation to turn into math.
- **Collaborative Mathematics:** this is a single-student item.

**Summary of order:** Representing → Procedural Fluency → Justifying (optional check)

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The problem is a bare computation, 1.03 − 0.06, with no context, pattern or argument involved. Getting it right comes down to carrying out the decimal subtraction algorithm correctly, and the hard step is regrouping across the zero in the tenths place to get 13 − 6 hundredths. That's a procedural fluency skill.

Representing (lining up the decimal points by place value) is a needed first step, but it's small and routine compared with the computation. Justifying is only an optional check. The answer is 0.97.

---

## Row 168 (problem_id 71526)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate mentally: 1.009 + 0.391
____
```

### Answer 1: practices in order

**Problem:** Evaluate mentally: 1.009 + 0.391

**Answer:** 1.4 (1.400)

**Practices available:** NAEP 2026 mathematical practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus NRC Procedural Fluency.

### Practices used, in order

**1. Abstracting and Generalizing (NAEP)**
Because the problem says "mentally," the student should look at the structure of the numbers before computing anything. The thousandths and hundredths go together nicely: 0.009 + 0.391 = 0.400 (9 thousandths + 391 thousandths = 400 thousandths). Seeing this lets the student regroup the sum as 1 + (0.009 + 0.391) instead of carrying digit by digit in their head. This is the key step. It uses general place-value and associative/commutative properties to make the calculation easy.

**2. Procedural Fluency (NRC)**
The student then does the simpler calculation quickly and correctly: 0.009 + 0.391 = 0.4, and 1 + 0.4 = 1.4. If they skip step 1, the same practice still covers adding the decimals mentally by place value (thousandths 9+1=10, carry; hundredths 0+9+1=10, carry; tenths 0+3+1=4; ones 1), which gives 1.400.

**(Optional, minor) 3. Justifying and Proving (NAEP)**
A quick check that the answer makes sense: about 1.0 + 0.4 = 1.4, so 1.400 is reasonable. This is a light self-check, not a formal justification, so it plays only a small role.

### Practices not used
- **Representing:** no diagram, table, graph, or change of representation is needed. Everything is in plain decimal notation.
- **Mathematical Modeling:** there is no real-world context.
- **Collaborative Mathematics:** this is a task done by one person.

**Summary order:** Abstracting and Generalizing → Procedural Fluency (→ a brief Justifying check, optional).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item asks the student to add two decimals mentally, correctly and efficiently: 1.009 + 0.391 = 1.4. That is what procedural fluency means. The student has to line up place values, regroup correctly across the thousandths, hundredths and tenths, and keep the running result in their head.

Abstracting and Generalizing (seeing that 0.009 + 0.391 = 0.4) makes the work easier, but it is a shortcut, not a requirement. A student who never notices it can still get the right answer through fluent place-value addition. A student who notices the structure but can't carry out decimal addition reliably will still get it wrong. So fluency is the practice the item really depends on, and the structural insight is a secondary supporting practice.

---

## Row 170 (problem_id 75309)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the product.
(2.05) · (0.004)
____
```

### Answer 1: practices in order

**Problem:** Find the product (2.05) · (0.004)

**Answer:** 2.05 × 0.004 = **0.0082**

---

### Practices available
From the NAEP Mathematics Framework (mathematical practices):
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC (*Adding It Up*) strands:
6. **Procedural Fluency**: carrying out procedures flexibly, accurately, and efficiently

### Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the decimals in place-value terms: 2.05 is 205 hundredths and 0.004 is 4 thousandths. Equivalently, 2.05 = 205 × 10⁻² and 0.004 = 4 × 10⁻³. This lets the problem be rewritten as a whole-number multiplication plus a power-of-ten shift. |
| 2 | **Procedural Fluency** (core step) | Multiplies the whole numbers: 205 × 4 = 820. |
| 3 | **Abstracting and Generalizing** | Uses the general rule that the product has as many decimal places as the factors have together: 2 + 3 = 5 decimal places (10⁻² · 10⁻³ = 10⁻⁵). |
| 4 | **Procedural Fluency** | Places the decimal point: 820 → 0.00820 = **0.0082**. This needs the leading zeros and drops the trailing zero. |
| 5 | **Justifying** (light use of Justifying and Proving) | Checks that the answer makes sense by estimating: 2 × 0.004 = 0.008, so 0.0082 is reasonable. This catches decimal-placement errors such as 0.082 or 0.00082. |

**Not needed:** Mathematical Modeling (there is no real-world context) and Collaborative Mathematics (this is an individual computation item).

### Summary
**Representing → Procedural Fluency → Abstracting and Generalizing → Procedural Fluency → (Justifying)**

Procedural Fluency is the main practice. This is mostly a routine decimal-multiplication item. The main difficulty, and the most common source of errors, is placing the decimal point correctly, which comes from the place-value representation and the general decimal-places rule.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item has no context, only a bare instruction ("Find the product") and two decimals. It asks the student to carry out a standard algorithm, and the answer is 2.05 × 0.004 = 0.0082.
- Every step of the solution is a routine procedure. The student multiplies 205 × 4 = 820, counts 2 + 3 = 5 decimal places, and writes 0.0082.
- The other practices play only a supporting role:
  - Representing (place value) and Abstracting and Generalizing (the decimal-places rule) are already built into the procedure a fluent student uses. The student does not need to construct them for this item.
  - Justifying (the estimation check) is a good habit, but the item does not require it.
- The likely mistakes are procedural: misplacing the decimal point (0.082 or 0.00082) or getting the leading zeros wrong. These are failures of accuracy in carrying out the procedure, which is what Procedural Fluency describes.

So if only one practice is chosen, it is **Procedural Fluency**.

---

## Row 171 (problem_id 76458)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the quotient.
5 ÷ 1/10
____
```

### Answer 1: practices in order

**Problem:** Find the quotient. 5 ÷ 1/10

**Answer:** 50

## Practices used, in order

The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Below I add Procedural Fluency from the NRC strands of proficiency (*Adding It Up*). Only some of these practices are needed for this item.

### 1. Representing (light use, optional)
- The student reads the symbolic expression 5 ÷ 1/10 and understands what it means: "How many tenths are in 5?"
- A student may also picture it as a model, for example 5 wholes each split into 10 tenths, which gives 5 × 10 = 50 tenths.
- This step matters most for a student who doesn't remember the rule and reasons from meaning instead.

### 2. Procedural Fluency (NRC), the main practice
- Apply the division-of-fractions procedure: 5 ÷ 1/10 = 5 × 10/1 = 50. In other words, multiply by the reciprocal ("keep, change, flip").
- The student needs to do this accurately and without hesitation. That includes writing 5 as 5/1 if needed and avoiding the common mistake of getting 5 × 1/10 = 1/2.
- This is the step that carries the item. It is a short, single-step computation.

### 3. Justifying (very light, optional self-check)
- A quick sense check: dividing by a number less than 1 should give a result *larger* than 5, so 50 is reasonable and 1/2 is not.
- This is not formal justifying or proving. It is just checking the answer, and no explanation is asked for.

### Practices not used
- **Abstracting and Generalizing:** no pattern or general rule has to be found. The item is a single computation.
- **Mathematical Modeling:** there is no real-world context to model.
- **Collaborative Mathematics:** the item is done individually.

## Summary order
**Representing (interpret 5 ÷ 1/10 as "how many tenths in 5") → Procedural Fluency (5 × 10 = 50) → (optional) quick reasonableness check**

Procedural Fluency is the main practice. Representing and the reasonableness check play only small, optional roles.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- The item is a bare computation: "Find the quotient. 5 ÷ 1/10". It has no context, asks for no explanation, and has no pattern to generalize.
- The success of the item comes down to carrying out the fraction-division procedure accurately: 5 ÷ 1/10 = 5 × 10 = 50.
- The usual wrong answer (1/2, which comes from multiplying by 1/10 instead of dividing) is a procedural error, not a problem with representing or reasoning.
- Representing ("how many tenths are in 5?") can help, but the student doesn't need it if they know the procedure. So it plays a supporting role, not the main one.

---

## Row 172 (problem_id 77299)

- **predicted_practice:** Abstracting and Generalizing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Compute the product using the equation 21 ⋅ 47 = 987 and what you know about fractions, decimals, and place value.
(2.1) ⋅ (4.7)
____
```

### Answer 1: practices in order

**Problem:** Using 21 · 47 = 987, compute (2.1) · (4.7). **Answer: 9.87**

The NAEP mathematical practices (from the NAEP Mathematics Framework) are: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added NRC **Procedural Fluency** to that list.

### Practices in order

**1. Abstracting and Generalizing (NAEP)**
Notice how the new problem is built from the known fact. 2.1 is 21 ÷ 10 and 4.7 is 47 ÷ 10. So (2.1)(4.7) is the same multiplication as 21 · 47, only scaled. The general rule is that moving a decimal point in a factor scales the product by the same power of ten. This is the key step: it lets you reuse the given equation instead of multiplying from scratch.

**2. Representing (NAEP)**
Write the decimals as fractions (or in powers-of-ten form) so the structure is clear:
(2.1)(4.7) = (21/10)(47/10) = (21 · 47)/100.
Switching between decimal, fraction, and place-value forms is what the problem asks for when it says "what you know about fractions, decimals, and place value."

**3. Procedural Fluency (NRC)**
Do the calculation quickly and accurately. Substitute 21 · 47 = 987, then divide by 100, which moves the decimal point two places left: 987/100 = **9.87**. This step relies on fluent decimal and place-value procedures, such as counting decimal places (1 + 1 = 2).

**4. Justifying and Proving (NAEP), light use**
Check that the answer makes sense. Estimate 2 × 5 = 10, or more closely 2.1 × 4.7 ≈ 2 × 4.7 = 9.4 plus a bit, so 9.87 is reasonable. This rules out place-value slips like 98.7 or 0.987.

**Not used:** Mathematical Modeling (there's no real-world context) and Collaborative Mathematics (it's an individual task).

**Order:** Abstracting and Generalizing → Representing → Procedural Fluency → (Justifying and Proving as a check)

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

The problem gives you 21 · 47 = 987 so you don't have to multiply 2.1 × 4.7 directly. The main thing it tests is whether you see the structure: 2.1 and 4.7 are 21 and 47 each scaled by 1/10, so the product is 987 scaled by 1/100. That gives 9.87.

The other practices support this step:
- **Representing** (writing 2.1 · 4.7 as (21/10)(47/10)) is how you express the relationship once you've seen it.
- **Procedural Fluency** (moving the decimal point two places) is easy once the structure is clear.
- **Justifying** (estimating ≈ 10) is only a check.

A student who misses the general rule that scaling a factor scales the product has to compute 2.1 × 4.7 from scratch or gets stuck. A student who sees it gets the answer almost right away. So Abstracting and Generalizing is the practice that decides the problem.

---

## Row 174 (problem_id 77578)

- **predicted_practice:** Abstracting and Generalizing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Compute the product using the equation 21 ⋅ 47 = 987 and what you know about fractions, decimals, and place value.
21 ⋅ (0.047)
____
```

### Answer 1: practices in order

**Problem:** Use 21 · 47 = 987 to compute 21 · (0.047).

**Answer: 0.987**

## Practices available

The NAEP 2026 Mathematics Framework names five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

To these I add **Procedural Fluency**, one of the five strands of mathematical proficiency in the NRC's *Adding It Up*. It means carrying out procedures flexibly, accurately and efficiently.

## Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Writes the decimal another way, as a fraction or in place-value form: 0.047 = 47/1000 = 47 × (1/1000). This turns the new product into one that uses the known fact: 21 · 0.047 = 21 · 47 × (1/1000). |
| 2 | **Abstracting and Generalizing** | Sees the general rule: if you scale one factor by 1/1000 (move it three place values to the right of the decimal point), the product is scaled the same way. So the given fact can be reused instead of multiplying again: 21 · 0.047 = 987 × (1/1000). |
| 3 | **Procedural Fluency (NRC)** | Does the arithmetic accurately: 987 ÷ 1000 = 0.987, moving the decimal point three places to the left. |
| 4 | **Justifying and Proving** *(light, for checking)* | Checks that the answer makes sense: 0.047 is a little less than 0.05, and 21 × 0.05 ≈ 1.05, so the answer should be just under 1. 0.987 fits. This also catches common place-value slips such as 9.87 or 0.0987. |

**Not used:** Mathematical Modeling, because there is no real-world context to turn into math, and Collaborative Mathematics, because this is an individual computation item.

## Summary of the order
**Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving as a check)**

The main step is the first two together: recognizing 0.047 as 47 thousandths and seeing that the known product just shifts three place values. The procedural step is short once that structure is clear.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

Why this one:

- **The problem is built around it.** The item gives you 21 · 47 = 987 and asks you to use it, not to multiply from scratch. The key step is seeing how 21 · 0.047 relates to the known fact: one factor is 1/1000 as large, so the product is also 1/1000 as large. That is a general rule about how multiplication and place value work together, used here in one specific case.
- **It is what tells students apart.** A student who sees this structure gets 0.987 right away. A student who doesn't either multiplies the long way, which defeats the purpose of the item, or misplaces the decimal (9.87, 0.0987).
- **The other practices support it.** Representing (0.047 = 47/1000) sets up the relationship, and Procedural Fluency (987 ÷ 1000) just finishes it off. Both are small, routine steps once the structure is clear.

If the item were coded for one practice only, I would code it as **Abstracting and Generalizing**, with Representing a close second.

---

## Row 175 (problem_id 78269)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of 36.8 ÷ 2.3.
____
```

### Answer 1: practices in order

**Problem:** Find the value of 36.8 ÷ 2.3. (Answer: **16**)

**Practices available:** the NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've also added **Procedural Fluency** from the NRC's *Adding It Up* strands.

This is a plain computation with no context, so most of the NAEP practices don't really apply. Here are the ones that do, in order:

1. **Representing** (minor, first step). Rewrite the division in an equivalent form that's easier to work with. Multiply the dividend and divisor by 10 so the divisor becomes a whole number:
   36.8 ÷ 2.3 → 368 ÷ 23 (or think of it as the fraction 36.8/2.3 = 368/23).
   This is a change of representation, not modeling. It relies on the fact that scaling both numbers by the same amount leaves the quotient unchanged.

2. **Procedural Fluency (NRC)** (main practice). Carry out the division accurately and efficiently:
   - 23 × 10 = 230, leaving 368 − 230 = 138
   - 23 × 6 = 138, leaving 0
   - So 368 ÷ 23 = **16**
   This step carries most of the problem: knowing how to place the decimal and running the long-division steps correctly.

3. **Justifying and Proving** (optional, light check). Confirm the answer is reasonable: 2.3 × 16 = 36.8 ✓. An estimate also works: 36.8 ÷ 2.3 ≈ 36 ÷ 2 = 18, so 16 is plausible. This is self-checking rather than a formal argument, so it plays a small part.

**Practices not used:**
- *Abstracting and Generalizing*: the problem doesn't ask for a general rule or pattern.
- *Mathematical Modeling*: there is no real-world situation to translate.
- *Collaborative Mathematics*: this is a solo task with no need to communicate or critique someone else's reasoning.

**Summary of order:** Representing → **Procedural Fluency** (main) → Justifying and Proving (check). Procedural fluency is the main practice this item measures.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item gives a bare computation, 36.8 ÷ 2.3, with no context, nothing to model, no pattern to generalize and no argument to make. What it tests is whether a student can do decimal division accurately and efficiently: shift the decimal so the divisor is a whole number (368 ÷ 23), then finish the division to get **16**. That is procedural fluency.

Representing (rewriting the problem as 368 ÷ 23) and Justifying (checking that 2.3 × 16 = 36.8) only support that main step. Students who get the item right or wrong are mostly showing whether they have command of the division procedure.

---

## Row 176 (problem_id 77861)

- **predicted_practice:** Abstracting and Generalizing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Compute the product using the equation 21 ⋅ 47 = 987 and what you know about fractions, decimals, and place value.
(0.021) ⋅ (4.7)
____
```

### Answer 1: practices in order

**Answer: 0.021 x 4.7 = 0.0987**

The practices to use, in order, are drawn from the NAEP 2026 Mathematics Framework (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus Procedural Fluency from the NRC.

### Order of practices

**1. Representing**
Rewrite the decimals as whole numbers scaled by powers of ten, or as fractions:
- 0.021 = 21/1000 = 21 x 10^-3
- 4.7 = 47/10 = 47 x 10^-1

This moves the problem from decimal notation into fraction and place-value notation. That notation is what links it to the given fact, 21 x 47 = 987.

**2. Abstracting and Generalizing**
Spot the structure: the digits 21 and 47 match the given equation, and only the place values differ. Apply the general rule (a/10^m)(b/10^n) = ab/10^(m+n). So the product is 987 scaled by 10^(-3-1) = 10^-4. This is the key step. It reuses a known fact in a new setting and doesn't redo the multiplication.

**3. Procedural Fluency (NRC)**
Carry out the steps quickly and accurately:
- (21/1000)(47/10) = (21 x 47)/(1000 x 10) = 987/10000
- 987/10000 = 0.0987. Shift the decimal point 4 places left, writing a leading zero as a placeholder.

**4. Justifying and Proving (checking)**
Confirm the answer is reasonable. 0.021 is about 0.02 and 4.7 is about 5, and 0.02 x 5 = 0.1. So 0.0987 has the right size. Also, the factors have 3 + 1 = 4 decimal places, and the answer has 4 decimal places.

### Practices not used
- **Mathematical Modeling**: there is no real-world situation to model.
- **Collaborative Mathematics**: this is an individual computation task.

### Summary
Representing -> Abstracting and Generalizing -> Procedural Fluency -> Justifying and Proving

The main practice is **Abstracting and Generalizing**: seeing that the place-value structure carries the known product over. Representing sets that step up, Procedural Fluency carries it out, and Justifying confirms it.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

Why this one:
- The problem tells students to use 21 x 47 = 987 rather than multiply again. Doing that means seeing that 0.021 x 4.7 has the same structure as 21 x 47, with only the place values different.
- The key step is applying a general rule, (a/10^m)(b/10^n) = ab/10^(m+n), to move a known fact into a new setting. That is abstracting and generalizing.
- The other practices support this step. Representing (rewriting the decimals as fractions or powers of ten) sets it up. Procedural Fluency (shifting the decimal point 4 places to get 0.0987) carries it out. Justifying (estimating 0.02 x 5 = 0.1) checks it.

A student who just multiplies 0.021 x 4.7 from scratch with good procedural fluency could get the right answer. But they would skip the reasoning the problem is designed to test.

---

## Row 179 (problem_id 79155)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Use the diagram to help you find (0.04) ⋅ (0.02).
____
```

### Answer 1: practices in order

**Problem:** Use the diagram to help you find (0.04) · (0.02).
**Answer:** 0.0008

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Below I add Procedural Fluency from the NRC strands as a sixth.

## Practices needed, in order

**1. Representing (NAEP), primary practice**
The problem tells the student to use the diagram, so the first step is reading the area model. The diagram is most likely a grid where one whole square is split into 100 parts (hundredths). Each of those parts may also be split again into 100, giving ten-thousandths. The student has to:
- see 0.04 as 4 hundredths along one side and 0.02 as 2 hundredths along the other side,
- read the product as the area of the overlapping rectangle, which is 4 × 2 = 8 small cells,
- work out how big each small cell is compared with the whole: (1/100) × (1/100) = 1/10,000.

Moving between the picture and the decimal symbols is the core of this item.

**2. Procedural Fluency (NRC)**
Once the representation is set up, the student carries out the calculation:
- multiply the whole numbers: 4 × 2 = 8,
- place the decimal point: 2 decimal places + 2 decimal places = 4 places, so the answer is 0.0008.

The student needs to do this correctly and quickly. A common mistake is to write 0.08 or 0.008 by misplacing the decimal point.

**3. Abstracting and Generalizing (NAEP), secondary and light**
The student links the diagram to the general rule "hundredths × hundredths = ten-thousandths". That rule is why the decimal-place count from step 2 works, and it is why the product (0.0008) is smaller than either factor.

**4. Justifying and Proving (NAEP), optional check**
This is only an informal check. Does the area in the diagram (8 out of 10,000 cells) match 0.0008? Both factors are less than 1, so the product should be smaller than each one. The item asks for no written justification, so this practice plays only a small part.

## Not needed
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** this is a single student working alone.

## Summary order
Representing → Procedural Fluency → Abstracting and Generalizing (minor) → Justifying and Proving (minor check)

The main practices are Representing and Procedural Fluency. The other two play a supporting role.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The problem says "Use the diagram to help you find (0.04) · (0.02)." The item is built around the diagram, and that is what sets it apart from a bare decimal-multiplication exercise. To answer it, the student has to read the area model. That means seeing 0.04 and 0.02 as the side lengths, the 4 × 2 = 8 shaded cells as the product, and each cell as 1/10,000 of the whole. Then they turn the picture into the symbolic answer 0.0008.

Procedural Fluency is a close second. A student could skip the diagram, multiply 4 × 2, and count decimal places. But the item explicitly asks them to reason from the diagram. So the skill it was designed to assess is moving between the visual model and the decimal notation, which is Representing.

---

## Row 180 (problem_id 81337)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the quotient. Write your answer as a fraction or a mixed number.
10 1/7 ÷ 5
____
```

### Answer 1: practices in order

**Problem:** Find the quotient 10 1/7 ÷ 5. Write it as a fraction or a mixed number.

**Solution:** 10 1/7 = 71/7, and 71/7 ÷ 5 = 71/7 × 1/5 = 71/35 = **2 1/35**.
(Another way: 10 ÷ 5 = 2 and 1/7 ÷ 5 = 1/35, so the answer is 2 1/35.)

---

### The practices available

The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

From the NRC's *Adding It Up* strands, I'm adding:
6. **Procedural Fluency**: carrying out procedures flexibly, accurately, and efficiently.

### Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Rewrites the problem in a form they can compute with. The mixed number 10 1/7 becomes the improper fraction 71/7, and "÷ 5" becomes "× 1/5", since dividing by 5 is the same as multiplying by its reciprocal. Also writes 5 as 5/1. |
| 2 | **Procedural Fluency** (main practice) | Carries out the fraction procedure correctly: 71/7 × 1/5 = 71/35. Checks whether it simplifies. 71 is prime, so it doesn't. |
| 3 | **Representing** (again, briefly) | Turns the answer back into the requested form: 71/35 = 2 1/35, because 35 × 2 = 70 with remainder 1. The answer 71/35 is also acceptable. |

So the sequence is **Representing → Procedural Fluency → Representing**. Procedural fluency does most of the work. Representing is the conversion step before and after the calculation.

### Practices not needed
- **Abstracting and Generalizing:** The student doesn't need to find a pattern or a general rule. They only apply a known one.
- **Justifying and Proving:** The student doesn't have to explain or prove anything.
- **Mathematical Modeling:** There is no real-world situation to turn into math. The problem is already written in math.
- **Collaborative Mathematics:** This is a task done alone.

**Summary:** This is mainly a procedural-fluency item. Representing comes before it (mixed number to improper fraction, dividing to multiplying by the reciprocal) and after it (improper fraction back to a mixed number).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Here's why:

- **The item asks for a calculation.** "Find the quotient" asks the student to run a known procedure on numbers they're given. There's no context to model, nothing to justify, and no pattern to generalize.
- **The work is mostly following the procedure.** The student converts 10 1/7 to 71/7, multiplies by the reciprocal (71/7 × 1/5 = 71/35), checks whether the fraction simplifies, and converts back to 2 1/35. Each step is a standard fraction routine.
- **Representing is a supporting practice.** Switching between mixed numbers and improper fractions, and rewriting ÷ 5 as × 1/5, matters, but it happens inside the procedure. Students learn these switches as steps of the fraction-division routine, not as a separate act of representation.
- **Errors here are procedural.** Typical mistakes are dividing only the whole-number part (getting 2 1/7), forgetting to take the reciprocal, or mistakes converting between mixed numbers and improper fractions. All of these are procedural-fluency errors.

If I had to choose only among the five NAEP practices, without the NRC strand, I would choose **Representing**. It's the only NAEP practice the item really uses, through the mixed-number/improper-fraction conversions and turning division into multiplication by the reciprocal.

---

## Row 181 (problem_id 81228)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the quotient. Write your answer as a fraction or a mixed number.
6 1/4 ÷ 2
____
```

### Answer 1: practices in order

**Problem:** Find the quotient, written as a fraction or mixed number: 6 1/4 ÷ 2

The NAEP Mathematics Framework names five mathematical practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, and (5) Collaborative Mathematics. Below I add **Procedural Fluency** from the NRC's *Adding It Up* strands, as you asked.

This is a short computation problem. It needs only two practices.

### Practices used, in order

**1. Representing (NAEP)**
The student first has to rewrite the mixed number 6 1/4 as the improper fraction 25/4. They also need to see the whole number 2 as 2/1 and dividing by it as multiplying by 1/2. Nothing can be computed until the problem is in this form.
- 6 1/4 = 25/4
- 25/4 ÷ 2 = 25/4 × 1/2

**2. Procedural Fluency (NRC)**
Next comes the procedure itself: multiply by the reciprocal, multiply numerators and denominators, then simplify or convert the answer to a mixed number.
- 25/4 × 1/2 = 25/8
- 25/8 = 3 1/8

Representing comes back for a moment at the end, when the student writes the result in the requested form (fraction or mixed number). This step is small, so I count it as part of the procedure.

**Answer:** 25/8 = **3 1/8**

### Practices not needed
- **Abstracting and Generalizing:** the student applies one known rule and builds no general pattern.
- **Justifying and Proving:** no explanation or argument is asked for.
- **Mathematical Modeling:** the problem has no real-world context to turn into math.
- **Collaborative Mathematics:** it is a single-student computation item.

### Summary
| Order | Practice | Role |
|---|---|---|
| 1 | Representing | Rewrite 6 1/4 as 25/4 and ÷2 as ×1/2 |
| 2 | Procedural Fluency | Compute 25/8 and convert it to 3 1/8 |

Procedural Fluency does most of the work here. Representing is the step that comes before it.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

This item is a direct computation, 6 1/4 ÷ 2, with no context and nothing to explain. Most of what it tests is whether the student can carry out the procedure correctly:

- convert 6 1/4 to 25/4
- multiply by the reciprocal: 25/4 × 1/2 = 25/8
- write the result as 3 1/8

Representing (turning the mixed number into an improper fraction) is needed, but it is a routine first step inside that procedure. Students usually get this item wrong because of a procedural slip, not a representation problem. Typical slips are:

- dividing only the whole part (giving 3 1/4)
- converting the mixed number incorrectly
- multiplying instead of dividing

So I would pick **Procedural Fluency** as the major practice, with Representing as a minor, supporting one.

---

## Row 183 (problem_id 86400)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A fence is being built around a rectangular garden that is 8 1/2 feet by 6 1/3 feet. Fencing comes in panels. Each panel is 2/3 of a foot wide. How many panels are needed?
____ panels
```

### Answer 1: practices in order

**Practices I used:** the NAEP 2026 Mathematics Framework practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus **Procedural Fluency** from the NRC's strands of proficiency.

**Answer: 45 panels.** The perimeter is 29 2/3 ft. That is 44.5 panel-widths, rounded up to 45.

## Practices in the order they are used

**1. Mathematical Modeling: set up the problem**
- A fence goes "around" the garden, so the length you need is the **perimeter**, not the area.
- A panel only comes whole, so the count must be a whole number of panels. This is the kind of real-world limit that modeling deals with.
- The model is: panels = perimeter ÷ panel width, rounded **up**.

**2. Representing: turn the words into math**
- Write the sides as numbers you can work with: 8 1/2 = 17/2 ft and 6 1/3 = 19/3 ft.
- Write the perimeter as an expression: P = 2(17/2 + 19/3).
- Write the panel count as a division: P ÷ 2/3.

**3. Procedural Fluency (NRC): do the calculations**
- Add the mixed numbers using a common denominator: 17/2 + 19/3 = 51/6 + 38/6 = 89/6 = 14 5/6 ft.
- Double it: P = 2 × 89/6 = 89/3 = 29 2/3 ft.
- Divide fractions by multiplying by the reciprocal: 89/3 ÷ 2/3 = 89/3 × 3/2 = 89/2 = 44 1/2.

**4. Mathematical Modeling again: interpret the result**
- 44.5 panels makes no sense in the real world. 44 panels leave a gap of 1/3 ft, so you need **45 panels**.

**5. Justifying and Proving: check that 45 is right (minor role)**
- 44 panels cover 44 × 2/3 = 29 1/3 ft, which is less than 29 2/3 ft, so 44 is too few.
- 45 panels cover 45 × 2/3 = 30 ft, which is at least 29 2/3 ft, so 45 is enough.
- 45 is therefore the smallest number that works.

## Not really used
- **Abstracting and Generalizing:** the problem asks for no general rule or pattern.
- **Collaborative Mathematics:** this is an individual assessment item.

## Summary
**Mathematical Modeling → Representing → Procedural Fluency → Mathematical Modeling (interpret and round up) → Justifying (check)**

The main steps are Modeling, Representing and Procedural Fluency. The most common mistakes are:
- using the area instead of the perimeter (a modeling error);
- giving 44 or 44.5 instead of rounding up to 45 (an interpretation error).

### Answer 2: major practice

**My pick for the major practice: Procedural Fluency (NRC).**

**Why:**
- **It is most of the work.** Almost every step is a fraction procedure:
  - change the mixed numbers to fractions (8 1/2 = 17/2, 6 1/3 = 19/3);
  - add them with a common denominator (51/6 + 38/6 = 89/6);
  - double the sum to get the perimeter (89/3 = 29 2/3 ft);
  - divide by a fraction using the reciprocal (89/3 × 3/2 = 44 1/2).
- **It is where students most likely go wrong.** Unlike denominators and dividing by a fraction are classic sticking points, and there are four or more chances to slip.
- **The other decisions are quick.** "Around" means perimeter, and a leftover part of a panel means rounding up. These are short, familiar steps. Once the student makes them, the item is a multi-step fraction calculation.

**Close second: Mathematical Modeling.** Seeing that you need the perimeter and must round 44.5 up to 45 is what separates a correct answer from 44 or from an area-based answer. If the item were mainly testing context and interpretation, with easy numbers, Modeling would be the major practice. Here the numbers are deliberately fraction-heavy, so the main demand is Procedural Fluency.

---

## Row 185 (problem_id 88)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate (1.6) · (0.215).
____
```

### Answer 1: practices in order

**Problem:** Calculate (1.6) · (0.215)

**Practices to choose from:** the five practices in the NAEP 2026 Mathematics Framework (Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics), plus Procedural Fluency from the NRC strands.

This is a plain computation with no context, no pattern to generalize and no claim to prove. So most of the work is **Procedural Fluency**. Only a little Representing is involved, and the estimation check is optional.

### Practices, in order

**1. Representing (minor): turn the decimals into whole numbers you can multiply**
- Rewrite the product as whole numbers scaled by powers of ten: 1.6 = 16 / 10 and 0.215 = 215 / 1000.
- So (1.6)(0.215) = (16 × 215) / 10,000.
- Most students do this without thinking about it ("ignore the decimals, then put them back"). It is still a change of representation, and it is the reason the decimal-placement rule works.

**2. Procedural Fluency (main practice): multiply and place the decimal point**
- Multiply the whole numbers: 16 × 215 = 16 × 200 + 16 × 15 = 3200 + 240 = 3440.
- Count the decimal places: 1.6 has 1 and 0.215 has 3, which makes 4 in total.
- 3440 with 4 decimal places is 0.3440, which is **0.344**.
- Doing this quickly and accurately, including the decimal point, is exactly what NRC means by procedural fluency.

**3. Justifying (light, optional): check that the answer is reasonable**
- Estimate: 1.6 × 0.2 = 0.32, and 0.215 is slightly more than 0.2, so the answer should be slightly more than 0.32.
- 0.344 fits. This rules out decimal-placement mistakes such as 3.44 or 0.0344.
- This is a self-check, not a formal proof, so it counts as Justifying and Proving only in a weak sense.

### Not used
- **Abstracting and Generalizing:** there is no pattern or general rule to find.
- **Mathematical Modeling:** there is no real-world situation.
- **Collaborative Mathematics:** this is a single-student computation.

### Summary
**Representing (minor) → Procedural Fluency (main) → Justifying (optional estimate check)**

**Answer: 0.344**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The problem only asks for a calculation, (1.6) · (0.215). To get it right, a student needs to:
- carry out the standard multiplication: 16 × 215 = 3440
- place the decimal point correctly (1 + 3 = 4 decimal places), giving 0.344

This is exactly what procedural fluency means: carrying out a procedure accurately and efficiently. Representing (writing the decimals as whole numbers over powers of ten) and the estimation check are small supporting steps. A student who is fluent with the procedure can solve the problem without consciously using either one.

**Answer: 0.344**

---

## Row 191 (problem_id 91640)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is the value of the expression?
(2^5 × 3^4 × 3^2)/(2 × 3^6 × 2^4)
____
```

### Answer 1: practices in order

**Problem:** What is the value of (2^5 × 3^4 × 3^2) / (2 × 3^6 × 2^4)?

**Answer: 1**

## The practice pool

The NAEP 2026 Mathematics Framework names five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

You asked me to add a sixth:
6. **Procedural Fluency** (from NRC, *Adding It Up*). This means carrying out procedures flexibly, accurately and efficiently.

## Practices needed, in order

**Step 1: Representing.** The student reads the fraction and rewrites it so the base-2 factors and base-3 factors are grouped:
(2^5 × 3^4 × 3^2) / (2^1 × 2^4 × 3^6)
They also need to see that the lone "2" in the denominator means 2^1. This step turns the given expression into a form that is easier to work with.

**Step 2: Abstracting and Generalizing.** The student recognizes that the general exponent rules apply here:
- Product rule: a^m × a^n = a^(m+n)
- Quotient rule: a^m / a^n = a^(m−n)
- Zero exponent: a^0 = 1

Choosing these structural rules is the key step. Without it, the student would have to multiply out 2^5 × 3^4 × 3^2 = 32 × 81 × 9 = 23,328 and divide by 2 × 729 × 16 = 23,328. That works, but it takes much longer and is easier to get wrong.

**Step 3: Procedural Fluency (NRC).** The student applies the rules accurately:
- Numerator: 2^5 × 3^(4+2) = 2^5 × 3^6
- Denominator: 2^(1+4) × 3^6 = 2^5 × 3^6
- Quotient: 2^(5−5) × 3^(6−6) = 2^0 × 3^0 = 1 × 1 = **1**

This is where most of the work happens: adding and subtracting exponents correctly, and not dropping the implied exponent of 1.

**Step 4 (optional, light): Justifying.** A short sense check: the numerator and denominator are the same product, so their quotient must be 1. This is a quick check, not a formal proof, so it plays a minor role.

## Practices not needed

- **Mathematical Modeling:** There is no real-world context to model.
- **Collaborative Mathematics:** This is an individual item with no discourse or critique of others' reasoning.
- **Justifying and Proving (formal):** The answer is a number to fill in, with no argument required.

## Summary sequence

**Representing → Abstracting and Generalizing → Procedural Fluency → (light Justifying check)**

Procedural Fluency is the main practice for this item. Abstracting and Generalizing (seeing which exponent rules apply) is the main conceptual step that comes before it.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- **The item tests whether you can carry out the exponent rules correctly.** Representing (grouping like bases) and Abstracting and Generalizing (knowing which rules to use) are quick setup steps. The real work, and the place students usually go wrong, is the execution:
  - adding exponents: 3^4 × 3^2 = 3^6 and 2^1 × 2^4 = 2^5
  - subtracting exponents to get 2^0 × 3^0
  - knowing that a^0 = 1
- **The common errors are procedural ones.** For example:
  - treating the lone "2" as 2^0 instead of 2^1
  - multiplying exponents when they should be added
  - writing 2^0 = 0 instead of 1

  These are fluency mistakes, not mistakes in choosing a strategy.
- **The item is short and has one standard method.** There is no context to interpret, no argument to build, and no real choice of strategy. That makes it a standard fluency item.

If you had to name the main *conceptual* practice instead, it would be Abstracting and Generalizing. But as the single major practice for this item, I would pick **Procedural Fluency**.

---

## Row 194 (problem_id 92205)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the product of 12 and 8.
____
```

### Answer 1: practices in order

**Problem:** Find the product of 12 and 8.

**Answer:** 12 × 8 = **96**

## Which practices to use, and in what order

The NAEP Mathematics Framework (2026) lists five mathematical practices:

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

On top of these I am adding **Procedural Fluency** from the NRC's *Adding It Up* (2001).

This is a one-step computation with no context, so most of the NAEP practices don't really apply. Only two practices do real work here.

### Step 1: Representing (light use)
The student turns the words into symbols. "Product" means multiply, so "the product of 12 and 8" becomes **12 × 8**. This is the only translation step, and it is small. All it takes is knowing that "product" means multiplication.

### Step 2: Procedural Fluency (main practice)
The student computes 12 × 8 accurately and efficiently, which is the core of the problem. Any of these routes works:
- Recall the fact directly (it's in the 12× table): 96
- Use the distributive property: 12 × 8 = (10 × 8) + (2 × 8) = 80 + 16 = 96
- Double repeatedly: 12 × 2 = 24, then 48, then 96
- Use the standard multiplication algorithm

Choosing a good strategy and carrying it out without mistakes is exactly what procedural fluency means.

### Step 3 (optional): a quick check
A student could check the answer by estimating (10 × 8 = 80, so 96 makes sense) or by reversing it (96 ÷ 8 = 12). This is a self-check, not formal **Justifying and Proving**. The problem doesn't ask for any justification, so I would not count that practice as required.

## Practices not used
- **Abstracting and Generalizing:** Nothing to generalize. It is a single numeric case.
- **Justifying and Proving:** The problem asks for no argument or explanation.
- **Mathematical Modeling:** There is no real-world situation to model.
- **Collaborative Mathematics:** It is a solo task.

## Summary

| Order | Practice | Role |
|---|---|---|
| 1 | Representing (NAEP) | Minor. Turn "product of 12 and 8" into 12 × 8 |
| 2 | Procedural Fluency (NRC) | **Primary.** Compute 12 × 8 = 96 |

**Dominant practice:** Procedural Fluency. This is basically a multiplication fact item, and Representing only shows up briefly at the start.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- The whole problem comes down to one computation, 12 × 8 = 96. Whether a student gets it right depends on recalling the fact or carrying out a multiplication strategy without mistakes, which is what procedural fluency means.
- The only other practice involved is Representing, and it does very little here. Students just have to read "product" as multiplication, which is a vocabulary step.
- A student who answers wrong almost certainly made a computation or fact-recall error, not a representation error. That also points to Procedural Fluency as the skill this item measures.

---

## Row 195 (problem_id 92479)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Use long division to find the quotient. Write your answer as a decimal.
216 ÷ 5
____
```

### Answer 1: practices in order

**Problem:** Use long division to find the quotient of 216 ÷ 5. Write the answer as a decimal.

**Practices available:** the NAEP 2026 mathematical practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematical Discourse), plus Procedural Fluency from the NRC strands of proficiency.

This is a computation exercise. There is no real-world context, nothing to generalize, and no one to discuss it with. That leaves two practices, plus an optional check at the end.

### Order of practices

**1. Representing (setting up)**
- Put the problem into long-division form: 5 is the divisor, 216 is the dividend.
- Because the answer has to be a decimal, write the dividend as **216.0**, adding a decimal point and a placeholder zero. That way the remainder carries on into tenths and doesn't stop as "R 1."

**2. Procedural Fluency (main practice)**
Run the long-division steps correctly and in order:
- 21 ÷ 5 = 4, and 4 × 5 = 20, so subtract to get 1. Bring down the 6 to make 16.
- 16 ÷ 5 = 3, and 3 × 5 = 15, so subtract to get 1.
- Bring the decimal point straight up into the quotient. Bring down the 0 to make 10.
- 10 ÷ 5 = 2, and 2 × 5 = 10, so subtract to get 0. Stop.
- Quotient = **43.2**

**3. Representing (writing the answer)**
- Give the result in the required form, the decimal 43.2. Don't write it as 43 R1 or 43 1/5. This means understanding that a remainder of 1 out of 5 is the same as 0.2.

**4. (Optional) Justifying and Proving (checking)**
- Check with the inverse operation: 43.2 × 5 = 216. This step is light, and the problem doesn't require it.

### Summary
**Representing → Procedural Fluency → Representing** (→ Justifying, optional)

Procedural Fluency is the main practice here. Representing appears twice: once to set up 216 as 216.0, and once to write the remainder as a decimal.

**Answer: 43.2**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The problem names the method ("Use long division"). The student doesn't have to choose a strategy, read a context, or build a model. The task is to run a known algorithm correctly.
- Most of the work, and most of the ways to get it wrong, are in the long-division steps: divide, multiply, subtract, bring down, place the decimal point, and carry on into the tenths place.
- Representing matters only at the edges: writing 216 as 216.0 and giving the answer as a decimal. A student who knows the long-division procedure well already does both as part of it.

**Answer: 43.2**

---

## Row 196 (problem_id 92518)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the least common multiple of 12 and 8.
____
```

### Answer 1: practices in order

**Problem:** Find the least common multiple of 12 and 8.

The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Here they are together with the NRC strand **Procedural Fluency**, in the order you would use them on this problem:

| Step | Practice | How it shows up in this problem |
|---|---|---|
| 1 | **Representing** (NAEP) | Turn "least common multiple of 12 and 8" into something you can work with. That could be a list of multiples (12, 24, 36...; 8, 16, 24...) or prime factorizations (12 = 2² · 3, 8 = 2³). |
| 2 | **Procedural Fluency** (NRC) | Carry out the procedure correctly and quickly. List multiples until one is shared, or take the highest power of each prime: 2³ · 3 = 24. You could also use LCM = (12 · 8) / GCD(12, 8) = 96 / 4 = 24. |
| 3 | **Justifying and Proving** (NAEP), minor | A quick check: 24 ÷ 12 = 2 and 24 ÷ 8 = 3, and no smaller multiple of 12 (just 12 itself) is divisible by 8. So 24 is the *least* common multiple. This step is optional because the item only asks for the answer. |

**Practices not needed:**
- **Abstracting and Generalizing:** No general rule or pattern has to be built. The student uses a known method on two specific numbers.
- **Mathematical Modeling:** There is no real-world context to turn into math.
- **Collaborative Mathematics:** The student solves it alone.

**Order:** Representing → Procedural Fluency → (Justifying and Proving, optional check)

**Main practice:** Procedural Fluency. This is a routine computation item, and Representing mainly sets up the procedure.

**Answer:** 24

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The problem is a plain, routine computation: "Find the least common multiple of 12 and 8." There's no context to interpret, no pattern to generalize and no argument to build.
- Almost all of the thinking goes into carrying out a known procedure correctly. You either list multiples until one is shared, or take the highest power of each prime (2³ · 3 = 24).
- Representing is barely involved. The numbers are given directly, so writing them as multiples or prime factors is just the first step of the procedure, not a separate translation task.
- Students who miss this item usually do so for procedural reasons. They might give the product (96) or the GCD (4), or mix up LCM and GCF. Those are fluency errors, not errors in representing or reasoning.

**Answer:** 24

---

## Row 197 (problem_id 92361)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the greatest common factor of 12 and 8.
____
```

### Answer 1: practices in order

**Practices available**

NAEP Mathematics Framework (2026) mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC (*Adding It Up*): **Procedural Fluency**, meaning carrying out procedures flexibly, accurately, and efficiently.

**Problem:** Find the greatest common factor of 12 and 8.

**Practices needed, in order**

1. **Representing.** Turn each number into a form where you can compare factors. You can list the factors or write the prime factorizations:
   - 12: 1, 2, 3, 4, 6, 12, or 2 × 2 × 3
   - 8: 1, 2, 4, 8, or 2 × 2 × 2

2. **Procedural Fluency.** Run the GCF procedure correctly. Find the factors the two lists share (1, 2, 4) and pick the largest. With prime factorization, multiply the shared primes (2 × 2). Either way the answer is **4**.

3. **Justifying and Proving (optional, minor).** You can check that 4 divides both 12 and 8, and that no larger shared factor exists (6 and 12 do not divide 8). The problem doesn't ask for a justification, so this is only a self-check.

**Not needed:** Abstracting and Generalizing (no general pattern is asked for), Mathematical Modeling (there is no real-world context), and Collaborative Mathematics.

**Summary:** Representing, then Procedural Fluency, with an optional check under Justifying. This is mainly a procedural-fluency item. Answer: **4**

### Answer 2: major practice

**Major practice: Procedural Fluency**

Finding the GCF of 12 and 8 is a routine procedure. You list the factors (or use prime factorization), find the ones the two numbers share, and pick the largest, which is 4. The item mainly checks whether a student can do that accurately and efficiently.

Representing (listing the factors) is only the first step of that procedure. It doesn't call for any real choice or translation between representations. No other practice plays a meaningful role here.

---

## Row 198 (problem_id 92677)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the product of the greatest common factor and the least common multiple of 12 and 8.
____
```

### Answer 1: practices in order

**Problem:** Find the product of the greatest common factor and the least common multiple of 12 and 8.

**Solution:** GCF(12, 8) = 4 and LCM(12, 8) = 24, so the product is 4 x 24 = **96**. As a check, this equals 12 x 8 = 96, because GCF(a, b) x LCM(a, b) = a x b.

---

### Practices to use, in order

The NAEP mathematics framework names five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Problem Solving. Below I add **Procedural Fluency** from the NRC's *Adding It Up* strands.

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the words into symbols: "GCF(12, 8) x LCM(12, 8)". A factor list or prime factorization gives a way to work with the numbers: 12 = 2^2 x 3 and 8 = 2^3. |
| 2 | **Procedural Fluency** (NRC) | Carries out the steps correctly. GCF: take the smallest power of each shared prime, 2^2 = 4 (or compare factor lists: 1, 2, 3, 4, 6, 12 and 1, 2, 4, 8). LCM: take the largest power of each prime, 2^3 x 3 = 24 (or list multiples: 8, 16, **24**). Then multiply: 4 x 24 = 96. This is the main practice in the problem. |
| 3 | **Abstracting and Generalizing** (NAEP), optional | Notices that the product equals 12 x 8 and that GCF x LCM = a x b holds for any two numbers. A student who already knows this can skip most of step 2 and compute 12 x 8 directly. |

**Practices that do not really apply:**
- **Justifying and Proving:** the problem asks only for a number, not an argument. At most, a student informally checks that 4 divides both numbers and that 24 is the smallest common multiple.
- **Mathematical Modeling:** there is no real-world context.
- **Collaborative Problem Solving:** this is an individual item.

**Order in brief:** Representing → Procedural Fluency → (optionally) Abstracting and Generalizing.

**Most important practice:** Procedural Fluency. Computing the GCF and LCM accurately is where the work is.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Here is why:

- **Most of the work is computation.** The student finds GCF(12, 8) = 4 and LCM(12, 8) = 24, then multiplies them to get 96. Each step is a standard procedure: list factors and multiples, or use prime factorization.
- **There is very little to represent.** The problem already names the operations. The student only has to recognize "GCF", "LCM" and "product".
- **Generalizing is not required.** Knowing that GCF x LCM = a x b is a shortcut. The problem never asks for it.
- **The errors you would expect are procedural.** Students mix up GCF and LCM, pick a common multiple that is not the least one (for example 48), or miss a factor.

So the item mainly tests whether the student can carry out the GCF and LCM procedures accurately. That makes Procedural Fluency the major practice.

---

## Row 201 (problem_id 97533)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
The store bought a table for $200 and sold it for $350. What percentage was the markup?
____ %
```

### Answer 1: practices in order

**Problem:** The store bought a table for $200 and sold it for $350. What percentage was the markup?

**Answer:** 75%

## Practices available

From the NAEP 2026 Mathematics Framework (Mathematical Practices):
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC (*Adding It Up*) strands:
6. Procedural Fluency

## Practices needed, in order

**1. Mathematical Modeling: turn the real-world situation into a math question**
- Read the business context and see what "markup" means: the amount added to the cost, expressed as a percent **of the cost** (the $200 purchase price), not of the selling price.
- Pick the quantities that matter: cost = $200, selling price = $350.
- The math question becomes: "What percent of 200 is the increase from 200 to 350?"

**2. Representing: write the relationship as a mathematical expression**
- Write the markup as a difference: 350 − 200.
- Write the markup percent as a ratio/fraction converted to a percent:
  markup % = (350 − 200) / 200 × 100

**3. Procedural Fluency (NRC): carry out the computation accurately**
- 350 − 200 = 150
- 150 / 200 = 0.75 (or simplify 150/200 = 3/4)
- 0.75 × 100 = **75%**

**4. (Light) Mathematical Modeling, interpretation step: check the result against the context**
- Interpret: the store added 75% of its cost. Check: 200 + 0.75 × 200 = 200 + 150 = 350. ✓
- This catches the common mistake of dividing by the selling price (150/350 ≈ 42.9%, which is the profit *margin*, not the markup).

## Practices not really needed
- **Abstracting and Generalizing:** no general pattern or rule has to be built; it's one specific case.
- **Justifying and Proving:** no formal argument is asked for; the check above is just verification.
- **Collaborative Mathematics:** it's an individual item.

## Summary order
**Mathematical Modeling → Representing → Procedural Fluency → (Modeling: interpret/check)**

Main practice: **Procedural Fluency** (the percent computation), with **Mathematical Modeling** as the key conceptual step (picking the cost as the base).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:
- The item mostly tests whether the student can carry out the standard percent-increase (markup) procedure: find the difference (350 − 200 = 150), divide by the cost (150 / 200 = 0.75), and convert to a percent (75%).
- The modeling demand is small. "Markup on cost" is a routine textbook setup, not an open real-world situation where the student has to make assumptions or pick a model. Once the student knows the markup formula, the context translates directly.
- Representing is minimal too. The expression (350 − 200)/200 × 100 comes straight from the known procedure.
- Where students go wrong (dividing by 350, forgetting to subtract, or not converting 0.75 to 75%), it is usually a slip in carrying out or remembering the procedure.

Runner-up: **Mathematical Modeling**, because the one conceptual decision here is using the cost ($200), not the selling price, as the base. But that decision is part of knowing the markup procedure, so Procedural Fluency is still the main practice.

---

## Row 204 (problem_id 99247)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A school’s art club holds a bake sale on Fridays to raise money for art supplies. Here are the number of cookies they sold each week in the fall and in the spring:
[Table:
fall | 20 | 26 | 25 | 24 | 29 | 20 | 19 | 19 | 24 | 24
spring | 19 | 27 | 29 | 21 | 25 | 22 | 26 | 21 | 25 | 25]
Find the mean number of cookies sold in the fall.
____
```

### Answer 1: practices in order

**Answer: the mean number of cookies sold in the fall is 23.**

**The practices I'm using**

The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands. It means carrying out procedures flexibly, accurately and efficiently.

**Which practices this problem needs, in order**

**1. Representing (reading the table)**
- The student has to read the two-row table and pick out only the **fall** row: 20, 26, 25, 24, 29, 20, 19, 19, 24, 24.
- They need to see that each number is one week's cookie sales, and that there are 10 weeks.
- They must ignore the spring row, which is there to distract.
- This step is about turning the table into a list of numbers to work with.

**2. Procedural Fluency (doing the mean calculation)**
- Recall the procedure: mean = sum of the values ÷ number of values.
- Add the values accurately:
  20 + 26 + 25 + 24 + 29 + 20 + 19 + 19 + 24 + 24 = 230
- Divide: 230 ÷ 10 = **23**
- A fluent student might group the numbers to add faster, for example 19 + 19 + 20 + 20 = 78 and 24 + 24 + 24 = 72. They might also add up how far each value is from 24 (−4, +2, +1, 0, +5, −4, −5, −5, 0, 0, which totals −10), so the mean is 24 − 1 = 23.
- **This is the main practice the problem tests.**

**3. Justifying and Proving (a quick check, minor)**
- The student checks that 23 makes sense: it falls between the lowest value (19) and the highest (29), and it is near the middle of the data.
- This step is optional and small. It mostly guards against adding mistakes.

**Practices this problem does not need**
- **Abstracting and Generalizing:** there is no pattern or general rule to find.
- **Mathematical Modeling:** the context is just a wrapper. No real-world modeling decisions are needed.
- **Collaborative Mathematics:** this is a single-student item.

**Summary of the order**

| Step | Practice | Role |
|---|---|---|
| 1 | Representing | Pull the fall data out of the table (10 values) |
| 2 | Procedural Fluency (NRC) | Add the values to get 230, then divide by 10 to get 23 (**main practice**) |
| 3 | Justifying and Proving (minor) | Check that 23 is a reasonable center for the data |

**Answer: 23**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why this one:**
- The task is to "find the mean." That is a request to run a standard procedure: add the 10 fall values to get 230, then divide by 10 to get 23.
- Most of the work, and most of the ways to go wrong, sit in this step. A student can slip when adding ten two-digit numbers or divide by the wrong count. A student who doesn't remember how to compute a mean can't do the problem at all.
- The other practices play only a small part:
  - **Representing** here just means reading one labeled row from a simple table. Hardly anyone would get the problem wrong at this step, except by grabbing the spring row.
  - **Justifying and Proving** is only an optional check that the answer makes sense.
- Nothing in the problem asks the student to interpret the data, compare fall with spring, or build a model. The skill being tested is carrying out the mean calculation correctly.

**Answer to the problem: 23**

---

## Row 206 (problem_id 99939)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
The MAD for the fall data is 2.8 cookies. The MAD for the spring data is 2.6 cookies. Express the difference in means as a multiple of the larger MAD.
Round your answer to the hundredth place.
____
```

### Answer 1: practices in order

**Practices in the NAEP Mathematics Framework (2026)** that I'm drawing on, plus the one from the NRC:
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics
- *(NRC "Adding It Up")* Procedural Fluency

**About the problem:** It gives the two MADs (fall = 2.8, spring = 2.6). It refers to "the difference in means" but doesn't give the means. Those would come from a data display (a table or dot plot of cookie counts) that the item points to but that isn't shown here.

---

### Practices needed, in order

**1. Representing**
- Read the fall and spring data from the display they're given in (table, dot plot, or list), so each data set can be worked with as numbers.
- Turn the words "difference in means as a multiple of the larger MAD" into a symbolic setup: |mean_fall − mean_spring| ÷ MAD_larger.

**2. Abstracting and Generalizing**
- Know what the MAD is: a measure of variability that works as a "unit" for comparing the gap between two distributions.
- Compare 2.8 and 2.6 to pick the larger MAD (2.8, the fall data).
- See that the task follows a general pattern for comparing two data distributions: (difference in centers) ÷ (measure of spread).

**3. Procedural Fluency (NRC)**
- Find each mean: add the values and divide by how many there are.
- Subtract to get the difference in means (as an absolute value).
- Divide that difference by 2.8.
- Round correctly to the hundredths place.

**4. Justifying and Proving (light, optional)**
- Check that the answer makes sense. A result below about 1 means the distributions overlap a lot. A larger multiple means the difference between seasons is more meaningful. This check also helps confirm that the right MAD (the larger one) was used.

**Not needed:** Mathematical Modeling, since the data are already given and there's no real-world situation to turn into a model. Collaborative Mathematics, since it's an individual item.

---

**Summary order:** Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving, as a check)

**Core practices:** Representing, Abstracting and Generalizing, and Procedural Fluency. The heaviest load falls on Procedural Fluency (finding the means, dividing, and rounding) and on Abstracting (choosing the larger MAD and understanding the "multiple of the MAD" comparison).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why this one:**
- Most of the work, and most of the ways to get it wrong, are computational:
  - Find the two means from the data. This means adding the values and dividing, which is where most errors happen.
  - Subtract the means.
  - Divide by 2.8.
  - Round to the hundredths place.
- The problem tells students exactly what to do: "express the difference in means as a multiple of the larger MAD." So there is little real choosing or interpreting left.
- The conceptual step of picking the larger MAD is just comparing 2.8 with 2.6. That's simple.
- The answer is a single number to the hundredths, so the item really tests whether the student can carry out the steps accurately.

**Runner-up:** Abstracting and Generalizing. It covers understanding the MAD as a unit for comparing two distributions. But the problem states that framing outright, so students don't have to come up with it themselves.

---

## Row 208 (problem_id 99606)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the mean number of cookies sold in the spring.
____
```

### Answer 1: practices in order

**Practices used (2026 NAEP Mathematics Framework, plus NRC procedural fluency)**

The NAEP 2026 framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added the NRC strand **Procedural Fluency** as a sixth.

Problem: *"Find the mean number of cookies sold in the spring."* The problem refers to a data display (a table, bar graph, or pictograph of cookie sales by month or season) that wasn't included in the text, so I'm assuming the spring values are read from that display.

**Order of practices**

1. **Representing** (primary). Read the data display and pull out the right values: find the "spring" months or entries, read each count correctly (watch the scale or pictograph key), and write those numbers down as a list. This step moves information from a visual or tabular form into numbers you can work with. Most errors on this item come from here: picking the wrong season, misreading the scale, or leaving out a month.

2. **Procedural Fluency** (NRC). Run the mean procedure accurately: add the spring values, then divide the total by how many values there are. Getting the right answer depends on doing the multi-digit addition and the division correctly and quickly.

3. **Justifying and Proving** (light, optional). Check that the answer makes sense. The mean has to fall between the smallest and largest spring values. If the answer comes out as a non-whole number, decide whether it's acceptable, since an average of cookie counts can be a decimal.

**Not meaningfully involved**
- Abstracting and Generalizing: no general pattern or rule has to be found.
- Mathematical Modeling: the context is only a label. There's no real-world situation to simplify or model, because you're told directly to compute the mean.
- Collaborative Mathematics: it's an individual item.

**Summary sequence:** Representing → Procedural Fluency → (Justifying and Proving as a reasonableness check)

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

In my last answer I called Representing the "primary" practice, because it comes first and causes many of the errors. If you want the single practice that best describes the item, I'd pick **Procedural Fluency**. Here's why:

- **The item is about computing a mean.** The question says "find the mean." What it really tests is whether the student knows the mean procedure (add the values, divide by how many there are) and does it correctly.
- **Reading the data is basic here.** Pulling the spring values out of a table or graph is a short retrieval step. The student doesn't have to build a representation, switch between representations, or interpret one in any depth. Representing is needed, but it isn't what the item is designed to measure.
- **No other practice plays a real role.** There's no pattern to generalize, no argument to make, and no real-world model to set up. The context is only a label.

**Caveat:** If the display is hard to read (an odd scale, a pictograph key with half-symbols, or seasons the student has to work out from month names), Representing becomes a bigger part of the challenge. It could then be a close second, or even the main practice. For a typical version of this item, though, Procedural Fluency is the main practice.

---

## Row 210 (problem_id 101254)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Here are several recipes for sparkling lemonade. For each recipe, describe how many tablespoons of lemonade mix it takes per cup of sparkling water.
1/2 tablespoon of lemonade mix and 3/4 cups of sparkling water.
____ tablespoons lemonade mix per cup of sparkling water
Write your answer as a fraction.
```

### Answer 1: practices in order

## The practices available

**NAEP Mathematics Framework (2026) – Mathematical Practices**
1. **Representing** – making, interpreting, and moving between representations (symbols, tables, diagrams, words).
2. **Abstracting and Generalizing** – finding structure and patterns and extending them to general rules.
3. **Justifying and Proving** – building and evaluating mathematical arguments.
4. **Mathematical Modeling** – using math to represent and analyze a real-world situation, then interpreting the result in context.
5. **Collaborative Mathematics** – working with others to make sense of problems and solve them.

**Added from the NRC (*Adding It Up*) strands**
6. **Procedural Fluency** – carrying out procedures (here, fraction operations) flexibly, accurately, and efficiently.

---

## The problem

> 1/2 tablespoon of lemonade mix for 3/4 cup of sparkling water. How many tablespoons of mix per **one** cup of water? (Answer as a fraction.)

---

## Practices needed, in order

### 1. Mathematical Modeling (set up the model)
Read the recipe as a real-world ratio and see that "tablespoons per cup" is a **unit rate**. To get it, you divide the amount of mix by the amount of water:

rate = (tablespoons of mix) ÷ (cups of water)

This step turns the recipe into a math question.

### 2. Representing (write it in symbols)
Write the situation as a ratio or complex fraction:

(1/2) : (3/4)  →  (1/2) / (3/4)

You could also picture it with a double number line or table: 1/2 tbsp ↔ 3/4 cup, ? tbsp ↔ 1 cup.

### 3. Procedural Fluency (NRC) (do the calculation)
Divide the fractions with the multiply-by-the-reciprocal procedure:

(1/2) ÷ (3/4) = (1/2) × (4/3) = 4/6 = **2/3**

Write the result in lowest terms, since the answer must be a fraction.

### 4. Mathematical Modeling (interpret and check), plus light Justifying
Put the number back into context: **2/3 tablespoon of mix per cup of sparkling water.**
Check that it makes sense: 3/4 cup is less than 1 cup, so a full cup needs a bit *more* than 1/2 tbsp, and 2/3 > 1/2 ✓. Another check: (2/3)(3/4) = 1/2 ✓.

---

## Summary

| Order | Practice | Role in this problem | Weight |
|---|---|---|---|
| 1 | Mathematical Modeling | Recognize that "per cup" means a unit rate, mix ÷ water | High |
| 2 | Representing | Write the ratio as (1/2)/(3/4) or as a double number line | Medium-High |
| 3 | Procedural Fluency (NRC) | Fraction division, simplify to 2/3 | **High (main practice)** |
| 4 | Modeling (interpret), Justifying | State 2/3 tbsp per cup and check it is reasonable | Low-Medium |
| — | Abstracting & Generalizing | Not really needed (only one recipe, no general rule asked for) | Low |
| — | Collaborative Mathematics | Not used (an individual item) | None |

**Answer: 2/3 tablespoons of lemonade mix per cup of sparkling water.**

### Answer 2: major practice

## Major practice: **Procedural Fluency (NRC)**

**Why this one:**

- **Most of the difficulty is in the calculation.** The context is simple and the problem says outright what to find ("tablespoons per cup of sparkling water"), so turning the situation into mix ÷ water takes little modeling. The step where students actually make mistakes is computing (1/2) ÷ (3/4). They might flip the wrong fraction, multiply straight across to get 3/8, divide in the wrong order to get 3/2, or forget to simplify 4/6 to 2/3.
- **The answer format points to the computation.** "Write your answer as a fraction" means a correct, simplified fraction-division result is what gets scored.
- **The other practices play supporting roles.** Modeling and Representing only set up one standard expression, and interpreting the result is a quick check. None of them is where the item tells skilled students apart from unskilled ones.

**Runner-up:** Mathematical Modeling, since the student has to see that "per cup" means a unit rate and divide in the right order (mix ÷ water, not water ÷ mix). But the problem's wording does most of that work, so it ranks second.

**Answer:** (1/2) ÷ (3/4) = (1/2) × (4/3) = **2/3 tablespoon of mix per cup of sparkling water.**

---

## Row 212 (problem_id 105377)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Use the graph to determine how much total rain fell on Tuesday.
____ cm
```

### Answer 1: practices in order

The NAEP Mathematics Framework lists five mathematical practices. I've added "procedural fluency" from the NRC's *Adding It Up* strands as a sixth:

1. **Representing** – translating between graphs, tables, symbols, words and diagrams, and reading information from them.
2. **Abstracting and Generalizing** – finding patterns, structure and general rules.
3. **Justifying and Proving** – building or judging arguments for why something is true.
4. **Modeling** – using math to represent and analyze a real-world situation.
5. **Mathematical Problem Solving** – making sense of a problem, choosing a strategy, carrying it out and checking the result.
6. **Procedural Fluency (NRC)** – carrying out procedures such as computation and reading a scale accurately, efficiently and flexibly.

**Problem:** "Use the graph to determine how much total rain fell on Tuesday. ____ cm"

The graph isn't included, so I'm assuming a typical setup. It is probably a bar graph or line graph of rainfall over time, maybe broken into parts of the day or into several readings for Tuesday. "Total" suggests you may need to add several values.

### Practices needed, in order

**1. Mathematical Problem Solving (light, at the start)**
- Work out what the question asks: the *total* rainfall for *one day* (Tuesday), in cm.
- Plan the steps: find Tuesday on the graph, read the value or values, and add them if there is more than one.
- Since the steps are simple, this practice plays a small role.

**2. Representing (main practice)**
- Read the graph: find the axes, labels, scale and key, then locate the Tuesday bar(s) or point(s).
- Turn the visual (bar height or point position) into numbers in cm. This may mean reading between gridlines or working out what each scale interval is worth (e.g., each gridline = 0.5 cm).
- This is the core of the task: getting quantities out of a graphical representation.

**3. Procedural Fluency (NRC)**
- Read the scale correctly and work out values that fall between gridlines.
- If there are several Tuesday readings (morning, afternoon, evening, or hourly), add them correctly, often with decimals.
- Write the final value with the right unit (cm).

**4. Mathematical Problem Solving (optional final check)**
- Check that the total makes sense against the graph. For example, it should be at least as big as the largest single Tuesday reading.

### Practices not needed (or barely needed)
- **Abstracting and Generalizing**: there is no pattern or general rule to find.
- **Justifying and Proving**: no explanation or argument is asked for.
- **Modeling**: the data is already shown on the graph, so the student doesn't have to build a model of a real situation.

### Summary order
**Problem Solving (understand the goal) → Representing (read Tuesday's values from the graph) → Procedural Fluency (scale reading and adding) → Problem Solving (check if it makes sense)**

Representing is the main practice, Procedural Fluency comes second, and Problem Solving plays a light role at the start and end.

### Answer 2: major practice

**Major practice: Representing**

Why:
- The problem says "Use the graph to determine...". Everything depends on reading the graph correctly: finding Tuesday, understanding the scale, and turning bar heights or point positions into numbers in cm.
- Most errors would come from misreading the graph. Examples are using the wrong day, misjudging the scale interval, or reading between gridlines incorrectly. Arithmetic slips are less likely.
- The other practices play a smaller role. Procedural Fluency covers any simple addition and the scale arithmetic. Problem Solving is only a short step to understand the goal and check the answer.

If the graph has several Tuesday readings that must be added, Procedural Fluency matters more. Even then, it comes second to Representing.

---

## Row 215 (problem_id 21866)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
What percentage of the students have more than one child in the family?
____ %
[Image: A dot plot that shows the number of children. Goes from 0 to 6 by 1's. Starting at 0, the number of dots above each increment is 0, 5, 7, 5, 2, 1, 0.]
```

### Answer 1: practices in order

**Answer: 75%**

The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I added Procedural Fluency from the NRC's *Adding It Up* strands as a sixth.

The problem needs three of them, in this order.

**1. Representing (read the dot plot)**
- Turn the dots into a frequency table:

| Children | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Students | 0 | 5 | 7 | 5 | 2 | 1 | 0 |

- Each dot is one student. The x-axis value is how many children are in that student's family.

**2. Abstracting and Generalizing (turn the words into a set and a ratio)**
- "More than one child" means the values 2, 3, 4, 5 and 6. It does not include 1. This strict reading of "more than" is the most likely place to go wrong.
- "Percentage of the students" means (number of students in that set) ÷ (total number of students) × 100.

**3. Procedural Fluency (NRC): count and compute**
- Total students: 5 + 7 + 5 + 2 + 1 = 20
- Students with more than one child: 7 + 5 + 2 + 1 + 0 = 15 (or 20 − 5 = 15)
- 15 / 20 = 0.75, which is **75%**

**Not needed:** Justifying and Proving (no argument is asked for), Mathematical Modeling (the data are already given as a clean representation, so there is no real-world situation to model), and Collaborative Mathematics (this is an individual task).

**Order:** Representing, then Abstracting and Generalizing, then Procedural Fluency.

### Answer 2: major practice

**Major practice: Representing**

- **It is the core demand.** All of the information is in the dot plot. The student has to read it as a frequency distribution: each dot is one student, and its x-value is that student's number of children. Without that reading, nothing else can start.
- **The arithmetic is easy.** Adding five small numbers and turning 15/20 into 75% is routine grade 6–7 work. Procedural Fluency is needed, but it is not what makes the item hard.
- **The abstraction step is small.** Reading "more than one" as 2 or more is a quick interpretation, and it is applied directly to the plot. It belongs to reading the data display correctly, not to a separate generalizing task.

The typical mistakes are miscounting dots, reading the height of a column as the value, or including the "1" column. All of these are failures to read the plot correctly, which makes Representing the main practice.

---

## Row 217 (problem_id 108574)

- **predicted_practice:** Abstracting and Generalizing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
What value could you write in after 3x that would make the equation true for all values of x?
3x + 8 = 3x +
____
```

### Answer 1: practices in order

**Answer: 8** (so the equation reads 3x + 8 = 3x + 8)

**Practices available.** The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. You asked me to add **Procedural Fluency** from the NRC's *Adding It Up* strands, so I've included it too.

**Practices used, in order:**

1. **Representing.** Read the symbolic equation 3x + 8 = 3x + __ and see what the blank stands for: a constant that completes the right-hand side. Both sides already have the same 3x term, so the blank decides how the two expressions compare.

2. **Abstracting and Generalizing (the key practice).** Notice that "true for all values of x" means the equation has to be an identity, not something solved for one value of x. An identity needs the two sides to be the same expression. The x-terms already match (3x and 3x), so the constants must match as well.

3. **Procedural Fluency (NRC).** Do the quick symbolic step. Subtract 3x from both sides to get 8 = __, so the blank is 8. (Any other number c leaves 8 = c, which is false for every x, so the equation would have no solution.)

4. **Justifying and Proving (brief check).** Confirm that 3x + 8 = 3x + 8 holds whatever x is, because both sides are the same expression. You can test a value or two if you like (for example, x = 0 gives 8 = 8, and x = 5 gives 23 = 23). This also explains why 8 is the only value that works.

**Not used:** Mathematical Modeling, because there's no real-world situation to model, and Collaborative Mathematical Discourse, because this is an individual item.

**Summary of order:** Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving. Abstracting and Generalizing does the main work, since the student has to recognize that "for all x" means the two sides must be identical.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

The hard part of this item is understanding what "true for all values of x" asks for. It isn't asking you to solve for one x. It's asking you to make the equation an identity, which means the two sides have to be the same expression. Once you see that, the answer (8) is obvious: the 3x terms already match, so the constants must match too.

The other practices play smaller roles:
- **Procedural Fluency:** the only computation is subtracting 3x from both sides to get 8 = __, which is trivial.
- **Representing:** reading the equation is routine.
- **Justifying and Proving:** checking a value or two is an optional confirmation.

A student who gets this wrong almost always does so by misunderstanding the "for all x" condition, not by making an arithmetic or reading error. That makes Abstracting and Generalizing the practice the item really measures.

---

## Row 218 (problem_id 111092)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of 2 5/8 ÷ 1/2
____
```

### Answer 1: practices in order

**Problem:** Find the value of 2 5/8 ÷ 1/2

**Answer:** 5 1/4 (or 21/4)

## Practices available

NAEP 2026 Mathematics Framework practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC (*Adding It Up*): **Procedural Fluency**, meaning carrying out procedures flexibly, accurately and efficiently.

## Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Rewrites the mixed number 2 5/8 as the improper fraction 21/8. Rewrites the division as multiplication by the reciprocal: 21/8 × 2/1. Converting between equivalent forms of a number and an operation is what Representing means here. |
| 2 | **Procedural Fluency (NRC)** | Does the steps: 21/8 × 2 = 42/8, which simplifies to 21/4, which converts back to 5 1/4. This is the main practice for this item. It is a standard fraction-division procedure. |
| 3 | **Justifying and Proving** (minor, optional) | Checks that the answer makes sense. Dividing by 1/2 means asking how many halves are in the number, which is the same as doubling it. 2 × 2 5/8 = 5 2/8 = 5 1/4, so the answer is right. A student who sees this relationship has used some **Abstracting and Generalizing** (the rule that dividing by 1/2 is the same as multiplying by 2). |

## Practices not used

- **Mathematical Modeling:** there is no real-world situation to model. The problem is just a number expression.
- **Collaborative Mathematics:** it is a single-student item with a short answer.
- **Abstracting and Generalizing:** only needed if the student uses the "dividing by 1/2 doubles the number" shortcut. The standard procedure does not need it.

## Summary order

**Representing → Procedural Fluency → (Justifying and Proving, optional check)**

Procedural Fluency carries most of the weight. Representing is needed first to set up the computation.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:

- The item is a bare expression, 2 5/8 ÷ 1/2. There is no context to model, nothing to prove, and no pattern to generalize. It asks only for a value.
- Solving it means running a standard algorithm: convert the mixed number to 21/8, multiply by the reciprocal to get 21/8 × 2 = 42/8, then simplify to 21/4, which is 5 1/4. Doing that accurately and efficiently is what Procedural Fluency means.
- Representing (changing the mixed number to an improper fraction, and rewriting division as multiplication) is part of that same procedure. It is a step within the computation, not a separate kind of thinking the item is testing.
- The most likely errors are procedural slips: forgetting to convert the mixed number, inverting the wrong fraction, or multiplying instead of dividing to get 1 5/16. Those are fluency errors.

If you can only pick from the NAEP practices, I would choose **Representing**, since the main thing done before computing is rewriting into equivalent forms. With the NRC option included, Procedural Fluency is the clear major practice.

---

## Row 220 (problem_id 112497)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the value of the expression below.
(-8) · (-2/3)
____
```

### Answer 1: practices in order

**Problem:** Find the value of (-8) · (-2/3)

**Answer:** 16/3 (also written 5 1/3, or about 5.33)

---

### The practices available

The NAEP 2026 Mathematics Framework lists five practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

I've added **Procedural Fluency** from the NRC's *Adding It Up* strands as a sixth.

### Practices used, in order

**1. Representing (first, and brief)**
The student reads the notation correctly:
- The dot "·" means multiplication.
- The parentheses mark two negative numbers.
- -2/3 is one negative fraction.
- The whole number -8 can be written as the fraction -8/1, so both numbers are in the same form.

**2. Procedural Fluency (the main practice)**
The student carries out the steps accurately:
- **Sign rule:** a negative times a negative is a positive, so the answer is positive.
- **Multiply:** 8 × 2/3 = (8 × 2)/3 = 16/3.
- **Simplify:** 16/3 is already in lowest terms. If a mixed number is wanted, it is 5 1/3.

**3. Justifying and Proving (optional, small)**
A quick check that the answer makes sense:
- Two negatives give a positive.
- 2/3 of 8 should be a bit more than 5. 16/3 ≈ 5.33 fits.

This step is not required to get the answer, but a careful student would do it.

### Practices not used

- **Abstracting and Generalizing:** The student only applies a rule they already know ("negative × negative = positive"). They are not forming or extending a general rule.
- **Mathematical Modeling:** There is no real-world situation to turn into math.
- **Collaborative Mathematics:** This is an individual item.

### Summary

**Representing → Procedural Fluency → (Justifying and Proving, as a check)**

Procedural Fluency carries almost all the weight. The core skill is the sign rule for multiplication plus multiplying a whole number by a fraction.

### Answer 2: major practice

**Major practice: Procedural Fluency**

**Why:**
- **The item tests computation.** The student only has to multiply two signed rational numbers. There is no real-world context, nothing to prove, and no pattern to generalize.
- **The work is mostly following known steps.** The student applies the sign rule (negative × negative = positive), multiplies 8 × 2/3 to get 16/3, and checks that the fraction is in lowest terms.
- **The other practices play a small part.** Representing is only reading the notation, which takes a moment. Justifying is an optional check at the end.
- **Mistakes on this item are almost always procedural.** Students get the sign wrong, multiply the denominator too (16/24), or simplify incorrectly.

If I had to pick only from the five NAEP practices, I would choose **Representing**, because it is the only one with a real role here. But it is a weak fit, and Procedural Fluency is clearly the main practice.

---

## Row 221 (problem_id 112290)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the value of the expression below.
(-8) · (2/3)
____
```

### Answer 1: practices in order

**Problem:** Calculate (-8) · (2/3). Answer: **-16/3** (also written -5 1/3 or about -5.33)

The NAEP Mathematics Framework lists these mathematical practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, and (5) Collaborative Mathematics. I've added **Procedural Fluency** from the NRC's *Adding It Up* strands, as you asked.

This is a plain computation with no context. Most NAEP practices don't really apply. Here are the practices in the order they're used:

### 1. Representing (minor, comes first)
- Read the symbolic expression and see what it asks for: a negative integer times a positive fraction.
- Treat -8 as the fraction -8/1 so it has the same form as 2/3. This is a small change of representation that sets up the procedure.

### 2. Procedural Fluency (NRC), the main practice
- **Sign rule:** a negative times a positive gives a negative, so the answer will be negative.
- **Multiply the fractions:** (-8/1) · (2/3) = (-8 · 2)/(1 · 3) = -16/3.
- **Simplify or convert:** 16 and 3 share no common factor, so -16/3 is in lowest terms. You can also write it as the mixed number -5 1/3 if asked.
- Doing this accurately and efficiently is what the item really tests.

### 3. Justifying (light, optional check at the end)
- Check that the answer makes sense. 2/3 of 8 is a bit more than 5, so the size should be about 5.3. The negative sign matches the sign rule. This is a quick estimate check, not a formal proof.

### Not used
- **Abstracting and Generalizing:** nothing needs to be generalized. The sign rule is applied, not derived.
- **Mathematical Modeling:** there is no real-world situation to model.
- **Collaborative Mathematics:** not relevant to a single-answer item done alone.

**Order: Representing → Procedural Fluency → (Justifying as a check)**

Procedural Fluency does almost all of the work here. Representing and Justifying play only small supporting roles.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- The item gives you a fully symbolic expression, (-8) · (2/3), and asks only for its value. There is nothing to model, generalize, or prove, and no context to translate.
- Solving it is carrying out a known procedure correctly: apply the sign rule (negative × positive = negative), multiply the integer by the fraction ((-8 · 2)/3 = -16/3), and check that the result is in simplest form.
- The likely mistakes are all procedural slips: getting the sign wrong, multiplying both numerator and denominator by 8, or dividing instead of multiplying. That shows what the item really measures.

Representing (writing -8 as -8/1) and Justifying (estimating about -5.3 as a check) play only small supporting roles. Procedural Fluency is clearly the main practice.

**Answer: -16/3 (= -5 1/3)**

---

## Row 222 (problem_id 112797)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the value of the expression below.
18/(-3)
____
```

### Answer 1: practices in order

**Problem:** Calculate 18 / (-3).

This is a one-step computation with integers. Most of the work is done by a single practice, and a light reasoning check comes before it.

The NAEP Mathematics framework lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. NAEP also describes "mathematical complexity" levels. To these I add Procedural Fluency from the NRC strands.

### Practices needed, in order

1. **Representing (minor, quick)**
   - Read the notation correctly. "18/(-3)" means 18 divided by negative 3. The parentheses mark the sign of the divisor and are not a separate operation.
   - This is only a light step: you read the symbols and turn them into the operation to carry out.

2. **Abstracting and Generalizing (minor): use the sign rule**
   - Recall the general rule for dividing signed numbers: a positive divided by a negative gives a negative.
   - Using a general rule here, instead of working out a special case, is the abstract/general part. The student knows that the rule for signs in multiplication also applies to division.

3. **Procedural Fluency (NRC), the main practice**
   - Divide the absolute values: 18 / 3 = 6.
   - Attach the sign from step 2 to get **-6**.
   - This is the main practice. The problem is a routine calculation that tests whether the student can carry out integer division quickly and correctly.

4. **Justifying (optional, minor): check the answer**
   - Check with the inverse operation: (-6) x (-3) = 18. This confirms both the size and the sign.
   - A strong student may do this. The item does not require it.

### Not used
- **Mathematical Modeling**: there is no real-world situation.
- **Collaborative Mathematical Discourse**: it is an individual computation item.
- **Justifying and Proving** in the formal sense: no explanation is asked for. The check in step 4 is only informal self-checking.

### Summary
| Order | Practice | Role |
|---|---|---|
| 1 | Representing | Read 18/(-3) as division by a negative number |
| 2 | Abstracting and Generalizing | Apply the sign rule (+ / - = -) |
| 3 | **Procedural Fluency (NRC)** | Compute 18 / 3 = 6 and attach the sign to get -6 (main practice) |
| 4 | Justifying (optional) | Check: (-6)(-3) = 18 |

**Answer: -6**

**Main practice:** Procedural Fluency. NAEP would rate this item low on mathematical complexity.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item says "Calculate the value of the expression." It is a plain integer division with no context, no representation to build, no argument to make, and no pattern to generalize.
- The student succeeds by carrying out a known procedure correctly: divide 18 by 3 to get 6, then use the sign rule (positive / negative = negative) to get **-6**.
- The sign rule is a memorized rule applied as part of that procedure, so it falls under procedural fluency here. It is not real abstracting or generalizing.
- Representing (reading the notation) and checking the answer are small supporting steps. Neither is what the item really tests.

So if only one practice can be chosen, it is **Procedural Fluency**.

---

## Row 223 (problem_id 112511)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is the coefficient of the variable?
____
```

### Answer 1: practices in order

**Note:** The problem as given ("What is the coefficient of the variable? ____") doesn't include the term or expression itself. It was probably an image that didn't come through. The practice sequence below applies to any expression of this kind, for example a term like 7x or an expression like 4 + 9n. I use 7x as the example.

### Practices used for this problem

NAEP Mathematics names five mathematical practices (Mathematical Reasoning, Mathematical Representation, Mathematical Modeling, Mathematical Communication, and Collaborative Mathematical Thinking). I've added **Procedural Fluency** from the NRC (*Adding It Up*) strands, as you asked.

This is a short recall-and-identify item, so only a few practices are involved.

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Representation** (NAEP) | Reads the symbolic expression and works out its parts: which symbol is the variable (x), which number is attached to it by multiplication (7), and which parts are constants or other terms. They need to know that "7x" means 7 · x. Edge cases fall here too: a bare "x" means 1·x, "−x" means −1·x, and "x/3" means (1/3)·x. |
| 2 | **Procedural Fluency** (NRC) | Uses the routine rule quickly and accurately: the coefficient is the numerical factor multiplying the variable. They pull out that number with its sign (7, or −1 in the "−x" case) and ignore any constant term. |
| 3 | **Mathematical Communication** (NAEP), minor | Writes the answer in the correct form: just the number (7), not "7x" and not "x". This means using the term "coefficient" correctly and not mixing it up with "constant", "term", or "variable". |

### Practices not really involved
- **Mathematical Reasoning**: there's nothing to justify, generalize, or infer. Recognizing the coefficient is a matter of definition. A small amount of reasoning only shows up in edge cases (implicit 1, negative sign, a fractional coefficient).
- **Mathematical Modeling**: there's no real-world context to turn into math.
- **Collaborative Mathematical Thinking**: this is a single-answer item done alone.

### Summary order
**Representation → Procedural Fluency → (Communication)**

The main practice is **Procedural Fluency**, together with **Representation** (reading the symbolic form).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

This item checks whether the student can quickly and accurately use a routine rule they already know: find the number multiplying the variable and write it down. There's no context to model and nothing to justify. Communicating the answer is trivial.

Representation (reading "7x" as 7 · x) is a close second, because the student has to read the symbolic form correctly first. That reading is part of applying the rule, though, not a separate challenge. A student who misses this item has most likely not mastered the "coefficient = numerical factor" procedure, including the implicit 1 and the sign. That points to procedural fluency as the main practice.

---

## Row 224 (problem_id 115723)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Use the sample space to determine the probability that a fifth person would get the same outcome as person 1.
____
```

### Answer 1: practices in order

**Note on the problem:** The text refers to a sample space and to "person 1's outcome," but neither is included here. It probably came with a table, list or tree diagram (for example, outcomes of coin flips or spinner spins for persons 1–4). The practice sequence below doesn't depend on those details. The final number does.

**Practices available.** NAEP Mathematics (2026 framework) lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added NRC **Procedural Fluency**.

### Practices needed, in order

1. **Representing (NAEP)** (main practice)
   - Read the given sample space (list, table or tree) and understand what each entry stands for: one possible equally likely outcome of the experiment.
   - Find person 1's outcome in that representation.

2. **Mathematical Modeling (NAEP)** (supporting, light use)
   - Treat the fifth person as a new, independent run of the same chance experiment.
   - Assume all outcomes in the sample space are equally likely, so theoretical probability applies: P = favorable outcomes / total outcomes.

3. **Procedural Fluency (NRC)** (main practice)
   - Count the total number of outcomes in the sample space.
   - Count how many of them match person 1's outcome. Usually that's 1, unless the outcome is defined in a way that several entries satisfy, such as "two heads" in any order.
   - Write the probability as a fraction and simplify it, e.g. 1/8 if the sample space has 8 equally likely outcomes.

4. **Justifying and Proving (NAEP)** (optional, light use)
   - Briefly check that the answer makes sense: what persons 1–4 got doesn't change the fifth person's probability, because each trial is independent, and the value is between 0 and 1.

**Not needed:** Abstracting and Generalizing (no general rule or pattern is asked for) and Collaborative Mathematics (this is an individual item).

**Summary of order:** Representing → Mathematical Modeling → Procedural Fluency → (Justifying and Proving)

The core of the item is Representing (reading the sample space) followed by Procedural Fluency (counting and forming the ratio).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The sample space is already given. The student doesn't build or change a representation; they only read it. So Representing plays a part, but a small one.
- Most of the work is a standard procedure:
  1. Count all the outcomes.
  2. Count the outcomes that match person 1's.
  3. Write P = favorable / total and simplify.

  Getting this right depends on doing that routine accurately.
- No model needs to be built and no argument is required, so Modeling and Justifying play only minor roles.

**Runner-up:** Representing (NAEP). It would be the major practice if the student had to build the sample space themselves, for example by drawing a tree diagram or listing outcomes, rather than using one that is given.

---

## Row 226 (problem_id 115027)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Teachers held a basketball shooting contest. Their goal was to make 60 baskets. For the teacher, determine what percentage of the goal they achieved.
Teacher D made 9 baskets.
____ %
```

### Answer 1: practices in order

**Problem:** The goal is 60 baskets. Teacher D made 9. What percentage of the goal did Teacher D reach?

**Practices to use:** the five NAEP mathematical practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematical Discourse) plus NRC *procedural fluency*. Only some of them are needed here, in this order:

1. **Mathematical Modeling (NAEP):** Turn the story into math. "Percentage of the goal achieved" means *part ÷ whole × 100*. The part is the baskets made (9) and the whole is the goal (60).

2. **Representing (NAEP):** Write the relationship as a fraction or proportion: 9/60 = x/100. You can also simplify it first: 9/60 = 3/20.

3. **Procedural Fluency (NRC):** Do the calculation correctly and efficiently:
   - 3/20 = 15/100 (multiply the top and bottom by 5), or
   - 9 ÷ 60 = 0.15, and 0.15 × 100 = 15.
   - **Answer: 15%**

4. **Justifying (NAEP), a light check:** See whether the answer makes sense. 10% of 60 is 6, and 5% is 3, so 15% is 6 + 3 = 9. That matches. The answer is also well under 100%, which fits making far fewer baskets than the goal.

**Not really needed:** Abstracting and Generalizing (you don't need a general rule from one case) and Collaborative Mathematical Discourse (this is a solo, single-answer item).

**Order:** Mathematical Modeling, then Representing, then Procedural Fluency, then Justifying (an optional check).

**Main practice:** Procedural Fluency. The modeling step is small because "percentage of the goal" points straight to part/whole. The work is mostly finding the fraction and changing it to a percent.

**Answer: 15 %**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:** Setting up the problem takes almost no thought. "What percentage of the goal" points straight to part ÷ whole, which is 9/60. Students rarely get this item wrong because of the setup. They get it wrong because they can't turn 9/60 into a percent: they can't simplify it to 3/20, rescale it to 15/100, or divide 9 by 60 to get 0.15 and then multiply by 100. That conversion is the core of the item, and it is procedural fluency.

Mathematical Modeling and Representing are each one short step at the start, and the Justifying check is optional. So if I can pick only one practice, it is **Procedural Fluency**.

---

## Row 229 (problem_id 117528)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is the common value?
____
```

### Answer 1: practices in order

**A caveat first:** the problem text is only "What is the common value? ____". The figure, table, or set of expressions it refers to isn't included. So the sequence below is based on the most likely form of this item: several representations (expressions, fractions, a table, or points) that all equal one value, and the student finds that value.

**Practices available:**
- NAEP Mathematics Framework practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Problem Solving.
- NRC strand added as you asked: Procedural Fluency.

**Practices to use, in order:**

1. **Representing.** Read and interpret the given representations: the expressions, figure, or table. Then translate them into a form you can work with, such as numbers or equations to evaluate or set equal.

2. **Procedural Fluency (NRC).** Carry out the routine calculations accurately and efficiently. Depending on the format, that means evaluating each expression, simplifying fractions, substituting values, or solving the equation that makes the quantities equal.

3. **Abstracting and Generalizing.** Notice that the results share one value, and state that value as the answer. This means recognizing the invariant that ties the representations together.

4. **Justifying and Proving (optional, light).** Check that the value really works for every given quantity, not just one or two. The item doesn't ask for a written justification, so this step is a self-check only.

**Not used:** Mathematical Modeling (there is no real-world situation to model) and Collaborative Problem Solving (this is an individual item).

**Core sequence:** Representing → Procedural Fluency → Abstracting and Generalizing, with an optional Justifying check at the end. If you can share the figure or expressions the item refers to, I can tighten this ordering.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC).**

Most of the work in this item is computation. The student has to evaluate or simplify each given quantity, or solve for the value that makes them equal, and get it right. Once those calculations are done, spotting the shared value is nearly automatic. So accurate, efficient procedures are what decide whether the student answers correctly.

The other practices play smaller roles:
- **Representing** comes first, but it is a light step: reading off the given expressions or table.
- **Abstracting and Generalizing** is real but thin here: the student only has to notice that the results match.

One caveat: the item's figure or expressions weren't included. If they turn out to be in different forms that must be connected before any calculation (for example a graph, a table, and an equation), Representing would become the major practice.

---

## Row 230 (problem_id 117994)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Calculate the quotient of 109.2 ÷ 6 using any method of your choice.
____
```

### Answer 1: practices in order

**Problem:** Calculate 109.2 ÷ 6 using any method you like. **Answer: 18.2**

The practice set is the five Mathematical Practices in the NAEP 2026 Mathematics Framework (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus **Procedural Fluency** from the NRC's *Adding It Up* strands.

### Practices used, in order

**1. Representing (choosing how to set up the division)**
"Any method" means the student first has to pick a representation of the problem. Examples are the long-division layout (6 into 109.2) or splitting the number by place value: 109.2 = 108 + 1.2. Both put the problem in a form that is easy to compute and keep the decimal point visible.

**2. Procedural Fluency (NRC): the main practice**
Next comes doing the division accurately and efficiently:
- With decomposition: 108 ÷ 6 = 18 and 1.2 ÷ 6 = 0.2, so 18 + 0.2 = **18.2**.
- With long division: 10 ÷ 6 = 1 r 4. Then 49 ÷ 6 = 8 r 1. Bring down the 2 after the decimal point and place the decimal point in the quotient: 12 ÷ 6 = 2. The result is **18.2**.
Most of the thinking in this item happens here: knowing the division facts, handling remainders and placing the decimal point correctly.

**3. Justifying and Proving (light use: checking the answer)**
To confirm the result, the student can multiply back (18.2 × 6 = 109.2) or estimate (110 ÷ 6 ≈ 18). This shows the quotient is reasonable and the decimal point is in the right place. It is optional and small, but it is the natural last step.

### Practices not used
- **Abstracting and Generalizing:** the student does not need to find a pattern or general rule.
- **Mathematical Modeling:** there is no real-world situation to turn into math.
- **Collaborative Mathematics:** this is an individual computation item.

### Summary
**Representing → Procedural Fluency → Justifying (checking)**. Procedural Fluency is the main practice. Representing is a short setup step, and Justifying is an optional check at the end.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item is a straight calculation: divide 109.2 by 6. It has no context to model, no pattern to generalize and no argument to make. What it tests is whether the student can do decimal division accurately and efficiently. That means knowing the division facts, handling remainders and putting the decimal point in the right place to get **18.2**.

Representing (choosing long division or splitting 109.2 into 108 + 1.2) and Justifying (checking that 18.2 × 6 = 109.2) only support that work. A student who gets the item wrong almost always makes a procedural mistake, such as misplacing the decimal point or getting a division fact wrong. So Procedural Fluency is the practice that decides success on this problem.

---

## Row 231 (problem_id 118176)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
The machine must be emptied to be serviced. If there are 40 bottles in the machine when it is to be serviced, what number will go in the second column in the table?
____
```

### Answer 1: practices in order

**Practices available (NAEP 2026 Mathematics Framework + NRC):**
- NAEP: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Problem Solving
- NRC (added): Procedural Fluency

**A note on the problem:** The item depends on a table and on rules about the machine (for example, how many bottles it holds, or how the table's columns relate) that aren't in the text you gave me. So the practice sequence below is based on how this kind of item usually works: a table that links the number of bottles in the machine to a related quantity, such as bottles to remove, bottles sold, or bottles needed to refill it. I can't give the actual number without the table.

**Practices, in the order they're used:**

1. **Representing** (main practice). First the student reads the table. They work out what the first and second columns stand for and how each row pairs a value in one column with a value in the other. Then they turn the situation ("40 bottles in the machine, and it must be emptied") into a table entry: 40 goes in the first column, and the unknown goes in the second.

2. **Abstracting and Generalizing** (supporting practice). Next the student looks at the rows already filled in to find the rule linking the columns. For example, "the second column is the number of bottles taken out, which equals the number in the machine," or "second column = capacity − first column." They then apply that rule to the new case of 40 bottles. Some items state the relationship outright in the text. If this one does, this step is small.

3. **Procedural Fluency** (NRC). Then the student applies the rule to 40 accurately. This is usually one simple operation: copying the value, or doing a subtraction or multiplication. They write the result in the blank.

4. **Representing** again (brief check). Finally, the student puts the answer back into the table and checks that it fits the other rows and makes sense for an emptied machine. For example, if the machine is emptied, nothing is left in it afterward.

**Practices not needed:** Justifying and Proving (no argument is asked for), Mathematical Modeling (the situation is already set up as a table), and Collaborative Problem Solving (this is a single-student item).

**Sequence:** Representing → Abstracting and Generalizing → Procedural Fluency → (Representing check)

If you share the table, I can work out the number and say for sure whether step 2 is needed.

### Answer 2: major practice

**Major practice: Representing**

Most of the work in this item is reading the table and translating between representations. The student has to:

- work out what each column stands for,
- turn the situation ("40 bottles, machine must be emptied") into the right row of the table,
- write the matching value in the second column.

Once the student understands the table, the calculation is trivial. It is most likely copying the number or doing one subtraction. Spotting the pattern across rows is also a small step. So the item mostly tests whether the student can read and work with the tabular representation, not their computation or generalizing.

One caveat: the table isn't in the text I have. If it turns out the second column needs a less obvious rule found from several rows, Abstracting and Generalizing would become a close second. Representing would still be the main practice.

---

## Row 232 (problem_id 118786)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the value of 61.12 ÷ 3.2.
____
```

### Answer 1: practices in order

**Problem:** Find the value of 61.12 ÷ 3.2.

**Answer: 19.1**

## Practices available

The NAEP Mathematics Framework (2026) lists these mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics (in the framework, but not assessed)

You asked me to add one more:
6. **Procedural Fluency** (NRC, *Adding It Up*): carrying out procedures flexibly, accurately, efficiently, and appropriately.

## Practices used, in order

**1. Representing (minor role)**
Change the problem into an equivalent form that is easier to work with. Multiply the dividend and the divisor by 10 so the divisor becomes a whole number:
61.12 ÷ 3.2 = 611.2 ÷ 32.
This is a change of symbolic representation. The quotient stays the same.

**2. Procedural Fluency (main practice)**
Do the long division accurately and put the decimal point in the right place:
- 61 ÷ 32 = 1, remainder 29
- Bring down 1: 291 ÷ 32 = 9, remainder 3 (32 × 9 = 288)
- Bring down 2, past the decimal point: 32 ÷ 32 = 1, remainder 0
- Quotient = **19.1**

Most of the problem's difficulty is here: the division algorithm and decimal place value.

**3. Justifying (light, optional)**
Check that the answer makes sense:
- Estimate: 60 ÷ 3 = 20, which is close to 19.1.
- Multiply back: 19.1 × 3.2 = 57.3 + 4.82... more exactly, 19.1 × 3 = 57.3 and 19.1 × 0.2 = 3.82, so 57.3 + 3.82 = 61.12. ✓

This is a quick self-check, not a formal proof. It only counts as a light use of Justifying and Proving.

## Practices not used
- **Abstracting and Generalizing:** no pattern or general rule needs to be found.
- **Mathematical Modeling:** there is no real-world context to model.
- **Collaborative Mathematics:** not part of a single-item assessment.

## Summary
**Representing → Procedural Fluency → (Justifying, as a check)**

This is mainly a **Procedural Fluency** item. Representing comes in only briefly, when you rewrite the problem with a whole-number divisor.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item is a bare calculation, 61.12 ÷ 3.2, with no context, no pattern and nothing to justify. The only task is to carry out decimal division correctly.
- Where students go wrong is procedural. They shift the decimal point in the divisor but not the dividend, misplace the decimal point in the quotient (1.91 or 191 instead of 19.1), or make a long-division error.
- Representing (rewriting the problem as 611.2 ÷ 32) is a standard step inside the decimal-division procedure. It isn't a separate act of choosing or translating between representations. Checking the answer is optional and isn't needed to get 19.1.

So if I had to pick one, it would be **Procedural Fluency**.

*Correction to my previous answer:* the multiply-back check had a garbled line ("57.3 + 4.82..."). The correct check is 19.1 × 3 = 57.3 and 19.1 × 0.2 = 3.82, so 57.3 + 3.82 = 61.12.

---

## Row 239 (problem_id 128141)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
A cube has edge length 11 inches.
Write an expression for its volume.
V = ____
```

### Answer 1: practices in order

**Problem:** A cube has edge length 11 inches. Write an expression for its volume. V = ____

**Answer:** V = 11³ (or 11 × 11 × 11), which is 1,331 cubic inches.

### Practices used, in order

The NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Procedural fluency comes from the NRC's *Adding It Up* strands. Only a few of these are needed for this problem.

1. **Representing (NAEP).** The student reads the words "cube with edge length 11 inches" and turns them into math: a cube has three equal dimensions, each 11. They then write the volume formula for a cube, V = s³, or length × width × height. This is the main practice here because the problem asks for an *expression*, which is a representation.

2. **Abstracting and Generalizing (NAEP), a small role.** The student uses the general rule (the volume of any cube is s³) and applies it to this case, s = 11. This only means recalling the general formula and plugging in a value, so it is light. Students who already know the formula may not notice they are using it.

3. **Procedural fluency (NRC).** The student substitutes correctly and writes the expression in a standard form: 11³ or 11 × 11 × 11. If they also evaluate it, they multiply quickly and correctly (11 × 11 = 121, then 121 × 11 = 1,331) and give the unit, cubic inches.

### Practices not needed

- **Justifying and Proving:** the student isn't asked to explain or prove anything.
- **Mathematical Modeling:** the context is just a label on a geometric figure. There's no real-world situation to simplify, model, or interpret.
- **Collaborative Mathematics:** this is a task done alone.

**Order in short:** Representing → (Abstracting/Generalizing, minor) → Procedural Fluency

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The problem asks the student to *write an expression* for the volume, not to work out a number. The main job is turning a verbal description ("a cube with edge length 11 inches") into a symbolic form: V = 11³, or 11 × 11 × 11. That translation is what Representing means, so it's where the problem succeeds or fails.

- A student who misreads the cube or uses the wrong formula fails at representing. Common slips are 11 × 3, 11², or 6 × 11², which is the surface area.
- Procedural fluency barely matters, because no calculation is required. Even if the student goes on to compute 1,331, that arithmetic is extra.
- Abstracting and Generalizing only means recalling the cube formula, which is too small a step to count as the major practice.

**Choice:** Representing

---

## Row 241 (problem_id 124672)

- **predicted_practice:** Abstracting and Generalizing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Polygon B is a scaled copy of Polygon A using a scale factor of 5. Polygon A’s area is what fraction of Polygon B’s area?
____
```

### Answer 1: practices in order

**Answer:** 1/25

**Practices available.** The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added Procedural Fluency from the NRC's *Adding It Up* strands, as you asked.

**Practices needed, in order:**

1. **Representing.** Turn the words into a relationship you can work with. "B is a scaled copy of A with scale factor 5" means every length in B is 5 times the matching length in A: L_B = 5·L_A. You can picture this with a simple stand-in, such as a 1×1 square scaled to a 5×5 square.

2. **Abstracting and Generalizing.** This is the key step. No polygon is given, so the student has to use the general rule rather than calculate one shape's area. When lengths scale by k, area scales by k², because area is two-dimensional and both dimensions grow by k. This holds for any polygon, so Area_B = 5²·Area_A = 25·Area_A.

3. **Procedural Fluency (NRC).** Do the arithmetic accurately: 5² = 25, then rewrite Area_A / Area_B = Area_A / (25·Area_A) = 1/25.

4. **Justifying and Proving** (a light check). Make sure the answer is sensible. A is the smaller polygon, so the fraction must be less than 1, which rules out 25. It is 1/25 and not 1/5 because area is two-dimensional. The 1×1 vs. 5×5 square example confirms it: 1 out of 25.

**Not needed:** Mathematical Modeling, since there is no real-world situation, and Collaborative Mathematics, since this is a single-student item.

**Main practice:** Abstracting and Generalizing. The most common mistake is answering 1/5, which happens when a student applies the length scale factor straight to area instead of squaring it.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

The problem never gives a specific polygon, side lengths, or area, so the student can't compute anything directly. To answer, they have to know and apply the general rule: if lengths scale by a factor k, area scales by k². That rule works for any polygon, which makes this step abstracting and generalizing.

The other practices are smaller parts of the solution:
- **Representing** is just reading "scale factor 5" as "lengths × 5," which is quick.
- **Procedural Fluency** is only 5² = 25 and writing the reciprocal, 1/25. That's minimal arithmetic.
- **Justifying** is an optional sense check.

The item also tests exactly this practice. Students who miss the generalization usually answer 1/5, because they apply the length scale factor directly to area. That wrong answer comes from failing at abstracting and generalizing, not from a procedural slip.

---

## Row 242 (problem_id 123193)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Find the scale factor from S to R.
____
```

### Answer 1: practices in order

**Problem:** "Find the scale factor from S to R." (The figure showing the two shapes S and R isn't included. In a problem like this they are usually two similar polygons on a grid or with side lengths labeled.)

## Practices used, in order

The NAEP mathematical practices (NAEP 2026 framework) are: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Discourse. I've added **Procedural Fluency** from the NRC strands (*Adding It Up*).

**1. Representing (primary)**
- Read the figure. Find shapes S and R and pick out the matching sides, for example the base of S and the base of R.
- Get the side lengths from the figure, by counting grid units or reading the labels.
- Keep the direction straight. "From S to R" means S is the original (pre-image) and R is the image, so the ratio is R ÷ S.

**2. Abstracting and Generalizing (secondary)**
- Recognize that a scale factor is a ratio that is the same for every pair of matching sides: scale factor = (length in R) / (length in S).
- Choose one pair of matching sides to work with, since any pair should give the same value.

**3. Procedural Fluency (NRC)**
- Divide to get the ratio and simplify it, for example 6/4 = 3/2 = 1.5, or 2/8 = 1/4.
- Write the answer as a whole number, fraction or decimal, as the blank asks.

**4. Justifying and Proving (light, optional)**
- Check a second pair of matching sides to confirm they give the same ratio, so the shapes really are similar.
- Check that the size of the answer makes sense. If R is bigger than S the factor should be greater than 1, and if R is smaller it should be between 0 and 1.

**Not used:** Mathematical Modeling, because there is no real-world situation to model, and Collaborative Discourse, because this is an individual item with a short answer.

## Summary order
**Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving as a check)**

Representing does most of the work here: the main difficulty is reading the figure correctly and matching the sides in the right direction (S to R, not R to S). The calculation itself is a single division.

### Answer 2: major practice

**Major practice: Representing**

Why I'd pick it:
- Most of the thinking goes into reading the figure. The student has to find S and R, match up their corresponding sides, and get the lengths by counting grid units or reading labels.
- The usual mistakes come from representation: matching sides that don't correspond, miscounting the grid, or reversing the direction (taking S to R as S/R instead of R/S).
- The rest is light by comparison. Once the sides are read and matched correctly, Procedural Fluency is just one division and a simplification. Abstracting (knowing a scale factor is image ÷ original) is basic background knowledge, not the main challenge.

So Representing is the major practice, and Procedural Fluency is a minor supporting step.

---

## Row 243 (problem_id 125385)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
After the discount, how much would the book cost?
$ ____
```

### Answer 1: practices in order

**Note on the problem:** The text only asks "After the discount, how much would the book cost? $ ____". The original price and the discount (a percent or a dollar amount) are not in the text, so they probably come from a figure or an earlier part of the item. The analysis below assumes the student is given an original price and a discount.

**The NAEP mathematical practices (2026 framework)**
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

**Added from NRC (*Adding It Up*):** Procedural Fluency

---

### Practices needed, in order

**1. Representing (NAEP)**
The student reads the price and the discount from the given information (text, picture, price tag, or table). They then turn the situation into a math form, for example "discount = 25% of $20" and "sale price = $20 − discount", or the single expression 0.75 × $20. This step means moving between a verbal or visual representation and a symbolic or numeric one.

**2. Mathematical Modeling (NAEP), light use**
This is a real-world shopping situation. The student has to decide what the operation means in context: a discount is subtracted from the original price, not added, and a percent discount is a percent of the original price. This is a short modeling step: mapping the real situation to an arithmetic model and checking that the result makes sense (the sale price must be less than the original price).

**3. Procedural Fluency (NRC)**
The student carries out the calculation accurately and efficiently. This means finding the percent of a number (or using the given dollar discount), then subtracting, or multiplying by the complement (for example 1 − 0.25 = 0.75). It includes working with decimals and money, and writing the answer in the $ blank with correct cents.

---

### Practices not needed
- **Abstracting and Generalizing:** There is no pattern or general rule to find. It is a single concrete calculation.
- **Justifying and Proving:** The student does not have to explain or defend their reasoning. Only a numeric answer is asked for.
- **Collaborative Mathematics:** This is an individual item with nothing to work out with others.

### Summary order
**Representing → Mathematical Modeling (light) → Procedural Fluency**

Procedural Fluency carries most of the weight in this item. Representing is the necessary entry step, and Modeling plays a small supporting role (knowing that a discount means subtracting from the original price).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item only asks for a number in a blank ("$ ____"). The student does not have to explain, justify, generalize, or build a model, so most of the cognitive work is the computation itself.
- The main thing the item tests is whether the student can carry out the discount procedure correctly. That means finding a percent of the price (or using the given dollar discount), subtracting it from the original price (or multiplying by the complement, such as 0.75), and handling decimals and money accurately.
- Representing and Modeling are present, but they are light. Reading the price and discount and knowing that "discount" means subtract is a routine, familiar setup for this grade level. It is unlikely to be where students go wrong. Errors on items like this usually come from the calculation: percent conversion, decimal placement, or forgetting to subtract.

**Runner-up:** Representing. It would become the major practice if the price and discount had to be pulled from a more complex figure, table, or advertisement rather than given directly.

---

## Row 244 (problem_id 123995)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Noah was assigned to make 64 cookies for the bake sale. He made 125% of that number. 90% of the cookies he made were sold. How many of Noah's cookies were left after the bake sale?
____ cookies
```

### Answer 1: practices in order

**Answer: 8 cookies**

The 2026 NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. I've added NRC's Procedural Fluency as a sixth. Here are the practices this problem needs, in the order you'd use them:

**1. Mathematical Modeling (set up the situation)**
Turn the story into a plan with two steps:
- Cookies made = 125% of 64.
- Cookies left = the part *not* sold. If 90% were sold, then 100% − 90% = 10% are left.

The key modeling decision is to see that the question asks for cookies **left**, not cookies sold. You also need to see that the second percent applies to the cookies he *made*, not to the 64 he was assigned.

**2. Representing (move between forms)**
Write the percents in a form you can compute with:
- 125% = 1.25 = 5/4
- 10% = 0.10 = 1/10

Then write the chain as one expression: 64 × 1.25 × 0.10.

**3. Procedural Fluency (NRC, compute accurately and efficiently)**
- 64 × 5/4 = 80 cookies made
- 80 × 1/10 = 8 cookies left

(Or the longer way: 90% of 80 = 72 sold, and 80 − 72 = 8.)

**4. Justifying and Proving (check the result)**
Make sure the answer makes sense:
- 125% is more than 100%, so he should have made more than 64. 80 > 64 ✓
- 10% of 80 is 8, and 72 sold + 8 left = 80 ✓

**Not really needed:** Abstracting and Generalizing (no pattern or general rule to find) and Collaborative Mathematical Discourse (this is a single-student item with no argument to share or critique).

**Order:** Mathematical Modeling → Representing → Procedural Fluency → Justifying and Proving

**Final answer: 8 cookies**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The problem mostly checks one skill: finding a percent of a number, done twice (125% of 64, then 10% or 90% of 80). Students who can do that correctly will almost always get it right.
- The setup is light. The story walks through the steps in order (assigned, then made, then sold), so the student doesn't have to build a model. They just follow the chain the text gives them.
- Most mistakes will be calculation mistakes. Examples: treating 125% as 1.25 incorrectly, multiplying 64 × 1.25 wrong, or subtracting 72 from the wrong total.

**Close second: Mathematical Modeling.** It matters for two traps: answering with the number *sold* (72) instead of the number *left*, and taking 90% of 64 instead of 90% of 80. These traps are real, but they are reading-and-setup checks inside a routine computation. They are not the main demand of the problem.

So Procedural Fluency is the major practice, with Mathematical Modeling as a minor supporting one.

---

## Row 245 (problem_id 126628)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is its answer?
____
```

### Answer 1: practices in order

The problem text is only:

> "What is its answer? ____"

That doesn't give enough to name the practices. "Its" points to an expression, equation or earlier item that isn't included. It was probably an image or the previous part of a multi-part item. Without it I can't say what math is involved. So I can't give a solid set of practices or an order for this problem.

**What can be said from the stem alone**

The item asks for one computed result in a fill-in blank. That shape usually means the student is carrying out a computation on something already given. Under that reading, the likely practices in order are:

1. **Representing (NAEP)**: read the given expression or object ("it") and understand what it stands for.
2. **Procedural Fluency (NRC)**: carry out the computation or procedure accurately and efficiently. This is the main practice.
3. **Communicating (NAEP)**, minor: write the result correctly in the blank, with the right form or units.

**Practices that are probably not involved**

These are unlikely unless the missing content brings them in:
- Reasoning
- Mathematical Modeling
- Connecting

**Note:** Please share the full problem: the expression, figure or earlier part that "its" refers to. Then I can give a definite list and order of practices.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

All the item asks is "What is its answer?" with a blank to fill in. That means the student has to produce one computed result from something already given. The main demand is carrying out the procedure correctly and efficiently, which is Procedural Fluency.

Representing (reading what "it" is) and Communicating (writing the result in the blank) only support that step.

This choice is tentative, because the problem text leaves out the expression or figure that "its" refers to. If that missing part turned out to need modeling or a multi-step justification, the major practice could change.

---

## Row 247 (problem_id 126091)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is its answer?
____
```

### Answer 1: practices in order

I can't give you an ordered list of practices for this problem because there's no math in it. The whole text is:

> What is its answer?
> ____

"Its" points back to an expression, figure, table or earlier question that didn't come through. Maybe it was an image, or it was the second part of a multi-part item. Without that, nothing tells me which practices the problem calls for or in what order.

**The practices I'd choose from:**

The five NAEP mathematical practices:
1. **Representing:** moving between words, symbols, tables, graphs and diagrams.
2. **Abstracting and Generalizing:** finding the pattern or structure and stating it as a general rule.
3. **Justifying and Proving:** giving reasons for why a result is true.
4. **Mathematical Modeling:** turning a real-world situation into a mathematical one, solving it, and reading the answer back in context.
5. **Collaborative Mathematical Discourse:** explaining and critiquing ideas with others. This one isn't usually assessed on a single individual item.

Plus, as you asked, from the NRC strands:
6. **Procedural Fluency:** carrying out procedures (arithmetic, algorithms, equation solving) accurately, efficiently and flexibly.

**What I can say from the text alone:**
- The item asks for a single answer in a blank and doesn't ask for an explanation. So **Justifying and Proving** and **Collaborative Mathematical Discourse** almost certainly don't apply.
- "What is its answer?" sounds like evaluating something already given, such as an expression or a computation. If so, the main practice would be **Procedural Fluency** (doing the computation). **Representing** might come first, if the quantity is shown in a picture, number line or table that has to be turned into symbols.
- The likely order would be: **Representing (only if needed) → Procedural Fluency**. That's a guess. I can't confirm it without the actual expression or figure.

If you paste the full problem (the expression, figure or earlier part that "its" refers to), I'll give you the exact practices and the order to use them in.

### Answer 2: major practice

If I have to pick one, I'd pick **Procedural Fluency** (from the NRC strands).

Why:
- The item asks "What is its answer?" and gives one blank. So the task is to produce a value, not to explain, prove or model anything.
- That wording usually means evaluating something already given, such as an expression or a computation. Doing that accurately is Procedural Fluency.
- Of the NAEP practices, **Representing** comes closest, but only if the quantity is shown in a figure or table that has to be turned into symbols first. Even then, most of the work is the computation itself.

This is still a low-confidence choice. The problem text doesn't include the expression or figure that "its" refers to. If that missing part turns out to be a word problem or a pattern, the main practice could become Mathematical Modeling or Abstracting and Generalizing. If you paste the full problem, I can confirm the choice.

---

## Row 248 (problem_id 126362)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is its answer?
____
```

### Answer 1: practices in order

The problem you shared only says:

> What is its answer?
> ____

It doesn't contain the actual math: no expression, numbers, figure, or context for what "its" means. It looks like the stem refers to an image, table, or earlier item that didn't come through. Without it, I can't honestly pick the specific practices or say what order they go in for this item.

**Practices I'd choose from (NAEP Mathematical Practices + NRC procedural fluency):**

1. **Representing**: translating between forms (words, symbols, diagrams, tables, graphs)
2. **Abstracting**: pulling out the mathematical structure of a situation
3. **Reasoning**: drawing logical conclusions, justifying steps
4. **Generalizing**: extending a pattern or result to a broader case
5. **Modeling**: using math to represent and solve a real-world situation
6. **Procedural fluency (NRC)**: carrying out procedures (computing, simplifying, applying algorithms) flexibly, accurately, and efficiently

**A tentative ordering for a bare "What is its answer?" item:**

Wording like this usually means a direct compute-the-result question, such as evaluating an expression shown in a figure. If that's what it is, the likely sequence is:

1. **Representing**: read the shown expression or figure and turn it into a computation you can work with.
2. **Procedural fluency**: carry out the arithmetic or algebra accurately to get the value.
3. (Optional) **Reasoning**: check that the result makes sense, for example with an estimate or reasonableness check.

The main practice would be **procedural fluency**, with representing as a short first step. Modeling, generalizing, and abstracting probably wouldn't apply unless the missing content is a word problem or pattern.

If you send the full problem (the expression, figure, or the item that "its" refers to), I can give you a firm, item-specific sequence.

### Answer 2: major practice

If I had to pick one, I'd choose **procedural fluency (NRC)**.

The item only asks "What is its answer?" with a blank for the response. That wording points to a direct compute-the-result task: take what's given and carry out the procedure accurately to get a value. Representing only takes a moment at the start (reading what's shown). Reasoning, abstracting, generalizing, and modeling don't seem central, because nothing in the stem asks for a justification, a pattern, or a real-world situation.

One caveat: the problem text I received has no actual math in it. It seems to refer to an expression or figure that's missing. If that missing piece is a word problem or a pattern, the major practice could change to modeling or generalizing. Based on what's here, though, procedural fluency is the best choice.

---

## Row 249 (problem_id 126648)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What value did Lin find for 62 ÷ 5?
____
```

### Answer 1: practices in order

**Problem:** "What value did Lin find for 62 ÷ 5?"

Note: the problem text refers to "Lin," so it was probably part of a larger item, perhaps showing Lin's work or the method Lin used. That context isn't included, so the analysis below covers the bare computation. It also says where the missing context would change things.

**Practices available** (NAEP Mathematical Practices from the 2026 framework, plus one from NRC):
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics
6. Procedural Fluency (NRC, *Adding It Up*)

**Practices needed, in order:**

1. **Representing** (light use)
   - Read "62 ÷ 5" as a division and decide what form the answer should take: a decimal (12.4), a mixed number (12 2/5), or a quotient with a remainder (12 R 2).
   - If the original item showed Lin's work, for example long division, an area model, or base-ten blocks, this step means reading that representation to find the value Lin got.

2. **Procedural Fluency** (main practice)
   - Do the division accurately: 5 goes into 62 twelve times (60), leaving 2. Then 2 ÷ 5 = 0.4.
   - Result: **62 ÷ 5 = 12.4** (equivalently 12 2/5, or 12 remainder 2).

**Not needed:** Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. The question asks for a single computed value. There is no rule to generalize, no argument to make, no real-world situation to model, and no group work. (If the full item asked whether Lin was *correct*, then **Justifying and Proving** would be a third step at the end.)

**Summary order:** Representing → Procedural Fluency (Procedural Fluency is the main practice).

**Answer:** 12.4

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The main work in this problem is doing the division 62 ÷ 5 correctly to get 12.4 (or 12 2/5, or 12 R 2). Representing comes into it only briefly, to read the expression and choose the answer form. Without the rest of the item, nothing else requires reasoning, justifying, modeling, or generalizing. Whether a student gets this right depends mostly on whether they can carry out the division procedure accurately.

(One caveat: if the full item asked students to read Lin's work from a model or diagram, Representing would become more important. Procedural Fluency would still most likely be the main practice.)

---

## Row 250 (problem_id 75189)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the product.
(21.2) · (0.02)
____
```

### Answer 1: practices in order

**Problem:** Find the product (21.2) · (0.02)

**Practices available**
- NAEP mathematical practices (2026 framework): Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics
- Added from NRC: Procedural Fluency

This is a one-step computation with no context, so most of the practices don't apply. Only two are really used, and Procedural Fluency does most of the work.

**Practices in order**

1. **Representing** (small role)
   - Read "·" as multiplication.
   - See both factors as decimals: 21.2 has one decimal place and 0.02 has two.
   - Optionally rewrite them in a form that's easier to multiply: 21.2 = 212/10 and 0.02 = 2/100, so the product is (212 × 2)/1000.

2. **Procedural Fluency** (main practice)
   - Multiply as if they were whole numbers: 212 × 2 = 424.
   - Count the decimal places: 1 + 2 = 3.
   - Put the decimal point back: 0.424.
   - Check by estimating: 21 × 0.02 ≈ 0.42, so 0.424 is reasonable.

**Not used:** Abstracting and Generalizing (the decimal-place rule is just applied, not worked out), Justifying and Proving (no argument is asked for), Mathematical Modeling (no real-world situation), and Collaborative Mathematics.

**Answer:** (21.2)(0.02) = **0.424**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The problem is a bare computation, (21.2) · (0.02), so the main thing it tests is whether you can carry out the decimal multiplication correctly:

- Multiply as whole numbers: 212 × 2 = 424.
- Count the decimal places: 1 + 2 = 3.
- Put the decimal point back: **0.424**.

Representing only plays a small part (reading "·" as multiplication and seeing the place values). There's no context to model, nothing to justify, and no pattern to generalize. If a student gets this wrong, it's almost always a procedure slip, such as putting the decimal point in the wrong place (4.24 or 0.0424). It's rarely a misreading of the problem.

---

## Row 251 (problem_id 127791)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What percentage remains? ____
```

### Answer 1: practices in order

**Note:** The problem as given ("What percentage remains? ____") is missing its context: there is no whole, no part used or removed, and no figure. It reads like one sub-question of a larger item. So the practice sequence below is for the usual form of this task: some percentage, fraction or amount of a whole has been used or taken away, and the student must say what percent is left.

**Practices used**, from the NAEP 2026 Mathematics Framework, plus Procedural Fluency from NRC's *Adding It Up*:

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Reads the situation and pictures the whole as 100%. If the problem gives a picture, fraction or amount, the student turns it into a percent of the whole. |
| 2 | **Mathematical Modeling** (NAEP) | Sees that "remains" means *whole minus the part taken away*. Writes the relationship: remaining % = 100% − used %. If several pieces are removed, they are added first. If the part is a percent *of what is left*, the student must notice that the base changes. |
| 3 | **Procedural Fluency** (NRC) | Does the arithmetic correctly: converts a fraction or decimal to a percent if needed, adds the parts removed, and subtracts from 100. |
| 4 | **Justifying and Proving** (NAEP), light use | Checks that the answer makes sense: it is between 0% and 100%, and remaining plus used equals 100%. |

**Short sequence:** Representing → Mathematical Modeling → Procedural Fluency → (Justifying, as a check)

**Notes:**
- *Abstracting and Generalizing* and *Collaborative Mathematics* (the other NAEP practices) are not really needed for a single fill-in item like this.
- If the hidden context is a simple one-step case (for example "30% was eaten"), the item is mostly **Procedural Fluency** with very little Modeling. The Representing step matters most when the amount used is shown in a graph or given as a fraction or a raw count instead of a percent.
- If you can share the full problem text or figure, I can confirm or change this ordering.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- The question as written is a single fill-in asking for one number. The key thinking is "remaining = 100% − the part used," which is a routine, well-known step for this item type. Little modeling or representing is needed beyond that.
- So what decides success is doing the calculation correctly: turning a fraction or decimal into a percent if needed, adding the parts removed, and subtracting from 100.
- Errors on items like this usually come from slips in the arithmetic or conversion, not from misreading the situation.

One caveat: the full problem text is missing. If the hidden context shows the used amount only in a figure, or as a raw count or fraction of a whole the student must work out, then **Representing** would become the major practice. If the percent is taken from a changing base (for example, "40% of what was left"), then **Mathematical Modeling** would. Based on the text given, though, I would pick Procedural Fluency.

---

## Row 254 (problem_id 129738)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Write an equation representing this relationship. Use c for cups and t for tablespoons.
c = ____
Use t as your variable.
```

### Answer 1: practices in order

**Note on the problem:** The text refers to "this relationship" but doesn't say what it is. It was probably shown in a table or image that didn't come through. Below I assume the standard conversion, **1 cup = 16 tablespoons**. With that, the answer is **c = t/16**.

**The practices available**

The NAEP 2026 Mathematics Framework names five practices:
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics

As you asked, I've added **Procedural Fluency** from the NRC strands. It means carrying out procedures accurately, efficiently and flexibly.

**Practices used, in order**

1. **Abstracting and Generalizing.** The student looks at the given pairs (for example, 1 cup = 16 tbsp and 2 cups = 32 tbsp). They notice the rule: the number of tablespoons is always 16 times the number of cups. This turns a few specific cases into a general rule.

2. **Representing.** The student writes that rule as an equation using the required letters. The natural first form is t = 16c. The student also has to see that the answer must be written as "c = ___" with t as the variable. That means cups must be expressed in terms of tablespoons.

3. **Procedural Fluency (NRC).** The student rearranges t = 16c by dividing both sides by 16, which gives **c = t/16**. They may check it with one value: t = 32 gives c = 2.

**Practices not needed:** Justifying and Proving, Mathematical Modeling and Collaborative Mathematics play no real part. A quick check by substituting a value is only light self-checking, not a formal justification. The problem is pure symbol translation, with no open-ended real-world modeling and no group work.

**Summary:** Abstracting and Generalizing -> Representing -> Procedural Fluency. The key practice is **Representing**: most of the difficulty is translating the relationship into an equation in the required direction (c in terms of t) instead of the more intuitive t = 16c.

### Answer 2: major practice

**Major practice: Representing.**

The problem asks for one thing: write the relationship between cups and tablespoons as an equation in a set form (c = ___, using t). That is translating a relationship into symbols, which is what Representing is.

- **Abstracting and Generalizing** comes first, but it takes little effort. The rule "16 tablespoons per cup" is a familiar unit fact or is easy to read off the given values.
- **Procedural Fluency** is a single step: divide by 16.
- The usual mistake is a representation error, not a computation error. Students write c = 16t, or give t = 16c when the problem wants c in terms of t. So most of the difficulty, and the source of most wrong answers, sits in Representing.

(This still assumes 1 cup = 16 tablespoons, which gives c = t/16.)

---

## Row 255 (problem_id 131112)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
The temperature in degrees Fahrenheit, F, is related to the temperature in degrees Celsius, C, by the equation F = 9/5C + 32,
In the Sahara desert, temperatures often reach 50 degrees Celsius. How many degrees Fahrenheit is this?
____ degrees Fahrenheit
```

### Answer 1: practices in order

**Practices available**

NAEP Mathematical Practices (2026 framework): Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics.
Added from the NRC (*Adding It Up*): **Procedural Fluency**, meaning carrying out procedures flexibly, accurately, and efficiently.

**Practices needed, in order**

1. **Representing** (primary, first)
   The student turns the words into symbols. "50 degrees Celsius" becomes C = 50, and the student sees that the question asks for F. They read the given equation F = (9/5)C + 32 as a symbolic version of the relationship and substitute: F = (9/5)(50) + 32. The core of the item is moving between the verbal context and the algebraic representation.

2. **Procedural Fluency** (primary, second)
   The student evaluates the expression correctly and in the right order (multiply before adding):
   - (9/5)(50) = 450/5 = 90 (or 50 / 5 = 10, then 10 x 9 = 90)
   - 90 + 32 = **122**

   Answer: **122 degrees Fahrenheit**

3. **Mathematical Modeling** (minor, optional final check)
   The model is given, so the student does not build one. At most, they interpret the result back in the real-world context: 122 F is very hot, which makes sense for the Sahara. This step is light and not required to get the answer.

**Not needed**
- *Abstracting and Generalizing*: the student applies one formula to one value and generalizes nothing.
- *Justifying and Proving*: the item asks for no argument or explanation.
- *Collaborative Mathematics*: this is an individual item.

**Summary order:** Representing -> Procedural Fluency (-> optional Mathematical Modeling check). Representing and Procedural Fluency carry almost all of the item.

### Answer 2: major practice

**Major practice: Procedural Fluency**

Representing is light work in this item:
- The problem gives the equation F = (9/5)C + 32 already written out.
- The context hands over the value C = 50 directly.
- The student builds no representation and translates nothing beyond plugging one number into a formula.

The real work, and the place students actually go wrong, is the procedure:
- substituting the value correctly
- doing the operations in the right order (multiply by 9/5 before adding 32)
- handling the fraction: (9/5)(50) = 90
- finishing the arithmetic: 90 + 32 = **122 degrees Fahrenheit**

The usual mistakes are procedural ones. Students add 32 first, divide by 9/5 instead of multiplying, or use the inverse formula. These are failures of accuracy and procedure, not of representation.

So if I pick one, it is **Procedural Fluency**. Representing is a small supporting step at the start.

---

## Row 257 (problem_id 130191)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find (4.2) · (1.6) by drawing an area diagram or using another method.
____
```

### Answer 1: practices in order

**Problem:** Find (4.2) · (1.6) by drawing an area diagram or using another method.

**Practices used** (NAEP Mathematical Practices plus NRC Procedural Fluency):
- NAEP practices: Representing; Abstracting and Generalizing; Justifying and Proving; Modeling; Reasoning; Mathematical Communication (shown here in the order they apply to this problem)
- NRC: Procedural Fluency

**Practices in order:**

1. **Representing (NAEP).** Turn the product into an area model. Treat 4.2 × 1.6 as the area of a rectangle with side lengths 4.2 and 1.6. Split each side by place value: 4.2 = 4 + 0.2 and 1.6 = 1 + 0.6. That gives a 2 × 2 grid of smaller rectangles.

2. **Reasoning (NAEP).** Use the distributive property, which is what the diagram shows. The whole area equals the sum of the four partial areas: (4 + 0.2)(1 + 0.6) = 4·1 + 4·0.6 + 0.2·1 + 0.2·0.6. You also have to reason about place value here: tenths times tenths gives hundredths (0.2 × 0.6 = 0.12).

3. **Procedural Fluency (NRC).** Work out each partial product correctly and add them up:
   - 4 × 1 = 4
   - 4 × 0.6 = 2.4
   - 0.2 × 1 = 0.2
   - 0.2 × 0.6 = 0.12
   - Total: 4 + 2.4 + 0.2 + 0.12 = **6.72**

   The "another method" option also falls under this practice: 42 × 16 = 672, and there are two decimal places in total, so the answer is 6.72.

4. **Justifying / checking (NAEP Reasoning, light use).** Check that the answer makes sense: 4 × 1.5 = 6 and 4.2 × 2 = 8.4, so 6.72 is in a reasonable range. The area model and the standard algorithm also give the same result.

5. **Communicating (NAEP Mathematical Communication).** Present the labeled area diagram and the sum of the partial products clearly. The problem asks you to show the diagram or method, not just give the number.

**Summary order:** Representing → Reasoning → Procedural Fluency → (Reasoning for the check) → Communicating

**Answer:** 4.2 · 1.6 = **6.72**

Modeling, and Abstracting and Generalizing, are not really needed here. There is no real-world situation to model, and the problem doesn't ask you to generalize a pattern.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why this one:**
- The task boils down to finding the product 4.2 × 1.6 = 6.72. The problem says "by drawing an area diagram **or using another method**," so the area diagram is one way to do it, not a requirement. A student can skip the diagram and still answer correctly with the standard algorithm (42 × 16 = 672, then place the decimal point to get 6.72).
- Whatever method a student picks, the one thing every correct solution needs is accurate decimal multiplication: getting the partial products right, handling place value (tenths × tenths = hundredths), and adding them correctly. That is procedural fluency.
- The other practices help but aren't strictly needed. Representing applies only if the student chooses the diagram. Reasoning (the distributive property) is built into the area model. Communicating is minor, because the answer is a single number.

**Runner-up: Representing (NAEP).** The problem's wording suggests the area model, so if a student actually draws it, representing becomes a big part of the work. But since another method is allowed, the representation is optional and the computation is not. That makes Procedural Fluency the better choice for the single major practice.

---

## Row 259 (problem_id 130824)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Now find x when y = 2.
y = 6x + 8
x = ____
```

### Answer 1: practices in order

**Problem:** Find x when y = 2, given y = 6x + 8.

**Practices to use**

The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. You asked me to add one more, Procedural Fluency from the NRC's *Adding It Up*.

This is a short, symbolic, one-step "plug in and solve" item. Only two of these practices do real work here. A third is an optional check.

**Order of use**

1. **Representing (NAEP).**
   Read the condition "y = 2" and put it into the equation. The relationship y = 6x + 8 becomes an equation in one unknown:
   2 = 6x + 8.
   The key step is seeing that the given value of y replaces y in the equation. This changes the task from "a rule linking x and y" to "an equation to solve for x."

2. **Procedural Fluency (NRC).**
   Solve the linear equation correctly and quickly using inverse operations:
   - Subtract 8 from both sides: 2 − 8 = 6x, so −6 = 6x
   - Divide both sides by 6: x = −1

   This is where most of the work happens. Common mistakes are sign errors (getting 6x = 6 and so x = 1) and doing the operations in the wrong order (dividing before subtracting).

3. **Justifying and Proving (NAEP), optional and light.**
   Check the answer by putting it back in: 6(−1) + 8 = −6 + 8 = 2. ✓
   This is a quick check, not a formal proof. The item doesn't require it, but it catches the sign error above.

**Practices not used**
- **Abstracting and Generalizing:** You don't need to find a pattern or make a general statement.
- **Mathematical Modeling:** There is no real-world context to turn into math.
- **Collaborative Mathematics:** This is a solo item.

**Answer:** x = −1

**Summary:** Representing → Procedural Fluency → (Justifying, as a check)

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why I picked it:

- **Most of the work is here.** Putting y = 2 into the equation is a very small step, because the problem tells you exactly which value goes where. What's left is solving 2 = 6x + 8. You subtract 8 from both sides, then divide by 6.
- **Mistakes usually happen here.** Students tend to get this wrong because of a sign error (2 − 8 = 6 instead of −6, which gives x = 1). Some also do the steps in the wrong order. Both are execution errors, not errors in understanding.
- **It's what the problem tests.** "Now find x when y = 2" asks whether a student can solve a one-variable linear equation correctly. That is exactly what procedural fluency means.

Representing is still needed, but it only sets the problem up. Procedural Fluency is what gets you to x = −1.

---

## Row 261 (problem_id 132416)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Now find x when y = 2.
y = 3/4x - 2 1/2
x = ____
```

### Answer 1: practices in order

## The problem

Find x when y = 2, given y = (3/4)x − 2 1/2.

**Answer: x = 6**

## Practices available

The NAEP Mathematics Framework (2026) names five mathematical practices:

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

You asked me to add one more:

6. **Procedural Fluency** (from the NRC's *Adding It Up* strands): carrying out procedures flexibly, accurately and efficiently.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Turns "find x when y = 2" into a symbolic statement by putting the value into the equation: 2 = (3/4)x − 2 1/2. The student also has to read the mixed number 2 1/2 correctly as 5/2 (not 2 × 1/2) and read (3/4)x as the coefficient 3/4 times x. |
| 2 | **Procedural Fluency** (NRC) | Solves the linear equation step by step: <br>• Add 5/2 to both sides: (3/4)x = 2 + 5/2 = 9/2 <br>• Multiply both sides by 4/3: x = (9/2)(4/3) = 36/6 = **6** <br>Most of the work happens here: rational-number arithmetic (adding a whole number and a fraction, multiplying by a reciprocal) and inverse operations done in the right order. |
| 3 | **Justifying and Proving** (light, optional) | Checks the answer by putting it back in: (3/4)(6) − 5/2 = 9/2 − 5/2 = 2. This confirms x = 6. It's a quick check, not a formal argument, so its weight is small. |

## Practices not needed

- **Abstracting and Generalizing:** the student is not asked to find a pattern or write a general rule. The equation is already given.
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** the item is done alone.

## Summary

**Representing → Procedural Fluency → (Justifying and Proving as a check)**

Procedural Fluency is the main practice. Representing comes first and is short: substitute y = 2 and read the mixed number correctly. Justifying is an optional check at the end. The word "Now" suggests this is the second part of a multi-part item. If the earlier part had the student build the equation from a context or a graph, Representing or Modeling would carry more weight there, not in this part.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:

- **Most of the work is procedure.** The equation is given and the value y = 2 is given. Representing is only a quick substitution. All the real work after that is solving 2 = (3/4)x − 5/2 with inverse operations: add 5/2, then multiply by 4/3.
- **Most errors happen here.** Students who miss this item usually slip on the fraction arithmetic (2 + 5/2 = 9/2, then (9/2)(4/3) = 6). Undoing the operations in the wrong order is another common mistake, and so is mishandling the coefficient 3/4. Those are fluency errors, not errors in representing or reasoning.
- **The other practices play a small part.** Representing is a short first step. Justifying is an optional check at the end. Modeling, Abstracting/Generalizing and Collaborative Mathematics don't come into it.

So if only one practice is tagged, it should be **Procedural Fluency**.

---

## Row 263 (problem_id 132200)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
For the following equation, find y when x=-3.
y = 3/4x - 2 1/2
y = ____
```

### Answer 1: practices in order

## Answer: y = -4 3/4 (or -19/4, or -4.75)

## Practices to use, in order

The NAEP 2026 Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. This is a short "substitute and evaluate" problem, so only two of them are really needed, plus NRC Procedural Fluency.

### 1. Representing (NAEP)
First, read the symbols correctly and turn them into a form you can compute with:
- Read "3/4x" as (3/4)·x. The fraction multiplies x; it is not 3 divided by 4x.
- Change the mixed number to an improper fraction: 2 1/2 = 5/2.
- Write the substitution with parentheses around the negative value: y = (3/4)(-3) - 5/2.

This is the step where most mistakes start: misreading the coefficient, mishandling the mixed number, or dropping the negative sign.

### 2. Procedural Fluency (NRC, *Adding It Up*)
Next, do the arithmetic accurately and efficiently:
- (3/4)(-3) = -9/4
- 5/2 = 10/4, so you have a common denominator
- -9/4 - 10/4 = -19/4
- Convert back to a mixed number: -19/4 = -4 3/4

The skills here are multiplying a fraction by a negative integer, finding a common denominator, subtracting with negatives, and converting between improper fractions and mixed numbers.

### 3. Justifying (NAEP: Justifying and Proving, used lightly)
Finally, check that the answer makes sense:
- (3/4)(-3) is a bit more negative than -2, and subtracting 2.5 should give about -4.75.
- The sign is negative and the size is reasonable, so -4 3/4 holds up.

This step is optional and informal. The item doesn't ask for any justification.

### Practices not used
- **Abstracting and Generalizing**: the problem asks for one value, not a pattern or a general rule.
- **Mathematical Modeling**: there is no real-world context to turn into math.
- **Collaborative Mathematics**: the problem is solved individually.

### Summary
**Representing → Procedural Fluency → (Justifying, as a check)**

The main load is Procedural Fluency. Representing comes first because the expression has to be read and set up correctly before any calculation can start.

### Answer 2: major practice

## Major practice: Procedural Fluency (NRC)

If I had to pick one, it would be **Procedural Fluency**.

**Why:**
- **Most of the work is calculation.** After the substitution is set up, everything left is a chain of steps: multiply a fraction by a negative integer, (3/4)(-3) = -9/4; rewrite 5/2 as 10/4; subtract with negatives to get -19/4; then convert to the mixed number -4 3/4. Each of those steps is a place where a student can slip.
- **Representing is quick here.** Reading (3/4)x and turning 2 1/2 into 5/2 are standard conventions, not real representational choices. The problem gives a ready-made equation and a value to plug in, so there's nothing to translate, no graph or table, and no context.
- **The item is built to test computation.** "Find y when x = -3" is a standard evaluate-the-expression item. It tells apart students who can or can't handle fraction and integer arithmetic accurately, which is exactly what Procedural Fluency describes.
- **Wrong answers usually come from arithmetic slips.** Common errors include writing -9/4 + 5/2 = 1/4, getting the sign wrong on the product, or making a mistake with the common denominator. All of these are fluency errors.

Representing is a close second, since misreading "3/4x" as 3/(4x) would also lead to a wrong answer. But it is the shorter step, and most of the difficulty is in the calculation.

---

## Row 264 (problem_id 132551)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find 1.8 ÷ 0.004. If you get stuck, think about what equivalent division expression you could write.
____
```

### Answer 1: practices in order

**Problem:** Find 1.8 ÷ 0.004. (Hint: think of an equivalent division expression you could write.)

**Answer: 450**

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added NRC's **Procedural Fluency** as a sixth. Here are the ones this problem uses, in the order you'd use them:

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Abstracting and Generalizing** | Remember the general rule behind the hint: multiplying the dividend and the divisor by the same nonzero number doesn't change the quotient (a ÷ b = (a·k) ÷ (b·k)). This is what makes an "equivalent division expression" possible. |
| 2 | **Representing** | Use the rule to rewrite the problem in an easier form. Multiply both numbers by 1000, so 1.8 ÷ 0.004 becomes 1800 ÷ 4. (You could also write it as the fraction 1.8/0.004 = 1800/4.) The decimal divisor becomes a whole number. |
| 3 | **Procedural Fluency (NRC)** | Do the whole-number division correctly: 1800 ÷ 4 = 450. Also choose the right power of ten (×1000, which matches the three decimal places in 0.004). |
| 4 | **Justifying and Proving** (optional, light) | Check the answer by multiplying back: 450 × 0.004 = 1.8. This confirms the rewritten expression gives the same answer as the original. |

**Not used:** Mathematical Modeling (there's no real-world situation to turn into math) and Collaborative Mathematics (it's a problem one student solves alone).

**Main practices:** Abstracting and Generalizing → Representing → Procedural Fluency. Justifying is only a quick self-check at the end. If a student skips the hint and uses the standard "move the decimal point" method, the problem is almost entirely Procedural Fluency.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:

- **The task is a calculation.** It says "Find 1.8 ÷ 0.004," and the answer is a single number (450). Success depends on dividing decimals correctly. That means scaling by the right power of ten (×1000) and then doing 1800 ÷ 4 without mistakes.
- **The hint is optional.** "If you get stuck…" is scaffolding, not part of what the problem asks. Many students will just use the standard move-the-decimal method and never write an equivalent expression on purpose. That path is pure procedural fluency.
- **The other practices support the procedure.** Abstracting and Generalizing (the quotient doesn't change when both numbers are scaled) and Representing (rewriting as 1800 ÷ 4) explain *why* the procedure works. They don't produce the answer on their own. Justifying is only a self-check at the end.

**Runner-up: Representing.** If you score the problem by the strategy the hint points to, rewriting it as an equivalent, easier division comes second. But the main thing the problem tests is decimal division, so Procedural Fluency comes first.

---

## Row 265 (problem_id 132688)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
For the following equation, find y when x = -3.
y = 1.5x + 11
y = ____
```

### Answer 1: practices in order

**Problem:** For y = 1.5x + 11, find y when x = -3.

**Practices to choose from**
- From the NAEP Mathematics Framework (2026): Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics.
- From the NRC, as you asked: Procedural Fluency.

**Practices needed, in order**

1. **Representing.** The student has to read the equation as a rule that links x and y. Then they connect the given value to it: "x = -3" means put -3 in place of x in the expression, which gives y = 1.5(-3) + 11. This step moves from the symbolic rule to one numeric case. It is also where many errors start, such as dropping the negative sign or reading 1.5x as 1.5 + x.

2. **Procedural Fluency.** Next the student has to do the arithmetic correctly and in the right order:
   - Multiply first: 1.5 × (-3) = -4.5. This needs the sign rule for multiplying a positive by a negative, plus decimal multiplication.
   - Then add: -4.5 + 11 = 6.5. This means adding a negative decimal and a positive whole number.

   **y = 6.5**

**Practices not needed**
- **Abstracting and Generalizing:** The student only evaluates one given rule. They don't find a pattern or extend it.
- **Justifying and Proving:** No explanation or argument is asked for.
- **Mathematical Modeling:** There is no real-world situation to turn into math. The equation is already given.
- **Collaborative Mathematics:** It is a task done alone.

**Summary:** Representing (substitute x = -3 into the equation), then Procedural Fluency (1.5 × (-3) + 11 = 6.5). Procedural Fluency carries most of the difficulty, because the sign and decimal work is where students tend to make mistakes.

### Answer 2: major practice

**Major practice: Procedural Fluency**

Representing is only a small first step here. The equation is already written as a rule in x, and the task says outright which value to substitute. Nothing has to be translated, built, or interpreted.

Most of the work, and most of the chance of error, comes after the substitution. The student has to:
- multiply a decimal by a negative number: 1.5 × (-3) = -4.5
- add a negative decimal to a positive number: -4.5 + 11 = 6.5
- do these in the right order (multiply before adding)

A student who gets this wrong will usually have slipped on a sign or the decimal work, not misunderstood what the equation means. So I would tag Procedural Fluency as the major practice, with Representing as a minor one that comes first.

---

## Row 266 (problem_id 133100)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the quotient mentally.
246 ÷ 12
____
```

### Answer 1: practices in order

**Problem:** Find the quotient mentally: 246 ÷ 12

**Answer:** 20.5 (or 20 R6, or 20½)

## Practices available

The NAEP 2026 Mathematics Framework lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC (*Adding It Up*): **Procedural Fluency**, meaning you carry out procedures flexibly, accurately, and efficiently.

## Practices needed, in order

### 1. Abstracting and Generalizing (find the structure)
The word "mentally" rules out long division, so first you have to see a structure that makes the division easy. Two options:
- **Decompose the dividend** using the distributive property: 246 = 240 + 6, because 240 is an easy multiple of 12 (12 × 20).
- **Scale both numbers by the same factor**, which keeps the quotient the same: 246 ÷ 12 = 123 ÷ 6.

This is the key step. It relies on general properties of division, not a memorized procedure.

### 2. Procedural Fluency (NRC) (do the calculation accurately)
Then carry out the simpler steps quickly and correctly in your head:
- 240 ÷ 12 = 20
- 6 ÷ 12 = 0.5 (or remainder 6, which is ½ of 12)
- 20 + 0.5 = **20.5**

(Using the halving route: 123 ÷ 6 = 20 with 3 left over, and 3/6 = 0.5, so 20.5.)

### 3. Justifying and Proving (optional, light check)
A quick check confirms the result: 12 × 20.5 = 240 + 6 = 246 ✓. This is a small self-check, not a formal proof. Many solvers skip it.

## Practices not needed
- **Representing:** the problem is already written in symbols, and you don't need to change it to another form (diagram, number line, and so on).
- **Mathematical Modeling:** there's no real-world situation to turn into math.
- **Collaborative Mathematics:** this is a solo task.

## Summary
**Abstracting and Generalizing → Procedural Fluency → (optional) Justifying and Proving**

The two main practices are Abstracting and Generalizing (seeing 246 as 240 + 6) and Procedural Fluency (doing the mental arithmetic).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why this one:**
- **This item is a computation task.** "Find the quotient mentally: 246 ÷ 12" asks for one number, worked out in your head. There's no situation to model, nothing to represent, and nothing to justify. The item checks whether you can do this division quickly and correctly.
- **The NRC definition already covers mental strategies.** In *Adding It Up*, procedural fluency means carrying out procedures *flexibly*, accurately, and efficiently. The NRC specifically includes knowing mental methods for computation. Splitting 246 into 240 + 6, or halving both numbers to get 123 ÷ 6, are standard mental-division strategies. Choosing and using them is part of procedural fluency.
- **Abstracting and Generalizing plays a supporting role.** Seeing 246 as 240 + 6 does use the distributive property. But for a familiar computation like this, a fluent student uses that structure without thinking about it. They aren't building or stating a general rule. NAEP's Abstracting and Generalizing practice fits better when the item asks students to find, extend, or state a pattern or general relationship.

**How this fits with my earlier answer:** Earlier I listed Abstracting and Generalizing first, because noticing the structure comes before the arithmetic. I'm not taking that back. But if I can pick only one practice that the item mainly tests, it's **Procedural Fluency**. Abstracting and Generalizing is a reasonable second choice.

---

## Row 267 (problem_id 133338)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Order these numbers from least to greatest.

Items to put in order:
- 11/20
- 0
- 49/100
- 8/9
- 1
- 1/2
- 1/13
```

### Answer 1: practices in order

**Answer:** 0, 1/13, 49/100, 1/2, 11/20, 8/9, 1

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added NRC Procedural Fluency as a sixth.

Three practices are needed, in this order:

**1. Representing (sets up the problem)**
- Treat every item as a point on the same number line from 0 to 1. This puts whole numbers, fractions and hundredths into one form you can compare.
- Use 0, 1/2 and 1 as benchmark points to split the items into groups:
  - Below 1/2: 1/13, 49/100
  - Equal to 1/2: 1/2
  - Above 1/2: 11/20, 8/9
  - Endpoints: 0 and 1

**2. Procedural Fluency (NRC) (does the main work)**
- Compare the fractions accurately with standard methods, either common denominators or decimal conversion:
  - 49/100 = 0.49, which is just under 0.50 = 1/2
  - 11/20 = 55/100 = 0.55, which is just over 1/2
  - 1/13 ≈ 0.077
  - 8/9 ≈ 0.889
- This settles the close cases around 1/2: 49/100 < 1/2 < 11/20.

**3. Abstracting and Generalizing (supports the shortcuts and the check)**
- Use general rules about fractions instead of computing each one:
  - A unit fraction with a large denominator is small: 1/13 is close to 0.
  - A fraction like 8/9 = 1 − 1/9 is just under 1.
  - A fraction is below, equal to, or above 1/2 depending on whether its numerator is less than, equal to, or more than half its denominator. For example, 11 > 10, so 11/20 > 1/2, and 49 < 50, so 49/100 < 1/2.
- These rules confirm the order without heavy arithmetic.

**Not central:** Justifying and Proving could appear lightly if a student must explain the order, but the item only asks for the order. Mathematical Modeling and Collaborative Mathematics are not involved.

**Order of practices:** Representing → Procedural Fluency → Abstracting and Generalizing (the last one supports and checks the comparisons).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item is a routine fraction-comparison task. The core demand is to compare the values accurately, either by converting to decimals or by using common denominators.
- The hardest part is the cluster around 1/2: 49/100 < 1/2 < 11/20. Getting it right depends on carrying out those comparisons correctly, which is procedural fluency.
- Representing (the number line and benchmarks) and Abstracting and Generalizing (rules about unit fractions and fractions near 1) help organize and check the work. A student who can't run the comparison procedures reliably will still miss the close cases.

**Runner-up:** Representing, because placing all the values on one 0-to-1 number line with benchmark points is what structures the solution.

---

## Row 268 (problem_id 134784)

- **predicted_practice:** Abstracting and Generalizing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Without calculating, order the quotients of these expressions from least to greatest.

Items to put in order:
- 426 ÷ 70
- 42.6 ÷ 70
- 42.6 ÷ 0.7
- 42.6 ÷ 0.07
```

### Answer 1: practices in order

**Answer (least to greatest):** 42.6 ÷ 70  <  426 ÷ 70  <  42.6 ÷ 0.7  <  42.6 ÷ 0.07

(Approximately 0.609 < 6.09 < 60.9 < 609. Each is 426 ÷ 7 ≈ 60.9 scaled by a power of ten.)

---

**Practices available.** The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. From the NRC strands I'm adding Procedural Fluency.

**Practices used, in order:**

1. **Abstracting and Generalizing.** The problem says "without calculating," so the student first has to see the shared structure. Every expression uses the digits 426 and 7, and only the place value changes. The student then applies two general rules. When the divisor is fixed, a larger dividend gives a larger quotient. When the dividend is fixed, a smaller divisor gives a larger quotient. This is the main step.

2. **Representing.** Next the student rewrites each expression in a common form so they can be compared. One way is to write each as (426 ÷ 7) × a power of ten:
   - 42.6 ÷ 70 = (426 ÷ 7) × 1/100
   - 426 ÷ 70 = (426 ÷ 7) × 1/10
   - 42.6 ÷ 0.7 = (426 ÷ 7) × 1
   - 42.6 ÷ 0.07 = (426 ÷ 7) × 10

   Another way is to scale the divisor and dividend together, for example 42.6 ÷ 0.07 = 4260 ÷ 7.

3. **Procedural Fluency (NRC).** The student has to move decimal points and adjust powers of ten quickly and correctly. That means knowing that dividing by 0.07 is the same as multiplying by 100/7, and that changing 426 to 42.6 divides the quotient by 10. A quick estimate also helps, for example 42.6 ÷ 70 is a bit more than 0.6. Without this fluency the student can't turn the structure from steps 1 and 2 into the correct order.

4. **Justifying and Proving.** Finally the student checks the order against the reasoning. Each quotient is 10 times the one before it, so the order is justified without exact division. This is a light use of the practice, since the item only asks for the order, but it is what confirms the answer.

**Not used:** Mathematical Modeling (there is no real-world context) and Collaborative Mathematics (this is an individual item).

**Order:** Abstracting and Generalizing, then Representing, then Procedural Fluency, then Justifying and Proving.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing.**

The words "without calculating" decide it. The item is built so that computing each quotient isn't the intended route. Instead, the student has to notice that all four expressions share the digits 426 and 7 and differ only by powers of ten. Then they apply two general rules about how quotients change. A larger dividend gives a larger quotient, and a smaller divisor gives a larger quotient.

The other practices play a supporting role:
- **Representing** rewrites each expression in a common form so they can be compared.
- **Procedural Fluency** moves the decimal points correctly.
- **Justifying** confirms the order at the end.

None of these gets started until the student has seen the structure, and seeing the structure is the part the item is really testing.

---

## Row 271 (problem_id 136203)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is the value of |1.8|?
____
```

### Answer 1: practices in order

**Problem:** What is the value of |1.8|?

**Answer:** |1.8| = 1.8

### Which practices are needed, and in what order

The NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Below I add **Procedural Fluency** from the NRC's *Adding It Up* strands, as you asked.

This is a one-step recall item. Only two practices are really used:

**1. Representing (NAEP)**
The student has to read the notation |1.8| as "the absolute value of 1.8." That means its distance from 0 on the number line. Recognizing what the symbol stands for is the first step. Without it, the student cannot start.

**2. Procedural Fluency (NRC)**
Next the student applies the rule. The absolute value of a non-negative number is the number itself. Since 1.8 > 0, |1.8| = 1.8. This is a quick, routine step that should be automatic.

**Order:** Representing -> Procedural Fluency

### Practices that are not needed
- **Abstracting and Generalizing:** The student only uses the general rule (|x| = x for x >= 0). They don't build or extend one.
- **Justifying and Proving:** The item asks for a value, not an argument.
- **Mathematical Modeling:** There is no real-world situation to model.
- **Collaborative Mathematics:** This is an individual item with no communication or shared reasoning.

### Note
The item is mostly a check of procedural fluency. The representing step is small: the student only needs to know the |·| symbol. A common mistake comes from a misconception about the symbol, such as thinking absolute value "changes the sign" and answering -1.8. Answering 1.8 shows the student understands that absolute value is a distance and can never be negative.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item asks the student to apply one known rule: for x >= 0, |x| = x. This is the core of the task, and it is a routine step that should be automatic. That is what procedural fluency means.
- Representing is needed only in a small way, to recognize the |·| symbol. Any student who has learned absolute value reads that symbol without effort. There is no translating between forms, such as a number line, a table, or words, and nothing to build or interpret.
- Students who get this item wrong usually fail at the procedure or the rule. For example, they treat absolute value as "flip the sign" and answer -1.8. Reading the notation is rarely the problem.

So if only one practice is tagged, **Procedural Fluency** is the main one. Representing is a minor first step.

---

## Row 272 (problem_id 135943)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is the value of |-7|?
____
```

### Answer 1: practices in order

**Problem:** What is the value of |-7|?  **Answer: 7**

The NAEP mathematics framework names five practices (Mathematical Practices): Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Per your request, I've also added NRC's **Procedural Fluency** (one of the five strands of mathematical proficiency in *Adding It Up*).

This is a short recall item with one step, so only a few practices are used.

### Practices used, in order

1. **Representing** (NAEP)
   - The student reads the symbol |  | as "absolute value" and connects it to what it means: the distance of a number from 0 on the number line. The student might picture -7 as sitting 7 units to the left of 0.
   - This step turns the notation into something the student can work with.

2. **Procedural Fluency** (NRC)
   - The student applies the rule quickly and correctly: the absolute value of a negative number is its opposite. So |-7| = 7.
   - This is the main practice the item tests. Most students who have learned absolute value answer it from memory.

3. **Justifying (light check)** (NAEP, minor, optional)
   - A brief check that the answer makes sense: distance can't be negative, so the result has to be positive (7, not -7).
   - The item doesn't require this, but it guards against the common mistake of writing -7.

### Practices not used
- **Abstracting and Generalizing:** no pattern or general rule has to be built.
- **Mathematical Modeling:** there is no real-world situation.
- **Collaborative Mathematics:** the student works alone.

### Summary
**Representing → Procedural Fluency → (optional) Justifying check**

Procedural Fluency is the main practice here. Representing is a small first step (reading the notation as distance from 0), and Justifying is just a quick check that the answer is positive.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- The item is a direct "evaluate this" question: |-7| = 7. To solve it, the student applies a known rule (the absolute value of a negative number is its opposite) quickly and correctly. That is what procedural fluency means.
- The other practices play only a small part. Representing is just reading the |  | notation, and Justifying is an optional check. Neither one is what the item is really testing.
- Students who get this wrong usually do so because they misapply or don't know the rule (for example, they answer -7). They don't fail because of trouble with representation, modeling, or reasoning.

So if you need one label, choose **Procedural Fluency**.

---

## Row 275 (problem_id 137016)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the quotient.
0.24 ÷ 0.015
____
```

### Answer 1: practices in order

**Problem:** Find the quotient 0.24 ÷ 0.015.

**Answer:** 16

**Practices used:** The 2026 NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. I've added Procedural Fluency from the NRC's *Adding It Up* strands as a sixth.

This is a short computation with no context, so only two practices are really needed.

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Rewrites the division in an equivalent form with a whole-number divisor. Multiplying both numbers by 1000 turns 0.24 ÷ 0.015 into 240 ÷ 15. The student also has to see that this doesn't change the quotient. |
| 2 | **Procedural Fluency** (NRC) | Divides correctly: 240 ÷ 15 = 16. This could be long division, or 15 × 16 = 240. This step does most of the work, so most of the item's difficulty sits here. |

**Optional third step: Justifying and Proving (NAEP), used lightly.** A careful student might check the answer. For example, 0.015 × 16 = 0.240, or a rough estimate: 0.24 is about 0.015 × 15, so the answer is near 15. The item doesn't ask for this, so it plays a minor role.

**Not used:**
- **Abstracting and Generalizing:** no pattern or general rule has to be formed.
- **Mathematical Modeling:** there is no real-world situation.
- **Collaborative Mathematical Discourse:** this is an individual item with no explanation to give.

**Summary:** Representing (move the decimal to make the divisor a whole number), then Procedural Fluency (carry out 240 ÷ 15 = 16). Procedural Fluency is the main practice.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The item just says "Find the quotient." It is a bare computation with no context, no explanation to write, and nothing to model or generalize. To get it right, the student has to divide decimals accurately:

- shift the decimal point in both numbers so 0.24 ÷ 0.015 becomes 240 ÷ 15
- carry out the division to get 16

The rewriting step does touch on Representing, but it is really just one step of the standard procedure for dividing decimals. Students learn it as a rule, not as a choice of how to represent the problem. Most mistakes on this item are procedural, such as moving the decimal point the wrong number of places (giving 1.6 or 160) or making an arithmetic slip. That makes Procedural Fluency the practice the item mainly measures.

---

## Row 277 (problem_id 137232)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Replace the formula with the number, and press enter to check your prediction.
What number does cell C2 now display?
____
```

### Answer 1: practices in order

**Problem:** "Replace the formula with the number, and press enter to check your prediction. What number does cell C2 now display?"

Note: the problem text doesn't include the spreadsheet itself (the formula in C2 or the values in the cells it refers to), so I can't give a numeric answer. What it does show is the task: read a spreadsheet formula, work out its value, and type that value into the cell to check. The practice sequence below is based on that task.

**Practices available** (NAEP 2026 Mathematics Framework practices, plus NRC Procedural Fluency):
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematical Discourse
6. Procedural Fluency (NRC, *Adding It Up*)

**Practices needed, in order:**

1. **Representing (first)**
   The student has to translate between two forms. The cell formula (e.g., `=A2*B2` or `=A2+B2`) is a symbolic expression that uses cell references as variables. The student must read it as an ordinary arithmetic expression, substituting the actual values in the referenced cells. Swapping a formula for the number it produces is moving from one representation (symbolic/relational) to another (a single numeric value).

2. **Procedural Fluency (second)**
   Once the expression is clear, the student has to carry out the arithmetic correctly: the right operations, in the right order (order of operations if the formula has more than one operator). This is the core computation that produces the number entered in C2.

3. **Justifying and Proving (third, light)**
   The prompt says "check your prediction." Pressing Enter and comparing the displayed value with the predicted value is a simple verification step. The student confirms that typing the number gives the same result as the formula, or notices a mismatch and rechecks. This is informal checking, not a formal argument, so it plays a minor role.

**Practices not needed:**
- **Abstracting and Generalizing:** the task asks for one specific value, not a general rule or pattern (unless the larger activity later asks why a formula is better than a hard-coded number when inputs change).
- **Mathematical Modeling:** there is no real-world situation to model in this step.
- **Collaborative Mathematical Discourse:** this is an individual computation item.

**Summary of order:** Representing -> Procedural Fluency -> Justifying and Proving (verification)

The main practices are **Representing** (reading the formula as an expression with values) and **Procedural Fluency** (computing it). Justifying and Proving only covers the brief prediction check.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:
- The item asks for **one number**: "What number does cell C2 now display?" Getting it right depends mainly on evaluating the formula correctly, using the right operations in the right order.
- **Representing** matters too, because the student has to read the formula's cell references as values. But for a typical spreadsheet formula (like `=A2*B2`) that step is short and fairly transparent. Most wrong answers would come from computation mistakes, not from misreading the formula.
- **Justifying and Proving** only covers the brief "check your prediction" step, so it plays a minor role.

If the formula in C2 turned out to be complex or unusual (for example, nested functions or references the student must trace across several cells), I would switch the major practice to **Representing**. Based on the problem as given, I'd pick **Procedural Fluency**.

---

## Row 279 (problem_id 139112)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
At this rate, how much would Lin be paid for 2.1 hours of work?
$ ____
```

### Answer 1: practices in order

**Note:** The problem says "at this rate," but the rate itself isn't in the text. It was probably given in an earlier part of the item, such as a table or a statement like "Lin earns $X for Y hours." The analysis below still holds, because the practices needed don't depend on the exact numbers. For example, if Lin earns $15 per hour, the answer is 2.1 × 15 = $31.50.

## Practices used (NAEP 2026 practices + NRC Procedural Fluency)

The NAEP 2026 framework lists these mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. This problem uses three of them, plus Procedural Fluency from the NRC.

### Order of use

1. **Representing (NAEP).** Read the given rate from wherever it appears (table, graph, or sentence) and write it as dollars per hour, e.g., $y = kx$ or "$k per 1 hour." If the rate is given for several hours (e.g., $45 for 3 hours), convert it to a per-hour amount or set up a proportion.

2. **Mathematical Modeling (NAEP).** Treat the situation as a proportional relationship, pay = rate × hours. Then use that model for the new case of 2.1 hours: pay = k × 2.1, or the proportion $45/3 h = $p/2.1 h.

3. **Procedural Fluency (NRC).** Do the arithmetic correctly: work out the unit rate if needed, then multiply by the decimal 2.1 (e.g., 15 × 2.1 = 31.5). Write the answer in money form ($31.50).

4. **Justifying (NAEP, light use).** Check that the answer makes sense. It should be a little more than twice the hourly rate, and the units should be dollars. This step is a quick check, not a formal proof.

### Not needed
- **Abstracting and Generalizing:** the problem is one specific case, with no general pattern or rule to find.
- **Collaborative Mathematics:** this is an individual item.

**Summary of the order:** Representing → Mathematical Modeling → Procedural Fluency → (Justifying, as a check)

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The rate is already given ("at this rate"), so setting up the problem is routine: pay = rate × hours. Students don't have to build a new model or create a representation. Most of the work, and most of the chances to make a mistake, is in the computation:
- finding the unit rate if the rate was given for more than one hour,
- multiplying by the decimal 2.1 correctly (decimal placement is the usual mistake),
- writing the result as money (e.g., $31.50).

A student who knows "pay = rate × time" can still get this wrong through a computation error. A student who computes accurately will almost certainly get it right. That makes Procedural Fluency the main practice. Mathematical Modeling (applying a proportional relationship) is second, and Representing comes before both but takes little effort.

---

## Row 280 (problem_id 138533)

- **predicted_practice:** Abstracting and Generalizing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Another cone has quadruple the radius, and the same height. How many times larger is the new cone’s volume?
____ times larger
```

### Answer 1: practices in order

**Problem:** Another cone has quadruple the radius and the same height. How many times larger is the new cone's volume?

**Answer: 16 times larger**

---

### Practices available
The NAEP Mathematics Framework (2026) names five mathematical practices: **Representing**, **Abstracting and Generalizing**, **Justifying and Proving**, **Mathematical Modeling**, and **Collaborative Mathematics**. You asked me to add **Procedural Fluency**, which comes from the NRC's *Adding It Up* strands of proficiency.

### Practices needed, in order

**1. Representing**
Turn the words into symbols. Start from the cone volume formula and write both cones with it:
- Original: V₁ = (1/3)πr²h
- New cone: the radius becomes 4r and the height stays h, so V₂ = (1/3)π(4r)²h

The student has to pick the right formula and see that only *r* changes.

**2. Abstracting and Generalizing**
The original radius and height are not given, so the student has to work with general *r* and *h* instead of numbers. The key idea is that volume grows with the **square** of the radius: multiplying the radius by k multiplies the volume by k². Seeing this structure is what lets the student solve the problem without plugging in sample values.

**3. Procedural Fluency (NRC)**
Do the algebra quickly and correctly:
- (4r)² = 16r², so V₂ = (1/3)π·16r²·h = 16 · (1/3)πr²h
- V₂ / V₁ = 16

The factors (1/3), π, r², and h cancel, which leaves **16**.

**4. Justifying and Proving (light, optional check)**
A short check of why the answer is 16 and not 4: the radius is squared in the formula, so the factor of 4 gets squared. This catches the common mistake of answering "4 times larger." Because the answer is fill-in-the-blank with no explanation asked for, this practice plays only a small role.

### Practices not needed
- **Mathematical Modeling**: there is no real-world situation to model. The problem is already a pure geometry and formula question.
- **Collaborative Mathematics**: this is a single-student item.

### Summary
**Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving as a quick check)**

Representing and Abstracting/Generalizing carry most of the thinking. Procedural Fluency carries the calculation.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

**Why this one:**
- **It decides whether students get the item right.** The problem gives no numbers for the radius or the height, so the student has to reason about the cone in general. The key step is noticing that volume depends on the **square** of the radius, so multiplying the radius by 4 multiplies the volume by 4² = 16. The common wrong answer, "4 times larger," comes from missing this. That error is a failure to generalize, not a calculation slip or a wrong formula.
- **Representing is needed, but it is the easy part.** Writing V = (1/3)πr²h and swapping in 4r for r is routine recall. Students who know the formula can do it, and it does not separate strong reasoners from weak ones.
- **Procedural Fluency carries little weight here.** The arithmetic is just 4² = 16 and canceling common factors. Once the student sees the scaling structure, the calculation is trivial.

**In short:** Abstracting and Generalizing is the major practice. Representing comes before it as a setup step, and Procedural Fluency comes after it as a light finishing step.

---

## Row 282 (problem_id 54974)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Find the surface area of the polyhedron in square centimeters.
[Image: Three rectangles in a row measuring 6 by 4, 6 by 5, and 6 by 3. The left rectangle is bordered on the top by a right triangle with side lengths 4, 3, and 5. The right rectangle is bordered on the bottom by a right triangle with side lengths 3, 4, and 5.]
____ square centimeters
```

### Answer 1: practices in order

**Answer: 84 square centimeters**

The figure is a net of a triangular prism. Its bases are 3-4-5 right triangles and its length is 6 cm.

## Practices used, in order

The NAEP 2026 Mathematics Framework lists these mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Procedural Fluency from the NRC's *Adding It Up* is added below as requested.

### 1. Representing (main practice)
- Read the 2-D net as a 3-D solid. The three rectangles fold into the side faces and the two triangles become the bases, so the solid is a triangular prism.
- Link each measurement on the net to a part of the solid. The 6 cm side is the prism's length. The triangle sides 3, 4 and 5 match the widths of the three rectangles (3, 4, 5).
- Check that the net is complete: 5 faces, with no face missing or counted twice.

### 2. Abstracting and Generalizing
- Use the general idea that the surface area of any polyhedron is the sum of the areas of its faces, and that a net shows every face exactly once.
- Notice the structure: the two triangles are congruent and the rectangles share the length 6. This allows the shortcut (perimeter of base × length) + 2 × (base area).

### 3. Procedural Fluency (NRC)
- Rectangles: 6 × 4 = 24, 6 × 5 = 30, 6 × 3 = 18. Their sum is 72 cm² (the same as 6 × (3 + 4 + 5) = 6 × 12 = 72).
- Triangles: it is a right triangle, so the legs 3 and 4 are the base and height. ½ × 3 × 4 = 6 cm² each, so 2 × 6 = 12 cm².
- Total: 72 + 12 = **84 cm²**.

### 4. Justifying and Proving (light, for checking)
- Explain why the legs, not the hypotenuse, are the base and height. The 3-4-5 triangle is a right triangle because 3² + 4² = 5².
- Confirm the face count and the units (square centimeters).

### Not needed
- **Mathematical Modeling**: there is no real-world situation to turn into math. The figure is already given in mathematical form.
- **Collaborative Mathematics**: this is an individual item.

## Summary
**Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving (check)**

Representing and Procedural Fluency are the two practices that matter most for this item.

### Answer 2: major practice

**Major practice: Representing**

This item hinges on Representing. The student has to see that the flat net folds into a triangular prism and work out what each part becomes:
- the three rectangles are the side faces
- the two 3-4-5 triangles are the bases
- the 6 cm side is the prism's length

Once the student understands the net this way, the calculation is routine: 72 + 12 = 84 cm². That arithmetic is basic Procedural Fluency with whole numbers and simple area formulas.

The common mistakes also come from misreading the net, not from the arithmetic:
- leaving out the triangles
- counting a face twice
- using the hypotenuse 5 as the triangle's height

So a student who can do the calculations but cannot interpret the net will still get the item wrong. That makes Representing the deciding practice.

---

## Row 286 (problem_id 111728)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Use your equation to find x.
x = ____
```

### Answer 1: practices in order

**Note:** This is a follow-up part of a multi-part item. "Your equation" refers to an equation the student wrote in an earlier part, which isn't included here. So the exact solving steps can't be given, but the practices this part needs are still clear.

**Practices available** (NAEP 2026 Mathematics Framework practices, plus NRC procedural fluency):
Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics, and Procedural Fluency (NRC).

**Practices needed, in order:**

1. **Representing.** The student has to go back to the equation they wrote earlier and treat it as the symbolic form of the situation. That means knowing which quantity x stands for and that the equation states a relationship that can be solved. This step is light, because the representation already exists. The student only has to read it and use it.

2. **Procedural Fluency (NRC).** This is the main practice in this part. The student solves the equation for x step by step: combining like terms, doing inverse operations on both sides (and distributing, if needed), and carrying out the arithmetic correctly. The answer is a single value written in the blank, so success depends almost entirely on doing these steps accurately and efficiently.

3. **Mathematical Modeling (optional, light).** After solving, the student can check that x makes sense in the original context. For example, a length or count shouldn't be negative, and the value should fit the problem's numbers. Many students skip this step, and it is not required to get the answer.

**Practices not needed:** Abstracting and Generalizing (no pattern or general rule is asked for), Justifying and Proving (no explanation or argument is asked for), and Collaborative Mathematics (individual work).

**Summary order:** Representing -> Procedural Fluency -> (Mathematical Modeling check, optional). **Procedural Fluency is the main practice.**

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

The student already wrote the equation in an earlier part, so the representing and modeling work is done. This part only asks them to solve that equation for x and write one number. Getting it right depends almost entirely on carrying out the algebra and arithmetic accurately. That is procedural fluency.

---

## Row 287 (problem_id 132758)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Neon bracelets cost $1 for 4.
What is the cost per bracelet?
$ ____
[image]
```

### Answer 1: practices in order

**Problem:** Neon bracelets cost $1 for 4. What is the cost per bracelet?

**Answer:** $0.25

The NAEP 2026 Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Below I add **Procedural Fluency** from the NRC's *Adding It Up* strands. This is a one-step unit-rate problem, so only two practices are really needed.

### Order of practices

1. **Representing.** First, turn the words "$1 for 4" into a math form. That form is the rate $1 : 4 bracelets, which can also be written as the division 1 ÷ 4 or the fraction 1/4 dollar per bracelet. The student also has to see that "cost per bracelet" means a unit rate. That tells them to divide the cost by the number of bracelets, not the other way around. The answer box starts with "$", so the result must be written as a decimal amount of money.

2. **Procedural Fluency (NRC).** Next, carry out the calculation correctly: 1 ÷ 4 = 0.25. This means knowing that 1/4 = 0.25 (a quarter of a dollar, 25 cents) and writing it in money form: **$0.25**.

### Practices not needed
- **Mathematical Modeling:** Only in a trivial sense. The situation is already a clean rate and needs no assumptions or checking against the real world.
- **Abstracting and Generalizing:** Not needed. Nothing has to be generalized beyond this one case.
- **Justifying and Proving:** Not needed. No argument or explanation is asked for.
- **Collaborative Mathematics:** Not needed. This is a solo task.

**Sequence:** Representing → Procedural Fluency

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Reasons:

- **Setting up the problem is easy.** "$1 for 4" and "cost per bracelet" lead almost directly to 1 ÷ 4. Little interpretation is needed, so Representing plays only a small part.
- **The main work is the calculation.** The answer has to be 1 ÷ 4 = 0.25, written as **$0.25**. That means dividing a smaller number by a larger one, turning the fraction 1/4 into a decimal, and writing it as money. These are the steps students are most likely to get wrong, for example by answering 4, 0.4, or $4.00.
- **What the item really tests.** It is a short-answer unit-rate item, and it mainly checks whether the student can carry out the division and write the result as money accurately.

Representing comes a close second. If the problem were written more indirectly, it would become the main practice. As written, though, the item mostly tests Procedural Fluency.

---

## Row 290 (problem_id 153281)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the equation. If you get stuck, try using a diagram.
5x + 1/4 = 61/4
x = ____
```

### Answer 1: practices in order

**Problem:** Solve 5x + 1/4 = 61/4. If you get stuck, try using a diagram.

**Solution:** 5x = 61/4 − 1/4 = 60/4 = 15, so **x = 3**.

## Practices used, in order

The 2026 NAEP Mathematics Framework lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I have added Procedural Fluency from the NRC's *Adding It Up* strands, as you asked.

1. **Representing (NAEP).** Read the symbolic equation as a structure: "five equal unknown amounts plus one-quarter make sixty-one quarters." If the student uses the suggested diagram, they draw a tape (bar) model. It has five equal x-segments plus a 1/4 piece, all equal to a bar of length 61/4. Moving between the symbols and this picture shows the two steps: remove the 1/4, then split what is left into 5 equal parts.

2. **Procedural Fluency (NRC).** Carry out the steps correctly and efficiently:
   - Subtract 1/4 from both sides: 61/4 − 1/4 = 60/4 (same denominator, so subtract the numerators).
   - Simplify: 60/4 = 15.
   - Divide both sides by 5: x = 3.

   This is where most of the work happens. The student has to undo operations in reverse order and do the fraction arithmetic.

3. **Justifying and Proving (NAEP), light use.** Check the answer by substituting it back: 5(3) + 1/4 = 15 + 1/4 = 60/4 + 1/4 = 61/4. ✓ This confirms the answer. It also confirms the reasoning that each step kept the equation balanced, because the same operation was done to both sides.

**Not needed:** Mathematical Modeling, since there is no real-world situation to turn into math. Abstracting and Generalizing, since no pattern or general rule is asked for. Collaborative Mathematics, since this is a single-student item.

**Summary order:** Representing → Procedural Fluency → Justifying and Proving (checking). Procedural Fluency is the main practice. Representing matters mainly when the student needs the diagram hint.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC).**

The problem is a standard two-step linear equation. The only work it requires is a fixed procedure done correctly:
- undo the addition: 61/4 − 1/4 = 60/4 = 15
- undo the multiplication: 15 ÷ 5 = 3

There is no situation to model, no pattern to generalize, and no argument to build. Representing (the tape diagram) comes in only as a fallback, since the item says "if you get stuck," and checking the answer is optional. A student who has the procedure solves it without either one. Whether the answer is right depends almost entirely on doing the inverse operations and the fraction arithmetic accurately. That makes Procedural Fluency the major practice.

---

## Row 291 (problem_id 154547)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Find the sum.
-5.7 + (-4.2)
____
```

### Answer 1: practices in order

**Problem:** Find the sum: -5.7 + (-4.2)

This is a short computation item. It mostly tests procedural fluency, with a small bit of conceptual understanding about adding two negative numbers.

## Practices used, in order

**1. Conceptual Understanding (NAEP)**
Notice that both addends are negative. Recall what that means for the sum: adding a negative number moves you further left on the number line. So the result is negative, and its size is the sum of the two absolute values (|-5.7| + |-4.2|). This step picks the right procedure: add the magnitudes and keep the negative sign, rather than subtracting the magnitudes as you would for numbers with opposite signs.

**2. Procedural Fluency (NRC)**
Carry out the decimal addition accurately and quickly:
5.7 + 4.2 = 9.9 (line up the decimal points: 7 tenths + 2 tenths = 9 tenths, 5 + 4 = 9).
Then attach the sign: **-9.9**.

**3. Reasoning (NAEP), minor and optional**
Check that the answer makes sense. Two negatives near -6 and -4 should give something near -10, and -9.9 fits. A quick estimate like this catches sign errors (for example, writing 9.9 or -1.5).

## Practices not needed
- **Problem Solving:** not needed. The item is a direct, routine computation with no context to model.
- **Mathematical Connections:** not needed beyond the basic link between the number line and signed addition.
- **Communicating:** not needed. Only a numeric answer is asked for.

## Summary order
Conceptual Understanding -> Procedural Fluency -> (Reasoning, for a quick check)

The main practice is **Procedural Fluency**.

**Answer:** -9.9

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- The item is a plain computation, "find the sum," with no context, no explanation asked for, and no strategy to choose.
- Most of the work is doing the signed decimal addition correctly: add 5.7 + 4.2 = 9.9 and keep the negative sign, giving **-9.9**.
- Knowing that two negatives add to a bigger negative is a quick sign rule. A fluent student applies it automatically as part of the procedure, so conceptual understanding plays only a small supporting role here.
- The likely errors (dropping the sign, subtracting instead of adding, misaligning the decimals) are execution errors, which is what procedural fluency covers.

If you need a NAEP practice instead, I would pick **Conceptual Understanding**, since it supplies the sign reasoning. But for this item, Procedural Fluency is clearly the main one.

---

## Row 292 (problem_id 155769)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the equation.
-3d + 7 = 1
d = ____
```

### Answer 1: practices in order

**Problem:** Solve -3d + 7 = 1, so d = ____

**The practices I'm using**

From the NAEP Mathematics Framework (Mathematical Practices):
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborating and Discussing

Added from the NRC (*Adding It Up*, five strands):
6. Procedural Fluency: carrying out procedures flexibly, accurately and efficiently.

**Which practices this problem needs, in order**

This is a short, routine linear equation. The equation is already written down, there's no real-world context, and the answer is a single blank. That means only a few practices actually come into play:

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (light) | Reads the symbolic statement -3d + 7 = 1 as a balance: "some number times -3, plus 7, gives 1." Sees that the job is to undo the operations on *d* in reverse order. |
| 2 | **Procedural Fluency** (main practice) | Uses inverse operations accurately: subtract 7 from both sides to get -3d = -6, then divide both sides by -3 to get d = 2. The signs need care here, because a negative divided by a negative gives a positive. |
| 3 | **Justifying** (optional, light) | Checks the answer by substituting it back: -3(2) + 7 = -6 + 7 = 1 ✓. This confirms the solution is correct. |

**Answer:** d = 2

**Practices not really used**
- **Mathematical Modeling:** there's no real-world situation to turn into math.
- **Abstracting and Generalizing:** the student doesn't need to spot a pattern or a general rule. The solving method gets used, not generalized.
- **Collaborating and Discussing:** this is a solo item with a single-answer response.

**Summary:** Representing (brief) → **Procedural Fluency** (main) → Justifying (an optional check). Procedural fluency does nearly all of the work. A wrong answer most likely comes from a procedural mistake, usually a sign error such as getting d = -2, or adding 7 instead of subtracting it to get -3d = 8. It's much less likely to come from misreading what the problem asks.

### Answer 2: major practice

**Major practice: Procedural Fluency** (NRC)

Why:
- The equation -3d + 7 = 1 is already given in symbols. The student doesn't have to represent, model or interpret anything first.
- Solving it is just running a standard procedure: subtract 7 from both sides to get -3d = -6, then divide by -3 to get d = 2.
- The places a student can go wrong are all procedural. The usual mistake is a sign error, like getting d = -2, or using the wrong inverse operation.
- The other practices are minor. Representing is just reading the equation, and Justifying is an optional substitution check.

So nearly all of what this item measures is whether the student can do two-step linear equation solving accurately, which is Procedural Fluency.

---

## Row 293 (problem_id 155730)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Solve the equation and check your solution.
4w − 7 = 6w + 31
w = ____
```

### Answer 1: practices in order

**Answer: w = −19**

The 2026 NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added NRC **Procedural Fluency** as a sixth.

The problem has two parts, "solve" and "check," and each part uses one main practice.

### Practices in order

**1. Procedural Fluency (NRC): the main practice**
The equation is already written in symbols, so most of the work is carrying out standard algebra steps accurately:
- Subtract 4w from both sides: −7 = 2w + 31
- Subtract 31 from both sides: −38 = 2w
- Divide both sides by 2: **w = −19**

Choosing which side to collect the variable on, and keeping the negative signs right, is the fluency being tested.

**2. Justifying and Proving (NAEP): the "check your solution" step**
Substitute w = −19 back into the original equation to show it is correct:
- Left: 4(−19) − 7 = −76 − 7 = −83
- Right: 6(−19) + 31 = −114 + 31 = −83
- Both sides equal −83, so the solution is confirmed.

This is verification, a simple form of justification: showing the answer actually satisfies the equation rather than just stating it.

### Practices that are minor or not used
- **Representing**: only a small role. The student reads the symbolic equation and keeps the equality balanced, but nothing has to be translated between representations such as words, tables, graphs, or symbols.
- **Abstracting and Generalizing**: not needed. This is one specific equation, not a pattern or a general case.
- **Mathematical Modeling**: not used. There is no real-world context.
- **Collaborative Mathematics**: not used. It is an individual item.

**Summary sequence:** Procedural Fluency (solve) → Justifying and Proving (check).

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why this one:
- **Most of the work is procedure.** The equation is already in symbols, so nothing needs to be modeled or translated. The student only has to carry out standard steps correctly: collect the w terms on one side, move the constants to the other, and divide.
- **This is where students go wrong.** Common mistakes are procedural: sign errors when moving −7 or 4w, getting −38 instead of 38, or dividing wrong and ending with +19 instead of −19.
- **The check depends on the solve.** Justifying and Proving comes in at the "check your solution" step, but that check is just substituting the answer back in and doing the arithmetic. Without a solution, there is nothing to check.

So Justifying and Proving is a secondary, supporting practice. Procedural Fluency is the main one.

---

## Row 295 (problem_id 272768)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Find the area of triangle MOQ in square units.
[Image: Triangle MOQ enclosed in rectangle MNPR.]
____ square units
```

### Answer 1: practices in order

**Problem:** Find the area of triangle MOQ, which sits inside rectangle MNPR. The figure is not included in the text, so I can't give a final number. What I can give is the reasoning path and the practices it uses.

**Practices available** (NAEP 2026 Mathematical Practices plus one from the NRC):
1. Representing (NAEP)
2. Abstracting and Generalizing (NAEP)
3. Justifying and Proving (NAEP)
4. Mathematical Modeling (NAEP)
5. Collaborative Mathematics (NAEP)
6. Procedural Fluency (NRC strand of mathematical proficiency)

---

### Practices needed, in order

**1. Representing (primary, first)**
The student has to read the diagram and turn it into usable measurements:
- Find the side lengths of rectangle MNPR from the figure, whether from grid units, labeled lengths or coordinates.
- Find where O and Q sit on the rectangle's sides, which gives the segment lengths along each side.
- Move from the picture to a numeric/geometric representation. Either see the triangle as the rectangle minus the corner right triangles, or pick a base and height for MOQ directly.

Almost all of the difficulty is here. The question is really about seeing how the triangle relates to the rectangle that encloses it.

**2. Abstracting and Generalizing (supporting, second)**
The student uses a general structural idea instead of a recipe tied to this one figure:
- Area of the inscribed triangle = area of rectangle - (sum of the areas of the right triangles outside MOQ but inside MNPR).
- Or, if a side of MOQ lies along a side of the rectangle and the third vertex is on the opposite side, the area is half the rectangle's area (A = 1/2 * base * height, with the height equal to the rectangle's width).

This means recognizing that a general decomposition / "box method" strategy applies.

**3. Procedural Fluency (NRC, third)**
The student carries out the computation accurately:
- Rectangle area = length * width.
- Each right triangle's area = 1/2 * leg1 * leg2.
- Subtract, or apply 1/2 * b * h directly, without arithmetic errors, and give the answer in square units.

**4. Justifying and Proving (minor, optional last step)**
A light check: confirm that the pieces subtracted plus triangle MOQ exactly tile the rectangle, and that the answer is reasonable (it must be less than the rectangle's area, and equals half of it in the special case). No formal argument is asked for, so this is a weak or optional component.

**Not needed:** Mathematical Modeling (there is no real-world context to translate) and Collaborative Mathematics (it's an individual constructed-response item).

---

### Summary sequence

**Representing -> Abstracting and Generalizing -> Procedural Fluency -> (Justifying and Proving, minor check)**

| Order | Practice | Role | Weight |
|---|---|---|---|
| 1 | Representing | Pull the dimensions and vertex positions from the figure; see MOQ inside MNPR | High |
| 2 | Abstracting and Generalizing | Use the rectangle-minus-corner-triangles (or 1/2 * b * h) strategy | Medium |
| 3 | Procedural Fluency (NRC) | Calculate the rectangle and triangle areas and subtract | Medium-High |
| 4 | Justifying and Proving | Check that the decomposition is complete and the answer is reasonable | Low |

### Answer 2: major practice

**Major practice: Representing (NAEP)**

Why I'd pick it:
- Everything depends on the diagram. The student has to pull the rectangle's dimensions and the positions of O and Q from the figure, then see how triangle MOQ sits inside rectangle MNPR.
- The key insight is a representational one: seeing the triangle as "rectangle minus the corner right triangles," or spotting a base and height that line up with the rectangle's sides. Once the student sees the figure that way, the rest is routine.
- Procedural fluency (multiplying, halving, subtracting) is needed, but it's simple arithmetic. It isn't what makes the item hard or what tells strong students apart from weak ones. Most errors on items like this come from misreading the figure or decomposing it wrong.

If the item turned out to be a plain "1/2 * base * height" with labeled lengths, Procedural Fluency would be a close second. For a triangle enclosed in a rectangle, though, Representing is the dominant practice.

---

## Row 296 (problem_id 273241)

- **predicted_practice:** Representing
- **claude_top_practice:** Representing

### Problem

```text
Find the area of this shape.
[Image: A four-sided shape on a grid, with two sides that drop 5 units as they cross 5 units and meet at a right angle, and two sides that drop two units as they cross 5 units.]
____ square units
```

### Answer 1: practices in order

## Practice options

From the 2026 NAEP Mathematics Framework, the mathematical practices are:
1. **Representing**: reading, making, and moving between representations such as diagrams, grids, and numbers.
2. **Abstracting and Generalizing**
3. **Justifying and Proving**
4. **Mathematical Modeling**
5. **Collaborative Mathematics**

Added from the NRC's *Adding It Up*:
6. **Procedural Fluency**: carrying out procedures such as counting, multiplying, and using area formulas accurately and efficiently.

## Reading the problem

The shape is a kite on a grid:
- The two lower sides each drop 5 units across 5 units, so they slope at 45°. They meet at the bottom vertex at a right angle.
- The two upper sides each drop 2 units across 5 units, rising to a top vertex.

So the left and right vertices are 10 units apart, which is the horizontal diagonal. The top vertex is 2 + 5 = 7 units above the bottom vertex, which is the vertical diagonal.

## Practices needed, in order

**Step 1: Representing.**
Turn the grid picture into numbers. The student reads the rise and run of each side by counting grid units, finds the vertices, and sees that the shape is a kite, or two triangles sharing a base. This is the key step. The shape is drawn on a grid with no labelled lengths, so all the numbers come from the picture.

**Step 2: Abstracting and Generalizing (light use, optional).**
Recognize the shape as a kite, whose area is half the product of its diagonals. Or split it into two triangles (top and bottom) on the horizontal diagonal. This means linking the specific picture to a general structure or formula. A student who just counts squares or splits the shape into pieces without naming it barely uses this step.

**Step 3: Procedural Fluency.**
Do the calculation correctly:
- Kite formula: (10 × 7) ÷ 2 = **35**
- Or with triangles: top triangle ½ × 10 × 2 = 10, bottom triangle ½ × 10 × 5 = 25, total = 35.

**Answer: 35 square units**

## Practices not needed

- **Justifying and Proving**: the problem asks only for a number, not an argument.
- **Mathematical Modeling**: there is no real-world situation to model.
- **Collaborative Mathematics**: this is a single-student item.

## Summary order

**Representing → (Abstracting and Generalizing) → Procedural Fluency**

Representing and Procedural Fluency are the main practices. Abstracting and Generalizing plays a small part, and only if the student uses the kite or triangle structure.

### Answer 2: major practice

**Major practice: Representing**

The arithmetic here is simple: (10 × 7) ÷ 2 = 35, or 10 + 25 = 35. That needs only basic procedural fluency.

The hard part, and the reason students get it wrong, is the picture. The shape is drawn on a grid with no lengths labelled. The student has to:
- count the rise and run of each side from the grid,
- find the vertices,
- see that the shape is a kite, or two triangles sharing a 10-unit diagonal, and
- work out the diagonals (10 and 7) or the triangle heights (2 and 5).

Common mistakes come from this reading step, not from the calculation. Examples are miscounting grid units, counting slanted side lengths as if they were horizontal or vertical, or not seeing how to break the shape into pieces. Once the picture has been turned into numbers correctly, the rest is routine.

So **Representing** is the major practice, and **Procedural Fluency** comes second.

---

## Row 299 (problem_id 158652)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Procedural Fluency

### Problem

```text
Evaluate the expression if x is 2/5, y is -4, and z is -0.2.
2x - z
____
```

### Answer 1: practices in order

**Problem:** Evaluate 2x − z when x = 2/5, y = −4, z = −0.2.

**Answer:** 2(2/5) − (−0.2) = 0.8 + 0.2 = **1**. (The value of y isn't needed.)

**Practices available:** the NAEP 2026 Mathematics practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus NRC's Procedural Fluency.

### Practices used, in order

1. **Representing (NAEP)**
   - Read the symbolic expression 2x − z. "2x" means 2 times x.
   - Put the values into the expression: 2(2/5) − (−0.2). The parentheses keep the negative sign of z.
   - Notice that the given values are in two forms (a fraction and a decimal) and switch to one form, for example 2/5 = 0.4 or −0.2 = −1/5.
   - Notice that y does not appear in the expression, so its value is extra information.

2. **Procedural Fluency (NRC)**
   - Multiply: 2 × 2/5 = 4/5 = 0.8.
   - Subtract a negative: 0.8 − (−0.2) = 0.8 + 0.2.
   - Add: 0.8 + 0.2 = 1.
   - This step is a matter of carrying out routine steps correctly, especially the sign rule for subtracting a negative.

3. **Justifying and Proving (NAEP), minor / optional**
   - A quick check: redo it with fractions, 4/5 + 1/5 = 5/5 = 1. The answer matches.

### Practices not needed
- **Abstracting and Generalizing:** there is no pattern or general rule to find.
- **Mathematical Modeling:** there is no real-world situation.
- **Collaborative Mathematics:** the problem is solved alone.

**Summary order:** Representing → Procedural Fluency → (Justifying and Proving, as a check)

Procedural Fluency carries most of the difficulty. The usual mistakes are getting the sign wrong on −(−0.2) and mixing up the fraction and decimal forms.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

Why:
- Once the values are put in, the problem is just computation: work out 2(2/5) − (−0.2) and get 1.
- Most of the difficulty is in routine steps:
  - multiplying a fraction by a whole number
  - handling a fraction and a decimal together (2/5 and −0.2)
  - the sign rule that subtracting a negative means adding: −(−0.2) = +0.2
- Students who miss this item usually make one of these mistakes, for example getting 0.6 instead of 1. Misreading the expression is a less common cause.
- Representing (putting values into the expression and ignoring y) is needed, but it is a short first step. It isn't where the item is hard.

