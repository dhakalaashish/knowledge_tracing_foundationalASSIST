# Claude vs qwen35_122b_noex: practice labels on rows 1–300

Claude: `claude_top_practice` and `claude_ordering` (Data/problems_300.csv, extracted from Claude's answer 1). qwen35_122b_noex: `qwen35_122b_noex_top_practice` and the order of `practices_used` in `qwen35_122b_noex_reasoning`. Made by `Code/generate_practice_reasoning/tools/compare_labels.js`. Row-by-row differences: [claude_vs_qwen35_122b_noex_differences.md](claude_vs_qwen35_122b_noex_differences.md).

## Headline

| Measure | Same | Different | Agreement | Cohen's κ |
|---|---:|---:|---:|---:|
| Top practice | 200 | 100 | 66.7% | 0.481 (moderate) |
| First practice in the ordering | 147 | 153 | 49.0% | 0.237 (fair) |
| Whole ordering (exact) | 53 | 247 | 17.7% | – |
| Top practice **and** ordering | 44 | 256 | 14.7% | – |

κ for the top practice: observed agreement 0.667, chance agreement 0.357 (from each labeler's own practice frequencies), κ = (p_o − p_e)/(1 − p_e). Chance agreement is high because both labelers pick Procedural Fluency and Representing most of the time, so κ is much lower than the raw agreement.

## Top practice: how often each is chosen

| Practice | Claude | qwen35_122b_noex | predicted_practice | |
|---|---:|---:|---:|---|
| Representing | 79 | 57 | 24 | `C ██████████          `<br>`q ███████             ` |
| Abstracting and Generalizing | 36 | 17 | 8 | `C ████                `<br>`q ██                  ` |
| Justifying and Proving | 2 | 2 | 3 | `C                     `<br>`q                     ` |
| Mathematical Modeling | 22 | 65 | 3 | `C ███                 `<br>`q ████████            ` |
| Collaborative Mathematics | 0 | 0 | 0 | `C                     `<br>`q                     ` |
| Procedural Fluency | 161 | 159 | 262 | `C ████████████████████`<br>`q ████████████████████` |

## Top practice: confusion matrix (rows = Claude, columns = qwen35_122b_noex)

| Claude ↓ / qwen35_122b_noex → | REP | A&G | J&P | MOD | COL | PF | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Representing | **38** | 2 | 1 | 20 | · | 18 | 79 |
| Abstracting and Generalizing | 4 | **15** | · | 7 | · | 10 | 36 |
| Justifying and Proving | · | · | **1** | 1 | · | · | 2 |
| Mathematical Modeling | 5 | · | · | **16** | · | 1 | 22 |
| Collaborative Mathematics | · | · | · | · | **0** | · | 0 |
| Procedural Fluency | 10 | · | · | 21 | · | **130** | 161 |
| **Total** | 57 | 17 | 2 | 65 | 0 | 159 | 300 |

Abbreviations: REP = Representing, A&G = Abstracting and Generalizing, J&P = Justifying and Proving, MOD = Mathematical Modeling, COL = Collaborative Mathematics, PF = Procedural Fluency.

Most common disagreements (Claude → qwen35_122b_noex):

- Procedural Fluency → Mathematical Modeling: 21
- Representing → Mathematical Modeling: 20
- Representing → Procedural Fluency: 18
- Procedural Fluency → Representing: 10
- Abstracting and Generalizing → Procedural Fluency: 10
- Abstracting and Generalizing → Mathematical Modeling: 7
- Mathematical Modeling → Representing: 5
- Abstracting and Generalizing → Representing: 4

## Per-practice agreement on the top practice

Each practice as a yes/no question ("is this the top practice?").

| Practice | Both yes | Only Claude | Only qwen35_122b_noex | Both no | κ (yes/no) |
|---|---:|---:|---:|---:|---:|
| Representing | 38 | 41 | 19 | 202 | 0.434 |
| Abstracting and Generalizing | 15 | 21 | 2 | 262 | 0.530 |
| Justifying and Proving | 1 | 1 | 1 | 297 | 0.497 |
| Mathematical Modeling | 16 | 6 | 49 | 229 | 0.290 |
| Collaborative Mathematics | 0 | 0 | 0 | 300 | – |
| Procedural Fluency | 130 | 31 | 29 | 110 | 0.598 |

## Orderings

| Relation between the two orderings | Rows | Share |
|---|---:|---:|
| Identical | 53 | 17.7% |
| Same practices, different order | 4 | 1.3% |
| qwen35_122b_noex adds practices to Claude's | 8 | 2.7% |
| qwen35_122b_noex drops practices from Claude's | 202 | 67.3% |
| Each has a practice the other lacks | 33 | 11.0% |

- Mean Jaccard overlap of the practice sets: **0.623** (1 = same practices).
- Where both use two or more of the same practices, those pairs are in the same relative order **189 of 198** times (95.5%).

### Number of practices in the ordering

| Practices | Claude | qwen35_122b_noex |
|---:|---:|---:|
| 1 | 15 | 110 |
| 2 | 147 | 161 |
| 3 | 110 | 28 |
| 4 | 24 | 1 |
| 5 | 4 | 0 |
| 6 | 0 | 0 |
| **mean** | 2.52 | 1.73 |

### How often each practice appears in the ordering (any position)

Per-practice κ: does each labeler say the practice is used at all?

| Practice | Claude | qwen35_122b_noex | Both | Only Claude | Only qwen35_122b_noex | κ (used or not) |
|---|---:|---:|---:|---:|---:|---:|
| Representing | 278 | 121 | 119 | 159 | 2 | 0.079 |
| Abstracting and Generalizing | 88 | 19 | 18 | 70 | 1 | 0.259 |
| Justifying and Proving | 25 | 4 | 3 | 22 | 1 | 0.188 |
| Mathematical Modeling | 67 | 79 | 47 | 20 | 32 | 0.530 |
| Collaborative Mathematics | 1 | 4 | 1 | 0 | 3 | 0.397 |
| Procedural Fluency | 296 | 293 | 290 | 6 | 3 | 0.168 |

### Which practice comes first

| Practice | Claude | qwen35_122b_noex |
|---|---:|---:|
| Representing | 218 | 114 |
| Abstracting and Generalizing | 16 | 5 |
| Justifying and Proving | 0 | 1 |
| Mathematical Modeling | 52 | 67 |
| Collaborative Mathematics | 1 | 4 |
| Procedural Fluency | 13 | 109 |

### Where the top practice sits in the labeler's own ordering

| Position of the top practice | Claude | qwen35_122b_noex |
|---|---:|---:|
| step 1 | 109 | 227 |
| step 2 | 150 | 68 |
| step 3 | 40 | 5 |
| step 4 | 1 | 0 |

## Agreement with the existing predicted_practice

| Top practice vs predicted_practice | Same | Agreement | Cohen's κ |
|---|---:|---:|---:|
| Claude | 187 | 62.3% | 0.256 |
| qwen35_122b_noex | 169 | 56.3% | 0.157 |

## Agreement by row block

| Rows | Top practice same | Ordering same |
|---|---:|---:|
| 1–50 | 32 / 50 | 10 / 50 |
| 51–100 | 35 / 50 | 14 / 50 |
| 101–150 | 33 / 50 | 4 / 50 |
| 151–200 | 41 / 50 | 7 / 50 |
| 201–250 | 26 / 50 | 6 / 50 |
| 251–300 | 33 / 50 | 12 / 50 |
