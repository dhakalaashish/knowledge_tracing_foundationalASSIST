# generate_practice_reasoning

Labels each problem in `Data/Problems.csv` with an LLM's view of which mathematical practices it needs, in which order, which ones it does not need, and which one is the top practice. It runs through an API (Claude, OpenAI, Gemini) or a local Qwen3-30B on vLLM.

## The three prompts

All prompts are in `prompts.py`. Each problem goes through three separate LLM calls, each a fresh conversation. None of them sees `predicted_practice` or any other label. Prompt 2, the order, was added because the two-prompt version (run `qwen3_30b_v2`) often listed the practices by importance (Procedural Fluency first) instead of in the order a student uses them.

Each practice in the system prompts lists, below its descriptors, example items from `Data/problems_naep_predicted.csv` whose `ground_truth` is that practice, rendered like the problems and without answers: all of them for five practices (4 Representing, 4 Abstracting and Generalizing, 7 Justifying and Proving, 3 Mathematical Modeling, 4 Collaborative Mathematics) and 4 of the 14 Procedural Fluency items. Run `qwen3_30b_v3` used the same prompts without the examples, so a run with the examples needs a new `--column-prefix` (e.g. `qwen3_30b_v4`); the run folder refuses changed prompts otherwise.

| | Prompt 1: practices used and not used | Prompt 2: order | Prompt 3: top practice |
|---|---|---|---|
| System prompt | `SYSTEM_PROMPT_1`: the task, the six practices with the definitions and descriptors from `Code/augment_mathematical_practice.py` (copied verbatim), notes about the items, and the format of answer 1 | `SYSTEM_PROMPT_2`: the task, the same definitions, descriptors and notes, the ordering rules, and the format of answer 2 | `SYSTEM_PROMPT_3`: the task, the same definitions, descriptors and notes, and the format of answer 3 |
| User prompt | `Q1_TEMPLATE`: *Using the practice definitions and descriptors, tell me which practices a student needs to use to solve this item, in the order the student uses them, how the student uses each one, and what a student could get wrong at each step. Then tell me which practices the student does not use, and why.* followed by the problem | `Q2_TEMPLATE`: the problem, the practices answer 1 lists as used, one line each with answer 1's "why", in the fixed order of the six practices (so answer 1's order is not shown), and *Using the practice definitions and descriptors, put these practices in the order in which a student working on this item uses them, from the first step to the last. Say what the student does at each step, and explain why the steps come in this order.* | `Q3_TEMPLATE`: the problem, answer 1 reordered as answer 2 says (JSON, indented) as "Analysis of the practices a student uses to solve this item", and *Using the practice definitions and descriptors and this analysis, tell me which single practice is the top practice of this item: the step where the item's difficulty lies, the one a student who answers incorrectly most likely failed at. Explain why it is the top practice and why the other practices the student uses are less likely to cause an incorrect answer.* |
| Answer | the practices used, in order, each with why and likely errors; the practices not used, each with why | the same practices in the order a student uses them (order in time, not importance), each with the step, and why this order | the top practice, with why |
| Sent | always | only after answer 1 passed the JSON check | only after answer 2 passed the JSON check |

Between prompts 2 and 3, answer 1 is reordered as answer 2 says (`common.combine`): its `practices_used` are put in answer 2's order and renumbered, keeping answer 1's `why` and `likely_errors`; `practices_not_used` stays as it is. This combined analysis is what prompt 3 sees and what goes into `<prefix>_reasoning`.

Answer 1:

```json
{
"practices_used": [
  {"order": 1, "practice": "Representing", "why": "...", "likely_errors": "..."},
  {"order": 2, "practice": "Procedural Fluency", "why": "...", "likely_errors": "..."}
],
"practices_not_used": [
  {"practice": "Abstracting and Generalizing", "why": "..."},
  {"practice": "Justifying and Proving", "why": "..."},
  {"practice": "Mathematical Modeling", "why": "..."},
  {"practice": "Collaborative Mathematics", "why": "..."}
]
}
```

Answer 2:

```json
{
"ordering": [
  {"order": 1, "practice": "Representing", "step": "..."},
  {"order": 2, "practice": "Procedural Fluency", "step": "..."}
],
"why": "..."
}
```

Answer 3:

```json
{"top_practice": "Representing", "why": "..."}
```

The JSON check (`common.AnswerChecker`) parses each answer with `json.loads`. The answer must be exactly one JSON object; a single ```` ```json ```` fence around it is accepted, but any other text before or after it fails. Answer 1 must list at least one practice as used, number the used practices 1, 2, 3... in order, name each of the six practices exactly once across the two lists, give a non-empty "why" for every entry, and a non-empty "likely_errors" for every used practice. Answer 2 must list exactly the practices answer 1 lists as used, each once, numbered 1, 2, 3..., each with a non-empty "step", and a non-empty "why". Answer 3 must name one of the six practices, one that the analysis lists as used, with a non-empty "why". A prompt is only sent after the answer before it passed.

## Retries and the list of failed problems

An attempt is prompts 1, 2 and 3. It fails if, in any prompt, the answer fails the JSON check (`invalid_answer`) or the call itself fails (`error`: output cut off at the token limit, empty answer, API error or refusal). A failed attempt is retried from prompt 1 in fresh conversations. One counter covers all three prompts and both kinds of failure: a problem gets at most 1 + `--max-retries-per-problem` attempts (default 3 retries, so 4 attempts). After that its status is `failed` and it is not tried again unless you pass `--retry-failed`.

At the end of every invocation the script writes `runs/<prefix>/failed_problems.csv`, listing every failed problem in the run folder: `row`, `problem_id`, `attempts`, which prompt failed in each attempt (`failed_steps`), the kind of failure (`failure_kinds`), and the reasons (`last_failure_reason`, `all_failure_reasons`). Failed problems get no values in the CSV columns.

(The API providers also retry a single HTTP request on 429/5xx/connection errors inside the SDK, `--max-retries`, default 8, before a call counts as failed.)

## Output columns

| Column | Content |
|---|---|
| `<prefix>_reasoning` | answer 1 reordered as answer 2 says, as compact JSON (read it back with `json.loads`); the order of its `practices_used` is the final ordering |
| `<prefix>_ordering_reasoning` | answer 2 as compact JSON: each step, and why this order |
| `<prefix>_top_practice` | `top_practice` from answer 3 |
| `<prefix>_top_practice_reasoning` | `why` from answer 3 |

Default prefixes: `claude_api`, `openAI`, `gemini`, `qwen3_30b`. The existing `claude_*` columns from the agent run are never touched. Only rows that finished with status `ok` are written.

`--replace-columns OLD_PREFIX` renames the `OLD_PREFIX_*` columns to `<prefix>_*` in place (same position in the CSV) and empties them first, so they hold only this run's values; the new `<prefix>_ordering_reasoning` column goes right after `<prefix>_reasoning`. Example: `--column-prefix qwen3_30b_v3 --replace-columns qwen3_30b_v2` turns the three `qwen3_30b_v2_*` columns into four `qwen3_30b_v3_*` columns. Later merges of the same run find the `qwen3_30b_v3_*` columns and rewrite them. Logs of the two-prompt version (`runs/qwen3_30b_v2`) can still be merged; they fill `<prefix>_reasoning` with answer 1 and leave `<prefix>_ordering_reasoning` empty.

## Files

| File | Purpose |
|---|---|
| `prompts.py` | the three system prompts and the three user prompts |
| `generate.py` | command-line entry point: runs the three prompts, checks the answers, logs everything, merges the columns into the CSV |
| `providers.py` | the four backends: `anthropic`, `openai` (also any OpenAI-compatible server), `gemini`, `local` (offline vLLM) |
| `common.py` | problem loading, building the prompts, combining answers 1 and 2, the JSON checks, logs, CSV merge |
| `problems_rendered.jsonl` | all 3,395 problems as plain text, one per data row (`row`, `problem_id`, `text`) |
| `tools/render_problems.awk`, `tools/to_jsonl.awk`, `tools/check_jsonl.awk` | how `problems_rendered.jsonl` was made and checked |

`problems_rendered.jsonl` holds the exact text the Claude agents read: HTML turned into plain text, MathML into linear math, tables into `a | b` rows, images into their alt text, multiple-choice options listed as A, B, C... The correct answer is never included. It was checked byte for byte against the rendered files of the agent run. To rebuild it (on any machine with gawk):

```bash
mkdir -p rendered
LC_ALL=C gawk -b --csv -v FROM=1 -v TO=3395 -v OUT=rendered -f tools/render_problems.awk ../../Data/Problems.csv > /dev/null
gawk --csv 'NR>1 {print NR-1 "\t" $10}' ../../Data/Problems.csv > ids.tsv
LC_ALL=C gawk -b -F'\t' -v PDIR=rendered -f tools/to_jsonl.awk ids.tsv > problems_rendered.jsonl
LC_ALL=C gawk -b -v PDIR=rendered -f tools/check_jsonl.awk problems_rendered.jsonl
```

Note: unlike this setup, the Claude agents of the rows 1-300 run had no system prompt (and no web access), were asked differently worded questions ("Look at the Math NAEP practices, and then tell me which practices needs to be used in which order to solve this problem..." and "If you had to choose one as the major practice, which one would you choose?") in one chat, answered in free text, and their top practice was the first practice named in answer 2. Results from this script are therefore not strictly comparable with the `claude_*` columns.

## Setup

```bash
pip install -r requirements.txt      # only the SDK you need; vLLM is already on the A100
export ANTHROPIC_API_KEY=...         # --provider anthropic
export OPENAI_API_KEY=...            # --provider openai
export GEMINI_API_KEY=...            # --provider gemini (GOOGLE_API_KEY also works)
```

### Docker (CUDA 13, for the GB300 or any NVIDIA machine)

`Dockerfile` builds on `vllm/vllm-openai:v0.20.0-cu130` (the newest vLLM release for CUDA 13; multi-arch, so arm64 on the GB300's Grace CPU) and adds git and `requirements.txt`, keeping vLLM, PyTorch and the CUDA libraries at the base image's versions. The image holds only the environment: `docker_run.sh` mounts the whole repository at `/workspace` and runs as your own user, so outputs land in your checkout, runs resume as usual, and a `git pull` needs no rebuild. The model download and compile caches go to `CACHE_DIR` (default `~/.cache`). The host needs an NVIDIA driver for CUDA 13 (580+) and the NVIDIA Container Toolkit.

```bash
bash docker_run.sh build                 # once
bash docker_run.sh run python3 -c "import torch; print(torch.cuda.device_count(), torch.cuda.get_device_name(0), 'CUDA', torch.version.cuda)"   # the GPU is visible in the container
bash docker_run.sh run python3 generate.py --provider local --model Qwen/Qwen3.5-122B-A10B-FP8 --rows 1-3 --dry-run
bash docker_run.sh                       # run_gb300.sh, all four steps, in the background
bash docker_run.sh status                # or: tail -f logs/step1.log
```

## Running

Always start with a dry run to see the exact prompts, then a few rows:

```bash
python3 generate.py --provider anthropic --rows 1-3 --dry-run
python3 generate.py --provider anthropic --rows 1-20
```

Full runs, from this folder on the A100:

```bash
PYTHONUNBUFFERED=1 nohup python3 generate.py --provider anthropic --workers 8 > claude_api.log 2>&1 &
PYTHONUNBUFFERED=1 nohup python3 generate.py --provider openai --model gpt-5 --workers 8 > openai.log 2>&1 &
PYTHONUNBUFFERED=1 nohup python3 generate.py --provider gemini --model gemini-2.5-pro --workers 8 > gemini.log 2>&1 &
VLLM_USE_FLASHINFER_SAMPLER=0 PYTHONUNBUFFERED=1 nohup python3 generate.py --provider local --num-gpus 1 \
    --column-prefix qwen3_30b_v3 --replace-columns qwen3_30b_v2 > qwen3_30b_v3_all.log 2>&1 &
```

Useful options:

| Option | Meaning |
|---|---|
| `--rows 301-400` | which data rows (default: all 3,395) |
| `--model` | model id; defaults: `claude-opus-5-5`, `gpt-5`, `gemini-2.5-pro`, `Qwen/Qwen3-30B-A3B-Instruct-2507` |
| `--column-prefix` | name of the output columns and of the run folder |
| `--workers` | problems run in parallel by the API providers (default 8) |
| `--max-retries-per-problem` | retries after a failed attempt, from prompt 1 (default 3, so at most 4 attempts) |
| `--retry-failed` | try problems that failed in an earlier invocation again, with a fresh set of attempts |
| `--merge-only` / `--no-merge` | only write the CSV columns from the logs / don't touch the CSV |
| `--replace-columns OLD_PREFIX` | when merging, turn the `OLD_PREFIX_*` columns into this run's columns in place (see Output columns) |
| `--no-ordering` | skip prompt 2 (the order): prompt 3 gets answer 1 in its own order, as in the two-prompt version; `<prefix>_ordering_reasoning` stays empty |
| `--effort` | Claude effort level (default `high`; Claude Opus 5.5 itself defaults to `medium`) |
| `--no-fallbacks` | Claude: turn off the server-side refusal fallback (on by default; if Opus 5.5 declines a request, the API answers with a fallback model and the log's `served_model` says which) |
| `--reasoning-effort` | OpenAI reasoning models |
| `--base-url` | any OpenAI-compatible server, e.g. a vLLM server (`--base-url http://localhost:8000/v1 --column-prefix qwen3_30b_server`) |
| `--gemini-include-thoughts` | log Gemini's thought summaries |
| `--temperature`, `--top-p`, `--top-k`, `--min-p`, `--seed` | sampling (local defaults follow Qwen's advice for the Instruct-2507 model: 0.7 / 0.8 / 20 / 0); for the local model each attempt and each prompt get their own seed (seed + 3 x earlier attempts + prompt number - 1; the first attempt of prompt 1 gets the same seed as in the two-prompt version), so a redo can differ |
| `--enable-thinking true` | for hybrid Qwen3 models (e.g. `Qwen/Qwen3-30B-A3B`); the thinking text is logged separately and is not part of the checked answer |

The OpenAI and Gemini default model names are only placeholders; check the current model names and pass `--model`.

## What is logged

Everything is kept under `runs/<prefix>/`:

- `manifest.json`: the settings of the run (provider, model, all three system prompts and user prompt templates with their hashes, generation parameters, the hash of `problems_rendered.jsonl`, the check rule, the output columns) and the environment (Python, package versions, git commit, host). A later invocation with a different prompt, model or parameters stops with an error, so one set of columns never mixes settings; use a new `--column-prefix`, or `--force`.
- `invocations.jsonl`: one line per invocation (command line, rows, settings, hardware settings).
- `rows/row_NNNNN.json`: one file per problem with the problem text and every attempt. Each attempt holds its calls (prompt 1, and prompts 2 and 3 if they were reached), the parsed answers, the combined analysis once answer 2 passed, which prompt failed (`failed_step`), the kind of failure (`failure_kind`: `invalid_answer` or `error`) and the reason (`failure_reason`). Each call holds the exact user prompt and request parameters, the answer text, the reasoning or thinking text when the model returns it, the full raw response, token usage, stop reason, the model that served it, and timestamps. To keep the row files small, the system prompt appears there by name and sha256 (`SYSTEM_PROMPT_1` / `_2` / `_3`); its full text is in `manifest.json`. For the local model the request also holds the chat-template-rendered prompt (with the system prompt shown by name) and the sampling settings with the seed. `final` gives the status (`ok` or `failed`; `pending_retry` while a run is in progress) and, for `ok`, the three answers as text and as parsed JSON, the combined analysis, the final ordering and the top practice.

Runs resume: rows whose status is `ok` or `failed` are skipped, so you can stop and restart, or run in batches with `--rows`. A row interrupted mid-way (`pending_retry`) continues with its attempt count. With `--retry-failed`, failed rows start again and their earlier attempts are kept under `earlier_failed_attempts`.

Before each merge the current `Problems.csv` is copied to `runs/_csv_backups/` (ignored by git). The merge matches rows by position (some `problem_id`s repeat) and checks the `problem_id` of every row. It writes the CSV with the same quoting and line endings as before, so the existing columns are unchanged byte for byte. After a merge, `git diff --stat` should show only the CSV changing.

On the A100, commit only what you mean to commit (no `git add .`), for example:

```bash
git add Data/Problems.csv Code/generate_practice_reasoning/runs/openAI
```

## Tested

The two-prompt version ran on the A100 (run `qwen3_30b_v2`, all 3,395 problems). The three-prompt version (prompt 2 and the merge changes) was written on the Windows machine, which has no Python, and has not been run yet: start with `--dry-run` and `--rows 1-3 --no-merge`, and look at one `rows/row_00001.json`, before a full run.

## NAEP Chapter 3 version (`--framework naep_ch3`)

`naep_chapter3.txt` is the text of Chapter 3 ("NAEP Mathematical Practices") of the NAEP 2026 Mathematics Framework, about 23k tokens, made from the PDF with `tools/naep_chapter_text.js` (Node). With `--framework naep_ch3`, that text is put in front of every system prompt, with a short note that Procedural Fluency comes from the NRC strands rather than NAEP. Everything after it is the same as the standard prompts, so the answers use the same six practices and formats. Figures are missing from the text and tables are flattened; the item text inside figures is partly garbled. The changed system prompts need a new `--column-prefix`.

## Wrong-answer diagnosis (`diagnose.py`, prompt 4)

For every wrong answer that at least `--min-students` students (default 2) gave on their first attempt without hints or answer views (`Results/practice_analysis/common_wrong_answers.csv`, from `Code/practice_analysis/wrong_answers.js`), one call asks which practice steps the student did correctly, where the student went wrong and which steps they did not reach. The prompt gets the item, its correct answer, the practice analysis from `Problems.csv` (`<practice prefix>_reasoning`, so run `generate.py` first), the wrong answer and how many students gave it.

The answer: a `reconstruction` (the calculation that produces the wrong answer), a status for each practice used (`correct`, `failed`, `not_reached`, `cannot_tell`), `error_type` (`practice`, `math_fact` or `guess`), the fact for `math_fact`, an explanation and a confidence. The check requires the steps to be the analysis's practices in order, at least one `failed` step for `practice` and `math_fact`, none for `guess`. Output: `Data/wrong_answer_diagnosis_<name>.csv`, logs in `runs/<name>/items/`.

```bash
python3 diagnose.py --provider local --model Qwen/Qwen3.5-122B-A10B-FP8 --practice-prefix qwen35_122b \
    --name qwen35_122b_diag --rows 1-300 --dry-run
```

Options: `--types fill,mc,all,order`, `--rows`, `--max-items` (quick tests), `--framework naep_ch3`, `--write-only` (rewrite the CSV from the logs).
