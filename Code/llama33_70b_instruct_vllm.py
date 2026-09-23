"""
Knowledge Tracing inference with Llama-3.3-70B-Instruct model.

Usage:
    CUDA_VISIBLE_DEVICES=0,1,2,3 python llama33_70b_instruct_vllm.py \
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
    "model_id": "meta-llama/Llama-3.3-70B-Instruct",
    "gen_configs": {
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 32768,
        "repetition_penalty": 1.0,
    },
    "output_prefix": "llama33_70b_instruct",
    "system_prompt_prefix": "",  # No prefix - standard instruct model
}

if __name__ == "__main__":
    run_inference(MODEL_CONFIG)
