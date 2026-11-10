# Claude vs Qwen: practice labels on rows 1–300

Claude: `claude_top_practice` and `claude_ordering` (Data/problems_300.csv, extracted from Claude's answer 1). Qwen: `qwen3_30b_v2_top_practice` and the order of `practices_used` in `qwen3_30b_v2_reasoning`. Made by `Code/generate_practice_reasoning/tools/compare_labels.js`. Row-by-row differences: [claude_vs_qwen_differences.md](claude_vs_qwen_differences.md).

## Headline

| Measure | Same | Different | Agreement | Cohen's κ |
|---|---:|---:|---:|---:|
| Top practice | 192 | 108 | 64.0% | 0.363 (fair) |
| First practice in the ordering | 102 | 198 | 34.0% | 0.014 (slight) |
| Whole ordering (exact) | 38 | 262 | 12.7% | – |
| Top practice **and** ordering | 19 | 281 | 6.3% | – |

κ for the top practice: observed agreement 0.640, chance agreement 0.435 (from each labeler's own practice frequencies), κ = (p_o − p_e)/(1 − p_e). Chance agreement is high because both labelers pick Procedural Fluency and Representing most of the time, so κ is much lower than the raw agreement.

## Top practice: how often each is chosen

| Practice | Claude | Qwen | predicted_practice | |
|---|---:|---:|---:|---|
| Representing | 79 | 61 | 24 | `C ████████            `<br>`Q ██████              ` |
| Abstracting and Generalizing | 36 | 17 | 8 | `C ███                 `<br>`Q ██                  ` |
| Justifying and Proving | 2 | 12 | 3 | `C                     `<br>`Q █                   ` |
| Mathematical Modeling | 22 | 1 | 3 | `C ██                  `<br>`Q                     ` |
| Collaborative Mathematics | 0 | 0 | 0 | `C                     `<br>`Q                     ` |
| Procedural Fluency | 161 | 209 | 262 | `C ███████████████     `<br>`Q ████████████████████` |

## Top practice: confusion matrix (rows = Claude, columns = Qwen)

| Claude ↓ / Qwen → | REP | A&G | J&P | MOD | COL | PF | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Representing | **33** | 3 | 1 | · | · | 42 | 79 |
| Abstracting and Generalizing | 6 | **13** | 3 | · | · | 14 | 36 |
| Justifying and Proving | 1 | · | **1** | · | · | · | 2 |
| Mathematical Modeling | 9 | · | 3 | **1** | · | 9 | 22 |
| Collaborative Mathematics | · | · | · | · | **0** | · | 0 |
| Procedural Fluency | 12 | 1 | 4 | · | · | **144** | 161 |
| **Total** | 61 | 17 | 12 | 1 | 0 | 209 | 300 |

Abbreviations: REP = Representing, A&G = Abstracting and Generalizing, J&P = Justifying and Proving, MOD = Mathematical Modeling, COL = Collaborative Mathematics, PF = Procedural Fluency.

Most common disagreements (Claude → Qwen):

- Representing → Procedural Fluency: 42
- Abstracting and Generalizing → Procedural Fluency: 14
- Procedural Fluency → Representing: 12
- Mathematical Modeling → Representing: 9
- Mathematical Modeling → Procedural Fluency: 9
- Abstracting and Generalizing → Representing: 6
- Procedural Fluency → Justifying and Proving: 4
- Mathematical Modeling → Justifying and Proving: 3

## Per-practice agreement on the top practice

Each practice as a yes/no question ("is this the top practice?").

| Practice | Both yes | Only Claude | Only Qwen | Both no | κ (yes/no) |
|---|---:|---:|---:|---:|---:|
| Representing | 33 | 46 | 28 | 193 | 0.314 |
| Abstracting and Generalizing | 13 | 23 | 4 | 260 | 0.448 |
| Justifying and Proving | 1 | 1 | 11 | 287 | 0.133 |
| Mathematical Modeling | 1 | 21 | 0 | 278 | 0.081 |
| Collaborative Mathematics | 0 | 0 | 0 | 300 | – |
| Procedural Fluency | 144 | 17 | 65 | 74 | 0.437 |

## Orderings

| Relation between the two orderings | Rows | Share |
|---|---:|---:|
| Identical | 38 | 12.7% |
| Same practices, different order | 97 | 32.3% |
| Qwen adds practices to Claude's | 18 | 6.0% |
| Qwen drops practices from Claude's | 124 | 41.3% |
| Each has a practice the other lacks | 23 | 7.7% |

- Mean Jaccard overlap of the practice sets: **0.777** (1 = same practices).
- Where both use two or more of the same practices, those pairs are in the same relative order **148 of 300** times (49.3%).

### Number of practices in the ordering

| Practices | Claude | Qwen |
|---:|---:|---:|
| 1 | 15 | 2 |
| 2 | 147 | 271 |
| 3 | 110 | 26 |
| 4 | 24 | 1 |
| 5 | 4 | 0 |
| 6 | 0 | 0 |
| **mean** | 2.52 | 2.09 |

### How often each practice appears in the ordering (any position)

Per-practice κ: does each labeler say the practice is used at all?

| Practice | Claude | Qwen | Both | Only Claude | Only Qwen | κ (used or not) |
|---|---:|---:|---:|---:|---:|---:|
| Representing | 278 | 288 | 269 | 9 | 19 | 0.132 |
| Abstracting and Generalizing | 88 | 28 | 22 | 66 | 6 | 0.277 |
| Justifying and Proving | 25 | 21 | 8 | 17 | 13 | 0.294 |
| Mathematical Modeling | 67 | 1 | 1 | 66 | 0 | 0.023 |
| Collaborative Mathematics | 1 | 0 | 0 | 1 | 0 | 0.000 |
| Procedural Fluency | 296 | 288 | 284 | 12 | 4 | -0.020 |

### Which practice comes first

| Practice | Claude | Qwen |
|---|---:|---:|
| Representing | 218 | 126 |
| Abstracting and Generalizing | 16 | 0 |
| Justifying and Proving | 0 | 2 |
| Mathematical Modeling | 52 | 1 |
| Collaborative Mathematics | 1 | 0 |
| Procedural Fluency | 13 | 171 |

### Where the top practice sits in the labeler's own ordering

| Position of the top practice | Claude | Qwen |
|---|---:|---:|
| step 1 | 109 | 218 |
| step 2 | 150 | 72 |
| step 3 | 40 | 9 |
| step 4 | 1 | 1 |

## Agreement with the existing predicted_practice

| Top practice vs predicted_practice | Same | Agreement | Cohen's κ |
|---|---:|---:|---:|
| Claude | 187 | 62.3% | 0.256 |
| Qwen | 213 | 71.0% | 0.223 |

## Agreement by row block

| Rows | Top practice same | Ordering same |
|---|---:|---:|
| 1–50 | 38 / 50 | 4 / 50 |
| 51–100 | 37 / 50 | 9 / 50 |
| 101–150 | 36 / 50 | 6 / 50 |
| 151–200 | 31 / 50 | 5 / 50 |
| 201–250 | 22 / 50 | 4 / 50 |
| 251–300 | 28 / 50 | 10 / 50 |
