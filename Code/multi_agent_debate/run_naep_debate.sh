#!/bin/bash
# Multi-agent debate on the NAEP ground-truth items: build dataset -> debates (both answer orders)
# -> judge -> aggregate + evaluate.
#
# Usage (from Code/):
#   bash multi_agent_debate/run_naep_debate.sh <run_name> [number_of_items]
# Examples:
#   bash multi_agent_debate/run_naep_debate.sh pilot 1    # 1 item, 30 debates
#   bash multi_agent_debate/run_naep_debate.sh full       # all 35 items, 1,050 debates
#
# Needs a running vLLM server (see README.md). Rerunning the same command resumes: finished
# debates and judgements are kept.
set -euo pipefail

name=${1:?"give a run name, e.g. pilot or full"}
limit=${2:-}
model="Qwen/Qwen3-30B-A3B-Instruct-2507"
vllm_base_url=${VLLM_BASE_URL:-http://localhost:8000/v1}

cd "$(dirname "$0")"  # Code/multi_agent_debate: core.* imports and config paths are relative to it
exp_dir="exp/${name}"
dataset="data/naep_pairs_${name}.csv"

echo "== Checking the vLLM server at ${vllm_base_url}"
if ! curl -sf "${vllm_base_url}/models" | grep -q "${model}"; then
    echo "The vLLM server is not reachable or is not serving ${model}. Start it first (see README.md)." >&2
    exit 1
fi

echo "== Building the pairwise dataset (${dataset})"
python3 build_dataset.py --data-dir ../../Data --output "${dataset}" ${limit:+--limit-problems "${limit}"}

echo "== Running debates (both answer orders)"
python3 -m core.debate exp_dir="${exp_dir}" +experiment=practice_debate \
    ++dataset_file="${dataset}" ++vllm_base_url="${vllm_base_url}"

echo "== Judging"
python3 -m core.judge exp_dir="${exp_dir}" +experiment=practice_debate \
    ++vllm_base_url="${vllm_base_url}"

echo "== Aggregating log-probabilities and evaluating against the ground truth"
python3 aggregate.py --exp-dir "${exp_dir}" --data-dir ../../Data --output-prefix "naep_debate_${name}"

echo "== Done: ${name}"
