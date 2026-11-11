#!/usr/bin/env bash
# Build and run the CUDA 13 container (see Dockerfile). Run from anywhere; paths are relative to this script.
#
#   bash docker_run.sh build              build the image (once; downloads about 10 GB)
#   bash docker_run.sh                    all four steps of run_gb300.sh, in the background (like nohup: it
#                                         keeps going after you log out, and restarts up to twice if it crashes)
#   bash docker_run.sh 1 3                only steps 1 and 3, in the background
#   bash docker_run.sh status             one progress snapshot (monitor.sh once)
#   bash docker_run.sh stop               stop the background run (starting it again resumes)
#   bash docker_run.sh shell              an interactive shell in the container
#   bash docker_run.sh run <command...>   one command in the container, e.g. the dry run or the 3-row test
#
# Passed into the container when set: MODEL, MAX_TOKENS, MAX_MODEL_LEN (see run_gb300.sh) and HF_TOKEN.
# CACHE_DIR: host folder for the model download and compile caches (default ~/.cache; the model needs ~130 GB).
# The background run keeps going after you log out; its output is in logs/step<N>.log.

set -euo pipefail
cd "$(dirname "$0")"

IMAGE="${IMAGE:-practice-reasoning:cu130}"
NAME="${NAME:-practice-gb300}"
REPO="$(cd ../.. && pwd)"
CACHE_DIR="${CACHE_DIR:-$HOME/.cache}"
mkdir -p "$CACHE_DIR" logs

OPTS=(--gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864
      --user "$(id -u):$(id -g)"
      -v "$REPO:/workspace"
      -v "$CACHE_DIR:/home/app/.cache"
      -w /workspace/Code/generate_practice_reasoning)
for v in MODEL MAX_TOKENS MAX_MODEL_LEN HF_TOKEN; do
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
    echo "started $NAME (steps: ${*:-1 2 3 4})"
    echo "watch:   bash monitor.sh        or: tail -f logs/step${1:-1}.log" ;;
  *)
    sed -n '2,15p' "$0"; exit 1 ;;
esac
