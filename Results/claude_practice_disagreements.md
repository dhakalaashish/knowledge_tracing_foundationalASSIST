# Disagreements: predicted_practice vs claude_top_practice (rows 1–300)

Each problem was answered by a fresh agent that saw only the problem text. **Answer 1** is the reply to the first question; it is stored in `claude_practice_reasoning`. **Answer 2** is the reply to the follow-up; `claude_top_practice` is the first practice it names.

---

## Row 1 (problem_id 151389)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
28 is 7 times what number?
____
```

### Answer 1: practices in order

**Problem:** "28 is 7 times what number?" The answer is **4**.

**Practices used, in order**

1. **Representing (NAEP)**: The student first turns the words into a number sentence: 7 × ☐ = 28 (or 28 = 7n). "is" means "=", "times" means "×", and "what number" is the unknown. This is the main reasoning step. Students who get the item wrong usually fail here, for example by doing 28 × 7 = 196 or 28 + 7.
2. **Procedural fluency (NRC)**: The student then finds the unknown factor. They either recall the fact 7 × 4 = 28 or divide 28 ÷ 7 = 4. This uses a single-digit multiplication or division fact, so a fluent student does it quickly from memory.

**Sequence:** Representing → Procedural fluency

**Practices not used**

- **Abstracting and Generalizing**: Seeing that a missing-factor problem can be solved by division is a weak link at most. It is really part of understanding the "7 × ☐ = 28" form, not a separate generalization. I would leave it out, or give it a low weight if your Q-matrix allows partial weights.
- **Justifying and Proving**: The item does not ask for an explanation. A student might check that 7 × 4 = 28, but the item does not require it.
- **Mathematical Modeling**: The problem has no real-world situation to model.
- **Collaborative Mathematics**: This does not apply to an individual item.

**For tagging:** This is a low-complexity item with two practices, Representing and Procedural fluency, used in that order.

### Answer 2: major practice

**Your follow-up question: if only one practice can be the major one, choose Representing.**

- **It's the main thing the item tests.** The arithmetic is one basic fact that any student who has learned it can do. The real demand is reading "28 is 7 times what number" as 7 × ☐ = 28.
- **It's where students go wrong.** The usual wrong answers are 196 (doing 28 × 7) and 35 or 21 (adding or subtracting). All of these come from misreading the sentence, not from a slip in the arithmetic.
- **It comes first and limits everything after.** If the number sentence is wrong, knowing the fact doesn't help. If it's right, the fact is easy.

**For tagging:** This is a low-complexity item. Tag Representing as the main practice and Procedural fluency as a secondary one, if your scheme allows a second tag.

---

## Row 8 (problem_id 2532)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the scale factor?
____
```

### Answer 1: practices in order

The problem text is only "What is the scale factor? ____". The figure it refers to is missing, so I'm assuming the usual setup for this kind of item: an original figure and a scaled copy (or a dilation), with some corresponding side lengths labeled. The student finds k = (length in the copy) ÷ (matching length in the original).

**Practices in the 2026 NAEP Mathematics Framework:** Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added **Procedural Fluency** from the NRC's five strands of proficiency, as you asked.

### Order of practices

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the diagram. Works out which figure is the original and which is the copy, then matches each side to its partner, keeping the orientation and labels straight. The final answer is also a representation: a single number written as a fraction, decimal, or whole number. |
| 2 | **Abstracting and Generalizing** | Recognizes the structure: every length in the copy equals k times the matching original length. So the scale factor is the ratio *copy ÷ original*, not a difference, and it is the same for every pair of matching sides. This is what tells the student which numbers to divide and in which order. |
| 3 | **Procedural Fluency (NRC)** | Does the arithmetic: divides one pair of matching lengths and simplifies, for example 12 ÷ 4 = 3 or 6 ÷ 9 = 2/3. |
| 4 | **Justifying and Proving** (light, optional) | Checks the result with a second pair of matching sides to confirm the ratio is the same. Also checks that k > 1 if the copy is bigger and k < 1 if it is smaller. This catches the common mistake of flipping the ratio. |

### Practices that don't apply
- **Mathematical Modeling:** not needed, since this is a pure geometry question. It would apply only if the item had a real-world setting, such as a map, blueprint, or scale model, that had to be turned into mathematics.
- **Collaborative Mathematics:** not part of a single-student item like this one.

**Short version:** Representing → Abstracting and Generalizing → Procedural Fluency, with optional Justifying and Proving at the end. If you want to tag only the core practices, use **Representing and Procedural Fluency**. Most of the difficulty is in matching the right sides and dividing in the right order. The arithmetic itself is easy.

### Answer 2: major practice

I'd pick **Representing**.

**Why:**
- **The item depends on the figure.** The question gives no numbers in the text, so everything the student needs comes from reading the diagram. They have to tell the original from the copy and match each side to its partner. That step is where the item is won or lost.
- **The common mistakes come from misreading the diagram.** Students pair the wrong sides, or divide original ÷ copy instead of copy ÷ original. Both errors start with how the student reads the figure, not with arithmetic.
- **Procedural Fluency comes second.** Once the right pair of lengths is chosen, the division is usually one easy step, such as 12 ÷ 4 = 3. A student who matches the sides correctly will almost always get the answer, so the arithmetic is not what separates students.
- **Abstracting and Generalizing is too strong a label.** Knowing that a scale factor is a ratio is needed, but here it is a known definition being applied, not a pattern the student has to generalize.

**One caveat:** I haven't seen the figure, because it isn't in the problem text. If the lengths turn out to be awkward, such as 7.5 → 4.5 (k = 0.6), or the student has to find missing lengths before dividing, **Procedural Fluency** would have a real case to be the main practice instead.

---

## Row 17 (problem_id 3566)

- **predicted_practice:** Representing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Andre is reviewing proportional relationships. He wants to practice using a graph that goes through a point so that each coordinate is between 1 and 10.
For the point, how many outcomes are in the sample space?
____
```

### Answer 1: practices in order

**Answer: 100 outcomes.** Each coordinate is a whole number from 1 to 10. A point is an ordered pair (x, y), so there are 10 × 10 = 100 possible points.

## The practices

The 2026 NAEP Mathematics Framework lists five mathematical practices:

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

As you asked, I added **Procedural Fluency** from the NRC's *Adding It Up* strands.

## Practices used, in order

| Step | Practice | What the student does in this problem |
|---|---|---|
| 1 | **Representing** | Turns the words into math. "A point where each coordinate is between 1 and 10" becomes an ordered pair (x, y) with x ∈ {1, …, 10} and y ∈ {1, …, 10}. The student can picture this as a 10 × 10 grid of points on the coordinate plane, or as a table with x-values as rows and y-values as columns. |
| 2 | **Abstracting and Generalizing** | Spots the structure and ignores the context that doesn't matter. "Proportional relationships" and "graph" are only the setting. Any point (a, b) with a ≠ 0 gives a proportional line y = (b/a)x, so the context rules out no points. What's left is two independent choices: 10 for x and 10 for y. Order matters, since (2, 3) ≠ (3, 2), and a value can repeat, as in (4, 4). So the fundamental counting principle applies: the total is the product of the choices. |
| 3 | **Procedural Fluency (NRC)** | Carries out the count: 10 × 10 = 100. |

## Practices not needed

- **Justifying and Proving:** at most a quick check that ordered pairs with repeated values count separately. Students don't build an argument.
- **Mathematical Modeling:** the context is only a label. No real situation has to be modeled, and no model has to be checked and revised.
- **Collaborative Mathematics:** this is a single item answered alone.

## One caveat

The answer of 100 assumes "between 1 and 10" means whole numbers from 1 to 10, including both ends. That is the usual reading for this kind of item. If the ends were excluded (2 to 9), the answer would be 8 × 8 = 64. The ordering of practices above stays the same either way.

### Answer 2: major practice

**I'd pick Abstracting and Generalizing as the major practice.**

That's the step where students actually succeed or fail on this item.

- **It's the hard part.** Students have to see that "proportional relationships" and "graph" are just setting. Any point (a, b) with a ≠ 0 lies on a proportional line, so the context rules nothing out. Once that's clear, the question is really "how many ordered pairs (x, y) are there with x and y each from 1 to 10?" They then need to see two independent choices where order matters and repeats are allowed, which means the counting principle applies. Wrong answers usually come from missing this structure. Students add instead of multiply (10 + 10 = 20), count unordered pairs (55), or think the proportional condition removes some points.
- **Representing is light here.** Writing the point as (x, y) or picturing a 10 × 10 grid is a quick translation. It supports the abstraction but doesn't carry the item.
- **Procedural Fluency is trivial here.** Once students see the structure, 10 × 10 = 100 is a single basic fact. It's needed, but it doesn't separate students who understand from those who don't.

So the sequence is still Representing → Abstracting and Generalizing → Procedural Fluency. If you have to tag one major practice, it should be **Abstracting and Generalizing**.

---

## Row 22 (problem_id 238362)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
Order from smallest to largest:

Items to put in order:
- Number of pennies in a stack that is 1 ft high
- Number of dollar bills in a stack that is 1 ft high
- Number of slices of bread in a stack that is 1 ft high
- Number of books in a stack that is 1 ft high
```

### Answer 1: practices in order

**Answer to the problem (smallest to largest):** books → slices of bread → pennies → dollar bills

**Practices used**

The NAEP 2026 Mathematics Framework names five mathematical practices: Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; and Collaborative Mathematics. I also included Procedural Fluency, one of the NRC's five strands of mathematical proficiency. Five of these six apply to this problem, in this order:

| Step | Practice | What the student does in this problem |
|---|---|---|
| 1 | **Mathematical Modeling** (formulate) | Treats the real-world question as a model: each stack is 1 ft tall and holds many items of the same size, so *number of items = stack height ÷ thickness of one item*. Assumes typical objects, such as an ordinary hardcover book and a regular sandwich-bread slice. |
| 2 | **Representing** | Turns each everyday object into a number in one shared unit. 1 ft = 12 in. Approximate thicknesses: book ≈ 1 in, bread slice ≈ ½ in, penny ≈ 1/16 in (≈1.5 mm), dollar bill ≈ 0.004 in (≈0.1 mm). |
| 3 | **Abstracting and Generalizing** | Sees the general rule: when height is fixed, the count goes up as thickness goes down. So the order of the counts is the order of the thicknesses reversed. This rule lets the student order the items without exact counts. |
| 4 | **Procedural Fluency** (NRC) | Does the calculations and comparisons correctly. Either divide: 12 ÷ 1 ≈ 12 books, 12 ÷ ½ = 24 slices, 12 ÷ 1/16 ≈ 190–200 pennies, 12 ÷ 0.004 ≈ 3,000 bills. Or simply rank the thicknesses from largest to smallest. Then put the counts in order. |
| 5 | **Justifying and Proving** (with the validate step of Modeling) | Checks that the answer makes sense and argues for it. The gaps between thicknesses are large (bills are about 15 times thinner than pennies, and pennies are about 8 times thinner than bread), so small errors in the estimates can't change those positions. The only close pair is **books and bread**: a very thin paperback could be thinner than thick-cut bread. The answer depends on assuming a typical book (≥ 1 in) is thicker than a typical slice (~½ in). |

**Not used:** Collaborative Mathematics. This is an individual task with no partner work or discussion of other people's reasoning.

**Notes for coding**
- The main practices are **Mathematical Modeling** (estimating from real-world quantities) and **Abstracting and Generalizing** (the inverse rule between thickness and count). Together these are the real thinking the item asks for.
- **Procedural Fluency** plays a small role. A student who uses the inverse rule only has to compare and order four thicknesses. Doing the division is optional.
- **Representing** is mostly mental, done by giving each object a size in a common unit. Nothing has to be drawn or written as a formal representation.

### Answer 2: major practice

**Major practice: Mathematical Modeling**

**Why this one:**
- **The hard part is the real world, not the math.** The problem gives no numbers. Students have to bring in what they know about how thick a book, a slice of bread, a penny and a dollar bill are. Then they turn "how many fit in a 1-ft stack?" into a quantity they can reason about. Making assumptions about real objects and estimating from them is what Mathematical Modeling is.
- **The other practices depend on it.**
  - Representing only puts the modeled estimates into common units.
  - Abstracting and Generalizing (thinner item → more items) is a rule *about* the model.
  - Procedural Fluency only orders four numbers, or does simple division if the student chooses to.
  - Justifying is the check-and-interpret step at the end of the modeling cycle.
- **It is where students actually go wrong.** Most errors come from poor size estimates. For example, a student may not realize how thin a dollar bill is compared with a penny, or may picture a very thin book. The ordering rule is rarely the problem.

**Runner-up:** Abstracting and Generalizing. The inverse rule between thickness and count is the main reasoning step that turns the estimates into an order. It is still secondary, because applying it is easy once the model is set up.

---

## Row 27 (problem_id 594494)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Find 12 ÷ 3/5. Try not to use a diagram, if possible.
____
```

### Answer 1: practices in order

**Problem:** Find 12 ÷ 3/5. Try not to use a diagram, if possible.
**Answer:** 20

**Practices available:** the five NAEP mathematical practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus Procedural Fluency from the NRC strands, as you asked.

## Practices in order

| Step | Practice | What the student does here |
|---|---|---|
| 1 | **Abstracting and Generalizing** (NAEP) | Sees that this is one case of a general rule and uses the rule instead of a picture. Dividing by a fraction is the same as multiplying by its reciprocal: a ÷ (b/c) = a × (c/b). Another way to say it: dividing by 1/5 multiplies by 5, and dividing by 3/5 then divides that by 3. The line "try not to use a diagram" is what pushes the student toward this practice. Without a diagram, they can't count fifths on a model, so they need the general structure. |
| 2 | **Procedural Fluency** (NRC) | Does the calculation accurately and quickly: 12 × 5/3 = 60/3 = 20. A more fluent student simplifies first: 12 ÷ 3 = 4, then 4 × 5 = 20. |
| 3 | **Justifying and Proving** (NAEP), light, optional | Checks the answer by going backward: 20 × 3/5 = 12. They can also check that it makes sense: dividing by a number less than 1 should give an answer bigger than 12. The item doesn't ask for a justification, so this is just a self-check. |

**Short sequence:** Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving)

## Practices not used (or barely used)

- **Representing:** This item mostly removes it on purpose. The usual way in is a visual model, like a number line or bar split into fifths, and the problem discourages that. The only representing left is a small symbolic one: reading 12 ÷ 3/5 as "how many 3/5 are in 12?" or as "3/5 × ? = 12". If you want to code that, put it at step 0, before Abstracting and Generalizing, with a low weight.
- **Mathematical Modeling:** Not used. There's no real-world situation to turn into math.
- **Collaborative Mathematics:** Not used. This is a problem one student solves alone.

**If you want one main practice for the item:** Abstracting and Generalizing, closely followed by Procedural Fluency. The "no diagram" wording is what separates this item from a plain 12 ÷ 3/5 computation, where Procedural Fluency alone would be the main practice.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

**Why this one:**

- **The item is written to force it.** "Try not to use a diagram" removes the concrete route, which is drawing fifths and counting groups. The student has to use the general rule instead: dividing by a fraction is the same as multiplying by its reciprocal, so 12 ÷ 3/5 = 12 × 5/3. That move from a pictured model to a general rule is what this practice means.
- **It separates students who succeed from those who don't.** If a student knows the general rule, the arithmetic left over (12 × 5/3 = 20, or 12 ÷ 3 × 5) is easy for anyone at this grade. A student who can't solve it without a diagram usually doesn't lack arithmetic skill. They lack the generalization.
- **Procedural Fluency is a close second, but it's not the main one.** With a plain "compute 12 ÷ 3/5," I would pick Procedural Fluency, because the item would just test running a learned algorithm. The "no diagram" wording is the only thing that changes the item, and it points to Abstracting and Generalizing.

**One caveat:** Suppose the students have already learned and practiced invert-and-multiply as a routine. Then the rule is something they recall, not something they abstract, and Procedural Fluency is the more defensible pick. Choose based on whether the instruction before this item taught the rule directly or built it from diagrams. The "try not to use a diagram, if possible" wording suggests the latter, so the answer here is Abstracting and Generalizing.

---

## Row 33 (problem_id 7635)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Han found a way to compute complicated expressions more easily. Since 2 ⋅ 5=10, he looks for pairings of 2s and 5s that he knows equal 10. For example,
3 · 2^4 · 5^5 = 3 · 2^4 · 5^4 · 5 = (3 · 5) · (2 · 5)^4 = 15 · 10^4 = 150,000.
Use Han's technique to compute the following:
2^4 · 5 · (3 · 5)^3
____
```

### Answer 1: practices in order

## Practices available

The NAEP Mathematics Framework (2026) has five mathematical practices:

1. **Representing**
2. **Abstracting and Generalizing**
3. **Justifying and Proving**
4. **Mathematical Modeling**
5. **Collaborative Mathematics**

You asked me to add **Procedural Fluency**, one of the NRC's five strands of mathematical proficiency (*Adding It Up*, 2001). It means carrying out procedures flexibly, accurately and efficiently.

## Solution

2^4 · 5 · (3 · 5)^3
= 2^4 · 5 · 3^3 · 5^3   (distribute the exponent: (ab)^n = a^n b^n)
= 3^3 · 2^4 · 5^4       (combine 5 · 5^3 = 5^4)
= 3^3 · (2 · 5)^4       (pair the 2s with the 5s)
= 27 · 10^4
= **270,000**

## Practices used, in order

**1. Abstracting and Generalizing**
The student first has to work out the general rule from Han's single worked example: "a 2 and a 5 make a 10, so match equal powers of 2 and 5 and combine them into a power of 10, using a^n · b^n = (ab)^n." Then they carry that rule over to a new expression with a different structure. Here the 5s are hidden inside (3 · 5)^3 and spread across separate factors, not sitting in one ready-made 5^5. Moving from one example to a general method you can use again is the core of this practice.

**2. Representing**
Next the student rewrites the expression in a different but equivalent symbolic form, one that shows the structure Han's method needs. They split (3 · 5)^3 into 3^3 · 5^3, gather the 5s into 5^4, and regroup the result as 3^3 · (2 · 5)^4. Picking and building this new form, where the 10s can be seen, is moving between symbolic representations.

**3. Procedural Fluency (NRC)**
Finally the student carries out the exponent rules and the arithmetic correctly: (3 · 5)^3 = 3^3 · 5^3, 5^1 · 5^3 = 5^4, 3^3 = 27, (2 · 5)^4 = 10^4 = 10,000, and 27 × 10,000 = 270,000. This strand also supports step 2, because the regrouping only works if the exponent laws are applied correctly. It is listed last because it is the main skill in the final computation.

**Sequence:** Abstracting and Generalizing → Representing → Procedural Fluency

## Practices not needed

- **Justifying and Proving:** the problem asks only for a numerical answer, not an explanation or argument for why the method works. A student might check their own steps informally, but the item does not ask for it.
- **Mathematical Modeling:** the problem is purely symbolic, with no real-world situation to model.
- **Collaborative Mathematics:** the problem is done individually, so nobody else's reasoning has to be shared or critiqued.

### Answer 2: major practice

## Major practice: Abstracting and Generalizing

If I have to pick one, it is **Abstracting and Generalizing**.

**Why this one**

- **The problem is built around it.** The instruction is "Use Han's technique." The student sees one worked example, works out the general rule behind it, and uses that rule on a new expression. The rule is to pair matching powers of 2 and 5 into powers of 10, using a^n · b^n = (ab)^n.
- **The new expression has a different structure.** In Han's example the 5s sit together in 5^5, and you just split off one extra 5. In 2^4 · 5 · (3 · 5)^3, three of the 5s are hidden inside a power of a product, and a fourth stands alone. Copying Han's steps one by one won't work. The student has to see that "4 twos and 4 fives make 10^4" in a form that looks different. That is the step where students succeed or fail.
- **The other two practices support it.** Representing is how the student writes out the structure they have spotted, 3^3 · (2 · 5)^4. Procedural fluency carries out the steps once the plan is clear. Neither one is the hard thinking the item is asking for.

**Caveat on the runner-up**

**Procedural Fluency** is a close second, and in practice it might be first. The item only scores the final number, so a student can skip Han's technique completely and multiply it out: 16 · 5 · 3375 = 270,000. A correct answer therefore doesn't prove the student used the structure. If you are tagging the practice the problem is *designed* to target, choose Abstracting and Generalizing. If you are tagging what a correct response actually *proves*, Procedural Fluency is the safer label.

---

## Row 34 (problem_id 7829)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Han found a way to compute complicated expressions more easily. Since 2 ⋅ 5=10, he looks for pairings of 2s and 5s that he knows equal 10. For example,
3 · 2^4 · 5^5 = 3 · 2^4 · 5^4 · 5 = (3 · 5) · (2 · 5)^4 = 15 · 10^4 = 150,000.
Use Han's technique to compute the following:
(2^3 · 5^2 · (2 · 3)^2 · (3 · 5)^2)/(3^2)
____
```

### Answer 1: practices in order

**Answer: 180,000**

**Solution**

(2^3 · 5^2 · (2·3)^2 · (3·5)^2) / 3^2
= (2^3 · 5^2 · 2^2 · 3^2 · 3^2 · 5^2) / 3^2
= (2^5 · 3^4 · 5^4) / 3^2
= 2^5 · 3^2 · 5^4
= (2 · 3^2) · (2 · 5)^4
= 18 · 10^4
= **180,000**

---

**Practices in order**

The NAEP 2026 practices are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling and Collaborative Mathematics. I added NRC Procedural Fluency to that list.

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Collaborative Mathematics** | Follows Han's worked example, which is someone else's strategy, and works out why it works: each 2·5 makes a 10, so 2^4 · 5^4 = (2·5)^4 = 10^4. |
| 2 | **Abstracting and Generalizing** | Turns the one example into a general method: write everything as powers of primes, pair each 2 with a 5, and multiply the leftover factors into a small coefficient. Then looks at the new expression's structure: (2·3)^2 and (3·5)^2 contain more 2s and 5s, and the 3^2 in the denominator will cancel against the 3s on top. |
| 3 | **Procedural Fluency (NRC)** | Uses the exponent rules correctly. Applies the exponent to each factor in a product, adds exponents for the same base, and subtracts exponents when dividing. This gives 2^5 · 3^2 · 5^4. |
| 4 | **Abstracting and Generalizing** | Applies Han's pairing to this result. There are five 2s and four 5s, so one 2 is set aside: (2 · 3^2) · (2·5)^4. |
| 5 | **Procedural Fluency (NRC)** | Computes 2 · 9 = 18, then 18 · 10^4 = 180,000. |

**Sequence:** Collaborative Mathematics → Abstracting and Generalizing → Procedural Fluency → Abstracting and Generalizing → Procedural Fluency

The two core practices are **Abstracting and Generalizing** and **Procedural Fluency**. Collaborative Mathematics only covers the opening step of understanding and adopting Han's method. If your coding counts Collaborative Mathematics only when students must evaluate or critique someone else's work, drop it and start at step 2.

**Practices not needed**
- **Representing:** The problem uses only a symbolic expression and asks for a number. Students never move between graphs, tables, diagrams or words. Rewriting one symbolic form as another counts as using structure and procedure, and changing 18 · 10^4 to 180,000 is too small to count.
- **Justifying and Proving:** No argument or explanation is asked for. Only the answer is scored.
- **Mathematical Modeling:** "Han" is just a framing. There is no real-world situation to model or interpret.

**Tagging note:** The blank only scores the final number, so a student can ignore Han's method and multiply directly: 8 · 25 · 36 · 225 / 9 = 8 · 25 · 36 · 25 = 180,000. That student uses only Procedural Fluency and skips steps 1, 2 and 4. The item is meant to test *flexible* procedural fluency, which NRC defines as carrying out procedures "flexibly, accurately, efficiently, and appropriately." A correct answer does not prove that the student used the structural method.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

**Why this one:**
- **It is what the item is built to test.** The prompt is "Use Han's technique." To follow it, a student has to take one worked example and turn it into a general method: factor into primes, pair each 2 with a 5, and carry the leftovers as a coefficient. Then they have to see that the same structure is hidden in a new expression. The (2·3)^2 and (3·5)^2 terms contain extra 2s and 5s, and the 3^2 in the denominator cancels. Seeing and using structure like this is the core of Abstracting and Generalizing.
- **It is what separates students.** The exponent rules and the final step (18 · 10^4 = 180,000) are routine for anyone at this level. The hard part is spotting the regrouping (2 · 3^2) · (2·5)^4.
- **The other practices play a smaller role.** Procedural Fluency carries out the plan but doesn't decide what the plan is. Collaborative Mathematics only covers reading Han's example.

**Caveat:** Only the final number is scored, so a student can skip Han's method and multiply directly (8 · 25 · 36 · 25 = 180,000) using Procedural Fluency alone. If you are tagging by what a correct response proves rather than by what the item intends, choose **Procedural Fluency**. For the item's intended practice, choose Abstracting and Generalizing.

---

## Row 37 (problem_id 9567)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
A train moves at constant speed and travels 6 miles in 4 minutes. What is its speed in miles per minute?
____ miles per minute
```

### Answer 1: practices in order

**Problem:** A train moves at constant speed and travels 6 miles in 4 minutes. What is its speed in miles per minute?

**Answer:** 6 ÷ 4 = **1.5 miles per minute**

---

### Practices to use

I used the mathematical practices from the NAEP 2026 Mathematics Framework (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics) and added **Procedural Fluency** from the NRC's *Adding It Up*. This problem needs two of them, in this order.

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the words into math. "Miles per minute" means distance divided by time, so the speed is 6 miles / 4 minutes, written as 6/4 or 6 ÷ 4. The student could also use a ratio table: 6 mi : 4 min → ? mi : 1 min. |
| 2 | **Procedural Fluency** (NRC) | Does the calculation correctly: 6 ÷ 4 = 1.5, or simplifies 6/4 to 3/2 and converts that to 1.5. |

**Order:** Representing → Procedural Fluency

### Practices not needed

- **Mathematical Modeling:** The problem already says the speed is constant, so the student doesn't have to make assumptions, choose a model or check it against the real situation. The context is just a wrapper around a rate. At most, the student briefly checks that 1.5 miles per minute makes sense, and the answer blank already supplies the units.
- **Abstracting and Generalizing:** The student doesn't need to find a pattern or generalize beyond this one case.
- **Justifying and Proving:** The problem doesn't ask for an explanation or argument.
- **Collaborative Mathematics:** It is a single-student item.

### Note for tagging

If you only want the main practice: this is mainly a **Representing** item, because the key step is recognizing that "miles per minute" means distance ÷ time. **Procedural Fluency** is the second skill, needed to get the number. A student who sets up 4 ÷ 6 (≈ 0.67) has made a Representing error. A student who sets up 6 ÷ 4 but gets something other than 1.5 has made a Procedural Fluency error.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

**Why:**

- **The setup is the step that matters.** The student has to turn the words "6 miles in 4 minutes" and "miles per minute" into the rate 6/4, with distance on top and time on the bottom. This is the step where students usually go wrong. The classic mistake is computing 4 ÷ 6 ≈ 0.67, which flips the quantities.
- **The calculation is routine.** 6 ÷ 4 = 1.5 is a basic division for students at the grade where unit rates are taught (around grade 6). Procedural Fluency is needed, but once the setup is right, the calculation is unlikely to separate students who understand the problem from those who don't.

**Caveat:** The unit label "miles per minute" almost hands the student the operation. So this is an easy Representing item, and someone could reasonably tag it as Procedural Fluency instead. If your tags are supposed to show where the item's difficulty comes from, I would still choose **Representing**, because getting the rate right side up is the main thing the item tests.

---

## Row 38 (problem_id 9673)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
A car moves at a constant speed of 50 miles per hour. How long does it take the car to go 200 miles?
____ hours
```

### Answer 1: practices in order

**Problem:** A car moves at a constant speed of 50 miles per hour. How long does it take the car to go 200 miles? **Answer: 4 hours**

**Practices available**

- NAEP Mathematics Framework (2026) practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics
- Added from the NRC strands: **Procedural Fluency**

**Practices needed, in order**

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the words into math. "50 miles per hour" is a rate, 200 miles is a distance, and time is the unknown. The student writes this as distance = rate × time, so 50 × t = 200, or as "how many 50s are in 200?", which is 200 ÷ 50. |
| 2 | **Procedural Fluency** (NRC) | Does the division correctly: 200 ÷ 50 = 4. One quick way is to cancel zeros (20 ÷ 5 = 4). Another is to count up by 50s: 50, 100, 150, 200 is 4 steps. |
| 3 | **Mathematical Modeling** (NAEP), light and optional | Puts the number back in the story and checks it. The 4 means 4 hours, and 4 hours × 50 mph = 200 miles, so the answer makes sense. This step is small because the problem already supplies the model ("constant speed") and the unit ("____ hours"). |

**Practices not needed**

- **Abstracting and Generalizing:** the student finds one value and never extends it to a general rule.
- **Justifying and Proving:** the problem asks for no argument or explanation.
- **Collaborative Mathematics:** the student works alone on the item.

**Short version:** Representing → Procedural Fluency, with an optional Mathematical Modeling check at the end. Representing carries the main thinking (seeing that time = distance ÷ speed). Procedural fluency is only a simple division.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

**Why Representing**

- **It is the step where students get stuck.** The student has to see that "50 miles per hour" and "200 miles" fit the relationship distance = rate × time, with time unknown. That turns into 50 × t = 200, or 200 ÷ 50. Students who miss the item usually go wrong here. Some multiply (50 × 200 = 10,000). Others divide the wrong way (50 ÷ 200 = 0.25). Their arithmetic is fine; they picked the wrong operation.
- **Procedural Fluency only plays a small part.** 200 ÷ 50 = 4 is basic, single-step arithmetic with friendly numbers. Once the student has the right setup, the calculation is almost automatic, so it doesn't separate students who know the material from those who don't.
- **Mathematical Modeling is minimal here.** The problem already gives the model ("constant speed") and the unit ("____ hours"). The student makes no assumptions and has almost nothing to interpret or check.

**In one line:** the challenge in this item is turning the words into the right equation, which is Representing. Doing the arithmetic is easy.

---

## Row 43 (problem_id 127330)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
A bucket contains 11 2/3 gallons of water and is 5/6 full. How many gallons of water would be in a full bucket?
Find the answer.
____ gallons
```

### Answer 1: practices in order

**Answer: 14 gallons**

**Practices used**

The 2026 NAEP Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've also added NRC's **Procedural Fluency** ("Adding It Up").

**Order used to solve the problem**

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the sentence into math. "11 2/3 gallons is 5/6 of a full bucket" becomes the part-whole equation (5/6) x F = 11 2/3, where F is the full amount. A tape diagram also works: 6 equal parts, 5 of them shaded, with the 5 shaded parts holding 11 2/3 gallons. This is the key step. Students who multiply 11 2/3 by 5/6 instead of dividing go wrong here. |
| 2 | **Procedural Fluency** (NRC) | Does the arithmetic correctly. Converts 11 2/3 to 35/3, then F = 35/3 ÷ 5/6 = 35/3 x 6/5 = 210/15 = 14. With the tape diagram: 11 2/3 ÷ 5 = 2 1/3 gallons per sixth, and 2 1/3 x 6 = 14. |
| 3 | **Justifying and Proving** (NAEP), light, as a check | Confirms the answer: 5/6 x 14 = 70/6 = 11 2/3. It also makes sense, because a full bucket should hold a little more than 11 2/3 gallons. The item doesn't ask for a justification, so this step is a self-check and isn't required. |

**Short sequence:** Representing -> Procedural Fluency -> (Justifying and Proving as a check)

**Practices not really needed**

- **Mathematical Modeling:** The bucket gives the problem a real-world setting, but there's nothing to model. The student makes no assumptions, simplifies nothing, and chooses no variables, and the only interpretation is reading 14 as gallons. This is a word problem with a context, not a modeling task. If you want to count it, it would only wrap step 1 (setting it up) and the end (stating the answer in gallons).
- **Abstracting and Generalizing:** Not used. The problem doesn't ask for a pattern or general rule.
- **Collaborative Mathematics:** Not used. Students solve it alone.

**Main practices to tag for this item:** Representing (primary) and Procedural Fluency (secondary).

### Answer 2: major practice

**Major practice: Representing**

The hard part of this problem is turning "11 2/3 gallons is 5/6 full" into the right relationship: (5/6) x F = 11 2/3, which means F = 11 2/3 ÷ 5/6. You could also draw it as a tape diagram with 6 parts, 5 of them filled.

That is where most students go wrong. The usual mistake is to multiply 11 2/3 by 5/6 and get about 9.7 gallons, which is less than what's already in the bucket. That's a setup error, not an arithmetic error.

The arithmetic itself, 35/3 x 6/5 = 14, is a routine fraction calculation. Procedural Fluency is needed, but it comes second. A student who sets up the relationship correctly will almost always get 14.

---

## Row 44 (problem_id 10007)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
What is the measure of angle AEB?
____ °
```

### Answer 1: practices in order

**Note:** The problem says only "What is the measure of angle AEB? ____°". It refers to a figure that isn't included, so I can't work out the number. The practice order below fits this kind of item, where you find an unknown angle from a labeled diagram (for example intersecting lines, a straight angle, a triangle, or parallel lines). If you share the figure, I'll solve it and make the order more specific.

**Practices used**
- **NAEP 2026 Mathematics Framework practices:** Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics.
- **Added from the NRC's *Adding It Up* (2001):** Procedural Fluency, meaning carrying out procedures flexibly, accurately, efficiently and appropriately.

**Order to use them**

1. **Representing.** Read the diagram:
   - Find angle AEB. Its vertex is E and its sides are rays EA and EB.
   - Note the given measures and marked relationships, such as straight lines, lines crossing at E, right-angle marks, parallel arrows and tick marks.
   - Turn these into relations, for example "∠AEB and ∠BEC form a straight line" or "∠AEB + x + 40 = 180".

2. **Abstracting and Generalizing.** Decide which general rule the figure is an example of. This is the key step:
   - vertical angles are equal
   - angles that form a straight line add to 180°
   - the angles of a triangle add to 180°
   - the angles around a point add to 360°
   - the base angles of an isosceles triangle are equal
   - with parallel lines, alternate interior angles and corresponding angles are equal

3. **Procedural Fluency (NRC).** Do the arithmetic to get the measure of ∠AEB. This might mean subtracting from 180° or 360°, or solving a linear equation and substituting (for example 3x + 15 = 180, so x = 55).

4. **Justifying and Proving.** This step is light and done in your head. Check the result: the angles add up correctly, and the value matches how the figure looks (acute or obtuse). If you need two angle facts in a row (say vertical angles, then a straight line), that chain is an informal proof, so this practice partly overlaps steps 2 and 3. The item asks only for a number, so no written justification is needed.

If the figure needs more than one step, steps 2 and 3 repeat: find an in-between angle, then use it to get ∠AEB.

**Not used**
- **Mathematical Modeling:** there is no real-world situation to turn into math. It is a pure geometry figure.
- **Collaborative Mathematics:** there is no other person's reasoning or work to evaluate or build on.

**Short version:** Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving (as a check)

### Answer 2: major practice

**My pick for the major practice is Abstracting and Generalizing.**

Why I chose it:
- **It decides whether students get the item right.** The item comes down to spotting which general angle rule the figure fits: vertical angles are equal, angles on a straight line add to 180°, the angles of a triangle add to 180°, or the parallel-line angle rules. A student who picks the right rule almost always gets the answer. A student who doesn't has no way to start.
- **Procedural Fluency is needed, but it's a small part.** Once the rule is chosen, the work is usually one subtraction or a simple linear equation, which most students at this level can already do.
- **Representing comes first, but it isn't the hard part.** Students do have to read the figure, but finding angle AEB and the given measures is fairly direct. The challenge is knowing what to do with what they see.
- **Justifying and Proving only plays a small role.** The item asks only for a number, so any reasoning stays in the student's head and isn't assessed directly.

**One caveat:** the figure wasn't included, so this assumes a typical figure where you find an angle from angle relationships. If the figure is very busy, with the relationships hard to see (for example, many overlapping lines), Representing could become the main practice. If it gives an algebraic setup like (3x + 15)° and the rule is obvious, Procedural Fluency could be the main one.

---

## Row 45 (problem_id 10706)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
The scale of a map says that 8 cm represents 5 km.
What distance on the map (in centimeters) represents an actual distance of 8 kilometers?
____ centimeters
```

### Answer 1: practices in order

**Answer: 12.8 centimeters**

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added procedural fluency, one of the five strands of mathematical proficiency in the NRC's *Adding It Up* (2001).

This problem needs two practices, in this order. A third step is an optional check.

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turn the sentence "8 cm represents 5 km" into a ratio and set up a proportion: 8 cm / 5 km = x cm / 8 km. A ratio table or a double number line also works. The key step is keeping map units with map units and real units with real units, so the ratio isn't flipped. |
| 2 | **Procedural fluency** (NRC) | Solve it. Cross-multiplying gives 5x = 64, so x = 12.8. Or use the unit rate: 8 ÷ 5 = 1.6 cm per km, and 1.6 × 8 = 12.8 cm. Either way the student has to divide and multiply decimals correctly. |
| 3 (optional) | *Justifying and Proving* (NAEP), informal only | Check that the answer makes sense. 8 km is more than 5 km, so the map distance must be more than 8 cm, and 12.8 is. Also, 12.8 / 8 = 1.6 = 8 / 5, so the ratio holds. The answer doesn't depend on this step, so I wouldn't count it as a required practice. |

**Core sequence: Representing → Procedural fluency**

**Practices that don't apply:**
- **Abstracting and Generalizing:** The problem asks about one case only. There's no pattern to extend and no general rule to state. You could write map = 1.6 × actual, but the item doesn't ask for it.
- **Mathematical Modeling:** The setting is real-world, but the scale already gives the model. The student doesn't choose assumptions, build a model, or test it.
- **Collaborative Mathematics:** This is an individual item.

**Errors to expect (both come from step 1, Representing):**
- **Flipped ratio:** 5/8 × 8 = 5 cm.
- **Adding instead of scaling:** 5 → 8 is "+3", so 8 + 3 = 11 cm.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The hard part of this problem is turning "8 cm represents 5 km" into the right ratio and keeping the units lined up: 8 cm / 5 km = x cm / 8 km. Once that's set up, the arithmetic is easy (8 ÷ 5 × 8 = 12.8), and most students who reach that point get it right.

Both common wrong answers also come from representing, not from computing:
- **Flipped ratio:** 5/8 × 8 = 5 cm.
- **Adding instead of scaling:** 8 + 3 = 11 cm.

So whether a student gets this item right depends mostly on Representing. Procedural fluency is needed too, but it plays a supporting role.

---

## Row 46 (problem_id 10412)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
A right triangle has side lengths of a, b, and c units. The longest side has a length of c units. Complete the equations to show three relations among a, b, and c.
c^2 = ____
Use the ^ symbol to represent an exponent.
For example: 5^2 should be typed as 5^2
```

### Answer 1: practices in order

**Practices available** (NAEP 2026 Mathematics Framework mathematical practices, plus the one from NRC you asked to add):

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics
6. *(added)* Procedural Fluency (NRC, *Adding It Up*)

**Answer:** c^2 = a^2 + b^2. The other two relations are a^2 = c^2 - b^2 and b^2 = c^2 - a^2.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Turns the words into a mental picture or sketch: a right triangle with legs a and b, and the hypotenuse c, because "the longest side" of a right triangle is the hypotenuse. |
| 2 | **Abstracting and Generalizing** | Sees that there are no numbers here, only variables, so the answer must be a general relation that holds for *every* right triangle. They recall the Pythagorean Theorem as that general rule. |
| 3 | **Representing** | Writes the relation as a symbolic equation, c^2 = a^2 + b^2, and uses the required notation (^ for exponents). |
| 4 | **Procedural Fluency (NRC)** | Rearranges the equation correctly and efficiently to get the other two relations: subtract b^2 to get a^2 = c^2 - b^2, and subtract a^2 to get b^2 = c^2 - a^2. |

## Practices not needed

- **Justifying and Proving:** the student does not have to explain why the theorem is true, only state it.
- **Mathematical Modeling:** there is no real-world situation to model. It is a pure geometry item.
- **Collaborative Mathematics:** it is an individual item.

**Short version:** Representing → Abstracting and Generalizing → Representing → Procedural Fluency.

Representing and Abstracting and Generalizing carry most of the weight. The main difficulty is seeing that c is the hypotenuse and using the general theorem. Procedural Fluency is needed only for the simple algebra that gives the three relations.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

**Why this one:**

- **The item gives no numbers.** The sides are only a, b, and c, so the student can't calculate anything. They have to state a relation that holds for *every* right triangle. Writing a general rule in variables is what Abstracting and Generalizing means.
- **The key step is choosing the general rule.** The student has to see that "right triangle, longest side c" calls for the Pythagorean Theorem, written as c^2 = a^2 + b^2. A student who can't make that step can't answer, even with good representing skills.
- **The other practices only support it.**
  - *Representing* turns the words into a triangle with c as the hypotenuse, and then into symbols. It is needed, but it is the way in and the way out, not the main difficulty.
  - *Procedural Fluency* only rearranges the equation into a^2 = c^2 - b^2 and b^2 = c^2 - a^2. That is simple algebra once the main relation is known.

**Second choice:** Representing would be my runner-up. You could argue for it if you see the task mainly as turning a verbal description into a symbolic equation. But the item asks for relations "among a, b, and c" for any right triangle, so the main thinking is generalization.

---

## Row 51 (problem_id 14063)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Find the sum without a calculator.
10 + 21 + 32 + 43 + 54 + (-54) + (-43) + (-32) + (-21) + (-10)
____
```

### Answer 1: practices in order

**Problem:** Find the sum without a calculator:
10 + 21 + 32 + 43 + 54 + (-54) + (-43) + (-32) + (-21) + (-10)

**Answer: 0**

## Practices available

**NAEP Mathematics practices (2026 framework):**
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

**Added from the NRC strands of mathematical proficiency:** Procedural Fluency

## Practices needed, in order

### 1. Abstracting and Generalizing (main practice)
The point of the item, especially the "without a calculator" part, is to get students to look at the structure of the expression before they start adding. The student has to notice that:
- the second half of the list is the first half with every sign flipped, in reverse order (54 and -54, 43 and -43, 32 and -32, 21 and -21, 10 and -10)
- any number plus its opposite is zero: a + (-a) = 0
- the commutative and associative properties of addition let you regroup the terms into those pairs

This step is what turns a ten-term computation into an obvious answer.

### 2. Procedural Fluency (NRC)
Next the student carries out the simplified computation correctly:
(10 + (-10)) + (21 + (-21)) + (32 + (-32)) + (43 + (-43)) + (54 + (-54))
= 0 + 0 + 0 + 0 + 0 = **0**

This needs accurate handling of signed-number addition, and the ability to pick the efficient method (pairing) instead of adding left to right.

### (Optional) 3. Justifying and Proving
This only applies if the student is asked to explain the answer. In that case they would say that regrouping is valid because addition is commutative and associative, and that each pair sums to zero by the additive inverse property. The item as written only asks for the number, so this step is light or implicit.

## Not needed
- **Representing:** the expression is already given in symbols. The student doesn't need a number line, diagram or table, though a number line could be used to show the cancellation.
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** this is a single-student item.

## Summary
**Abstracting and Generalizing → Procedural Fluency** (→ Justifying and Proving only if an explanation is required)

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

Why this one and not Procedural Fluency:

- **The item is built around it.** The second half of the expression is the first half negated and reversed. That design, plus "without a calculator," signals that the test is whether students see the structure, not how well they add.
- **It decides whether students succeed easily.** Once a student sees that each number has its opposite in the list (a + (-a) = 0), the answer is 0 at once. A student who misses this has to add ten signed numbers left to right, which is slow and easy to get wrong.
- **The fluency part is trivial once the structure is seen.** After pairing, all that's left is 0 + 0 + 0 + 0 + 0. That's a small amount of procedure compared with the insight that set it up.

Procedural Fluency is the alternative for a student who ignores the structure and adds term by term. That still gets the right answer, but it isn't what the item is designed to elicit. So the item's main practice is **Abstracting and Generalizing**.

---

## Row 53 (problem_id 15569)

- **predicted_practice:** Justifying and Proving
- **claude_top_practice:** Procedural Fluency

### Problem

```text
A child’s pass costs $15. How many dollars does an adult pass cost?
$ ____
```

### Answer 1: practices in order

**Note on the problem:** The text gives only the child's pass price ($15). It doesn't say how an adult pass relates to it. The item almost certainly came with a stimulus (a table, a price list or a statement such as "an adult pass costs twice as much" or "$7 more") that wasn't included. So I can't give a numeric answer. The practice sequence below holds for any of those versions. The steps show where the missing information would be used.

## Practices used (NAEP 2026 Mathematical Practices + NRC Procedural Fluency)

The NAEP practices are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling and Collaborative Mathematics. Collaborative Mathematics is not assessed on individual items. The NRC strand added here is Procedural Fluency.

### Order of use

1. **Representing** (first, essential)
   - Read the stimulus (table, price list or verbal statement) and turn it into a usable form. This means finding the known value (child = $15), the unknown (adult price) and the stated relationship between them.
   - Example: "adult = 2 × child", or "adult = child + 7", or "family pass of 2 adults + 2 children = $X". Each becomes an expression or equation.

2. **Mathematical Modeling** (only if the stimulus is a context with more than one quantity, such as a total cost for a group)
   - Set up the equation that matches the situation, e.g., 2a + 2(15) = total.
   - Skip this step if the relationship is given directly ("twice as much"). In that case Representing already covers it.

3. **Procedural Fluency (NRC)** (core execution step)
   - Do the arithmetic correctly and efficiently: multiply, add, or solve the one-step/two-step equation (e.g., 2 × 15 = 30; or (total − 30) ÷ 2).
   - This is where most of the item's work happens. It is a short-answer computation item.

4. **Justifying and Proving** (light, optional)
   - Check that the answer makes sense: an adult pass is usually priced at or above a child's pass, and the units are dollars. If the answer is substituted back into the relationship, it should reproduce the given values.
   - The item only asks for a number, so this is only an internal check and is not demonstrated.

### Not used
- **Abstracting and Generalizing**: the item asks for one specific value, not a general rule or pattern.
- **Collaborative Mathematics**: not assessed on an individual item.

### Summary sequence
**Representing → (Mathematical Modeling, if the context needs an equation) → Procedural Fluency → (Justifying and Proving as a self-check)**

Primary practices: **Representing** and **Procedural Fluency**. If you share the missing stimulus (the table or the sentence that relates adult and child prices), I can confirm whether Modeling is needed and give the numeric answer.

### Answer 2: major practice

**Major practice: Procedural Fluency (NRC)**

**Why:**
- The item is a short-answer computation. Once the relationship between adult and child prices is known, the task is a one- or two-step calculation, such as 2 × 15 or 15 + k. The score depends on doing that arithmetic correctly.
- The problem already supplies the relationship, so Representing is light. The student identifies the known value and the operation but does not build a new representation.
- Modeling and Justifying are minor or absent, and the item has no generalization.

**Caveat:** The stimulus that relates the adult and child prices is missing from the text I was given. If it is a complex table, or a multi-quantity context such as "a family pass for 2 adults and 2 children costs $80," the main demand moves to **Representing**: pulling the right relationship out of the stimulus and setting it up. With the problem as given, Procedural Fluency is my choice.

---

## Row 58 (problem_id 21347)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
How much will a car be worth after one year if its initial value was x dollars? If you get stuck, consider using diagrams or a table to organize your work.
____ dollars
Use x as your variable.
```

### Answer 1: practices in order

## Mathematical practices for this problem

**Problem:** How much will a car be worth after one year if its initial value was x dollars? (Answer in terms of x. Tables or diagrams may help.)

**A caveat first:** the text as given does not say how fast the car loses value. Items like this usually sit under a stem such as "a car loses 15% of its value each year." Below I assume a yearly depreciation rate of r%. If the rate were 15%, the answer would be **0.85x**.

### Practices used (NAEP 2026 math practices + NRC procedural fluency)

| Order | Practice | What the student does here |
|---|---|---|
| 1 | **Mathematical Modeling** (NAEP) | Turns the real situation into math. The car loses a percentage of its value, so the new value = original value − (rate × original value). The student also notes that the answer must be in dollars and written in terms of x. |
| 2 | **Representing** (NAEP) | Uses what the problem suggests: a table or diagram. For example, a table with rows for "Initial value: 100, 1000, x" and "Value lost: 15, 150, 0.15x," or a bar model showing the part lost and the part kept. Moving between the words, the table and symbols is the core of this step. |
| 3 | **Abstracting and Generalizing** (NAEP) | Moves from specific numbers (100 → 85, 1000 → 850) to the general rule for any starting value x: value after one year = x − 0.15x. This step is the key one, because the answer has to be an expression in x, not a number. |
| 4 | **Procedural Fluency** (NRC) | Does the algebra and percent work correctly: changes the percent to a decimal (15% → 0.15) and combines like terms, x − 0.15x = (1 − 0.15)x = **0.85x**. In general, x(1 − r/100). |
| (5, optional) | **Justifying and Proving** (NAEP) | Quick check: put a value back in (x = 1000 gives 850, which is less than 1000, as depreciation should). The item doesn't ask for a justification, so this practice is minor or absent. |

**Not used:** Collaborative Mathematics. This is a single-student, single-answer item.

### Summary of the order
**Mathematical Modeling → Representing → Abstracting and Generalizing → Procedural Fluency** (with an optional Justifying check at the end).

Main practices: **Abstracting and Generalizing** and **Mathematical Modeling**. The main difficulty is writing a general expression in x from a percent-decrease situation. Procedural Fluency is needed, but the computation itself is light.

### Answer 2: major practice

## Major practice: **Abstracting and Generalizing** (NAEP)

**Why this one:**
- **It is what the item asks for.** The answer must be an expression in x ("Use x as your variable"), not a number. The student has to go from "a car worth some amount loses a percent of its value" to one rule that works for any starting value: x − 0.15x = 0.85x (or x(1 − r) in general).
- **It is the main difficulty.** A student who knows the price drops by a percent can still get stuck if they can't write it with a variable. The hint about using a table or diagram is there to help with this step: try specific values (100 → 85, 1000 → 850), then generalize to x.
- **The other practices support it:**
  - *Mathematical Modeling*: the context is a familiar depreciation setting, and setting it up takes only a little modeling.
  - *Representing*: the table or diagram is suggested as a help, not required.
  - *Procedural Fluency*: the algebra (combining x − 0.15x) is short.

**Runner-up:** Mathematical Modeling. If the depreciation rate and setting were unfamiliar or needed more interpretation, modeling would carry more weight. As the item is written, the hard part is the generalization, not the modeling.

---

## Row 60 (problem_id 22078)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
How far are the hurdles from one another?
____ meters
```

### Answer 1: practices in order

**Note:** The problem text is only "How far are the hurdles from one another? ____ meters". The diagram or numbers it refers to are missing. Items like this usually show a race track drawn as a number line or diagram, with the start, the first hurdle, the last hurdle and/or the finish labeled in meters, and the hurdles spaced equally. The sequence below assumes that setup.

**Practices used (NAEP 2026 mathematical practices + NRC Procedural Fluency), in order**

1. **Representing** (NAEP)
   - Read the diagram as a number line, a picture or a table. Find the labeled positions, such as the first and last hurdle, and count the hurdles.
   - Turn the picture into numbers. One example is "first hurdle at 13 m, last hurdle at 85 m, 9 hurdles."

2. **Mathematical Modeling** (NAEP)
   - Treat the track as a real-world situation. Equal spacing between hurdles means the hurdles split a known length into equal parts.
   - Choose the model: spacing = (distance from first to last hurdle) / (number of gaps).

3. **Abstracting and Generalizing** (NAEP)
   - See that the number of gaps is one less than the number of hurdles (n hurdles make n - 1 gaps). This "fencepost" structure is the main idea that stops the usual off-by-one mistake.

4. **Procedural Fluency** (NRC strand)
   - Do the arithmetic correctly and efficiently. Subtract the positions to get the total span, then divide by the number of gaps. For example, (85 - 13) / 8 = 9 m.

5. **Justifying and Proving** (NAEP), optional check
   - Check the answer by adding the spacing step by step from the first hurdle. It should land on the last hurdle, or on the finish if that is given. Then write the answer in meters.

**Compact order:** Representing -> Mathematical Modeling -> Abstracting & Generalizing -> Procedural Fluency -> (Justifying & Proving as a check).

**Core practices:** Representing, Abstracting & Generalizing (the n - 1 gaps) and Procedural Fluency. Modeling is light here, and Justifying is only a self-check. Collaborative Mathematics does not apply to an individual item like this.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

**Why:**
- The question gives no numbers. Everything needed to answer it is in the diagram: hurdle positions, distance labels and how many hurdles there are. The main thing a student must do is read that picture and turn it into quantities.
- Once those are pulled out correctly, the rest is short. The n - 1 gaps idea and one subtraction plus one division follow almost directly from a well-read diagram.
- Most errors on this kind of item come from reading the figure wrong. Students use the wrong labels, miscount the hurdles, or don't see that the marked distances are between hurdles and not from the start.

**Close second:** Abstracting and Generalizing, for seeing that n hurdles make n - 1 equal gaps. If the diagram shows only the first and last hurdle positions and the student has to work out the number of gaps, this becomes the deciding step. Procedural Fluency is needed, but it is routine here, so it is not the major practice.

*(This answer depends on the missing diagram. Suppose the figure labels the distance between two neighboring hurdles directly. Then Representing is almost the whole task.)*

---

## Row 65 (problem_id 23822)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
The equation d = 3t represents the relationship between the distance (d) in inches that a snail is from a certain rock and the time (t) in minutes.
How many minutes does it take the snail to get 9 inches from the rock?
____ minutes
```

### Answer 1: practices in order

**Practices available:** the NAEP 2026 Mathematics Framework practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus Procedural Fluency from the NRC strands.

**Answer: 3 minutes**

## Practices used, in order

**1. Representing**
- Read the equation d = 3t in terms of the story. d is the snail's distance from the rock in inches, t is the time in minutes, and 3 is the rate (3 inches per minute).
- Turn the question "get 9 inches from the rock" into the symbols: it means d = 9, so the equation becomes 9 = 3t.
- This step moves between the words and the algebra, which is what Representing covers.

**2. Procedural Fluency (NRC)**
- Solve the one-step equation 9 = 3t by dividing both sides by 3, which gives t = 3.
- This is a routine procedure done accurately, so it is Procedural Fluency.

## Practices not needed
- **Mathematical Modeling:** the model (d = 3t) is already given. The student does not build one, choose assumptions or test a model against the situation. Writing the answer as "minutes" is just reading the units back, not modeling.
- **Abstracting and Generalizing:** this is one specific case. Nothing is generalized.
- **Justifying and Proving:** the item asks only for a number, not an explanation or argument.
- **Collaborative Mathematics:** this is an individual item.

**Sequence:** Representing → Procedural Fluency

### Answer 2: major practice

**Major practice: Representing**

The item really tests whether a student can read d = 3t in terms of the story. They need to see that "9 inches from the rock" is a value of d, not t, and set up 9 = 3t. Students who get this wrong usually do so at this step. The common mistake is substituting t = 9 and answering 27.

The Procedural Fluency step (9 ÷ 3 = 3) is a basic fact that almost any student who reaches it will get right, so it adds little difficulty. Representing is where the item tells students apart, so it is the main practice. Procedural Fluency is secondary.

---

## Row 69 (problem_id 25520)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
The graph of a proportional relationship contains the point with coordinates (3, 12). What is the constant of proportionality of the relationship?
____
```

### Answer 1: practices in order

**Problem:** The graph of a proportional relationship contains the point (3, 12). What is the constant of proportionality?

**Answer: 4** (y = 4x)

## Practices available
NAEP 2026 Mathematics Framework practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics. Added from the NRC strands: **Procedural Fluency**.

## Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the graph point (3, 12) as x = 3, y = 12. Links the phrase "graph of a proportional relationship" to the equation form y = kx, a line through the origin. This moves between the graphical, coordinate and symbolic forms. |
| 2 | **Abstracting and Generalizing** | Uses the general rule that in any proportional relationship the ratio y/x is the same constant k for every point. So one point is enough to find k. |
| 3 | **Procedural Fluency (NRC)** | Substitutes and computes: 12 = k * 3, so k = 12 / 3 = 4. |

**Order:** Representing -> Abstracting and Generalizing -> Procedural Fluency

## Practices not needed
- **Justifying and Proving:** The task asks only for a value, not an argument. At most, a student might check that 4 * 3 = 12.
- **Mathematical Modeling:** There is no real-world context to turn into math.
- **Collaborative Mathematics:** This is an individual item.

**Note:** Steps 1 and 2 are light here. For a student who has memorized "k = y/x," the item comes down almost entirely to Representing (reading the point) followed by Procedural Fluency (dividing). Abstracting and Generalizing is the most debatable of the three. You could drop it, or fold it into Representing, if your coding scheme needs fewer labels.

### Answer 2: major practice

**Major practice: Representing**

**Why Representing:** The hard part of this item is reading the graph point (3, 12) and seeing that it encodes the relationship y = kx, with x = 3 and y = 12. That means moving from a graph or coordinate representation to a symbolic one. A student who can make that move gets the answer. A student who can't has no way to start.

**Why not Procedural Fluency:** The computation is a single, trivial division, 12 / 3 = 4. It is needed, but it doesn't separate students who understand the problem from those who don't. A wrong answer here almost always comes from misreading what the point means, such as answering 3/12 = 1/4 or 12 - 3 = 9, not from a division error. All of those are Representing errors.

**Why not Abstracting and Generalizing:** Knowing that y/x is constant for every point helps, but on this item it is used as a known fact, not built. That makes it a supporting role.

**Ranking:** Representing (major) > Procedural Fluency (minor) > Abstracting and Generalizing (minor)

---

## Row 70 (problem_id 24963)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the constant of proportionality?
____ sale dollars per original dollar
```

### Answer 1: practices in order

**Note:** The problem text only gives the question ("What is the constant of proportionality? ____ sale dollars per original dollar"). The table, graph or equation that relates original prices to sale prices is not included. So the analysis below describes the general solution path, and I can't give the numerical answer.

## Practices used (NAEP 2026 Mathematical Practices + NRC Procedural Fluency)

The NAEP 2026 framework lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Here is the order I'd expect for this item:

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Read the given representation (table, graph or equation). Identify the input as the *original price* (x) and the output as the *sale price* (y). Use the unit label "sale dollars per original dollar" to see that k = y / x, not x / y. |
| 2 | **Abstracting and Generalizing** (NAEP) | See the relationship as proportional, y = kx, where one ratio holds for every pair. That means any single pair (or the point at x = 1 on a graph) gives k. |
| 3 | **Procedural Fluency** (NRC) | Compute the ratio accurately: divide sale price by original price (for example, 15 / 20 = 0.75), simplify, and write it as a decimal or fraction. |
| 4 | **Justifying** (NAEP, light use, optional) | Check that the same ratio holds for a second pair, or that the graph passes through the origin, to confirm the relationship really is proportional. |
| 5 | **Mathematical Modeling** (NAEP, interpretation step, optional) | Read k in context: for example, k = 0.75 means each original dollar becomes $0.75 on sale, which is a 25% discount. |

**Core sequence:** Representing → Abstracting/Generalizing → Procedural Fluency. Justifying and the modeling interpretation are optional checks that come after.

**Not used:** Collaborative Mathematics. This is an individual item.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The main work in this item is reading the given representation correctly. The student has to look at the table, graph or equation, decide which quantity is "sale" and which is "original," and use the unit label ("sale dollars per original dollar") to set k = sale / original instead of the reverse. That reading step is where students are most likely to go wrong. For example, they might flip the ratio, misread a graph point, or not see that the value at x = 1 is k.

The other practices play smaller roles:
- **Procedural Fluency:** the computation is just one division, such as 15 / 20 = 0.75. It's needed but short.
- **Abstracting and Generalizing:** the item already says the relationship is proportional ("the constant of proportionality"), so students don't have to work that out themselves.

Caveat: if the hidden stimulus gives the prices as a word problem or a percent discount rather than a table or graph, the item depends more on computation. In that case I'd pick **Procedural Fluency** as the major practice.

---

## Row 72 (problem_id 27276)

- **predicted_practice:** Representing
- **claude_top_practice:** Procedural Fluency

### Problem

```text
What is the value of c?
____
```

### Answer 1: practices in order

**Note first:** the problem as given ("What is the value of c?" followed by an answer blank) is missing what *c* refers to. There is no equation, figure, table or pattern. The original item almost certainly had a stimulus that didn't come through, for example an equation like `3c + 5 = 20`, a diagram with an unknown angle or side labeled *c*, or a pattern or table. So I can't pin the practices down exactly. Below is the most likely sequence for a typical "find the value of c" item. Send me the missing stimulus and I'll tighten it.

**Practices used** (NAEP mathematical practices, plus NRC procedural fluency):

1. **Representing (NAEP).** Read the given equation or figure and turn it into a usable mathematical form. For example, read the diagram as "the angles sum to 180°, so c + 65 + 40 = 180", or recognize that *c* is the unknown in the given equation.
2. **Procedural fluency (NRC).** Carry out the solving steps accurately and efficiently: combine like terms, apply inverse operations to isolate *c*, and do the arithmetic. This is where most of the work in this item happens.
3. **Mathematical reasoning (NAEP), optional and light.** Check that the value makes sense, either by substituting *c* back in or by confirming it fits the figure or context. This is usually implicit in a short fill-in-the-blank item.

**Order:** Representing → Procedural fluency → (Reasoning to check).

**Practices that probably don't apply:**
- *Abstracting and generalizing*: the item asks for one value, not a general rule. This changes if *c* is defined by a pattern, such as "the c-th term".
- *Modeling*: no real-world context is mentioned. This changes if the missing stimulus is a word problem, in which case Modeling would replace Representing as step 1.
- *Collaborative mathematics*: this is an individual assessment item.

**Short version:** Representing → Procedural fluency, with an optional reasoning check. This depends on the missing stimulus.

### Answer 2: major practice

**Procedural fluency (NRC)**, with a caveat.

It's a bare "find the value of c" item with one numeric answer. Most of the work and most of the ways to get it wrong are in the solving steps: isolating *c*, using inverse operations and doing the arithmetic correctly. Representing comes first, but it's usually a quick step of reading off a given equation or relationship. Reasoning is only an optional check.

**Caveat:** the problem text is missing its stimulus, so this depends on what *c* is.
- If *c* comes from a diagram where you have to work out the relationship yourself (for example, an unknown angle that needs a geometric property), **Representing** could be the main practice.
- If it's a word problem, **Modeling** could be.

For a typical equation-solving item, I'd still pick procedural fluency.

---

## Row 73 (problem_id 27019)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
All of the points in the picture are on the same line.
[image]
Find the slope of the line.
____
```

### Answer 1: practices in order

**Note:** The picture isn't in the text I have, so I can't give the numeric slope. The way the problem is solved, and the practices it needs, are the same for any set of points on a line.

**NAEP mathematical practices (2026 framework):** Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics (not assessed). I've added **Procedural Fluency** from the NRC strands of proficiency.

### Practices needed, in order

1. **Representing**
   - Read the picture: find the given points, either on a coordinate grid or as labeled ordered pairs.
   - Turn the picture into numbers: write two or more points as (x1, y1) and (x2, y2).
   - Read how the picture shows "the same line": the points lie in a straight line, so they share one constant rate of change.

2. **Abstracting and Generalizing**
   - See that slope means "change in y over change in x" (rise over run): m = (y2 - y1) / (x2 - x1).
   - Because every point is on the same line, the ratio is the same for *any* pair of points. That means the student can pick whichever two are easiest, such as points with integer coordinates or points where a coordinate is 0.
   - This step takes the general idea of slope as a constant rate and applies it to this particular picture.

3. **Procedural Fluency (NRC)**
   - Do the arithmetic correctly: subtract the y-values and the x-values in the same order, keep the signs right (a line that falls from left to right has a negative slope), then divide and simplify the fraction.
   - Write the answer in the blank as a simplified number or fraction.

### Practices not needed
- **Justifying and Proving:** the problem asks only for a value, not an argument. At most, a student might check the result with a third point. That is a light self-check, not a required step.
- **Mathematical Modeling:** there is no real-world situation to model. The problem is purely about a graph or set of coordinates.
- **Collaborative Mathematics:** this is an individual item, and NAEP doesn't assess this practice.

### Summary order
**Representing → Abstracting and Generalizing → Procedural Fluency**

### Answer 2: major practice

**Major practice: Representing**

**Why:**
- All the information is in the picture. The main thing the student has to do is turn a graphical representation (points on a line) into a numerical one (coordinates, then rise over run). If the student misreads the picture, the answer will be wrong however good their arithmetic is.
- The other two practices are smaller here:
  - **Abstracting and Generalizing:** this is just recalling the slope formula and the fact that slope is constant along a line. That is standard knowledge at this level, not real generalizing.
  - **Procedural Fluency:** this is one short subtraction-and-divide calculation. It matters, but it isn't what makes the item hard.

**If you want a backup tag:** **Procedural Fluency** comes second. If the picture labels the points' coordinates directly, there is less to read off the graph, and the item becomes mostly a "plug into the slope formula" calculation. In that case Procedural Fluency could reasonably be the major practice instead.

---

## Row 75 (problem_id 33653)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Solve the problem below.
21 is what percentage of 30?
____ %
```

### Answer 1: practices in order

**Problem:** 21 is what percentage of 30?  **Answer: 70%**

The NAEP mathematical practices are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added NRC's Procedural Fluency to that list. This problem needs only two of these practices, used in this order:

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Turn the words into math. "21 is what percent of 30" becomes 21 = (p/100) × 30, or the proportion 21/30 = p/100. The student has to see that 30 is the whole (the base) and 21 is the part. |
| 2 | **Procedural Fluency (NRC)** | Do the arithmetic correctly: 21 ÷ 30 = 0.7, then 0.7 × 100 = 70. Another route is scaling the fraction: 21/30 = 7/10 = 70/100. Answer: **70%**. |

**Practices that don't apply:**
- **Mathematical Modeling:** there is no real-world situation to model. The problem is already stated as a bare relationship between numbers.
- **Abstracting and Generalizing:** the student doesn't need to find a pattern or a general rule. They only apply the part/whole × 100 relationship once.
- **Justifying and Proving:** the student isn't asked to explain or defend the answer. A quick check (70% of 30 = 21) is just part of fluent computation.
- **Collaborative Mathematics:** this is a problem solved alone.

**Summary:** Representing → Procedural Fluency. Representing is the main step, because the most common mistake is setting up 30/21 instead of 21/30.

### Answer 2: major practice

**Major practice: Representing**

The key step is turning "21 is what percentage of 30?" into the right relationship, 21/30 = p/100. That means seeing 30 as the whole and 21 as the part. Most wrong answers come from this step: students divide 30 by 21, or they mix up the part and the whole. The arithmetic afterward (21 ÷ 30 = 0.7, so 70%) is short and routine. It uses friendly numbers that reduce to 7/10.

Procedural Fluency is a close second because this is a routine item. If you think the translation from words is automatic for most students at this level, you could pick Procedural Fluency instead. Even so, a student who sets up the right ratio almost always gets the problem right, and one who sets it up wrong can't get it right. That is why I would pick **Representing**.

---

## Row 76 (problem_id 351353)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
Find the answer. Draw a diagram, if needed.
A set of books that are each 1.5 inches wide are being organized on a bookshelf that is 36 inches wide. How many books can fit on the shelf?
____ books
```

### Answer 1: practices in order

**Answer: 24 books** (36 ÷ 1.5 = 24)

**Practices in the order a student would use them**

The NAEP 2026 Mathematics Framework names five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added Procedural Fluency from the NRC's *Adding It Up* strands, as you asked.

1. **Mathematical Modeling (setting up the problem).** The student turns the real situation into a math question. They need to see that "how many 1.5-inch books fit in 36 inches" asks how many groups of 1.5 fit into 36. That means division (or repeated addition) is the right operation.

2. **Representing.** The problem says "Draw a diagram, if needed." The student shows the situation as a diagram (a 36-inch shelf split into 1.5-inch segments, or a number line jumping by 1.5) and as the expression 36 ÷ 1.5. Going from the words to a picture or an equation is the core of this practice.

3. **Procedural Fluency (NRC).** The student does the calculation correctly and efficiently. Dividing by a decimal is the main computing step. One way is to rewrite it as 360 ÷ 15 = 24. Another is to notice that 2 books take 3 inches, so 36 ÷ 3 = 12 pairs, and 12 × 2 = 24 books.

4. **Mathematical Modeling (reading the answer in context).** The student checks that the result makes sense for the situation. A count of books has to be a whole number. Here 24 comes out exactly, so no rounding down is needed and no space is left over.

5. **Justifying and Proving (optional check).** The student can confirm the answer by multiplying back: 24 × 1.5 = 36 inches. The item doesn't ask for this, so it's a minor or optional step.

**Not needed:** Abstracting and Generalizing (the student doesn't extend a pattern or form a general rule) and Collaborative Mathematics (it's a single-student item).

**Short version:** Modeling → Representing → Procedural Fluency → Modeling (interpret) → (Justifying, optional)

### Answer 2: major practice

**My pick for the major practice: Mathematical Modeling**

**Why:** The hard part is seeing that "how many 1.5-inch books fit on a 36-inch shelf" is a division question: how many 1.5s are in 36. A student who sets that up has basically solved the problem. A student who doesn't (for example, multiplies 36 × 1.5, or subtracts) gets it wrong no matter how well they compute. Students most often miss items like this at the setup step, not the arithmetic.

**Runner-up: Procedural Fluency.** Dividing by a decimal (36 ÷ 1.5) takes real computing skill at this grade level. If the item were scored for computation errors, this would be the second most likely place for a student to fail.

**Why not Representing:** The diagram is offered only "if needed." It helps students who struggle with the setup, but the item doesn't require a representation. So it supports the modeling step rather than being the main demand.

---

## Row 78 (problem_id 30276)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
Diego made 6 boxes of spaghetti to feed 20 people who attended his dinner party. Next time, 50 people are coming! How many boxes of spaghetti should Diego buy to feed all those people?
____ boxes of spaghetti
```

### Answer 1: practices in order

**Problem:** Diego made 6 boxes of spaghetti for 20 people. How many boxes does he need for 50 people?

**Answer: 15 boxes.** The rate is 6 boxes ÷ 20 people = 0.3 box per person, and 0.3 × 50 = 15. You can also scale: 50 ÷ 20 = 2.5, and 6 × 2.5 = 15.

---

## Practices available

The **NAEP Mathematics Framework** (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematical Discourse

**Procedural Fluency** is added from the NRC strands of mathematical proficiency (*Adding It Up*, 2001).

---

## Practices used, in order

| Step | Practice | What the student does on this problem |
|---|---|---|
| 1 | **Mathematical Modeling** (set up the model) | Reads the real-world situation and sees that boxes needed grow in proportion to the number of people. This assumes each person eats about the same amount. The context question becomes a proportion question. |
| 2 | **Representing** | Turns the situation into a math form: the ratio 6 boxes : 20 people, the proportion 6/20 = x/50, a ratio table (20 → 6, 10 → 3, 50 → 15), or a unit rate (0.3 box per person). |
| 3 | **Abstracting and Generalizing** (light use) | Pulls out the rule that holds for any number of people: boxes = 0.3 × people, or "multiply by the same scale factor, 2.5". This lets one known case be applied to a new one. |
| 4 | **Procedural Fluency** (NRC) | Does the arithmetic correctly and efficiently: 6 ÷ 20 = 0.3 and 0.3 × 50 = 15. Or 50 ÷ 20 = 2.5 and 6 × 2.5 = 15. Or cross-multiply: 20x = 300, so x = 15. |
| 5 | **Mathematical Modeling** (interpret and validate) | Takes the result back to the situation: 15 is a whole number of boxes, so no rounding up is needed. It is reasonable because 2.5 times as many people need 2.5 times as many boxes. |

### Short form of the order
**Mathematical Modeling → Representing → Abstracting and Generalizing → Procedural Fluency → Mathematical Modeling (interpret)**

### Practices not needed
- **Justifying and Proving:** the item asks only for a numeric answer, not an argument or explanation.
- **Collaborative Mathematical Discourse:** this is an individual assessment item with no group discussion.

### Core vs. supporting
- **Core:** Mathematical Modeling, Representing, Procedural Fluency.
- **Supporting:** Abstracting and Generalizing. A student who scales the ratio table directly may barely use it.

### Answer 2: major practice

**Major practice: Mathematical Modeling**

**Why I chose it:**
- **It is the hardest step.** The problem is a real-world situation, not a ready-made equation. The student has to see that spaghetti scales in proportion to the number of people, which assumes a fixed amount per person. Then they turn "6 boxes for 20 people → ? for 50 people" into a proportional model. Students who miss this usually make the classic additive error: 50 − 20 = 30 more people, so 6 + 30 = 36 boxes. Another version is "add 3 boxes per extra 10 people" done wrong.
- **It frames the whole solution.** Modeling starts the solution (setting up the proportional model) and ends it (checking that 15 is a sensible whole number of boxes for 2.5 times as many people).
- **The other practices are smaller here.**
  - Representing (writing 6/20 = x/50 or a ratio table) follows almost directly once the model is chosen.
  - Procedural Fluency (6 ÷ 20 × 50 = 15) is simple arithmetic.
  - Abstracting and Generalizing is used only lightly.

**Runner-up:** Representing. One could argue for it if the item is seen mainly as "write the proportion". Even so, deciding that a proportion is the right representation is itself a modeling decision. That is why Mathematical Modeling is the main practice.

---

## Row 84 (problem_id 31058)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
A snail travels 10 cm in 4 minutes. At this rate:
How long will it take the snail to travel 24 cm?
____ minutes
```

### Answer 1: practices in order

**Answer: 9.6 minutes**

## Practices available

**NAEP Mathematical Practices (2026 framework):**
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

**NRC strand you asked me to add:** Procedural Fluency, meaning you carry out procedures accurately, efficiently and flexibly.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (light use) | Reads "at this rate" as a constant, proportional relationship between distance and time. That turns the story into a mathematical model, distance ∝ time. |
| 2 | **Representing** | Writes the relationship in a usable form: a proportion (10/4 = 24/x), a unit rate (2.5 cm per minute, or 0.4 min per cm), or a ratio table (10 cm → 4 min, 20 cm → 8 min, 2 cm → 0.8 min, 24 cm → 9.6 min). |
| 3 | **Procedural Fluency** (NRC) | Does the computation: x = 24 × 4 / 10 = 96 / 10 = 9.6. Equivalently, 24 ÷ 2.5 = 9.6, or 24 × 0.4 = 9.6. This needs fluent work with decimals and division. |
| 4 | **Justifying** (optional, light) | Checks that the answer makes sense. 24 cm is a bit less than 2.5 times 10 cm, so the time should be a bit less than 2.5 × 4 = 10 minutes. 9.6 fits. |

## Practices not needed

- **Abstracting and Generalizing:** the student doesn't need to form a general rule beyond this single rate.
- **Collaborative Mathematics:** this is an individual item.

## Summary
The core sequence is **Modeling → Representing → Procedural Fluency**. A light Justifying check at the end is optional. The main work is in Representing (setting up the proportion or unit rate) and Procedural Fluency (the decimal arithmetic).

### Answer 2: major practice

**Major practice: Representing**

Representing is the deciding step in this problem. The student has to turn "10 cm in 4 minutes, at this rate" into a usable form: a proportion (10/4 = 24/x), a unit rate (2.5 cm/min or 0.4 min/cm), or a ratio table. Once that's set up correctly, the rest is routine.

- **Why not Procedural Fluency:** the arithmetic (24 × 4 ÷ 10 = 9.6) is short and simple. Decimals can trip some students, but most errors on this kind of item come from setting up the relationship wrong. A common one is inverting the ratio and getting 24 × 10 ÷ 4 = 60. Fluency comes second.
- **Why not Mathematical Modeling:** the context is already clean and the item states the proportional assumption outright ("at this rate"). Very little modeling is needed.
- **Why not Justifying:** only an optional sense check.

If you need one label for this item, use **Representing**. Procedural Fluency is the secondary practice.

---

## Row 89 (problem_id 33334)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Solve the problem below.
18 is 120% of what number?
____
```

### Answer 1: practices in order

**Problem:** 18 is 120% of what number?

**Answer:** 15

## Practices to use, in order

The NAEP Mathematics Framework (2026) lists five mathematical practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, and (5) Collaborative Mathematics. I've added NRC **Procedural Fluency** (one of the five strands of mathematical proficiency in *Adding It Up*, 2001).

This is a short, one-step percent problem with no context, so it only needs a few practices:

| Order | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the sentence into math. "18 is 120% of what number" becomes 18 = 1.20 × n (or the proportion 18/n = 120/100). The student has to see that 18 is the *part*, the unknown is the *whole*, and that 120% can be written as 1.2 or 6/5. |
| 2 | **Procedural Fluency** (NRC) | Solves the equation quickly and correctly: n = 18 ÷ 1.2 = 15 (or cross-multiply: 120n = 1800, so n = 15; or with fractions, 18 × 5/6 = 15). |
| 3 | **Justifying** (NAEP, light use) | Checks the answer: 120% of 15 = 1.2 × 15 = 18 ✓. It also makes sense, because a percent over 100% means 18 should be *greater* than the unknown, and 15 < 18. |

## Practices not used

- **Abstracting and Generalizing:** the student doesn't need to spot a pattern or general rule. This is one specific computation.
- **Mathematical Modeling:** there is no real-world situation to model. It is a bare number sentence.
- **Collaborative Mathematics:** this is a solo item.

**Summary:** Representing → Procedural Fluency → (optional) Justifying. Representing is the main step: most errors come from setting it up backwards (for example, computing 120% of 18 = 21.6). Once the equation is set up correctly, procedural fluency does the rest.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The hard part of "18 is 120% of what number?" is the setup. The student has to read the sentence correctly: 18 is the *part*, the unknown is the *whole*, and 120% is the multiplier, which gives 18 = 1.2 × n. The usual mistake is setting it up the wrong way round, for example finding 120% of 18 = 21.6, or putting 18 and n in the wrong places in the proportion. That is a representation error, not a computation error.

Once the equation is right, the procedure is just one division (18 ÷ 1.2 = 15). Procedural Fluency is a close second because it is still needed, but it is the routine step. Whether a student gets this item right depends mainly on whether they can represent it correctly.

---

## Row 92 (problem_id 37276)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What fraction of the daily recommended value of iron is in 1 cup of oatmeal?
____
```

### Answer 1: practices in order

## Practices to use, in order

The problem refers to a nutrition label for oatmeal that isn't in the text you gave me. The label would show the serving size and the iron "% Daily Value" per serving. With that in mind, here is the order of practices a student would use.

The NAEP Mathematics Framework (2026) lists these practices: **Representing**, **Abstracting and Generalizing**, **Justifying and Proving**, **Mathematical Modeling** and **Collaborative Mathematics**. I've added **Procedural Fluency** from the NRC's *Adding It Up* strands, as you asked.

| Step | Practice | What the student does in this problem |
|---|---|---|
| 1 | **Representing** (NAEP) | Reads the nutrition label, which is a table or graphic, and finds the needed values: the serving size (for example, ½ cup or 1 cup) and the iron % Daily Value per serving. The student also has to see that "% of daily recommended value" is a part-of-a-whole quantity that can be written as a fraction. |
| 2 | **Procedural Fluency** (NRC) | If the serving size isn't 1 cup, scales the percentage to 1 cup. For example, if ½ cup gives 10%, then 1 cup gives 2 × 10% = 20%. Then rewrites the percent as a fraction (20% = 20/100) and simplifies it (= 1/5). These are routine steps that need to be done accurately and efficiently. |
| 3 | **Representing** (NAEP), final move | Gives the answer in the form the question asks for, which is a fraction rather than a percent or a decimal, and checks that it makes sense as part of the daily total (it should be less than 1). |

### Practices that are not needed
- **Abstracting and Generalizing:** the student doesn't need to find a general pattern or rule. This is a single, specific calculation.
- **Justifying and Proving:** the student isn't asked to give reasons or build an argument.
- **Mathematical Modeling:** at most this is a very small step. The context is real-world, but the student only reads values off the label and doesn't have to make modeling assumptions. Some coders might tag the serving-size scaling as light modeling, but it fits better under Procedural Fluency.
- **Collaborative Mathematics:** it doesn't apply to an individual assessment item.

### Summary of the order
**Representing → Procedural Fluency → Representing (stating the answer as a fraction)**

Representing is the main practice because the item mostly tests whether the student can pull the right number from the label and turn a percent into a fraction. Procedural Fluency handles the arithmetic: scaling to 1 cup, then converting the percent to a fraction and simplifying.

### Answer 2: major practice

## Major practice: **Representing** (NAEP)

If I had to pick one, it would be Representing. The problem mostly tests whether the student can:

1. **Read the nutrition label**, a table or graphic, and find the right row and value: iron, % Daily Value, and the serving size it applies to.
2. **Move between representations.** The label gives the amount as a percent of the daily recommended value, and the question asks for a fraction. Seeing that "% of daily value" is a part-of-a-whole amount that can be written as a fraction (for example, 20% → 20/100 → 1/5) is the main idea of the item.

Procedural Fluency is needed too, for scaling the serving size and simplifying the fraction. But the arithmetic is short and routine, so it supports the main step rather than driving it. A student who gets the representation step wrong, by reading the wrong row, ignoring the serving size, or giving a percent instead of a fraction, will get the item wrong even with perfect arithmetic. That is why Representing is the better choice for the major practice.

---

## Row 93 (problem_id 297138)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
A teacher asked all the students in one class how many minutes it takes them to get to school. Here is a table of their responses:
[Table:
20 | 10 | 15 | 8 | 5 | 15 | 10 | 5
20 | 5 | 15 | 10 | 3 | 10 | 18 | 5
25 | 5 | 5 | 12 | 10 | 30 | 5 | 10]
What fraction of the students in this class say it takes them 5 minutes to get to school?
____
```

### Answer 1: practices in order

## The practices to choose from

The 2026 NAEP Mathematics Framework names five mathematical practices:

1. **Representing**: reading, making and moving between forms of a mathematical object, such as tables, symbols, graphs and words.
2. **Abstracting and Generalizing**: finding structure and patterns and stating general relationships.
3. **Justifying and Proving**: building and checking mathematical arguments.
4. **Mathematical Modeling**: using math to describe and answer a real-world situation.
5. **Collaborative Mathematics**: working with others on mathematical ideas.

As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands. It means carrying out procedures such as counting, computing and simplifying accurately, efficiently and flexibly.

## The problem and its answer

- There are 3 rows of 8 responses, so **24 students** in all.
- Responses equal to 5: row 1 has 2, row 2 has 2 and row 3 has 3, so **7 students**.
- The fraction is **7/24**. It is already in simplest form.

## Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (interpreting a representation) | Reads the table: each cell is one student's answer in minutes. The question asks for a fraction of the *students*, not of the minutes. So the number of cells is the whole, and the cells containing 5 are the part. |
| 2 | **Procedural Fluency** (counting) | Counts all the entries (3 × 8 = 24). Then counts the 5s carefully (2 + 2 + 3 = 7) without missing or double-counting any, for example by not confusing 5 with 15 or 25. |
| 3 | **Representing** (changing the representation) | Turns the count into the symbolic form the question wants: part / whole = 7/24. |
| 4 | **Procedural Fluency** (simplifying) | Checks whether 7/24 can be reduced. 7 is prime and does not divide 24, so 7/24 is the final answer. |

**Short sequence:** Representing → Procedural Fluency → Representing → Procedural Fluency. If you collapse the repeats, it is **Representing → Procedural Fluency**.

## Practices that are not needed

- **Abstracting and Generalizing**: the student finds no general pattern or rule. It is a single count from data.
- **Justifying and Proving**: the student gives no argument or justification.
- **Mathematical Modeling**: the context is real-world, but the student doesn't build or test a model. The question is a direct data lookup with a fraction. At most, the step "fraction of students = count / total" is a very light modeling idea, and it is better counted as part of Representing.
- **Collaborative Mathematics**: this is an individual item.

**Main practice:** Representing, because reading the table and writing the result as a fraction is where students usually go wrong. **Supporting practice:** Procedural Fluency, for the accurate counting and the simplest-form check.

### Answer 2: major practice

## Major practice: Representing

If I had to pick just one, I'd pick **Representing**. Here is why:

- **The task depends on reading a representation.** The data comes as an unlabeled table of 24 values. The student has to see that each cell is one student, so the number of cells (24) is the whole. The cells showing 5 (there are 7) are the part.
- **The answer must be written in a different form.** The student has to turn a count from the table into a symbolic fraction, part/whole = **7/24**. Moving from a table to a fraction is the core of Representing.
- **Most mistakes happen here.** The usual errors come from reading the representation wrongly, not from the arithmetic:
  - using the number of distinct values as the denominator
  - using the sum of the minutes as the denominator
  - giving the count (7) instead of a fraction
  - writing 7/17 (5s compared with the other students) instead of 7/24
- **Procedural Fluency plays a supporting role.** Counting 24 entries and 7 fives, and checking that 7/24 can't be simplified, is routine work. It is needed, but it is not what the item is mainly testing.

**Answer:** Representing is the major practice, and Procedural Fluency is secondary.

---

## Row 95 (problem_id 37735)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What fraction of 1/2 is 1/3?
Enter your answer as an exact fraction.
____
```

### Answer 1: practices in order

**Problem:** What fraction of 1/2 is 1/3? (Answer: **2/3**)

**Practice set used:** the NAEP 2026 Mathematics Framework practices (Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics), plus **Procedural Fluency** from the NRC's *Adding It Up* strands.

## Practices in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the words "what fraction of 1/2 is 1/3" into symbols: find *x* such that *x* · (1/2) = 1/3. That means *x* = (1/3) ÷ (1/2). The student has to read "of" as multiplication and see that 1/2 is the whole (the referent), not 1/3. This is where most errors happen; a common one is computing (1/2) ÷ (1/3) = 3/2 instead. |
| 2 | **Procedural Fluency** (NRC) | Carries out the fraction division correctly: (1/3) ÷ (1/2) = (1/3) × (2/1) = 2/3. The answer is already in lowest terms, so it can be entered as an exact fraction. |
| 3 | **Justifying and Proving** (NAEP), light and optional | Checks the result: (2/3) × (1/2) = 2/6 = 1/3. ✓ The student can also reason that the answer should be less than 1, because 1/3 < 1/2. This step is self-checking, not a formal proof. |

**Sequence:** Representing → Procedural Fluency → (Justifying and Proving)

## Practices not used
- **Abstracting and Generalizing:** the problem asks for no general rule or pattern.
- **Mathematical Modeling:** there is no real-world context to model.
- **Collaborative Mathematics:** this is an individual item.

**Main practices:** Representing (setting up the problem correctly) and Procedural Fluency (dividing the fractions). Justifying is a secondary check.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The hard part of this item is turning "What fraction of 1/2 is 1/3?" into the right expression: *x* · (1/2) = 1/3, so *x* = (1/3) ÷ (1/2). The student has to see that 1/2 is the whole (the referent) and that "of" means multiplication.

That is where students usually fail. A common mistake is setting it up backwards as (1/2) ÷ (1/3) = 3/2. Another is just subtracting, 1/2 − 1/3 = 1/6.

The calculation after that is a routine fraction division, (1/3) × 2 = 2/3. That makes Procedural Fluency a secondary practice. The item mainly tells apart students who can set up the relationship from those who can't, not students who can or can't divide fractions.

---

## Row 97 (problem_id 37464)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
The two triangles shown are similar. Find the value of a/b.
[image]
____
```

### Answer 1: practices in order

**Problem:** "The two triangles shown are similar. Find the value of a/b." (The figure isn't included, so I can't see the side lengths or where *a* and *b* sit. The practice sequence below holds for this kind of problem either way.)

### The practices available
The NAEP 2026 Mathematics Framework lists these mathematical practices:
1. **Representing:** moving between representations, such as reading a diagram and turning it into symbols or equations.
2. **Abstracting and Generalizing:** spotting the structure or general principle behind a specific situation.
3. **Justifying and Proving:** building or checking an argument for why a result holds.
4. **Mathematical Modeling:** turning a real-world situation into mathematics and interpreting the result.
5. **Collaborative Mathematics:** working with others (not assessed in individual items).

Added from the NRC's *Adding It Up* strands:
6. **Procedural Fluency:** carrying out procedures such as setting up and solving proportions, cross-multiplying and simplifying fractions accurately and efficiently.

### Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the figure: finds the matching vertices and angles of the two triangles and which sides correspond. Finds where *a* and *b* are and which known lengths match them. |
| 2 | **Abstracting and Generalizing** | Uses the general fact that similar triangles have proportional corresponding sides. Writes the scale-factor relation, e.g. a / (matching side) = b / (matching side) = k, or recognizes that a/b equals the ratio of the matching sides in the other triangle. |
| 3 | **Procedural Fluency (NRC)** | Does the arithmetic: sets up the proportion, cross-multiplies or uses the scale factor to find *a* and/or *b*, then forms a/b and simplifies the fraction. |
| 4 | **Justifying and Proving** (light, optional) | Checks the result: are the correct sides paired, and is a/b consistent with the scale factor and the other side ratios? This is a sanity check, not a formal proof. |

**Not needed:** Mathematical Modeling, because there is no real-world context. Collaborative Mathematics, because this is a single-student item.

### Summary
**Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving as a check)**

The main practices are Representing (reading the corresponding sides from the figure) and Procedural Fluency (solving the proportion and simplifying a/b). Abstracting and Generalizing connects them through the similarity principle. If you share the figure, I can work out the actual value of a/b.

### Answer 2: major practice

**Major practice: Representing**

That's where the real work of this problem is:

- **The main task is translating the figure.** The problem gives no equations, only a diagram. The student has to read which vertices, angles and sides of the two triangles match and turn that into a correct proportion involving *a* and *b*. Once the proportion is written correctly, the rest is routine.
- **This is where most students go wrong.** The usual mistake in similar-triangle items is pairing the wrong sides, especially when one triangle is rotated or flipped. That is a failure to read the figure correctly, not a failure of arithmetic or of knowing the rule.
- **The other practices play smaller roles:**
  - *Abstracting and Generalizing:* the rule that similar triangles have proportional sides is standard, recalled knowledge, so it is applied rather than discovered.
  - *Procedural Fluency:* cross-multiplying and simplifying a/b is short, simple arithmetic.
  - *Justifying and Proving:* only a quick check at the end.

**Runner-up:** Procedural Fluency. If the figure makes the matching sides obvious (same orientation, clearly labeled), the item mostly tests whether the student can compute and simplify the ratio, and Procedural Fluency would become the major practice. Seeing the figure would settle which case this is.

---

## Row 99 (problem_id 40512)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Justifying and Proving

### Problem

```text
Correct the error. What should the line actually be?
____
```

### Answer 1: practices in order

**Note first:** the problem as given is incomplete. It says "Correct the error. What should the line actually be?" followed by a blank. The line, graph, table, or worked solution that has the error is missing (it was probably an image). So I can't name the corrected line. What I can do is give the practice sequence that a "find and fix the error in a line" item calls for. If you send the missing figure or work, I can check each step against it.

### Practices available
- **NAEP Mathematical Practices (2026 framework):** Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics
- **Added from NRC (*Adding It Up*):** Procedural Fluency

### Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Reads the given line, whether it's a graph, an equation, or a table of points. Moves between forms, for example reading two points off the graph or turning the equation into slope-intercept form, so the line's slope and intercept can be compared with the conditions it should meet. |
| 2 | **Justifying and Proving** (error analysis) | Checks the given line against the correct one and finds exactly where they differ: a sign error in the slope, rise and run swapped, the wrong y-intercept, or a misplotted point. Explains why that step is wrong. This is the core practice in a "correct the error" item. |
| 3 | **Procedural Fluency** (NRC) | Recomputes accurately. Finds the slope (Δy/Δx), solves for b in y = mx + b, and simplifies to the final equation. |
| 4 | **Representing** (again) | Writes the corrected line in the form the question asks for, either as an equation or as a re-drawn graph. Checks it by plugging in the given points. |

**Not needed:** Mathematical Modeling, since there's no real-world context to model; Abstracting and Generalizing, since this is a single specific case with no pattern to extend; and Collaborative Mathematics, since the item is done alone.

**Short version:** Representing → Justifying and Proving → Procedural Fluency → Representing (verify).

If the missing part shows the error is only an arithmetic slip, Justifying and Proving becomes a light check and Procedural Fluency becomes the main practice. If the error is conceptual, for example a line drawn through the wrong points, Representing becomes more central.

### Answer 2: major practice

**Major practice: Justifying and Proving (error analysis).**

The item's core demand is "Correct the error." To answer, the student has to compare the given line with what it should be, find the step or feature that's wrong, and understand why it's wrong. That critique-and-justify step is what separates this item from a plain "write the equation of the line" question.

The other practices support that step:
- **Representing** is how the student reads the line and writes the answer.
- **Procedural Fluency** is the recomputation once the error is found.

Neither of those alone would let a student answer an error-correction item.

One caveat still applies: the line itself is missing from the problem text. If the missing part showed only a simple arithmetic slip, Procedural Fluency would compete for the top spot. Given how the item is framed, though, I'd label it **Justifying and Proving**.

---

## Row 100 (problem_id 297237)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
A teacher asked all the students in one class how many minutes it takes them to get to school. Here is a table of their responses:
[Table:
20 | 10 | 15 | 8 | 5 | 15 | 10 | 5
20 | 5 | 15 | 10 | 3 | 10 | 18 | 5
25 | 5 | 5 | 12 | 10 | 30 | 5 | 10]
What fraction of the students in this class say it takes them more than 10 minutes to get to school?
____
```

### Answer 1: practices in order

## The practices available

The NAEP 2026 Mathematics Framework names five mathematical practices:

1. **Representing**: reading, translating between and using representations such as tables, graphs, symbols and words.
2. **Abstracting and Generalizing**: finding structure or patterns and extending them beyond the given cases.
3. **Justifying and Proving**: building and checking mathematical arguments.
4. **Mathematical Modeling**: turning a real-world situation into a mathematical model, solving it and interpreting the result.
5. **Collaborative Mathematics**: working on mathematics with others.

As you asked, I've added one practice from the NRC (*Adding It Up*, 2001):

6. **Procedural Fluency**: carrying out procedures (counting, computing, simplifying) flexibly, accurately and efficiently.

## Practices needed, in order

**Step 1: Representing (reading the table and translating the question)**
- Read the table as raw data. Each of the 24 cells is one student's travel time, so the class has 3 x 8 = **24 students**.
- Turn the words into math: "more than 10 minutes" means a time **strictly greater than 10**, so the 10s are left out. "What fraction of the students" means (number of students with time > 10) / (total number of students).

**Step 2: Procedural Fluency (counting and computing)**
- Count the values greater than 10 in each row:
  - Row 1 (20, 10, 15, 8, 5, 15, 10, 5): 20, 15, 15 gives **3**
  - Row 2 (20, 5, 15, 10, 3, 10, 18, 5): 20, 15, 18 gives **3**
  - Row 3 (25, 5, 5, 12, 10, 30, 5, 10): 25, 12, 30 gives **3**
  - Total = **9**
- Write the fraction and simplify it: 9/24 = **3/8**.

**Step 3: Representing again (giving the answer in the requested form)**
- Turn the count back into the requested form, a fraction of the whole class: **3/8**.

## Practices not needed

- **Abstracting and Generalizing**: there is no pattern or rule to extend beyond the data.
- **Justifying and Proving**: the item asks for no argument or explanation. At most, a student might quickly check that the 10s are excluded and the three rows add up correctly.
- **Mathematical Modeling**: the context is real-world, but the student builds no model. They only read and count the given data.
- **Collaborative Mathematics**: this is an individual item.

## Summary

**Representing -> Procedural Fluency -> Representing**

**Answer: 9/24 = 3/8** of the students take more than 10 minutes to get to school.

### Answer 2: major practice

## Major practice: **Representing**

If I had to pick one, I would choose **Representing**.

**Why Representing comes first:**
- **The hard part is reading the data correctly, not doing the math.** The student has to see that the 3 x 8 table is raw data in which each cell is one student. That gives the denominator of **24**. It is not 3 rows or 8 columns.
- **The question has to be translated.** "More than 10 minutes" means **strictly greater than 10**, so the six 10s are left out. "What fraction of the students" means part/whole, which is count/24.
- **The likely mistakes are mistakes of representation:**
  - counting the 10s, which gives 15/24
  - using the wrong total
  - giving a count (9) or a time instead of a fraction
- **The answer has to be given back in the requested form,** as a fraction of the class: **3/8**.

**Why not Procedural Fluency:**
- It is clearly needed, but it plays a small part. The student only counts 9 values and simplifies 9/24 to 3/8, which is routine work.
- A student with weak fluency but a correct reading of the table would probably still get the answer. A student who misreads the table or the "more than" condition will get it wrong no matter how fluent they are.

**Answer: Representing is the major practice. Procedural Fluency is a secondary, supporting practice.**

---

## Row 102 (problem_id 40656)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
An area of 6 square yards is equal to 54 square feet. 9 square yards is equal to how many square feet?
____ square feet
```

### Answer 1: practices in order

**Problem:** 6 square yards = 54 square feet. How many square feet are in 9 square yards?

**Answer: 81 square feet.** (54 / 6 = 9 sq ft per sq yd, and 9 x 9 = 81.)

## Practices used, in order

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Problem Solving. I've added NRC's **Procedural Fluency** as a sixth.

1. **Representing (NAEP)**
   First, turn the sentence into a mathematical relationship. Write it as a ratio (6 sq yd : 54 sq ft) or as a proportion, 6/54 = 9/x. This sets up the problem as a fixed relationship between two units.

2. **Abstracting and Generalizing (NAEP)**
   Next, see that the relationship is a constant conversion rate. Every square yard equals the same number of square feet. Pulling the unit rate (54 / 6 = 9 sq ft per sq yd) out of this one example and applying it to any number of square yards is the key reasoning step.

3. **Procedural Fluency (NRC)**
   Then do the arithmetic correctly: 54 / 6 = 9, then 9 x 9 = 81. You could also cross-multiply, 6x = 486, so x = 81. These are routine whole-number steps, so fluency here means picking an efficient method and getting it right.

4. **Justifying and Proving (NAEP), minor and optional**
   Last, check that the answer makes sense. 9 sq yd is 1.5 times 6 sq yd, and 1.5 x 54 = 81, so the answer is consistent. It also matches the fact that 1 yd = 3 ft, so 1 sq yd = 9 sq ft. This only checks the answer, so it plays a small role.

**Not needed:** Mathematical Modeling, because the problem is already given in mathematical terms and there's no real-world situation to simplify. Collaborative Problem Solving also isn't needed, because it's a task done alone.

**Summary order:** Representing -> Abstracting and Generalizing -> Procedural Fluency -> (Justifying and Proving, as a check)

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

The problem is mostly about seeing that the example (6 sq yd = 54 sq ft) shows a constant conversion rate. Every square yard equals 9 square feet, and that rate holds for any amount. Once a student pulls the unit rate out of that one example and applies it to 9 square yards, the problem is essentially solved.

The other practices play smaller roles:
- **Representing** is light. The sentence turns directly into a ratio, so little translation is needed.
- **Procedural Fluency** is routine. The arithmetic is 54 / 6 = 9 and 9 x 9 = 81, which are basic whole-number facts. A student who misses this item is much more likely to have failed to see the proportional relationship than to have divided or multiplied wrong. For example, they might add 3 yards and 27 feet, or answer 54 + 3 = 57.
- **Justifying and Proving** is only an optional sanity check.

So the item mainly measures whether the student can generalize from a given instance to a constant rate. That makes **Abstracting and Generalizing** the major practice.

---

## Row 103 (problem_id 42388)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Another temperature scale frequently used in science is the Kelvin scale. In this scale, 0 is the lowest possible temperature of anything in the universe, and it is -273.15 degrees in the Celsius scale. Each 1 K is the same as 1°C so 10 K is the same as -263.15°C.
Water boils at 100°C. What is this temperature in K?
____ K
```

### Answer 1: practices in order

**Answer: 373.15 K**

The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added Procedural Fluency from the NRC's *Adding It Up* strands as a sixth.

Solving this problem takes three of them, in this order.

**1. Representing**
The relationship is given only in words. "0 K is −273.15 °C" and "1 K is the same size as 1 °C" have to be turned into something you can calculate with. That could be a pair of points on two parallel number lines, a small table, or a shift such as "°C = K − 273.15." Translating the verbal description into a usable form is the first step.

**2. Abstracting and Generalizing**
The text gives two specific cases: 0 K = −273.15 °C and 10 K = −263.15 °C. From these the student has to pull out the general rule: the two scales differ by a constant 273.15, so K = °C + 273.15. The rule must also be applied in the direction the text didn't show, Celsius to Kelvin rather than Kelvin to Celsius. Going from worked examples to a reversible rule is the abstracting step.

**3. Procedural Fluency (NRC)**
Once the rule is set up, what's left is an accurate decimal addition: 100 + 273.15 = 373.15. This means lining up the decimals correctly and not sliding into the common mistake of subtracting (100 − 273.15 = −173.15) or rounding to 373.

**Practices not needed**
- **Mathematical Modeling**: the model (a constant offset) is given in the text, so the student doesn't have to build or refine one from a real-world situation.
- **Justifying and Proving**: no argument or explanation is requested, only a number.
- **Collaborative Mathematics**: this is a single-student item.

**Order:** Representing → Abstracting and Generalizing → Procedural Fluency

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

This is the step that decides whether a student gets the problem right:

- **The text never states the rule.** It only gives two specific cases (0 K = −273.15 °C and 10 K = −263.15 °C). The student has to see the pattern behind them: the scales differ by a constant offset, so K = °C + 273.15.
- **The rule has to be used in the other direction.** Both examples go from Kelvin to Celsius, but the question goes from Celsius to Kelvin. To reverse the relationship correctly (add 273.15, not subtract it), the student needs the general rule, not just the two examples.
- **This is where the wrong answers come from.** Students who don't generalize correctly tend to answer −173.15 (subtracting) or copy the given pattern without adjusting it. Errors in the arithmetic itself are much less common.

The other two practices play a smaller role:

- **Representing** prepares the information, but there isn't much to represent: two sentences describing a shift.
- **Procedural Fluency** is just one decimal addition, 100 + 273.15 = 373.15. Once the rule is known, that's routine.

So the item mostly tests whether a student can pull a general relationship out of worked examples and apply it to a new case.

---

## Row 105 (problem_id 43208)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
Andre picks blocks out of a bag 60 times and notes that 43 of them were green.
What should Andre estimate for the probability of picking out a green block from this bag?
____
```

### Answer 1: practices in order

**Answer:** 43/60 (about 0.717, or roughly 72%)

## Practices used

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added NRC's Procedural Fluency as a sixth.

Here is the order a student would use them in:

### 1. Mathematical Modeling (main practice)
The student has to see that 60 real draws, 43 of them green, can stand in for the bag's unknown contents. The bag is modeled as a random process, and the observed relative frequency is used as the estimate of the true probability. This is the key step. Students who miss it often say "I can't know, I don't know what's in the bag," or they try a theoretical model that doesn't fit, such as "green or not green, so 1/2."

### 2. Representing
Next, the student turns "43 green out of 60 picks" into a probability:
P(green) ≈ favorable outcomes / total trials = 43/60.
This means choosing the right parts of the ratio (green over total, not green over non-green, which would be 43/17) and writing it as a fraction, decimal or percent.

### 3. Procedural Fluency (NRC)
Then the student carries out the routine steps correctly. They check whether 43/60 simplifies (43 is prime, so it doesn't), and if needed convert it: 43 ÷ 60 ≈ 0.717 ≈ 72%. The computation is small, but it still has to be accurate.

### 4. Justifying and Proving (optional, light check)
Finally, a quick check that the answer makes sense: it falls between 0 and 1, and it's well above 1/2 because most draws were green. A stronger student might also note that this is only an *estimate* and would change with more trials. The problem doesn't require this.

### Not used
- **Abstracting and Generalizing:** no pattern or general rule has to be found.
- **Collaborative Mathematics:** this is an individual item.

## Summary order
**Mathematical Modeling → Representing → Procedural Fluency → (Justifying and Proving, optional)**

Mathematical Modeling and Representing do most of the work. Procedural Fluency covers the short fraction or decimal step.

### Answer 2: major practice

**Major practice: Mathematical Modeling**

This item tests one idea: whether the student understands that data from repeated trials can be used to estimate an unknown probability. In other words, can they treat the bag as a random process and use the observed relative frequency (43 out of 60) as its experimental probability? That is a modeling decision, and it's where students most often go wrong. Common wrong answers include "it can't be determined," a theoretical guess like 1/2, or a ratio built the wrong way.

Once a student makes that modeling step, the rest is small:
- **Representing** is just writing 43/60.
- **Procedural Fluency** is, at most, a short division to get about 0.717.

Neither is what really separates students who get the item right from those who don't. So if I could pick only one, it would be **Mathematical Modeling**.

---

## Row 109 (problem_id 45372)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Answer the question below.
35% of f is 14. What is f?
____
```

### Answer 1: practices in order

**Problem:** 35% of f is 14. What is f?

**Answer:** f = 40

## Practices available

The NAEP 2026 Mathematics Framework names five practices:
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics

You asked me to add one more:
- **Procedural Fluency** (from the NRC's *Adding It Up*): carrying out procedures accurately, efficiently and flexibly.

## Practices needed, in order

### 1. Representing (main practice)
Turn the sentence into math. "35% of f is 14" becomes:

  0.35 · f = 14  (or (35/100) · f = 14)

To do this, the student has to know that "%" means "out of 100", that "of" means multiply, and that "is" means equals. This translation is the key step. Most mistakes on this item happen here. A common one is computing 35% of 14 (which gives 4.9) instead of treating 14 as the part.

### 2. Procedural Fluency (main practice)
Solve the one-step equation:

  f = 14 ÷ 0.35 = 1400 ÷ 35 = 40

Another way is to scale: 35% → 14, so 5% → 2, so 100% → 40. Either way, this step needs accurate division by a decimal, or reasoning with fractions or ratios.

### 3. Justifying and Proving (minor, optional)
Check the answer: 35% of 40 = 0.35 × 40 = 14. ✓
This is a quick check, not a formal argument. The problem does not ask for it, so it plays a small role.

## Practices not needed
- **Abstracting and Generalizing:** there is no pattern or general rule to find. This is a single specific case.
- **Mathematical Modeling:** there is no real-world situation to model. The problem is already stated in math terms.
- **Collaborative Mathematics:** this is an individual item.

## Summary
**Representing → Procedural Fluency → (Justifying and Proving)**

Representing and Procedural Fluency carry most of the work. Justifying is just a quick check at the end.

### Answer 2: major practice

**Major practice: Representing**

Why I'd pick Representing over Procedural Fluency:

- **It's the step that decides success or failure.** A student who writes 0.35 · f = 14 has nearly solved the problem. A student who reads it the wrong way, for example computing 35% of 14 = 4.9, gets it wrong no matter how good their arithmetic is.
- **The computation is routine once the setup is right.** 14 ÷ 0.35 = 40 is a single step with friendly numbers. You can even do it in your head: 35% → 14, 5% → 2, 100% → 40.
- **It's what the item is really testing.** The phrase "35% of f is 14" makes the unknown the *whole*, not the part. Spotting which quantity is the whole and which is the part is the whole point of the item.

Procedural Fluency comes a close second. Students who are shaky dividing by decimals may still slip at that step. But if I could only tag one practice, it would be **Representing**.

---

## Row 110 (problem_id 43417)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
A restaurant offers delivery for their pizzas. The total cost is a delivery fee added to the price of the pizzas. One customer pays $25 to have 2 pizzas delivered. Another customer pays $58 for 5 pizzas. How many pizzas are delivered to a customer who pays $80?
____ pizzas
```

### Answer 1: practices in order

**Answer: 7 pizzas**

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added Procedural Fluency from the NRC's *Adding It Up* strands. Here is the order a student would use them to solve this problem:

### 1. Mathematical Modeling: set up the situation
The student turns the story into a mathematical structure. "A delivery fee added to the price of the pizzas" means a fixed fee plus a constant price per pizza, which is a linear relationship:
Total cost = (price per pizza) × (number of pizzas) + fee.

### 2. Representing: write the information as math
The two customers become data points or equations:
- 2p + f = 25
- 5p + f = 58

(The same information could also be written as the points (2, 25) and (5, 58) or as a small table.)

### 3. Abstracting and Generalizing: find the general rule
The student sees that the difference between the two orders tells you the price per pizza. Going from 2 to 5 pizzas adds 3 pizzas and $33, so each pizza costs $11. The fee then comes from 25 − 2(11) = 3. That gives the general rule:
**C = 11n + 3**

### 4. Procedural Fluency (NRC): do the calculations
- 58 − 25 = 33, and 33 ÷ 3 = 11
- 25 − 22 = 3
- 80 − 3 = 77, and 77 ÷ 11 = **7**

The student has to carry out the subtraction, division, and solving steps accurately and efficiently.

### 5. Justifying and Proving: check the answer
The student checks that the answer makes sense: 11(7) + 3 = 80. The rule also matches both original customers: 11(2) + 3 = 25 and 11(5) + 3 = 58. The answer is also a whole number, which it has to be for a count of pizzas.

### Not used: Collaborative Mathematics
This is a single-student item with no group work, so this practice does not apply.

---

**Summary of the order:**
Mathematical Modeling → Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving

The most important practices here are **Abstracting and Generalizing** and **Mathematical Modeling**. The main difficulty is realizing that the two orders differ only in the number of pizzas, so their difference gives the per-pizza price. After that, the arithmetic is simple.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

This problem never hands you the rule. You get two specific cases ($25 for 2 pizzas, $58 for 5 pizzas), and you have to work out the general relationship behind them. The key step is noticing that the two orders differ only in the number of pizzas. That means the extra $33 for 3 more pizzas gives the per-pizza price ($11), and from there you get the fixed fee ($3) and the rule C = 11n + 3. Once you have that rule, the question for $80 is just a quick calculation.

Why I didn't pick the others:
- **Mathematical Modeling** comes close, but the problem already tells you the structure ("a delivery fee added to the price of the pizzas"). You don't have to figure out on your own that the situation is linear. Your main job is to find the rule's parameters, not to build the model.
- **Representing** means writing down two equations or two points. That's a setup step, not the hard part.
- **Procedural Fluency** is simple arithmetic here (subtract, divide, subtract, divide).
- **Justifying and Proving** is just an optional check at the end.

So the part of this problem that actually separates students is moving from specific cases to the general rule, which is **Abstracting and Generalizing**.

---

## Row 112 (problem_id 81543)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
A roll of ribbon was 12 meters long. Diego cut 9 pieces of ribbon that were 0.4 meter each to tie some presents. He then used the remaining ribbon to make some wreaths. Each wreath required 0.6 meter.
How many wreaths could Diego make with the available ribbon?
____ wreaths
```

### Answer 1: practices in order

**Answer: 14 wreaths**

Here is how the practices fit, using the NAEP mathematical practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics) plus NRC's **Procedural Fluency**.

### Practices in order

**1. Mathematical Modeling (setting up the model)**
Turn the story into a math plan. The ribbon starts at 12 m. Some goes to presents (9 pieces × 0.4 m). What's left goes to wreaths at 0.6 m each. The plan has three steps: find the ribbon used, find the ribbon left, then find how many 0.6 m pieces fit in what's left.

**2. Representing**
Write the plan as expressions:
- Ribbon used for presents: 9 × 0.4
- Ribbon left: 12 − (9 × 0.4)
- Number of wreaths: [12 − (9 × 0.4)] ÷ 0.6

You could also use a tape or bar diagram: one 12 m bar split into a "presents" part and a "wreaths" part, with the wreaths part divided into 0.6 m pieces.

**3. Procedural Fluency (NRC)**
Do the decimal arithmetic correctly and quickly:
- 9 × 0.4 = 3.6 m
- 12 − 3.6 = 8.4 m
- 8.4 ÷ 0.6 = 84 ÷ 6 = 14

This step uses decimal multiplication, subtraction with regrouping, and decimal division (shifting the decimal point so you divide by a whole number).

**4. Mathematical Modeling (interpreting the result)**
Check the answer against the story. You can only make whole wreaths. 8.4 ÷ 0.6 comes out to exactly 14 with no ribbon left over, so no rounding is needed. Diego can make **14 wreaths**.

**5. Justifying (optional check)**
Check it backward: 14 × 0.6 = 8.4 and 8.4 + 3.6 = 12. That matches the starting length, so the answer is right.

### Summary sequence
Modeling (set up) → Representing → Procedural Fluency → Modeling (interpret) → Justifying (verify)

The main practices are **Mathematical Modeling** and **Procedural Fluency**. Representing links the two, and Justifying is a light final check. Abstracting/Generalizing and Collaborative Mathematics aren't really needed for this problem.

### Answer 2: major practice

**Major practice: Mathematical Modeling**

Why I'd pick it:

- **It's what makes the problem hard.** This is a multistep word problem. The key move is seeing that you have to (1) take out the ribbon used for presents, (2) find what's left, and (3) divide that by 0.6. Students who get it wrong usually set it up wrong. Common errors are dividing 12 by 0.6 straight away (getting 20), skipping the 9 × 0.4 step, or doing the operations in the wrong order.
- **Every other step depends on it.** The arithmetic only helps after the situation has been turned into the right sequence of operations. Getting the model right is the step that unlocks the rest.
- **The interpretation step is modeling too.** Checking that the answer has to be a whole number of wreaths, and that 14 makes sense in the story, is the last part of the modeling cycle.

**Close second: Procedural Fluency.** The decimal operations (9 × 0.4, 12 − 3.6, 8.4 ÷ 0.6) are a real part of the work. Dividing by a decimal in particular trips up many students. But the numbers are friendly and the result comes out exact. So for a student who has set up the problem correctly, the arithmetic is less of a barrier than the setup.

---

## Row 113 (problem_id 45043)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Answer the question below.
125% of e is 30. What is e?
____
```

### Answer 1: practices in order

**Problem:** 125% of e is 30. What is e?

**Answer:** e = 24

The NAEP Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Modeling, and Mathematical Problem Solving. I've added the NRC's **Procedural Fluency** as a sixth. Here are the ones this problem needs, in the order they're used:

### 1. Representing (NAEP)
Turn the words into an equation. "125% of e" becomes 1.25 x e (or 5/4 x e), and "is 30" becomes "= 30":

  1.25e = 30

This is the key step. Students need to see that e is the whole (the base) and 30 is the part. Because the percent is over 100%, the part here is bigger than the whole.

### 2. Mathematical Problem Solving (NAEP)
Plan the solution. The unknown is the base, not the part, so you divide 30 by 1.25 instead of multiplying. A good student also checks that the answer makes sense: 125% is more than 100%, so e must be smaller than 30.

### 3. Procedural Fluency (NRC)
Do the arithmetic correctly:

  e = 30 / 1.25 = 30 x 4/5 = 24

Writing 1.25 as 5/4 makes this easy. Fluency also covers the percent-to-decimal or percent-to-fraction step (125% = 1.25 = 5/4), which is actually used back in step 1.

### 4. Justifying (NAEP, light use)
Check the answer: 125% of 24 = 1.25 x 24 = 30. This is only a substitution check, not a formal proof, so this practice plays a small role.

### Not needed
- **Abstracting and Generalizing:** there's no pattern or general rule to find.
- **Modeling:** there's no real-world situation to model. The problem is already stated in math terms.

### Summary
**Representing -> Mathematical Problem Solving -> Procedural Fluency -> (Justifying, as a check)**

The two practices that matter most are Representing (translating the words, and seeing that e is the base) and Procedural Fluency (dividing by 1.25). The most common mistake comes from the Representing step: computing 125% of 30 = 37.5 instead of solving for the base.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

This is the step that decides whether a student gets the problem right. They have to turn "125% of e is 30" into the equation 1.25e = 30, and see that e is the base (the whole) and 30 is the part.

Why Representing and not Procedural Fluency:
- The arithmetic is easy: 30 / 1.25 = 24, or 30 x 4/5 = 24. Most students who reach this step can do it.
- The common mistakes all come from setting the problem up wrong. Students compute 125% of 30 = 37.5, or 30 x 0.25 = 7.5, instead of solving for the base. They can carry out the procedures. They just applied them to the wrong setup.
- Once the equation is written correctly, solving it is routine.

Procedural Fluency comes a close second, but Representing is the main practice.

---

## Row 115 (problem_id 44380)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Noah enlarged a photograph by a scale factor of 6. The area of the enlarged photo is how many times as large as the area of the original?
____ times as many
```

### Answer 1: practices in order

**Problem:** Noah enlarged a photograph by a scale factor of 6. How many times as large as the original is the area of the enlarged photo?

**Answer:** 36 times as many. Area scales by the square of the linear scale factor: 6² = 36.

## Practices to use, in order

The NAEP mathematics framework names five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Discourse. As you asked, I've added the NRC's **Procedural Fluency** as a sixth.

| Order | Practice | What the student does in this problem |
|---|---|---|
| 1 | **Representing** | Turns the words into a mathematical picture: the photo is a rectangle with length *L* and width *W*. After enlargement it measures 6*L* by 6*W*. A quick sketch or a 1×1 → 6×6 grid makes the change visible. |
| 2 | **Abstracting and Generalizing** (main practice) | Sees the general rule that the problem is testing. A scale factor *k* multiplies every length by *k*, so area (length × width) is multiplied by *k*²: (6*L*)(6*W*) = 36*LW*. This is the key step. Students who skip it give the common wrong answer of 6. |
| 3 | **Procedural Fluency** (NRC) | Does the calculation quickly and correctly: 6 × 6 = 36, or 6² = 36. |
| 4 | **Justifying and Proving** (light) | Checks that 36 is right and not 6. For example, a 1-by-1 square enlarged by 6 becomes 6 by 6, which holds 36 of the original unit squares. Ratio of areas = 36*LW* / *LW* = 36. |

## Practices not needed

- **Mathematical Modeling:** The problem is already stated in mathematical terms ("scale factor of 6"). There is no messy real-world situation to model or assumptions to choose.
- **Collaborative Discourse:** It is a single-answer task done by one student, so no discussion or critique of others' reasoning is involved.

## Summary of order

**Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving)**

The step that decides the problem is Abstracting and Generalizing: realizing that area grows by the square of the scale factor. The actual computation is trivial once that idea is in place.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

This problem hinges on one general rule: if a figure is scaled by a factor *k*, its area is scaled by *k*². For a photo that's (6*L*)(6*W*) = 36*LW*, so the enlarged photo has 36 times the area.

Why this practice and not the others:

- **It decides the answer.** The common wrong answer, 6, comes from students who apply the linear scale factor to area without generalizing how area behaves. Students who know the *k*² rule get 36. Students who don't, fail. No other practice separates the two groups this way.
- **Representing** helps, for example sketching the rectangle with sides 6*L* and 6*W*. But students can skip it if they already know the rule.
- **Procedural Fluency** only covers working out 6 × 6 = 36. That step is trivial and isn't where students struggle.
- **Justifying and Proving** is an optional check on the answer, not something the problem requires.

So the single major practice is **Abstracting and Generalizing**.

---

## Row 116 (problem_id 44248)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
A textbook has 428 pages numbered in order starting with 1. You flip to a random page in the book in a way that it is equally likely to stop at any of the pages.
What is the probability that you turn to an even numbered page?
____
```

### Answer 1: practices in order

**Answer: 214/428 = 1/2 (0.5)**

**Practices used, in order**

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added Procedural Fluency from the NRC's *Adding It Up*.

1. **Mathematical Modeling (light)**: Turn the story into a probability model. "Flip to a random page, every page equally likely" becomes a uniform sample space of 428 outcomes. The event is "the page number is even." So P(even) = (number of even pages) / 428.

2. **Representing**: Write the situation down as numbers. The pages are the list 1, 2, 3, …, 428. The favorable outcomes are 2, 4, 6, …, 428. You can also write the probability as the fraction favorable/total.

3. **Abstracting and Generalizing**: Spot the structure instead of counting one by one. Page numbers go odd, even, odd, even, and the book starts at 1 (odd) and ends at 428 (even). That means the pages pair up as (1,2), (3,4), …, (427,428), with exactly one even page in each pair. So the number of even pages is 428 ÷ 2 = 214. In general, a book with an even number of pages 2n has n even pages.

4. **Procedural Fluency (NRC)**: Do the arithmetic quickly and correctly. 428 ÷ 2 = 214, then 214/428 simplifies to 1/2, which is 0.5 or 50%.

5. **Justifying and Proving (brief check)**: Make sure the result makes sense. The pairing argument shows evens and odds are exactly equal, 214 each, and 214 + 214 = 428. So 1/2 is exact, not an estimate. This step is optional for a fill-in item, but it confirms the answer.

**Not used:** Collaborative Mathematics, since this is a single-student item.

**Key practices:** Representing → Abstracting and Generalizing → Procedural Fluency. Modeling sets the problem up and Justifying is a quick final check.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

This problem hinges on one idea: seeing that exactly half the pages are even. That comes from noticing that page numbers alternate odd, even, odd, even. Since the book runs from 1 to 428, the pages split cleanly into 214 odd–even pairs. Once you see that, the answer is 1/2 almost right away, and you never have to count anything.

The other practices are minor here:
- **Representing / Modeling**: Writing P = favorable/total with 428 equally likely pages is a routine setup step.
- **Procedural Fluency**: 428 ÷ 2 = 214, and 214/428 = 1/2. The arithmetic is trivial.
- **Justifying**: This is only a sanity check.

A student who gets this wrong usually didn't miss the division. They failed to see the half-and-half structure, or they doubted it, for example by worrying that starting at 1 or ending at 428 makes the counts unequal. Seeing that structure is Abstracting and Generalizing, so that is the major practice.

---

## Row 117 (problem_id 45097)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
Now solve: You need 3/4 yard of ribbon for one gift box. You have 3 yards of ribbon. How many gift boxes do you have ribbon for?
____ gift boxes
```

### Answer 1: practices in order

**Problem:** You need 3/4 yard of ribbon for each gift box and you have 3 yards. How many gift boxes can you wrap?

**Answer: 4 gift boxes** (3 ÷ 3/4 = 3 × 4/3 = 4)

## Practices used, in order

The NAEP Mathematics Framework lists five mathematical practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, and (5) Collaborative Mathematics. Below, NRC's **Procedural Fluency** is added as a sixth.

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (NAEP) | Turns the story into math. "How many 3/4-yard pieces fit into 3 yards?" is a measurement (quotitive) division, so the expression is 3 ÷ 3/4. This is the key step. A common mistake is to multiply (3 × 3/4 = 2 1/4) or to divide the wrong way (3/4 ÷ 3 = 1/4). |
| 2 | **Representing** (NAEP) | Pictures or rewrites the quantities to back up or carry out the model. For example, draw a 3-yard number line split into fourths (12 fourths) and group them by 3, or write 3 yards as 12/4. Students who move straight from the model to the procedure can skip this step. |
| 3 | **Procedural Fluency** (NRC) | Does the fraction division correctly: 3 ÷ 3/4 = 3 × 4/3 = 12/3 = 4. Another route is 12/4 ÷ 3/4 = 12 ÷ 3 = 4. |
| 4 | **Justifying** (NAEP, Justifying and Proving; light use) | Checks that the answer makes sense in the story: 4 boxes × 3/4 yard = 3 yards, with no ribbon left over. The answer is a whole number, which fits counting boxes, and it is bigger than 3 because each box uses less than a yard. |

**Not used:** Abstracting and Generalizing (no general pattern or rule is asked for) and Collaborative Mathematics (it is a single-student item).

**Summary order:** Mathematical Modeling → Representing → Procedural Fluency → Justifying (check).

The main practices are **Mathematical Modeling** (choosing division) and **Procedural Fluency** (dividing by a fraction). Representing helps along the way, and Justifying is a short final check.

### Answer 2: major practice

**Major practice: Mathematical Modeling (NAEP)**

**Why Modeling over the others:**

- **It is the main source of difficulty.** The numbers are easy. The hard part is seeing that "how many 3/4-yard pieces fit in 3 yards" is a division, 3 ÷ 3/4. Students usually go wrong at this step. They multiply (3 × 3/4 = 2 1/4) or divide in the wrong order (3/4 ÷ 3 = 1/4).
- **Everything later depends on it.** Once 3 ÷ 3/4 is set up, the arithmetic is short. A student with perfect procedural fluency still gets the wrong answer if the model is wrong.
- **This item tests it directly.** The problem is written as a real-world story about ribbon and gift boxes. The story adds no difficulty beyond the translation, so the item mainly tests turning the situation into the right operation.

**Runner-up: Procedural Fluency (NRC).** The student still has to divide by a fraction. That step is routine here, though, because 3 × 4/3 = 4 comes out to a whole number. Many students can also skip the fraction algorithm by counting fourths: 3 yards is 12 fourths, and 12 ÷ 3 = 4.

---

## Row 118 (problem_id 44687)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
How many times around the park did he ride?
____
```

### Answer 1: practices in order

**Note on the problem text:** Only the question stem came through: "How many times around the park did he ride? ____". The setup is missing. That would be the total distance he rode, the distance around the park (or a picture or map of the park's sides), and the units. I'm assuming the usual form of this item: you are given (or must work out) the distance of one trip around the park and the total distance ridden, and you find the number of laps. The practices below follow that assumption. If the real item differs, say a perimeter has to be read off a diagram first, the order still holds, but step 1 carries more weight.

### Practices used, in order

The practices come from the 2026 NAEP Mathematics Framework (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus Procedural Fluency from the NRC strands of proficiency.

1. **Mathematical Modeling (formulate the situation).** Turn the story into math. "Riding around the park" is one lap, so one lap equals the perimeter of the park. "How many times around" means how many laps fit into the total distance. This tells you the operation: total distance divided by distance per lap (or repeated addition of the lap length until you reach the total).

2. **Representing.** Pull the needed quantities out of the text or diagram and put them in a usable form. If the park is shown as a shape with side lengths, add the sides to get the perimeter. Write the relationship as an equation, such as *laps × lap length = total distance*, or draw a bar or number-line model. Convert units if needed (for example, miles vs. yards, or a fraction of a mile).

3. **Procedural Fluency (NRC).** Do the computation accurately and efficiently. Add the side lengths for the perimeter, then divide the total distance by the perimeter. This may involve whole numbers, decimals, or fractions (for example, 3 ÷ ¾ = 4).

4. **Mathematical Modeling (interpret and validate).** Bring the number back to the context. Check that it makes sense as a count of laps. Decide what to do with any remainder, given what the question asks (whole laps completed vs. an exact number of laps).

5. **Justifying and Proving (light, optional).** Check the answer by working backward: laps × lap length should equal the total distance. This matters more if the item asks students to explain or show their work. With only a fill-in blank, it is just a self-check.

**Not really needed:** Abstracting and Generalizing (no pattern or general rule is asked for) and Collaborative Mathematics (it is a solo item).

**Compact sequence:** Mathematical Modeling (formulate), then Representing, then Procedural Fluency, then Mathematical Modeling (interpret), then Justifying and Proving (check).

The core of the item is Modeling plus Procedural Fluency: seeing that "times around" means dividing by the perimeter, then doing that division correctly.

### Answer 2: major practice

**Major practice: Mathematical Modeling.**

The hard part of this item is recognizing what the situation means mathematically. "Times around the park" means one lap is the park's perimeter, and the number of laps is total distance ÷ distance per lap. Once a student sees that, the arithmetic (adding sides, then dividing) is usually routine. Students who miss this item most often pick the wrong operation, such as multiplying, or use the wrong quantity, such as one side length instead of the whole perimeter. That is a failure to formulate the model, not a computation slip.

Modeling also covers the final step of reading the number back in context (whole laps, any remainder). So it brackets the whole solution.

**Runner-up: Procedural Fluency.** It matters if the numbers are fractions or decimals (for example, 3 ÷ ¾). If this version of the item uses awkward fractional distances, fluency could be the main source of difficulty. Even so, Modeling is the practice that defines the problem.

(This assumes the usual form of the item. Only the question stem came through, without the distances or the diagram.)

---

## Row 131 (problem_id 47523)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
There are 20 pennies in a jar. If 16% of the coins in the jar are pennies, how many coins are there in the jar?
____ coins
```

### Answer 1: practices in order

**Problem:** There are 20 pennies in a jar. If 16% of the coins in the jar are pennies, how many coins are there in the jar?

**Answer:** 125 coins (0.16 × N = 20, so N = 20 / 0.16 = 125)

The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. Below I add NRC's **Procedural Fluency** (from *Adding It Up*, 2001) to that list.

### Practices used, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the words into math. The unknown is the total number of coins, N, and "16% of the coins are pennies" becomes 0.16 × N = 20 (or the proportion 16/100 = 20/N). The key move is spotting that 20 is the *part* and the total is what we need to find. This is the reverse of the usual "find 16% of a number" task. |
| 2 | **Procedural Fluency** (NRC) | Solves the equation quickly and correctly: N = 20 ÷ 0.16 = 125, or cross-multiplies 16N = 2000, so N = 125. This includes turning the percent into a decimal or fraction and dividing by a decimal. |
| 3 | **Justifying and Proving** (NAEP), in a light form | Checks the answer: 16% of 125 = 0.16 × 125 = 20 ✓. Also checks that it makes sense: pennies are a small share (16%), so the total must be much bigger than 20. |

### Practices not needed
- **Abstracting and Generalizing:** no pattern or general rule is being built.
- **Mathematical Modeling:** the context is already fully mathematical. There is no real-world situation that needs simplifying, assumptions, or a model to refine. Writing the equation counts as Representing, not full modeling.
- **Collaborative Mathematics:** this is a solo item with no communication or teamwork part.

### Summary
**Representing → Procedural Fluency → Justifying (check)**

The main difficulty is Step 1: setting up the part/whole relationship the right way round. The most common mistake is computing 16% of 20 (= 3.2) instead of solving for the whole.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

**Why this one:**
- **It is where the problem gets hard.** Once you have 0.16 × N = 20 (or 16/100 = 20/N), only one routine division is left: 20 ÷ 0.16 = 125. Getting to that equation is the real difficulty. You have to see that 20 is the *part*, 16% is the rate, and the *whole* is the unknown. That runs against the usual "find a percent of a number" pattern.
- **It is where students go wrong.** The most common wrong answer is 3.2 (16% of 20). Students who give it can multiply just fine. Their mistake is that they set up the relationship the wrong way round. That is a representing error, not a fluency error.
- **The other practices depend on it.** Procedural fluency only works on the equation that Representing produces, and the check (Justifying) only confirms it. If the setup is wrong, neither of them can save the answer.

Procedural fluency comes a close second, since dividing by a decimal or cross-multiplying is required. But it is routine once the setup is right, so it does not decide whether a student succeeds.

---

## Row 136 (problem_id 49232)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Justifying and Proving

### Problem

```text
What value makes sense for the slope of the line that represents the amounts on Han’s fare card in July?
____
```

### Answer 1: practices in order

**Note on the problem text:** The item mentions a line for "the amounts on Han's fare card in July," but the graph, table or story that defines that line isn't included. So I can't give an exact number. The practice sequence below works either way. The most likely situation is that the card starts with a balance and goes down by a fixed fare each time Han rides. In that case the slope is **negative** and equals the cost of one ride (for example, about -$2.50 per ride, or -$X per day). A positive slope, or a slope much larger than one fare, wouldn't "make sense."

### The practices

From the NAEP 2026 Mathematics Framework (mathematical practices):
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics (not needed here, since this is an individual item)

Added from NRC *Adding It Up*:
- Procedural Fluency

### Practices in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** | Reads the July fare-card situation as a linear model. The x-axis is time or number of rides, the y-axis is the dollar balance on the card. The student decides what the quantities are and that the balance changes at a constant rate. |
| 2 | **Representing** | Links the situation to the line (graph, table or equation). The slope is "change in balance per ride/day." The student reads two points or the rate off the representation and notes the units ($ per ride). |
| 3 | **Procedural Fluency** | Works out the slope as rise over run, (y2 - y1)/(x2 - x1), with the sign and units correct. For a balance going down by one fare per ride, this gives a negative value equal to the fare. |
| 4 | **Justifying and Proving** (sense-making) | Checks that the value "makes sense" in context. It should be negative because the card is used up. Its size should match a realistic fare. A value that is positive, zero or too large doesn't fit the story, which is what the question asks. |

**Order: Mathematical Modeling -> Representing -> Procedural Fluency -> Justifying and Proving**

Abstracting and Generalizing has at most a minor role. It would come in only if the student generalized "slope = rate of change per unit" from earlier months or other cards. It isn't needed to answer this item.

**Main practice:** Justifying and Proving (with Modeling close behind). The question asks what value *makes sense*, so judging whether a slope is reasonable in context matters more than the calculation itself.

### Answer 2: major practice

**Major practice: Justifying and Proving (sense-making / checking reasonableness)**

Why this one:
- The question doesn't ask the student to "calculate the slope." It asks what value **makes sense** for it. That means judging whether a slope fits the situation.
- What decides success is reasoning about the context. The balance on a fare card goes **down** as Han rides, so the slope must be negative. Its size should be about one fare per ride (or per day). A student who can't make that argument will choose a value that doesn't fit, even if they can compute rise over run.
- The other practices support this step. Mathematical Modeling and Representing set up what the slope means (dollars per ride over time). Procedural Fluency comes in only if exact numbers have to be computed. The question itself is aimed at deciding whether a value is reasonable.

If the full item asks the student to compute the slope exactly from given data points (not just pick or estimate a sensible value), I would move the major practice to **Mathematical Modeling**. In that case the main challenge becomes reading the rate of change as "cost per ride" from the fare-card situation.

---

## Row 139 (problem_id 53019)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
How many triangles can you fit together at one vertex?
Do not include units (triangles) in your answer.
____
```

### Answer 1: practices in order

**Problem:** How many triangles can you fit together at one vertex? (Answer with a number only.)

**Answer: 6**

The problem doesn't say what kind of triangle, but "fitting together at one vertex" is tessellation language. That means identical equilateral triangles meeting around a point with no gaps and no overlaps.

---

### Practices used, in order

The practices below are the NAEP Mathematical Practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Problem Solving), plus NRC Procedural Fluency.

**1. Representing (NAEP)**
- Turn the words into a picture: equilateral triangles placed side by side around one shared point.
- See that the question is really about the angles at that shared point.
- Recall that each angle of an equilateral triangle is 60°.

**2. Abstracting and Generalizing (NAEP)**
- Move from the picture to the general rule: tiles fit around a point with no gaps or overlaps only if the angles meeting there add up to exactly 360°.
- That gives the equation: number of triangles × 60° = 360°.

**3. Procedural Fluency (NRC)**
- Do the calculation quickly and correctly: 360 ÷ 60 = 6.

**4. Justifying and Proving (NAEP)** (brief check)
- Check the answer against the rule. 5 triangles cover 300°, which leaves a 60° gap. 7 triangles need 420°, which overlaps. Only 6 fills the space exactly.
- Remember the format rule: write just "6", with no units.

**Not used**
- **Mathematical Modeling:** there's no real-world situation to translate into math.
- **Collaborative Problem Solving:** the task is done alone.

---

### Summary order
**Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving**

The main steps are Representing and Abstracting and Generalizing. The hard part is knowing that angles around a point add up to 360° and that each angle of an equilateral triangle is 60°. Once you have that, the calculation is easy.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

**Why:** The key step is applying a general rule. Tiles meet at a point with no gaps or overlaps only when their angles add up to exactly 360°. Using that rule, plus the fact that each angle of an equilateral triangle is 60°, turns the question into 360 ÷ 60.

- **Representing** is only the setup: seeing that the question is about angles at a shared point.
- **Procedural Fluency** is the easy part: one division, 360 ÷ 60 = 6.
- **Justifying and Proving** is a quick final check.

A student who gets this wrong most likely doesn't know or can't apply the "360° around a point" rule. The arithmetic is unlikely to be the problem.

---

## Row 140 (problem_id 52844)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
What is the measure of each angle in an equilateral triangle?
Do not include units (degrees) in your answer.
____
```

### Answer 1: practices in order

**Problem:** What is the measure of each angle in an equilateral triangle? (Answer: 60)

**Practices used (NAEP Mathematics practices plus NRC "Procedural Fluency"):**

NAEP lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Modeling, and Collaborative Mathematical Discourse. NRC's Procedural Fluency is added as a sixth. Only three of these six are needed for this problem.

**Order in which they are used**

1. **Representing.** The student turns the words "equilateral triangle" into a mental picture or quick sketch: a triangle with three equal sides. Because equal sides sit opposite equal angles, the three angles are also equal. This step connects the verbal definition to a geometric representation with three equal unknown angles (x, x, x).

2. **Abstracting and Generalizing.** The student brings in the general fact that the interior angles of *any* triangle add up to 180°. Then they apply it to this special case, so x + x + x = 180. This step goes from a general property to the specific triangle. It is the main conceptual step.

3. **Procedural Fluency (NRC).** The student does the arithmetic quickly and correctly: 3x = 180, so x = 180 ÷ 3 = 60. They write **60** with no units, as the problem asks.

**Not needed:** Justifying and Proving (no argument has to be written; the student only has to recall and use the angle-sum fact), Modeling (there is no real-world situation), and Collaborative Mathematical Discourse (it is a single-answer item done alone).

**Summary order:** Representing → Abstracting and Generalizing → Procedural Fluency

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

**Why this one:**

- **It is where the difficulty is.** To solve the problem, the student has to bring in the general fact that the angles of every triangle add up to 180°. Then they apply it to the special case where all three angles are equal. A student who gets this wrong almost always failed at this step, either by not knowing the 180° fact or by not seeing that equal sides mean equal angles.
- **Representing is light here.** Picturing a triangle with three equal sides is quick. The problem gives no diagram, table or graph to read or build.
- **Procedural Fluency is light here.** Working out 180 ÷ 3 = 60 is one easy division. Many students simply remember "60°" as a fact, which needs almost no procedure.

**Close second:** Procedural Fluency. If the item is treated as plain recall of a memorized fact ("equilateral triangle angles = 60"), you could argue it is the main practice. But the reasoning the problem actually tests is applying a general triangle property to a specific case. That makes **Abstracting and Generalizing** the best single choice.

---

## Row 142 (problem_id 54666)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
How many students are in the school in 63 of them are sixth graders?
____ students
```

### Answer 1: practices in order

**Note on the problem:** The text as given ("How many students are in the school if 63 of them are sixth graders?") is missing information. On its own, 63 sixth graders does not tell you the school total. The original item almost certainly came with a stimulus, such as a circle graph, table, or statement like "sixth graders make up 35% (or 3/8) of the school." I'll lay out the practice sequence for that intended part-to-whole problem: given that a known part (63) is a stated fraction or percent of the whole, find the whole.

**Practices available** (the 2026 NAEP Mathematics Framework practices, plus the one you asked to add):
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics
- *Added:* Procedural Fluency (NRC, *Adding It Up*)

**Order to solve:**

1. **Representing.** Read the given display (graph, table, or percent) and turn it into a mathematical relationship. That means finding the fraction or percent of the whole that sixth graders make up, and recognizing that 63 is the *part* and the school total is the unknown *whole*. You could write this as an equation (p × N = 63), a tape diagram, or a ratio table.

2. **Mathematical Modeling** (light use). Set up the context as a proportional model: part = rate × whole, or 63 / N = p / 100. This is a direct translation from a real situation into a proportion, so it is a minor role rather than a full modeling cycle.

3. **Procedural Fluency (NRC).** Carry out the computation accurately: N = 63 ÷ p. For example, if sixth graders are 35%, then N = 63 ÷ 0.35 = 180. If they are 3/8, then N = 63 × 8/3 = 168. This means dividing by a decimal or fraction, or scaling a ratio, correctly and efficiently.

4. **Justifying and Proving** (light use, checking). Confirm that the answer makes sense: it is a whole number of students, it is larger than 63, and p × N gives back 63.

**Not needed:** Abstracting and Generalizing (there is no pattern or general rule to extract) and Collaborative Mathematics (this is an individual item).

**Summary sequence:** Representing → Mathematical Modeling → Procedural Fluency → Justifying (check). The main demands are **Representing** (seeing that 63 is the part and the total is the whole) and **Procedural Fluency** (the division).

### Answer 2: major practice

**Major practice: Representing**

Most of the difficulty is in reading the given information, presumably a graph, table, or percent, and turning it into the right relationship. The student has to see that 63 is the *part*, that the school total is the unknown *whole*, and set up p × N = 63 (or 63 / N = p / 100).

Students who get this item wrong usually do so because of the setup, not the arithmetic. A common error is taking p% *of* 63 instead of finding the whole that 63 is p% *of*. Once the relationship is set up correctly, the division (procedural fluency) is routine.

Procedural Fluency is the second most important practice. Modeling and justifying play only minor roles.

---

## Row 144 (problem_id 54441)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
How many sixth graders are there if the school has 28 students?
____ sixth graders
```

### Answer 1: practices in order

**Practices you need, in order:** 1. Representing, then 2. Procedural Fluency. Mathematical Modeling might add a small step in between, depending on the missing figure.

**What's available to choose from**

The 2026 NAEP Mathematics Framework lists five mathematical practices:
1. **Representing**: reading, making, and moving between tables, graphs, diagrams, and symbols.
2. **Abstracting and Generalizing**: finding patterns and stating general rules.
3. **Justifying and Proving**: building and checking mathematical arguments.
4. **Mathematical Modeling**: turning a real situation into math, solving it, and reading the result back in context.
5. **Collaborative Mathematics**: working through math with others.

You asked me to add a sixth:
6. **Procedural Fluency** (NRC, *Adding It Up*): carrying out procedures like computing with fractions, percents, or ratios flexibly, accurately, and efficiently.

**A note on the problem**

The text only says "How many sixth graders are there if the school has 28 students?" The data needed to answer it (the share or ratio of sixth graders) must be in a figure that isn't in the text, probably a circle graph, bar graph, table, or picture of students by grade. So the order below assumes the student has to get that information from the figure.

**Order of practices**

1. **Representing** (first and most important)
   The student reads the figure to find what part of the school is sixth graders. Examples: "1/4 of the students," a sector labeled 25%, a ratio like 2 sixth graders for every 7 students, or a picture count. They then turn it into a number they can work with, such as a fraction, percent, or ratio. This is the main thinking step. If the figure is misread, nothing after it helps.

2. **Mathematical Modeling** (light, and only if the figure is a sample or ratio, not the whole school)
   If the figure shows a smaller group or a "for every" ratio, the student has to see that it scales up to all 28 students. That means setting up a proportion or a "part of a whole" multiplication. If the figure already gives the fraction for the whole school, this step reduces to choosing the right operation and can be folded into step 3.

3. **Procedural Fluency** (NRC)
   The student does the arithmetic: multiplies 28 by the fraction or percent, or solves the proportion. For example, 1/4 x 28 = 7. Then they write the whole-number answer in the blank. Since 28 is a small number with easy factors (2, 4, 7, 14), this should be quick if the student is fluent.

**Not needed:** Abstracting and Generalizing (no pattern or general rule), Justifying and Proving (no explanation asked for), and Collaborative Mathematics (individual item).

**Summary:** Representing, then (Mathematical Modeling, if a proportion is needed), then Procedural Fluency.

### Answer 2: major practice

**Major practice: Representing**

The arithmetic is easy. With a total of 28, it is something like 1/4 x 28 = 7. What the item really tests is whether the student can get the sixth-grade share out of the figure and turn it into a fraction, percent, or ratio. The figure isn't in the text, but it is probably a graph, table, or picture.

Most mistakes will come from reading the figure wrong, not from multiplying wrong. Examples:
- reading the wrong sector or bar
- mixing up a part-to-part ratio with a part-to-whole ratio
- miscounting icons

Once the student has the share right, Procedural Fluency finishes the problem almost automatically. That makes Representing the main practice. Procedural Fluency is a supporting practice.

---

## Row 145 (problem_id 54562)

- **predicted_practice:** Representing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
If the school has x students, write an expression for the number of sixth graders in terms of x.
____
```

### Answer 1: practices in order

**Note on the problem:** The text as given ("If the school has x students, write an expression for the number of sixth graders in terms of x.") points back to information that isn't included, such as a fraction, percent, ratio, or table/graph showing what share of the school is in sixth grade. The practice sequence below holds for any of those versions. For a worked example I'll assume the missing stem says something like "1/4 of the students are sixth graders" (or "25% of the students").

---

## The practices used

**NAEP Mathematics Framework (2026) practices:**
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

**Added from the NRC (*Adding It Up*) strands:**
- Procedural Fluency

---

## Which practices are needed, in order

### 1. Mathematical Modeling (light use): read the situation and pick out the relationship
The student converts the real-world description (a school, its students, the share that are sixth graders) into a math relationship: *number of sixth graders = (share of sixth graders) × (total students)*. This is only a light use of modeling. There's no open-ended model to build and no assumptions to choose; it's a direct translation of a "part of a whole" situation. If the share comes from a table or circle graph, this step also includes reading that display.

### 2. Abstracting and Generalizing (central practice): use a variable for the unknown total
This is the heart of the problem. Instead of working with a specific school size (say, 400 students → 100 sixth graders), the student has to state the relationship for **any** total x. Going from "a particular number" to "a general expression in terms of x" is exactly what Abstracting and Generalizing means.

### 3. Representing (central practice): write the symbolic expression
The student has to express the relationship in algebraic notation, e.g., **(1/4)x**, **x/4**, **0.25x**, or **x − (number in other grades)** if the stem is set up that way. Writing the answer as an algebraic expression, and possibly translating from a verbal, percent, or graphical form, is Representing.

### 4. Procedural Fluency (NRC; supporting): carry out the conversion and simplification correctly
The student turns a percent or ratio into a usable coefficient (25% → 0.25 or 1/4; a ratio of 1:3 sixth graders to others → 1/4 of the total). They also write the product of a coefficient and a variable in standard form and simplify if needed (e.g., x − 3x/4 = x/4). This is routine, accurate, efficient procedure work. It isn't the main challenge, but mistakes here (e.g., writing 25x or x + 1/4) are common.

### Not needed
- **Justifying and Proving:** The item asks only for an expression, not an explanation or argument. A student could check it by substituting a number (x = 400 → 100), but the task doesn't require that.
- **Collaborative Mathematics:** This is an individual constructed-response item, with no communicating with or critiquing others.

---

## Summary

| Order | Practice | Role |
|---|---|---|
| 1 | Mathematical Modeling | Light: turn the school context into "part = fraction × whole" |
| 2 | Abstracting and Generalizing | **Primary:** state the relationship for any total, using variable x |
| 3 | Representing | **Primary:** write it as an algebraic expression |
| 4 | Procedural Fluency (NRC) | Supporting: convert percent/ratio to a coefficient and simplify |

**Example answer** (assuming 1/4 of students are sixth graders): **(1/4)x**, or equivalently **x/4** or **0.25x**.

If you send the missing part of the stem (the fraction, percent, ratio, or graph), I can confirm the exact expression and whether the order changes. For example, a ratio given in parts-to-parts form would put more weight on Procedural Fluency.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

The hard part of this item isn't the arithmetic. It's moving from "a specific school with a specific number of students" to a relationship that holds for **any** total, written with the variable x. Most students who can find the number of sixth graders for 400 students can still get stuck when asked to state the rule for x students. Using a variable to stand for a general quantity and stating the rule for every case is exactly what Abstracting and Generalizing covers.

**Why not the others:**
- **Representing** is a close second, since the answer has to be written as an algebraic expression. But the notation (e.g., (1/4)x) is just the form the generalization takes. If a student has abstracted the relationship, writing it down is the easy part.
- **Procedural Fluency (NRC)** supports the work (turning a percent or ratio into a coefficient, simplifying), but it's routine and isn't what the item is testing.
- **Mathematical Modeling** shows up only lightly, because the context maps directly onto "part = fraction × whole."

So if I have to pick one, it's **Abstracting and Generalizing**, with Representing as the secondary practice.

---

## Row 151 (problem_id 58785)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
A cone fits snugly inside a hemisphere, and they share a radius of 5.
[image]
What is the volume of the cone?
____ cubic units
Use pi to represent the π symbol. For example: 32π would be typed as 32pi
```

### Answer 1: practices in order

**Answer: 125π/3 cubic units (typed as 125pi/3), about 130.9**

The 2026 NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. Adding Procedural Fluency from the NRC strands, three of these practices are needed for this problem. They apply in this order:

**1. Representing (NAEP)**
Read the picture and the words, and turn them into geometry. "Fits snugly" means the cone's base is the hemisphere's flat circular face, so the cone's base radius is r = 5. The cone's tip touches the top of the dome.

**2. Abstracting and Generalizing (NAEP)**
Find the hidden fact the problem depends on. The distance from the center of the flat face to any point on the dome equals the radius, so the cone's height is h = r = 5. This is the key insight, because the height is never given directly.

**3. Procedural Fluency (NRC)**
Pick the cone volume formula and work it out correctly, leaving the answer in terms of π:
V = (1/3)πr²h = (1/3)π(5²)(5) = (1/3)π(125) = **125π/3**

**Practices not needed:**
- **Justifying and Proving:** you could briefly check why h = r, but the problem doesn't ask for a proof.
- **Mathematical Modeling:** the problem is purely geometric, with no real-world situation to model.
- **Collaborative Mathematical Discourse:** this is a solo task.

**Order:** Representing → Abstracting and Generalizing → Procedural Fluency

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

**Why this one:**
- **It's the step where students get stuck.** The problem gives only the radius, but the cone volume formula also needs a height. To solve it, a student has to see that every point on the dome is the same distance (the radius) from the center of the flat face. So the cone's height equals the radius: h = r = 5. Students who miss this can't go on, or they guess a wrong height.
- **Procedural Fluency matters, but it's routine here.** Once h = 5 is known, V = (1/3)π(25)(5) = 125π/3 is a direct use of a standard formula. That step doesn't make the item hard.
- **Representing is a lighter step.** Reading "fits snugly" as "the cone and the hemisphere share the same circular base" is fairly direct. The real reasoning is the next step: turning the hemisphere's radius into the cone's height.

So Abstracting and Generalizing, seeing that h = r, is the deciding practice. Representing and Procedural Fluency support it.

---

## Row 155 (problem_id 62350)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
A shopper bought a watermelon, a pack of napkins, and some paper plates. In his state, there is no tax on food. The tax rate on non-food items is 5%. The total for the three items he bought was $8.25 before tax, and he paid $0.19 in tax. How much did the watermelon cost?
$ ____
```

### Answer 1: practices in order

**Answer: the watermelon cost $4.45.**

## Practices used, in order

The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added NRC's **Procedural Fluency** from *Adding It Up*. This problem uses four of these, in this order:

### 1. Mathematical Modeling (turning the situation into math)
Read the real-world setup and decide what matters:
- The watermelon is food, so it is **not taxed**.
- The napkins and paper plates are non-food, so they are taxed at **5%**.
- So the whole $0.19 of tax comes only from the non-food items. The watermelon's price doesn't affect the tax.

This is the key step. A student who misses it may try 5% of $8.25 (about $0.41) and get stuck.

### 2. Representing (writing the relationships down)
Let *n* = the cost of the non-food items and *w* = the cost of the watermelon.
- Tax: 0.05 × *n* = 0.19
- Total: *w* + *n* = 8.25

### 3. Procedural Fluency (NRC) (doing the arithmetic correctly)
- *n* = 0.19 ÷ 0.05 = **$3.80**
- *w* = 8.25 − 3.80 = **$4.45**

This takes accurate decimal division (or turning 5% into the fraction 1/20, so *n* = 0.19 × 20) and decimal subtraction.

### 4. Justifying and Proving (checking the answer)
- 5% of $3.80 = $0.19, which matches the tax paid.
- $4.45 + $3.80 = $8.25, which matches the pre-tax total.
- The answer makes sense: the watermelon has no tax, and the tax fits the non-food items exactly.

### Not used
- **Abstracting and Generalizing:** the problem asks for one specific number, not a general rule or pattern.
- **Collaborative Mathematics:** this is a problem for one student working alone.

## Summary
**Mathematical Modeling → Representing → Procedural Fluency → Justifying and Proving**

Mathematical Modeling is the main practice here, because the problem depends on seeing that only the non-food items are taxed. Procedural Fluency is the main computing skill.

**Answer: $4.45**

### Answer 2: major practice

**Major practice: Mathematical Modeling**

**Why:**
- **It is the deciding step.** The problem depends on one insight from the real-world context: food isn't taxed, so the whole $0.19 of tax comes only from the napkins and plates. Once a student sees that, the rest is routine.
- **It is where students most likely go wrong.** The usual mistakes are modeling mistakes. One is taking 5% of the full $8.25. Another is not seeing how the tax tells you the non-food cost. These are failures to understand the situation, not arithmetic slips.
- **The other practices are light here:**
  - *Representing* is just writing 0.05n = 0.19, which follows directly once the model is clear.
  - *Procedural Fluency* is one decimal division (0.19 ÷ 0.05 = 3.80) and one subtraction (8.25 − 3.80 = 4.45). It's grade-level arithmetic.
  - *Justifying and Proving* is an optional check.

**Runner-up:** Procedural Fluency. Dividing by 0.05 is a real decimal skill, and some students who model the problem correctly will still slip there. But it isn't what makes this problem hard.

**Answer: $4.45**

---

## Row 161 (problem_id 10467)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Use Priya’s method to calculate (1.05) · (2.8). You can use the fact that 105 · 28 = 2,940.
____
```

### Answer 1: practices in order

**Answer: (1.05) · (2.8) = 2.94** (written as 2.940 before dropping the trailing zero)

The problem text doesn't spell out Priya's method. The usual version of this item, and the one the given fact 105 · 28 = 2,940 points to, is: multiply the numbers as if they were whole numbers, then use place value (powers of ten) to put the decimal point back.

- 1.05 = 105 ÷ 100, and 2.8 = 28 ÷ 10
- So (1.05)(2.8) = (105 · 28) ÷ 1,000 = 2,940 ÷ 1,000 = **2.94**
- Check: 1 × 2.8 ≈ 2.8, and 1.05 is a bit more than 1, so an answer a bit above 2.8 makes sense.

---

## Practices needed, in order

I used the NAEP Mathematics Framework (2026) practices (Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics) plus **Procedural Fluency** from the NRC's *Adding It Up* strands.

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Abstracting and Generalizing** (NAEP) | Understands Priya's method as a general rule for multiplying decimals: multiply as whole numbers, then adjust by powers of ten. Applies it to this new pair of numbers. This is the main demand, since the item says "use Priya's method." |
| 2 | **Representing** (NAEP) | Rewrites the decimals in another form: 1.05 = 105/100 and 2.8 = 28/10, so the product is (105 · 28)/1,000. This links the decimal problem to the whole-number fact. |
| 3 | **Procedural Fluency** (NRC) | Does the computation accurately: uses 2,940, divides by 1,000 (moves the decimal point three places, or counts 2 + 1 = 3 decimal places), and gets 2.940 = 2.94. |
| 4 | **Justifying and Proving** (NAEP), minor and optional | Checks that the decimal point is in the right place by estimating (about 1 × 3 ≈ 3, so 2.94 is reasonable, not 29.4 or 0.294). The item doesn't ask for a justification, so this is only a self-check. |

**Not involved:** Mathematical Modeling (there's no real-world situation) and Collaborative Mathematics (it's an individual item).

**Order in brief:** Abstracting and Generalizing → Representing → Procedural Fluency → (Justifying and Proving as a check).

Main practices: **Abstracting and Generalizing** and **Procedural Fluency**, with **Representing** as the step that connects them.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

**Why this one:**

- **The item is built around transferring a method.** It says "Use Priya's method," so the student has to take a worked strategy (multiply as whole numbers, then adjust by powers of ten) and apply it to a new pair of numbers. Spotting that general structure and reusing it is what Abstracting and Generalizing means.
- **The hard part of the computation is already done.** Since 105 · 28 = 2,940 is given, there is almost no arithmetic left. What remains is seeing why 1.05 · 2.8 relates to 105 · 28: the factors are scaled by 1/100 and 1/10, so the product is scaled by 1/1,000. That is a relationship between structures, not a procedure being carried out.
- **The other practices support this step.** Representing (writing 1.05 = 105/100 and 2.8 = 28/10) is how the student shows the generalization. Procedural Fluency (moving the decimal point three places to get 2.94) is a small final step once the structure is understood.

**Runner-up: Procedural Fluency.** A student who just memorized "count the decimal places, 2 + 1 = 3" could get 2.94 without reasoning about the method. If the item is scored only on the final answer, procedure alone can be enough. But the wording ("use Priya's method," "you can use the fact that...") is designed to bring out generalizing from a known result, so I would label it Abstracting and Generalizing.

---

## Row 163 (problem_id 153894)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
There are 90 kids in the band. 20% of the kids own their own instruments, and the rest rent them.
How many kids rent instruments?
____ kids
```

### Answer 1: practices in order

**Problem:** There are 90 kids in the band. 20% of them own their own instruments, and the rest rent them. How many kids rent instruments?

**Answer: 72 kids**

The NAEP mathematical practices (from the 2026 NAEP Mathematics Framework) are:

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

I've added a sixth practice, **Procedural Fluency**, from the NRC's *Adding It Up* strands of mathematical proficiency.

---

### Practices needed, in order

**1. Mathematical Modeling (formulate)**
Turn the word problem into a math problem. Name the whole (90 kids). Note that "own" and "rent" divide the whole into two parts: 20% own, so the rest (80%) rent. See that the question asks for the *rent* group, not the 20% group the problem mentions. Most of the thinking happens here. The common mistake is answering 18, the number who own.

**2. Representing**
Write the situation in mathematical form. Two routes work:
- Direct: rent = 80% of 90 = 0.80 × 90
- Two steps: own = 0.20 × 90, then rent = 90 − own
(A percent bar or tape diagram split into 10% blocks of 9 kids each also works.)

**3. Procedural Fluency (NRC)**
Do the arithmetic correctly and quickly:
- 100% − 20% = 80%
- 0.80 × 90 = 72 (or 10% of 90 = 9, so 80% = 8 × 9 = 72)
- Or: 0.20 × 90 = 18, then 90 − 18 = 72

**4. Mathematical Modeling (interpret and validate)**
Take the result back to the story. Check that 72 + 18 = 90, that 72 is more than half (it should be, since 80% rent), and that the answer is a whole number of kids. Answer: **72 kids**.

---

### Practices not really needed
- **Abstracting and Generalizing:** no pattern or general rule is required. This is a single case.
- **Justifying and Proving:** the item asks for a number, not an argument. The step 4 check is light self-checking, not formal justification.
- **Collaborative Mathematics:** this is an individual item.

### Summary order
**Mathematical Modeling (formulate) → Representing → Procedural Fluency → Mathematical Modeling (interpret/check)**

Main practices: Mathematical Modeling and Procedural Fluency. Supporting practice: Representing.

### Answer 2: major practice

**Major practice: Mathematical Modeling**

**Why:**
- **It's where the problem is hard.** The arithmetic is easy (0.20 × 90 = 18, 90 − 18 = 72, or 0.8 × 90 = 72). The real demand is reading the situation correctly. The 90 kids are the whole, and they split into two parts: own and rent. The problem gives the percent for the part it *doesn't* ask about. So the student has to see that "the rest" means 80%, or that they must subtract after finding 20%.
- **It's where students go wrong.** The usual wrong answer is 18, the number who own. That's a modeling error (they answered the wrong question), not a calculation error. A student who models the situation correctly almost always gets 72.
- **It covers the whole solution.** Modeling starts the solution (turning the story into math) and ends it (checking that 72 + 18 = 90 and that 72 makes sense as a count of kids).

**Close second: Procedural Fluency.** The student does need to compute a percent of a number reliably, and many would label this item a routine percent calculation. But the arithmetic is simple, and the problem doesn't really test it. It tests whether the student sets up the right calculation.

---

## Row 169 (problem_id 80072)

- **predicted_practice:** Representing
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
Another stack of books is 43 inches tall. Each book is 1/2 -inch thick.
Write an expression that represents the number of books in the stack.
____
```

### Answer 1: practices in order

**Problem:** A stack of books is 43 inches tall, and each book is 1/2 inch thick. Write an expression for the number of books in the stack.

**Answer:** 43 ÷ 1/2 (equivalently 43 × 2, which equals 86 books)

---

### Practices available

NAEP 2026 Mathematics Framework practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from NRC (*Adding It Up*):
6. Procedural Fluency

---

### Practices used, in order

**1. Mathematical Modeling (main practice).**
The student turns the real-world situation into a math relationship. They have to see that the total height is made of equal "chunks" of 1/2 inch, one per book. So the question "how many books?" becomes "how many 1/2s fit into 43?", which is a measurement (quotative) division. Picking the right operation (divide, not multiply 43 × 1/2) is the key thinking step, and it is where most mistakes happen.

**2. Representing.**
Next the student writes that relationship in symbols: **43 ÷ 1/2**. The task asks for an expression, so this written form is what gets graded. The student can also show it as 43 × 2 (two books per inch), which is an equivalent form.

**3. Procedural Fluency (optional or supporting).**
The problem only asks for an expression, so no computation is strictly needed. Still, a student who can quickly divide by a fraction (43 ÷ 1/2 = 43 × 2 = 86) can use the result to check that the expression makes sense. For example, 86 books × 1/2 inch = 43 inches. This practice is secondary here.

### Not used (or very minor)
- **Abstracting and Generalizing:** Not needed. It would only come in if the student wrote a general form such as height ÷ thickness.
- **Justifying and Proving:** The problem does not ask for an explanation.
- **Collaborative Mathematics:** This is an individual item.

### Summary

| Order | Practice | Role |
|---|---|---|
| 1 | Mathematical Modeling | See the situation as "how many 1/2s are in 43" (division) |
| 2 | Representing | Write the expression 43 ÷ 1/2 (or 43 × 2) |
| 3 | Procedural Fluency (NRC) | Optionally evaluate (86) to check the expression |

### Answer 2: major practice

**Major practice: Mathematical Modeling**

The hard part of this problem is understanding the situation, not writing symbols or doing arithmetic. The student has to see that a 43-inch stack made of 1/2-inch books means asking "how many halves fit into 43?". That makes it a division, 43 ÷ 1/2. The most common mistake is multiplying (43 × 1/2 = 21.5). That is a modeling error: the student picked the wrong operation for the context.

Once the relationship is clear, writing the expression (Representing) is simple. Computing 86 (Procedural Fluency) is not even required. So Mathematical Modeling is the practice that decides whether a student gets this item right.

---

## Row 173 (problem_id 77198)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
A scale drawing of a school bus has a scale of 1/2 inches to 5 feet. If the length of the school bus is 4 1/2 inches on the scale drawing, what is the actual length of the bus?
____ feet
```

### Answer 1: practices in order

**Answer: 45 feet**

**Practices available**
- NAEP 2026 mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics
- From the NRC strands: Procedural Fluency

**Practices used, in order**

1. **Representing.** Turn the words into math. "1/2 inch to 5 feet" is a ratio. Write the unknown as a proportion:
   (1/2 in) / (5 ft) = (4 1/2 in) / (x ft)
   You could also think of it as "how many 1/2-inch pieces fit in 4 1/2 inches?" The main thinking in this problem is switching from the scale statement to a ratio or proportion, with units kept straight (inches on the drawing, feet in real life).

2. **Procedural Fluency.** Do the arithmetic correctly and quickly:
   - Change 4 1/2 to 9/2 (or 4.5)
   - (9/2) ÷ (1/2) = 9, so there are 9 scale units
   - 9 × 5 ft = 45 ft
   (Cross-multiplying works too: x = 5 × 4.5 ÷ 0.5 = 45.)
   This is the step where students usually slip, for example by mishandling the mixed number or the fraction division.

3. **Mathematical Modeling (minor, at the end).** Check that the answer fits the real situation. A school bus about 45 ft long is realistic, so the answer makes sense. The model here is given, not built by the student, so this practice plays only a small part.

**Not really used:** Abstracting and Generalizing (you don't need a general rule), Justifying and Proving (no argument is asked for), and Collaborative Mathematics (it's a solo item).

**Order: Representing → Procedural Fluency → (light) Mathematical Modeling**

### Answer 2: major practice

**Major practice: Representing**

The key step is reading "1/2 inch to 5 feet" as a ratio between the drawing and the real bus, then setting up the proportion (1/2 in : 5 ft = 4 1/2 in : x ft). You can also think of it as counting how many 1/2-inch units fit in 4 1/2 inches. Once that representation is in place, the rest is routine: 4.5 ÷ 0.5 = 9, and 9 × 5 = 45 ft.

Procedural Fluency is a close second because the item does need fraction and mixed-number arithmetic. But the numbers are friendly, and the arithmetic is easy once the setup is right. When students get this wrong, it is usually because they misread the scale relationship, for example by multiplying 4 1/2 × 5 = 22.5 or confusing which quantity maps to which. That is a Representing error, not a computation error.

**Answer: 45 feet. Major practice: Representing.**

---

## Row 177 (problem_id 77528)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
A farm lets you pick 3 pints of raspberries for $12.00.
What is the cost per pint?
$ ____
```

### Answer 1: practices in order

**Practice set used:** the NAEP 2026 Mathematics Framework practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematical Discourse) plus **Procedural Fluency** from the NRC's *Adding It Up* strands.

**Problem:** 3 pints of raspberries cost $12.00. What is the cost per pint?

### Practices needed, in order

**1. Mathematical Modeling (main practice)**
The student turns a real-world situation into a math operation. "Cost per pint" is a unit rate, so the student has to see that the total cost gets split equally across the pints: cost per pint = $12.00 ÷ 3. This is the step that needs real thinking. It means knowing that "per" means division, and that the money is divided by the pints, not the other way around. The model here is a simple one-step model, but it is still the core of the item.

**2. Procedural Fluency (NRC)**
The student carries out the division: 12.00 ÷ 3 = 4.00. This is a basic fact (12 ÷ 3 = 4). The student also has to handle the money format and write the answer as dollars and cents.

**3. Representing (minor, optional)**
At the end, the student writes the result in the form the answer blank expects ($ 4.00). Some students may also picture the problem as 3 equal groups, or set up a ratio such as 12/3 = x/1. That step is a small act of representing, but most students won't need it.

### Practices not needed
- **Abstracting and Generalizing:** There's no pattern or general rule to find. It's a single specific case.
- **Justifying and Proving:** The student doesn't have to explain or defend the answer.
- **Collaborative Mathematical Discourse:** This is an individual, short-answer item.

### Summary
**Mathematical Modeling → Procedural Fluency** (with a light touch of **Representing** at the end).

**Answer:** $4.00 per pint

### Answer 2: major practice

**Major practice: Mathematical Modeling**

**Why:** Once the problem is set up, the math is just 12 ÷ 3 = 4, a basic fact that almost no student gets wrong. Students who miss this item usually miss it earlier, when they turn "3 pints for $12.00, what is the cost per pint?" into the right operation. They have to see that "per pint" means a unit rate. They also have to divide the dollars by the pints, not multiply and not divide the other way. That translation from the real situation to the math is the Mathematical Modeling step, and it's the part that separates students who get the item right from those who don't.

**Caveat:** This is a very thin model: one step, with a familiar context and whole numbers. If you read NAEP's Mathematical Modeling strictly as the full cycle (make assumptions, build the model, check it, revise it), this item barely counts. In that case, **Procedural Fluency** is a reasonable second choice, because the item then works as a routine unit-rate calculation. Still, if I can pick only one, I would choose **Mathematical Modeling**.

---

## Row 178 (problem_id 77616)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
A box contains 1 3/4 pounds of pancake mix. Jada used 7/8 pound for a recipe. What fraction of the pancake mix in the box did she use?
____
```

### Answer 1: practices in order

**Answer: 1/2**

## Practices available

From the NAEP 2026 Mathematics Framework, the mathematical practices are:
1. **Representing**
2. **Abstracting and Generalizing**
3. **Justifying and Proving**
4. **Mathematical Modeling**
5. **Collaborative Mathematics** (part of the framework but not assessed individually)

Added from the NRC's *Adding It Up* strands:
6. **Procedural Fluency**: carrying out procedures flexibly, accurately and efficiently.

## Practices needed, in order

**Step 1: Mathematical Modeling (formulate)**
Turn the story into math. "What fraction of the mix did she use?" is a part-of-whole question: the part (7/8 lb) divided by the whole (1 3/4 lb). The hard part is seeing that the answer is a ratio, not a subtraction (1 3/4 − 7/8) and not just "7/8".

**Step 2: Representing**
Write the relationship as symbols and switch to a form you can compute with:
- 1 3/4 = 7/4
- Fraction used = (7/8) ÷ (7/4), or (7/8) / (7/4)
(Another option is to write both amounts in eighths: 7/8 and 14/8. Then the comparison is 7 out of 14.)

**Step 3: Procedural Fluency**
Do the computation correctly:
- (7/8) ÷ (7/4) = (7/8) × (4/7) = 28/56 = **1/2**
- Or, with eighths: 7/14 = 1/2

**Step 4: Mathematical Modeling (interpret / validate)**
Read the result back into the story and check that it makes sense. 7/8 is half of 14/8 (= 1 3/4), so Jada used half the box. The answer is 1/2, not a weight in pounds.

## Practices not needed
- **Abstracting and Generalizing**: there is no pattern or general rule to find.
- **Justifying and Proving**: the item asks for a number only, not an argument. (The Step 4 check is a light sense-check, not a formal justification.)
- **Collaborative Mathematics**: the item is solved by one student.

**Order: Mathematical Modeling → Representing → Procedural Fluency → Mathematical Modeling (interpret)**

### Answer 2: major practice

**Major practice: Mathematical Modeling**

This item is hard because of how you set it up, not because of the arithmetic. The student has to read "what fraction of the pancake mix in the box did she use?" and see that it is a part-of-whole relationship: 7/8 lb divided by 1 3/4 lb. The common wrong answers come from getting this formulation wrong:
- answering **7/8** (just repeating the amount used, in pounds),
- answering **7/8 lb left** (1 3/4 − 7/8, i.e. subtracting instead of comparing),
- or dividing the wrong way (7/4 ÷ 7/8 = 2).

Once the student has the correct model, (7/8) ÷ (7/4), the other steps are fairly routine:
- **Representing** (1 3/4 → 7/4 or 14/8) is a standard conversion.
- **Procedural Fluency** (7/8 × 4/7 = 1/2, or 7/14 = 1/2) is a short computation with friendly numbers. The 7s cancel.

The last step, checking that "half the box" makes sense, is also part of Mathematical Modeling. So Mathematical Modeling covers both the hardest step and the bookend steps of the solution.

If you wanted a runner-up, it would be **Procedural Fluency**. But the numbers are simple enough that fluency probably separates fewer students than modeling does.

---

## Row 182 (problem_id 57665)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
A large bucket holds 5 gallons of water, which is about the same as 19 liters of water.
A small bucket holds 2 gallons of water. About how many liters does it hold?
____ liters
```

### Answer 1: practices in order

**Problem:** 5 gallons ≈ 19 liters. About how many liters does a 2-gallon bucket hold?

**Answer:** about 7.6 liters (≈ 8 liters)

## Practices available

The NAEP 2026 Mathematics Framework lists these mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I'm adding **Procedural Fluency** from the NRC's *Adding It Up* strands.

## Practices used, in order

### 1. Representing
Turn the words into a math relationship. You can write it as a ratio or proportion, such as 5 gal : 19 L = 2 gal : ? L, or 5/19 = 2/x, or as a small two-column table (gallons | liters).
*Why it's first:* until the quantities are set up this way, there is nothing to calculate.

### 2. Abstracting and Generalizing
Notice that the gallon-to-liter relationship is **proportional**: every gallon is worth the same number of liters. So you can find a unit rate (19 ÷ 5 = 3.8 liters per gallon) and use it for any number of gallons. You could also scale directly: 2 gallons is 2/5 of 5 gallons, so the answer is 2/5 of 19 liters.
*Why it's here:* this step picks the method. It moves from one given fact to a rule that works for any amount.

### 3. Procedural Fluency (NRC)
Do the arithmetic correctly and quickly:
- 19 ÷ 5 = 3.8 L per gallon
- 3.8 × 2 = 7.6 L
- (or 19 × 2 = 38, then 38 ÷ 5 = 7.6)
*Why it's here:* the plan is set, so what's left is a multi-step calculation with decimals or fractions.

### 4. Justifying (reasonableness check), minor
Check that the answer makes sense. 2 gallons is a bit less than half of 5 gallons. Half of 19 is 9.5, so the answer should be a bit under 9.5. Also, 1 gallon ≈ 4 liters, so 2 gallons ≈ 8 liters. 7.6 fits both checks. The word "about" means 7.6 or 8 are both fine.
*Why it's last and minor:* the item asks for a number, not an explanation. This step is just a quick self-check.

### Not really used
- **Mathematical Modeling:** the context is real-world, but the item gives you the conversion and the question directly. You don't have to make assumptions or build a model from a messy situation. At most it plays a very small role.
- **Collaborative Mathematics:** this is an individual item.

## Summary order
**Representing → Abstracting & Generalizing (proportional reasoning / unit rate) → Procedural Fluency → Justifying (reasonableness check)**

The main practices are Representing, Abstracting & Generalizing, and Procedural Fluency. Justifying is a small extra step.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (proportional reasoning / unit rate)**

**Why this one:**
- **It's the main hurdle.** The key step is seeing that liters and gallons are proportional: every gallon is the same number of liters. Then you apply that rate to 2 gallons, either as 19 ÷ 5 × 2 or as 2/5 of 19. Students who miss this usually make an additive mistake, for example "5 − 2 = 3, so 19 − 3 = 16 liters." That is the classic error on this item.
- **Representing is easy here.** The problem gives one simple pair (5 gal ↔ 19 L). Writing it as a ratio takes very little work.
- **Procedural Fluency is second.** 19 ÷ 5 = 3.8 and 3.8 × 2 = 7.6 take some care with decimals. But "about" makes estimating (≈ 4 L per gallon → ≈ 8 L) acceptable. So the arithmetic is not what decides success.
- **Justifying is only a quick self-check.** The item asks for a number, not an argument.

**Ranking:** Abstracting & Generalizing (major) > Procedural Fluency > Representing > Justifying (minor)

---

## Row 184 (problem_id 87931)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the slope of the graph between 0 and 10?
____
```

### Answer 1: practices in order

## Practices for: "What is the slope of the graph between 0 and 10?"

Note: the graph itself isn't included in the problem text, so I can't give the numeric answer. The practices and their order are the same for any graph like this, though.

The NAEP Mathematics Framework names five mathematical practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, and (5) Collaborative Mathematics. As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands.

### Practices used, in order

1. **Representing (NAEP)**: *primary practice*
   The student has to read the graph. That means finding the x-values 0 and 10 on the horizontal axis and reading the matching y-values off the line or curve. The information starts out as a picture and has to become numbers: the points (0, y₀) and (10, y₁₀). This is the main thinking step in the problem, and most errors happen here, such as misreading the scale or mixing up the axes.

2. **Procedural Fluency (NRC)**: *secondary practice*
   Next the student applies the slope formula correctly:
   slope = (y₁₀ − y₀) / (10 − 0) = rise / run.
   This means subtracting in the right order, dividing, and simplifying. It's a routine procedure once the points are known.

3. **Representing (NAEP), brief return**: *interpretation check*
   Last, the student matches the answer to the picture. If the graph goes up from left to right, the slope should be positive. If it goes down, it should be negative. If it's flat, it should be zero. This is a quick consistency check, not a separate main step.

### Practices not meaningfully used
- **Abstracting and Generalizing**: no general pattern or rule has to be found. The student uses a known definition of slope.
- **Justifying and Proving**: the student doesn't have to give an argument or explain why.
- **Mathematical Modeling**: there's no real-world situation to turn into math.
- **Collaborative Mathematics**: this is a single-student item.

### Summary
**Representing → Procedural Fluency (→ quick Representing check)**

Representing is the main practice because getting the right coordinates from the graph is the hard part. Procedural Fluency comes second because the calculation itself is routine.

### Answer 2: major practice

## Major practice: **Representing (NAEP)**

If I have to pick just one, it's **Representing**.

**Why:**
- **The hard part is reading the graph.** To answer, the student has to find x = 0 and x = 10, read the matching y-values at the right scale, and turn the picture into the numbers rise and run. Most errors come from this step: misreading the axis scale, swapping x and y, or reading the wrong point.
- **The procedure is short and routine.** After the two points are known, (y₁₀ − y₀) / 10 is one subtraction and one division. Procedural Fluency is needed, but it isn't what makes the item hard.
- **The item is built around a graph.** The question exists to check whether a student can get slope from a graph. Without the graph it would just be arithmetic. Linking the graph to the meaning of slope as rate of change (rise over run) is a Representing skill.

**Ranking:** Representing (major) > Procedural Fluency (supporting).

---

## Row 186 (problem_id 88453)

- **predicted_practice:** Justifying and Proving
- **claude_top_practice:** Representing

### Problem

```text
How many circles of radius 1 can you fit inside a circle of radius 3 units so that they do not overlap?
If you get stuck, consider using coins or other circular objects.
____
```

### Answer 1: practices in order

**Answer: 7 circles.** Put one circle in the center and six around it. Each outer circle touches the center circle and the big circle.

## Practices used

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Problem Solving. I added Procedural Fluency from the NRC's *Adding It Up*.

This problem uses four of them, in this order:

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** (NAEP) | Turns the words into a picture. Draws a circle of radius 3 and places unit circles (or coins) inside it. The hint about coins points straight to this practice. |
| 2 | **Mathematical Modeling** (NAEP) | Simplifies the picture into a geometric model. Each small circle becomes its center point, and two rules follow: (a) every center must be at most 3 − 1 = 2 from the big center, so it stays inside; (b) any two centers must be at least 1 + 1 = 2 apart, so they don't overlap. |
| 3 | **Procedural Fluency** (NRC) | Does the calculations. One circle sits at the center. Each ring circle's center lies 2 from the big center. Adjacent ring centers are exactly 2 apart, so each pair forms an equilateral triangle with the big center, giving 60° per circle and 360° / 60° = 6 ring circles. Total: 1 + 6 = 7. |
| 4 | **Justifying and Proving** (NAEP) | Explains why 7 is the most and an 8th won't fit. All centers must lie within distance 2 of the big center, and every pair must be at least 2 apart. Putting more than 6 centers on the ring makes each angle smaller than 60°. For example, 7 on the ring gives a gap of 2·2·sin(180°/7) ≈ 1.74 < 2, so they overlap. Moving a circle inward collides with the center circle. So 7 is the maximum. |

**Not really needed:**
- **Abstracting and Generalizing** would only come in as an extension, such as noticing the hexagonal "1 + 6" pattern or asking what happens with other radius ratios.
- **Collaborative Problem Solving** doesn't apply because this is a single-student item.

**Order in short:** Representing → Mathematical Modeling → Procedural Fluency → Justifying and Proving.

### Answer 2: major practice

**Major practice: Representing (NAEP).**

The main job here is spatial: draw or arrange unit circles inside a radius-3 circle and see how many fit. My reasons:

- **The problem's own hint is a representation.** "Consider using coins or other circular objects" asks students to build a physical or drawn model of the setup. That is Representing.
- **The answer comes from the picture.** Once the student draws one circle in the center with a ring around it, the "1 + 6 = 7" arrangement is easy to see. Little calculation is needed.
- **The other practices play supporting roles.**
  - Mathematical Modeling (centers within 2 of the middle, at least 2 apart) only formalizes what the drawing already shows.
  - Procedural Fluency is light: 3 − 1 = 2, 360° / 60° = 6, 1 + 6 = 7.
  - Justifying and Proving would matter if the item asked "explain why no more fit." The item only has an answer blank, so it doesn't require a proof.

If the item asked students to prove that 7 is the maximum, I would pick Justifying and Proving instead. As written, a student who can represent the situation well will solve it.

---

## Row 187 (problem_id 88478)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
In her English class, Mai’s teacher gives 4 quizzes each worth 5 points. After 3 quizzes, she has the scores 4, 3, and 4. What does she need to get on the last quiz to have a mean score of 4?
____
```

### Answer 1: practices in order

## Practices to use (NAEP 2026 Mathematical Practices + NRC Procedural Fluency)

The NAEP 2026 framework lists these mathematical practices: **Representing**, **Abstracting and Generalizing**, **Justifying and Proving**, **Mathematical Modeling**, and **Collaborative Mathematics**. As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands.

**Answer: 5 points.** She needs 4 × 4 = 16 points in total, she has 4 + 3 + 4 = 11, and 16 − 11 = 5.

### Order of practices

**1. Representing (main practice)**
Turn the words into math. "A mean of 4 over 4 quizzes" becomes an equation, (4 + 3 + 4 + x) / 4 = 4. You could also say it as a total: the 4 scores must add up to 4 × 4 = 16. This is the key step. Once the mean condition is written as a needed total or an equation, the rest is routine.

**2. Procedural Fluency (NRC)**
Do the arithmetic correctly:
- 4 + 3 + 4 = 11
- 4 × 4 = 16 (or multiply both sides by 4)
- 16 − 11 = 5, so x = 5

**3. Justifying and Proving (light, as a check)**
Make sure the answer makes sense in the problem. Each quiz is worth 5 points, so a score of 5 is possible: it is the maximum. Check it: (4 + 3 + 4 + 5) / 4 = 16 / 4 = 4. You can also check by deviations: the scores are 0, −1, 0 away from 4, so the last quiz has to make up +1, and 4 + 1 = 5.

### Practices not really needed
- **Mathematical Modeling**: The situation is already stated in clean math terms, with no assumptions or real-world simplifying to do. At most it's a very small part of Representing.
- **Abstracting and Generalizing**: Nothing needs to be generalized. One could note the general rule "needed score = n × target mean − current sum", but the problem doesn't ask for it.
- **Collaborative Mathematics**: Not part of a single-student item.

### Summary
**Representing → Procedural Fluency → Justifying and Proving (check)**

Representing is the main practice and also the most likely source of mistakes. For example, a student might take the mean of 4, 3, 4 and stop, or answer "4" without thinking about the total.

### Answer 2: major practice

## Major practice: Representing

If I have to pick one, it's **Representing**.

**Why:**
- **It's the hard part of the problem.** Mai has to turn "a mean score of 4 over 4 quizzes" into "the four scores must add up to 16", or write (4 + 3 + 4 + x) / 4 = 4. Once she has that, the rest is easy.
- **It's where students go wrong.** Common mistakes happen at this step: averaging 4, 3, 4 and stopping, answering "4" because the target mean is 4, or not linking the mean to a total. Those are representation mistakes, not arithmetic mistakes.
- **Procedural Fluency comes second.** The arithmetic (4 + 3 + 4 = 11, 4 × 4 = 16, 16 − 11 = 5) is simple whole-number work. A student who can represent the problem correctly will almost never miss the answer because of the calculation.
- **Justifying is only a quick check.** Confirming that 5 is allowed (it's the maximum score) and that the mean works out to 4 is helpful, but it isn't needed to get the answer.

**Answer: 5.**

---

## Row 188 (problem_id 88342)

- **predicted_practice:** Mathematical Modeling
- **claude_top_practice:** Representing

### Problem

```text
How many circles of radius 1 can you fit inside a circle of radius 2 units so that they do not overlap?
If you get stuck, consider using coins or other circular objects.
____
```

### Answer 1: practices in order

**Answer: 2 circles.**

The NAEP Mathematics Framework (2026) lists five mathematical practices: **Representing**, **Abstracting and Generalizing**, **Justifying and Proving**, **Mathematical Modeling**, and **Collaborative Mathematics**. I've added **Procedural Fluency** from the NRC's *Adding It Up* strands as a sixth.

### Practices used, in order

**1. Representing (start here)**
Turn the words into a picture. Draw the big circle (radius 2) and try placing small circles (radius 1) inside it, or use coins as the hint suggests. This step gets you to a first guess: two small circles fit side by side along a diameter, each touching the other at the big circle's center.

**2. Procedural Fluency (supporting step)**
Do the quick routine measurements correctly:
- Each small circle has diameter 2 × 1 = 2.
- The big circle has diameter 2 × 2 = 4.
- Two small diameters laid end to end: 2 + 2 = 4, exactly the big diameter. So two circles fit with no gap left along that line.

**3. Abstracting and Generalizing**
Move from the picture to a general condition. Think about where the center of each small circle can go rather than about the whole circle:
- A small circle stays inside the big one only if its center is at most 2 − 1 = **1** from the big center. So every small center lies in a disk of radius 1.
- Two small circles don't overlap only if their centers are at least 1 + 1 = **2** apart.

The question becomes: how many points can you put in a disk of radius 1 so that every pair is at least 2 apart?

**4. Justifying and Proving (finish here)**
Show that 2 is the maximum and not just your best attempt:
- The widest two points in a disk of radius 1 can be is its diameter, 2. So any two valid centers must sit at opposite ends of a diameter, on the boundary.
- A third center would have to be at least 2 from both. But the only point 2 away from one end of a diameter is the other end, which is already taken. So a third circle can't fit.
- Two circles are possible (step 1) and three are impossible (this step), so the answer is **2**.

### Practices not really used
- **Mathematical Modeling**: there's no real-world situation to model. The coins are a physical way to represent the problem, which counts as Representing.
- **Collaborative Mathematics**: the item is solved by one person.

### Summary of order
Representing → Procedural Fluency → Abstracting and Generalizing → Justifying and Proving

### Answer 2: major practice

**Major practice: Representing**

Why this one:

- **The item points to it.** The hint says "consider using coins or other circular objects." That tells students to make a physical or drawn version of the situation and test arrangements.
- **It's how most students get the answer.** Once you draw the radius-2 circle, or put two coins inside a circle twice their size, you can see right away that two small circles fill a diameter and there's no room for a third.
- **The item only asks for a number.** The answer is a fill-in ("____"), with no request for an explanation or proof. So Justifying and Proving is what an expert would do to be sure, but the item doesn't require it.
- **The other practices play smaller roles.** Procedural Fluency (2 × 1 = 2, 2 + 2 = 4) is minor arithmetic. Abstracting and Generalizing (reasoning about where the centers can go) is a more advanced path that most students won't take.

If the item asked students to *explain why* no more than two circles fit, I would choose **Justifying and Proving** as the major practice instead.

---

## Row 189 (problem_id 88561)

- **predicted_practice:** Mathematical Modeling
- **claude_top_practice:** Representing

### Problem

```text
How many circles of radius 1 can you fit inside a circle of radius 4 units so that they do not overlap?
If you get stuck, consider using coins or other circular objects.
____
```

### Answer 1: practices in order

## Practices used to solve the problem

The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added Procedural Fluency from the NRC's *Adding It Up* strands, as you asked.

This problem uses five of the six, in this order:

### 1. Mathematical Modeling
Turn the physical question ("fit coins inside a bigger circle without overlap") into a geometry question. If each small circle has radius 1, its center must be at least 2 units from every other center. It must also be at most 4 − 1 = 3 units from the big circle's center. The hint about coins invites a hands-on model.

### 2. Representing
Draw a diagram, or lay out coins. Put the big circle's center at O. Mark the circle of radius 3 where the centers of the outer small circles can sit. Then shade the region left over in the middle. The diagram shows the useful arrangement: an outer ring of circles touching the big circle, and a few circles inside it.

### 3. Procedural Fluency (NRC)
Do the calculations.
- **Outer ring:** each circle's center sits 3 units from O. Two touching circles on that ring take up a central angle of 2·arcsin(1/3) ≈ 38.94°. Then 360° / 38.94° ≈ 9.24, so **9** circles fit in the outer ring.
- **Inner region:** the outer ring circles reach in to 3 − 1 = 2 units from O, which leaves a free disc of radius 2. A disc of radius 2 holds exactly **2** circles of radius 1, placed side by side through its diameter.
- **Total:** 9 + 2 = **11**.

### 4. Abstracting and Generalizing
Notice the general strategy: fill the outer ring first, then pack the smaller disc left in the middle. This is the same problem over again at a smaller size. Also compare it with the simple hexagonal layout (1 in the center + 6 around it = 7). That layout leaves a lot of empty space, so better arrangements must exist.

### 5. Justifying and Proving
Check that the arrangement works. Neighbouring centers on the ring are 2·3·sin(19.47°) ≈ 2 apart or more. The inner circles stay inside radius 2, so they don't overlap the ring. Every circle stays inside radius 4. To argue that a 12th circle can't fit: the outer ring can't hold a 10th circle (9.24 < 10), and the radius-2 disc can't hold a 3rd. This matches the known optimal packing result: 12 unit circles need an enclosing radius of about 4.03, which is more than 4.

(Collaborative Mathematics is not needed for an individual solution, though the coin activity could be done in groups.)

**Order:** Mathematical Modeling → Representing → Procedural Fluency → Abstracting and Generalizing → Justifying and Proving

**Answer: 11 circles**

### Answer 2: major practice

## Major practice: Representing

If I had to pick one, it would be **Representing**.

**Why:**
- **The main difficulty is seeing the arrangement.** No formula gives the answer. You have to find a good way to lay out the circles: an outer ring of 9 with 2 more in the middle. You find that by drawing the circles or moving physical objects around.
- **The problem itself points to this.** The hint "consider using coins or other circular objects" asks students to build a concrete model and work with it. That is representing.
- **The other practices depend on it.** The calculations (Procedural Fluency) and the check that it works (Justifying and Proving) only make sense once a diagram shows which arrangement to test. The modeling step needed to set up the problem is small. Turning "fit coins" into "centers at least 2 apart and within 3 of the middle" takes very little work.
- **It's what separates answers.** Students who don't explore different layouts usually stop at the hexagonal 7. Students who draw or try several layouts find 11.

**Runner-up:** Mathematical Modeling, because the problem starts as a physical fitting task. But the deciding step is finding and showing the arrangement, so Representing is the main practice.

---

## Row 190 (problem_id 88244)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the slope of the graph between 11 and 15?
____
```

### Answer 1: practices in order

## Practices to choose from

The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. **Representing**: reading, interpreting, making and moving between representations (graphs, tables, equations, words).
2. **Abstracting and Generalizing**: spotting structure and patterns and stating general rules.
3. **Justifying and Proving**: building and checking mathematical arguments.
4. **Mathematical Modeling**: using math to describe and analyze a real-world situation.
5. **Collaborative Mathematics**: working with others on mathematical ideas.

You asked me to add a sixth:
6. **Procedural Fluency** (from the NRC's strands of proficiency): carrying out procedures flexibly, accurately and efficiently.

## Problem

> "What is the slope of the graph between 11 and 15?"

The graph isn't in the problem text. I assume it is a line or piecewise graph, and "11" and "15" are x-values on its horizontal axis.

## Practices needed, in order

**Step 1: Representing (main practice)**
- Read the graph to find the points where x = 11 and x = 15, and their y-values: (11, y₁) and (15, y₂).
- Understand that "slope between 11 and 15" means the rate of change over that part of the graph. You can see it as rise over run: the vertical change divided by the horizontal change.
- This is the core of the problem. The student has to pull numbers out of a visual representation and understand what slope looks like on a graph.

**Step 2: Procedural Fluency**
- Apply the slope formula: m = (y₂ − y₁) / (15 − 11) = (y₂ − y₁) / 4.
- Do the subtraction and division correctly. This includes keeping the sign right when the graph goes down (negative slope) and simplifying the fraction or decimal.

**Step 3: Representing again (short check)**
- Look back at the graph to see if the answer makes sense. Rising means positive slope, falling means negative, and flat means zero. Steeper segments should give larger absolute values.

## Practices not needed

- **Abstracting and Generalizing**: no pattern or general rule is asked for. It is one calculation on one interval.
- **Justifying and Proving**: the question asks for a number, not an explanation.
- **Mathematical Modeling**: the problem as given has no real-world setting to model. If the graph has a context (for example distance vs. time), reading the slope as a unit rate would add a small modeling or interpreting step after Step 2.
- **Collaborative Mathematics**: it is a single-student item.

## Summary

**Representing → Procedural Fluency → (Representing, as a check)**

Representing is the main practice: reading the graph and understanding slope as rise over run. Procedural fluency is second: computing the change in y divided by the change in x correctly.

### Answer 2: major practice

**Major practice: Representing**

Why:
- **The hard part is reading the graph.** The student has to find x = 11 and x = 15 on the graph, read the matching y-values correctly, and understand that "slope between 11 and 15" means the rise over the run on that segment. That means turning a visual representation into numbers and back, which is what Representing covers.
- **The calculation is small.** Once the two points are known, (y₂ − y₁) / 4 is one subtraction and one division. Procedural fluency is needed, but it is a supporting step.
- **Most errors come from the graph.** Students typically go wrong by reading the wrong grid value or mixing up the axes. They also tend to compute run over rise, or lose the sign on a falling segment. All of these come from interpreting the graph, not from doing arithmetic.

**Procedural Fluency** would be the secondary practice.

---

## Row 192 (problem_id 91688)

- **predicted_practice:** Justifying and Proving
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Based on the information in the table, what do you think the inventory will be at on Saturday morning? Explain your reasoning.
____
```

### Answer 1: practices in order

**Note:** The table the problem refers to isn't included, so I can't work out the actual Saturday number. The practices and their order depend on the type of task, not on the specific values, so I can still map them. The task: read daily inventory values from a table, find the pattern, extend it to Saturday morning, and explain why.

**Practice set used:** the five mathematical practices in the NAEP Mathematics Framework (Representing; Abstracting and Generalizing; Justifying and Proving; Mathematical Modeling; Collaborative Mathematics), plus **Procedural Fluency** from the NRC's *Adding It Up* strands.

## Practices in the order they are used

**1. Representing**
- Read the table and turn it into a usable form: which column is the day, which is the inventory, and how the rows line up (for example Monday morning to Friday morning).
- Change the table into another view, such as a list of day-to-day changes (+/− amounts) or a quick mental graph of inventory over time. The pattern becomes visible in that view.

**2. Abstracting and Generalizing**
- Find the regularity in the changes. Is it a constant drop each day (linear), a constant percent drop, or a repeating cycle such as a restock?
- State it as a general rule, for example "inventory goes down by *d* each day" or *I(n) = I₀ − d·n*. Only a rule like that lets you go beyond the given rows.

**3. Mathematical Modeling**
- Treat the rule as a model of a real situation and use it to predict past the data, out to Saturday morning.
- Check whether the model makes sense in context. Does the store restock? Is Saturday morning exactly one step after the last row, or two? Can inventory go below zero? Change the prediction if the context calls for it.

**4. Procedural Fluency (NRC)**
- Do the arithmetic accurately and efficiently: subtract or add the change for each step (or multiply the rate by the number of days) to get the Saturday value.
- This is the step that actually produces the number. Mistakes here make the answer wrong even if the reasoning is right.

**5. Justifying and Proving**
- The prompt says "Explain your reasoning," so the answer must be backed up. Point to the consistent change in the table, show that the rule fits every given day, and show how applying it once more (or *n* more times) gives the Saturday value.
- Mention any assumption, for example "assuming sales continue at the same rate and no new stock arrives."

**Collaborative Mathematics:** not needed. This is a single-student written task, with no step where you build on or critique someone else's reasoning.

## Summary order

**Representing → Abstracting and Generalizing → Mathematical Modeling → Procedural Fluency → Justifying and Proving**

The main practices are **Abstracting and Generalizing** (finding the pattern) and **Justifying and Proving** (the required explanation). Representing is the entry point. Procedural Fluency carries out the calculation.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

Why this one:

- **It decides the answer.** Saturday morning isn't in the table, so a student has to find the pattern in the inventory values (for example, "it drops by the same amount each day") and extend it past the data. Get the pattern right and the prediction follows. Miss it and nothing else can fix the answer.
- **The other practices depend on it.** Representing just sets up the data to look for a pattern. Modeling and Procedural Fluency apply the rule and do the arithmetic. Justifying explains the rule. Each one needs the generalization first.
- **It is where students most often go wrong.** Reading the table and doing the subtraction are routine. The thinking that makes this task hard is spotting the regularity and trusting it enough to predict with it.

**Close second: Justifying and Proving.** The prompt says "Explain your reasoning," so the explanation is part of the score. What it explains, though, is the generalization: why the pattern holds and how it gives the Saturday value. That makes it secondary to Abstracting and Generalizing.

---

## Row 193 (problem_id 91790)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the difference between greatest and least inventory?
____
```

### Answer 1: practices in order

**Note:** The problem refers to inventory data ("greatest and least inventory"), but no table, graph or list of values was included. My answer below assumes the original item shows the inventory amounts in a data display, such as a table, bar graph or pictograph.

**Practices available:**
- NAEP 2026 Mathematics Framework practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics
- From the NRC (*Adding It Up*): Procedural Fluency

**Practices needed, in order:**

1. **Representing (NAEP).** The student has to read the data display and turn it into numbers. That means pulling the inventory value for each item or time period from the table or graph, then comparing them to find the greatest and the least. Reading the scale on a graph, or the key on a pictograph, is part of this step. It is the main thinking step, and most errors happen here, for example misreading a bar or picking the wrong extreme.

2. **Procedural Fluency (NRC).** Once the two values are known, the student subtracts: greatest minus least. This is the "difference", which is the range of the data. Subtracting accurately and quickly, including regrouping if needed, is procedural fluency. The student also needs to know that "difference" means subtraction, but that is a quick translation and not a separate practice.

**Practices not needed:**
- **Mathematical Modeling:** There is no real-world situation to turn into a model. The quantities and the operation are given directly.
- **Abstracting and Generalizing:** The student finds one specific number. No pattern or general rule is involved.
- **Justifying and Proving:** The student only enters a number. No explanation or argument is asked for.
- **Collaborative Mathematics:** This is a task done alone.

**Summary:** Representing, then Procedural Fluency.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

**Why:** Most of the work in this problem is reading the data display. The student has to pull the inventory values out of the table or graph, read the scale or key correctly, and find the greatest and least values. This is where the problem is hard and where most students go wrong. They might misread a bar height or a pictograph key, or pick the wrong value as the greatest or least.

Procedural Fluency is still needed for the last step, greatest minus least. But that subtraction is usually simple whole-number work. It only gives the right answer if the two values were read correctly first. Representing is the practice that sets this item apart from a plain subtraction problem.

One caveat: the data display wasn't included in the problem text. If the inventory values were given directly as large numbers that need regrouping, and finding the greatest and least were trivial, Procedural Fluency could be the major practice instead. For the usual "read the graph/table" version of this item, Representing is the major practice.

---

## Row 199 (problem_id 96902)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
What is the probability the computer produces the first letter of your first name?
____
```

### Answer 1: practices in order

**Problem:** What is the probability that the computer produces the first letter of your first name?

**What I'm assuming:** The problem text doesn't show the setup, but this type of item normally has a computer that picks one letter of the English alphabet at random, with every letter equally likely. So there are 26 possible outcomes and 1 of them is a success.

**Answer:** 1/26 (about 0.038, or roughly 3.8%)

---

### The practices available

The NAEP Mathematics Framework (2026) lists these mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

To these I've added **Procedural Fluency**, one of the five strands of mathematical proficiency in the NRC's *Adding It Up*.

### Practices used, in order

**1. Mathematical Modeling (main practice)**
The student turns a real situation into a probability model. Here that means seeing that the computer's output is one random draw from the 26 letters, that each letter is equally likely, and that a "success" is exactly one letter: the first letter of their own name. Making that equally-likely assumption, and seeing that it doesn't matter which letter their name starts with, is the main thinking the problem asks for.

**2. Representing**
The student writes the model as a probability: P(event) = favorable outcomes / total outcomes = 1/26. This moves from words to a symbolic fraction.

**3. Procedural Fluency (NRC)**
The student carries out the routine part: counts the outcomes (1 favorable out of 26) and writes the answer as a fraction in simplest form (1/26), or as a decimal or percent if asked. This takes little effort, but it's the step that produces the number.

**4. Abstracting and Generalizing (minor, optional)**
A student might notice that the answer is the same for every student, whatever their name. In general, the probability of any single outcome out of n equally likely outcomes is 1/n. This deepens understanding but isn't needed to get the answer.

### Practices not needed
- **Justifying and Proving:** the item asks for a value, not an argument.
- **Collaborative Mathematics:** it's an individual item.

### Summary
**Mathematical Modeling → Representing → Procedural Fluency** (with Abstracting and Generalizing as an optional extra). Modeling carries most of the thinking. Fluency only covers the final easy step of writing 1/26.

### Answer 2: major practice

**Major practice: Mathematical Modeling**

This is the step where students most often go wrong. The problem is set in a real situation (a computer producing a letter, and *your* name), and the student has to turn it into a probability model. That means seeing that the sample space is the 26 letters of the alphabet, that each letter is equally likely, and that exactly one of them is a favorable outcome, whichever letter their name happens to start with.

Once that model is in place, the other steps are routine. Writing it as P = 1/26 (Representing) and stating the fraction (Procedural Fluency) take very little extra thought. So the item really tests whether the student can model a random process in context. That makes Mathematical Modeling the major practice.

---

## Row 200 (problem_id 97230)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Find the area of each parallelogram.
[Image: Two different quadrilaterals on a grid. The one on the left is labeled A and the right one is labeled B.]
Parallelogram B: ____ square units.
```

### Answer 1: practices in order

**The NAEP mathematical practices** (2026 NAEP Mathematics Framework), plus the practice you asked to add:

1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematical Discourse
6. *(added)* Procedural Fluency (from NRC, *Adding It Up*): carrying out procedures flexibly, accurately and efficiently

**Note:** I can't see the grid image, so I can't give the numeric area for Parallelogram B. Below is the order of practices needed to solve the problem.

---

### Practices in order of use

**Step 1: Representing (primary)**
The figure is given as a picture on a grid, so the student has to turn it into numbers first:
- Pick a side of parallelogram B to use as the **base**, and count its length in grid units.
- Find the **height**: the perpendicular (straight up-and-down, or straight across) distance between that base and the opposite side. Count it in grid units too.
- The key step here is telling the height apart from the slanted side. A common mistake is to count the slanted edge instead.

**Step 2: Abstracting and Generalizing**
The student recognizes that B is a parallelogram. Then they apply the general rule that works for every parallelogram: **Area = base × height**. This rule comes from the idea that you can cut a triangle off one end and slide it to the other end to make a rectangle with the same base and height. The student needs to see that this specific figure is one case of that general rule.

**Step 3: Procedural Fluency (NRC)**
The student multiplies base × height correctly and gives the answer in **square units**. If B is drawn at a slant, a fluent alternative is to draw a rectangle around it, then subtract the corner triangles. This step should be quick and routine.

**Step 4 (optional): Justifying and Proving**
The student checks the answer another way. For example, they can count whole squares and combine the partial squares, or use the cut-and-slide picture to confirm that the area matches the rectangle. A plain fill-in-the-blank answer doesn't require this.

**Not needed:** Mathematical Modeling (there's no real-world situation to model) and Collaborative Mathematical Discourse (the task is done alone with no explanation to share).

---

### Summary

| Order | Practice | Role |
|---|---|---|
| 1 | Representing | Read the base and the perpendicular height from the grid |
| 2 | Abstracting and Generalizing | Apply A = b × h, which works for all parallelograms |
| 3 | Procedural Fluency (NRC) | Multiply correctly and give the answer in square units |
| 4 (optional) | Justifying and Proving | Check by counting squares or by decomposing the shape |

**Most important practice:** Representing. On a grid area problem, the hard part is finding the right height. Once you have it, the arithmetic is easy.

### Answer 2: major practice

**Major practice: Representing**

Why this one:

- **The problem is given only as a picture.** Parallelogram B is drawn on a grid with no numbers. Before you can use any formula, you have to turn the drawing into numbers: the base length and the perpendicular height.
- **This is where students get it wrong.** The most common mistake is to use the slanted side instead of the perpendicular height. If you read the grid correctly, you get the right answer. If you don't, you get it wrong.
- **The other practices are simple here.** Knowing A = base × height (Abstracting and Generalizing) is a standard fact for this grade level. Multiplying two small whole numbers (Procedural Fluency) is routine. Neither of these is likely to be what separates students who get it right from students who don't.

So the problem mostly tests whether a student can read the needed measurements off a grid drawing. That is Representing.

---

## Row 202 (problem_id 97915)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the probability of selecting a random month of the year and getting a month that starts with the letter “J?” If you get stuck, consider listing the sample space.
____
```

### Answer 1: practices in order

**Problem:** What is the probability that a month picked at random from the year starts with the letter "J"? (Hint: list the sample space.)

**Answer:** 3/12 = **1/4** (January, June, July)

---

### The practices used

From the NAEP Mathematics Framework (the mathematical practices):
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Modeling
5. Using Mathematical Tools
6. Collaborative Mathematics

Plus, from the NRC (*Adding It Up*) strands: **Procedural Fluency**

### Practices this problem needs, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Write out the sample space as a list of the 12 months (January through December). The hint asks for exactly this, and it is the key move: it turns a word question into a concrete set of outcomes you can count. |
| 2 | **Abstracting and Generalizing** (light use) | See the problem as an equally-likely-outcomes situation, so P(event) = favorable outcomes / total outcomes. Then pick out the event subset {January, June, July}. |
| 3 | **Procedural Fluency** (NRC) | Count the outcomes (3 favorable, 12 total), write the ratio 3/12, and simplify it to 1/4 (or 0.25 / 25%). |

**Not meaningfully used:** Justifying and Proving (no argument is asked for), Modeling (no real-world model has to be built or tested beyond "random = equally likely"), Using Mathematical Tools (none needed), and Collaborative Mathematics (individual item).

**Order summary:** Representing → Abstracting and Generalizing → Procedural Fluency

The main practice is **Representing**, since the item's own hint points to listing the sample space. Procedural fluency comes last, for the count and the simplification. Abstracting plays only a small part: recognizing the classical probability ratio.

### Answer 2: major practice

**Major practice: Representing**

Why this one:

- **The problem asks for it directly.** The hint says "consider listing the sample space," and writing the 12 months as a set of outcomes is a representation.
- **It does most of the work.** Once the months are written out, picking January, June and July and getting 3/12 = 1/4 is easy.
- **It is where students go wrong.** The usual mistakes are miscounting the months that start with "J" (missing June or July) or using the wrong total. Both are failures to represent the sample space correctly. The fraction itself is simple.
- **The other practices play smaller parts.** Procedural fluency here is just counting and simplifying 3/12, which is basic. Abstracting only means knowing the usual "favorable over total" rule.

So if you pick one, pick **Representing**. **Procedural fluency** would be second.

---

## Row 203 (problem_id 98095)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
A practice field is 250 feet long. The game field is 40% longer than the practice field. How long is the game field?
____ feet
```

### Answer 1: practices in order

**Problem:** A practice field is 250 feet long. The game field is 40% longer than the practice field. How long is the game field? **Answer: 350 feet**

## Practices available

NAEP Mathematics "mathematical complexity / process" practices (2026 framework):
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics (not applicable to an individual item)

Plus NRC strand: **Procedural Fluency**: carrying out procedures flexibly, accurately, and efficiently.

## Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (main practice) | Turn the word situation into math: "40% longer than 250" means the game field = practice field + 40% of the practice field. The real decision is reading "longer than" as *add on top of the original*, not "40% of 250." |
| 2 | **Representing** | Write that relationship as an expression: 250 + 0.40 × 250, or 1.40 × 250 (or 250 × 140/100). |
| 3 | **Procedural Fluency** | Do the arithmetic: 0.40 × 250 = 100, then 250 + 100 = 350 (or 1.4 × 250 = 350). |
| 4 | **Mathematical Modeling** (interpret/validate, brief) | Read the number back into the situation: 350 feet is longer than 250 feet, which makes sense, and it goes in the blank as feet. |

**Short order:** Mathematical Modeling -> Representing -> Procedural Fluency -> (quick Modeling check)

## Not needed

- **Abstracting and Generalizing:** nothing has to be generalized beyond this one case.
- **Justifying and Proving:** the item only asks for a number, with no argument or explanation.
- **Collaborative Mathematics:** this is an individual item.

## Most important practice

**Mathematical Modeling** (steps 1 and 4). The computation is light. The most common mistake is answering **100** (40% of 250) instead of 350, and that comes from misreading the situation, not from bad arithmetic. **Procedural Fluency** comes second, because students must compute a percent of a number correctly.

### Answer 2: major practice

**Major practice: Mathematical Modeling**

Why this one:

- **The main difficulty is interpreting the situation.** The student has to read "40% longer than the practice field" as the original length plus 40% more (250 + 0.40 × 250, or 1.4 × 250). That step turns a real-world statement into a mathematical relationship, which is what modeling means.
- **The most common wrong answer comes from modeling, not arithmetic.** Students who answer **100** (just 40% of 250) can compute fine. They set up the wrong model. The answer 350 depends on setting it up correctly.
- **The arithmetic is light.** 0.4 × 250 = 100 and 250 + 100 = 350 are routine. Procedural Fluency is needed, but it only supports the main step. It is not what separates students who get this right from those who don't.
- **Representing is a small step here.** Once the situation is understood, writing 1.4 × 250 follows almost automatically. So Representing is part of the modeling work rather than a separate challenge.

**Runner-up:** Procedural Fluency (computing a percent of a number correctly). It would be the major practice only if the item asked directly for "40% of 250", without the "longer than" context.

---

## Row 205 (problem_id 46235)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the third quartile (Q3)? ____
[Image: A dot plot showing word value in points. Goes from 0 to 22 by 2's. Beginning at 4 in increments of 1, the number of dots above each increment is 4, 2, 4, 3, 3, 3. There is a dot above 22.]
```

### Answer 1: practices in order

## Practices for this problem

**Practices to choose from.** The NAEP 2026 Mathematics Framework lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

You asked me to add a sixth from the NRC (*Adding It Up*):

6. **Procedural Fluency**: carrying out procedures accurately, efficiently and flexibly.

**Solution in brief.**
Read the dot plot:
- 4 has 4 dots, 5 has 2, 6 has 4, 7 has 3, 8 has 3 and 9 has 3.
- 22 has 1 dot.
- That makes n = 20.

Sorted data: 4, 4, 4, 4, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 22

The upper half is the 11th through 20th values: 7, 7, 7, 8, 8, 8, 9, 9, 9, 22.
Q3 is the median of the upper half, which is the average of the 15th and 16th values: (8 + 8)/2 = **8**.

### Practices needed, in order

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Representing** | Turns the dot plot into numbers. The student reads the height of each dot column as a frequency (4, 2, 4, 3, 3, 3 for the values 4 to 9, plus one dot at 22). Then they list the data as an ordered set and get n = 20. They need to read the scale correctly: the axis is labeled by 2's, but the dots sit on every whole number from 4 to 9. |
| 2 | **Procedural Fluency** (NRC) | Runs the quartile procedure correctly. Because n = 20 is even, the student splits the data into two halves of 10, finds the middle of the upper half (the 15th and 16th values) and averages them to get Q3 = 8. They also need to know that the outlier at 22 counts as a data point but does not change Q3. |

**Practices not needed:**
- **Abstracting and Generalizing:** the student applies the definition of a quartile but does not generalize anything.
- **Justifying and Proving:** the student gives no argument and just fills in a number.
- **Mathematical Modeling:** there is no real-world situation to model. The context (word values in points) is only a label.
- **Collaborative Mathematics:** this is an individual task.

**Order: Representing, then Procedural Fluency.** The main practice is Representing, because most errors come from misreading the dot plot. Procedural Fluency is the second, computational step.

### Answer 2: major practice

**Major practice: Representing**

The math itself is a routine quartile calculation. The hard part is getting from the dot plot to a correct ordered list of 20 values:
- The axis is labeled by 2's, but the dots sit on every whole number from 4 to 9. A student can easily misread which value a column of dots belongs to.
- The student has to turn the dot counts into frequencies (4, 2, 4, 3, 3, 3) and add the single point at 22 to get n = 20.
- The student also has to count that point at 22 as part of the data, even though it sits far from the others.

Once the list is right (4, 4, 4, 4, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 22), finding Q3 = 8 takes one standard step: take the median of the upper half. That step is Procedural Fluency, which plays a supporting role here.

Most mistakes on this item would come from misreading the plot, not from doing the quartile procedure wrong. That makes Representing the practice that decides whether a student gets it right.

---

## Row 207 (problem_id 100714)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
If 6 coins are flipped, find the probability that there is at least 1 heads.
____
```

### Answer 1: practices in order

**Problem:** If 6 coins are flipped, find the probability that there is at least 1 heads.

**Answer:** 1 - (1/2)^6 = 1 - 1/64 = **63/64** (about 0.984)

---

### Practices used (NAEP Mathematical Practices + NRC Procedural Fluency)

NAEP's mathematical practices are: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, and (5) Collaborating and Discussing. I've added NRC's **Procedural Fluency** as a sixth.

Here are the practices this problem needs, in the order you'd use them:

**1. Mathematical Modeling (NAEP)**
Turn the situation into a probability model. Each coin is an independent trial with P(H) = P(T) = 1/2, so the sample space is all 2^6 = 64 equally likely outcomes. Read "at least 1 heads" as the event you need to find.

**2. Abstracting and Generalizing (NAEP)**
This is the key step. Counting every case with "at least 1" (exactly 1, 2, ... 6 heads) is slow. A student who sees the structure uses the **complement** instead: the only outcome *without* a head is all tails. So P(at least 1 H) = 1 - P(no heads). This uses a general rule, P(A) = 1 - P(not A), rather than counting each case.

**3. Representing (NAEP)**
Write the idea in symbols: P(all tails) = (1/2)^6, so P(at least 1 H) = 1 - (1/2)^6. The structural idea becomes an expression you can compute. This step is light here and could be merged into step 2.

**4. Procedural Fluency (NRC)**
Do the arithmetic correctly and quickly: (1/2)^6 = 1/64, and 1 - 1/64 = 63/64. This needs exponent rules for fractions and subtracting from 1 using a common denominator.

**5. Justifying and Proving (NAEP), optional or minor**
Check that the answer makes sense. "At least one head in six flips" should be very likely, and 63/64 ≈ 98% is. You could also check by counting: 64 total outcomes - 1 all-tails outcome = 63 favorable outcomes. This step isn't needed for a fill-in-the-blank answer, but it confirms the result.

**Not needed:** Collaborating and Discussing. This is a solo, short-answer problem.

---

### Summary order

| Step | Practice | Role in this problem |
|---|---|---|
| 1 | Mathematical Modeling | Independent fair-coin model, 64 equally likely outcomes |
| 2 | Abstracting & Generalizing | Spot the complement: "at least 1" = 1 - "none" |
| 3 | Representing | Write 1 - (1/2)^6 |
| 4 | Procedural Fluency (NRC) | Compute 1/64, then 63/64 |
| 5 | Justifying & Proving (minor) | Check the answer: 63/64 is close to 1; 64 - 1 = 63 |

The main cognitive demand is **step 2**. Students who miss the complement usually either try to list every case or answer 6 × 1/2 = 3 (which is impossible) or 1/2.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

The key step in this problem is seeing that "at least 1 heads" is the **complement** of "no heads" (all tails), so P = 1 - (1/2)^6 = 63/64. To do that, a student has to stop counting cases one by one and apply a general rule, P(A) = 1 - P(not A). That shift is what Abstracting and Generalizing means.

The other practices play smaller roles:
- **Mathematical Modeling**: setting up independent fair coins with 64 outcomes is routine for this kind of problem.
- **Representing**: writing 1 - (1/2)^6 follows almost automatically once the complement is spotted.
- **Procedural Fluency (NRC)**: the arithmetic (1/64, then 63/64) is simple.
- **Justifying and Proving**: only an optional check.

What separates students who get it right from those who don't is spotting the complement. Students who miss it list every case or give wrong answers like 3 or 1/2. That is why Abstracting and Generalizing is the major practice.

---

## Row 209 (problem_id 100544)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
[Table:
A cereal box says that now it contains 20% more. Originally, it came with 18.5 ounces of cereal. How much cereal does the box come with now?
____ ounces of cereal
| [image]]
```

### Answer 1: practices in order

**Answer: 22.2 ounces** (18.5 × 1.20 = 22.2)

The NAEP Mathematics Framework (2026) lists five mathematical practices: **Representing**, **Abstracting and Generalizing**, **Justifying and Proving**, **Mathematical Modeling**, and **Collaborative Mathematics**. Below, NRC's **Procedural Fluency** is added as a sixth. These are the practices this problem uses, in order:

### 1. Mathematical Modeling: understand the real-world situation
- The student turns the context into a mathematical relationship: "20% more" means the new amount is the original amount plus 20% *of the original*.
- The key modeling decision is that the 20% is taken from 18.5 oz, the original amount, and not from the unknown new amount.
- A common mistake here is to add 20 ounces, or to read "20% more" as "20% of".

### 2. Representing: write the relationship in symbols
- The verbal relationship becomes an expression:
  - New = 18.5 + 0.20 × 18.5, or the shorter form
  - New = 18.5 × 1.20
- This step also changes one representation into another: percent to decimal (20% = 0.20, and 120% = 1.20).

### 3. Procedural Fluency (NRC): do the arithmetic
- Multiply decimals accurately: 0.20 × 18.5 = 3.7, then 18.5 + 3.7 = 22.2, or directly 18.5 × 1.2 = 22.2.
- This is the routine computation: decimal multiplication, decimal addition, and placing the decimal point correctly.

### 4. Mathematical Modeling, again: interpret and check the result
- The number is read back in context: 22.2 ounces.
- Sanity check: the answer should be a bit more than 18.5. 10% of 18.5 is 1.85, so 20% is 3.7, which makes 22.2 reasonable.

### Practices that play little or no role
- **Abstracting and Generalizing**: minor. It applies only if the student uses the general rule "increase by p% means multiply by (1 + p/100)".
- **Justifying and Proving**: not required. The answer is a single fill-in number with no explanation asked for.
- **Collaborative Mathematics**: not applicable. This is an individual item.

**Order in short:** Mathematical Modeling, then Representing, then Procedural Fluency, then Mathematical Modeling (interpret and check).

### Answer 2: major practice

**Major practice: Mathematical Modeling**

**Why this one:**
- The hard part of this item is not the arithmetic. It is reading the real-world phrase "now it contains 20% more" correctly and turning it into the right relationship: new amount = original + 20% of the original, which is 18.5 × 1.2.
- Students who miss this item usually miss it at the modeling step, not because they can't multiply. Typical wrong answers are:
  - 18.5 + 20 = 38.5 (treating the percent as ounces)
  - 0.2 × 18.5 = 3.7 (finding only the increase)
  - 18.5 ÷ 1.2 (taking the percent of the wrong base)
- Modeling also covers the last step, checking that 22.2 oz makes sense as "a bit more than 18.5 oz."

**Close second: Procedural Fluency.** Once the model is set up, the item is a short decimal calculation (18.5 × 1.2 = 22.2). That calculation is needed, but it is routine and doesn't tell strong and weak students apart much. Representing (percent to decimal, writing the expression) is so closely tied to the modeling step here that I count it as part of modeling, not as a separate main practice.

---

## Row 211 (problem_id 104881)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
Tyler wonders what proportion of students at his school would dye their hair blue if their parents would let them. He surveyed a random sample of 10 students at his school, and 2 of them said they would. Kiran didn’t think Tyler’s estimate was very accurate, so he surveyed a random sample of 100 students, and 17 of them said they would.
Based on Tyler's sample, what proportion of the students would dye their hair blue?
____
```

### Answer 1: practices in order

**Problem recap:** Tyler surveyed 10 students, and 2 said they would dye their hair blue. Based on Tyler's sample, what proportion of the students would do it?

**Answer:** 2/10 = **0.2** (or 1/5, or 20%)

---

### Practices used, in order

NAEP mathematics describes five mathematical practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, and (5) Collaborative Mathematics. This answer adds Procedural Fluency from the NRC's *Adding It Up* strands, as you asked.

This is a short, single-step item, so only a few practices really come into play:

**1. Mathematical Modeling (NAEP), the main practice**
- The student turns the real situation into a math object. The question about the whole school becomes the sample proportion (students who said yes) / (students surveyed), and that sample proportion stands in for the school's proportion.
- The student has to pick the right numbers. That means Tyler's data (2 out of 10), not Kiran's (17 out of 100). The student also has to see that the sample statistic estimates the population proportion.

**2. Representing (NAEP), supporting role**
- The student writes the count as a ratio or fraction (2/10). If the answer format calls for it, they then switch to another form, such as the decimal 0.2, the percent 20%, or the simplified fraction 1/5.

**3. Procedural Fluency (NRC)**
- The student computes 2 ÷ 10 = 0.2 correctly and quickly, or simplifies 2/10 to 1/5. This is a routine step that should come automatically.

**Not really needed for this part:**
- *Abstracting and Generalizing:* this would come up in a follow-up that asks why Kiran's larger sample gives a better estimate. That part would also use *Justifying and Proving*.
- *Collaborative Mathematics:* this is a single-student item, so it doesn't apply.

**Order:** Mathematical Modeling → Representing → Procedural Fluency

### Answer 2: major practice

**Major practice: Mathematical Modeling (NAEP)**

**Why:** The main thinking in this item is in setting the problem up. The arithmetic is easy.
- The student has to treat Tyler's random sample as a model of the whole school. That means seeing that the sample proportion (2 out of 10) is the estimate for the school's proportion.
- The student also has to pick the right data from the story. The question asks about Tyler's sample, so the student uses Tyler's numbers and ignores Kiran's 17 out of 100.

The other practices are small by comparison:
- **Representing:** writing 2/10 as 0.2 or 20% is just changing the form of the answer.
- **Procedural Fluency:** working out 2 ÷ 10 takes almost no effort.

A student who gets the setup right will almost always get the answer right. So the modeling step is what this item really tests.

**One caveat:** this item is very easy, and some people would call it mostly Procedural Fluency, since it is basically "write 2 out of 10 as a proportion." Still, if I can only pick one, I would choose Mathematical Modeling. It is the step that links the sample to the question about the whole school.

---

## Row 213 (problem_id 320443)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Un funcionario de tren analiza la ruta de un viaje y registra la distancia que recorre el tren en ciertos intervalos de tiempo.
[Table:
tiempo (horas) | distancia (millas)
0.5 | 22.5
1 | 45
1.5 | 67.5]
El tren viaja a una rapidez constante. ¿Cuál es su rapidez?
____ millas por hora
```

### Answer 1: practices in order

**Problem (translated):** A train official records how far a train travels at certain times (0.5 h → 22.5 mi, 1 h → 45 mi, 1.5 h → 67.5 mi). The train travels at a constant speed. What is its speed? **Answer: 45 miles per hour.**

**Practices available.** The 2026 NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've also included NRC Procedural Fluency.

**Practices needed, in order:**

1. **Representing (NAEP).** Read the table as a set of paired values: each row links a time in hours to a distance in miles. You have to understand that the table stands for a distance–time relationship, and that "speed" means miles per one hour. That lets you translate the table into a rate question. If you can't read the representation, you can't start.

2. **Abstracting and Generalizing (NAEP).** Notice that the ratio of distance to time is the same in every row (22.5/0.5 = 45/1 = 67.5/1.5). That constant ratio is the speed, so the pattern can be written as d = 45t. The row "1 hour → 45 miles" gives the unit rate directly, once you see that the unit rate is what's being asked for.

3. **Procedural Fluency (NRC).** Do the division accurately: 22.5 ÷ 0.5 = 45, or read the value straight off the t = 1 row. You can check another row (67.5 ÷ 1.5 = 45) to confirm. Then enter 45 with the right unit, miles per hour.

**Practices not really needed:** Justifying and Proving (no argument is asked for). Mathematical Modeling is only marginal: the problem already says the speed is constant, so no real modeling decisions are required. Collaborative Mathematics doesn't apply to a single-student item.

**Order:** Representing → Abstracting and Generalizing → Procedural Fluency.

### Answer 2: major practice

**My pick for the major practice: Representing (NAEP).**

**Why:** The hard part of this item is reading the table correctly. You have to see that it shows a distance–time relationship and that "speed in miles per hour" means the distance covered in one hour. Once you see that, the answer is right there in the table: the 1-hour row says 45 miles. You don't even need to calculate.

**Why not the others:**
- **Abstracting and Generalizing** matters less here. The problem already tells you the speed is constant, so you don't have to discover the constant ratio yourself.
- **Procedural Fluency** is small. At most you do one easy division (22.5 ÷ 0.5), and you can skip even that by using the 1-hour row.

So most of the thinking is turning the table into "miles per one hour," which is Representing.

---

## Row 214 (problem_id 318309)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
The population of city B was approximately 7,150,000, and it increased by 0.8% in one year. What was the new population?
Approximately ____ people
```

### Answer 1: practices in order

**Practice set used:** the five mathematical practices in the 2026 NAEP Mathematics Framework (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus **Procedural Fluency** from the NRC's *Adding It Up* strands.

**Problem:** City B had about 7,150,000 people, and the population grew by 0.8% in one year. What is the new population?

---

### Practices needed, in order

**1. Mathematical Modeling (light use): set up the situation**
- Read the context and see that this is a percent-increase situation. The new population is the old population plus 0.8% of it.
- Choose the model: new = original × (1 + rate).
- This is a routine, already-structured model. You don't have to make assumptions or refine anything, so this practice is only lightly used.

**2. Representing: change the forms of the quantities**
- Rewrite the percent as a decimal: 0.8% = 0.008. A common mistake is writing 0.08.
- Write the increase as a single multiplier: 1 + 0.008 = 1.008.
- Write the expression: 7,150,000 × 1.008, or 7,150,000 + 0.008 × 7,150,000.
- This is the key step. Most errors come from turning 0.8% into the wrong decimal.

**3. Procedural Fluency (NRC): do the calculation accurately**
- 0.008 × 7,150,000 = 57,200
- 7,150,000 + 57,200 = **7,207,200**
- This takes accurate decimal multiplication and handling of large numbers, including place value with the 0.008 factor.

**4. Justifying (light check): is the answer reasonable?**
- 1% of 7,150,000 is 71,500, so 0.8% should be a little less, and 57,200 is.
- The new population should be only slightly larger than the old one, and it is.
- This is an informal check, not a formal proof. It's optional, but it catches the 0.08 mistake, which would give 7,722,000.

---

### Practices not needed
- **Abstracting and Generalizing:** no pattern or general rule has to be found. It's a single calculation.
- **Collaborative Mathematics:** the item is solved alone.

---

### Summary order
**Mathematical Modeling (light) → Representing → Procedural Fluency → Justifying (light check)**

The main practices are **Representing** (0.8% → 0.008 → ×1.008) and **Procedural Fluency** (the calculation).

**Answer:** Approximately **7,207,200** people

### Answer 2: major practice

**Major practice: Representing**

**Why Representing:**
- This problem is mainly decided by one step: turning "increased by 0.8%" into the right form, either 0.008 or the growth multiplier 1.008.
- Converting a percent below 1% into a decimal is where students most often go wrong. Writing 0.08 instead of 0.008 gives 7,722,000. Using 0.8 directly gives a huge number.
- Once the quantity is in the right form, the rest is routine.

**Why not Procedural Fluency:**
- The calculation (7,150,000 × 0.008 = 57,200, then add it to get 7,207,200) is easy. It's a standard decimal multiplication and an addition.
- It's needed to get the answer, but it isn't what makes the item hard or what tells strong students apart from weak ones.

**Close second:** Procedural Fluency. You could argue for it if you see percent increase as a memorized routine for this grade level. Even then, the step that decides success is choosing the correct decimal form, and that is Representing.

**Answer:** Approximately **7,207,200** people

---

## Row 216 (problem_id 320538)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
Noah y Andre están a 15 millas de distancia por un camino y comienzan a andar en bicicleta el uno hacia el otro. Noah pedalea a una rapidez constante de 4 millas por hora y Andre a una rapidez constante de 2 millas por hora. ¿Cuánto tiempo tardan en encontrarse?
____ horas
```

### Answer 1: practices in order

**Problem (translated):** Noah and Andre start 15 miles apart on a road and ride their bikes toward each other. Noah rides at a constant 4 mph and Andre at a constant 2 mph. How long until they meet? (____ hours)

**Answer: 2.5 hours**

### Practices available
The NAEP Mathematics Framework (2026) lists these mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC (*Adding It Up*): **Procedural Fluency**

### Practices in the order you use them

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** | Turns the story into a math setup. Both riders move toward each other, so the 15-mile gap shrinks at the sum of their speeds: 4 + 2 = 6 miles per hour. The key modeling choice is to add the speeds and treat it as a single closing rate. |
| 2 | **Representing** | Writes the model in symbols, for example 4t + 2t = 15 (the two distances add up to the full gap), or draws a line segment with both riders moving toward the middle. |
| 3 | **Procedural Fluency** | Solves it: 6t = 15, so t = 15 / 6 = 2.5 hours. |
| 4 | **Mathematical Modeling** (interpret / check) | Checks that the answer makes sense in the story: in 2.5 h Noah rides 10 mi and Andre rides 5 mi, and 10 + 5 = 15. Then gives the answer in the unit asked for (hours). |

**Order: Mathematical Modeling → Representing → Procedural Fluency → (Mathematical Modeling: interpret and check)**

### Practices you don't need
- **Abstracting and Generalizing**: at most a small part. Seeing that "objects moving toward each other close the gap at the sum of their speeds" is a general rule, but the problem never asks you to state or extend it.
- **Justifying and Proving**: not needed. The answer is a fill-in number, and no argument is asked for.
- **Collaborative Mathematics**: not needed. This is a task you do on your own.

**Main practices:** Mathematical Modeling (most important, because the hard part is setting up the combined rate), then Representing, then Procedural Fluency (the arithmetic is easy).

### Answer 2: major practice

**Major practice: Mathematical Modeling**

Why this one:
- **The hard part is the setup.** The student has to see that two riders moving toward each other close the 15-mile gap at the sum of their speeds (4 + 2 = 6 mph). That is turning a real situation into a math model. Students who get this wrong usually make a modeling mistake, such as using only one rider's speed or subtracting the speeds, not an arithmetic mistake.
- **Procedural Fluency is easy here.** Once the model is set up, 15 / 6 = 2.5 is a simple division.
- **Representing is a short step in between.** Writing 4t + 2t = 15 just records the model you already built. It doesn't add much difficulty of its own.
- **The other practices don't apply much.** Nobody asks for a justification, a generalization, or group work.

So, if you have to pick one, the practice that best describes this problem is **Mathematical Modeling**.

---

## Row 219 (problem_id 110017)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
After how many months will the bamboo plant be 66 inches tall? ____ months
```

### Answer 1: practices in order

**Note:** The problem text ("After how many months will the bamboo plant be 66 inches tall?") leaves out the data it depends on. That is probably a table or graph of the bamboo's height by month, or a starting height and growth rate. So I can't give a numeric answer, but the practices and their order are clear from the type of task.

**Practices used** (from the NAEP 2026 Mathematics Framework, plus NRC procedural fluency):

| Order | Practice | What the student does in this problem |
|---|---|---|
| 1 | **Representing** (NAEP) | Reads the table or graph of the bamboo's height and pulls out the given values: the starting height and the height at each month. |
| 2 | **Abstracting and Generalizing** (NAEP) | Spots the pattern in the data: the plant grows by a constant amount each month. Turns that into a general rule, height = start + (growth per month) x months. |
| 3 | **Mathematical Modeling** (NAEP) | Uses the rule as a model for the real situation and sets up the question as an equation: start + rate x m = 66. Alternatively, extends the table or line until the height reaches 66. |
| 4 | **Procedural Fluency** (NRC) | Does the arithmetic correctly and efficiently: subtracts the starting height from 66, divides by the monthly growth, or counts on by the growth amount, to get m. |
| 5 | **Justifying and Proving** (NAEP), light use | Checks the answer by putting m back into the rule, or checking it against the table, to confirm the height is exactly 66 inches. Also confirms the answer is in months. |

**Not used:** Collaborative Mathematical Discourse. This is a single-answer, individual item.

**Order:** Representing → Abstracting and Generalizing → Mathematical Modeling → Procedural Fluency → Justifying and Proving (optional check)

The core of the problem is steps 1–4. The key step is finding the constant monthly growth (Abstracting and Generalizing). Procedural fluency is needed to compute the number of months from that rate.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

The problem asks about a height, 66 inches, that is not in the given data. The student can't just read the answer off the table or graph. They have to spot the regular growth pattern, an equal increase each month, and turn it into a rule. Then they extend that rule beyond the data to find when the plant reaches 66 inches. Turning a few data points into a rule you can extend is the core of Abstracting and Generalizing.

The other practices play supporting roles:
- **Representing** only gets the data off the table or graph.
- **Mathematical Modeling** is light here. The context is already a clean linear pattern, so there is little real modeling to do.
- **Procedural Fluency** is just one subtraction and one division (or counting on) once the rule is known.

A student who finds the monthly growth rate and extends it will get the answer. A student who can't see the pattern can't get started, no matter how fluent their arithmetic is.

---

## Row 225 (problem_id 114889)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Teachers held a basketball shooting contest. Their goal was to make 60 baskets. For the teacher, determine what percentage of the goal they achieved.
Teacher C made 66 baskets.
____ %
```

### Answer 1: practices in order

**Problem:** The goal is 60 baskets. Teacher C made 66. What percentage of the goal did Teacher C reach?

**Answer:** 66 / 60 = 1.1, which is **110%**

---

## Practices used, in order

The NAEP mathematical practices (from the NAEP Mathematics Framework) are:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Modeling
5. Using Computational Strategies
6. Communicating

The NRC strand **Procedural Fluency** (from *Adding It Up*) is added to that list.

Here is the order in which they come up for this problem:

### 1. Representing (NAEP)
Turn the words into a math relationship: "percent of the goal achieved" = (baskets made / goal) x 100. That gives the ratio 66/60, or the equation 66 = p% x 60. This is the main step that sets up the problem. The usual trap is to flip the ratio and write 60/66.

### 2. Using Computational Strategies (NAEP)
Pick a fast way to get the answer. Some options:
- Simplify 66/60 to 11/10 and see that this is 1.1.
- Reason with benchmarks: 60 is 100% of the goal, 6 is 10% of it, so 66 = 100% + 10% = 110%.
- Use the ratio table 60 : 100 = 66 : x.

### 3. Procedural Fluency (NRC)
Carry out the steps correctly and quickly: divide 66 by 60 to get 1.1, then multiply by 100 to get 110. Change the decimal to a percent without dropping or misplacing the decimal point.

### 4. Justifying (NAEP: Justifying and Proving), light use
Check that the answer makes sense. Teacher C made more baskets than the goal, so the percent has to be above 100%. If you get 90.9%, you inverted the ratio. This step is mostly a quick check.

### 5. Communicating (NAEP), minimal
Write the answer in the format the question asks for, which is a number in the "____ %" blank: **110**.

---

**Not really used:** Abstracting and Generalizing, and Modeling. The problem is a direct one-step percent calculation, so neither practice plays a real role beyond what Representing already covers.

**Summary order:** Representing -> Using Computational Strategies -> Procedural Fluency -> (Justifying) -> (Communicating)

The most important practices here are **Representing** (setting up 66/60 the right way round) and **Procedural Fluency** (doing the arithmetic and converting to a percent).

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The hard part of this problem is not the arithmetic. It is setting up the right relationship: percent of goal = made / goal = 66/60. Once that is written correctly, the calculation (66 / 60 = 1.1, so 110%) is a short routine step.

This problem also has a twist that tests Representing in particular. Teacher C went **over** the goal, so the answer is above 100%. Students who represent the situation wrong usually make one of two mistakes:
- They flip the ratio to 60/66 and get about 90.9%.
- They assume a percent can't go above 100, so they write 100% or compute the 6 extra baskets as 10%.

Both mistakes come from representing the problem wrong, not from weak procedures.

Procedural Fluency would come second. If you are coding a single label for this problem, use **Representing**.

---

## Row 227 (problem_id 115187)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
What is the height of the 500 ml mark? Recall that 1 liter (L) is equal to 1000 milliliters (ml), and that 1 liter (L) is equal to 1,000 cm^3.
____ cm
```

### Answer 1: practices in order

**Practices available.** The NAEP 2026 Mathematics Framework lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added the NRC's **Procedural Fluency** as a sixth.

**Note on the problem.** The text mentions a "500 ml mark" but doesn't include the container or its dimensions. The item probably came with a figure, such as a measuring container with a known base (for example a rectangular prism or cylinder). So I can't give a final number, but I can lay out how it would be solved: 500 ml = 500 cm³, and height = 500 cm³ ÷ (base area in cm²).

---

### Practices used, in order

**1. Representing**
- Read the figure: work out the container's shape and pull out its base dimensions in cm. If it has other marks (such as 1 L), note where they sit.
- Translate the units given in words into symbols: 1 L = 1000 ml = 1000 cm³, so 1 ml = 1 cm³.
- This comes first because nothing can be set up until the student has turned the picture and the unit facts into usable numbers.

**2. Mathematical Modeling**
- Model the liquid up to the 500 ml mark as a solid with the container's base and an unknown height *h*: Volume = (base area) × *h*.
- Plug in the converted volume: 500 cm³ = (base area) × *h*, so *h* = 500 ÷ (base area).
- Another way to see it: if the 1 L mark is at height *H*, the 500 ml mark is at *H*/2, since height is proportional to volume when the cross-section is constant.
- This is the main step of the problem. It turns a real situation (a measuring container) into an equation.

**3. Procedural Fluency (NRC)**
- Do the arithmetic correctly: work out the base area (l × w, or πr² for a cylinder), then divide 500 by it. Round or simplify as needed and give the answer in cm.

**4. Justifying and Proving (light, optional)**
- Check that the answer makes sense: the units should come out as cm³ ÷ cm² = cm. The 500 ml height should be half the 1 L height, and it must fit inside the container.
- This is a check on the answer, not something the problem requires, so it is a minor last step.

**Not used:** Abstracting and Generalizing (the problem doesn't ask for a general rule) and Collaborative Mathematics (it is a single-student item).

---

### Summary order
**Representing → Mathematical Modeling → Procedural Fluency → (Justifying and Proving as an optional check)**

The most important practice here is **Mathematical Modeling**: the volume = base area × height relationship combined with the ml-to-cm³ conversion. Procedural Fluency is needed to get the number right.

### Answer 2: major practice

**Major practice: Mathematical Modeling**

This is the step where the problem actually gets solved. The student has to treat the liquid up to the 500 ml mark as a solid with the container's base, then use Volume = base area × height. They also have to use the given unit facts to turn 500 ml into 500 cm³, which gives h = 500 ÷ (base area).

The other practices play supporting roles. Representing comes before modeling: it reads the dimensions off the figure. Procedural Fluency comes after: it does the division. A student who reads the figure correctly and divides accurately will still fail without the volume model and the ml-to-cm³ link. But once that model is set up, the arithmetic is simple.

---

## Row 228 (problem_id 117898)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Order the following pairs of coordinates from closest to farthest apart. Be prepared to explain your reasoning.

Items to put in order:
- 6) and (5
- (1
- 6)
- -9)
- 0) and (7
- 4) and (2
- (7
- -12) and (-12
- 10)
- (-12
- -1)
- -10) and (-4
- (2
- (-3
- -10)
```

### Answer 1: practices in order

**A note on the problem text:** the item list looks like it was split at every comma, so each pair of points is broken into pieces. Putting the pieces back together gives five pairs. In each pair the two points share an x-coordinate or a y-coordinate, so each pair lies on a horizontal or vertical line. One reconstruction that fits the pieces:

- (1, 6) and (5, 6): distance 4
- (7, 0) and (7, -9): distance 9
- (2, 4) and (2, 10): distance 6
- (-12, -12) and (-12, -1): distance 11
- (-3, -10) and (-4, -10): distance 1

The pieces don't fix every pairing. For example, (1 and (-3 could swap. The practices needed are the same either way.

## Practices, in the order you'd use them

The NAEP mathematical practices are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. I've added Procedural Fluency from the NRC strands.

### 1. Representing (NAEP)
First, read each ordered pair as a location on the coordinate plane. You can sketch the points or picture them. The key thing to see is that the two points in each pair sit on the same horizontal line (same y) or the same vertical line (same x). That tells you which coordinate to compare.

### 2. Abstracting and Generalizing (NAEP)
Next, turn that picture into a general rule:
- If the points share a coordinate, the distance is the difference of the other coordinates.
- If both of those coordinates are on the same side of zero, subtract their absolute values. Example: |-12| - |-1| = 11.
- If they are on opposite sides of zero, add their absolute values. Example: |0| + |-9| = 9.

With this rule you can use one method for all five pairs instead of counting squares each time.

### 3. Procedural Fluency (NRC)
Then apply the rule quickly and correctly to each pair. Compute the distances (1, 4, 6, 9, 11 in the reconstruction above) and sort them. The order from closest to farthest is:

(-3, -10)&(-4, -10) → (1, 6)&(5, 6) → (2, 4)&(2, 10) → (7, 0)&(7, -9) → (-12, -12)&(-12, -1)

### 4. Justifying and Proving (NAEP)
The problem says "Be prepared to explain your reasoning." So the last step is to justify the order. Explain why only one coordinate matters when the points line up horizontally or vertically. Explain why opposite signs mean you add the absolute values. Then check each distance against the rule or by counting on a sketch.

### Optional: Collaborative Mathematical Discourse (NAEP)
If students share their explanations with each other, this practice comes in at the end, after step 4. The problem doesn't require it, though.

**Practices in order:** Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving. Mathematical Modeling isn't used, because there is no real-world situation to model.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

Why this one:

- **It's the hardest step.** Seeing the points is easy, and once you have a rule the arithmetic is easy. The work that takes thought is building the rule. The rule says that when two points share an x or a y coordinate, only the other coordinate matters. If those values have the same sign, you subtract their absolute values. If they have opposite signs, you add them. Students usually go wrong at this step: for example, they compute |0 - (-9)| as 0 - 9, or they subtract when the signs are opposite.
- **The other practices depend on it.** Procedural Fluency is just applying the rule to each pair. The explanation the problem asks for ("be prepared to explain your reasoning") is mostly stating the rule and saying why it works.
- **The problem is built to test it.** The five pairs mix horizontal and vertical lines, same-sign and opposite-sign coordinates, and one pair that includes zero. That mix pushes students toward one general method instead of counting squares for each pair.

**Runner-up: Procedural Fluency (NRC).** If you treat the problem as a routine grade-6 exercise in which students already know the rule, the main work becomes computing and ordering five distances accurately. Procedural Fluency would then be the main practice.

---

## Row 233 (problem_id 119945)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
At a school, 460 of the students walk to school.
The number of students who ride the school bus is 110% of the number of students who walk. How many students ride the school bus?
____ students
```

### Answer 1: practices in order

**Answer: 506 students**

## Practices available

The NAEP Mathematics Framework (2026) lists five mathematical practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematical Discourse

Added as you asked: **Procedural Fluency** (NRC, *Adding It Up*). This means carrying out procedures flexibly, accurately and efficiently.

## Practices needed, in order

**Step 1: Representing (main practice)**
Turn the words into math. "110% of the number who walk" becomes a percent-of-a-quantity expression:
- Bus riders = 110% × 460
- 110% = 1.10 (or 110/100)
- So: Bus riders = 1.10 × 460

This is where the problem's real thinking happens. You have to see that "110% of" means multiply, and that a percent above 100 gives a result bigger than the starting number.

**Step 2: Procedural Fluency (main practice)**
Do the calculation correctly:
- 1.10 × 460 = 460 + 0.10 × 460 = 460 + 46 = **506**
- (Or: 460 × 110 ÷ 100 = 50,600 ÷ 100 = 506)

**Step 3: Justifying (light use, optional)**
Check that the answer makes sense. 110% is more than 100%, so more students ride the bus than walk. 506 > 460, and the difference of 46 is exactly 10% of 460. This is a quick reasonableness check, not a formal proof, so it plays a minor role.

## Practices not needed
- **Abstracting and Generalizing:** You don't need a general rule or pattern. It's one calculation.
- **Mathematical Modeling:** The setting is already simplified. There's nothing to assume, idealize or interpret beyond direct translation, so Representing covers it.
- **Collaborative Mathematical Discourse:** This is a single-response item with no communication or argument with others.

## Summary
**Representing → Procedural Fluency → (Justifying, as a check)**

The two main practices are Representing and Procedural Fluency. Representing is probably where students struggle most, for example by computing 10% of 460 = 46 and reporting 46, or by not knowing how to handle a percent over 100.

### Answer 2: major practice

**Major practice: Representing**

Why it ranks above Procedural Fluency:

- **It decides the problem.** Once a student writes "bus riders = 1.10 × 460", the arithmetic (460 + 46 = 506) is easy for the grade level. A student who gets the representation right will almost certainly get the right answer.
- **It's where students go wrong.** The typical errors come from misreading the setup, not from arithmetic:
  - reporting only 10% of 460 (46)
  - computing 460 − 46 = 414, as if the percent meant a decrease
  - not knowing what to do with a percent above 100
- **It's what the item tests.** The problem checks whether students understand that "110% of a quantity" means multiplying by 1.10, which gives more than the original. Calculating 1.1 × 460 is just the routine last step.

Procedural Fluency is still needed, but in a supporting role. So the major practice is **Representing**.

---

## Row 234 (problem_id 121533)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
It takes an ant farm 3 days to consume 1/2 of an apple. At that rate, in how many days will the ant farm consume 3 apples?
____ days
```

### Answer 1: practices in order

**Problem:** An ant farm takes 3 days to eat 1/2 of an apple. At that rate, how many days will it take to eat 3 apples?

**Answer: 18 days**

---

### NAEP Mathematical Practices (plus NRC Procedural Fluency)

NAEP's mathematics framework lists these practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematical Discourse

You asked me to add a sixth:
6. **Procedural Fluency** (NRC, *Adding It Up*): carrying out procedures flexibly, accurately, and efficiently.

---

### Practices needed, in order

**1. Representing**
Turn the words into a rate or proportion you can work with:
- 3 days ↔ 1/2 apple, so you need *x* days ↔ 3 apples
- Written as a proportion: 3 / (1/2) = x / 3, or as a unit rate in days per apple

This is the key step. The rate has a fraction in it ("1/2 apple"), so the student has to set up the relationship carefully. A common mistake is flipping the ratio, for example using apples per day in one place and days per apple in another.

**2. Mathematical Modeling** (light use)
"At that rate" tells you to assume the ants eat at a constant speed. That makes it a direct proportion: total days = (days per apple) × (number of apples). The student is choosing a proportional model for a real situation, but the situation is simple and the model is basically handed to them, so this practice plays a small role.

**3. Procedural Fluency (NRC)**
Do the arithmetic:
- Unit rate: 3 ÷ (1/2) = 6 days per apple
- Scale up: 6 × 3 = **18 days**
(Or: 3 apples is 6 halves, and 6 × 3 days = 18 days.)

The student needs to divide by a fraction correctly (3 ÷ 1/2 = 6, not 1.5) and then multiply. This is where most computational errors would happen.

**4. Justifying (light use, optional)**
Check that the answer makes sense. Half an apple takes 3 days, so a whole apple takes 6 days, and 3 apples take 18 days. The answer is larger than 3 days, as it should be. The item only asks for a number, so this is just a self-check and isn't required.

---

### Summary

| Order | Practice | Role |
|---|---|---|
| 1 | Representing | Main: turn the rate with a fraction into a proportion or unit rate |
| 2 | Mathematical Modeling | Minor: "at that rate" means assume a constant, proportional rate |
| 3 | Procedural Fluency (NRC) | Main: 3 ÷ 1/2 = 6, then 6 × 3 = 18 |
| 4 | Justifying | Optional check that the answer is reasonable |

**Not needed:** Abstracting and Generalizing (the student doesn't have to generalize beyond this one case) and Collaborative Mathematical Discourse (it's an individual item with a single answer).

**Most important practices:** Representing and Procedural Fluency.

### Answer 2: major practice

**Major practice: Representing**

Why I'd pick it:

- **The hard part of this problem is the setup, not the arithmetic.** The student has to read "3 days for 1/2 apple" and turn it into a usable relationship, such as 6 days per apple or the proportion 3 / (1/2) = x / 3. A student who sets this up correctly will very likely get 18.
- **The most common mistakes are representation mistakes.** Students flip the ratio (apples per day vs. days per apple), treat the 1/2 as if it were 1 apple (and answer 9), or halve instead of double (and answer 1.5 days per apple, then 4.5). All of these come from setting up the rate wrong, not from bad computation.
- **Procedural Fluency comes second.** The calculations (3 ÷ 1/2 = 6, then 6 × 3 = 18) are short and routine once the setup is right. Some students do skip the fraction division entirely by reasoning "3 apples = 6 halves, so 6 × 3 = 18." That shortcut is itself a representation move, so the arithmetic depends on the setup even more.

If I ranked them: **Representing** (major) > Procedural Fluency (secondary) > Mathematical Modeling (minor) > Justifying (optional check).

---

## Row 235 (problem_id 122745)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Figures R, S, and T are all scaled copies of one another. Figure S is a scaled copy of R using a scale factor of 3. Figure T is a scaled copy of S using a scale factor of 2.
Find the scale factor from T to S.
____
```

### Answer 1: practices in order

## Practices for this problem

**Problem:** Figure S is R scaled by 3, and figure T is S scaled by 2. Find the scale factor from T to S.

**Answer:** 1/2

---

### Practices (NAEP Mathematical Practices, plus NRC Procedural Fluency)

The NAEP Mathematics Framework lists five practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, and (5) Collaborative Mathematics. From the NRC strands I added **Procedural Fluency**.

### Order used to solve the problem

**1. Representing**
Turn the words into a chain of relationships: R → S (×3), S → T (×2). The question asks about the reverse direction, T → S. Drawing it as arrows, or writing S = 3R and T = 2S, shows that the step you need is the inverse of the S → T step.

**2. Abstracting and Generalizing**
Use the general rule for scale factors. If going from A to B multiplies by k, then going from B back to A multiplies by 1/k. The fact that S is R scaled by 3 is a distractor here, because the question only involves S and T. The point is to see the structure (inverse direction means reciprocal) and not just multiply every number in the problem.

**3. Procedural Fluency (NRC)**
Do the arithmetic: the reciprocal of 2 is **1/2**. As a check, T = 2S, so S = (1/2)T.

**4. Justifying and Proving (light use)**
Check that the answer makes sense. T is bigger than S, so shrinking T back to S needs a scale factor below 1. So 1/2 is reasonable, and answers like 2, 6, or 1/6 are not.

### Practices not used
- **Mathematical Modeling**: there is no real-world situation to model.
- **Collaborative Mathematics**: this is a single-student item.

### Summary order
**Representing → Abstracting and Generalizing → Procedural Fluency → Justifying (check)**

The main challenge is in Representing and Abstracting. Students need to see the reverse direction and ignore the factor of 3. The calculation itself is trivial.

### Answer 2: major practice

## Major practice: Abstracting and Generalizing

If I had to pick one, it would be **Abstracting and Generalizing**.

**Why:**
- The key step is applying the general rule that reversing a scaling uses the reciprocal factor. If A → B is ×k, then B → A is ×1/k. The student also has to see that the R → S factor of 3 has nothing to do with the question. Both of these come from understanding the structure of scale-factor relationships, not from calculating.
- The usual wrong answers (2, 6, 1/6) come from failing here: forgetting about direction, or multiplying every number in the problem. Getting this practice right is what separates correct answers from wrong ones.
- **Representing** matters, but setting up the chain R → S → T is simple once you read the problem. **Procedural Fluency** is trivial here, since the reciprocal of 2 is 1/2. **Justifying** only works as a final check.

So the difficulty and the learning value of this item both sit in Abstracting and Generalizing. Representing would be a close second.

---

## Row 236 (problem_id 123335)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Find the scale factor from R to T.
____
```

### Answer 1: practices in order

**Problem:** "Find the scale factor from R to T." The problem refers to a figure showing two similar shapes, R (the original) and T (the scaled copy). The figure isn't included in the text, so I can't give the numeric answer. The practices and their order are the same whatever the dimensions are.

**Practices used: NAEP mathematical practices, plus Procedural Fluency from the NRC**

The NAEP framework lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Discourse. This problem draws on some of them, and the NRC's Procedural Fluency is added as you asked.

**Order of practices:**

1. **Representing (NAEP).** Read the figure. Pick out the matching (corresponding) sides of R and T, using the grid or the labeled lengths. Then turn that visual information into numbers, for example "side of R = 4, matching side of T = 6." This is the first step because nothing else can happen until the picture becomes numbers.

2. **Abstracting and Generalizing (NAEP).** See that "scale factor from R to T" means the multiplier that maps R onto T. Express it as the general relationship *scale factor = length in T ÷ matching length in R*. The direction matters: going from R to T puts T on top. The key idea is that one constant multiplier applies to every pair of matching sides.

3. **Procedural Fluency (NRC).** Do the calculation. Divide the length in T by the matching length in R and simplify the fraction or decimal, for example 6/4 = 3/2 = 1.5.

4. **Justifying and Proving (NAEP), light use.** Check the answer by testing a second pair of matching sides to make sure it gives the same ratio. Also check that the result makes sense: if T is larger than R the factor should be greater than 1, and if T is smaller it should be between 0 and 1. This confirms the figures really are scaled copies and that the division wasn't done backwards (R ÷ T).

**Not used:** Mathematical Modeling, because there is no real-world situation to model, and Collaborative Discourse, because this is an individual item.

**Summary of order:** Representing → Abstracting and Generalizing → Procedural Fluency (NRC) → Justifying and Proving (check)

The main practices are Representing and Procedural Fluency. The most common mistake is getting the direction wrong (dividing R by T), and that's where Abstracting and Generalizing matters.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The hard part of this problem is reading the figure correctly. The student has to work out which sides of R and T match and get their lengths from the picture, usually by counting grid units or reading labels. They also have to keep the direction "from R to T" straight, so that T's length goes on top. Once the right numbers are on the page, the division is a single step. That's why Procedural Fluency comes second here and isn't the main practice.

Most mistakes on this item come from the representation step: pairing sides that don't match, miscounting grid units, or flipping the ratio. They rarely come from the arithmetic. So Representing is the practice the item mainly tests.

---

## Row 237 (problem_id 123444)

- **predicted_practice:** Representing
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Find the scale factor from T to R.
____
```

### Answer 1: practices in order

**Problem:** "Find the scale factor from T to R." (The figure showing shapes T and R isn't in the text I have, so I'm describing the solution process, not giving a number.)

**Practices available:** the five practices in the NAEP 2026 Mathematics Framework (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus **Procedural Fluency** from the NRC strands of proficiency.

### Practices needed, in order

1. **Representing (NAEP)**
   - Read the figure: find shapes T and R, the side lengths (or grid units) shown, and which sides of T match which sides of R.
   - Turn the picture into numbers you can use, for example "side of T = a, matching side of R = b".

2. **Abstracting and Generalizing (NAEP)**
   - Recognize the general idea: a scale factor is the same ratio for every pair of matching lengths in similar figures.
   - Get the direction right. "From T to R" means T is the original and R is the image, so scale factor = (length in R) / (length in T), not the other way round.

3. **Procedural Fluency (NRC)**
   - Do the calculation correctly: divide the R length by the T length and simplify the fraction or decimal (for example 6/4 = 3/2 = 1.5).
   - Optionally check with a second pair of matching sides to make sure you get the same ratio.

### Practices not needed
- **Justifying and Proving:** the problem only asks for a value. You don't have to prove the shapes are similar.
- **Mathematical Modeling:** there is no real-world situation to turn into math.
- **Collaborative Mathematics:** this is a task done alone.

**Order:** Representing → Abstracting and Generalizing → Procedural Fluency

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

This is the step that decides whether the answer is right:

- **It is the key idea.** The student has to know that a scale factor is the single ratio that every pair of matching lengths shares in similar figures.
- **It is where students usually go wrong.** "From T to R" means the answer is (R length) / (T length). Students most often flip this ratio, for example answering 2/3 when the answer is 3/2. Getting the direction right depends on understanding the general rule.
- **The other two steps support it.**
  - Representing only means reading matching side lengths off the figure.
  - Procedural Fluency is usually one simple division.
  - A student can do both of these perfectly and still give the wrong answer without the right idea of what a scale factor is.

If the figure turned out to be complicated (for example, shapes rotated or reflected so matching sides are hard to spot), Representing would be a close second.

---

## Row 238 (problem_id 123500)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the constant of proportionality?
____ wheels per bus
```

### Answer 1: practices in order

**A note on the problem first.** The text asks for "the constant of proportionality" in "wheels per bus", but the table, graph or equation that relates buses to wheels isn't included. So I can't give a definite number. Below is the order of practices that solves it, and how the numbers would work once you have the data.

**Practices used (the NAEP 2026 mathematical practices, plus procedural fluency from the NRC)**

The NAEP Mathematics Framework names five mathematical practices:
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Problem Solving

This problem uses three of them, plus procedural fluency, in this order.

**1. Representing (primary)**
- Read the given representation: a table, graph or set of number pairs for buses (x) and wheels (y).
- Pick out which quantity is the input (buses) and which is the output (wheels).
- Read off one or more matching pairs. For example, a point such as (2, 12) or a table row "3 buses, 18 wheels".
- The answer frame "____ wheels per bus" also tells you the rate must be wheels ÷ buses, not buses ÷ wheels.

**2. Abstracting and Generalizing**
- See that the relationship is proportional: wheels = k × buses, with the same ratio y/x in every pair.
- Treat the constant of proportionality k as the unit rate: the number of wheels for 1 bus.

**3. Procedural fluency (NRC strand)**
- Do the division accurately: k = wheels ÷ buses. For example, 12 ÷ 2 = 6, or 18 ÷ 3 = 6.
- If the table already has a row for 1 bus, just read the value there.

**4. Justifying and Proving (minor check, optional)**
- Check that the same k works for a second pair, such as 6 × 5 = 30. This confirms the relationship really is proportional and that you didn't flip the ratio.

Mathematical Modeling and Collaborative Problem Solving aren't needed here. There's no real-world model to build and no group work involved.

**Order:** Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving as a quick check)

**Answer:** k = (number of wheels) ÷ (number of buses), using any pair from the given data. With typical values like 2 buses and 12 wheels, k = **6 wheels per bus**. Please check this against the actual table or graph in the problem.

### Answer 2: major practice

**Major practice: Representing**

Why:
- The real difficulty in this problem is reading the given data correctly. The student has to take the table, graph or number pairs for buses and wheels and work out what they say.
- That means knowing which variable is buses and which is wheels, and pulling out matching pairs.
- It also means reading the "____ wheels per bus" frame as wheels ÷ buses, not the other way round.
- Once the student has read the representation correctly, the rest is small:
  - Seeing the constant ratio (Abstracting and Generalizing) is a light step.
  - The division, such as 12 ÷ 2 = 6 (procedural fluency), is a one-step calculation.
- Most likely errors are representation errors: flipping the ratio, misreading a point on the graph, or picking a non-matching pair. Arithmetic errors are less likely.

So if I could tag only one practice, it would be **Representing**. Procedural fluency and Abstracting and Generalizing are secondary.

---

## Row 240 (problem_id 124041)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
You spin the spinner 80 times. About how many times do you expect it will land on something other than A?
____ times
```

### Answer 1: practices in order

The NAEP Mathematics Framework names five mathematical practices: (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, and (5) Collaborative Mathematics. You asked me to add (6) Procedural Fluency from the NRC's *Adding It Up* strands.

**The problem:** "You spin the spinner 80 times. About how many times do you expect it will land on something other than A?"

Note: the spinner picture isn't in the text, so I can't give the final number. The practice sequence doesn't depend on the exact sections, though. For example, if A covers 1/4 of the spinner, the answer is 80 × 3/4 = 60.

### Practices needed, in order

**1. Representing (read and interpret the spinner diagram)**
- The student has to turn the picture into numbers: how many sections there are, whether they are the same size, and how much of the spinner A takes up.
- Then they write this as a probability: P(A) = (A's share of the spinner) / (whole spinner).
- This comes first because nothing else can happen until the visual is read correctly.

**2. Abstracting and Generalizing (complement idea and the expected-value rule)**
- The question asks about "something other than A", so the student needs the complement rule: P(not A) = 1 − P(A). This is often where students slip, because they compute for A instead.
- They also need the general rule linking probability to long-run frequency: expected count = number of trials × probability.

**3. Mathematical Modeling (apply the probability model to the 80 spins)**
- The student treats the 80 real spins as repeated independent trials with a fixed theoretical probability, so expected outcome = 80 × P(not A).
- The word "About" in the question signals a model-based prediction, not a promise of what will actually happen. Seeing that difference is part of modeling.

**4. Procedural Fluency (NRC) (do the arithmetic)**
- Subtract to get the complement fraction, e.g. 1 − 1/4 = 3/4.
- Multiply a whole number by a fraction, e.g. 80 × 3/4 = 60, or find 80 ÷ 4 = 20 and then 80 − 20 = 60.
- This needs to be quick and accurate. It is the last computational step.

**5. Justifying and Proving (optional, light sense-check)**
- A quick reasonableness check: the answer must be between 0 and 80. If A is smaller than half the spinner, the answer should be more than 40.
- This isn't formally required for a fill-in-the-blank item, but it's a useful step.

**Not used:** Collaborative Mathematics, since this is an individual item.

### Summary order
**Representing → Abstracting and Generalizing → Mathematical Modeling → Procedural Fluency → (Justifying, optional check)**

The most important practices are **Representing**, **Mathematical Modeling** and **Procedural Fluency**. **Abstracting and Generalizing** is a key secondary practice because of the complement ("other than A"). Students who skip that step and answer for A itself will get the most common wrong answer.

### Answer 2: major practice

If I had to pick one, the major practice is **Mathematical Modeling**.

**Why:**
- The heart of the item is applying a probability model to a real situation: 80 physical spins. The student has to treat the spins as repeated trials with a fixed probability and predict a long-run count with expected = n × p. That step is modeling.
- The word "About" shows the item is testing a model-based prediction, not exact counting. Knowing that the real result will vary around the expected value is a modeling idea.
- The other practices support this central step:
  - **Representing** (reading the spinner) supplies the model's input, P(A).
  - **Abstracting and Generalizing** (the complement, 1 − P(A)) adjusts which event the model is about.
  - **Procedural Fluency** (80 × 3/4, for example) works out the model's answer. The arithmetic is simple, so it isn't what makes the item hard.

**Runner-up:** Representing. Without the image, a student who misreads how much of the spinner A covers will get it wrong. But that is a prerequisite, not the main point of the item.

---

## Row 246 (problem_id 126669)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the probability Mai will win the game?
____
```

### Answer 1: practices in order

**Note:** The problem text only says "What is the probability Mai will win the game? ____". It leaves out the game itself (the spinner, dice, cards, or rules, and what counts as a win for Mai). It looks like part of a longer item whose stimulus was cut off. So I can't compute a number, but I can lay out the practice sequence such an item needs.

**NAEP mathematical practices** (NAEP 2026 Framework): (1) Representing, (2) Abstracting and Generalizing, (3) Justifying and Proving, (4) Mathematical Modeling, (5) Collaborative Mathematics. **Added from NRC (*Adding It Up*):** Procedural Fluency.

**Recommended order:**

1. **Representing** (main practice). Turn the game description into a mathematical form: list the sample space (all equally likely outcomes) and mark which ones mean Mai wins. You might use a list, a table, or a tree diagram.
2. **Mathematical Modeling** (secondary practice). Treat the game as a probability model: assume the outcomes are equally likely (a fair spinner, fair die, or random draw) and apply the rule P(win) = favorable outcomes ÷ total outcomes.
3. **Procedural Fluency** (NRC). Count the favorable and total outcomes accurately and write the fraction, simplifying it or converting it to a decimal or percent if asked.
4. *(Optional, light)* **Justifying and Proving.** Quickly check that the answer makes sense: it falls between 0 and 1, and Mai's probability plus her opponent's adds up to 1 if no ties are possible.

**Not needed:** Abstracting and Generalizing, because no general rule or pattern is asked for; and Collaborative Mathematics, because the item is answered alone.

**Summary order:** Representing, then Mathematical Modeling, then Procedural Fluency, then (optionally) Justifying.

If you can share the full game description, I can work out the actual probability and adjust the practice weights.

### Answer 2: major practice

**Major practice: Representing.**

The hard part of this item is turning the game into a sample space. You have to see every equally likely outcome and mark which ones mean Mai wins, usually with a list, a table, or a tree diagram. Once that's set up, the rest is routine: the favorable ÷ total model and counting the fraction (Procedural Fluency). Most student errors on items like this come from a wrong or incomplete outcome list, which is a representation error, not an arithmetic one.

One caveat: the game description is missing from the problem text. If the full item turns out to be a simple case (for example, "a spinner with 3 of 8 equal sections red"), the sample space is given outright. Then Procedural Fluency would arguably be the major practice instead.

---

## Row 252 (problem_id 128001)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Noah wants to save $60 so that he can purchase a concert ticket. If he has saved $45 so far, what percentage of his goal has he saved?
____ %
```

### Answer 1: practices in order

**Problem:** Noah wants to save $60 for a concert ticket. He has saved $45 so far. What percentage of his goal has he saved?

**Answer:** 45/60 = 3/4 = 0.75, so he has saved **75%**.

## Practices available

NAEP Mathematics Framework (2026) practices:
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Mathematical Modeling
5. Collaborative Mathematics

Added from the NRC's *Adding It Up* strands: **Procedural Fluency**, meaning you carry out procedures accurately, efficiently, and flexibly.

## Practices used, in order

### 1. Mathematical Modeling (light use): set up the problem
The student turns the everyday situation (a savings goal and the amount saved) into a math question: "What part of the whole goal is the amount saved?" This means seeing that the $60 goal is the whole (100%) and the $45 saved is the part. This is a small amount of modeling. The situation is simple and fully given, so there are no assumptions to make, no model to refine, and no result to check against the situation.

### 2. Representing: write the relationship in math form
The student writes the relationship as a fraction or ratio, part over whole: 45/60. They could also write the proportion 45/60 = x/100. This step moves the word problem into symbols, and it is where most of the thinking happens. A common mistake here is flipping the ratio (60/45) or subtracting (60 − 45 = 15).

### 3. Procedural Fluency (NRC): do the calculation
The student carries out the arithmetic correctly:
- Simplify 45/60 to 3/4 (divide both by 15), or divide 45 ÷ 60 = 0.75.
- Convert to a percent: 0.75 × 100 = 75%. Or solve the proportion: x = 45 × 100 / 60 = 75.
- Write 75 in the blank, without the % sign, which is already provided.

Knowing that 3/4 = 75% by heart makes this step quick.

### 4. (Optional) Justifying: a quick check
The student checks that the answer makes sense. $45 is less than $60, so the percent must be under 100%. Also, 75% of $60 = $45. This is an informal check, not a formal justification, so it is a minor, optional step.

## Practices not used
- **Abstracting and Generalizing:** no pattern or general rule has to be found.
- **Justifying and Proving (formal):** the problem doesn't ask for an argument.
- **Collaborative Mathematics:** this is an individual item.

## Summary order
**Mathematical Modeling (light) → Representing → Procedural Fluency → (optional) Justifying as a check**

The two main practices are **Representing** (setting up 45/60 as part over whole) and **Procedural Fluency** (turning it into 75%).

### Answer 2: major practice

**Major practice: Representing**

Why:
- **It's the key step.** The main task is turning "saved $45 of a $60 goal" into the part-over-whole fraction 45/60 (or the proportion 45/60 = x/100). Once that is written, the rest is routine.
- **It's where students go wrong.** The usual mistakes all come from setting it up wrong: flipping the ratio (60/45 ≈ 133%), subtracting (60 − 45 = 15), or using the remaining amount (15/60 = 25%). Few students fail at the arithmetic itself.
- **It's what the item checks.** The question tests whether a student understands a percent as a part of a whole, which is a representation idea.

**Close second: Procedural Fluency.** Turning 45/60 into 3/4, then 0.75, then 75% is necessary. But the numbers are friendly and 3/4 = 75% is a well-known fact, so this step is unlikely to be what makes the problem hard.

Mathematical Modeling is involved only lightly. The situation is simple and fully given, so there is no real modeling cycle (no assumptions to make, nothing to check against the situation).

---

## Row 253 (problem_id 128305)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
How many pages are in the book?
____ pages
```

### Answer 1: practices in order

**Note first:** The problem text you shared is only the question, "How many pages are in the book?" with a blank for "____ pages". It leaves out the information the question depends on: a figure, a table, a story setup, or details like pages read per day and pages left. So I can't say for sure which practices apply. Below is the most likely sequence for a typical item of this kind. A common example: "Maria read 1/3 of the book on Monday and 1/4 on Tuesday. She has 50 pages left. How many pages are in the book?" Another: "She reads 12 pages a day for 9 days and finishes the book."

**Practices available**

- NAEP Mathematical Practices (2026 NAEP Mathematics Framework):
  1. Representing
  2. Abstracting and Generalizing
  3. Justifying and Proving
  4. Mathematical Modeling
  5. Collaborative Mathematics
- Added from the NRC strands of mathematical proficiency: **Procedural Fluency**

**Practices in the order they're used**

1. **Mathematical Modeling** (primary)
   The student has to turn a real-world situation (reading a book) into a mathematical problem. That means picking out the unknown (total pages) and the given quantities (pages read, pages left, rate, number of days), and deciding how they relate. Examples are parts adding up to the whole, or rate × time = total.

2. **Representing** (primary)
   The student writes that structure down as a mathematical object. It could be an equation such as x − (1/3)x − (1/4)x = 50 or 12 × 9 = p, a tape or bar diagram, or a table. If the item gives a picture or table, this step also includes reading the needed values from it.

3. **Procedural Fluency (NRC)** (primary)
   The student carries out the calculation accurately and efficiently. Depending on the version, that means multiplying, adding, combining fractions, or solving a one-step or two-step linear equation to get a single whole number of pages.

4. **Justifying and Proving** (secondary, light)
   The student checks that the answer makes sense in context. Is it a whole number of pages? Do the parts add back up to the total? It is light here because the item only asks for a number in a blank, not a written argument.

**Not really involved**

- **Abstracting and Generalizing**: the item asks for one specific number, not a general pattern or rule.
- **Collaborative Mathematics**: it is a single-student item with a short answer.

**Summary order:** Mathematical Modeling → Representing → Procedural Fluency → (light) Justifying and Proving.

If you send the full problem, including any figure, table or story text, I can tighten this up. For example, Representing may come first if the data is given as a picture or table that has to be read before any modeling.

### Answer 2: major practice

**Major practice: Mathematical Modeling**

Here is why I'd pick it over the others:

- **It's where the thinking happens.** The hard part of "How many pages are in the book?" is turning the book situation into math. The student has to decide which quantities matter (pages read, pages left, a rate, a number of days) and how they connect: parts make up the whole, or rate × time = total. Students who get this item wrong usually go wrong at this step, not in the arithmetic.
- **Representing comes after it.** Writing the equation or drawing the bar diagram depends on modeling. Once the relationship is clear, writing it down is fairly routine.
- **Procedural Fluency is real but small.** The calculation is usually just a multiplication, adding fractions, or a one-step or two-step equation. That's grade-level computation, and it only works if the model is right.

**Caveat:** The problem text I have is only the question, with no figure, table or story numbers. Two versions would change my pick:

- If the item just gives a direct calculation, such as "12 pages a day for 9 days," the modeling is trivial. Then **Procedural Fluency** would be the major practice.
- If the information is in a picture or table that has to be read carefully, **Representing** could become the major practice.

---

## Row 256 (problem_id 129451)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
What is the constant of proportionality for this relationship?
____ cups per tablespoon
```

### Answer 1: practices in order

**Note:** The problem refers to "this relationship," but the table, graph, or recipe that defines it isn't included in the text. So I can't give the numeric answer. I can still lay out which practices are needed and in what order. I'm assuming the relationship is given as pairs of (tablespoons, cups) values, for example in a table or a graph.

The practices come from the NAEP 2026 Mathematics Framework: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added Procedural Fluency from the NRC's *Adding It Up*.

### Practices in order

**1. Representing (NAEP).**
First, read the relationship from the representation it is given in (table, graph, or description). Pick out matching pairs of tablespoons and cups. Note which quantity is which: the answer is in *cups per tablespoon*, so cups is the dependent quantity (y) and tablespoons is the independent quantity (x).

**2. Abstracting and Generalizing (NAEP).**
Treat the specific pairs as one proportional relationship, y = kx, where the constant k is the same for every pair. The key step is seeing that "constant of proportionality" means the unit rate: cups ÷ tablespoons, and not the other way around.

**3. Procedural Fluency (NRC).**
Do the arithmetic accurately. Divide cups by tablespoons for a pair (k = cups / tablespoons), and simplify the fraction or decimal. Often the result is a small fraction, since 1 tablespoon = 1/16 cup.

**4. Justifying and Proving (NAEP), light use.**
Check the result by confirming that the same k works for at least one other pair (or that the graph is a straight line through the origin). This confirms that the relationship really is proportional and the ratio wasn't flipped.

### Practices not needed

- **Mathematical Modeling:** not needed. The relationship is already given in mathematical form, so there is no real-world situation to turn into a model.
- **Collaborative Mathematics:** not used. It applies to group work and is not assessed on individual items.

### Summary order
**Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving (brief check)**

The main practice is Abstracting and Generalizing, because recognizing k as cups-per-tablespoon is the core idea. Procedural Fluency carries out the division.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing (NAEP)**

**Why this one:**
- The problem asks for "the constant of proportionality." That is the general description of a proportional relationship (y = kx), not the value of any single data point. To answer, a student has to look past the individual (tablespoons, cups) pairs and see the one fixed multiplier that connects every pair. That is abstraction and generalization.
- This is where students most often go wrong. The usual mistakes are flipping the ratio (giving tablespoons per cup) or reporting one of the values themselves instead of the constant. Both come from not grasping k as the unit rate "cups per tablespoon." They are not arithmetic errors.
- The other practices play supporting roles:
  - **Representing** only gets the numbers out of the table or graph.
  - **Procedural Fluency** is a single division once the ratio is set up correctly.
  - **Justifying and Proving** is an optional check.

So if only one practice could be credited, it would be Abstracting and Generalizing. Procedural Fluency would be a distant second, since it does the actual calculation.

---

## Row 258 (problem_id 112350)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
For the equation 2n − 3 = 7
What is the variable?
____
```

### Answer 1: practices in order

**Problem:** For the equation 2n − 3 = 7, what is the variable?  **Answer:** n

This item doesn't ask you to solve the equation. It only asks you to find which symbol is the variable, so it uses just a few practices.

**Practices used, in order:**

1. **Representing (NAEP).** Read 2n − 3 = 7 as an equation. Tell its parts apart: 2 is a coefficient, 3 and 7 are constants, "−" and "=" are operation and relation signs, and n is a letter that stands for an unknown amount. Knowing what each symbol stands for is the main thing being tested.

2. **Communicating (NAEP).** Know the math word "variable" and what it means: a letter or symbol for an unknown or changing value. This is what links the question's wording to the symbol you just picked out.

3. **Procedural Fluency (NRC).** Spot the letter that isn't a number and write it down quickly and correctly: **n**. This is a light, nearly automatic step here. The skill is recognizing a variable term like "2n" as 2 times n, so the variable is n and not "2n".

**Practices not really needed:** Mathematical Reasoning (no argument or justification is asked for) and Connecting (no link between representations or ideas is needed). Problem solving and computation don't come in either, because nobody asks you to find what n equals (n = 5).

**Order:** Representing → Communicating → Procedural Fluency

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The item asks whether the student understands the symbols in 2n − 3 = 7. The student has to see that the letter n stands for an unknown amount, and that 2, 3 and 7 are fixed numbers. Reading what each symbol means is the core of Representing.

The other practices play a smaller role:
- **Communicating** only adds the vocabulary: knowing that the word "variable" names the letter.
- **Procedural Fluency** only covers writing down "n" once it's found. It's minor here because no solving or computation is needed.

A student who gets this wrong most likely can't yet read an algebraic expression, meaning they don't see that a letter stands for a number. That is a Representing gap.

---

## Row 260 (problem_id 131934)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Tyler orders a meal that costs $15.
If the tax rate is 6.6%, how much will the sales tax be on Tyler’s meal?
$ ____
```

### Answer 1: practices in order

**Answer:** $15 × 0.066 = **$0.99**

The 2026 NAEP Mathematics Framework lists these mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. I've added Procedural Fluency from the NRC's *Adding It Up* strands.

This is a routine one-step percent problem, so only a few practices apply.

### Practices in order

1. **Representing.** This is the main practice. The student turns the words into math:
   - "tax rate is 6.6%" becomes 0.066 (or 6.6/100)
   - "sales tax on a $15 meal" becomes the expression 15 × 0.066

   Switching between the percent, the decimal and the expression is the key step. Most errors here come from mistakes like using 6.6 or 0.66 in place of 0.066.

2. **Procedural Fluency (NRC).** The student does the decimal multiplication correctly: 15 × 0.066 = 0.990, which is $0.99. A common equivalent route is 10% of 15 = 1.50, so 1% = 0.15, and 6.6 × 0.15 = 0.99. Placing the decimal point correctly is the main fluency demand.

3. **Mathematical Modeling (light, optional).** The student reads the result back in context. It's an amount of money, about $1. A quick check (7% of $15 ≈ $1.05) confirms that $0.99 makes sense. This step is minor because the problem already supplies the model (tax = rate × price). The student doesn't have to build it.

### Practices not needed
- **Abstracting and Generalizing:** no pattern or general rule to find.
- **Justifying and Proving:** no explanation or argument is asked for.
- **Collaborative Mathematics:** this is an individual item.

**Summary order:** Representing → Procedural Fluency → (Mathematical Modeling, as a reasonableness check)

### Answer 2: major practice

**Major practice: Representing**

Procedural fluency is close behind, but Representing is the core of this problem:

- The thinking step is translating "a 6.6% tax rate on $15" into 15 × 0.066. Students can only get the answer once they read the percent as the decimal 0.066 and see that sales tax means rate × price.
- Most wrong answers on items like this come from the representation, not the arithmetic. Typical slips are using 6.6 or 0.66 for the rate, adding the tax to the price ($15.99), or dividing.
- Once the expression is set up correctly, the multiplication (15 × 0.066 = 0.99) is routine. That makes procedural fluency the supporting practice, not the one that decides whether the student succeeds.

If the item mainly tested decimal multiplication (for example, "Compute 15 × 0.066"), Procedural Fluency would be the major practice. Because this one is a percent word problem, Representing is.

---

## Row 262 (problem_id 132567)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Mathematical Modeling

### Problem

```text
At a used book sale, 5 books cost $15.
At this rate, how many books can you buy for $21?
____ books
```

### Answer 1: practices in order

**Problem:** At a used book sale, 5 books cost $15. At this rate, how many books can you buy for $21?

**Answer:** 7 books. The price is $15 / 5 = $3 per book, and $21 / $3 = 7.

## Practices used, in order

The NAEP Mathematics Framework (2026) lists five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborating and Discussing. I've also added Procedural Fluency from the NRC's *Adding It Up* strands, as you asked.

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (NAEP) | Turns the story into a math relationship. "At this rate" means price and number of books are proportional. So the student sets up a constant unit rate (dollars per book), or the proportion 5/15 = x/21. |
| 2 | **Representing** (NAEP) | Writes that relationship in a form they can work with. Options include a unit-rate statement ($15 for 5 books, so $3 per book), a proportion, or a ratio table (5 books for $15, 1 book for $3, 7 books for $21). |
| 3 | **Procedural Fluency** (NRC) | Does the arithmetic quickly and correctly: 15 ÷ 5 = 3, then 21 ÷ 3 = 7. Cross-multiplying (15x = 105, so x = 7) works too. |
| 4 | **Justifying** (NAEP, light use) | Checks the answer against the context: 7 books × $3 = $21, and it's a whole number of books. This is a quick check, not a formal proof. |

**Not really used:** Abstracting and Generalizing (the student doesn't need a general rule beyond this one rate) and Collaborating and Discussing (it's a single-person short-answer item).

**Most important:** Modeling (spotting the proportional relationship) and Procedural Fluency (the division). Representing links the two, and Justifying is optional.

### Answer 2: major practice

**Major practice: Mathematical Modeling (NAEP)**

**Why:**

- **The hard part is setting up the problem.** The student has to see that "at this rate" means a proportional relationship and turn it into a unit rate ($3 per book). Then they need to know to divide $21 by that rate.
- **Errors happen mostly at this step.** Students who get it wrong usually pick the wrong operation or combine the numbers wrongly. Typical mistakes are 21 ÷ 5, 21 − 15 + 5 = 11, or 21 × 5 ÷ 15 set up incorrectly. Bad arithmetic is a less common cause.
- **The arithmetic is easy.** 15 ÷ 5 and 21 ÷ 3 are basic division facts for students at this grade level. Procedural Fluency is needed, but it's unlikely to be what separates students who get the item right from those who don't.

**Runner-up:** Procedural Fluency. If you view this as a routine textbook unit-rate exercise, where "at this rate" practically tells the student what to do, you could argue for fluency instead. I'd still put Modeling first because it captures the reasoning the item is actually testing.

---

## Row 269 (problem_id 135051)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Use this answer to find the quotient of one of the previous expressions.
____
```

### Answer 1: practices in order

**Problem:** "Use this answer to find the quotient of one of the previous expressions."

**Caveat:** This item depends on earlier parts that aren't shown here, namely "this answer" and "the previous expressions." It is almost certainly one step in a multi-part task. An earlier step found a result, most likely a product such as 6 x 8 = 48 or a related fact. This step asks the student to reuse that result to get a related quotient (for example 48 ÷ 8 = 6). That is the inverse relationship between multiplication and division, often taught as a fact family. The practices below assume that setup.

**Practices used (NAEP Mathematical Practices + NRC Procedural Fluency):**

The NAEP 2026 framework lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. As you asked, I've added NRC's Procedural Fluency as a sixth.

**Order to solve:**

1. **Abstracting and Generalizing (main practice).** The student has to see the structure linking the earlier answer to a quotient: multiplication and division are inverses, so if a x b = c, then c ÷ b = a and c ÷ a = b. They also have to see that this general relationship applies to one of the earlier expressions. This is the key insight the item tests.

2. **Representing.** Next they rewrite the known fact in a new form, turning the earlier equation (e.g., 6 x 8 = 48) into the matching division (48 ÷ 8 = ?). They also have to pick which earlier expression can be written this way.

3. **Procedural Fluency (NRC).** Then they state the quotient quickly and accurately from the known fact, without recomputing the division from scratch. The point of the item is efficient, flexible use of known facts.

4. **Justifying and Proving (minor, optional).** Finally, a careful student checks the result by multiplying back (quotient x divisor = dividend). That confirms the quotient and shows why reusing the earlier answer is valid.

**Not involved:** Mathematical Modeling (there is no real-world situation to model) and Collaborative Mathematics (this is an individual item).

**Summary order:** Abstracting and Generalizing -> Representing -> Procedural Fluency -> (Justifying and Proving as a check)

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

The item doesn't really test whether the student can divide. It tests whether they see that an answer they already have gives them the quotient right away. To do that, they need to recognize the inverse relationship between multiplication and division (if a x b = c, then c ÷ b = a) and see that this structure fits one of the earlier expressions. Seeing and using that structure is what Abstracting and Generalizing means.

The other practices support this step:
- Representing (rewriting the fact as a division) follows once the relationship is seen.
- Procedural Fluency (stating the quotient) is trivial once the connection is made.
- Justifying (checking by multiplying back) is optional.

A student who misses the structure can still get the quotient by dividing from scratch. But they would be ignoring the instruction to "use this answer," which is the point of the item.

---

## Row 270 (problem_id 137401)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Abstracting and Generalizing

### Problem

```text
Copy and paste the formula to check your prediction.
What number does cell D2 display?
____
```

### Answer 1: practices in order

**A note first:** this item is a follow-up part of a spreadsheet task. The text doesn't include the spreadsheet, the original formula, or the cell values. So I can't give the actual number in D2. What I can give is which practices the item needs and in what order.

**Practices used** (the NAEP 2026 Mathematics Framework practices, plus NRC's procedural fluency)

1. **Representing** (first)
   - Read the spreadsheet as a mathematical representation: cells, cell references, and a formula like `=B2*C2` or `=A2+B1`.
   - Turn the symbolic formula into a quantity relationship ("D2 = the value in column B times the value in column C, same row").

2. **Abstracting and Generalizing** (second)
   - The key idea in "copy and paste the formula" is that relative references shift by the same offset as the paste. For example, `=B1*C1` pasted one row down becomes `=B2*C2`.
   - The student has to generalize the formula from the source cell into a rule that applies to D2. This is what produces the "prediction" the item asks them to check.

3. **Procedural Fluency** (NRC, third)
   - Fill in the actual values from the referenced cells and do the arithmetic (add, multiply, and so on) correctly to get the number D2 displays.

4. **Justifying and Proving** (last, lighter role)
   - "Check your prediction" asks the student to compare the displayed value with the predicted one and confirm the generalized rule is right, or explain the gap.
   - This is a verification step rather than a formal argument.

**Not really involved:** Mathematical Modeling (there's no real-world situation to model in this part) and Collaborative Problem Solving.

**Order:** Representing → Abstracting and Generalizing → Procedural Fluency → Justifying and Proving

**Main practices:** Representing and Abstracting and Generalizing. Procedural fluency is needed to get the final number, but the arithmetic is usually simple.

### Answer 2: major practice

**Major practice: Abstracting and Generalizing**

This is the step the item is really built around. When you copy and paste a spreadsheet formula, the relative cell references shift with the paste. To know what D2 shows, the student has to take the formula from the source cell and turn it into a rule ("each reference moves by the same row/column offset"). Then they apply that rule to D2. That rule is the "prediction" the item tells them to check.

The other practices matter less here:
- **Representing** is needed to read the formula and cell references, but it only sets up the problem.
- **Procedural fluency** gets the final number, but the arithmetic is usually simple.
- **Justifying** is only a light "check your prediction" step.

A student who reads the spreadsheet correctly and does the arithmetic well will still get the wrong answer if they don't understand how the copied formula changes. Abstracting and Generalizing is the main source of difficulty, so it's the major practice.

---

## Row 273 (problem_id 242640)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Find the area of the triangle.
____ square units.
[Image: A triangle on a grid.]
```

### Answer 1: practices in order

**Problem:** Find the area of a triangle drawn on a grid. Answer: ____ square units.

The image isn't available, so I can't give the numeric answer. I can still lay out which practices the problem calls on and in what order. NAEP math describes five practices (Representing, Abstracting, Justifying/Proving, Mathematical Modeling, Using Tools). I've added Procedural Fluency from the NRC strands.

### Practices in order

1. **Representing (NAEP).** Read the grid picture and turn it into numbers. Pick a side to use as the base, ideally one that runs along a grid line. Count grid units to get its length. Then count the height, which is the straight-across distance from the opposite corner to that base line. If no side runs along a grid line, use the box method instead: draw a rectangle around the triangle. Either way, the main step is turning the picture into base, height, or rectangle measurements.

2. **Abstracting (NAEP).** See this as a case of the general rule A = ½ × base × height. The height does not have to be a side of the triangle. It can fall outside the triangle, as with an obtuse triangle. For the box method, see the triangle as the rectangle with some right triangles cut away.

3. **Procedural Fluency (NRC).** Do the arithmetic quickly and correctly. Compute ½ × b × h, or work out the rectangle's area and subtract the corner triangles' areas. Watch for halves when the product is odd. Give the answer in square units.

4. **Justifying / Proving (NAEP), as a light check.** Make sure the result makes sense. The triangle should cover about half of a rectangle with the same base and height. You can also count roughly how many grid squares it covers to see if the number is close.

### Not needed
- **Mathematical Modeling:** this is not a real-world situation, so nothing has to be modeled.
- **Using Tools:** the grid is given and needs no special tool beyond counting. You could fold it into Representing if you want.

### Summary order
**Representing → Abstracting → Procedural Fluency → (Justifying as a check)**

The main practice is Representing, because reading the base and height off the grid is where students most often go wrong. Procedural Fluency carries out the calculation.

### Answer 2: major practice

**Major practice: Representing (NAEP).**

The hard part of this problem is reading the picture. The student has to look at the triangle on the grid and pull out the right numbers. That means picking a base, counting its length in grid units, and counting the height straight across to that base. The height can fall outside the triangle. If no side runs along a grid line, the student has to draw a box around the triangle instead.

Once those numbers are right, the rest is easy. Using ½ × base × height and doing the arithmetic (Procedural Fluency) is routine for a student who knows the formula. Most wrong answers on grid-area problems come from the reading step, such as counting a slanted side as the height or miscounting grid units. They rarely come from the calculation. So Representing is the practice that decides whether a student gets this problem right.

---

## Row 274 (problem_id 242640)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Find the area of the triangle.
____ square units.
[Image: A triangle on a grid.]
```

### Answer 1: practices in order

**Problem:** Find the area of a triangle drawn on a grid (answer in square units).

**Practices available:** the NAEP Mathematics Framework (2026) lists five practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. You asked me to add **Procedural Fluency** from the NRC's *Adding It Up* strands.

The image isn't available to me, so I can't give the numerical answer. I can still give the practice sequence, because a "find the area of the triangle on a grid" item is solved the same way whatever the exact triangle is.

### Practices needed, in order

**1. Representing (NAEP).** This is the main practice. The student has to read the grid picture and turn it into numbers:
- Pick a side to use as the base (usually a horizontal or vertical side) and count its length in grid units.
- Find the height: the perpendicular distance from the opposite vertex to the line through the base, counted in grid units. If the triangle is obtuse, the height may fall outside the triangle.
- If no side lies along a grid line, the student instead draws a rectangle around the triangle (or splits the figure into right triangles). Changing the figure into one whose measures can be counted is still Representing.

**2. Procedural Fluency (NRC).** Once the measures are known, the student applies the routine procedure accurately:
- Use A = ½ × base × height. In the enclosing-rectangle case, use rectangle area minus the corner right triangles.
- Do the arithmetic and write the answer in square units.

### Practices not needed

- **Abstracting and Generalizing:** the formula is simply recalled. The student doesn't derive or generalize it.
- **Justifying and Proving:** the item asks only for a number, with no explanation or argument.
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** this is an individual item.

### Summary

**Representing → Procedural Fluency**

Representing carries most of the difficulty, because the usual mistakes are miscounting the height or using a slanted side as the height. Procedural Fluency covers applying ½bh and computing the result.

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The arithmetic is easy. Once you have a base and a height, ½ × b × h is one quick calculation, so Procedural Fluency is only the final step.

The hard part is reading the grid picture and turning it into the right measurements:
- picking a base and counting its length
- finding the perpendicular height, which may fall outside the triangle when the triangle is obtuse
- if no side lies on a grid line, putting a rectangle around the triangle or splitting it into smaller pieces

Most mistakes on this kind of item come from that step: using a slanted side as the height, miscounting grid units, or picking the wrong segment. That makes Representing the main practice.

---

## Row 276 (problem_id 137056)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Type in the formula, and press enter to check your prediction.
What number does cell C2 display?
____
```

### Answer 1: practices in order

## Practices needed for this problem, in order

**Note on the problem text:** The problem asks the student to type a spreadsheet formula, press Enter, and report the number shown in cell C2. The formula and the values in the other cells are not in the text. They were probably in a table or an earlier step. Without them I can't work out the actual number. I can still say which practices the task calls for and in what order.

**Practice set used:** the 2026 NAEP Mathematics Framework practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics), plus **Procedural Fluency** from the NRC's strands of mathematical proficiency.

### Order of use

1. **Representing (NAEP)**
   The student first has to read the spreadsheet as a mathematical representation. Cell references like A2 and B2 act as variables. The formula in C2 is a symbolic expression in those variables, and the displayed value is the result. This means turning the formula into ordinary arithmetic, for example "=A2*B2" becomes "the value in A2 times the value in B2".

2. **Procedural Fluency (NRC)**
   Next the student substitutes the cell values and carries out the operations accurately, using the correct order of operations. This produces the prediction. This is where the actual computing happens.

3. **Justifying and Proving (NAEP)** (light use)
   Finally the student types in the formula and presses Enter to check the prediction against what the spreadsheet shows. If the two numbers differ, the student has to find the cause, such as a wrong cell reference, the order of operations, or an arithmetic slip.

### Practices not needed
- **Abstracting and Generalizing:** Not needed for a single cell. It would matter only if the formula were filled down a column and the student had to see the general pattern.
- **Mathematical Modeling:** No real-world situation has to be turned into a model. The formula is already given.
- **Collaborative Mathematics:** This is a task done alone.

**Summary sequence:** Representing → Procedural Fluency → Justifying and Proving (check). The main practices are Representing and Procedural Fluency.

### Answer 2: major practice

## Major practice: Representing (NAEP)

If I had to pick one, I would pick **Representing**.

**Why:**
- **It's the main hurdle.** To predict what C2 shows, the student has to understand spreadsheet notation. Cell references like A2 and B2 stand for values, the "=" means "compute this," and the formula is a symbolic expression. A student who can't move between the formula and the arithmetic it stands for can't even start. A student who can usually gets the right answer.
- **The arithmetic is probably easy.** Spreadsheet prediction tasks like this usually use simple numbers and one or two operations. So Procedural Fluency is needed but probably isn't what makes the problem hard.
- **The check is built in.** The spreadsheet itself confirms the answer when the student presses Enter, so Justifying plays only a small part.

**Caveat:** The formula and cell values aren't in the problem text. If the formula turns out to be long, with several operations where order of operations is the main trap, Procedural Fluency would be a close second and could even come first. Based on what the task shows, though, the key skill is reading the formula as a representation.

---

## Row 278 (problem_id 138605)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the area of the triangle?
____ square units
```

### Answer 1: practices in order

**Problem:** "What is the area of the triangle? ____ square units"

Note: the problem text refers to a figure that isn't included, probably a triangle drawn on a grid or with its base and height labeled. The analysis below assumes that standard setup: read the base and height from the figure, then use A = ½ × b × h.

**NAEP Mathematical Practices (2026 framework):**
1. Representing
2. Abstracting and Generalizing
3. Justifying and Proving
4. Modeling
5. Collaborative Mathematics
6. (added) **Procedural Fluency** (NRC, *Adding It Up*): carrying out procedures flexibly, accurately, and efficiently.

**Practices needed, in order:**

1. **Representing (primary, first step).** The student has to read the diagram and turn it into numbers. That means finding a side to use as the base and the perpendicular height that goes with it, either by counting grid units or reading labels. If the triangle is on a grid with no labels, the student may need to count squares, or picture an enclosing rectangle and subtract pieces from it. This is the main cognitive step and the place where most mistakes happen, such as using a slanted side as the height.

2. **Procedural Fluency (primary, second step).** The student recalls A = ½ × b × h, multiplies, halves the result, and writes it in square units. This step is routine once the measurements are known.

3. **Justifying and Proving (minor, optional).** The student might briefly check the answer, for example by noting that the triangle is half of a b × h rectangle. The item doesn't ask for this.

**Not needed:** Abstracting and Generalizing (it's a single case with no pattern to generalize), Modeling (there's no real-world context), and Collaborative Mathematics (it's an individual item).

**Order:** Representing → Procedural Fluency (→ optional Justifying as a self-check)

### Answer 2: major practice

**Major practice: Representing**

If I have to pick one, it's **Representing**. The item names no measurements in its text, so everything the student needs comes from the figure. The student has to read the triangle and turn it into numbers: which side is the base, and which perpendicular segment is the height that goes with it. With a grid, that means counting units. With an obtuse or tilted triangle, the height may fall outside the triangle, or the student may need to use an enclosing rectangle and subtract pieces from it.

That step is what makes the item hard. Most wrong answers come from it: using a slanted side as the height, or miscounting grid units. Once b and h are right, applying A = ½ × b × h (Procedural Fluency) is routine and rarely where students go wrong. So Procedural Fluency is a necessary but secondary practice, and Representing is the main one.

Caveat: if the figure labels the base and height directly, the item becomes close to pure formula use. In that case Procedural Fluency would be the major practice instead.

---

## Row 281 (problem_id 138263)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Use the table to help you solve the following problems.
[Table:
number of tacos | price in dollars
|
|
|
|
|]
Noah bought 4 tacos and paid $6. At this rate, how many tacos could he buy for $15?
____
```

### Answer 1: practices in order

## Practices used to solve the problem, in order

**Problem:** Noah bought 4 tacos for $6. At the same rate, how many tacos can he buy for $15? (A blank table with columns for number of tacos and price in dollars is provided.)

**Answer:** 10 tacos

The NAEP Mathematics Framework names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Discourse. I added a sixth, Procedural Fluency from the NRC's *Adding It Up* strands, as you asked. Four of these are needed, in this order:

| Step | Practice | What the student does |
|---|---|---|
| 1 | **Mathematical Modeling** (NAEP) | Turns the story into a math relationship. "At this rate" means price and number of tacos stay in proportion, so this is a constant-rate (ratio) situation: 4 tacos ↔ $6, and the unknown number of tacos ↔ $15. |
| 2 | **Representing** (NAEP) | Fills in the table to show the ratio, e.g. 2 tacos → $3, 4 → $6, 6 → $9, 8 → $12, 10 → $15. Here the table is the main tool for solving, not just decoration. |
| 3 | **Procedural Fluency** (NRC) | Does the arithmetic correctly: finds the unit rate ($6 ÷ 4 = $1.50 per taco, or 2 tacos per $3), then $15 ÷ $1.50 = 10. Another route is $15 ÷ $3 = 5 groups, and 5 × 2 = 10 tacos. |
| 4 | **Abstracting and Generalizing** (NAEP), light | Sees the pattern in the table (each extra 2 tacos adds $3, so price = 1.5 × tacos) and extends it to $15. This is a small role, since the pattern is one of the easiest kinds. |

### Practices not needed
- **Justifying and Proving:** the item only asks for a number, not an explanation or argument. At most the student checks that 10 × $1.50 = $15.
- **Collaborative Discourse:** this is an individual item with no peer interaction.

### Summary order
**Mathematical Modeling → Representing → Procedural Fluency → (Abstracting and Generalizing)**

Representing and Procedural Fluency do most of the work. Modeling is the key first step that makes the rest possible, and Abstracting and Generalizing plays a supporting role.

### Answer 2: major practice

## Major practice: **Representing** (NAEP)

If I have to pick one, it's **Representing**. Here's why:

- **The item tells students to use it.** It opens with "Use the table to help you solve the following problems" and gives an empty table with columns for *number of tacos* and *price in dollars*. The intended solution is to fill that table with equivalent ratios (4 → $6, 6 → $9, 8 → $12, 10 → $15) until the price reaches $15.
- **The table does most of the work.** Once the ratio is in the table, the answer can be read straight from it. The student doesn't need much separate calculation or formal reasoning.
- **The other practices play a smaller part:**
  - *Mathematical Modeling* is easy here. "At this rate" says outright that the relationship is proportional, so there's almost nothing to model.
  - *Procedural Fluency* is needed, but the arithmetic is small (adding 2 tacos and $3, or $15 ÷ $1.50). The table lets students avoid most formal computation.
  - *Abstracting and Generalizing* is just extending a simple repeating pattern.

**Runner-up: Procedural Fluency.** A student who ignores the table and computes the unit rate ($6 ÷ 4 = $1.50, then $15 ÷ $1.50 = 10) uses fluency instead of representing. But the item is clearly designed around the table, so **Representing** is the best single label.

---

## Row 283 (problem_id 24929)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Find the area of the shape.
[Image: A shape with six sides. It is 9 units long and six units wide at it’s widest point. Two vertical sides connect four sloped sides, which meet at either end of the shape.]
____ square units
```

### Answer 1: practices in order

## Practices for this problem

The practices I can draw on are the NAEP Mathematics Framework (2026) practices: **Representing**, **Abstracting and Generalizing**, **Justifying and Proving**, **Mathematical Modeling**, and **Collaborative Mathematics**. I've added **Procedural Fluency** from the NRC strands of proficiency (*Adding It Up*), as you asked.

**The problem:** find the area of a six-sided shape that is 9 units long and 6 units wide at its widest point. It has two vertical sides joined by four sloped sides, and the sloped sides meet in a point at each end.

### Practices in order

**1. Representing (NAEP)**
The student turns the picture into a structure they can calculate with. They break the hexagon into simpler pieces: a rectangle in the middle, between the two vertical sides, and a triangle at each end where the sloped sides meet. Or they enclose the whole shape in a 9 × 6 rectangle and see four right triangles cut off the corners. They also read the needed lengths off the figure or grid: overall length 9, greatest width 6 (the vertical sides), and how far each pointed end sticks out past the vertical sides.

**2. Abstracting and Generalizing (NAEP)** *(a small role)*
The student sees that the two end pieces are the same shape, so they only need to work out one and double it. They also see that the area of any pieced-together shape is the sum of its parts, or the enclosing rectangle minus the corners cut away. This choice of method is what drives the calculation.

**3. Procedural Fluency (NRC)**
The student uses the area formulas correctly and does the arithmetic:
- Rectangle: width × middle length = 6 × *m*
- Each end triangle: ½ × base × height = ½ × 6 × *t*, with 2*t* + *m* = 9
- Total = 6*m* + 6*t* = 3(9 + *m*)

For example, if the vertical sides are 3 units apart (*m* = 3, *t* = 3): 18 + 9 + 9 = **36 square units**. You get the same answer by subtraction: 54 − 4 × (½ × 3 × 3) = 54 − 18 = 36. The student must use the actual middle length shown in the figure.

**4. Justifying and Proving (NAEP)** *(optional, light)*
The student checks the answer makes sense. It must be less than the 9 × 6 = 54 bounding rectangle and more than the middle rectangle alone. Getting the same total by adding the pieces and by subtracting the corners confirms it. Answering in square units is also part of this check.

### Practices that don't apply
- **Mathematical Modeling:** there is no real-world situation to model. It's a pure geometry figure.
- **Collaborative Mathematics:** it's a task done alone, and NAEP doesn't assess this practice on individual items.

### Summary
**Representing → Abstracting and Generalizing → Procedural Fluency → (Justifying and Proving)**

The most important practices are **Representing**, to break the figure into pieces and read off the lengths, and **Procedural Fluency**, to apply the rectangle and triangle area formulas and do the arithmetic.

### Answer 2: major practice

## Major practice: **Representing (NAEP)**

The hard part of this problem is seeing how to break up the hexagon. No single area formula fits a six-sided shape with pointed ends. The student has to split it into a middle rectangle and two end triangles, or enclose it in a 9 × 6 rectangle and subtract the corner triangles. They also have to read the right lengths off the figure: the overall length of 9, the width of 6, and the middle length versus how far each end sticks out.

Once the shape is split up, the rest is routine. It's just ½ × base × height, length × width, and a sum. That calculation is **Procedural Fluency**, and it comes a close second. But the errors that separate students who get this right from those who don't are mostly about representing the shape. Examples are using 9 × 6 = 54 for the whole shape, or using the wrong lengths for the triangles. Errors in the arithmetic itself are less common.

**Answer: Representing**

---

## Row 284 (problem_id 146150)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Order the people from greatest to least in terms of how fast they checked the comments.

Items to put in order:
- Person 1
- Person 4
- Person 2
- Person 3
```

### Answer 1: practices in order

**Practices available:** the NAEP 2026 mathematical practices are Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematical Discourse. I've added NRC Procedural Fluency to that list.

**Note:** I only have the item's text, not the table or graph it refers to. The text only names Persons 1–4, so I can't give the actual ranking. The practice sequence below follows from what the item asks: rank people by "how fast" they checked comments. That means rank them by a rate, comments per unit of time, read from the data shown.

### Practices to use, in order

1. **Representing (main practice)**
   - Read the data display (table, graph, or list of times and counts) and pull out each person's numbers.
   - If it's a graph, a steeper line, or more comments in the same time, means faster.
   - Turn what's shown into something you can compare: a rate for each person.

2. **Procedural Fluency (NRC)**
   - Do the calculations accurately.
   - Divide comments by time, or time by comments, for each person. Convert units if needed, such as minutes to hours.
   - Compare the resulting numbers, including fractions or decimals.

3. **Abstracting and Generalizing (supporting, minor)**
   - Recognize that "fastest" means the highest rate (most comments per unit of time) or the shortest time per comment, not simply the largest count or the longest time.
   - Apply that one rule the same way to all four people.

4. **Justifying and Proving (light check, optional)**
   - Check that the order runs from greatest to least speed, not least to greatest.
   - Make sure every comparison is consistent with the computed rates.

**Not needed:** Mathematical Modeling, since there's no real-world situation to build a model from, and Collaborative Mathematical Discourse.

**Summary order:** Representing → Procedural Fluency → (Abstracting and Generalizing) → (Justifying and Proving). Representing and Procedural Fluency do most of the work.

### Answer 2: major practice

**Major practice: Representing**

Answering this item mostly depends on reading the data display correctly: the table, graph, or list of times and counts. From that display you get a "speed" for each person, then rank them. The task gives no numbers in its text. Everything comes from the representation.

The arithmetic is usually a simple division or a comparison of slopes, which is Procedural Fluency. Most errors happen in reading the display. Students take the wrong quantity, read "fastest" as the largest count instead of the highest rate, or misread a graph's steepness. So Representing is the practice that decides whether a student gets this item right.

Caveat: I only have the item's text, not its data display. If the display gives times that need real calculation, such as unequal comment counts that must be turned into comments per minute, Procedural Fluency becomes a close second. Representing would still be my pick.

---

## Row 285 (problem_id 146018)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
A company is hiring people to read through all the comments posted on their website to make sure they are appropriate. Four people applied for the job and were given one day to show how quickly they could check comments.
- Person 1 worked for 210 minutes and checked a total of 50,000 comments.
- Person 2 worked for 200 minutes and checked 1,325 comments every 5 minutes.
- Person 3 worked for 120 minutes, at a rate represented by c = 331t,
where c is the number of comments checked and t is the time in minutes.
- Person 4 worked for 150 minutes, at a rate represented by t = (3/800)c
Order the people from greatest to least in terms of total number of comments checked.

Items to put in order:
- Person 1
- Person 2
- Person 3
- Person 4
```

### Answer 1: practices in order

## Practices available

The NAEP Mathematics Framework (2026) names five mathematical practices:
1. **Representing** – moving between and reading different forms of the same quantity (words, tables, equations, graphs).
2. **Abstracting and Generalizing** – finding the common structure across cases, such as treating different descriptions as the same kind of relationship.
3. **Justifying and Proving** – building or checking an argument for why a result is true.
4. **Mathematical Modeling** – turning a real situation into mathematics, working inside the model, then reading the result back in context.
5. **Collaborative Mathematical Discourse** – reasoning together with others. NAEP does not assess this one on individual items.

Added from the NRC's *Adding It Up* strands:
6. **Procedural Fluency** – carrying out procedures (multiplying, dividing, solving for a variable) accurately and efficiently.

## Practices needed, in order

**Step 1 – Representing (main practice).**
Each person's work is described in a different form:
- Person 1: a total in words (50,000 comments in 210 minutes)
- Person 2: a rate in words (1,325 comments every 5 minutes)
- Person 3: an equation with c as a function of t (c = 331t)
- Person 4: an inverse equation with t as a function of c (t = (3/800)c)

The student has to read each form and see what it tells them about the total. The key representational step is Person 4. That equation gives time in terms of comments, so it has to be rearranged to c = (800/3)t. Without that, the student cannot compare Person 4 with the others. This is where most of the difficulty is.

**Step 2 – Mathematical Modeling (light).**
The student sets up the same model for everyone, total comments = rate × time, using each person's own working time. Person 1 is a distractor. The 210 minutes is extra information because the total is already given. The student must see that the question asks for *totals*, not rates.

**Step 3 – Procedural Fluency.**
Do the arithmetic:
- Person 1: 50,000 (given)
- Person 2: 200 ÷ 5 = 40 intervals, and 40 × 1,325 = **53,000**
- Person 3: 331 × 120 = **39,720**
- Person 4: c = (800/3) × 150 = 800 × 50 = **40,000**

**Step 4 – Representing / interpreting in context (brief).**
Order the totals from greatest to least and match them back to the people.

**Answer:** Person 2 (53,000) > Person 1 (50,000) > Person 4 (40,000) > Person 3 (39,720)

## Summary

| Order | Practice | Role |
|---|---|---|
| 1 | Representing | Read four different forms and rearrange t = (3/800)c into c = (800/3)t (**primary**) |
| 2 | Mathematical Modeling | Use total = rate × time for everyone and ignore the extra 210 minutes (secondary) |
| 3 | Procedural Fluency (NRC) | Do the division and multiplication accurately (secondary, but required) |

**Not needed:** Abstracting and Generalizing, beyond a slight sense that all four cases are proportional; Justifying and Proving, since no argument is asked for; Collaborative Mathematical Discourse, which NAEP does not assess.

### Answer 2: major practice

**Major practice: Representing**

What makes this item hard is that each person's rate comes in a different form. Person 1 has a total in words, Person 2 has a rate in words, Person 3 has an equation c = 331t, and Person 4 has an inverse equation t = (3/800)c. The arithmetic is simple (40 × 1,325, 331 × 120, (800/3) × 150), so Procedural Fluency is not where students separate.

The task is mainly about reading and translating between these forms. The hardest single step is noticing that Person 4's equation gives time in terms of comments, and rewriting it as c = (800/3)t. Getting that one translation right decides whether Person 4 ends up in the right place in the order.

Mathematical Modeling plays a smaller part. It means using total = rate × time for everyone and seeing that Person 1's 210 minutes is extra information. But the item has already set up the situation, so students mostly need to read the given representations, not build a model of their own.

Answer: Person 2 (53,000) > Person 1 (50,000) > Person 4 (40,000) > Person 3 (39,720).

---

## Row 288 (problem_id 151647)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
4000 is 4 times what number?
____
```

### Answer 1: practices in order

**Problem:** 4000 is 4 times what number? (Answer: 1000)

The NAEP Mathematics Framework (2026) names five mathematical practices: Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, and Collaborative Mathematics. You asked me to add NRC's **Procedural Fluency** as well.

This is a short, one-step item, so only a few practices really come into play. Here is the order I'd expect a student to use them.

### 1. Representing (NAEP)
The student turns the words into math. "4000 is 4 times what number" becomes an equation with an unknown, **4 × n = 4000**. The student could also picture it as 4 equal groups that add up to 4000. Most of the thinking in this problem happens here: reading "is" as "=" and "4 times what number" as 4 × n.

### 2. Procedural Fluency (NRC)
The student solves the equation by undoing the multiplication with the inverse operation: **n = 4000 ÷ 4 = 1000**. A fluent student does this quickly and correctly, using a known fact (4 ÷ 4 = 1) and place value (keeping the three zeros) instead of doing long division.

### 3. Justifying (NAEP Justifying and Proving), light and optional
The student checks the answer by putting it back into the original statement: 4 × 1000 = 4000. This is a quick self-check, not a written argument. It confirms that the student divided rather than multiplied by mistake (writing 16000 is the classic error).

### Practices that don't apply
- **Abstracting and Generalizing:** No pattern or general rule has to be found.
- **Mathematical Modeling:** There's no real-world situation to model. The item is purely numerical.
- **Collaborative Mathematics:** This is an individual item.

**Summary order:** Representing → Procedural Fluency → (Justifying as a check)

### Answer 2: major practice

**Major practice: Representing (NAEP)**

The main challenge in this problem is turning the words into the right equation. A student has to read "4000 is 4 times what number" as **4 × n = 4000**. That means seeing that 4000 is the product, not one of the factors, so the student has to divide.

The other practices matter less here:
- **Procedural Fluency** is needed, but the computation is easy. 4000 ÷ 4 = 1000 follows from a basic fact plus place value. Once the equation is set up correctly, almost every student gets this step right.
- **Justifying** is only an optional check.

The most common wrong answer is 16000, which comes from multiplying 4000 × 4. That is a representation error, not a computation error. Students who miss this item most likely misread the relationship, not the arithmetic. That is why I'd pick Representing as the major practice.

---

## Row 289 (problem_id 151533)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
8 is 32 times what number?
____
```

### Answer 1: practices in order

**Problem:** 8 is 32 times what number?

**Answer:** 8 ÷ 32 = **1/4 (0.25)**

---

### Practices available
The NAEP Mathematics Framework (2026) lists five mathematical practices: **Representing**, **Abstracting and Generalizing**, **Justifying and Proving**, **Mathematical Modeling**, and **Collaborative Mathematics**. As you asked, I've added **Procedural Fluency** from the NRC's *Adding It Up* strands.

### Practices used, in order

**1. Representing** (main practice)
The student has to turn the sentence into math. "8 is 32 times what number" becomes **32 × n = 8**. This is the hardest part of the problem. The usual mistake is to reverse the relationship and compute 32 ÷ 8 = 4, or to multiply 8 × 32 = 256. Getting the answer right depends on reading "is" as "=" and "times what number" as "32 × n", with the unknown number being the smaller one.

**2. Procedural Fluency (NRC)**
Next, solve the equation. Use the inverse of multiplication: n = 8 ÷ 32. Then simplify the fraction 8/32 to 1/4, or convert it to 0.25. Here the student has to be comfortable dividing a smaller number by a larger one and getting a fraction less than 1, instead of assuming the answer must be a whole number.

**3. Justifying and Proving** (light, optional)
Check the answer by putting it back in: 32 × 1/4 = 8. This is a quick reasonableness check, not a formal proof. Many students will skip it, so it plays a small role.

### Practices not used
- **Abstracting and Generalizing:** the problem doesn't ask for a pattern or general rule.
- **Mathematical Modeling:** there is no real-world context. The problem is already stated mathematically.
- **Collaborative Mathematics:** this is an individual item.

### Summary
**Representing → Procedural Fluency → (Justifying, as a check)**

Representing does most of the work, because translating the words in the right direction is the main difficulty. Procedural fluency comes second, for dividing to get a fraction less than 1.

### Answer 2: major practice

**Major practice: Representing**

The arithmetic here is easy: 8 ÷ 32 = 1/4. What makes the problem hard is turning "8 is 32 times what number?" into **32 × n = 8**.

Wrong answers come from getting that translation wrong, not from the calculation:
- Reversing the relationship gives 32 ÷ 8 = **4**. This is the most common error, since students expect the answer to be a whole number bigger than 1.
- Treating "times" as "multiply the numbers you see" gives 8 × 32 = **256**.

A student who writes 32 × n = 8 correctly will almost always finish the problem. A student who sets it up wrong can't be rescued by good computation. Procedural fluency, meaning dividing to get a fraction less than 1, still matters, but it comes second. Representing is the practice that decides whether the answer is right.

---

## Row 294 (problem_id 157579)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
What is the slope of this line?
____
```

### Answer 1: practices in order

**Problem:** "What is the slope of this line?" (The line is shown in a graph on a coordinate plane. The graph isn't in the text, so the steps below are general rather than tied to specific numbers.)

**Practices available:** the five NAEP mathematical practices (Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling, Collaborative Mathematics) plus NRC **Procedural Fluency**.

### Practices needed, in order

**1. Representing (main practice)**
- Read the graph. Find two points where the line crosses grid intersections exactly, and write down their coordinates, e.g. (x1, y1) and (x2, y2).
- Turn the picture into numbers: "rise over run". Count the vertical change and horizontal change between the two points, or set up (y2 − y1)/(x2 − x1).
- Get the sign from the picture: a line going up from left to right has a positive slope, and one going down has a negative slope.
- Most of the difficulty is here. Common mistakes are misreading the axis scale, picking points that aren't exactly on grid lines, and swapping rise and run.

**2. Procedural Fluency (NRC)**
- Do the arithmetic: subtract the coordinates in a consistent order, divide, and simplify the fraction (for example 6/4 → 3/2) with the correct sign.
- This is quick and routine once step 1 is right.

**3. (Optional, minor) Abstracting and Generalizing**
- Recognize that slope is a constant rate of change, so any two points on the line give the same answer. A student can check by using a second pair of points.
- A routine solution doesn't need this, so it plays a small part at most.

### Practices not used
- **Justifying and Proving:** the problem asks only for a value, not an argument.
- **Mathematical Modeling:** there is no real-world context to turn into math.
- **Collaborative Mathematics:** this is an individual item.

### Summary
**Representing → Procedural Fluency** (optionally → Abstracting and Generalizing as a check).
Representing is the main practice. Procedural fluency is a small, routine final step.

### Answer 2: major practice

**Major practice: Representing**

Why this one:
- **Most of the work is reading the graph.** The student has to pick two points that sit exactly on grid intersections, read their coordinates correctly using the axis scale, and turn the picture into "rise over run". That means moving from a graph to numbers, which is what Representing is.
- **Most mistakes happen here.** Students misread the scale, choose points that aren't exactly on the line, swap rise and run, or get the sign wrong for a line that falls from left to right. All of these are errors in reading the graph, not in arithmetic.
- **Procedural fluency is a small part.** Once the student has the rise and run, all that's left is one subtraction, one division and maybe simplifying a fraction. That is quick and routine.

So the item is mainly testing whether the student can get slope from a graph, and that makes Representing the major practice.

---

## Row 297 (problem_id 156692)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
A population of red ants was 640. After a season of heavy rainfall, the ant population decreased by 50%. In the following dry season, the population increased by 5%. What is the ant population after the increase?
____ red ants
```

### Answer 1: practices in order

**Practices available**

The NAEP 2026 Mathematics Framework lists five mathematical practices:
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics

You asked me to add one more:
- **Procedural Fluency** (NRC, *Adding It Up*): carrying out procedures flexibly, accurately and efficiently.

**Answer: 336 red ants**

**Practices in the order they are used**

1. **Representing** (main practice)
   - Turn the story into math. "Decreased by 50%" becomes multiplying by (1 − 0.50) = 0.50. "Increased by 5%" becomes multiplying by (1 + 0.05) = 1.05.
   - The key point: the second change is a percent of the *new* population, not of the original 640. So the steps are chained: 640 → ×0.50 → ×1.05.
   - This step also blocks the common mistake of combining the percents into one change (−50% + 5% = −45%, giving 640 × 0.55 = 352).

2. **Procedural Fluency** (main practice)
   - Do the arithmetic:
     - 640 × 0.50 = 320
     - 320 × 1.05 = 320 + 16 = 336
   - This means finding a percent of a number and multiplying decimals accurately, perhaps using the shortcut "5% of 320 = 16."

3. **Justifying and Proving** (minor, optional)
   - A quick check that the answer makes sense. Halving should give about 300, and a small 5% increase should add only a little, so 336 is reasonable.
   - It also confirms the answer is not 352, the result of combining the percents.

**Practices not needed**
- **Mathematical Modeling**: the situation is already a clean, fully stated math task, with no assumptions to make or model to refine.
- **Abstracting and Generalizing**: there is no pattern or general rule to find.
- **Collaborative Mathematics**: this is a solo task.

**Summary:** Representing → Procedural Fluency → (optional) Justifying and Proving. Answer: **336**.

### Answer 2: major practice

**Major practice: Representing**

**Why Representing comes first**
- The real challenge is how you set the problem up, not the arithmetic. You have to turn "decreased by 50%" and then "increased by 5%" into two chained multiplications (640 × 0.50 × 1.05). Each percent applies to the population at that moment, not to the original 640.
- Most wrong answers start here. The common mistake is to combine the percents into one change (−50% + 5% = −45%, giving 352), or to take 5% of the original 640. Both are representation errors, not calculation errors.
- Once the problem is set up correctly, the arithmetic is easy. Halving 640 and adding 5% of 320 is routine, with friendly numbers (320, 16, 336).

**A close second: Procedural Fluency**
- The problem does test the routine percent procedure, so a student who can't find a percent of a number accurately would still fail.
- But the numbers are chosen to make the calculation easy. That suggests the item is really checking whether students model successive percent changes correctly.

**Answer: Representing** (Procedural Fluency is secondary).

---

## Row 298 (problem_id 3216)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
The two triangles displayed are scaled copies of one another.
[Image: Two triangles. Triangle on left, left side = x, bottom side = 4. Triangle on right, left side = 25, bottom = 10.]
What is the value of x?
x = ____ units
```

### Answer 1: practices in order

**Practices available (NAEP 2026 Mathematics Framework, plus one from NRC):**
- Representing
- Abstracting and Generalizing
- Justifying and Proving
- Mathematical Modeling
- Collaborative Mathematics
- Procedural Fluency (NRC, *Adding It Up*)

**Solution:** The triangles are scaled copies, so matching sides share one scale factor. The bottom sides match: 4 → 10, so the scale factor is 10 ÷ 4 = 2.5. The left sides match: x → 25, so x = 25 ÷ 2.5 = **10 units**. (As a proportion: x/4 = 25/10, so x = 10.)

**Practices used, in order:**

1. **Representing.** Read the diagram and turn it into math. You have to see which side of the small triangle goes with which side of the large one (left with left, bottom with bottom), then write that as a ratio or proportion: x/25 = 4/10, or x/4 = 25/10. This is the main step of the problem. If you pair the wrong sides, you get the wrong answer.

2. **Abstracting and Generalizing** (supporting role). Use the general idea that "scaled copies" means every pair of matching sides has the same ratio. That rule is what lets you turn the picture into one equation. This step is small because it uses a familiar fact; you aren't building a new generalization.

3. **Procedural Fluency (NRC).** Do the arithmetic correctly: find the scale factor (10 ÷ 4 = 2.5), then 25 ÷ 2.5 = 10, or cross-multiply (10x = 100, so x = 10).

**Optional final check:** 4 × 2.5 = 10 and 10 × 2.5 = 25, so the answer works. This is a light check, not a full use of Justifying and Proving.

**Practices not needed:** Justifying and Proving (no argument has to be written), Mathematical Modeling (there is no real-world situation to model), and Collaborative Mathematics (this is an individual item).

**Order in short:** Representing → (Abstracting and Generalizing) → Procedural Fluency. Representing is the key step.

### Answer 2: major practice

**Major practice: Representing**

The hard part of this problem is reading the diagram. You have to see which side of the small triangle goes with which side of the large one (x with 25, 4 with 10). Then you turn that into a proportion: x/4 = 25/10, or x/25 = 4/10. Once that proportion is right, the arithmetic is simple (Procedural Fluency: x = 10). If you pair the wrong sides (for example, x/10 = 4/25), you get the wrong answer even if every calculation is correct.

So most of the difficulty, and most of the chances to go wrong, comes from turning the picture into math. That is why I'd choose Representing as the major practice.

---

## Row 300 (problem_id 158484)

- **predicted_practice:** Procedural Fluency
- **claude_top_practice:** Representing

### Problem

```text
Each square on a grid represents 1 unit on each side.
[image]
Calculate the slope of graph D.
____
```

### Answer 1: practices in order

## Practices available

The NAEP 2026 Mathematics Framework lists five mathematical practices:
1. **Representing**: moving between representations (graphs, tables, symbols, words) and reading information off them.
2. **Abstracting and Generalizing**: seeing a structure or relationship that holds beyond one case.
3. **Justifying and Proving**: building or judging a mathematical argument.
4. **Mathematical Modeling**: using mathematics to describe a real-world situation and reading the result back into it.
5. **Collaborative Mathematical Discourse**: discussing, critiquing, and building on other people's mathematical ideas.

Added from the NRC (*Adding It Up*) strands:
6. **Procedural Fluency**: carrying out procedures (such as computing and simplifying) accurately, efficiently, and flexibly.

## The problem

"Each square on a grid represents 1 unit on each side. [graph] Calculate the slope of graph D."

The image isn't included, so I can't give the numerical slope. The practices and their order don't depend on the specific line, though.

## Practices needed, in order

**1. Representing (main practice)**
- Find graph D among the graphs shown.
- Use the scale (1 square = 1 unit) to read the coordinates of two points where line D crosses grid intersections exactly, for example its intercepts.
- Turn the visual line into numbers: the vertical change (rise) and the horizontal change (run) between those points. Note the direction: if the line falls from left to right, the rise is negative.

**2. Procedural Fluency (secondary practice)**
- Apply the slope procedure: m = (y2 − y1)/(x2 − x1), or rise/run.
- Do the signed subtraction correctly and reduce the fraction to simplest form (or write it as a whole number or decimal).
- This step is routine once the numbers are read correctly, but the common errors happen here: reversing the subtraction order, dropping a negative sign, or computing run/rise.

**3. Abstracting and Generalizing (minor, optional)**
- Knowing that slope is a constant rate of change, so any two points on a straight line give the same value. A student can use this to choose convenient lattice points, or to check the answer with a second pair of points.
- This helps but isn't needed for a basic correct answer.

**Not needed:**
- **Justifying and Proving**: no argument or explanation is asked for.
- **Mathematical Modeling**: there is no real-world context.
- **Collaborative Mathematical Discourse**: this is an individual task with no discussion of other people's reasoning.

## Summary

**Representing → Procedural Fluency** (optionally → Abstracting and Generalizing, as a check)

Representing carries most of the cognitive load: reading a graph correctly using the grid scale. Procedural fluency then turns the rise and run into a simplified slope.

### Answer 2: major practice

**Major practice: Representing**

Why Representing rather than Procedural Fluency:

- **Most of the work is reading the graph.** The student has to find graph D, use the scale (1 square = 1 unit) to pick two exact points on the line, and turn the picture into a signed rise and run. Once those numbers are right, the answer is nearly done.
- **The calculation is short and routine.** Rise ÷ run is a single division, plus simplifying the fraction. That takes procedural fluency, but very little of it.
- **Most errors come from reading the graph.** Students misread a coordinate, count squares wrong, miss that the line falls (so the slope is negative), or invert rise and run because they don't see what slope means on a graph. These are representation errors, not computation errors.
- **The problem is built around a graph.** It gives a grid and its scale and asks for a property of the line, so it tests moving from a graph to a number.

Procedural Fluency is a clear second: it is needed to finish the problem, but it isn't what the problem is mainly testing.

