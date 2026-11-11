#!/usr/bin/env bash
# All GB300 runs, one after another (one GPU, so never in parallel):
#   1. labeling with the standard prompts          -> Problems.csv columns qwen35_122b_*
#   2. labeling with NAEP Chapter 3 in the prompts  -> Problems.csv columns qwen35_122b_ch3_*
#   3. wrong-answer diagnosis, standard prompts     -> Data/wrong_answer_diagnosis_qwen35_122b_diag.csv
#   4. wrong-answer diagnosis, Chapter 3 prompts    -> Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv
# Steps 1 and 2 use all three prompts (practices, order, top practice), like the Qwen3-30B v3/v4 runs,
# so step 1 compares directly with v4 (the same standard prompts). Every call uses thinking.
# Every step resumes where it stopped, so after an interruption just start the script again.
#
# Usage (from Code/generate_practice_reasoning):
#   bash run_gb300.sh                       all four steps
#   bash run_gb300.sh 1 3                   only steps 1 and 3
#   SMOKE=1 bash run_gb300.sh               smoke test: all four steps on 6 problems, one of each question type
#   MAX_TOKENS=49152 bash run_gb300.sh      a larger output limit (thinking + answer) per call
# Logs: logs/step<N>.log (smoke test: logs/smoke_step<N>.log)
#
# Smoke test: rows 1 (fill-in, numeric), 6 (fill-in, drop-down), 9 (fill-in, algebraic expression), 809 (order),
# 2221 (multiple choice) and 2232 (select all), each with wrong answers given by at least 2 students. Exactly the
# settings of the real run, but everything goes to runs/smoke*/ (the labels into a copy of Problems.csv there,
# the diagnoses into runs/smoke/), so Data/ is not touched. Each smoke test starts afresh.
#
# Token limits: each call is one fresh conversation, so its context is the system prompt (about 9k tokens
# standard, about 32k with Chapter 3) + the user prompt (a few thousand) + the output. MAX_MODEL_LEN must cover
# all three; 131072 leaves room for MAX_TOKENS up to about 90k even with Chapter 3. Qwen3.5 supports 262144.

set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs

MODEL="${MODEL:-Qwen/Qwen3.5-122B-A10B-FP8}"
MAX_TOKENS="${MAX_TOKENS:-32768}"         # Qwen's recommended output length for thinking mode
MAX_MODEL_LEN="${MAX_MODEL_LEN:-131072}"
SMOKE="${SMOKE:-0}"
STEPS="${*:-1 2 3 4}"

# thinking on, with Qwen's sampling advice for thinking mode
COMMON=(--provider local --model "$MODEL" --num-gpus 1 --max-model-len "$MAX_MODEL_LEN"
        --enable-thinking true --max-tokens "$MAX_TOKENS" --temperature 0.6 --top-p 0.95)

if [ "$SMOKE" = "1" ]; then
  TAG=smoke_
  LOG=logs/smoke_step
  SMOKE_ROWS="${SMOKE_ROWS:-1,6,9,809,2221,2232}"
  rm -rf runs/smoke runs/smoke_qwen35_122b runs/smoke_qwen35_122b_ch3 runs/smoke_qwen35_122b_diag \
         runs/smoke_qwen35_122b_ch3_diag logs/smoke_step*
  mkdir -p runs/smoke
  cp ../../Data/Problems.csv runs/smoke/Problems.csv
  GEN_EXTRA=(--rows "$SMOKE_ROWS" --problems-csv runs/smoke/Problems.csv)
  DIAG_EXTRA=(--rows "$SMOKE_ROWS" --problems-csv runs/smoke/Problems.csv)
  diag_out() { echo "runs/smoke/wrong_answer_diagnosis_$1.csv"; }
else
  TAG=
  LOG=logs/step
  GEN_EXTRA=()
  DIAG_EXTRA=()
  diag_out() { echo "../../Data/wrong_answer_diagnosis_$1.csv"; }
fi

for step in $STEPS; do
  echo "=== step $step started $(date)" | tee -a "$LOG$step.log"
  touch "$LOG$step.started"   # monitor.sh measures the speed from here
  case "$step" in
    1) python3 -u generate.py "${COMMON[@]}" ${GEN_EXTRA[@]+"${GEN_EXTRA[@]}"} --column-prefix "${TAG}qwen35_122b" ;;
    2) python3 -u generate.py "${COMMON[@]}" ${GEN_EXTRA[@]+"${GEN_EXTRA[@]}"} --framework naep_ch3 \
         --column-prefix "${TAG}qwen35_122b_ch3" ;;
    3) python3 -u diagnose.py "${COMMON[@]}" ${DIAG_EXTRA[@]+"${DIAG_EXTRA[@]}"} --practice-prefix "${TAG}qwen35_122b" \
         --name "${TAG}qwen35_122b_diag" --out "$(diag_out "${TAG}qwen35_122b_diag")" ;;
    4) python3 -u diagnose.py "${COMMON[@]}" ${DIAG_EXTRA[@]+"${DIAG_EXTRA[@]}"} --framework naep_ch3 \
         --practice-prefix "${TAG}qwen35_122b_ch3" --name "${TAG}qwen35_122b_ch3_diag" \
         --out "$(diag_out "${TAG}qwen35_122b_ch3_diag")" ;;
    *) echo "unknown step $step"; exit 1 ;;
  esac >> "$LOG$step.log" 2>&1
  echo "=== step $step finished $(date)" | tee -a "$LOG$step.log"
done

if [ "$SMOKE" = "1" ]; then
  echo "=== smoke test done. Check with: bash smoke_check.sh"
fi
