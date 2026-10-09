import json
import logging
from functools import lru_cache

import numpy as np
import yaml
from tenacity import retry, retry_if_result, stop_after_attempt

LOGGER = logging.getLogger(__name__)
SEPARATOR = "---------------------------------------------\n\n"
SEPARATOR_CONVERSATIONAL_TURNS = "=============================================\n\n"

LOGGING_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}


def setup_environment(logger_level: str = "info"):
    """Set up logging. Unlike the original, no SECRETS file or API keys are needed (local vLLM)."""
    setup_logging(logger_level)


def setup_logging(level_str):
    level = LOGGING_LEVELS.get(
        level_str.lower(), logging.INFO
    )  # default to INFO if level_str is not found
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Disable request logging from the openai client
    logging.getLogger("openai").setLevel(logging.CRITICAL)
    logging.getLogger("httpx").setLevel(logging.CRITICAL)


def load_yaml(file_path):
    with open(file_path) as f:
        content = yaml.safe_load(f)
    return content


@lru_cache(maxsize=8)
def load_yaml_cached(file_path):
    with open(file_path) as f:
        content = yaml.safe_load(f)
    return content


def load_jsonl(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return data


@retry(
    stop=stop_after_attempt(16),
    retry=retry_if_result(lambda result: result is not True),
)
async def async_function_with_retry(function, *args, **kwargs):
    return await function(*args, **kwargs)


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)
