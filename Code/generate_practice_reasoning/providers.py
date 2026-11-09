"""LLM backends. Every call is a fresh single-turn conversation: one system prompt, one user prompt.

API backends (anthropic, openai, gemini):
    call(system, prompt, step, calls) sends one request, appends its record to `calls` and returns
    the record. It appends before raising (refusal, token limit, empty answer), so a failed call is
    still logged. The caller runs many problems in parallel with threads.
Local backend (offline vLLM):
    call_many(requests) runs a batch of (key, system, prompt, step) and returns
    [(key, record, error or None)] in the same order.

A call record holds what is needed to reproduce and audit the call:
    step, system_prompt (name and sha256; the full text is in the run's manifest.json),
    user_prompt, request (the exact request parameters), response_text, reasoning_text (thinking
    or reasoning, when the model returns it), raw_response (the full response as JSON), usage,
    stop_reason, served_model, started_at, finished_at.
"""

import os
import re

from common import now, sha256

THINK_RE = re.compile(r"^\s*<think>(.*?)</think>\s*", re.S)
SYSTEM_NAMES = {1: "SYSTEM_PROMPT_1", 2: "SYSTEM_PROMPT_2"}


def split_think(text):
    """Qwen-style output: '<think>...</think>answer' -> (answer, reasoning)."""
    text = text or ""
    m = THINK_RE.match(text)
    if m:
        return text[m.end():], m.group(1).strip()
    if "</think>" in text:  # opening tag added by the chat template
        before, after = text.split("</think>", 1)
        return after.lstrip(), before.replace("<think>", "").strip()
    return text, None


def system_ref(system, step):
    """Stand-in for the system prompt in the logged request (the full text is in manifest.json)."""
    return {"name": SYSTEM_NAMES[step], "sha256": sha256(system)}


def base_record(step, system, prompt):
    return {"step": step, "system_prompt": system_ref(system, step), "user_prompt": prompt,
            "started_at": now()}


# ---------------------------------------------------------------- Claude (Anthropic API)

class AnthropicProvider:
    name = "anthropic"

    def __init__(self, args):
        import anthropic
        self.client = anthropic.Anthropic(max_retries=args.max_retries)
        self.model = args.model
        self.params = {
            "max_tokens": args.max_tokens or 16000,
            "effort": args.effort,
            "thinking": args.claude_thinking,
            "fallbacks": not args.no_fallbacks,
        }

    def describe(self):
        return {"provider": self.name, "model": self.model, "params": self.params}

    def call(self, system, prompt, step, calls):
        rec = base_record(step, system, prompt)
        body = {"model": self.model, "max_tokens": self.params["max_tokens"], "system": system,
                "messages": [{"role": "user", "content": prompt}]}
        if self.params["effort"]:
            body["output_config"] = {"effort": self.params["effort"]}
        if self.params["thinking"] == "adaptive_summarized":
            body["thinking"] = {"type": "adaptive", "display": "summarized"}
        if self.params["fallbacks"]:
            # Server-side refusal fallback: on a policy decline the API re-runs the request on a
            # fallback model inside the same call; served_model says which model answered.
            body["betas"] = ["server-side-fallback-2026-07-01"]
            body["fallbacks"] = "default"
            resp = self.client.beta.messages.create(**body)
        else:
            resp = self.client.messages.create(**body)
        raw = resp.to_dict()
        content = raw.get("content", [])
        rec.update({
            "request": {**body, "system": system_ref(system, step)},
            "response_text": "".join(b.get("text", "") for b in content if b.get("type") == "text"),
            "reasoning_text": "\n\n".join(b.get("thinking", "") for b in content
                                          if b.get("type") == "thinking" and b.get("thinking")) or None,
            "raw_response": raw, "usage": raw.get("usage"), "stop_reason": raw.get("stop_reason"),
            "served_model": raw.get("model"), "request_id": getattr(resp, "_request_id", None),
            "finished_at": now(),
        })
        calls.append(rec)
        if rec["stop_reason"] == "refusal":
            raise RuntimeError(f"refusal in step {step}: {raw.get('stop_details')}")
        if rec["stop_reason"] == "max_tokens":
            raise RuntimeError(f"step {step} hit max_tokens ({self.params['max_tokens']})")
        if not rec["response_text"].strip():
            raise RuntimeError(f"empty answer in step {step}")
        return rec


# ---------------------------------------------------------------- OpenAI (and OpenAI-compatible servers)

class OpenAIProvider:
    name = "openai"

    def __init__(self, args):
        from openai import OpenAI
        kw = {"max_retries": args.max_retries}
        if args.base_url:
            kw["base_url"] = args.base_url
            kw["api_key"] = os.environ.get("OPENAI_API_KEY", "EMPTY")
        self.client = OpenAI(**kw)
        self.model = args.model
        self.params = {"base_url": args.base_url, "max_completion_tokens": args.max_tokens,
                       "temperature": args.temperature, "reasoning_effort": args.reasoning_effort}

    def describe(self):
        return {"provider": self.name, "model": self.model, "params": self.params}

    def call(self, system, prompt, step, calls):
        rec = base_record(step, system, prompt)
        body = {"model": self.model, "messages": [{"role": "system", "content": system},
                                                  {"role": "user", "content": prompt}]}
        if self.params["max_completion_tokens"]:
            body["max_completion_tokens"] = self.params["max_completion_tokens"]
        if self.params["temperature"] is not None:
            body["temperature"] = self.params["temperature"]
        if self.params["reasoning_effort"]:
            body["reasoning_effort"] = self.params["reasoning_effort"]
        resp = self.client.chat.completions.create(**body)
        raw = resp.model_dump(mode="json")
        choice = raw["choices"][0]
        msg = choice.get("message") or {}
        text, think = split_think(msg.get("content") or "")
        logged = dict(body)
        logged["messages"] = [{"role": "system", "content": system_ref(system, step)},
                              {"role": "user", "content": prompt}]
        rec.update({
            "request": logged, "response_text": text,
            "reasoning_text": msg.get("reasoning_content") or msg.get("reasoning") or think,
            "raw_response": raw, "usage": raw.get("usage"), "stop_reason": choice.get("finish_reason"),
            "served_model": raw.get("model"), "finished_at": now(),
        })
        calls.append(rec)
        if rec["stop_reason"] == "length":
            raise RuntimeError(f"step {step} hit the token limit")
        if not text.strip():
            raise RuntimeError(f"empty answer in step {step} (finish_reason {rec['stop_reason']})")
        return rec


# ---------------------------------------------------------------- Gemini (google-genai)

class GeminiProvider:
    name = "gemini"

    def __init__(self, args):
        from google import genai
        from google.genai import types
        self.types = types
        self.client = genai.Client()
        self.model = args.model
        self.params = {"max_output_tokens": args.max_tokens, "temperature": args.temperature,
                       "include_thoughts": args.gemini_include_thoughts}

    def describe(self):
        return {"provider": self.name, "model": self.model, "params": self.params}

    def call(self, system, prompt, step, calls):
        types = self.types
        rec = base_record(step, system, prompt)
        kw = {"system_instruction": system}
        if self.params["max_output_tokens"]:
            kw["max_output_tokens"] = self.params["max_output_tokens"]
        if self.params["temperature"] is not None:
            kw["temperature"] = self.params["temperature"]
        if self.params["include_thoughts"]:
            kw["thinking_config"] = types.ThinkingConfig(include_thoughts=True)
        config = types.GenerateContentConfig(**kw)
        contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        logged_config = config.model_dump(mode="json", exclude_none=True)
        logged_config["system_instruction"] = system_ref(system, step)
        rec["request"] = {"model": self.model, "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                          "config": logged_config}
        resp = self.client.models.generate_content(model=self.model, contents=contents, config=config)
        raw = resp.model_dump(mode="json", exclude_none=True)
        cand = resp.candidates[0] if resp.candidates else None
        parts = (cand.content.parts or []) if cand and cand.content else []
        text = "".join(p.text or "" for p in parts if not getattr(p, "thought", False))
        thoughts = "\n\n".join(p.text or "" for p in parts if getattr(p, "thought", False))
        rec.update({
            "response_text": text, "reasoning_text": thoughts or None, "raw_response": raw,
            "usage": raw.get("usage_metadata"),
            "stop_reason": str(cand.finish_reason) if cand and cand.finish_reason is not None else None,
            "served_model": raw.get("model_version"), "finished_at": now(),
        })
        calls.append(rec)
        if cand is None:
            raise RuntimeError(f"no candidate in step {step}: {raw.get('prompt_feedback')}")
        if not text.strip():
            raise RuntimeError(f"empty answer in step {step} (finish_reason {rec['stop_reason']})")
        return rec


# ---------------------------------------------------------------- local Qwen3 with offline vLLM

class LocalVLLMProvider:
    name = "local"

    def __init__(self, args):
        os.environ.setdefault("VLLM_USE_FLASHINFER_SAMPLER", "0")  # needed on the A100 server
        import torch
        visible = torch.cuda.device_count()
        if args.num_gpus > visible:
            raise SystemExit(f"--num-gpus {args.num_gpus} but only {visible} GPU(s) are visible "
                             f"(CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES', 'not set')}). "
                             f"Use --num-gpus {max(visible, 1)}.")
        from vllm import LLM, SamplingParams
        llm_kwargs = {"model": args.model, "tensor_parallel_size": args.num_gpus,
                      "gpu_memory_utilization": args.gpu_memory_utilization,
                      "max_model_len": args.max_model_len, "trust_remote_code": True}
        if args.cache_dir:
            llm_kwargs["download_dir"] = args.cache_dir
        self.llm = LLM(**llm_kwargs)
        self.tokenizer = self.llm.get_tokenizer()
        self.model = args.model
        self.batch_size = args.batch_size
        self._sampling_cls = SamplingParams
        self.sampling_kwargs = {"temperature": 0.7 if args.temperature is None else args.temperature,
                                "top_p": args.top_p, "top_k": args.top_k, "min_p": args.min_p,
                                "max_tokens": args.max_tokens or 8192}
        self.base_seed = args.seed
        self.attempt_of = {}  # key -> attempts already made; set by generate.py so a redo gets a new seed
        self.chat_template_kwargs = None
        if args.enable_thinking is not None:
            self.chat_template_kwargs = {"enable_thinking": args.enable_thinking}
        # params: settings that change the output (locked per run directory);
        # infra: hardware and loading settings (recorded, not locked).
        self.params = {"sampling": {**self.sampling_kwargs, "seed": args.seed},
                       "chat_template_kwargs": self.chat_template_kwargs, "max_model_len": args.max_model_len}
        self.infra = {"llm": llm_kwargs, "batch_size": args.batch_size}

    def describe(self):
        return {"provider": self.name, "model": self.model, "params": self.params, "infra": self.infra}

    def sampling_for(self, key, step):
        # A different seed for each attempt (so a redo can differ) and for each step.
        return {**self.sampling_kwargs, "seed": self.base_seed + 2 * self.attempt_of.get(key, 0) + step - 1}

    def _rendered(self, conv, system, step):
        kw = dict(tokenize=False, add_generation_prompt=True)
        if self.chat_template_kwargs:
            kw.update(self.chat_template_kwargs)
        text = self.tokenizer.apply_chat_template(conv, **kw)
        # The system prompt is replaced by its name; the full text is in manifest.json.
        return text.replace(system, "{" + SYSTEM_NAMES[step] + "}")

    def call_many(self, requests):
        out = []
        for start in range(0, len(requests), self.batch_size):
            chunk = requests[start:start + self.batch_size]
            convs = [[{"role": "system", "content": system}, {"role": "user", "content": prompt}]
                     for _, system, prompt, _ in chunk]
            params = [self._sampling_cls(**self.sampling_for(key, step)) for key, _, _, step in chunk]
            kw = {"use_tqdm": True}
            if self.chat_template_kwargs is not None:
                kw["chat_template_kwargs"] = self.chat_template_kwargs
            started = now()
            results = self.llm.chat(convs, params, **kw)
            finished = now()
            for (key, system, prompt, step), conv, res in zip(chunk, convs, results):
                gen = res.outputs[0]
                text, think = split_think(gen.text)
                rec = base_record(step, system, prompt)
                rec.update({
                    "started_at": started,
                    "request": {"messages": [{"role": "system", "content": system_ref(system, step)},
                                             {"role": "user", "content": prompt}],
                                "rendered_prompt": self._rendered(conv, system, step),
                                "sampling": self.sampling_for(key, step),
                                "chat_template_kwargs": self.chat_template_kwargs},
                    "response_text": text, "reasoning_text": think,
                    "raw_response": {"text": gen.text, "finish_reason": gen.finish_reason,
                                     "stop_reason": gen.stop_reason},
                    "usage": {"prompt_tokens": len(res.prompt_token_ids or []),
                              "completion_tokens": len(gen.token_ids or [])},
                    "stop_reason": gen.finish_reason, "served_model": self.model, "finished_at": finished,
                })
                error = None
                if gen.finish_reason == "length":
                    error = f"step {step} hit max_tokens"
                elif not text.strip():
                    error = f"empty answer in step {step}"
                out.append((key, rec, error))
        return out


PROVIDERS = {"anthropic": AnthropicProvider, "openai": OpenAIProvider,
             "gemini": GeminiProvider, "local": LocalVLLMProvider}
