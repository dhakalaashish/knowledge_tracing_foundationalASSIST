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
#   MAX_TOKENS=49152 bash run_gb300.sh      a larger output limit (thinking + answer) per call
# Logs: logs/step<N>.log
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
STEPS="${*:-1 2 3 4}"

# thinking on, with Qwen's sampling advice for thinking mode
COMMON=(--provider local --model "$MODEL" --num-gpus 1 --max-model-len "$MAX_MODEL_LEN"
        --enable-thinking true --max-tokens "$MAX_TOKENS" --temperature 0.6 --top-p 0.95)

for step in $STEPS; do
  echo "=== step $step started $(date)" | tee -a "logs/step$step.log"
  touch "logs/step$step.started"   # monitor.sh measures the speed from here
  case "$step" in
    1) python3 -u generate.py "${COMMON[@]}" --column-prefix qwen35_122b ;;
    2) python3 -u generate.py "${COMMON[@]}" --framework naep_ch3 --column-prefix qwen35_122b_ch3 ;;
    3) python3 -u diagnose.py "${COMMON[@]}" --practice-prefix qwen35_122b --name qwen35_122b_diag ;;
    4) python3 -u diagnose.py "${COMMON[@]}" --framework naep_ch3 --practice-prefix qwen35_122b_ch3 --name qwen35_122b_ch3_diag ;;
    *) echo "unknown step $step"; exit 1 ;;
  esac >> "logs/step$step.log" 2>&1
  echo "=== step $step finished $(date)" | tee -a "logs/step$step.log"
done
