#!/usr/bin/env bash
# Build and run the CUDA 13 container (see Dockerfile). Run from anywhere; paths are relative to this script.
#
#   bash docker_run.sh build              build the image (once; downloads about 10 GB)
#   bash docker_run.sh                    all four steps of run_gb300.sh, in the background (like nohup: it
#                                         keeps going after you log out, and restarts up to twice if it crashes)
#   bash docker_run.sh 1 3                only steps 1 and 3, in the background
#   SMOKE=1 bash docker_run.sh            the smoke test (6 problems, all four steps), in the background
#   bash docker_run.sh status             one progress snapshot (monitor.sh once)
#   bash docker_run.sh stop               stop the background run (starting it again resumes)
#   bash docker_run.sh shell              an interactive shell in the container
#   bash docker_run.sh run <command...>   one command in the container, e.g. the dry run or the 3-row test
#
# Passed into the container when set: MODEL, MAX_TOKENS, MAX_MODEL_LEN, SMOKE, SMOKE_ROWS (see run_gb300.sh), HF_TOKEN.
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
for v in MODEL MAX_TOKENS MAX_MODEL_LEN HF_TOKEN SMOKE SMOKE_ROWS; do
  if [ -n "${!v:-}" ]; then OPTS+=(-e "$v"); fi
done
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
  status)
    bash monitor.sh once ;;
  ""|[1-4]*)
    if docker ps -q --filter "name=^${NAME}$" | grep -q .; then
      echo "$NAME is already running (bash docker_run.sh status / stop)"; exit 1
    fi
    docker rm "$NAME" >/dev/null 2>&1 || true   # the container of an earlier, finished run
    # --restart on-failure:2: if a step crashes (e.g. a vLLM error), Docker starts run_gb300.sh again, which
    # resumes every step where it stopped. A run stopped with "docker_run.sh stop" is not restarted.
    docker run -d --restart on-failure:2 --name "$NAME" "${OPTS[@]}" "$IMAGE" bash run_gb300.sh "$@" >/dev/null
    if [ "${SMOKE:-0}" = "1" ]; then
      echo "started the smoke test in $NAME (steps: ${*:-1 2 3 4})"
      echo "watch:   SMOKE=1 bash monitor.sh     when done: bash smoke_check.sh"
    else
      echo "started $NAME (steps: ${*:-1 2 3 4})"
      echo "watch:   bash monitor.sh        or: tail -f logs/step${1:-1}.log"
    fi ;;
  *)
    sed -n '2,15p' "$0"; exit 1 ;;
esac
