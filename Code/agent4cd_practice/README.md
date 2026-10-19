# Agent4CD on FoundationalASSIST

This folder implements **Agent4CD** (Sun et al., *Agent4CD: Generative Agent for Cognitive Diagnosis in Intelligent Education*, IEEE TNNLS 2026) on FoundationalASSIST. It is the paper's method only: no mathematical practices are used. The folder name leaves room for a practice version later.

**What the method does.** Every learner gets an LLM agent. The agent is given:
- a profile of the learner;
- a memory of the learner's past answers;
- a knowledge-state tool (NCDM, or MACA-CD) that says how well the learner masters each concept.

For each test record, in time order, the agent:
1. reasons about how the learner would solve the exercise;
2. infers the learner's current affective state;
3. predicts Yes/No: will the learner answer correctly?
4. With online feedback (the paper's protocol), it is then told the true outcome, stores it in memory, and reflects on its mistake and on the learner's overall *learning status*. The reflection is the agent's updated reading of the learner, and it is used in the next prediction. No model weights change.

**Sources.**
- **Prompts:** the paper's appendix.
- **Memory details:** the official Agent4CD repository only publishes a driver script (`main.py`) that imports its modules from Agent4Edu (Gao et al. 2025). The details missing from the paper follow Agent4Edu: short-term memory of 5 records, and the tool's mastery tiers (>0.66 good, >0.33 common, otherwise poor).
- **NCDM:** ported from the official NeuralCD code.

## Components (paper section and equation → file)

| Paper | What it is here | File |
|---|---|---|
| Data (Sec. III-A) | maca_cd's split records, so Agent4CD is scored on the same test records as MACA-CD. Each learner's records are in time order (`end_time`). A seeded 1/8 of the training records is held out for validation, giving the paper's **70/10/20**. | `prepare_data.py` |
| **Behavioral patterns** (Eq. 1) | P^act = \|E_s\|/\|E\|, P^div = \|K_s\|/\|KC\|, P^suc = mean r, computed on each learner's history (all non-test records) | `prepare_data.py` (`profile_statistics`) |
| **Cognitive factor** (Eq. 2) | IRT 2PL ability P^ab: P(r=1) = σ(α_e(P^ab_s − β_e)), with α_e > 0 via softplus | `tools/irt.py` |
| **Profile mapping** f^P (Eq. 3) | Each statistic is placed in a tertile across all learners and becomes the appendix-A description: "frequently / regularly / rarely practice", "wide / moderate / limited range", success "high / medium / low", ability "good / common / poor". The most-practiced concept is also stated. This is the agent's system prompt. | `agent/learner_profile.py` |
| **Factual memory** (Eq. 4) | M ← M ∪ {l_si}. Every stored record whose concepts are related to the new record's concepts is reinforced: f_sj += 1. The prompt shows the `factual_k` (10) most-reinforced records related to the current exercise. | `agent/memory.py` |
| KC relation R(·) (Eq. 4, "RCD's statistical tool") | From consecutive training records that were both answered correctly, count transitions concept i → j. C_ij = n_ij / Σ_k n_ik, and i → j is an edge when C_ij > mean + std of the non-zero C_ij. Two concept sets are related when they share a concept or an edge joins them. | `prepare_data.py` (`kc_relations`) |
| **Reasoning** f^R (Eq. 5) | Task 1: infer the learner's reasoning path from the profile, the factual memory and the previous reasoning R_{i−1} | `agent/prompts.py` (`prediction_prompt`) |
| **Affect analysis** f^A (Eq. 6) | Task 2: confident / frustrated / bored (slip) / engaged (flow), inferred from the short-term memory (the last d = 5 records), with the paper's definitions | `agent/prompts.py` |
| **Problem comprehension** (Eq. 9) | S_state = the tool's θ ⊙ Q_e: the mastery of the exercise's concepts, written as `concept: tier (value)`, plus the latest learning status | `agent/prompts.py`, `tools/knowledge_state.py` |
| **Reasoning and solving** (Eq. 10) | Task 3: Yes/No. The answer is a schema-constrained JSON object `{task1, task2, task3}`. P(Yes) is read from the Yes/No token's log-probabilities, which gives AUC. | `agent/prompts.py`, `agent/llm.py` |
| **Error-correction reflection** (Eq. 7) | When the prediction was wrong, the paper's false-negative / false-positive trigger is inserted into the reflection | `agent/prompts.py` (`reflection_prompt`) |
| **Summary reflection** (Eq. 8) | "Reflect on results, affect, and update knowledge state… summarize your # Learning Status # within 500 words", based on the profile, short- and long-term memory, the previous learning status and the tool's θ | `agent/prompts.py` |
| **Adaptive update** (Eq. 11) | θ, M and CR are updated at the agent level: the record joins the memory, the new learning status replaces the old one in the next prompt, and CR stores the trigger. The CD tool is never retrained. | `agent/agent.py` |
| Knowledge-state tool (NCDM) | Official NeuralCD `Net` and `NoneNegClipper`. Training follows its `train.py`: Adam lr 0.002, NLLLoss on log[1−p, p], clipping after each step, batch 32. The epoch is picked by validation AUC. | `tools/ncdm.py` |
| Knowledge-state tool (MACA-CD) | Plain MACA-CD's students × concepts proficiency from its best epoch | `tools/knowledge_state.py`, `../maca_cd/model/train.py` (`save_state`) |
| Metrics (Sec. V-C) | ACC and F1 (the paper's), plus AUC from P(Yes). IRT, NCDM and MACA-CD are scored on the same records. | `evaluate.py` |
| Ablations (RQ6) | `no_profile`, `no_reasoning`, `no_affect`, `no_reflection` | `config.json` → `agent.ablation` |

### One learner's run (`agent/agent.py`)
```
memory <- history (all non-test records, time order, Eq. 4 reinforcement)
SR_0   <- summary reflection over the history                     (1 LLM call)
for each test record e_i, in time order:
    {task1 reasoning, task2 affect, task3 Yes/No}  <- prediction   (1 LLM call: Eqs. 5, 6, 9, 10)
    if online_feedback:
        reveal r_i; memory <- memory + (e_i, r_i)                   (Eq. 4)
        SR_i <- reflection (+ corrective trigger if wrong)          (1 LLM call: Eqs. 7, 8, 11)
```
- **Online feedback** (`online_feedback: true`, the paper's protocol): each prediction can use the outcomes of the learner's earlier test records.
- **Offline** (`false`): no test outcome is ever revealed. That is the fair comparison with MACA-CD, which never sees test outcomes. It is also about 3× cheaper.

## Settings (`config.json`)

| Setting | Default | Meaning |
|---|---|---|
| `num_students` | 300 | Number of learners simulated. They come from a fixed seeded order, so 1,000 contains the first 300. |
| `knowledge_tool` | `ncdm` | `ncdm` or `maca_cd` (plain MACA-CD, no practices) |
| `maca_cd_seed` | null | Which maca_cd run to read (`--seed` of its `train.py`; null = unseeded) |
| `val_fraction` | 0.125 | Share of maca_cd's training records used to validate IRT/NCDM (70/10/20 overall) |
| `relation_threshold` | null | KC-relation edge threshold (null = mean + std) |
| `agent.short_term_size` | 5 | Recent records d (paper: 5) |
| `agent.factual_k` | 10 | Reinforced related records shown |
| `agent.summary_max_words` | 500 | Learning-status length (paper: 500 words) |
| `agent.online_feedback` | true | The paper's protocol (see above) |
| `agent.ablation` | none | none / no_profile / no_reasoning / no_affect / no_reflection |
| `llm.*` | Qwen3-30B-A3B-Instruct-2507 on :8000, temperature 0 (paper), 64 requests in flight | |

`run_agent.py` can override `--num-students`, `--knowledge-tool`, `--ablation` and `--online-feedback` for one run.

## How to run (A100)

**Prerequisites.**
- maca_cd's preprocessing must exist: `../maca_cd/data/cleaned_data.csv`, `../maca_cd/data/preprocessed/*_spilt.pkl` and `../maca_cd/data/graph/concept_data.json`.
- Packages: torch, numpy, pandas, scikit-learn, openai, bs4 and vllm. `prepare_data.py` imports the item-text helpers of `augment_mathematical_practice.py`.

```bash
cd ~/knowledge_tracing_foundationalASSIST && git pull
cd Code/agent4cd_practice

# 1. Inputs for the split (a minute or two)
python3 prepare_data.py --split standard

# 2. IRT + NCDM tools (about 20-40 min; run it while the GPU is free, or add --device cpu)
python3 train_tools.py --split standard

# 2b. Only for knowledge_tool maca_cd: retrain maca_cd once so it saves its proficiency
#     (writes ../maca_cd/model/results/OurModel/state_standard.npz)
# cd ../maca_cd/model && python3 train.py --split standard && cd ../../agent4cd_practice

# 3. vLLM server (its own terminal, or nohup)
VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=0 nohup vllm serve Qwen/Qwen3-30B-A3B-Instruct-2507 \
    --port 8000 --max-model-len 32768 --enable-prefix-caching > vllm_server.log 2>&1 &

# 4. Check the prompts of 2 learners, then run
python3 run_agent.py --split standard --run-name full --dry-run
mkdir -p logs
PYTHONUNBUFFERED=1 nohup python3 run_agent.py --split standard --run-name full > logs/standard_full.log 2>&1 &
tail -f logs/standard_full.log            # progress lines: records done, ACC, records/h, ETA

# 5. Scores (the same records for every row)
python3 evaluate.py --split standard --run-name full
```

**A fixed learner list.** To reuse the same learners in later experiments, save a list once and keep it in git:
```bash
python3 make_learner_list.py --split standard --n 50      # learners/standard_50.json
PYTHONUNBUFFERED=1 nohup python3 run_agent.py --split standard --run-name pilot50 \
    --learner-file learners/standard_50.json > logs/standard_pilot50.log 2>&1 &
```
The list is the first 50 learners of the seeded order, so they are also the first 50 of the default 300.

**Resuming.** If a run stops, rerun the same command: it continues where each learner stopped. To add learners, rerun with a larger `--num-students`. A run name is tied to its settings: changing the tool, the feedback mode, the ablation or the model needs a new `--run-name`.

**Other runs.** Ablations, the offline protocol and the MACA-CD tool each need their own run name. Score them together on their common records:
```bash
PYTHONUNBUFFERED=1 nohup python3 run_agent.py --split standard --run-name offline --online-feedback false > logs/standard_offline.log 2>&1 &
PYTHONUNBUFFERED=1 nohup python3 run_agent.py --split standard --run-name no_affect --ablation no_affect > logs/standard_no_affect.log 2>&1 &
PYTHONUNBUFFERED=1 nohup python3 run_agent.py --split standard --run-name maca_tool --knowledge-tool maca_cd > logs/standard_maca_tool.log 2>&1 &
python3 evaluate.py --split standard --run-name full offline no_affect maca_tool
```
Runs share the vLLM server, so running two at once splits its throughput between them.

## Outputs
- `data/<split>/`: records, learner sequences, exercise texts, concepts and KC relations (from `prepare_data.py`).
- `tool_outputs/<split>/irt.npz`, `ncdm.npz`: ability, proficiency and test predictions.
- `results/<split>/<run>/`:
  - `run_config.json` holds the settings and the learners;
  - `students/<id>.jsonl` holds each learner's steps: prediction, P(Yes), reasoning, affect, reflection and tokens;
  - `predictions.csv` and `metrics.json` (written by `evaluate.py`), with per-affect accuracy.
- `results/<split>/evaluation_<runs>.md`: the comparison table.

## Cost

The standard split has about 66 test records per learner, so 300 learners give about 20k test records.
- **Online:** 2 calls per record, about 1k output tokens. Roughly 1.5–3 h on one A100.
- **Offline:** 1 call per record, roughly 0.5–1 h.

The progress lines print the real rate.

## Where this differs from the paper, and why
- **Data.** These are FoundationalASSIST math items with maca_cd's split (80/20 records, plus 10 points of the training part held out for validation), not PISA. All four maca_cd splits (`standard`, `cold`, `zeroshot`, `colditem`) work.
- **Output format.** The agent answers with a schema-constrained JSON object instead of "Task1:/Task2:/Task3:" lines, so every answer parses. If an answer is cut off, it is retried with twice the tokens. If it still fails, the step uses the tool's own prediction and is counted in `metrics.json` (`fallbacks`).
- **AUC.** AUC is added, from the Yes/No token probabilities. The paper reports only ACC and F1.
- **History.** The learner's history is written into memory before the first test record, without LLM calls, and summarized once (SR_0). The paper's memory "starts empty", but it does not say how training records reach the agent.
- **Forgetting.** Agent4Edu's forgetting of long-term facts is not used: Agent4CD's paper does not describe it.
- **Reflection.** The appendix's corrective trigger and summary instruction share one reflection call per test record.
