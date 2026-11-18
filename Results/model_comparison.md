# Qwen runs compared with Claude Opus 5.5, with Aashish's reviews, and with each other

Made by `Code/generate_practice_reasoning/tools/compare_models.js`. Claude's labels: `claude_top_practice` and `claude_ordering` (rows 1–300). Each run's ordering is the order of `practices_used` in `<prefix>_reasoning` (answer 1 in the order of answer 2 for the three-prompt runs). v3 prompts = no example items; v4 prompts = with the NAEP example items under each practice's descriptors.

## Against Claude, rows 1–300

| Run | Top practice same | Cohen's κ (top) | Whole ordering same | Same set of practices | First practice same | Mean Jaccard (sets) | Practices per item (Claude: CL) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen3 30B, v3 prompts (no examples) | 188/300 (62.7%) | 0.364 | 131 (43.7%) | 132 (44.0%) | 216 (72.0%) | 0.77 | 2.09 |
| Qwen3 30B, v4 prompts (with examples) | 189/300 (63.0%) | 0.333 | 131 (43.7%) | 132 (44.0%) | 217 (72.3%) | 0.76 | 2.00 |
| Qwen3.5 122B, v3 prompts (no examples) | 200/300 (66.7%) | 0.481 | 53 (17.7%) | 57 (19.0%) | 147 (49.0%) | 0.62 | 1.73 |
| Qwen3.5 122B, v4 prompts (with examples) | 211/300 (70.3%) | 0.528 | 62 (20.7%) | 64 (21.3%) | 132 (44.0%) | 0.62 | 1.63 |
| Qwen3.5 122B, v4 prompts + NAEP Chapter 3 | 207/300 (69.0%) | 0.480 | 63 (21.0%) | 68 (22.7%) | 132 (44.0%) | 0.64 | 1.60 |

Claude uses 2.52 practices per item on average (CL).

## Top practice chosen, rows 1–300

| Practice | Claude | qwen3_30b_v3 | qwen3_30b_v4 | qwen35_122b_noex | qwen35_122b | qwen35_122b_ch3 |
|---|---:|---:|---:|---:|---:|---:|
| Representing | 79 | 73 | 48 | 57 | 74 | 96 |
| Abstracting and Generalizing | 36 | 20 | 22 | 17 | 19 | 14 |
| Justifying and Proving | 2 | 15 | 9 | 2 | 3 | 1 |
| Mathematical Modeling | 22 | 2 | 1 | 65 | 43 | 16 |
| Collaborative Mathematics | 0 | 0 | 0 | 0 | 0 | 0 |
| Procedural Fluency | 161 | 190 | 220 | 159 | 161 | 173 |

## How often each practice is listed as used, rows 1–300

| Practice | Claude | qwen3_30b_v3 | qwen3_30b_v4 | qwen35_122b_noex | qwen35_122b | qwen35_122b_ch3 |
|---|---:|---:|---:|---:|---:|---:|
| Representing | 278 | 287 | 293 | 121 | 123 | 149 |
| Abstracting and Generalizing | 88 | 25 | 30 | 19 | 19 | 16 |
| Justifying and Proving | 25 | 29 | 13 | 4 | 5 | 3 |
| Mathematical Modeling | 67 | 2 | 1 | 79 | 50 | 16 |
| Collaborative Mathematics | 1 | 0 | 0 | 4 | 0 | 0 |
| Procedural Fluency | 296 | 283 | 262 | 293 | 291 | 296 |

## Orderings with Representing left out, rows 1–300

The 122B runs often list only Procedural Fluency where Claude lists Representing > Procedural Fluency (reading the item's representation as a step). This table compares the orderings with Representing removed from both sides.

| Run | Whole ordering same | Same with Representing left out | Differ only because Claude adds Representing | Ordering is just Procedural Fluency (Claude: 13) |
|---|---:|---:|---:|---:|
| Qwen3 30B, v3 prompts (no examples) | 131 (43.7%) | 143 (47.7%) | 2 | 3 |
| Qwen3 30B, v4 prompts (with examples) | 131 (43.7%) | 146 (48.7%) | 2 | 1 |
| Qwen3.5 122B, v3 prompts (no examples) | 53 (17.7%) | 166 (55.3%) | 110 | 107 |
| Qwen3.5 122B, v4 prompts (with examples) | 62 (20.7%) | 172 (57.3%) | 108 | 125 |
| Qwen3.5 122B, v4 prompts + NAEP Chapter 3 | 63 (21.0%) | 157 (52.3%) | 92 | 132 |

## Against Aashish's reviews (16 rows: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 127)

Too few rows for percentages to mean much; the counts are here so they can grow as more rows are reviewed.

| Labeler | Top practice same | Whole ordering same |
|---|---:|---:|
| Claude Opus 5.5 | 14/16 | 6/16 |
| Qwen3 30B, v3 prompts (no examples) | 12/16 | 5/16 |
| Qwen3 30B, v4 prompts (with examples) | 12/16 | 4/16 |
| Qwen3.5 122B, v3 prompts (no examples) | 12/16 | 12/16 |
| Qwen3.5 122B, v4 prompts (with examples) | 14/16 | 13/16 |
| Qwen3.5 122B, v4 prompts + NAEP Chapter 3 | 13/16 | 13/16 |

## Runs against each other, all 3395 problems

| Comparison | What changes | Top practice same | Cohen's κ (top) | Whole ordering same | Mean Jaccard (sets) |
|---|---|---:|---:|---:|---:|
| qwen3_30b_v3 vs qwen35_122b_noex | model (30B → 122B), v3 prompts | 1495/3395 (44.0%) | 0.256 | 936 (27.6%) | 0.59 |
| qwen3_30b_v4 vs qwen35_122b | model (30B → 122B), v4 prompts | 1728/3394 (50.9%) | 0.294 | 1171 (34.5%) | 0.62 |
| qwen3_30b_v3 vs qwen3_30b_v4 | examples added, 30B | 2401/3395 (70.7%) | 0.550 | 2507 (73.8%) | 0.88 |
| qwen35_122b_noex vs qwen35_122b | examples added, 122B | 2353/3395 (69.3%) | 0.575 | 1995 (58.8%) | 0.78 |
| qwen35_122b vs qwen35_122b_ch3 | NAEP Chapter 3 added, 122B | 2327/3395 (68.5%) | 0.538 | 2161 (63.7%) | 0.81 |

## Top practice chosen, all 3395 problems

| Practice | qwen3_30b_v3 | qwen3_30b_v4 | qwen35_122b_noex | qwen35_122b | qwen35_122b_ch3 |
|---|---:|---:|---:|---:|---:|
| Representing | 849 (25.0%) | 624 (18.4%) | 774 (22.8%) | 1031 (30.4%) | 1229 (36.2%) |
| Abstracting and Generalizing | 229 (6.7%) | 284 (8.4%) | 290 (8.5%) | 233 (6.9%) | 243 (7.2%) |
| Justifying and Proving | 712 (21.0%) | 567 (16.7%) | 123 (3.6%) | 141 (4.2%) | 134 (3.9%) |
| Mathematical Modeling | 16 (0.5%) | 12 (0.4%) | 899 (26.5%) | 559 (16.5%) | 211 (6.2%) |
| Collaborative Mathematics | 1 (0.0%) | 0 (0.0%) | 33 (1.0%) | 8 (0.2%) | 25 (0.7%) |
| Procedural Fluency | 1588 (46.8%) | 1907 (56.2%) | 1276 (37.6%) | 1423 (41.9%) | 1553 (45.7%) |
| (no answer) | 0 | 1 | 0 | 0 | 0 |

## How often each practice is listed as used, all 3395 problems

| Practice | qwen3_30b_v3 | qwen3_30b_v4 | qwen35_122b_noex | qwen35_122b | qwen35_122b_ch3 |
|---|---:|---:|---:|---:|---:|
| Representing | 3145 (92.6%) | 3219 (94.8%) | 1848 (54.4%) | 2014 (59.3%) | 2258 (66.5%) |
| Abstracting and Generalizing | 366 (10.8%) | 348 (10.3%) | 342 (10.1%) | 271 (8.0%) | 288 (8.5%) |
| Justifying and Proving | 1008 (29.7%) | 733 (21.6%) | 327 (9.6%) | 222 (6.5%) | 241 (7.1%) |
| Mathematical Modeling | 25 (0.7%) | 16 (0.5%) | 1086 (32.0%) | 664 (19.6%) | 243 (7.2%) |
| Collaborative Mathematics | 10 (0.3%) | 8 (0.2%) | 122 (3.6%) | 14 (0.4%) | 48 (1.4%) |
| Procedural Fluency | 2799 (82.4%) | 2482 (73.1%) | 3015 (88.8%) | 2984 (87.9%) | 3036 (89.4%) |
| Practices per problem | 2.17 | 2.01 | 1.99 | 1.82 | 1.80 |

