"""
Pedagogical Grounding benchmark with Llama-3.3-70B-Instruct model.

Usage:
    # Run difficulty comparison task
    CUDA_VISIBLE_DEVICES=0,1,2,3 python pedagogical_grounding/llama33_70b_instruct_pedagogical.py \
        --task difficulty \
        --data-dir . \
        --num-gpus 4 \
        --num-samples 1000 \
        --sampling-mode stratified \
        --cache-dir /data1/

    # Run discrimination comparison task
    CUDA_VISIBLE_DEVICES=0,1,2,3 python pedagogical_grounding/llama33_70b_instruct_pedagogical.py \
        --task discrimination \
        --data-dir . \
        --num-gpus 4 \
        --num-samples 1000

    # Run most common distractor task
    CUDA_VISIBLE_DEVICES=0,1,2,3 python pedagogical_grounding/llama33_70b_instruct_pedagogical.py \
        --task distractor_most \
        --data-dir . \
        --num-gpus 4

    # Run least common distractor task
    CUDA_VISIBLE_DEVICES=0,1,2,3 python pedagogical_grounding/llama33_70b_instruct_pedagogical.py \
        --task distractor_least \
        --data-dir . \
        --num-gpus 4

    # Run all tasks
    CUDA_VISIBLE_DEVICES=0,1,2,3 python pedagogical_grounding/llama33_70b_instruct_pedagogical.py \
        --task all \
        --data-dir . \
        --num-gpus 4 \
        --num-samples 500
"""

from pedagogical_inference_base import run_inference

MODEL_CONFIG = {
    "model_id": "meta-llama/Llama-3.3-70B-Instruct",
    "gen_configs": {
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 1024,
        "repetition_penalty": 1.0,
    },
    "output_prefix": "llama33_70b_instruct",
    "system_prompt_prefix": "",
}

if __name__ == "__main__":
    run_inference(MODEL_CONFIG)
