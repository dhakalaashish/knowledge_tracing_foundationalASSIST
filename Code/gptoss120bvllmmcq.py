"""
Knowledge Tracing inference with GPT-OSS-120B model.

Usage:
    CUDA_VISIBLE_DEVICES=0,1,2,3 python gptoss120bvllmmcq.py \
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
    "model_id": "openai/gpt-oss-120b",
    "gen_configs": {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 20,
        "max_tokens": 32768,
        "repetition_penalty": 1.0,
    },
    "output_prefix": "gptoss120b",
    "system_prompt_prefix": "Reasoning: medium\n\n",
}

if __name__ == "__main__":
    run_inference(MODEL_CONFIG)
