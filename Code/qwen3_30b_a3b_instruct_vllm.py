"""
Knowledge Tracing inference with Qwen3-30B-A3B-Instruct-2507 model.

This is the standard instruction-following model (no thinking blocks).
Recommended sampling: temperature=0.7, top_p=0.8, top_k=20, min_p=0

Usage:
    CUDA_VISIBLE_DEVICES=0,1,2,3 python qwen3_30b_a3b_instruct_vllm.py \
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
    "model_id": "Qwen/Qwen3-30B-A3B-Instruct-2507",
    "gen_configs": {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 20,
        "min_p": 0.0,
        "max_tokens": 32768,
        "repetition_penalty": 1.0,
    },
    "output_prefix": "qwen3_30b_a3b_instruct",
    "system_prompt_prefix": "",  # No prefix - standard instruct model
}

if __name__ == "__main__":
    run_inference(MODEL_CONFIG)
