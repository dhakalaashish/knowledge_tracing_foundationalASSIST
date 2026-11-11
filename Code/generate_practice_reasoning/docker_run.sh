#!/usr/bin/env bash
# Build and run the CUDA 13 container (see Dockerfile). Run from anywhere; paths are relative to this script.
#
#   bash docker_run.sh build              build the image (once; downloads about 10 GB)
#   bash docker_run.sh download           download the model (~125 GB) in the background; again resumes it
#   bash docker_run.sh check-model        is the whole model downloaded?
#   bash docker_run.sh                    run_gb300.sh (steps 1 5 2 3 4), in the background (like nohup: it
#                                         keeps going after you log out, and restarts up to twice if it crashes)
#   bash docker_run.sh 1 3                only steps 1 and 3, in the background
#   SMOKE=1 bash docker_run.sh            the smoke test (6 problems, steps 1 5 2 3 4), in the background
#   bash docker_run.sh status             one progress snapshot (monitor.sh once)
#   bash docker_run.sh stop               stop the background run (starting it again resumes)
#   bash docker_run.sh shell              an interactive shell in the container
#   bash docker_run.sh run <command...>   one command in the container, e.g. the dry run or the 3-row test
#
# Passed into the container when set: MODEL, MAX_TOKENS, MAX_MODEL_LEN, SMOKE, SMOKE_ROWS (see run_gb300.sh), HF_TOKEN,
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
for v in MODEL MAX_TOKENS MAX_MODEL_LEN HF_TOKEN HF_HUB_OFFLINE SMOKE SMOKE_ROWS; do
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
  ""|[1-6]*)
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
      echo "started the smoke test in $NAME (steps: ${*:-1 5 2 3 4})"
      echo "watch:   SMOKE=1 bash monitor.sh     when done: bash smoke_check.sh"
    else
      echo "started $NAME (steps: ${*:-1 5 2 3 4})"
      echo "watch:   bash monitor.sh        or: tail -f logs/step${1:-1}.log"
    fi ;;
  *)
    sed -n '2,20p' "$0"; exit 1 ;;
esac
