#!/usr/bin/env bash
# Build and run the CUDA 13 container (see Dockerfile). Run from anywhere; paths are relative to this script.
#
#   bash docker_run.sh build              build the image (once; downloads about 10 GB)
#   bash docker_run.sh download           download the model (~125 GB) in the background; again resumes it
#   bash docker_run.sh check-model        is the whole model downloaded?
#   bash docker_run.sh                    run_gb300.sh (steps 1 2 3 6), in the background (like nohup: it
#                                         keeps going after you log out, and restarts up to twice if it crashes)
#   bash docker_run.sh 1 3                only steps 1 and 3, in the background
#   bash docker_run.sh 9                  step 9: diagnose every remaining wrong answer (122B, Chapter 3)
#   SMOKE=1 bash docker_run.sh            the smoke test (6 problems, steps 1 2 3 6), in the background
#   bash docker_run.sh status             one progress snapshot (monitor.sh once)
#   bash docker_run.sh stop               stop the background run (starting it again resumes)
#   bash docker_run.sh shell              an interactive shell in the container
#   bash docker_run.sh run <command...>   one command in the container, e.g. the dry run or the 3-row test
#   bash docker_run.sh kt <args...>       the KT benchmark in the background (container practice-kt, from Code/):
#                                         python3 kt_practice_benchmark.py <args...>; log: Code/kt_gb300.log.
#                                         Model: MODEL, default cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit
#                                         (MODEL=<that id> bash docker_run.sh download  first)
#   bash docker_run.sh kt-stop            stop the KT run (starting it again resumes)
#   KT_NAME=<name> KT_LOG=<file>          per-run container name and log, to run two KT runs side by side
#   bash docker_run.sh kt-both <args...>  both lookup runs on the one GPU from one command, in the background:
#                                         stage, profile + lookup, then (once its model is loaded) practice +
#                                         lookup, each with KT_UTIL (default 0.45) of the GPU memory; evaluate when
#                                         both are done. Progress: Code/kt_both.log.  Stop: kt-both-stop
#                                         KT_SET=all: the runs with every diagnosed wrong answer (after step 9);
#                                         logs then end in _all (kt_both_all.log, ...)
#                                         KT_PAIR=filtered: the filtered and IRT runs instead (containers kt-filtered,
#                                         kt-irt; logs kt_both_filtered.log, kt_filtered.log, kt_irt.log); before the
#                                         GPU starts, every prompt of both is built and its length checked
#   bash docker_run.sh agent4cd-after <args...>   Agent4CD + cognitive student modeling on the KT benchmark
#                                         (Code/agent4cd_practice), in the background: inputs + a dry run now, then
#                                         wait until kt-filtered or kt-irt has finished, then the agents (container
#                                         kt-agent4cd, its own vLLM server with KT_UTIL of the GPU memory), then the
#                                         tables. Progress: Code/kt_both_agent4cd.log; agents: Code/kt_agent4cd.log.
#                                         Stop: agent4cd-stop (starting again resumes)
#
# Passed into the container when set: MODEL, MAX_TOKENS, MAX_MODEL_LEN, SMOKE, SMOKE_ROWS, RETRY_FAILED (see run_gb300.sh), HF_TOKEN,
# HF_HUB_OFFLINE. Runs (and smoke tests) are offline by default: vLLM reads the model from the cache and never
# contacts Hugging Face, whose anonymous API limit is shared by everyone behind the same IP address.
# CACHE_DIR: host folder for the model download and compile caches (default ~/.cache; the model needs ~130 GB).
# The background run keeps going after you log out; its output is in logs/step<N>.log.

set -euo pipefail
cd "$(dirname "$0")"

IMAGE="${IMAGE:-practice-reasoning:cu130}"
NAME="${NAME:-practice-gb300}"
REPO="$(cd ../.. && pwd)"
CACHE_DIR="${CACHE_DIR:-$HOME/.cache}"
mkdir -p "$CACHE_DIR" logs

# The container writes the model download into $CACHE_DIR/huggingface and results into the repository, as you.
# Stop early, with a clear message, if a folder there belongs to someone else (e.g. root).
for d in "$CACHE_DIR" "$CACHE_DIR/huggingface" "$CACHE_DIR/huggingface/hub" "$REPO" "$REPO/Data" "$PWD/runs"; do
  if [ -e "$d" ] && [ ! -w "$d" ]; then
    echo "error: you ($(id -un)) cannot write to $d (owner: $(stat -c %U "$d"))."
    echo "Use a cache folder of your own, e.g.:  export CACHE_DIR=\$HOME/aashish/cache   then run this again."
    exit 1
  fi
done

# Normal Docker: run as your own user id, so files written into the repository are yours, not root's.
# Rootless Docker: the container's root already is you on the host, and --user would map to a stranger.
USER_OPT=(--user "$(id -u):$(id -g)")
SECOPTS=$(docker info --format '{{.SecurityOptions}}' 2>/dev/null || true)
case "$SECOPTS" in
  *rootless*) USER_OPT=() ;;
  *userns*) echo "warning: Docker uses user-namespace remapping, so the container may not be able to write" \
                 "your files; if it fails, tell me the output of: docker info --format '{{.SecurityOptions}}'" ;;
esac

# Which GPU the container gets: GPU=<index> (as nvitop / nvidia-smi number them), or by default the one with the
# most memory. The GB300 machine also has a small 24 GB card (GPU 0); the model must go on the GB300 (GPU 1).
if [ -z "${GPU:-}" ]; then
  GPU=$(python3 - 2>/dev/null <<'EOF' || true
import pynvml as n
n.nvmlInit()
mem = [n.nvmlDeviceGetMemoryInfo(n.nvmlDeviceGetHandleByIndex(i)).total for i in range(n.nvmlDeviceGetCount())]
print(max(range(len(mem)), key=mem.__getitem__))
EOF
)
fi
if [ -n "$GPU" ]; then
  GPU_OPT=(--gpus "device=$GPU")
  echo "using GPU $GPU (inside the container it is the only GPU, device 0)" >&2
else
  GPU_OPT=(--gpus all)
  echo "warning: could not tell the GPUs apart; the container sees all of them (set GPU=<index> to choose)" >&2
fi

OPTS=("${GPU_OPT[@]}" --ipc=host --ulimit memlock=-1 --ulimit stack=67108864
      ${USER_OPT[@]+"${USER_OPT[@]}"}
      -v "$REPO:/workspace"
      -v "$CACHE_DIR:/home/app/.cache"
      -w /workspace/Code/generate_practice_reasoning)
# the host's time zone, so the time estimates in the logs are in local time
if [ -e /etc/localtime ]; then OPTS+=(-v /etc/localtime:/etc/localtime:ro); fi
for v in MODEL MAX_TOKENS MAX_MODEL_LEN HF_TOKEN HF_HUB_OFFLINE SMOKE SMOKE_ROWS RETRY_FAILED V5_ROWS MIN_STUDENTS; do
  if [ -n "${!v:-}" ]; then OPTS+=(-e "$v"); fi
done
MODEL_ID="${MODEL:-Qwen/Qwen3.5-122B-A10B-FP8}"   # the same default as run_gb300.sh

# Is the whole model in the cache: config.json and every weight file its index lists (files still downloading
# have no entry in snapshots/ yet)? Needs only the host's python3.
model_cached() {
  python3 - "$CACHE_DIR/huggingface/hub" "$MODEL_ID" <<'PYEOF'
import glob, json, os, sys
hub, model = sys.argv[1], sys.argv[2]
snaps = sorted(glob.glob(os.path.join(hub, "models--" + model.replace("/", "--"), "snapshots", "*")))
if not snaps:
    print(f"model {model} not found in {hub}"); sys.exit(1)
for s in snaps:
    idx = os.path.join(s, "model.safetensors.index.json")
    if not (os.path.exists(idx) and os.path.exists(os.path.join(s, "config.json"))):
        continue
    with open(idx) as f:
        shards = sorted(set(json.load(f)["weight_map"].values()))
    missing = [x for x in shards if not os.path.exists(os.path.join(s, x))]
    if missing:
        print(f"model {model} incomplete: {len(missing)} of {len(shards)} weight files missing"); sys.exit(1)
    print(f"model {model} complete: {len(shards)} weight files in {s}"); sys.exit(0)
print(f"model {model} incomplete: no config.json / weight index yet"); sys.exit(1)
PYEOF
}

# Start one KT run in the background: kt_start <container name> <log file in Code/> <kt_practice_benchmark.py args...>
# Offline, as the labeling runs; the paper's sampling path as on the A100 (FlashInfer sampler off); the KT run resumes
# by itself, so a crash restarts it (up to twice); -w: the KT scripts live in Code/.
kt_start() {
  local name="$1" log="$2"; shift 2
  local model="${MODEL:-cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit}"
  if docker ps -q --filter "name=^${name}$" | grep -q .; then
    echo "$name is already running (tail -f ../$log; KT_NAME=$name bash docker_run.sh kt-stop)"; exit 1
  fi
  if [ "${SKIP_MODEL_CHECK:-0}" != "1" ] && ! MODEL_ID="$model" model_cached; then
    echo "Download the model first: MODEL=$model bash docker_run.sh download   (then: MODEL=$model bash docker_run.sh check-model)"; exit 1
  fi
  docker rm "$name" >/dev/null 2>&1 || true
  docker run -d --restart on-failure:2 --name "$name" "${OPTS[@]}" -w /workspace/Code \
    -e "HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}" -e "TRANSFORMERS_OFFLINE=${HF_HUB_OFFLINE:-1}" \
    -e VLLM_USE_FLASHINFER_SAMPLER=0 -e "KT_MODEL_ID=$model" -e "KT_LOG=$log" \
    "$IMAGE" bash -c 'python3 -u kt_practice_benchmark.py "$@" >> "$KT_LOG" 2>&1' kt "$@" >/dev/null
  echo "started $name: kt_practice_benchmark.py $*  (log: Code/$log)"
}

# The two runs of kt-both: KT_PAIR=lookup (default; KT_SET=all for the _all runs) or KT_PAIR=filtered
kt_pair() {
  KS=""; KD=""; if [ "${KT_SET:-common}" = "all" ]; then KS="_all"; KD="-all"; fi
  if [ "${KT_PAIR:-lookup}" = "filtered" ]; then
    A_NAME=kt-filtered; A_CMD=infer-filtered; A_LOG=kt_filtered.log; A_COND=filtered; A_DESC="filtered"
    B_NAME=kt-irt; B_CMD=infer-irt; B_LOG=kt_irt.log; B_COND=irt; B_DESC="IRT"
    BOTH_LOG=kt_both_filtered.log
  else
    A_NAME=kt-profile; A_CMD=infer-profile-lookup${KD}; A_LOG=kt_profile_lookup${KS}.log; A_COND=""; A_DESC="profile + lookup"
    B_NAME=kt-practice; B_CMD=infer-practice-lookup${KD}; B_LOG=kt_practice_lookup${KS}.log; B_COND=""; B_DESC="practice + lookup"
    BOTH_LOG=kt_both${KS}.log
  fi
}

TTY=()   # interactive only when started from a terminal (not under nohup)
if [ -t 0 ] && [ -t 1 ]; then TTY=(-it); fi

case "${1:-}" in
  build)
    docker build -t "$IMAGE" ${VLLM_IMAGE:+--build-arg "VLLM_IMAGE=$VLLM_IMAGE"} . ;;
  shell)
    docker run --rm -it "${OPTS[@]}" "$IMAGE" bash ;;
  run)
    shift
    docker run --rm ${TTY[@]+"${TTY[@]}"} "${OPTS[@]}" "$IMAGE" "$@" ;;
  stop)
    docker stop "$NAME" ;;
  download)
    docker rm practice-download >/dev/null 2>&1 || true
    docker run -d --name practice-download "${OPTS[@]}" "$IMAGE" python3 -c       "from huggingface_hub import snapshot_download; print(snapshot_download('$MODEL_ID', max_workers=8)); print('DOWNLOAD DONE')" >/dev/null
    echo "downloading $MODEL_ID in the background (container practice-download)"
    echo "follow:  docker logs -f practice-download      size so far: du -sh $CACHE_DIR/huggingface"
    echo "done when 'bash docker_run.sh check-model' says complete"
    [ -n "${HF_TOKEN:-}" ] || echo "tip: with a Hugging Face token (export HF_TOKEN=...) the rate limit is yours alone, not your IP's" ;;
  check-model)
    model_cached ;;
  status)
    bash monitor.sh once ;;
  kt)
    shift
    # KT_NAME / KT_LOG: container name and log file (in Code/), so two KT runs can share the GPU, each with its own
    kt_start "${KT_NAME:-practice-kt}" "${KT_LOG:-kt_gb300.log}" "$@"
    echo "watch:   tail -f ../${KT_LOG:-kt_gb300.log}      stop: KT_NAME=${KT_NAME:-practice-kt} bash docker_run.sh kt-stop" ;;
  kt-both)
    kt_pair
    # both lookup runs side by side on the one GPU, from one command; the rest runs in the background (survives
    # logging out): stage once -> profile + lookup -> (when its model is loaded) practice + lookup -> wait for both
    # -> evaluate. Progress: ../kt_both${KS}.log; each run: ../kt_profile_lookup${KS}.log, ../kt_practice_lookup${KS}.log
    shift
    MODEL_ID="${MODEL:-cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit}"
    if [ "${SKIP_MODEL_CHECK:-0}" != "1" ] && ! model_cached; then
      echo "Download the model first: MODEL=$MODEL_ID bash docker_run.sh download   (then: MODEL=$MODEL_ID bash docker_run.sh check-model)"; exit 1
    fi
    if [ -n "$KS" ] && [ ! -f ../../Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag_all.csv ]; then
      echo "Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag_all.csv is missing: diagnose every wrong answer first (bash docker_run.sh 9)"; exit 1
    fi
    if [ "${KT_PAIR:-lookup}" = "filtered" ] && [ ! -f ../../Results/kt_profile/problem_irt.json ]; then
      echo "Results/kt_profile/problem_irt.json is missing: git pull (or node Code/tools/fit_irt.js)"; exit 1
    fi
    for n in "$A_NAME" "$B_NAME"; do
      if docker ps -q --filter "name=^${n}$" | grep -q .; then echo "$n is already running (bash docker_run.sh kt-both-stop)"; exit 1; fi
    done
    nohup bash "$PWD/$(basename "$0")" _kt-both "$@" >> ../$BOTH_LOG 2>&1 &
    echo "started both runs in the background (pid $!): stage -> $A_DESC -> $B_DESC -> evaluate"
    echo "progress: tail -f ../$BOTH_LOG     each run: tail -f ../$A_LOG  /  ../$B_LOG"
    echo "stop both: ${KT_PAIR:+KT_PAIR=$KT_PAIR }bash docker_run.sh kt-both-stop   (starting kt-both again resumes both)" ;;
  _kt-both)
    shift
    kt_pair
    UTIL="${KT_UTIL:-0.45}"   # each run's share of the GPU memory
    echo "=== kt-both started $(date); runs: $A_DESC, $B_DESC; arguments: $*; GPU memory per run: $UTIL"
    # 1. stage once, before either run (both would otherwise write the staged data at the same time)
    docker run --rm "${OPTS[@]}" -w /workspace/Code "$IMAGE" python3 -u kt_practice_benchmark.py stage "$@"
    # 1b. new conditions: build every prompt of both and check its length on the CPU first, so a mistake stops here
    for c in $A_COND $B_COND; do
      if ! docker run --rm "${OPTS[@]}" -w /workspace/Code -e HF_HUB_OFFLINE=1 -e TRANSFORMERS_OFFLINE=1 \
             -e "KT_MODEL_ID=${MODEL:-cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit}" "$IMAGE" \
             python3 -u kt_practice_benchmark.py check-length --condition "$c" "$@"; then
        echo "check-length --condition $c failed: nothing started ($(date))"; exit 1
      fi
    done
    # 2. the first run, then wait until its model is loaded (two vLLM engines that start at the same moment can
    #    both misjudge the free memory), or until it has stopped (e.g. nothing left to do)
    LOG_START=$(stat -c %s ../$A_LOG 2>/dev/null || echo 0)   # only this start's lines count
    kt_start "$A_NAME" "$A_LOG" "$A_CMD" "$@" --gpu-memory-utilization "$UTIL"
    for i in $(seq 1 120); do
      if tail -c +$((LOG_START + 1)) ../$A_LOG 2>/dev/null | \
           grep -qE "GPU KV cache size|Maximum concurrency|Processed prompts|All predictions already completed"; then
        echo "$A_DESC: model loaded ($(date))"; break
      fi
      if [ "$(docker inspect -f '{{.State.Running}}' "$A_NAME" 2>/dev/null)" != "true" ]; then
        echo "$A_DESC: container stopped before loading; see ../$A_LOG"; break
      fi
      sleep 15
    done
    # 3. the second run
    kt_start "$B_NAME" "$B_LOG" "$B_CMD" "$@" --gpu-memory-utilization "$UTIL"
    # 4. wait for both to finish (a restart after a crash counts as still running), then the tables
    for n in "$A_NAME" "$B_NAME"; do
      while [ "$(docker inspect -f '{{.State.Status}}' "$n" 2>/dev/null)" = "running" ] || \
            [ "$(docker inspect -f '{{.State.Restarting}}' "$n" 2>/dev/null)" = "true" ]; do sleep 60; done
      echo "$n finished ($(date)), exit code $(docker inspect -f '{{.State.ExitCode}}' "$n" 2>/dev/null)"
    done
    docker run --rm "${OPTS[@]}" -w /workspace/Code "$IMAGE" python3 -u kt_practice_benchmark.py evaluate "$@"
    echo "=== kt-both finished $(date)" ;;
  agent4cd-after)
    shift
    MODEL_ID="${MODEL:-cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit}"
    if [ "${SKIP_MODEL_CHECK:-0}" != "1" ] && ! model_cached; then
      echo "Download the model first: MODEL=$MODEL_ID bash docker_run.sh download"; exit 1
    fi
    if docker ps -q --filter "name=^kt-agent4cd$" | grep -q . || pgrep -f "docker_run.sh _agent4cd-after" >/dev/null; then
      echo "Agent4CD is already running or waiting (bash docker_run.sh agent4cd-stop)"; exit 1
    fi
    nohup bash "$PWD/$(basename "$0")" _agent4cd-after "$@" >> ../kt_both_agent4cd.log 2>&1 &
    echo "started in the background (pid $!): inputs + dry run -> wait for kt-filtered or kt-irt to finish -> Agent4CD -> tables"
    echo "progress: tail -f ../kt_both_agent4cd.log     agents (once started): tail -f ../kt_agent4cd.log"
    echo "stop: bash docker_run.sh agent4cd-stop   (starting it again resumes)" ;;
  _agent4cd-after)
    shift
    UTIL="${KT_UTIL:-0.45}"
    MODEL_ID="${MODEL:-cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit}"
    echo "=== agent4cd-after started $(date); arguments: $*; GPU memory: $UTIL"
    # 1. the inputs (NCDM on the other students, mastery per bin, profiles) and one student's prompts, no LLM:
    #    a mistake stops here, before any waiting
    if ! docker run --rm "${OPTS[@]}" -w /workspace/Code/agent4cd_practice "$IMAGE" bash -c \
         'mkdir -p logs && python3 -u kt_benchmark.py "$@" && python3 -u run_kt_agent.py --dry-run "$@" > logs/kt_dry_run.txt && head -3 logs/kt_dry_run.txt' kt "$@"; then
      echo "inputs or dry run failed: nothing started ($(date))"; exit 1
    fi
    echo "dry run OK; one student's prompts: Code/agent4cd_practice/logs/kt_dry_run.txt"
    # 2. wait until one of the two runs has finished (a restart after a crash counts as running)
    running() {
      case "$(docker inspect -f '{{.State.Status}} {{.State.Restarting}}' "$1" 2>/dev/null || echo gone)" in
        running*|*true) return 0 ;;
        *) return 1 ;;
      esac
    }
    echo "waiting for kt-filtered or kt-irt to finish ($(date))"
    while running kt-filtered && running kt-irt; do sleep 60; done
    echo "a GPU slot is free ($(date))"
    # 3. the agents: their own vLLM server for the same model, then run_kt_agent.py (resumes after a crash)
    docker rm kt-agent4cd >/dev/null 2>&1 || true
    docker run -d --restart on-failure:2 --name kt-agent4cd "${OPTS[@]}" -w /workspace/Code/agent4cd_practice \
      -e "HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}" -e "TRANSFORMERS_OFFLINE=${HF_HUB_OFFLINE:-1}" \
      -e VLLM_USE_FLASHINFER_SAMPLER=0 -e "KT_MODEL_ID=$MODEL_ID" -e "KT_UTIL=$UTIL" \
      "$IMAGE" bash -c 'bash run_kt_gb300.sh "$@" >> ../kt_agent4cd.log 2>&1' kt "$@" >/dev/null
    echo "started kt-agent4cd ($(date)); log: Code/kt_agent4cd.log"
    while running kt-agent4cd; do sleep 60; done
    code=$(docker inspect -f '{{.State.ExitCode}}' kt-agent4cd 2>/dev/null || echo "?")
    echo "kt-agent4cd finished ($(date)), exit code $code"
    # 4. the tables, with the runs that are complete
    if [ "$code" = "0" ]; then
      docker run --rm "${OPTS[@]}" -w /workspace/Code "$IMAGE" python3 -u kt_practice_benchmark.py evaluate "$@" \
        --runs paper,baseline,practice,profile,profile_lookup,agent4cd
    fi
    echo "=== agent4cd-after finished $(date)" ;;
  agent4cd-stop)
    pkill -f "docker_run.sh _agent4cd-after" 2>/dev/null || true
    docker stop kt-agent4cd 2>/dev/null || true ;;
  kt-both-stop)
    kt_pair
    pkill -f "docker_run.sh _kt-both" 2>/dev/null || true
    docker stop "$A_NAME" "$B_NAME" 2>/dev/null || true ;;
  kt-stop)
    docker stop "${KT_NAME:-practice-kt}" ;;
  ""|[1-9]*)
    if docker ps -q --filter "name=^${NAME}$" | grep -q .; then
      echo "$NAME is already running (bash docker_run.sh status / stop)"; exit 1
    fi
    if [ "${SKIP_MODEL_CHECK:-0}" != "1" ] && ! model_cached; then
      echo "Download the model first: bash docker_run.sh download   (then: bash docker_run.sh check-model)"; exit 1
    fi
    # offline: load the model from the cache without asking Hugging Face anything (HF_HUB_OFFLINE=0 to allow it)
    OPTS+=(-e "HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}" -e "TRANSFORMERS_OFFLINE=${HF_HUB_OFFLINE:-1}")
    docker rm "$NAME" >/dev/null 2>&1 || true   # the container of an earlier, finished run
    # --restart on-failure:2: if a step crashes (e.g. a vLLM error), Docker starts run_gb300.sh again, which
    # resumes every step where it stopped. A run stopped with "docker_run.sh stop" is not restarted.
    docker run -d --restart on-failure:2 --name "$NAME" "${OPTS[@]}" "$IMAGE" bash run_gb300.sh "$@" >/dev/null
    if [ "${SMOKE:-0}" = "1" ]; then
      echo "started the smoke test in $NAME (steps: ${*:-1 2 3 6})"
      echo "watch:   SMOKE=1 bash monitor.sh     when done: bash smoke_check.sh"
    else
      echo "started $NAME (steps: ${*:-1 2 3 6})"
      echo "watch:   bash monitor.sh        or: tail -f logs/step${1:-1}.log"
    fi ;;
  *)
    sed -n '2,20p' "$0"; exit 1 ;;
esac
