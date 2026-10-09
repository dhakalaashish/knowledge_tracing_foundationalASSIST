import logging
from typing import Callable, Literal, Union

import attrs

from core.llm_api.base_llm import LLMResponse
from core.llm_api.vllm_llm import VLLMChatModel

LOGGER = logging.getLogger(__name__)


@attrs.define()
class ModelAPI:
    """
    Same interface as the original llm_debate ModelAPI (candidate sampling, is_valid filtering,
    padding), but every model id is served by a local vLLM server instead of the OpenAI or
    Anthropic APIs.
    """

    vllm_base_url: str = "http://localhost:8000/v1"
    vllm_num_threads: int = 128
    print_prompt_and_response: bool = False

    _vllm_chat: VLLMChatModel = attrs.field(init=False)

    running_cost: float = attrs.field(init=False, default=0)
    model_timings: dict[str, list[float]] = attrs.field(init=False, factory=dict)
    model_wait_times: dict[str, list[float]] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):
        self._vllm_chat = VLLMChatModel(
            base_url=self.vllm_base_url,
            num_threads=self.vllm_num_threads,
            print_prompt_and_response=self.print_prompt_and_response,
        )

    async def call_single(
        self,
        model_ids: Union[str, list[str]],
        prompt: Union[list[dict[str, str]], str],
        max_tokens: int,
        print_prompt_and_response: bool = False,
        n: int = 1,
        max_attempts_per_api_call: int = 10,
        num_candidates_per_completion: int = 1,
        is_valid: Callable[[str], bool] = lambda _: True,
        insufficient_valids_behaviour: Literal[
            "error", "continue", "pad_invalids"
        ] = "error",
        **kwargs,
    ) -> str:
        assert n == 1, f"Expected a single response. {n} responses were requested."
        responses = await self(
            model_ids,
            prompt,
            max_tokens,
            print_prompt_and_response,
            n,
            max_attempts_per_api_call,
            num_candidates_per_completion,
            is_valid,
            insufficient_valids_behaviour,
            **kwargs,
        )
        assert len(responses) == 1, "Expected a single response."
        return responses[0].completion

    async def __call__(
        self,
        model_ids: Union[str, list[str]],
        prompt: Union[list[dict[str, str]], str],
        max_tokens: int,
        print_prompt_and_response: bool = False,
        n: int = 1,
        max_attempts_per_api_call: int = 10,
        num_candidates_per_completion: int = 1,
        is_valid: Callable[[str], bool] = lambda _: True,
        insufficient_valids_behaviour: Literal[
            "error", "continue", "pad_invalids"
        ] = "error",
        **kwargs,
    ) -> list[LLMResponse]:
        """
        Request n * num_candidates_per_completion completions, keep the ones that pass
        is_valid, and return up to n of them (see the original llm_debate ModelAPI).
        """
        if isinstance(model_ids, str):
            model_ids = [model_ids]
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        num_candidates = num_candidates_per_completion * n
        candidate_responses = await self._vllm_chat(
            model_ids,
            prompt,
            print_prompt_and_response,
            max_attempts_per_api_call,
            n=num_candidates,
            **kwargs,
        )

        valid_responses = [
            response for response in candidate_responses if is_valid(response.completion)
        ]
        num_valid = len(valid_responses)
        success_rate = num_valid / num_candidates
        if success_rate < 1:
            LOGGER.info(f"`is_valid` success rate: {success_rate * 100:.2f}%")

        if num_valid < n:
            if insufficient_valids_behaviour == "error":
                raise RuntimeError(
                    f"Only found {num_valid} valid responses from {num_candidates} candidates."
                )
            elif insufficient_valids_behaviour == "continue":
                responses = valid_responses
            else:  # pad_invalids
                invalid_responses = [
                    response
                    for response in candidate_responses
                    if not is_valid(response.completion)
                ]
                invalids_needed = n - num_valid
                responses = [*valid_responses, *invalid_responses[:invalids_needed]]
                LOGGER.info(
                    f"Padded {num_valid} valid responses with {invalids_needed} invalid responses to get {len(responses)} total responses"
                )
        else:
            responses = valid_responses

        for response in responses:
            self.model_timings.setdefault(response.model_id, []).append(response.api_duration)
            self.model_wait_times.setdefault(response.model_id, []).append(
                response.duration - response.api_duration
            )
        return responses[:n]

    def reset_cost(self):
        self.running_cost = 0
