# Mathematical practices: exploration report

Students: 5,000; attempts: 1,712,991; concept level: domain; labels: all (top practice, ties listed).
Practices in the models (at least 20 problems): Representing, Abstracting, Justifying, Procedural. Struggle = not correct on the first try without help (`discrete_score` 0).

## RQ1: Do students struggle more with practices they meet less often?

### 1. Exposure

| practice | problems | share_of_attempts_pct | students_ever_pct | per_student_median | correct_pct | hint_pct | mc_2_options_pct |
|---|---|---|---|---|---|---|---|
| Representing | 650 | 17.2 | 100.0 | 58.0 | 58.0 | 5.4 | 12.9 |
| Abstracting | 315 | 8.2 | 100.0 | 29.0 | 55.2 | 4.6 | 27.5 |
| Justifying | 57 | 1.8 | 99.8 | 6.0 | 64.3 | 0.7 | 81.6 |
| Modeling | 10 | 0.1 | 28.8 | 0.0 | 70.3 | 1.3 | 24.5 |
| Collaborative | 2 | 0.0 | 1.9 | 0.0 | 50.5 | 10.9 | 0.0 |
| Procedural | 2334 | 72.6 | 100.0 | 246.0 | 62.9 | 5.3 | 8.3 |

### 2. Difficulty on equal footing (gap vs Procedural, percentage points)

Adjusted = average marginal effect from a logistic model with answer format (two-option multiple choice is 50% guessable), grade, domain, time of year (the problem's usual position in the course) and student ability; 95% intervals clustered by student and problem. Raw and adjusted gaps can differ in sign when a practice comes mostly in an easy format (Simpson's paradox).

| outcome | practice | raw_gap_pp | adjusted_gap_pp | adjusted_low | adjusted_high |
|---|---|---|---|---|---|
| correct | Representing | -4.9 | -1.7 | -3.9 | 0.5 |
| correct | Abstracting | -7.7 | -7.6 | -10.1 | -5.1 |
| correct | Justifying | 1.4 | -12.7 | -17.7 | -7.8 |
| hint used | Representing | 0.1 | 0.6 | -0.0 | 1.2 |
| hint used | Abstracting | -0.7 | 2.2 | 1.0 | 3.3 |
| hint used | Justifying | -4.6 | 3.0 | 0.9 | 5.0 |
| answer revealed | Representing | 0.8 | 2.2 | 0.3 | 4.2 |
| answer revealed | Abstracting | 1.4 | 7.2 | 4.7 | 9.7 |
| answer revealed | Justifying | -16.8 | 8.2 | 4.1 | 12.3 |

![gaps](rq1_practice_gaps.png)

### 3. Is it because of rarity?

If rarity caused the struggle, students who had met a practice more often would do better on the *same* problem. `slope` is the effect of log(1 + earlier encounters with the practice) on success, controlling for the problem's difficulty, the student's prior accuracy and their overall progress. It is converted to percentage points for the 1st vs 5th encounter and for the 10th vs 90th percentile of earlier encounters actually seen for that practice (no extrapolation).

| practice | slope | slope_low | slope_high | pp_1st_to_5th_encounter | pp_low | pp_high | encounters_before_p10 | encounters_before_p90 | pp_p10_to_p90 | pp_p10_to_p90_low | pp_p10_to_p90_high |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Representing | 0.018 | -0.014 | 0.050 | 0.552 | -0.423 | 1.522 | 5.000 | 56.000 | 0.769 | -0.593 | 2.105 |
| Abstracting | 0.058 | 0.027 | 0.088 | 1.759 | 0.839 | 2.677 | 2.000 | 36.000 | 2.732 | 1.308 | 4.138 |
| Justifying | -0.009 | -0.071 | 0.053 | -0.266 | -2.142 | 1.572 | 0.000 | 7.000 | -0.344 | -2.776 | 2.025 |
| Procedural | 0.017 | -0.005 | 0.039 | 0.497 | -0.160 | 1.150 | 24.000 | 228.000 | 0.677 | -0.221 | 1.543 |
| (any problem: general progress) | -0.043 | -0.065 | -0.021 |  |  |  |  |  |  |  |  |

![curves](rq1_learning_curves.png)

### Answer to RQ1

- **Representing** (17.2% of attempts): adjusted gap -1.7 pp (95% CI -3.9 to +0.5). **Not clearly harder** than Procedural, although it is met less often (+0.8 pp going from 5 to 56 earlier encounters, the 10th to 90th percentile).
- **Abstracting** (8.2% of attempts): adjusted gap -7.6 pp (95% CI -10.1 to -5.1). Harder, and **rarity explains only part of it** (at most about 36%): more encounters help (+2.7 pp going from 2 to 36 earlier encounters, the 10th to 90th percentile), less than the 7.6 pp gap.
- **Justifying** (1.8% of attempts): adjusted gap -12.7 pp (95% CI -17.7 to -7.8). Harder, and **not because of rarity**: on the same problem, students who had met this practice more often did not do better (-0.3 pp going from 0 to 7 earlier encounters, the 10th to 90th percentile; slope CI includes 0).

## RQ2: Does mastery of a practice transfer across concepts?

Earlier attempts are split into A same practice + same concept, B same practice + other concept, C other practice + same concept, D other practice + other concept, E earlier part of the same problem.

### 1. All attempts (log-odds per logit of smoothed accuracy)

| model | term | estimate | low | high |
|---|---|---|---|---|
| all attempts | accuracy A: same practice, same concept | 0.389 | 0.374 | 0.404 |
| all attempts | accuracy B: same practice, other concept | 0.269 | 0.254 | 0.285 |
| all attempts | accuracy C: other practice, same concept | 0.226 | 0.212 | 0.240 |
| all attempts | accuracy D: other practice, other concept | 0.225 | 0.210 | 0.241 |
| all attempts | accuracy E: earlier part of the same problem | 0.651 | 0.614 | 0.687 |
| all attempts | B minus D (transfer beyond general ability) | 0.044 | 0.021 | 0.068 |

### 2. Cold start: first attempt of a practice in a new concept

`B_minus_placebo` compares two equal-size random samples (up to 20 problems) from the student's history: same practice in other concepts (B) versus other practices in other concepts (D, the placebo). Equal sizes mean equal measurement noise, so a positive difference means the practice itself carries over. `B_beyond_all_of_D` is the coefficient of all same-practice history when all of D (general ability) is controlled.

| practice | targets | B_estimate | placebo_estimate | B_minus_placebo | low | high | B_beyond_all_of_D | B_beyond_low | B_beyond_high |
|---|---|---|---|---|---|---|---|---|---|
| all | 56368 | 0.369 | 0.364 | 0.005 | -0.052 | 0.062 | 0.305 | 0.256 | 0.354 |
| Representing | 18315 | 0.419 | 0.403 | 0.016 | -0.102 | 0.134 | 0.257 | 0.152 | 0.362 |
| Abstracting | 12959 | 0.264 | 0.340 | -0.076 | -0.157 | 0.006 | 0.161 | 0.105 | 0.217 |
| Justifying | 5159 | 0.190 | 0.192 | -0.003 | -0.139 | 0.134 | 0.110 | -0.018 | 0.239 |
| Procedural | 19935 | 0.441 | 0.349 | 0.092 | -0.001 | 0.185 | 0.557 | 0.484 | 0.630 |

![transfer](rq2_transfer.png)

The next figure shows the raw association behind `B_beyond_all_of_D`: within each general-ability decile, students who were strong at the practice in other concepts do better on its first attempt in a new concept. On its own this does not show a *practice-specific* skill. The equal-size placebo test above asks whether other-practice history of the same size predicts just as well.

![cold start](rq2_cold_start.png)

### 3. Source -> target matrix

Each target practice's first attempt in a new concept, predicted from 3 random problems of each source practice in other concepts (equal sizes, so the entries are comparable). `own_minus_others` tests the diagonal: the target's own practice minus the average of the others.

| target | source | estimate | low | high | targets |
|---|---|---|---|---|---|
| Representing | Representing | 0.229 | 0.154 | 0.305 | 7707 |
| Representing | Abstracting | 0.244 | 0.159 | 0.328 | 7707 |
| Representing | Justifying | 0.102 | 0.041 | 0.162 | 7707 |
| Representing | Procedural | 0.235 | 0.151 | 0.320 | 7707 |
| Abstracting | Representing | 0.181 | 0.081 | 0.281 | 6984 |
| Abstracting | Abstracting | 0.152 | 0.081 | 0.223 | 6984 |
| Abstracting | Justifying | 0.112 | 0.050 | 0.174 | 6984 |
| Abstracting | Procedural | 0.199 | 0.125 | 0.272 | 6984 |
| Justifying | Representing | 0.098 | -0.013 | 0.209 | 4760 |
| Justifying | Abstracting | 0.094 | -0.013 | 0.200 | 4760 |
| Justifying | Justifying | 0.187 | 0.065 | 0.310 | 4760 |
| Justifying | Procedural | 0.105 | 0.000 | 0.209 | 4760 |
| Procedural | Representing | 0.228 | 0.163 | 0.294 | 7613 |
| Procedural | Abstracting | 0.261 | 0.190 | 0.332 | 7613 |
| Procedural | Justifying | 0.142 | 0.054 | 0.231 | 7613 |
| Procedural | Procedural | 0.351 | 0.279 | 0.423 | 7613 |

| target | targets | own_minus_others | low | high |
|---|---|---|---|---|
| Representing | 7707 | 0.036 | -0.040 | 0.112 |
| Abstracting | 6984 | -0.012 | -0.084 | 0.060 |
| Justifying | 4760 | 0.089 | -0.016 | 0.194 |
| Procedural | 7613 | 0.141 | 0.052 | 0.229 |

![matrix](rq2_transfer_matrix.png)

### 4. Predictive value for knowledge tracing (held-out students)

| model | test_auc | test_log_loss | auc_gain_low | auc_gain_high |
|---|---|---|---|---|
| baseline (difficulty, overall and same-concept history) | 0.7896 | 0.5347 |  |  |
| baseline + same-practice history | 0.7898 | 0.5342 |  |  |
| difference (AUC gain) | 0.0003 | -0.0004 | 0.0002 | 0.0004 |

### Answer to RQ2

- **Not in general**: being good at a practice in other concepts predicts the first attempt in a new concept (coefficient 0.31 even beyond general ability), but an equally large sample of *other*-practice history predicts about as well (+0.005 (95% CI -0.052 to +0.062) log-odds). So it mostly reflects being a strong student, not a skill in that practice.
- Over all attempts, same-practice history in other concepts is slightly more predictive than other-practice history (+0.044 (95% CI +0.021 to +0.068) log-odds), but this comparison does not equalize sample sizes.
- **Representing**: cold start +0.016 (95% CI -0.102 to +0.134); own practice vs others in the matrix +0.036 (95% CI -0.040 to +0.112). No practice-specific transfer beyond general ability.
- **Abstracting**: cold start -0.076 (95% CI -0.157 to +0.006); own practice vs others in the matrix -0.012 (95% CI -0.084 to +0.060). No practice-specific transfer beyond general ability.
- **Justifying**: cold start -0.003 (95% CI -0.139 to +0.134); own practice vs others in the matrix +0.089 (95% CI -0.016 to +0.194). No practice-specific transfer beyond general ability.
- **Procedural**: cold start +0.092 (95% CI -0.001 to +0.185); own practice vs others in the matrix +0.141 (95% CI +0.052 to +0.229). **Practice-specific transfer** (source-target matrix).
- **Practical value**: adding same-practice history to a knowledge-tracing model changes held-out AUC by +0.0003 (95% CI +0.0002 to +0.0004).

## Limitations

- Practice labels come from an LLM (Qwen3-30B), not from expert raters; rerun with `--confident-labels` to check the results on problems with a clear top practice.
- Observational data: teachers choose assignments, so exposure is not randomized. The models compare equally able students on the same problems, but unmeasured differences (e.g. classes) can remain.
- `discrete_score` counts hint use as a failure; hint and answer outcomes are reported separately.
- Practices with fewer than 20 problems (Modeling, Collaborative) are only described.
