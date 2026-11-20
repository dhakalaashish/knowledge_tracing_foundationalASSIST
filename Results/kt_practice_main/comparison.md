# KT and cognitive student modeling, 100 random paper students (5,501 predictions in every run)

| Metric | Paper: Qwen3-Next-80B-Instruct (BF16, published) | Baseline: Qwen3-Next-80B-Instruct AWQ, paper prompts | Practice: Qwen3-Next-80B-Instruct AWQ, + practices | Profile: Qwen3-Next-80B-Instruct AWQ, student profile + last 10 |
|---|---|---|---|---|
| Predictions | 5,501 | 5,501 | 5,501 | 5,501 |
| Parsed predictions | 99.6% | 99.6% | 99.4% | 99.8% |
| KT accuracy (question level) | 53.3% | 54.1% | 55.8% | 56.4% |
| KT AUC | 0.533 | 0.540 | 0.555 | 0.562 |
| KT accuracy when the student was correct | 54.9% | 57.0% | 69.7% | 67.5% |
| KT accuracy when the student was incorrect | 51.3% | 50.7% | 40.6% | 44.8% |
| Predicted 'correct' rate | 51.7% | 53.1% | 64.3% | 61.4% |
| All-correct baseline | 50.9% | 50.9% | 50.9% | 50.9% |
| Cognitive accuracy, correct answers | 49.3% | 51.2% | 63.0% | 60.8% |
| Cognitive accuracy, incorrect answers | 13.6% | 14.0% | 9.9% | 8.9% |
|   MC (select 1) | 47.7% | 46.9% | 30.2% | 29.4% |
|   MC (select all) | 3.9% | 3.2% | 2.4% | 2.9% |
|   Fill-in | 7.3% | 8.1% | 6.3% | 4.9% |

## Practice vs baseline on the same 5,448 targets (paired)

|  | only baseline right | only practice right | McNemar p |
|---|---|---|---|
| KT (question level) | 931 | 1020 | 0.0463 |
| Cognitive, incorrect answers (2266 targets) | 160 | 67 | 5.91e-10 |

## Profile vs baseline on the same 5,472 targets (paired)

|  | only baseline right | only profile right | McNemar p |
|---|---|---|---|
| KT (question level) | 964 | 1093 | 0.00476 |
| Cognitive, incorrect answers (2278 targets) | 184 | 69 | 2.97e-13 |

## Profile vs practice on the same 5,459 targets (paired)

|  | only practice right | only profile right | McNemar p |
|---|---|---|---|
| KT (question level) | 835 | 874 | 0.358 |
| Cognitive, incorrect answers (2266 targets) | 111 | 89 | 0.137 |
