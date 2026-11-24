#!/usr/bin/env bash
# Agent4CD + cognitive student modeling on the KT benchmark, inside the GB300 container (docker_run.sh agent4cd-after
# starts it): the inputs (kt_benchmark.py; skipped when already built), a vLLM server for the same 4-bit model with
# KT_UTIL of the GPU memory, the agents (run_kt_agent.py), then the server is stopped.
#   bash run_kt_gb300.sh --out-dir /workspace/Results/kt_practice_main --n 100
set -euo pipefail
cd "$(dirname "$0")"
MODEL="${KT_MODEL_ID:-cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit}"
UTIL="${KT_UTIL:-0.45}"
mkdir -p logs

echo "=== $(date): inputs"
python3 -u kt_benchmark.py "$@"

echo "=== $(date): vLLM server for $MODEL (GPU memory $UTIL), log: Code/agent4cd_practice/logs/vllm_kt.log"
vllm serve "$MODEL" --port 8000 --gpu-memory-utilization "$UTIL" --max-model-len 32768 \
    --enable-prefix-caching > logs/vllm_kt.log 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null || true; wait $SERVER 2>/dev/null || true' EXIT
for i in $(seq 1 180); do
  if python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/v1/models', timeout=5)" 2>/dev/null; then
    echo "server ready ($(date))"; break
  fi
  if ! kill -0 "$SERVER" 2>/dev/null; then
    echo "the vLLM server stopped while loading:"; tail -40 logs/vllm_kt.log; exit 1
  fi
  if [ "$i" = 180 ]; then echo "the vLLM server is not ready after 30 minutes"; tail -40 logs/vllm_kt.log; exit 1; fi
  sleep 10
done

echo "=== $(date): agents"
python3 -u run_kt_agent.py "$@"
echo "=== $(date): done"
