# Multi-agent debate for mathematical practice classification

Predicts which mathematical practice an item mainly assesses with the debate protocol of
Khan et al. (2024), *Debating with More Persuasive LLMs Leads to More Truthful Answers*
(arXiv:2402.06782), and scores the predictions against the 35 ground-truth items in
`Data/problems_naep.csv`.

`core/` is a trimmed copy of the paper's code (`llm_debate`, MIT license, Copyright (c) 2024 UCL DARK
Lab; see `LICENSE`), adapted as described below. Everything else in this folder is new.

## How the paper's setup maps to this task

| Paper (QuALITY) | Here |
|---|---|
| Story (debaters see it, judge does not) | Practice framework: definition and descriptors of the six practices (same text as `augment_mathematical_practice_test5.py`), followed by the item |
| Question | "Which mathematical practice does this item mainly assess?" plus the item (the judge sees both) |
| Two answers | Two practices. Every pair of the six practices is debated: 15 pairs, each in both answer orders = **30 debates per item** |
| Judge's answer | The judge's log-probabilities of "A" and "B" after round 3 |

**Protocol** (unchanged from the paper's interactive debate):
- 3 simultaneous rounds: opening arguments; then the judge asks each debater a question and they
  attack the opponent's argument; then the judge asks again and they defend their own.
- Each debater turn: best-of-4 drafts (rated by the judge model), then critique-and-refinement with
  8 critiques (the most helpful one, rated by a critique model, is used to refine).
- Quotes from the framework or the item are checked: `<v_quote>` (verified) or `<u_quote>` (not).

**Prediction:** for each item, every practice takes part in 10 debates (5 opponents x 2 orders). Its
score is the mean of the judge's log-probability for it over those debates; the highest mean wins.

All agents (debaters, critic, raters, cross-examiner, judge) are `Qwen/Qwen3-30B-A3B-Instruct-2507`
served by a local vLLM server.

## Files

| File | What it does |
|---|---|
| `build_dataset.py` | `problems_naep.csv` -> `data/naep_pairs_<run>.csv`, one row per item and practice pair. Drops `ground_truth` before anything else. |
| `core/` | The debate and judge code (see changes below). `config/experiment/practice_debate.yaml` sets the protocol. |
| `aggregate.py` | Judge log-probabilities -> mean per practice -> prediction; prints accuracy, per-practice results, confusion matrix, misclassified items, and how often swapping the answer order changed a pair's winner. Writes `Data/naep_debate_<run>_predicted.csv` and `Data/naep_debate_<run>_eval.json`. |
| `run_naep_debate.sh` | Runs all of the above. |
| `practices.py` | The six practice names in output order. |

## Changes to the original code

- **LLM backend:** new `core/llm_api/vllm_llm.py` talks to a local vLLM server through `openai>=1`.
  `llm.py` routes every model id to it. The OpenAI (`openai==0.28`) and Anthropic clients are removed.
- **Item placeholder:** `<ITEM>` in prompts (stored in `transcript.extra["item"]` by
  `core/rollouts/quality_sim.py`), so prompts show the item separately from the short question.
- **Prompts:** new `practice_*.yaml` configs, adapted from `debaters/v1_interactive.yaml`,
  `judge/debate/preference.yaml` (final judge and best-of-N rater), `judge/debate/intermediary.yaml`,
  `critic/debate/critic_story.yaml` and `critique_pm_story.yaml`. Only the wording changed ("story" ->
  "practice framework"); the structure and instructions are the paper's.
- **Data loading:** `core/debate.py` copies the CSV from `build_dataset.py` (`++dataset_file=`)
  instead of loading QuALITY.
- **Log-probabilities:** `find_choice_logprobs` reads the first generated position that contains the
  choice letters, instead of always position 0, in case the model emits a stray token first.
- **Compatibility:** `pydantic.v1` imports; a `StrEnum` fallback for Python 3.10; no SECRETS file;
  quote verification (`core/parser.py`) copied without the web app's database imports.
- **Removed:** web frontend and backend, database, tournament, sequential debate, consultancy
  scripts, scoring.

## Running on the A100

All commands run from `Code/`. Install the extra packages into the vLLM environment once:
```bash
pip install --user -r multi_agent_debate/requirements.txt
```

Start the model server (keep it running for the whole experiment):
```bash
VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=0 nohup vllm serve Qwen/Qwen3-30B-A3B-Instruct-2507 --port 8000 --max-model-len 32768 --enable-prefix-caching > ../Data/vllm_server.log 2>&1 &
```
Wait until `curl -s localhost:8000/v1/models` lists the model.

Pilot on 1 item (30 debates):
```bash
bash multi_agent_debate/run_naep_debate.sh pilot 1
```

All 35 items (1,050 debates), in the background:
```bash
nohup bash multi_agent_debate/run_naep_debate.sh full > ../Data/naep_debate_full.log 2>&1 &
```

Rerunning a command resumes it: finished debate steps are cached in `multi_agent_debate/exp/<run>/`.

**Cost:** about 20 model calls per debater turn (4 drafts x 3 candidates, 4 ratings, 8 critiques,
8 critique ratings, 4 refinements x 3 candidates, 4 ratings), about 120 per debate, so about 3,600
per item. Time the pilot before starting the full run.
