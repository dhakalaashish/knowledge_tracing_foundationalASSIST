# Claude vs Qwen_v4: practice labels on rows 1–300

Claude: `claude_top_practice` and `claude_ordering` (Data/problems_300.csv, extracted from Claude's answer 1). Qwen_v4: `qwen3_30b_v4_top_practice` and the order of `practices_used` in `qwen3_30b_v4_reasoning`. Made by `Code/generate_practice_reasoning/tools/compare_labels.js`. Row-by-row differences: [claude_vs_qwen_v4_differences.md](claude_vs_qwen_v4_differences.md).

## Headline

| Measure | Same | Different | Agreement | Cohen's κ |
|---|---:|---:|---:|---:|
| Top practice | 189 | 111 | 63.0% | 0.333 (fair) |
| First practice in the ordering | 217 | 83 | 72.3% | 0.058 (slight) |
| Whole ordering (exact) | 131 | 169 | 43.7% | – |
| Top practice **and** ordering | 100 | 200 | 33.3% | – |

κ for the top practice: observed agreement 0.630, chance agreement 0.445 (from each labeler's own practice frequencies), κ = (p_o − p_e)/(1 − p_e). Chance agreement is high because both labelers pick Procedural Fluency and Representing most of the time, so κ is much lower than the raw agreement.

## Top practice: how often each is chosen

| Practice | Claude | Qwen_v4 | predicted_practice | |
|---|---:|---:|---:|---|
| Representing | 79 | 48 | 24 | `C ███████             `<br>`Q ████                ` |
| Abstracting and Generalizing | 36 | 22 | 8 | `C ███                 `<br>`Q ██                  ` |
| Justifying and Proving | 2 | 9 | 3 | `C                     `<br>`Q █                   ` |
| Mathematical Modeling | 22 | 1 | 3 | `C ██                  `<br>`Q                     ` |
| Collaborative Mathematics | 0 | 0 | 0 | `C                     `<br>`Q                     ` |
| Procedural Fluency | 161 | 220 | 262 | `C ███████████████     `<br>`Q ████████████████████` |

## Top practice: confusion matrix (rows = Claude, columns = Qwen_v4)

| Claude ↓ / Qwen_v4 → | REP | A&G | J&P | MOD | COL | PF | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Representing | **24** | 5 | 2 | · | · | 48 | 79 |
| Abstracting and Generalizing | 5 | **15** | 3 | · | · | 13 | 36 |
| Justifying and Proving | · | 1 | **1** | · | · | · | 2 |
| Mathematical Modeling | 9 | · | 1 | **1** | · | 11 | 22 |
| Collaborative Mathematics | · | · | · | · | **0** | · | 0 |
| Procedural Fluency | 10 | 1 | 2 | · | · | **148** | 161 |
| **Total** | 48 | 22 | 9 | 1 | 0 | 220 | 300 |

Abbreviations: REP = Representing, A&G = Abstracting and Generalizing, J&P = Justifying and Proving, MOD = Mathematical Modeling, COL = Collaborative Mathematics, PF = Procedural Fluency.

Most common disagreements (Claude → Qwen_v4):

- Representing → Procedural Fluency: 48
- Abstracting and Generalizing → Procedural Fluency: 13
- Mathematical Modeling → Procedural Fluency: 11
- Procedural Fluency → Representing: 10
- Mathematical Modeling → Representing: 9
- Representing → Abstracting and Generalizing: 5
- Abstracting and Generalizing → Representing: 5
- Abstracting and Generalizing → Justifying and Proving: 3

## Per-practice agreement on the top practice

Each practice as a yes/no question ("is this the top practice?").

| Practice | Both yes | Only Claude | Only Qwen_v4 | Both no | κ (yes/no) |
|---|---:|---:|---:|---:|---:|
| Representing | 24 | 55 | 24 | 197 | 0.223 |
| Abstracting and Generalizing | 15 | 21 | 7 | 257 | 0.469 |
| Justifying and Proving | 1 | 1 | 8 | 290 | 0.173 |
| Mathematical Modeling | 1 | 21 | 0 | 278 | 0.081 |
| Collaborative Mathematics | 0 | 0 | 0 | 300 | – |
| Procedural Fluency | 148 | 13 | 72 | 67 | 0.413 |

## Orderings

| Relation between the two orderings | Rows | Share |
|---|---:|---:|
| Identical | 131 | 43.7% |
| Same practices, different order | 1 | 0.3% |
| Qwen_v4 adds practices to Claude's | 15 | 5.0% |
| Qwen_v4 drops practices from Claude's | 129 | 43.0% |
| Each has a practice the other lacks | 24 | 8.0% |

- Mean Jaccard overlap of the practice sets: **0.759** (1 = same practices).
- Where both use two or more of the same practices, those pairs are in the same relative order **251 of 260** times (96.5%).

### Number of practices in the ordering

| Practices | Claude | Qwen_v4 |
|---:|---:|---:|
| 1 | 15 | 1 |
| 2 | 147 | 299 |
| 3 | 110 | 0 |
| 4 | 24 | 0 |
| 5 | 4 | 0 |
| 6 | 0 | 0 |
| **mean** | 2.52 | 2.00 |

### How often each practice appears in the ordering (any position)

Per-practice κ: does each labeler say the practice is used at all?

| Practice | Claude | Qwen_v4 | Both | Only Claude | Only Qwen_v4 | κ (used or not) |
|---|---:|---:|---:|---:|---:|---:|
| Representing | 278 | 293 | 273 | 5 | 20 | 0.106 |
| Abstracting and Generalizing | 88 | 30 | 24 | 64 | 6 | 0.303 |
| Justifying and Proving | 25 | 13 | 3 | 22 | 10 | 0.107 |
| Mathematical Modeling | 67 | 1 | 1 | 66 | 0 | 0.023 |
| Collaborative Mathematics | 1 | 0 | 0 | 1 | 0 | 0.000 |
| Procedural Fluency | 296 | 262 | 259 | 37 | 3 | 0.024 |

### Which practice comes first

| Practice | Claude | Qwen_v4 |
|---|---:|---:|
| Representing | 218 | 291 |
| Abstracting and Generalizing | 16 | 1 |
| Justifying and Proving | 0 | 2 |
| Mathematical Modeling | 52 | 1 |
| Collaborative Mathematics | 1 | 0 |
| Procedural Fluency | 13 | 5 |

### Where the top practice sits in the labeler's own ordering

| Position of the top practice | Claude | Qwen_v4 |
|---|---:|---:|
| step 1 | 109 | 57 |
| step 2 | 150 | 243 |
| step 3 | 40 | 0 |
| step 4 | 1 | 0 |

## Agreement with the existing predicted_practice

| Top practice vs predicted_practice | Same | Agreement | Cohen's κ |
|---|---:|---:|---:|
| Claude | 187 | 62.3% | 0.256 |
| Qwen_v4 | 230 | 76.7% | 0.323 |

## Agreement by row block

| Rows | Top practice same | Ordering same |
|---|---:|---:|
| 1–50 | 31 / 50 | 22 / 50 |
| 51–100 | 36 / 50 | 26 / 50 |
| 101–150 | 35 / 50 | 24 / 50 |
| 151–200 | 33 / 50 | 22 / 50 |
| 201–250 | 25 / 50 | 15 / 50 |
| 251–300 | 29 / 50 | 22 / 50 |
