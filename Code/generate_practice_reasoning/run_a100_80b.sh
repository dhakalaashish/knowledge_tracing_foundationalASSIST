#!/usr/bin/env bash
# Qwen3-Next-80B-A3B-Thinking, 4-bit (cyankiwi/Qwen3-Next-80B-A3B-Thinking-AWQ-4bit), on one A100 80 GB: the
# descriptors-only pipeline, to compare by hand with the Qwen3.5-122B runs.
#   1. labeling, descriptors only (no examples; practices, order, top practice: the prompts of the 122B's
#      qwen35_122b_noex run)                       -> Problems.csv columns qwen3next80b_think_noex_*
#   2. wrong-answer diagnosis, descriptors-only prompts, from step 1's practices
#                                                  -> Data/wrong_answer_diagnosis_qwen3next80b_think_noex_diag.csv
# Every problem, and every wrong answer given by at least MIN_STUDENTS (default 3) students on their first attempt
# (12,841 answers, as in the 122B's diagnosis). The model always thinks (it is the Thinking model); sampling as Qwen
# recommends for it (temperature 0.6, top-p 0.95, top-k 20). Every step resumes where it stopped: after an
# interruption, start the script again.
#
# Compare with: labels qwen35_122b_noex_* (same prompts). The 122B's diagnosis that exists used the Chapter 3
# prompts and Chapter 3 practices (wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv), so the diagnoses differ in
# prompt and labels as well as model.
#
# Usage (from Code/generate_practice_reasoning):
#   SMOKE=1 bash run_a100_80b.sh        smoke test: both steps on 6 problems (one of each question type); writes only
#                                       to runs/smoke*/ (a copy of Problems.csv), Data/ is not touched
#   nohup bash run_a100_80b.sh > logs/a100_80b.out 2>&1 &     the full run (steps 1 then 2)
#   bash run_a100_80b.sh 2              only step 2
# Logs: logs/a100_80b_step<N>.log (smoke test: logs/smoke_a100_80b_step<N>.log)

set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
export VLLM_USE_FLASHINFER_SAMPLER="${VLLM_USE_FLASHINFER_SAMPLER:-0}"   # as for the KT runs on this A100

MODEL="${MODEL:-cyankiwi/Qwen3-Next-80B-A3B-Thinking-AWQ-4bit}"
MAX_TOKENS="${MAX_TOKENS:-32768}"          # Qwen's recommended output length (thinking + answer)
MAX_MODEL_LEN="${MAX_MODEL_LEN:-65536}"    # system prompt (~9k) + user prompt + MAX_TOKENS
SMOKE="${SMOKE:-0}"
STEPS="${*:-1 2}"
# Conversations per vLLM batch (speed only, answers do not depend on it). Results are written when a batch ends,
# so a crash loses at most one batch; with thinking on an A100 a batch takes a while.
LABEL_BATCH="${LABEL_BATCH:-512}"
DIAG_BATCH="${DIAG_BATCH:-1024}"
MIN_STUDENTS="${MIN_STUDENTS:-3}"
NAME=qwen3next80b_think_noex

COMMON=(--provider local --model "$MODEL" --num-gpus 1 --max-model-len "$MAX_MODEL_LEN"
        --max-tokens "$MAX_TOKENS" --temperature 0.6 --top-p 0.95 --top-k 20 --min-p 0)

if [ "$SMOKE" = "1" ]; then
  TAG=smoke_
  LOG=logs/smoke_a100_80b_step
  SMOKE_ROWS="${SMOKE_ROWS:-1,6,9,809,2221,2232}"
  rm -rf "runs/smoke_${NAME}" "runs/smoke_${NAME}_diag" runs/smoke_a100 logs/smoke_a100_80b_step*
  mkdir -p runs/smoke_a100
  cp ../../Data/Problems.csv runs/smoke_a100/Problems.csv
  GEN_EXTRA=(--rows "$SMOKE_ROWS" --problems-csv runs/smoke_a100/Problems.csv)
  DIAG_EXTRA=(--rows "$SMOKE_ROWS" --problems-csv runs/smoke_a100/Problems.csv --min-students "$MIN_STUDENTS")
  diag_out() { echo "runs/smoke_a100/wrong_answer_diagnosis_$1.csv"; }
else
  TAG=
  LOG=logs/a100_80b_step
  GEN_EXTRA=(--batch-size "$LABEL_BATCH")
  DIAG_EXTRA=(--batch-size "$DIAG_BATCH" --min-students "$MIN_STUDENTS")
  diag_out() { echo "../../Data/wrong_answer_diagnosis_$1.csv"; }
fi
if [ "${RETRY_FAILED:-0}" = "1" ]; then
  GEN_EXTRA+=(--retry-failed)
  DIAG_EXTRA+=(--retry-failed)
fi

for step in $STEPS; do
  printf '\n=== step %s started %s\n' "$step" "$(date)" | tee -a "$LOG$step.log"
  case "$step" in
    1) python3 -u generate.py "${COMMON[@]}" "${GEN_EXTRA[@]}" --framework no_examples \
         --column-prefix "${TAG}${NAME}" ;;
    2) python3 -u diagnose.py "${COMMON[@]}" "${DIAG_EXTRA[@]}" --framework no_examples \
         --practice-prefix "${TAG}${NAME}" --name "${TAG}${NAME}_diag" --out "$(diag_out "${TAG}${NAME}_diag")" ;;
    *) echo "unknown step $step"; exit 1 ;;
  esac >> "$LOG$step.log" 2>&1
  printf '\n=== step %s finished %s\n' "$step" "$(date)" | tee -a "$LOG$step.log"
done
