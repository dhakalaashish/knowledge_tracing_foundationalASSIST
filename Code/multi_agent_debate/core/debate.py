import asyncio
import logging
from datetime import datetime
from pathlib import Path
from shutil import copyfile

import hydra
import pandas as pd
from omegaconf import DictConfig

from core.create_agents import setup_debate
from core.file_handler import Experiment
from core.llm_api.llm import ModelAPI
from core.rollouts.rollout_base import RolloutBase
from core.utils import async_function_with_retry, setup_environment

LOGGER = logging.getLogger(__name__)


async def run_debates(
    rollout: RolloutBase,
    filename: Path,
    swap: bool = False,
    limit: int = None,
    num_debate_threads: int = 20,
):
    # load dataset
    full_df = pd.read_csv(filename, encoding="utf-8")
    if limit is not None:
        full_df = full_df.head(int(limit))
    if "complete" not in full_df.columns:
        full_df["complete"] = False
    if "transcript" not in full_df.columns:
        full_df["transcript"] = ""
    df = full_df[full_df["complete"] == False]

    start_time = datetime.now()
    LOGGER.info(f"Processing {filename}")
    LOGGER.info(f"Time is {start_time}")
    LOGGER.info(f"Processing {len(df)} rows")

    async def bounded_run(sem, index, row, swap):
        async with sem:
            return await rollout.run(index, row, swap=swap)

    sem = asyncio.Semaphore(num_debate_threads)
    tasks = [bounded_run(sem, index, row, swap) for index, row in df.iterrows()]
    results = await asyncio.gather(*tasks)
    correct = sum([bool(result["complete"]) for result in results])
    LOGGER.info(f"Processed {len(results)} rows. {correct}  were complete.")

    # Update dataframe
    df.update(
        pd.DataFrame(
            {
                "transcript": [result["transcript"] for result in results],
                "complete": [result["complete"] for result in results],
            },
            index=df.index,
        )
    )
    full_df.update(df)

    # save results
    full_df.to_csv(filename, index=False, encoding="utf-8")
    LOGGER.info(f"Time taken: {datetime.now() - start_time}")

    if full_df["complete"].eq(True).all():
        return True
    else:
        return False


def load_dataset(filename: Path, dataset_file: str):
    """
    Copy the practice-pair dataset written by build_dataset.py to the experiment's debate file.
    Replaces the QuALITY loader of the original code. An existing debate file is kept, so a
    stopped run resumes where it left off.
    """
    if filename.exists():
        return
    if not dataset_file or not Path(dataset_file).exists():
        raise FileNotFoundError(
            f"No debate file at {filename} and dataset_file={dataset_file!r} does not exist. "
            f"Run build_dataset.py first and pass ++dataset_file=<path>."
        )
    filename.parent.mkdir(parents=True, exist_ok=True)
    copyfile(dataset_file, filename)
    LOGGER.info(f"Copied dataset {dataset_file} to {filename}")


@hydra.main(version_base=None, config_path="config/", config_name="config")
def main(cfg: DictConfig):
    complete = asyncio.run(async_main(cfg))
    return complete


async def async_main(cfg: DictConfig):
    setup_environment(logger_level=cfg.logging)
    api_handler = ModelAPI(
        vllm_base_url=cfg.vllm_base_url,
        vllm_num_threads=cfg.vllm_num_threads,
        print_prompt_and_response=cfg.print_prompt_and_response,
    )
    exp_dir = Path(cfg.exp_dir)
    exp_dir.mkdir(parents=True, exist_ok=True)
    experiment = Experiment(
        exp_dir,
        cfg.method,
        cfg.method_type,
        cfg.use_intermediary,
    )
    if cfg.method_type == "baseline":
        assert cfg.rollout.num_steps == 0, "Baseline requires num_steps to be 0"

    # Load dataset
    filename = experiment.get_debate_filename(seed=cfg.seed, swap=False)
    cache_dir = filename.parent / f"cache_{filename.stem}"
    load_dataset(filename, cfg.dataset_file)

    rollout = setup_debate(
        cfg,
        cache_dir,
        api_handler,
    )

    # Heuristic to work out num threads
    _BoN_correct = cfg.correct_debater.BoN
    _BoN_incorrect = cfg.incorrect_debater.BoN
    num_debate_threads = int(int(cfg.num_threads) / max(1, _BoN_correct, _BoN_incorrect))

    LOGGER.info(f"Running debates with {num_debate_threads} threads")

    # Run with retry
    complete = await async_function_with_retry(
        run_debates,
        rollout,
        filename,
        swap=False,
        limit=cfg.limit,
        num_debate_threads=num_debate_threads,
    )

    # Interactive (intermediary) debates are run again with the answer order swapped, because the
    # judge's questions depend on the order. Each practice pair is therefore debated twice.
    if cfg.method_type == "seq" or (cfg.method == "debate" and cfg.use_intermediary):
        filename = experiment.get_debate_filename(seed=cfg.seed, swap=True)
        cache_dir = filename.parent / f"cache_{filename.stem}"
        load_dataset(filename, cfg.dataset_file)

        rollout.cache_dir = cache_dir
        complete_swap = await async_function_with_retry(
            run_debates,
            rollout,
            filename,
            swap=True,
            limit=cfg.limit,
            num_debate_threads=num_debate_threads,
        )
    else:
        complete_swap = True
    return complete and complete_swap


if __name__ == "__main__":
    main()
