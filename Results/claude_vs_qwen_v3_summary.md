# Claude vs Qwen_v3: practice labels on rows 1–300

Claude: `claude_top_practice` and `claude_ordering` (Data/problems_300.csv, extracted from Claude's answer 1). Qwen_v3: `qwen3_30b_v3_top_practice` and the order of `practices_used` in `qwen3_30b_v3_reasoning`. Made by `Code/generate_practice_reasoning/tools/compare_labels.js`. Row-by-row differences: [claude_vs_qwen_v3_differences.md](claude_vs_qwen_v3_differences.md).

## Headline

| Measure | Same | Different | Agreement | Cohen's κ |
|---|---:|---:|---:|---:|
| Top practice | 188 | 112 | 62.7% | 0.364 (fair) |
| First practice in the ordering | 216 | 84 | 72.0% | 0.109 (slight) |
| Whole ordering (exact) | 131 | 169 | 43.7% | – |
| Top practice **and** ordering | 107 | 193 | 35.7% | – |

κ for the top practice: observed agreement 0.627, chance agreement 0.413 (from each labeler's own practice frequencies), κ = (p_o − p_e)/(1 − p_e). Chance agreement is high because both labelers pick Procedural Fluency and Representing most of the time, so κ is much lower than the raw agreement.

## Top practice: how often each is chosen

| Practice | Claude | Qwen_v3 | predicted_practice | |
|---|---:|---:|---:|---|
| Representing | 79 | 73 | 24 | `C ████████            `<br>`Q ████████            ` |
| Abstracting and Generalizing | 36 | 20 | 8 | `C ████                `<br>`Q ██                  ` |
| Justifying and Proving | 2 | 15 | 3 | `C                     `<br>`Q ██                  ` |
| Mathematical Modeling | 22 | 2 | 3 | `C ██                  `<br>`Q                     ` |
| Collaborative Mathematics | 0 | 0 | 0 | `C                     `<br>`Q                     ` |
| Procedural Fluency | 161 | 190 | 262 | `C █████████████████   `<br>`Q ████████████████████` |

## Top practice: confusion matrix (rows = Claude, columns = Qwen_v3)

| Claude ↓ / Qwen_v3 → | REP | A&G | J&P | MOD | COL | PF | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Representing | **36** | 4 | 3 | · | · | 36 | 79 |
| Abstracting and Generalizing | 8 | **13** | 5 | · | · | 10 | 36 |
| Justifying and Proving | · | 1 | **1** | · | · | · | 2 |
| Mathematical Modeling | 9 | 1 | 2 | **2** | · | 8 | 22 |
| Collaborative Mathematics | · | · | · | · | **0** | · | 0 |
| Procedural Fluency | 20 | 1 | 4 | · | · | **136** | 161 |
| **Total** | 73 | 20 | 15 | 2 | 0 | 190 | 300 |

Abbreviations: REP = Representing, A&G = Abstracting and Generalizing, J&P = Justifying and Proving, MOD = Mathematical Modeling, COL = Collaborative Mathematics, PF = Procedural Fluency.

Most common disagreements (Claude → Qwen_v3):

- Representing → Procedural Fluency: 36
- Procedural Fluency → Representing: 20
- Abstracting and Generalizing → Procedural Fluency: 10
- Mathematical Modeling → Representing: 9
- Abstracting and Generalizing → Representing: 8
- Mathematical Modeling → Procedural Fluency: 8
- Abstracting and Generalizing → Justifying and Proving: 5
- Representing → Abstracting and Generalizing: 4

## Per-practice agreement on the top practice

Each practice as a yes/no question ("is this the top practice?").

| Practice | Both yes | Only Claude | Only Qwen_v3 | Both no | κ (yes/no) |
|---|---:|---:|---:|---:|---:|
| Representing | 36 | 43 | 37 | 184 | 0.295 |
| Abstracting and Generalizing | 13 | 23 | 7 | 257 | 0.414 |
| Justifying and Proving | 1 | 1 | 14 | 284 | 0.107 |
| Mathematical Modeling | 2 | 20 | 0 | 278 | 0.156 |
| Collaborative Mathematics | 0 | 0 | 0 | 300 | – |
| Procedural Fluency | 136 | 25 | 54 | 85 | 0.463 |

## Orderings

| Relation between the two orderings | Rows | Share |
|---|---:|---:|
| Identical | 131 | 43.7% |
| Same practices, different order | 1 | 0.3% |
| Qwen_v3 adds practices to Claude's | 18 | 6.0% |
| Qwen_v3 drops practices from Claude's | 120 | 40.0% |
| Each has a practice the other lacks | 30 | 10.0% |

- Mean Jaccard overlap of the practice sets: **0.768** (1 = same practices).
- Where both use two or more of the same practices, those pairs are in the same relative order **279 of 290** times (96.2%).

### Number of practices in the ordering

| Practices | Claude | Qwen_v3 |
|---:|---:|---:|
| 1 | 15 | 3 |
| 2 | 147 | 268 |
| 3 | 110 | 29 |
| 4 | 24 | 0 |
| 5 | 4 | 0 |
| 6 | 0 | 0 |
| **mean** | 2.52 | 2.09 |

### How often each practice appears in the ordering (any position)

Per-practice κ: does each labeler say the practice is used at all?

| Practice | Claude | Qwen_v3 | Both | Only Claude | Only Qwen_v3 | κ (used or not) |
|---|---:|---:|---:|---:|---:|---:|
| Representing | 278 | 287 | 269 | 9 | 18 | 0.184 |
| Abstracting and Generalizing | 88 | 25 | 19 | 69 | 6 | 0.237 |
| Justifying and Proving | 25 | 29 | 8 | 17 | 21 | 0.227 |
| Mathematical Modeling | 67 | 2 | 2 | 65 | 0 | 0.046 |
| Collaborative Mathematics | 1 | 0 | 0 | 1 | 0 | 0.000 |
| Procedural Fluency | 296 | 283 | 279 | 17 | 4 | -0.022 |

### Which practice comes first

| Practice | Claude | Qwen_v3 |
|---|---:|---:|
| Representing | 218 | 282 |
| Abstracting and Generalizing | 16 | 0 |
| Justifying and Proving | 0 | 3 |
| Mathematical Modeling | 52 | 1 |
| Collaborative Mathematics | 1 | 0 |
| Procedural Fluency | 13 | 14 |

### Where the top practice sits in the labeler's own ordering

| Position of the top practice | Claude | Qwen_v3 |
|---|---:|---:|
| step 1 | 109 | 86 |
| step 2 | 150 | 208 |
| step 3 | 40 | 6 |
| step 4 | 1 | 0 |

## Agreement with the existing predicted_practice

| Top practice vs predicted_practice | Same | Agreement | Cohen's κ |
|---|---:|---:|---:|
| Claude | 187 | 62.3% | 0.256 |
| Qwen_v3 | 196 | 65.3% | 0.184 |

## Agreement by row block

| Rows | Top practice same | Ordering same |
|---|---:|---:|
| 1–50 | 35 / 50 | 23 / 50 |
| 51–100 | 36 / 50 | 24 / 50 |
| 101–150 | 35 / 50 | 24 / 50 |
| 151–200 | 31 / 50 | 23 / 50 |
| 201–250 | 20 / 50 | 13 / 50 |
| 251–300 | 31 / 50 | 24 / 50 |
