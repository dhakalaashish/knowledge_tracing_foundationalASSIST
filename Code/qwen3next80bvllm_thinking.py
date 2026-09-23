"""
Knowledge Tracing inference with Qwen3-Next-80B-A3B-Thinking model.

This model has native thinking mode - it automatically generates <think>...</think> blocks.
Recommended sampling: temperature=0.6, top_p=0.95, top_k=20, min_p=0

Usage:
    CUDA_VISIBLE_DEVICES=0,1,2,3 python qwen3next80bvllm_thinking.py \
        --data-dir foundationalktdataset/ \
        --num-gpus 4 \
        --batch-size 10 \
        --cache-dir /data1/ \
        --num-students 500 \
        --bin-size 50 \
        --min-history 50
"""

from kt_inference_base import run_inference

MODEL_CONFIG = {
    "model_id": "Qwen/Qwen3-Next-80B-A3B-Thinking",
    "gen_configs": {
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 20,
        "min_p": 0.0,
        "max_tokens": 32768,
        "repetition_penalty": 1.0,
    },
    "output_prefix": "qwen3next80bthinking",
    "system_prompt_prefix": "",  # No prefix - model has native thinking
}

if __name__ == "__main__":
    run_inference(MODEL_CONFIG)
