"""
Pedagogical Grounding benchmark with Qwen3-Next-80B-A3B-Thinking model.

This model has native thinking mode - it automatically generates <think>...</think> blocks.
Recommended sampling: temperature=0.6, top_p=0.95, top_k=20, min_p=0

Usage:
    # Run difficulty comparison task
    CUDA_VISIBLE_DEVICES=0,1,2,3 python qwen3next80b_thinking_pedagogical.py \
        --task difficulty \
        --data-dir . \
        --num-gpus 4 \
        --num-samples 1000 \
        --sampling-mode stratified \
        --cache-dir /data1/

    # Run discrimination comparison task
    CUDA_VISIBLE_DEVICES=0,1,2,3 python qwen3next80b_thinking_pedagogical.py \
        --task discrimination \
        --data-dir . \
        --num-gpus 4 \
        --num-samples 1000

    # Run most common distractor task
    CUDA_VISIBLE_DEVICES=0,1,2,3 python qwen3next80b_thinking_pedagogical.py \
        --task distractor_most \
        --data-dir . \
        --num-gpus 4

    # Run least common distractor task
    CUDA_VISIBLE_DEVICES=0,1,2,3 python qwen3next80b_thinking_pedagogical.py \
        --task distractor_least \
        --data-dir . \
        --num-gpus 4

    # Run all tasks
    CUDA_VISIBLE_DEVICES=0,1,2,3 python qwen3next80b_thinking_pedagogical.py \
        --task all \
        --data-dir . \
        --num-gpus 4 \
        --num-samples 500
"""

from pedagogical_inference_base import run_inference

MODEL_CONFIG = {
    "model_id": "Qwen/Qwen3-Next-80B-A3B-Thinking",
    "gen_configs": {
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 20,
        "min_p": 0.0,
        "max_tokens": 4096,  # Longer for thinking blocks + response
        "repetition_penalty": 1.0,
    },
    "output_prefix": "qwen3next80bthinking",
    "system_prompt_prefix": "",  # No prefix - model has native thinking
}

if __name__ == "__main__":
    run_inference(MODEL_CONFIG)
