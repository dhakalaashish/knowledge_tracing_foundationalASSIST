# Environment for generate.py and diagnose.py: vLLM built for CUDA 13.0, plus the API clients in requirements.txt.
# The base image is multi-arch, so it builds as arm64 on the GB300 (Grace CPU) and as amd64 elsewhere.
#
# The code and data are NOT copied into the image. docker_run.sh mounts the whole repository at /workspace, so:
#   - results (Data/Problems.csv, Data/wrong_answer_diagnosis_*.csv, runs/, logs/) land in your checkout,
#   - runs resume from runs/ after a restart, as without Docker,
#   - a git pull updates the code without rebuilding the image.
#
# Build (on the GB300, from this folder):  bash docker_run.sh build
#
# Base image: v0.20.0-cu130 is the newest vLLM release published for CUDA 13 (later releases ship CUDA 12.9 only),
# and Qwen3.5 needs vLLM >= 0.17. Another image can be used with:  VLLM_IMAGE=<image> bash docker_run.sh build
# The host needs an NVIDIA driver for CUDA 13 (580 or newer) and the NVIDIA Container Toolkit.
ARG VLLM_IMAGE=vllm/vllm-openai:v0.20.0-cu130
FROM ${VLLM_IMAGE}

ENV PIP_BREAK_SYSTEM_PACKAGES=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# git: each run records the code's commit in runs/<name>/manifest.json. The mounted repository belongs to
# another user id than the container's, so git must be told to trust it.
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/* \
 && git config --system --add safe.directory '*'

# The API clients (anthropic, openai, google-genai). vLLM, PyTorch, Transformers and the CUDA libraries stay
# exactly at the versions the base image was built with.
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip --version >/dev/null 2>&1 || python3 -m ensurepip \
 && python3 -m pip freeze \
    | grep -iE '^(vllm|torch|torchvision|torchaudio|transformers|tokenizers|triton|xformers|numpy|flashinfer[a-z0-9_-]*|nvidia-[a-z0-9_-]+)==' \
    > /tmp/constraints.txt \
 && python3 -m pip install -c /tmp/constraints.txt -r /tmp/requirements.txt \
 && (python3 -m pip check || true) \
 && python3 -c "import vllm, torch, anthropic, openai; from google import genai; print('vllm', vllm.__version__, '| torch', torch.__version__, '| CUDA', torch.version.cuda)"

# FlashInfer (vLLM's FP8 MoE and attention kernels on Blackwell) creates symlinks inside its own package folders
# the first time a kernel is used. Those folders belong to root; the container runs as your user, so make them
# writable (without this: PermissionError in .../flashinfer_cubin/cubins/flashinfer and "Engine core
# initialization failed").
RUN python3 -c "import importlib.util as u; [print(p) for n in ('flashinfer', 'flashinfer_cubin', 'flashinfer_jit_cache') if (s := u.find_spec(n)) and s.submodule_search_locations for p in s.submodule_search_locations]" \
    | xargs -r -t chmod -R a+rwX

# docker_run.sh runs the container as your own user id (so files written into the repository are yours, not
# root's). That id has no account in the image: HOME and USER give it a writable home, where docker_run.sh mounts
# the host cache folder (model downloads, torch.compile, Triton and FlashInfer caches survive between runs).
RUN mkdir -p /home/app/.cache && chmod -R 1777 /home/app
ENV HOME=/home/app \
    USER=app \
    HF_HOME=/home/app/.cache/huggingface

WORKDIR /workspace/Code/generate_practice_reasoning
# the base image starts "vllm serve"; this image starts a shell or the command given to docker run
ENTRYPOINT []
CMD ["bash"]
