"""
Async client for the local vLLM server (OpenAI-compatible API), after
Code/multi_agent_debate/core/llm_api/vllm_llm.py: one AsyncOpenAI client, a semaphore that caps the
requests in flight, and retries with backoff. Prediction calls use a JSON schema (response_format) and
return the top logprobs, from which yes_probability() reads P(Yes) for AUC.
"""

import asyncio
import json
import logging
import math
import os
import re

LOGGER = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, cfg):
        from openai import AsyncOpenAI

        self.cfg = cfg
        self.client = AsyncOpenAI(base_url=cfg["base_url"], api_key=os.environ.get("VLLM_API_KEY", "EMPTY"),
                                  timeout=1800, max_retries=0)
        self.semaphore = asyncio.Semaphore(cfg["concurrency"])

    async def check_server(self):
        models = await self.client.models.list()
        served = [m.id for m in models.data]
        if self.cfg["model"] not in served:
            raise RuntimeError(f"The server at {self.cfg['base_url']} serves {served}, not {self.cfg['model']}")

    async def chat(self, messages, max_tokens, schema=None, logprobs=False):
        request = {"model": self.cfg["model"], "messages": messages,
                   "temperature": self.cfg["temperature"], "max_tokens": max_tokens}
        if schema is not None:
            request["response_format"] = {"type": "json_schema",
                                          "json_schema": {"name": "agent4cd", "schema": schema}}
        if logprobs:
            request["logprobs"] = True
            request["top_logprobs"] = self.cfg["top_logprobs"]
        attempts = self.cfg["max_attempts"]
        for attempt in range(attempts):
            try:
                async with self.semaphore:
                    response = await self.client.chat.completions.create(**request)
                break
            except Exception as exc:  # server busy, connection reset, ...
                if attempt == attempts - 1:
                    raise
                LOGGER.warning(f"vLLM call failed ({type(exc).__name__}: {exc}); retry {attempt + 1}/{attempts - 1}")
                await asyncio.sleep(min(2 ** attempt, 30))
        choice = response.choices[0]
        usage = response.usage
        return {
            "text": choice.message.content or "",
            "finish_reason": choice.finish_reason,
            "logprobs": choice.logprobs.content if choice.logprobs is not None else None,
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
        }


def parse_prediction(text):
    """The {task1, task2, task3} object, or None. task3 is read leniently (any value starting with y / n)."""
    candidates = [text]
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        candidates.append(match.group(0))
    for candidate in candidates:
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            answer = str(obj.get("task3", "")).strip().lower()
            if answer.startswith(("y", "n")):
                obj["task3"] = "Yes" if answer.startswith("y") else "No"
                return obj
    match = re.search(r'"task3"\s*:\s*"\s*(yes|no)', text, re.IGNORECASE)
    if match:
        return {"task3": "Yes" if match.group(1).lower() == "yes" else "No"}
    return None


def _norm(token):
    return token.strip().strip('"').strip().lower()


def yes_probability(logprob_content):
    """
    P(Yes) = e^lp(Yes) / (e^lp(Yes) + e^lp(No)) at the task3 answer token. task3 is the last field of the
    JSON object, so the answer token is the last generated token that reads Yes or No. When only one of
    the two is among the top logprobs, its own probability is used.
    """
    if not logprob_content:
        return None
    for position in reversed(logprob_content):
        if _norm(position.token) in ("yes", "no"):
            break
    else:
        return None
    lp = {}
    for top in [position] + list(position.top_logprobs or []):
        key = _norm(top.token)
        if key in ("yes", "no") and (key not in lp or top.logprob > lp[key]):
            lp[key] = top.logprob
    if "yes" in lp and "no" in lp:
        return 1.0 / (1.0 + math.exp(lp["no"] - lp["yes"]))
    if "yes" in lp:
        return math.exp(lp["yes"])
    return 1.0 - math.exp(lp["no"])
