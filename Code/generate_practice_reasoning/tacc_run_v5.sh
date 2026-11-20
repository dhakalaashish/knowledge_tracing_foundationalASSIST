#!/bin/bash
# v5 labels (label_v5.py) on TACC Stampede3, queue h100 (1 node with 4x H100 96 GB), started through the lab's job
# wrapper from the work directory that holds slurm/ and this repository:
#
#   cd $WORK/stampede3
#   bash slurm/gen_job/job_setup.sh FoundationalASSIST/config/job.env            # test: rows 1-300
#   bash slurm/gen_job/job_setup.sh FoundationalASSIST/config/job_full.env       # full run, rows 301-3395, one job
#   (or job_full_a.env + job_full_b.env: the same rows split over two nodes at once)
#
# The wrapper loads the job.env (its V5_ROWS etc. become environment variables), sets PROJECT_ROOT (the repository
# root), copies this script into a scratch work folder and runs it there, on the compute node.
#
# What it does:
#   1. vLLM comes from the official Docker image, pulled once with Apptainer to $SCRATCH/containers (TACC has no
#      Docker). v0.20.0-cu130 is the vLLM the GB300 runs used; it needs NVIDIA driver >= 580, else v0.20.0 (CUDA
#      12.9, driver >= 575). VLLM_IMAGE in the job.env overrides the choice.
#   2. The model is downloaded once to $SCRATCH/hf_cache (export HF_TOKEN before submitting to avoid Hugging Face's
#      rate limit; it is passed in, never written to a file). $SCRATCH is purged after 10 days without use.
#   3. label_v5.py runs with the settings of step 8 of run_gb300.sh (thinking on, 32768 output tokens, temperature
#      0.6, top-p 0.95, wrong answers given by >= 3 students), on all GPUs of the node (tensor parallel). It is
#      stopped V5_RESERVE_MIN minutes (default 30) before the job's wall-time limit, so there is always time for 4.
#   4. The results are written (Data/Problems.csv columns qwen35_122b_v5_*, Data/wrong_answer_diagnosis_
#      qwen35_122b_v5.csv, runs/qwen35_122b_v5/) and committed and pushed to GitHub, also after a time-out or an
#      error (whatever finished is kept). V5_PUSH=0 in the job.env turns the push off; V5_PUSH_ROW_LOGS=0 leaves the
#      per-row logs (every call, with the thinking) out of the commit.
#   Runs resume: rows already done are skipped, so a job that stopped at its limit is simply submitted again.
#
# One-time setup for the push (on the login node; see the README): git-lfs on PATH, git user.name and user.email set
# in this clone, and a GitHub token saved with the "store" credential helper (a batch job cannot type a password).
set -euo pipefail
: "${PROJECT_ROOT:?run this through slurm/gen_job/job_setup.sh, which sets PROJECT_ROOT}"
CODE="$PROJECT_ROOT/Code/generate_practice_reasoning"
cd "$CODE"
mkdir -p logs

MODEL="${MODEL:-Qwen/Qwen3.5-122B-A10B-FP8}"
V5_ROWS="${V5_ROWS:-1-300}"
PREFIX="${V5_PREFIX:-qwen35_122b_v5}"
MAX_TOKENS="${MAX_TOKENS:-32768}"
MAX_MODEL_LEN="${MAX_MODEL_LEN:-131072}"
MIN_STUDENTS="${MIN_STUDENTS:-3}"
BATCH="${V5_BATCH:-1024}"
RESERVE_MIN="${V5_RESERVE_MIN:-30}"
DIAG_OUT="../../Data/wrong_answer_diagnosis_${PREFIX}.csv"
LOG="$CODE/logs/tacc_v5_rows_${V5_ROWS}.log"   # full path: the push step works from the repository root
EXTRA=()
if [ "${V5_RETRY_FAILED:-0}" = "1" ]; then EXTRA+=(--retry-failed); fi
export GIT_TERMINAL_PROMPT=0          # never wait for a password in a batch job: fail instead
# nor for an SSH key passphrase (an ssh-agent key still works); only when no SSH command is set already
export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-ssh -o BatchMode=yes}"
say() { printf '%s\n' "$*" | tee -a "$LOG"; }

# ---------------------------------------------------------------- 1. container
# V5_NO_CONTAINER=1: run with the machine's own python3 and vLLM instead of Apptainer, for a test outside TACC (e.g.
# on the A100, with PROJECT_ROOT set by hand and a smaller MODEL / MAX_MODEL_LEN / MAX_TOKENS).
NO_CONTAINER="${V5_NO_CONTAINER:-0}"
nvidia-smi
NUM_GPUS=$(nvidia-smi -L | wc -l)
DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1)
MAJOR=${DRIVER%%.*}
if [ "$NO_CONTAINER" = "1" ]; then
  VLLM_IMAGE="(none: this machine's python3)"
  in_container() { (cd "$CODE" && "$@"); }
else
command -v apptainer >/dev/null 2>&1 || module load tacc-apptainer
if [ -z "${VLLM_IMAGE:-}" ]; then
  if [ "$MAJOR" -ge 580 ]; then VLLM_IMAGE=docker://vllm/vllm-openai:v0.20.0-cu130     # the GB300's vLLM
  elif [ "$MAJOR" -ge 575 ]; then VLLM_IMAGE=docker://vllm/vllm-openai:v0.20.0         # same vLLM, CUDA 12.9
  else
    echo "NVIDIA driver $DRIVER is older than 575. Set VLLM_IMAGE in the job.env to a vLLM image (>= 0.17, needed for" \
         "Qwen3.5) built for this driver's CUDA version (nvidia-smi shows it), then submit again." >&2
    exit 1
  fi
fi
mkdir -p "$SCRATCH/containers" "$SCRATCH/apptainer_cache" "$SCRATCH/hf_cache" "$SCRATCH/v5_home"
export APPTAINER_CACHEDIR="$SCRATCH/apptainer_cache"
SIF="$SCRATCH/containers/$(basename "${VLLM_IMAGE#docker://}" | tr ':' '_').sif"
if [ ! -s "$SIF" ]; then
  echo "pulling $VLLM_IMAGE to $SIF (first time only; several minutes)"
  apptainer pull "$SIF" "$VLLM_IMAGE"
fi
# Only these variables enter the container (--cleanenv keeps the host's modules and library paths out).
export APPTAINERENV_HF_HOME="$SCRATCH/hf_cache"
export APPTAINERENV_PYTHONUNBUFFERED=1
if [ -n "${HF_TOKEN:-}" ]; then export APPTAINERENV_HF_TOKEN="$HF_TOKEN"; fi
# --writable-tmpfs: some vLLM/FlashInfer kernels write next to their own files the first time they are used
# --home: torch.compile, Triton and FlashInfer caches go to $SCRATCH, not the small $HOME
in_container() {
  apptainer exec --nv --cleanenv --writable-tmpfs --home "$SCRATCH/v5_home" \
    --bind "$PROJECT_ROOT" --bind "$SCRATCH" --pwd "$CODE" "$SIF" "$@"
}
fi

# ---------------------------------------------------------------- 3. the run, stopped before the wall-time limit
to_seconds() {   # squeue's time left: [D-]HH:MM:SS, MM:SS or SS
  local t=$1 d=0 h=0 m=0 s=0
  case "$t" in *-*) d=${t%%-*}; t=${t#*-} ;; esac
  IFS=: read -r a b c <<< "$t"
  if [ -n "$c" ]; then h=$a; m=$b; s=$c; elif [ -n "$b" ]; then m=$a; s=$b; else s=$a; fi
  echo $(( 10#$d * 86400 + 10#$h * 3600 + 10#$m * 60 + 10#$s ))
}
LEFT=$(squeue -h -j "${SLURM_JOB_ID:-0}" -o %L 2>/dev/null || true)
if [[ "$LEFT" =~ ^[0-9:-]+$ ]]; then
  RUN_SECS=$(( $(to_seconds "$LEFT") - RESERVE_MIN * 60 ))
else
  RUN_SECS=$(( 47 * 3600 ))           # time left unknown (e.g. run by hand): at most 47 h
fi
if [ "$RUN_SECS" -lt 900 ]; then
  echo "only ${LEFT:-?} left in this job, not enough to run (and keep ${RESERVE_MIN} min to save and push)" >&2
  exit 1
fi

printf '\n=== v5 rows %s started %s (job %s, %s GPUs, driver %s, %s; labeling stops after %s min)\n' "$V5_ROWS" \
  "$(date)" "${SLURM_JOB_ID:-?}" "$NUM_GPUS" "$DRIVER" "$VLLM_IMAGE" "$(( RUN_SECS / 60 ))" | tee -a "$LOG"
if [ "$NO_CONTAINER" = "1" ]; then RUNNER=(); else
  RUNNER=(apptainer exec --nv --cleanenv --writable-tmpfs --home "$SCRATCH/v5_home"
          --bind "$PROJECT_ROOT" --bind "$SCRATCH" --pwd "$CODE" "$SIF"); fi
set +e
timeout --signal=TERM --kill-after=180 "$RUN_SECS" \
  ${RUNNER[@]+"${RUNNER[@]}"} \
    python3 -u label_v5.py --provider local --model "$MODEL" --num-gpus "$NUM_GPUS" \
      --max-model-len "$MAX_MODEL_LEN" --enable-thinking true --max-tokens "$MAX_TOKENS" --temperature 0.6 --top-p 0.95 \
      --batch-size "$BATCH" --min-students "$MIN_STUDENTS" --rows "$V5_ROWS" --column-prefix "$PREFIX" \
      --diagnosis-out "$DIAG_OUT" ${EXTRA[@]+"${EXTRA[@]}"} 2>&1 | tee -a "$LOG"
STATUS=${PIPESTATUS[0]}
set -e
case "$STATUS" in
  0)   say "=== v5 rows $V5_ROWS finished $(date)" ;;
  124) say "=== v5 rows $V5_ROWS stopped $(date): time limit near; finished rows are kept, submit the job again to continue" ;;
  *)   say "=== v5 rows $V5_ROWS FAILED (exit $STATUS) $(date); finished rows are kept" ;;
esac
if [ "$STATUS" != 0 ]; then
  # label_v5.py writes the CSVs only when it ends normally: write them from the row logs (no model needed)
  in_container python3 -u label_v5.py --provider local --merge-only --column-prefix "$PREFIX" \
    --diagnosis-out "$DIAG_OUT" 2>&1 | tee -a "$LOG" || say "writing the CSVs from the logs failed"
fi

# ---------------------------------------------------------------- 4. commit and push
push_results() {
  if [ "${V5_PUSH:-1}" != "1" ]; then say "V5_PUSH=0: results not pushed"; return 0; fi
  cd "$PROJECT_ROOT"
  if ! git lfs version >/dev/null 2>&1; then
    say "git-lfs not found on this node: NOT pushed (the CSVs are Git LFS files). Push from the login node, or put git-lfs on PATH."
    return 1
  fi
  if [ -z "$(git config user.email)" ] || [ -z "$(git config user.name)" ]; then
    say "git user.name / user.email not set in this clone: NOT pushed (set them once on the login node)"
    return 1
  fi
  exec 9> "$PROJECT_ROOT/.git/v5_push.lock"
  flock 9                                      # two jobs share this clone: one commit and push at a time
  local run="Code/generate_practice_reasoning/runs/$PREFIX" paths=() p n_ok branch
  if [ "${V5_PUSH_ROW_LOGS:-1}" = "1" ]; then paths=("$run"); else
    paths=("$run/manifest.json" "$run/failed_problems.csv" "$run/invocations.jsonl"); fi
  paths+=("Data/Problems.csv" "Data/wrong_answer_diagnosis_${PREFIX}.csv")
  for p in "${paths[@]}"; do [ -e "$p" ] && git add -- "$p"; done
  if git diff --cached --quiet; then say "nothing new to commit"; flock -u 9; return 0; fi
  n_ok=$(grep -l -m1 -E '^    "status": "ok"' "$run"/rows/*.json 2>/dev/null | wc -l)
  git commit -q -m "v5 labels ($PREFIX): rows $V5_ROWS, job ${SLURM_JOB_ID:-manual} (exit $STATUS); $n_ok problems done in all"
  branch=$(git rev-parse --abbrev-ref HEAD)
  for attempt in 1 2 3; do
    if git push origin "HEAD:$branch" 2>&1 | tee -a "$LOG"; then
      [ "${PIPESTATUS[0]}" = 0 ] && { say "pushed to $branch: $n_ok problems done"; flock -u 9; return 0; }
    fi
    say "push failed (attempt $attempt); pulling the branch (rebase) and trying again"
    # --autostash: other uncommitted edits in the clone (e.g. parameter files) are set aside and put back
    if ! git pull -q --rebase --autostash origin "$branch" 2>&1 | tee -a "$LOG" || [ "${PIPESTATUS[0]}" != 0 ]; then
      git rebase --abort 2>/dev/null || true
      say "pull --rebase failed (the same files changed on GitHub, or no network/login). The commit is kept in this clone; push it by hand from the login node."
      flock -u 9; return 1
    fi
    sleep 20
  done
  say "push failed 3 times; the commit is kept in this clone: push it by hand from the login node"
  flock -u 9; return 1
}
PUSHED=0
push_results && PUSHED=1 || true
cd "$CODE"
# the job's exit code: 0 when the run finished (or stopped for time) and the results are on GitHub
if [ "$STATUS" = 0 ] || [ "$STATUS" = 124 ]; then [ "$PUSHED" = 1 ] || [ "${V5_PUSH:-1}" != "1" ] || exit 2; exit 0; fi
exit "$STATUS"
