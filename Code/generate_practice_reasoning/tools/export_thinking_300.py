"""Export the model's thinking for rows 1-300 (labels and wrong-answer diagnoses) for the review page.

    python3 tools/export_thinking_300.py        (from Code/generate_practice_reasoning; standard library only)

Reads the run logs (runs/<labels>/rows/row_NNNNN.json and runs/<diagnosis>/items/rNNNNN_wNNN.json) and writes
thinking_300/rows_001-010.json, rows_011-020.json, ... (10 rows per file), each
    {"labels": {"<row>": {"1": text, "2": text, "3": text}}, "diagnoses": {"<key>": text}}
taking the thinking of the attempt that succeeded. A prompt that was not asked (the order prompt for a one-practice
answer) or a diagnosis made with thinking off has no entry. Then packs the folder into thinking_300.tar.gz.
"""
import json
import os
import sys
import tarfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABELS = sys.argv[1] if len(sys.argv) > 1 else "qwen35_122b_ch3"
DIAG = sys.argv[2] if len(sys.argv) > 2 else "qwen35_122b_ch3_diag"
N, CHUNK = 300, 10
OUT = os.path.join(HERE, "thinking_300")


def succeeded(rec):
    """The calls of the attempt that succeeded, or None."""
    f = rec.get("final", {})
    if f.get("status") != "ok":
        return None
    return rec["attempts"][f["attempt"] - 1].get("calls", [])


files = {}
def chunk(row):
    a = (row - 1) // CHUNK * CHUNK + 1
    return files.setdefault(f"rows_{a:03d}-{a + CHUNK - 1:03d}.json", {"labels": {}, "diagnoses": {}})


n_labels = n_diag = 0
for row in range(1, N + 1):
    p = os.path.join(HERE, "runs", LABELS, "rows", f"row_{row:05d}.json")
    if not os.path.exists(p):
        continue
    with open(p, encoding="utf-8") as f:
        calls = succeeded(json.load(f))
    if not calls:
        continue
    texts = {str(c["step"]): c.get("reasoning_text") for c in calls if c.get("reasoning_text")}
    if texts:
        chunk(row)["labels"][str(row)] = texts
        n_labels += len(texts)

items = os.path.join(HERE, "runs", DIAG, "items")
for name in sorted(os.listdir(items)) if os.path.isdir(items) else []:
    if not name.endswith(".json"):
        continue
    row = int(name[1:6])
    if row > N:
        continue
    with open(os.path.join(items, name), encoding="utf-8") as f:
        calls = succeeded(json.load(f))
    if calls and calls[0].get("reasoning_text"):
        chunk(row)["diagnoses"][name[:-5]] = calls[0]["reasoning_text"]
        n_diag += 1

os.makedirs(OUT, exist_ok=True)
for name, data in sorted(files.items()):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
tar = os.path.join(HERE, "thinking_300.tar.gz")
with tarfile.open(tar, "w:gz") as t:
    t.add(OUT, arcname="thinking_300")
print(f"{n_labels} label answers and {n_diag} diagnoses with thinking, in {len(files)} files under {OUT}; "
      f"packed into {tar} ({os.path.getsize(tar) / 1e6:.1f} MB)")
