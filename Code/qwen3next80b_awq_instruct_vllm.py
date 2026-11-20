"""
Knowledge Tracing inference with Qwen3-Next-80B-A3B-Instruct, 4-bit AWQ, so it fits on one A100 80 GB
(the BF16 model the paper used needs about 160 GB). Same generation settings as the paper's
qwen3next80bvllm_instruct.py; only the checkpoint differs.

The checkpoint is a community quantization (there is no official Qwen AWQ release). Override it with
the environment variable KT_MODEL_ID, e.g. KT_MODEL_ID=cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit.

Usage (normally started by kt_practice_benchmark.py):
    python qwen3next80b_awq_instruct_vllm.py --data-dir <kt_data> --num-students 0 \
        --bin-size 10 --min-history 50 --num-gpus 1 --max-model-len 196608 --output <file.jsonl>
"""

import os

from kt_inference_base import run_inference

MODEL_ID = os.environ.get("KT_MODEL_ID", "cpatonn/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit")

MODEL_CONFIG = {
    "model_id": MODEL_ID,
    "gen_configs": {            # as the paper's Qwen3-Next-80B-Instruct run
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 20,
        "min_p": 0.0,
        "max_tokens": 32768,
        "repetition_penalty": 1.0,
    },
    "output_prefix": "qwen3next80b_awq_instruct",
    "system_prompt_prefix": "",  # standard instruct model, no reasoning prefix
}

if __name__ == "__main__":
    run_inference(MODEL_CONFIG)
