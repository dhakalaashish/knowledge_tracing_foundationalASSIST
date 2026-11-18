# Claude vs qwen35_122b: practice labels on rows 1–300

Claude: `claude_top_practice` and `claude_ordering` (Data/problems_300.csv, extracted from Claude's answer 1). qwen35_122b: `qwen35_122b_top_practice` and the order of `practices_used` in `qwen35_122b_reasoning`. Made by `Code/generate_practice_reasoning/tools/compare_labels.js`. Row-by-row differences: [claude_vs_qwen35_122b_differences.md](claude_vs_qwen35_122b_differences.md).

## Headline

| Measure | Same | Different | Agreement | Cohen's κ |
|---|---:|---:|---:|---:|
| Top practice | 211 | 89 | 70.3% | 0.528 (moderate) |
| First practice in the ordering | 132 | 168 | 44.0% | 0.157 (slight) |
| Whole ordering (exact) | 62 | 238 | 20.7% | – |
| Top practice **and** ordering | 49 | 251 | 16.3% | – |

κ for the top practice: observed agreement 0.703, chance agreement 0.371 (from each labeler's own practice frequencies), κ = (p_o − p_e)/(1 − p_e). Chance agreement is high because both labelers pick Procedural Fluency and Representing most of the time, so κ is much lower than the raw agreement.

## Top practice: how often each is chosen

| Practice | Claude | qwen35_122b | predicted_practice | |
|---|---:|---:|---:|---|
| Representing | 79 | 74 | 24 | `C ██████████          `<br>`q █████████           ` |
| Abstracting and Generalizing | 36 | 19 | 8 | `C ████                `<br>`q ██                  ` |
| Justifying and Proving | 2 | 3 | 3 | `C                     `<br>`q                     ` |
| Mathematical Modeling | 22 | 43 | 3 | `C ███                 `<br>`q █████               ` |
| Collaborative Mathematics | 0 | 0 | 0 | `C                     `<br>`q                     ` |
| Procedural Fluency | 161 | 161 | 262 | `C ████████████████████`<br>`q ████████████████████` |

## Top practice: confusion matrix (rows = Claude, columns = qwen35_122b)

| Claude ↓ / qwen35_122b → | REP | A&G | J&P | MOD | COL | PF | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Representing | **49** | 4 | 1 | 11 | · | 14 | 79 |
| Abstracting and Generalizing | 4 | **13** | · | 5 | · | 14 | 36 |
| Justifying and Proving | · | · | **1** | 1 | · | · | 2 |
| Mathematical Modeling | 7 | · | · | **15** | · | · | 22 |
| Collaborative Mathematics | · | · | · | · | **0** | · | 0 |
| Procedural Fluency | 14 | 2 | 1 | 11 | · | **133** | 161 |
| **Total** | 74 | 19 | 3 | 43 | 0 | 161 | 300 |

Abbreviations: REP = Representing, A&G = Abstracting and Generalizing, J&P = Justifying and Proving, MOD = Mathematical Modeling, COL = Collaborative Mathematics, PF = Procedural Fluency.

Most common disagreements (Claude → qwen35_122b):

- Abstracting and Generalizing → Procedural Fluency: 14
- Procedural Fluency → Representing: 14
- Representing → Procedural Fluency: 14
- Procedural Fluency → Mathematical Modeling: 11
- Representing → Mathematical Modeling: 11
- Mathematical Modeling → Representing: 7
- Abstracting and Generalizing → Mathematical Modeling: 5
- Abstracting and Generalizing → Representing: 4

## Per-practice agreement on the top practice

Each practice as a yes/no question ("is this the top practice?").

| Practice | Both yes | Only Claude | Only qwen35_122b | Both no | κ (yes/no) |
|---|---:|---:|---:|---:|---:|
| Representing | 49 | 30 | 25 | 196 | 0.518 |
| Abstracting and Generalizing | 13 | 23 | 6 | 258 | 0.425 |
| Justifying and Proving | 1 | 1 | 2 | 296 | 0.395 |
| Mathematical Modeling | 15 | 7 | 28 | 250 | 0.404 |
| Collaborative Mathematics | 0 | 0 | 0 | 300 | – |
| Procedural Fluency | 133 | 28 | 28 | 111 | 0.625 |

## Orderings

| Relation between the two orderings | Rows | Share |
|---|---:|---:|
| Identical | 62 | 20.7% |
| Same practices, different order | 2 | 0.7% |
| qwen35_122b adds practices to Claude's | 5 | 1.7% |
| qwen35_122b drops practices from Claude's | 212 | 70.7% |
| Each has a practice the other lacks | 19 | 6.3% |

- Mean Jaccard overlap of the practice sets: **0.624** (1 = same practices).
- Where both use two or more of the same practices, those pairs are in the same relative order **170 of 178** times (95.5%).

### Number of practices in the ordering

| Practices | Claude | qwen35_122b |
|---:|---:|---:|
| 1 | 15 | 132 |
| 2 | 147 | 149 |
| 3 | 110 | 18 |
| 4 | 24 | 1 |
| 5 | 4 | 0 |
| 6 | 0 | 0 |
| **mean** | 2.52 | 1.63 |

### How often each practice appears in the ordering (any position)

Per-practice κ: does each labeler say the practice is used at all?

| Practice | Claude | qwen35_122b | Both | Only Claude | Only qwen35_122b | κ (used or not) |
|---|---:|---:|---:|---:|---:|---:|
| Representing | 278 | 123 | 123 | 155 | 0 | 0.104 |
| Abstracting and Generalizing | 88 | 19 | 15 | 73 | 4 | 0.197 |
| Justifying and Proving | 25 | 5 | 4 | 21 | 1 | 0.246 |
| Mathematical Modeling | 67 | 50 | 34 | 33 | 16 | 0.482 |
| Collaborative Mathematics | 1 | 0 | 0 | 1 | 0 | 0.000 |
| Procedural Fluency | 296 | 291 | 288 | 8 | 3 | 0.138 |

### Which practice comes first

| Practice | Claude | qwen35_122b |
|---|---:|---:|
| Representing | 218 | 120 |
| Abstracting and Generalizing | 16 | 7 |
| Justifying and Proving | 0 | 1 |
| Mathematical Modeling | 52 | 44 |
| Collaborative Mathematics | 1 | 0 |
| Procedural Fluency | 13 | 128 |

### Where the top practice sits in the labeler's own ordering

| Position of the top practice | Claude | qwen35_122b |
|---|---:|---:|
| step 1 | 109 | 245 |
| step 2 | 150 | 53 |
| step 3 | 40 | 2 |
| step 4 | 1 | 0 |

## Agreement with the existing predicted_practice

| Top practice vs predicted_practice | Same | Agreement | Cohen's κ |
|---|---:|---:|---:|
| Claude | 187 | 62.3% | 0.256 |
| qwen35_122b | 175 | 58.3% | 0.180 |

## Agreement by row block

| Rows | Top practice same | Ordering same |
|---|---:|---:|
| 1–50 | 38 / 50 | 15 / 50 |
| 51–100 | 34 / 50 | 17 / 50 |
| 101–150 | 31 / 50 | 3 / 50 |
| 151–200 | 43 / 50 | 6 / 50 |
| 201–250 | 26 / 50 | 8 / 50 |
| 251–300 | 39 / 50 | 13 / 50 |
