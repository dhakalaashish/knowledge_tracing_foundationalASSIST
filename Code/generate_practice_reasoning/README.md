# generate_practice_reasoning

Labels each problem in `Data/Problems.csv` with an LLM's view of which mathematical practices it needs, in which order, which ones it does not need, and which one is the top practice. It runs through an API (Claude, OpenAI, Gemini) or a local Qwen3-30B on vLLM.

## The two prompts

All prompts are in `prompts.py`. Each problem goes through two separate LLM calls, each a fresh conversation. Neither call sees `predicted_practice` or any other label.

| | Prompt 1: practice order | Prompt 2: top practice |
|---|---|---|
| System prompt | `SYSTEM_PROMPT_1`: the task, the six practices with the definitions and descriptors from `Code/augment_mathematical_practice.py` (copied verbatim), notes about the items, and the format of answer 1 | `SYSTEM_PROMPT_2`: the task, the same definitions and descriptors and notes, and the format of answer 2 |
| User prompt | `Q1_TEMPLATE`: *Using the practice definitions and descriptors, tell me which practices a student needs to use to solve this item, in the order the student uses them, and how the student uses each one. Then tell me which practices the student does not use, and why.* followed by the problem | `Q2_TEMPLATE`: the problem, answer 1 (the checked JSON, indented) as "Analysis of the practices a student uses to solve this item", and *Using the practice definitions and descriptors and this analysis, tell me which single practice is the top practice of this item, the one the item mainly assesses. Explain why it is the top practice and why it outweighs the other practices the student uses.* |
| Answer | the practices used, in order, each with why; the practices not used, each with why | the top practice, with why it is the top practice and outweighs the other practices used |
| Sent | always | only after answer 1 passed the JSON check |

Answer 1:

```json
{
"practices_used": [
  {"order": 1, "practice": "Representing", "why": "..."},
  {"order": 2, "practice": "Procedural Fluency", "why": "..."}
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
{"top_practice": "Representing", "why": "..."}
```

The JSON check (`common.AnswerChecker`) parses each answer with `json.loads`. The answer must be exactly one JSON object; a single ```` ```json ```` fence around it is accepted, but any other text before or after it fails. Answer 1 must list at least one practice as used, number the used practices 1, 2, 3... in order, name each of the six practices exactly once across the two lists, and give a non-empty "why" for every entry. Answer 2 must name one of the six practices, one that answer 1 listed as used, with a non-empty "why". If answer 1 fails, prompt 2 is not sent.

## Retries and the list of failed problems

An attempt is prompt 1 plus prompt 2. It fails if, in either prompt, the answer fails the JSON check (`invalid_answer`) or the call itself fails (`error`: output cut off at the token limit, empty answer, API error or refusal). A failed attempt is retried from prompt 1 in fresh conversations. One counter covers both prompts and both kinds of failure: a problem gets at most 1 + `--max-retries-per-problem` attempts (default 3 retries, so 4 attempts). After that its status is `failed` and it is not tried again unless you pass `--retry-failed`.

At the end of every invocation the script writes `runs/<prefix>/failed_problems.csv`, listing every failed problem in the run folder: `row`, `problem_id`, `attempts`, which prompt failed in each attempt (`failed_steps`), the kind of failure (`failure_kinds`), and the reasons (`last_failure_reason`, `all_failure_reasons`). Failed problems get no values in the CSV columns.

(The API providers also retry a single HTTP request on 429/5xx/connection errors inside the SDK, `--max-retries`, default 8, before a call counts as failed.)

## Output columns

| Column | Content |
|---|---|
| `<prefix>_reasoning` | answer 1 as compact JSON (read it back with `json.loads`) |
| `<prefix>_top_practice` | `top_practice` from answer 2 |
| `<prefix>_top_practice_reasoning` | `why` from answer 2 |

Default prefixes: `claude_api`, `openAI`, `gemini`, `qwen3_30b`. The existing `claude_*` columns from the agent run are never touched. Only rows that finished with status `ok` are written.

## Files

| File | Purpose |
|---|---|
| `prompts.py` | both system prompts and both user prompts |
| `generate.py` | command-line entry point: runs both prompts, checks the answers, logs everything, merges the columns into the CSV |
| `providers.py` | the four backends: `anthropic`, `openai` (also any OpenAI-compatible server), `gemini`, `local` (offline vLLM) |
| `common.py` | problem loading, building the prompts, the JSON check, logs, CSV merge |
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
CUDA_VISIBLE_DEVICES=0,1,2,3 PYTHONUNBUFFERED=1 nohup python3 generate.py --provider local \
    --num-gpus 4 --cache-dir /data1/ > qwen3_30b.log 2>&1 &
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
| `--effort` | Claude effort level (default `high`; Claude Opus 5.5 itself defaults to `medium`) |
| `--no-fallbacks` | Claude: turn off the server-side refusal fallback (on by default; if Opus 5.5 declines a request, the API answers with a fallback model and the log's `served_model` says which) |
| `--reasoning-effort` | OpenAI reasoning models |
| `--base-url` | any OpenAI-compatible server, e.g. a vLLM server (`--base-url http://localhost:8000/v1 --column-prefix qwen3_30b_server`) |
| `--gemini-include-thoughts` | log Gemini's thought summaries |
| `--temperature`, `--top-p`, `--top-k`, `--min-p`, `--seed` | sampling (local defaults follow Qwen's advice for the Instruct-2507 model: 0.7 / 0.8 / 20 / 0); for the local model each attempt and each prompt get their own seed (seed + 2 x earlier attempts + prompt number - 1), so a redo can differ |
| `--enable-thinking true` | for hybrid Qwen3 models (e.g. `Qwen/Qwen3-30B-A3B`); the thinking text is logged separately and is not part of the checked answer |

The OpenAI and Gemini default model names are only placeholders; check the current model names and pass `--model`.

## What is logged

Everything is kept under `runs/<prefix>/`:

- `manifest.json`: the settings of the run (provider, model, both full system prompts and both user prompt templates with their hashes, generation parameters, the hash of `problems_rendered.jsonl`, the check rule, the output columns) and the environment (Python, package versions, git commit, host). A later invocation with a different prompt, model or parameters stops with an error, so one set of columns never mixes settings; use a new `--column-prefix`, or `--force`.
- `invocations.jsonl`: one line per invocation (command line, rows, settings, hardware settings).
- `rows/row_NNNNN.json`: one file per problem with the problem text and every attempt. Each attempt holds its calls (prompt 1, and prompt 2 if it was reached), the parsed answers, which prompt failed (`failed_step`), the kind of failure (`failure_kind`: `invalid_answer` or `error`) and the reason (`failure_reason`). Each call holds the exact user prompt and request parameters, the answer text, the reasoning or thinking text when the model returns it, the full raw response, token usage, stop reason, the model that served it, and timestamps. To keep the row files small, the system prompt appears there by name and sha256 (`SYSTEM_PROMPT_1` / `SYSTEM_PROMPT_2`); its full text is in `manifest.json`. For the local model the request also holds the chat-template-rendered prompt (with the system prompt shown by name) and the sampling settings with the seed. `final` gives the status (`ok` or `failed`; `pending_retry` while a run is in progress) and, for `ok`, both answers as text and as parsed JSON.

Runs resume: rows whose status is `ok` or `failed` are skipped, so you can stop and restart, or run in batches with `--rows`. A row interrupted mid-way (`pending_retry`) continues with its attempt count. With `--retry-failed`, failed rows start again and their earlier attempts are kept under `earlier_failed_attempts`.

Before each merge the current `Problems.csv` is copied to `runs/_csv_backups/` (ignored by git). The merge matches rows by position (some `problem_id`s repeat) and checks the `problem_id` of every row. It writes the CSV with the same quoting and line endings as before, so the existing columns are unchanged byte for byte. After a merge, `git diff --stat` should show only the CSV changing.

On the A100, commit only what you mean to commit (no `git add .`), for example:

```bash
git add Data/Problems.csv Code/generate_practice_reasoning/runs/openAI
```

## Untested

These scripts were written on the Windows machine, which has no Python, so they have not been run yet. Start with `--dry-run` and then `--rows 1-3` for each provider and look at one `rows/row_00001.json` before a full run.
