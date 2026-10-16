# MACA-CD (practice version) for FoundationalASSIST

This folder is a copy of `../maca_cd/` in which the model diagnoses proficiency per
(concept, mathematical practice) instead of per concept. Everything else is identical to `maca_cd`
(see the sections after this one).

## Practice version

Notation: K concepts, P = 6 practices (the order of `mathematical_practice` in `Data/Problems.csv`:
Representing, Abstracting and Generalizing, Justifying and Proving, Mathematical Modeling,
Collaborative Mathematics, Procedural Fluency), M students, N questions, d = `mf_dim`.

1. **z_p** (P x d): the embedding of each practice's definition and descriptors (the text of the
   zero-shot labeler `Code/augment_mathematical_practice.py`), projected like the concept text.
2. **h_kp = MLP(o_k * z_p)** (K x P x d), where o_k is MACA-CD's fused concept embedding (`o_t_final`:
   concept text + prerequisite graph).
3. **C_mkp = sigmoid(<u_m, h_kp> + b_m)**: proficiency of student m on practice p for concept k.
   b_m is the student bias MACA-CD uses in its mastery.
4. **D_nkp = sigmoid(<v_n, h_kp>)**: difficulty of question n for practice p on concept k.
5. **Q_joint_n** (K x P): the joint Q-matrix of question n (below).
6. **x_mn = Q_joint_n * (C_m - D_n)**, flattened to K*P. As in MACA-CD, the sigmoid is applied once
   (in steps 3 and 4), not again here.
7. **r_mn = MLP(x_mn)**: MACA-CD's positive-weight MLP, with input size K*P.

The concept graph encoder, its contrastive loss, the text/graph fusion, the training loop and the
evaluation are unchanged. `mastery_levels()` returns C (M x K x P). DOA weights each exercise by its
joint Q-matrix entries.

### The joint Q-matrix

Q_joint is N x K x P. Row k of Q_joint_n holds concept k's practice weights in question n; the rows of
concepts the question does not involve are 0.
- A question with one skill: its concept gets the question's six zero-shot scores
  (`mathematical_practice`).
- A question with several skills: each skill gets its own six scores (`concept_practice`, from
  `Code/augment_practice_per_concept.py`, which prompts the zero-shot labeler once per skill).
- Each vector is divided by its sum, so each involved concept's weights sum to 1. Summing Q_joint_n over
  practices gives back the concept Q-matrix exactly, and each concept's (C - D) term is a weighted
  average of its practice terms. The weights of one practice over concepts are not normalized (like any
  Q-matrix column).
- An all-zero score vector falls back to the question's scores, then to a one-hot of
  `predicted_practice`. Dividing by the sum (not a softmax) keeps the practices the LLM scored 0 at 0;
  a softmax of scores in [0, 1] would be nearly uniform.

Files that differ from `maca_cd`:
- `data/concept_main.py`: new stage `--stage practice_embed` (`practice_texts`, `practice_meta_embed`)
  -> `data/concept_preknowledge/practice_meta_emb.json`.
- `data/data_preprocess.py`: reads `mathematical_practice`, `concept_practice` and `predicted_practice`
  from `Data/Problems.csv` and adds `Q_joint` (exercise -> {concept id: six weights}) and
  `practice_names` to every split. The splits themselves are the same as `maca_cd`'s.
- `model/data_loader.py`: `load_practice_embedding`, `joint_q_tensor`; each split's output has the joint
  Q-matrix `QJ` (exercise x concept x practice).
- `model/train.py`: passes the practice embedding and `QJ` to the model and to DOA.
- `model/OurModel.py`: `Prac_Encoder` (z_p), `KP_MLP` (h_kp), `practice_matrices` (C, D) and the joint
  interaction in `forward`.

### How to run (A100, from `Code/maca_cd_practice/`)

Needs the finished `maca_cd` concept stages, the zero-shot practice labels in `Data/Problems.csv`
(`Code/augment_mathematical_practice.py`) and the per-skill scores of the multi-skill problems
(`Code/augment_practice_per_concept.py`; run from `Code/` with the GPU free). Reuse maca_cd's LLM
outputs, so both models share the concepts, the prerequisite graph and the splits:
```bash
cp -r ../maca_cd/data/cleaned_data.csv ../maca_cd/data/used_concepts.txt ../maca_cd/data/graph ../maca_cd/data/concept_preknowledge data/
```
With the embedding server on port 8001 (step 3 below):
```bash
python3 data/concept_main.py --stage practice_embed
```
Then build the splits and train the three splits in parallel:
```bash
python3 data/data_preprocess.py
cd model && for s in standard cold zeroshot; do PYTHONUNBUFFERED=1 nohup python3 train.py --split $s > train_$s.log 2>&1 & done
```
Results are in `model/results/OurModel/training_logs_<split>.txt`; `python3 ../compare_maca_cd_results.py`
(from `Code/maca_cd_practice/`) prints the benchmark table against `maca_cd` (`--format markdown` or
`latex` for a paper).

To run the whole benchmark at once (both models, all three splits: 6 runs on one GPU, then the table),
from `Code/`: `nohup bash run_maca_benchmark.sh > ../Data/maca_benchmark.log 2>&1 &`.

---

# MACA-CD for FoundationalASSIST (shared with maca_cd)

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
