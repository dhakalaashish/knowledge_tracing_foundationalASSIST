#!/usr/bin/env bash
# All GB300 runs, one after another (one GPU, so never in parallel):
#   1. labeling, standard prompts (v4: with examples) -> Problems.csv columns qwen35_122b_*
#   2. labeling, no examples (v3 prompts)              -> Problems.csv columns qwen35_122b_noex_*
#   3. labeling, NAEP Chapter 3 + standard prompts     -> Problems.csv columns qwen35_122b_ch3_*
#   4. wrong-answer diagnosis from step 1's practices  -> Data/wrong_answer_diagnosis_qwen35_122b_diag.csv
#   5. wrong-answer diagnosis from step 2's practices  -> Data/wrong_answer_diagnosis_qwen35_122b_noex_diag.csv
#   6. wrong-answer diagnosis from step 3's practices  -> Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv
# By default only the Chapter 3 diagnosis (step 6) runs; steps 4 and 5 run only when asked for (bash run_gb300.sh 4).
# The diagnoses cover wrong answers given by at least MIN_STUDENTS (default 3) students on their first attempt.
# Each diagnosis uses the same prompt version as its labeling step. The labeling steps use all three prompts
# (practices, order, top practice), like the Qwen3-30B v3/v4 runs: step 1 has exactly v4's prompts and step 2
# exactly v3's, so each compares directly with the 30B run of the same prompts. Every call uses thinking.
# Every step resumes where it stopped, so after an interruption just start the script again.
#
# Usage (from Code/generate_practice_reasoning):
#   bash run_gb300.sh                       steps 1 2 3 6: the three labelings, then the Chapter 3 diagnosis
#   bash run_gb300.sh 4 5                   only steps 4 and 5 (in the order given)
#   SMOKE=1 bash run_gb300.sh               smoke test: steps 1 2 3 6 on 6 problems, one of each question type
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
STEPS="${*:-1 2 3 6}"
# Conversations per vLLM batch. Each batch (and each prompt within a labeling batch) waits for its slowest answer,
# and with thinking a few answers run to 10k-32k tokens alone at the end while the GPU idles; fewer, bigger
# batches mean fewer such waits. Results are written when a batch ends, so a crash loses at most one batch.
# Settings for speed only: the answers do not depend on them.
LABEL_BATCH="${LABEL_BATCH:-1024}"
DIAG_BATCH="${DIAG_BATCH:-2048}"
# Diagnose the wrong answers given by at least this many students (first attempts): 3 gives about 10,400 wrong
# answers, which still cover about 94% of the students behind wrong answers given by 2 or more.
MIN_STUDENTS="${MIN_STUDENTS:-3}"

# thinking on, with Qwen's sampling advice for thinking mode
COMMON=(--provider local --model "$MODEL" --num-gpus 1 --max-model-len "$MAX_MODEL_LEN"
        --enable-thinking true --max-tokens "$MAX_TOKENS" --temperature 0.6 --top-p 0.95)

if [ "$SMOKE" = "1" ]; then
  TAG=smoke_
  LOG=logs/smoke_step
  SMOKE_ROWS="${SMOKE_ROWS:-1,6,9,809,2221,2232}"
  rm -rf runs/smoke runs/smoke_qwen35_122b runs/smoke_qwen35_122b_ch3 runs/smoke_qwen35_122b_diag \
         runs/smoke_qwen35_122b_ch3_diag runs/smoke_qwen35_122b_noex runs/smoke_qwen35_122b_noex_diag \
         logs/smoke_step*
  mkdir -p runs/smoke
  cp ../../Data/Problems.csv runs/smoke/Problems.csv
  GEN_EXTRA=(--rows "$SMOKE_ROWS" --problems-csv runs/smoke/Problems.csv)
  DIAG_EXTRA=(--rows "$SMOKE_ROWS" --problems-csv runs/smoke/Problems.csv)
  diag_out() { echo "runs/smoke/wrong_answer_diagnosis_$1.csv"; }
else
  TAG=
  LOG=logs/step
  GEN_EXTRA=(--batch-size "$LABEL_BATCH")
  DIAG_EXTRA=(--batch-size "$DIAG_BATCH" --min-students "$MIN_STUDENTS")
  diag_out() { echo "../../Data/wrong_answer_diagnosis_$1.csv"; }
fi
# RETRY_FAILED=1: give the items that failed all their attempts a fresh set of attempts (their earlier attempts
# stay in the logs); everything already ok is skipped as usual. E.g. RETRY_FAILED=1 bash run_gb300.sh 3 6
# relabels step 3's failed problems, then diagnoses their wrong answers and retries step 6's failed ones.
if [ "${RETRY_FAILED:-0}" = "1" ]; then
  GEN_EXTRA+=(--retry-failed)
  DIAG_EXTRA+=(--retry-failed)
fi

for step in $STEPS; do
  # each marker on a line of its own: vLLM's progress bars end without a newline
  printf '\n=== step %s started %s\n' "$step" "$(date)" | tee -a "$LOG$step.log"
  touch "$LOG$step.started"   # monitor.sh measures the speed from here
  case "$step" in
    # labeling: standard (v4 prompts), no examples (v3 prompts), NAEP Chapter 3
    1) python3 -u generate.py "${COMMON[@]}" ${GEN_EXTRA[@]+"${GEN_EXTRA[@]}"} --column-prefix "${TAG}qwen35_122b" ;;
    2) python3 -u generate.py "${COMMON[@]}" ${GEN_EXTRA[@]+"${GEN_EXTRA[@]}"} --framework no_examples \
         --column-prefix "${TAG}qwen35_122b_noex" ;;
    3) python3 -u generate.py "${COMMON[@]}" ${GEN_EXTRA[@]+"${GEN_EXTRA[@]}"} --framework naep_ch3 \
         --column-prefix "${TAG}qwen35_122b_ch3" ;;
    # diagnosis of the wrong answers, each with the same prompts and the practices of steps 1, 2 and 3
    4) python3 -u diagnose.py "${COMMON[@]}" ${DIAG_EXTRA[@]+"${DIAG_EXTRA[@]}"} --practice-prefix "${TAG}qwen35_122b" \
         --name "${TAG}qwen35_122b_diag" --out "$(diag_out "${TAG}qwen35_122b_diag")" ;;
    5) python3 -u diagnose.py "${COMMON[@]}" ${DIAG_EXTRA[@]+"${DIAG_EXTRA[@]}"} --framework no_examples \
         --practice-prefix "${TAG}qwen35_122b_noex" --name "${TAG}qwen35_122b_noex_diag" \
         --out "$(diag_out "${TAG}qwen35_122b_noex_diag")" ;;
    6) python3 -u diagnose.py "${COMMON[@]}" ${DIAG_EXTRA[@]+"${DIAG_EXTRA[@]}"} --framework naep_ch3 \
         --practice-prefix "${TAG}qwen35_122b_ch3" --name "${TAG}qwen35_122b_ch3_diag" \
         --out "$(diag_out "${TAG}qwen35_122b_ch3_diag")" ;;
    *) echo "unknown step $step"; exit 1 ;;
  esac >> "$LOG$step.log" 2>&1
  printf '\n=== step %s finished %s\n' "$step" "$(date)" | tee -a "$LOG$step.log"
done

if [ "$SMOKE" = "1" ]; then
  echo "=== smoke test done. Check with: bash smoke_check.sh"
fi
