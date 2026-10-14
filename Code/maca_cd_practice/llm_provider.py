import os


SUPPORTED_PROVIDERS = {"qwen", "openai", "vllm"}


def _normalize_provider(provider):
    normalized = str(provider or "qwen").strip().lower()
    aliases = {
        "dashscope": "qwen",
        "gpt": "openai",
        "local": "vllm",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in SUPPORTED_PROVIDERS:
        supported = ", ".join(sorted(SUPPORTED_PROVIDERS))
        raise ValueError(
            f"Unsupported Agent_provider '{provider}'. Choose one of: {supported}"
        )
    return normalized


def _resolve_api_key(config, provider, prefix="Agent"):
    configured_key = str(config.get(f"{prefix}_API_key", "")).strip()
    if not configured_key:
        configured_key = str(config.get("API_key", "")).strip()

    if configured_key and set(configured_key) != {"*"}:
        return configured_key

    default_env = "OPENAI_API_KEY" if provider == "openai" else "DASHSCOPE_API_KEY"
    env_name = config.get(f"{prefix}_API_key_env") or default_env
    api_key = os.getenv(env_name, "").strip()
    if not api_key:
        raise ValueError(
            f"No API key configured for {provider}. Set {prefix}_API_key "
            f"or the {env_name} environment variable."
        )
    return api_key


class OpenAIResponsesAssistant:
    def __init__(self, config, system_message):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError(
                "The OpenAI provider requires the 'openai' package. "
                "Install it with: pip install -U openai"
            ) from exc

        api_key = _resolve_api_key(config, "openai")
        model_server = str(config.get("model_server", "")).strip()
        client_kwargs = {"api_key": api_key}
        if model_server and model_server not in {"openai", "dashscope"}:
            client_kwargs["base_url"] = model_server

        self.client = OpenAI(**client_kwargs)
        self.model = config["model"]
        self.system_message = system_message

    def run(self, messages):
        normalized_messages = [
            {
                "role": message["role"],
                "content": message["content"],
            }
            for message in messages
        ]
        response = self.client.responses.create(
            model=self.model,
            instructions=self.system_message,
            input=normalized_messages,
        )
        content = response.output_text
        if not content:
            raise RuntimeError("OpenAI returned an empty response.")
        yield [{"role": "assistant", "content": content}]


class QwenDashScopeAssistant:
    def __init__(self, config, system_message):
        try:
            import dashscope
        except ImportError as exc:
            raise ImportError(
                "The Qwen provider requires the 'dashscope' package. "
                "Install it with: pip install -U dashscope"
            ) from exc

        self.dashscope = dashscope
        self.api_key = _resolve_api_key(config, "qwen")
        self.model = config["model"]
        self.system_message = system_message
        self.temperature = config.get("temperature", 0.5)
        self.top_p = config.get("top_p", 0.8)

    def run(self, messages):
        normalized_messages = [
            {"role": "system", "content": self.system_message},
            *[
                {
                    "role": message["role"],
                    "content": message["content"],
                }
                for message in messages
            ],
        ]
        response = self.dashscope.Generation.call(
            api_key=self.api_key,
            model=self.model,
            messages=normalized_messages,
            result_format="message",
            temperature=self.temperature,
            top_p=self.top_p,
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"DashScope generation request failed: "
                f"{response.code} - {response.message}"
            )
        content = response.output.choices[0].message.content
        if not content:
            raise RuntimeError("DashScope returned an empty response.")
        yield [{"role": "assistant", "content": content}]


def _vllm_client(base_url):
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError(
            "The vllm provider requires the 'openai' package. "
            "Install it with: pip install -U openai"
        ) from exc

    base_url = str(base_url or "").strip()
    if not base_url.startswith("http"):
        raise ValueError(
            f"The vllm provider needs the server URL, e.g. http://localhost:8000/v1, got '{base_url}'"
        )
    # A local vLLM server accepts any key unless it was started with --api-key
    return OpenAI(base_url=base_url, api_key=os.getenv("VLLM_API_KEY", "EMPTY"))


class VLLMChatAssistant:
    """Local vLLM server (OpenAI-compatible Chat Completions API)."""

    def __init__(self, config, system_message):
        self.client = _vllm_client(config.get("model_server"))
        self.model = config["model"]
        self.system_message = system_message
        self.temperature = config.get("temperature", 0.5)
        self.top_p = config.get("top_p", 0.8)

    def run(self, messages):
        normalized_messages = [
            {"role": "system", "content": self.system_message},
            *[
                {
                    "role": message["role"],
                    "content": message["content"],
                }
                for message in messages
            ],
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=normalized_messages,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("vLLM returned an empty response.")
        yield [{"role": "assistant", "content": content}]


def create_assistant(config, system_message):
    provider = _normalize_provider(config.get("provider"))
    if provider == "openai":
        return OpenAIResponsesAssistant(config, system_message)
    if provider == "vllm":
        return VLLMChatAssistant(config, system_message)
    return QwenDashScopeAssistant(config, system_message)


def _vllm_embedding(text, config, dimension):
    client = _vllm_client(
        config.get("Embedding_model_server") or config.get("model_server")
    )
    model = config.get("Embedding_model")
    if not model:
        raise ValueError("Set Embedding_model for the vllm embedding provider.")
    try:
        response = client.embeddings.create(model=model, input=text, dimensions=dimension)
        return response.data[0].embedding
    except Exception as exc:
        # Servers that do not support `dimensions`: take the full vector and keep its first
        # `dimension` values (valid for Matryoshka models such as Qwen3-Embedding).
        print(f"Embedding request with dimensions={dimension} failed ({exc}); truncating instead.")
    embedding = client.embeddings.create(model=model, input=text).data[0].embedding[:dimension]
    norm = sum(x * x for x in embedding) ** 0.5
    return [x / norm for x in embedding] if norm > 0 else embedding


def embed_text(text, config):
    agent_provider = _normalize_provider(config.get("provider"))
    configured_provider = str(config.get("Embedding_provider", "")).strip().lower()
    if configured_provider in {"", "same", "agent"}:
        provider = agent_provider
    else:
        provider = _normalize_provider(configured_provider)
    dimension = int(config.get("Embedding_dimension", 256))
    if provider == "vllm":
        return _vllm_embedding(text, config, dimension)
    embedding_config = dict(config)
    if provider == agent_provider and not embedding_config.get("Embedding_API_key"):
        embedding_config["Embedding_API_key"] = embedding_config.get(
            "Agent_API_key", ""
        )
    api_key = _resolve_api_key(embedding_config, provider, prefix="Embedding")

    if provider == "openai":
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError(
                "OpenAI embeddings require the 'openai' package. "
                "Install it with: pip install -U openai"
            ) from exc

        model_server = str(config.get("Embedding_model_server", "")).strip()
        if not model_server and provider == agent_provider:
            agent_model_server = str(config.get("model_server", "")).strip()
            if agent_model_server not in {"", "openai", "dashscope"}:
                model_server = agent_model_server
        client_kwargs = {"api_key": api_key}
        if model_server:
            client_kwargs["base_url"] = model_server
        client = OpenAI(**client_kwargs)
        response = client.embeddings.create(
            model=config.get("Embedding_model") or "text-embedding-3-small",
            input=text,
            dimensions=dimension,
        )
        return response.data[0].embedding

    try:
        import dashscope
    except ImportError as exc:
        raise ImportError(
            "Qwen embeddings require the 'dashscope' package. "
            "Install it with: pip install -U dashscope"
        ) from exc

    dashscope.api_key = api_key
    response = dashscope.TextEmbedding.call(
        model=config.get("Embedding_model") or "text-embedding-v3",
        input=text,
        dimension=dimension,
        output_type="dense",
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope embedding request failed: "
            f"{response.code} - {response.message}"
        )
    return response["output"]["embeddings"][0]["embedding"]
