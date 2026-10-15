# MACA-CD for FoundationalASSIST

The MACA-CD cognitive diagnosis pipeline (LLM concept augmentation + the MACA-CD model) applied to
FoundationalASSIST. The code is a copy of the SLP folder of MACA-CD
(github.com/ShaoPengyang/MACA-CD, by its authors; the repository has no license file) with the changes
listed below. MACA-CD ships the same pipeline for Eedi, SLP and XES; this folder is its
FoundationalASSIST counterpart.

## Pipeline

1. **Preprocessing** (`data/concept_main.py --stage preprocess`): `Data/Interactions.csv` and
   `Data/Skills.csv` -> `data/cleaned_data.csv`, `data/used_concepts.txt`, `data/graph/concept_data.json`
   (concept ids 1..N).
2. **Concept augmentation** (`data/concept_main.py`). Every step is a debate between two agents, repeated
   until a judge agent answers "yes" (at most 50 rounds):
   - `metadata`: a description of each concept -> `data/concept_preknowledge/concept_meta_data.json`
   - `init`: the concepts no other concept depends on -> `data/graph/initial_nodes.json`
   - `extend`: breadth-first prerequisite DAG from those nodes -> `data/graph/DAG_edges.json`
   - `embed`: an embedding of each description -> `data/concept_preknowledge/concept_meta_emb.json`
3. **Splits** (`data/data_preprocess.py`): `data/preprocessed/{standard,cold,zeroshot}_spilt.pkl` and the
   student, exercise and concept counts in `parameter.json`.
   - standard: random 80/20 split of the responses
   - cold: half the students are test students, with only 2 of their responses in training
   - zeroshot: 20% of the concepts are held out; responses to problems with a held-out concept are the test set
4. **Training** (`model/train.py --split <split>`): MACA-CD, reporting ACC and AUC on the test set each
   epoch; the best epochs are logged in `model/results/OurModel/training_logs_<split>.txt`.
   At every new best epoch it also computes the DOA (degree of agreement) of the diagnosed proficiency
   over all responses of the split (`degree_of_agreement` in `model/utils.py`, same definition as
   `doa_eval`; the practice version also prints the DOA of each practice).

LLM: `Qwen/Qwen3-30B-A3B-Instruct-2507` on the local vLLM server (port 8000). Embeddings:
`Qwen/Qwen3-Embedding-0.6B` on a second vLLM server (port 8001), 256 dimensions. Both are set in
`parameter.json`.

## Changes from MACA-CD/SLP

- **Data:**
  - A concept is a skill `node_code`, named by its `node_name`. The 224 `skill_id`s in `Skills.csv` share
    164 codes and names.
  - Each interaction is kept once (`drop_duplicates("id")`), and only the first attempt per student and
    problem.
  - Students and problems with fewer than `min_interactions` (30) responses are dropped, as in SLP.
- **Multi-skill problems:** 355 problems have 2-3 skills, so `Q_matrix` maps each exercise to a list of
  concept ids and the model's Q-matrix row is multi-hot. In the zeroshot split, a response is a test
  response when any of its problem's concepts is held out.
- **LLM backend:** `llm_provider.py` has a `vllm` provider, which uses OpenAI-compatible chat completions
  and embeddings on a local server. The `qwen` and `openai` providers are unchanged.
- **Concept names with commas** (e.g. "Add, Subtract, Multiply & Divide Multi-Digit Decimals"):
  - the root-node prompt asks for quoted names, like the extension prompt already does;
  - both answers are parsed by the quotes.
- **Robustness for long runs:**
  - `extend` saves its state after every concept and resumes from `data/graph/execution_state.json`;
  - `metadata` skips concepts that are already described;
  - names the LLM returns that match no concept are not visited;
  - `pdb.set_trace()` calls are now errors;
  - the judge's "Yes." counts as "yes";
  - a description that is not valid JSON falls back to its text.
- **Stages** are chosen with `--stage` instead of commenting lines in `__main__`.
- **Splits** are seeded (`seed` in `parameter.json`), and `train.py` uses `learning_rate` from
  `parameter.json` (0.001, the value SLP hard-coded).
- **Unchanged:**
  - the prompts and the debate loop;
  - the DAG cycle check and concept-name matching;
  - the model (`OurModel.py`) and the training loop.

## How to run (A100)

Install the extra packages into the vLLM environment once (torch, pandas and openai are already there):
```bash
pip install --user python-Levenshtein networkx scikit-learn scipy joblib tqdm
```

All commands start in `Code/maca_cd/`.

**1. Preprocess** (CPU, a few minutes; prints the student, problem and concept counts):
```bash
python3 data/concept_main.py --stage preprocess
```

**2. Concept descriptions and graph** with the 30B server (start it as for the other experiments and wait
until `curl -s localhost:8000/v1/models` lists it):
```bash
VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=0 nohup vllm serve Qwen/Qwen3-30B-A3B-Instruct-2507 --port 8000 --max-model-len 32768 --enable-prefix-caching > ../../Data/vllm_server.log 2>&1 &
python3 data/concept_main.py --stage metadata --limit 2     # smoke test: 2 concepts
nohup python3 data/concept_main.py --stage metadata > data/metadata.log 2>&1 &
python3 data/concept_main.py --stage init
nohup python3 data/concept_main.py --stage extend > data/extend.log 2>&1 &
```
`metadata` and `extend` resume when rerun. Rerun `init` only after deleting `data/graph/execution_state.json`
and `data/graph/DAG_edges.json`, because they belong to the old root nodes.

**3. Embeddings:** stop the 30B server (`pkill -f "vllm serve"`), then serve the embedding model:
```bash
VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=0 nohup vllm serve Qwen/Qwen3-Embedding-0.6B --port 8001 --runner pooling > ../../Data/vllm_embed.log 2>&1 &
python3 data/concept_main.py --stage embed
```
Older vLLM versions take `--task embed` instead of `--runner pooling`.

**4. Splits:**
```bash
python3 data/data_preprocess.py
```

**5. Train:** stop the embedding server, then run from `model/`:
```bash
cd model
python3 train.py --split standard
python3 train.py --split cold
python3 train.py --split zeroshot
```
`--device cuda:1` picks another GPU. Training runs 200 epochs (`number_epoch` in `parameter.json`).

Rerunning `preprocess` with a different `min_interactions` changes the concepts. It then stops and asks you
to delete `data/graph/` and `data/concept_preknowledge/`, because the LLM outputs use the old concept ids.
