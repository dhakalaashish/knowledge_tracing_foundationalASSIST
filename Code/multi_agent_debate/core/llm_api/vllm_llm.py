"""
Chat client for a local vLLM server (OpenAI-compatible API).

Replaces the OpenAI and Anthropic clients of the original llm_debate code, which used
openai==0.28 and called the hosted APIs. Start the server separately, e.g.:

    vllm serve Qwen/Qwen3-30B-A3B-Instruct-2507 --port 8000 --max-model-len 32768 --enable-prefix-caching

Responses are returned as the repo's LLMResponse objects, so the agents need no changes.
"""

import asyncio
import logging
import time

from termcolor import cprint

from core.llm_api.base_llm import PRINT_COLORS, LLMResponse

LOGGER = logging.getLogger(__name__)

# Sampling parameters the server understands; anything else the agents pass (e.g. timeout)
# is dropped.
_PASSTHROUGH_PARAMS = {"n", "temperature", "top_p", "max_tokens", "stop", "seed"}


def _convert_logprobs(choice_logprobs) -> list[dict[str, float]] | None:
    """
    Convert the server's per-token logprobs to the repo's format: one {token: logprob} dict
    per generated token, built from that position's top_logprobs. Tokens are stripped, so
    " A" and "A" both count as "A" (keeping the higher logprob).
    """
    if choice_logprobs is None or not choice_logprobs.content:
        return None
    converted = []
    for position in choice_logprobs.content:
        candidates = {}
        for top in position.top_logprobs or []:
            token = top.token.strip()
            if token not in candidates or top.logprob > candidates[token]:
                candidates[token] = top.logprob
        converted.append(candidates)
    return converted


def _stop_reason(finish_reason: str | None) -> str:
    """Map vLLM finish reasons onto the two the repo's StopReason understands."""
    return "length" if finish_reason == "length" else "stop"


class VLLMChatModel:
    def __init__(self, base_url: str, num_threads: int, print_prompt_and_response: bool = False):
        from openai import AsyncOpenAI

        self.base_url = base_url
        self.client = AsyncOpenAI(base_url=base_url, api_key="EMPTY", timeout=1800, max_retries=0)
        self.semaphore = asyncio.Semaphore(num_threads)
        self.print_prompt_and_response = print_prompt_and_response

    async def __call__(
        self,
        model_ids: list[str],
        prompt: list[dict[str, str]],
        print_prompt_and_response: bool,
        max_attempts: int,
        **kwargs,
    ) -> list[LLMResponse]:
        model_id = model_ids[0]
        request = {"model": model_id, "messages": prompt}
        request.update({k: v for k, v in kwargs.items() if k in _PASSTHROUGH_PARAMS and v is not None})
        top_logprobs = kwargs.get("logprobs")
        if top_logprobs:
            request["logprobs"] = True
            request["top_logprobs"] = int(top_logprobs)

        start = time.time()
        response = None
        for attempt in range(max_attempts):
            try:
                async with self.semaphore:
                    api_start = time.time()
                    response = await self.client.chat.completions.create(**request)
                    api_duration = time.time() - api_start
                break
            except Exception as e:  # server busy, connection reset, etc.
                LOGGER.warning(
                    f"vLLM call failed ({type(e).__name__}: {e}); retrying (attempt {attempt + 1}/{max_attempts})"
                )
                await asyncio.sleep(min(2**attempt, 30))
        if response is None:
            raise RuntimeError(
                f"Failed to get a response from the vLLM server at {self.base_url} after {max_attempts} attempts."
            )

        duration = time.time() - start
        responses = [
            LLMResponse(
                model_id=model_id,
                completion=choice.message.content or "",
                stop_reason=_stop_reason(choice.finish_reason),
                cost=0.0,
                duration=duration,
                api_duration=api_duration,
                logprobs=_convert_logprobs(choice.logprobs),
            )
            for choice in response.choices
        ]
        if self.print_prompt_and_response or print_prompt_and_response:
            for message in prompt:
                cprint(f"=={message['role'].upper()}:", "white")
                cprint(message["content"], PRINT_COLORS[message["role"]])
            for i, item in enumerate(responses):
                cprint(f"==RESPONSE {i + 1} ({item.model_id}):", "white")
                cprint(item.completion, PRINT_COLORS["assistant"], attrs=["bold"])
        return responses
