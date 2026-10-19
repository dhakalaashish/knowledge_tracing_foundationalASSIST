"""
The knowledge-state tool the agent reads mastery theta from (config "knowledge_tool"):
    ncdm     NeuralCDM trained by train_tools.py               -> tool_outputs/<split>/ncdm.npz
    maca_cd  plain MACA-CD trained by maca_cd/model/train.py   -> maca_cd/model/results/OurModel/state_<split>[_seed<N>].npz
Both give a students x concepts proficiency matrix (column c - 1 is concept id c) and the tool's own
probability for every test record, in the order of records['test'].
"""

import numpy as np

from common import TOOLS, maca_cd_state_file, tool_dir

TOOL_NAMES = {"ncdm": "NCDM", "maca_cd": "MACA-CD"}


def load_knowledge_tool(split, config, records):
    tool = config["knowledge_tool"]
    if tool not in TOOLS:
        raise ValueError(f"knowledge_tool must be one of {TOOLS}, not {tool!r}")
    if tool == "ncdm":
        path = tool_dir(split) / "ncdm.npz"
        if not path.exists():
            raise FileNotFoundError(f"{path} is missing: run python3 train_tools.py --split {split}")
        state = np.load(path)
    else:
        path = maca_cd_state_file(split, config.get("maca_cd_seed"))
        if not path.exists():
            raise FileNotFoundError(
                f"{path} is missing: train maca_cd on this split (cd ../maca_cd/model && python3 train.py "
                f"--split {split}), which saves its proficiency at the best epoch")
        state = np.load(path)
        if not np.array_equal(state["test_records"][:, :3], records["test"]):
            raise ValueError(f"{path} was trained on different test records than data/{split}: "
                             f"rerun maca_cd's data_preprocess.py/train.py or prepare_data.py")
    proficiency = state["proficiency"]
    expected = (records["n_students"], records["n_concepts"])
    if proficiency.shape != expected:
        raise ValueError(f"{path}: proficiency has shape {proficiency.shape}, expected {expected}")
    return {"name": TOOL_NAMES[tool], "proficiency": proficiency, "test_pred": state["test_pred"], "path": str(path)}
