# Claude vs qwen35_122b_ch3: practice labels on rows 1–300

Claude: `claude_top_practice` and `claude_ordering` (Data/problems_300.csv, extracted from Claude's answer 1). qwen35_122b_ch3: `qwen35_122b_ch3_top_practice` and the order of `practices_used` in `qwen35_122b_ch3_reasoning`. Made by `Code/generate_practice_reasoning/tools/compare_labels.js`. Row-by-row differences: [claude_vs_qwen35_122b_ch3_differences.md](claude_vs_qwen35_122b_ch3_differences.md).

## Headline

| Measure | Same | Different | Agreement | Cohen's κ |
|---|---:|---:|---:|---:|
| Top practice | 207 | 93 | 69.0% | 0.480 (moderate) |
| First practice in the ordering | 132 | 168 | 44.0% | 0.095 (slight) |
| Whole ordering (exact) | 63 | 237 | 21.0% | – |
| Top practice **and** ordering | 47 | 253 | 15.7% | – |

κ for the top practice: observed agreement 0.690, chance agreement 0.403 (from each labeler's own practice frequencies), κ = (p_o − p_e)/(1 − p_e). Chance agreement is high because both labelers pick Procedural Fluency and Representing most of the time, so κ is much lower than the raw agreement.

## Top practice: how often each is chosen

| Practice | Claude | qwen35_122b_ch3 | predicted_practice | |
|---|---:|---:|---:|---|
| Representing | 79 | 96 | 24 | `C █████████           `<br>`q ███████████         ` |
| Abstracting and Generalizing | 36 | 14 | 8 | `C ████                `<br>`q ██                  ` |
| Justifying and Proving | 2 | 1 | 3 | `C                     `<br>`q                     ` |
| Mathematical Modeling | 22 | 16 | 3 | `C ███                 `<br>`q ██                  ` |
| Collaborative Mathematics | 0 | 0 | 0 | `C                     `<br>`q                     ` |
| Procedural Fluency | 161 | 173 | 262 | `C ███████████████████ `<br>`q ████████████████████` |

## Top practice: confusion matrix (rows = Claude, columns = qwen35_122b_ch3)

| Claude ↓ / qwen35_122b_ch3 → | REP | A&G | J&P | MOD | COL | PF | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Representing | **54** | 3 | · | 5 | · | 17 | 79 |
| Abstracting and Generalizing | 8 | **9** | · | 1 | · | 18 | 36 |
| Justifying and Proving | · | · | **1** | · | · | 1 | 2 |
| Mathematical Modeling | 12 | · | · | **8** | · | 2 | 22 |
| Collaborative Mathematics | · | · | · | · | **0** | · | 0 |
| Procedural Fluency | 22 | 2 | · | 2 | · | **135** | 161 |
| **Total** | 96 | 14 | 1 | 16 | 0 | 173 | 300 |

Abbreviations: REP = Representing, A&G = Abstracting and Generalizing, J&P = Justifying and Proving, MOD = Mathematical Modeling, COL = Collaborative Mathematics, PF = Procedural Fluency.

Most common disagreements (Claude → qwen35_122b_ch3):

- Procedural Fluency → Representing: 22
- Abstracting and Generalizing → Procedural Fluency: 18
- Representing → Procedural Fluency: 17
- Mathematical Modeling → Representing: 12
- Abstracting and Generalizing → Representing: 8
- Representing → Mathematical Modeling: 5
- Representing → Abstracting and Generalizing: 3
- Procedural Fluency → Abstracting and Generalizing: 2

## Per-practice agreement on the top practice

Each practice as a yes/no question ("is this the top practice?").

| Practice | Both yes | Only Claude | Only qwen35_122b_ch3 | Both no | κ (yes/no) |
|---|---:|---:|---:|---:|---:|
| Representing | 54 | 25 | 42 | 179 | 0.462 |
| Abstracting and Generalizing | 9 | 27 | 5 | 259 | 0.314 |
| Justifying and Proving | 1 | 1 | 0 | 298 | 0.665 |
| Mathematical Modeling | 8 | 14 | 8 | 270 | 0.383 |
| Collaborative Mathematics | 0 | 0 | 0 | 300 | – |
| Procedural Fluency | 135 | 26 | 38 | 101 | 0.568 |

## Orderings

| Relation between the two orderings | Rows | Share |
|---|---:|---:|
| Identical | 63 | 21.0% |
| Same practices, different order | 5 | 1.7% |
| qwen35_122b_ch3 adds practices to Claude's | 4 | 1.3% |
| qwen35_122b_ch3 drops practices from Claude's | 224 | 74.7% |
| Each has a practice the other lacks | 4 | 1.3% |

- Mean Jaccard overlap of the practice sets: **0.641** (1 = same practices).
- Where both use two or more of the same practices, those pairs are in the same relative order **176 of 186** times (94.6%).

### Number of practices in the ordering

| Practices | Claude | qwen35_122b_ch3 |
|---:|---:|---:|
| 1 | 15 | 136 |
| 2 | 147 | 149 |
| 3 | 110 | 14 |
| 4 | 24 | 1 |
| 5 | 4 | 0 |
| 6 | 0 | 0 |
| **mean** | 2.52 | 1.60 |

### How often each practice appears in the ordering (any position)

Per-practice κ: does each labeler say the practice is used at all?

| Practice | Claude | qwen35_122b_ch3 | Both | Only Claude | Only qwen35_122b_ch3 | κ (used or not) |
|---|---:|---:|---:|---:|---:|---:|
| Representing | 278 | 149 | 147 | 131 | 2 | 0.118 |
| Abstracting and Generalizing | 88 | 16 | 14 | 74 | 2 | 0.197 |
| Justifying and Proving | 25 | 3 | 3 | 22 | 0 | 0.200 |
| Mathematical Modeling | 67 | 16 | 15 | 52 | 1 | 0.301 |
| Collaborative Mathematics | 1 | 0 | 0 | 1 | 0 | 0.000 |
| Procedural Fluency | 296 | 296 | 293 | 3 | 3 | 0.240 |

### Which practice comes first

| Practice | Claude | qwen35_122b_ch3 |
|---|---:|---:|
| Representing | 218 | 146 |
| Abstracting and Generalizing | 16 | 5 |
| Justifying and Proving | 0 | 1 |
| Mathematical Modeling | 52 | 13 |
| Collaborative Mathematics | 1 | 0 |
| Procedural Fluency | 13 | 135 |

### Where the top practice sits in the labeler's own ordering

| Position of the top practice | Claude | qwen35_122b_ch3 |
|---|---:|---:|
| step 1 | 109 | 248 |
| step 2 | 150 | 48 |
| step 3 | 40 | 4 |
| step 4 | 1 | 0 |

## Agreement with the existing predicted_practice

| Top practice vs predicted_practice | Same | Agreement | Cohen's κ |
|---|---:|---:|---:|
| Claude | 187 | 62.3% | 0.256 |
| qwen35_122b_ch3 | 186 | 62.0% | 0.190 |

## Agreement by row block

| Rows | Top practice same | Ordering same |
|---|---:|---:|
| 1–50 | 42 / 50 | 16 / 50 |
| 51–100 | 36 / 50 | 14 / 50 |
| 101–150 | 33 / 50 | 5 / 50 |
| 151–200 | 36 / 50 | 6 / 50 |
| 201–250 | 22 / 50 | 8 / 50 |
| 251–300 | 38 / 50 | 14 / 50 |
