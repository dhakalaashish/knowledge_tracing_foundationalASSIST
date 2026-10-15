# Qwen3-30B-A3B-Instruct: FoundationalASSIST benchmark

### Table 2. Knowledge tracing accuracy broken down by correctness

| Model | FKT Acc. | Correct: FKT Acc. | Correct: Cog. Acc. | Incorrect: FKT Acc. | Incorrect: Cog. Acc. |
|---|---|---|---|---|---|
| GPT-OSS-120B | 56.2% | 68.2% | 62.9% | 43.4% | 10.1% |
| Llama-3.3-70B | 52.3% | 85.4% | 72.6% | 12.6% | 3.7% |
| Qwen3-80B-Inst. | 54.0% | 56.5% | 50.3% | 51.0% | 13.5% |
| Qwen3-80B-Think. | 55.8% | 63.6% | 57.6% | 44.6% | 12.9% |
| **Qwen3-30B-A3B-Instruct** | 52.0% | 72.2% | 70.3% | 28.0% | 11.5% |

| Extra (this run) | Value |
|---|---|
| Predictions | 498 |
| All-correct baseline | 52.0% |
| FKT AUC-ROC | 0.511 |
| Parsed predictions | 98.0% |
| Predicted 'correct' rate | 71.1% |
| Incorrect: truly-wrong answers used for Cog. Acc. | 209/239 |
| Incorrect: Cog. Acc. without the truly-wrong filter | 20.1% |

### Table 3. Cognitive modeling accuracy by problem type for incorrect answers

| Model | MC (select 1) | MC (select all) | Fill-in-blank |
|---|---|---|---|
| GPT-OSS-120B | 30.3% | 7.0% | 5.7% |
| Llama-3.3-70B-Instruct | 11.8% | 0.9% | 1.7% |
| Qwen3-Next-80B-Instruct | 47.5% | 3.9% | 7.5% |
| Qwen3-Next-80B-Thinking | 34.7% | 5.6% | 6.7% |
| Random Baseline | 41.3% | 2.9% | 0.0% |
| **Qwen3-30B-A3B-Instruct** | 45.5% | 3.8% | 3.8% |
| Random baseline (this run's targets) | 40.4% | 3.3% | 0.0% |

n: Multiple Choice (select 1)=33, Multiple Choice (select all)=26, Fill-in-the-blank(s)=157

Order / Sort (not in the paper): 0.0% (n=1)
