#!/usr/bin/env bash
# All GB300 runs, one after another (one GPU, so never in parallel):
#   1. labeling with the standard prompts          -> Problems.csv columns qwen35_122b_*
#   2. labeling with NAEP Chapter 3 in the prompts  -> Problems.csv columns qwen35_122b_ch3_*
#   3. wrong-answer diagnosis, standard prompts     -> Data/wrong_answer_diagnosis_qwen35_122b_diag.csv
#   4. wrong-answer diagnosis, Chapter 3 prompts    -> Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv
# Every step resumes where it stopped, so after an interruption just start the script again.
#
# Usage (from Code/generate_practice_reasoning):
#   bash run_gb300.sh                 all four steps
#   bash run_gb300.sh 1 3             only steps 1 and 3
#   THINKING=false bash run_gb300.sh  without thinking (faster)
# Logs: logs/step<N>.log

set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs

MODEL="${MODEL:-Qwen/Qwen3.5-122B-A10B-FP8}"
THINKING="${THINKING:-true}"
STEPS="${*:-1 2 3 4}"

COMMON=(--provider local --model "$MODEL" --num-gpus 1 --max-model-len 65536)
if [ "$THINKING" = "true" ]; then
  # Qwen's usual sampling advice for thinking mode; thinking text needs a larger output limit
  COMMON+=(--enable-thinking true --max-tokens 16384 --temperature 0.6 --top-p 0.95)
else
  COMMON+=(--enable-thinking false --max-tokens 8192)
fi

for step in $STEPS; do
  echo "=== step $step started $(date)" | tee -a "logs/step$step.log"
  case "$step" in
    1) python3 -u generate.py "${COMMON[@]}" --column-prefix qwen35_122b --no-ordering ;;
    2) python3 -u generate.py "${COMMON[@]}" --framework naep_ch3 --column-prefix qwen35_122b_ch3 --no-ordering ;;
    3) python3 -u diagnose.py "${COMMON[@]}" --practice-prefix qwen35_122b --name qwen35_122b_diag ;;
    4) python3 -u diagnose.py "${COMMON[@]}" --framework naep_ch3 --practice-prefix qwen35_122b_ch3 --name qwen35_122b_ch3_diag ;;
    *) echo "unknown step $step"; exit 1 ;;
  esac >> "logs/step$step.log" 2>&1
  echo "=== step $step finished $(date)" | tee -a "logs/step$step.log"
done
