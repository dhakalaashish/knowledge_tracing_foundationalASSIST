"""
Side-by-side ACC, AUC and DOA of the MACA-CD variants, per split.

Reads training_logs_<split>.txt from the results folder of every model below. Each train.py run
appends a timestamp line and then a line for every epoch that set a new best test AUC, so the last
line of the latest run is that run's best epoch. Older runs in the same file are ignored. While a run
is still going, its line is the best so far.

Usage (from Code/):
    python3 compare_maca_cd_results.py
"""

import os
import re

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
# (name shown, results folder relative to Code/); maca_cd_practice writes one folder per practice_q
MODELS = [
    ("maca_cd", "maca_cd/model/results/OurModel"),
    ("practice_probabilities", "maca_cd_practice/model/results/OurModel_practice_probabilities"),
    ("practice_one_hot", "maca_cd_practice/model/results/OurModel_practice_one_hot"),
    ("practice_per_concept", "maca_cd_practice/model/results/OurModel_practice_per_concept"),
]
SPLITS = ["standard", "cold", "zeroshot"]


def best_line(path):
    """Last epoch line of the latest run in a training_logs file, or None."""
    if not os.path.exists(path):
        return None
    run = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip().strip('"').strip()
            if line.startswith("epoch"):
                run.append(line)
            elif line:
                run = []  # a timestamp line starts a new run
    return run[-1] if run else None


def value(line, key):
    match = re.search(key + r":([\d.]+)", line)
    return match.group(1) if match else "-"


def main():
    print("%-9s %-23s %6s %7s %7s %7s" % ("split", "model", "epoch", "ACC", "AUC", "DOA"))
    by_practice = []
    for split in SPLITS:
        for model, results_dir in MODELS:
            path = os.path.join(CODE_DIR, results_dir, "training_logs_%s.txt" % split)
            line = best_line(path)
            if line is None:
                print("%-9s %-23s no results" % (split, model))
                continue
            epoch = re.match(r"epoch: (\d+)", line).group(1)
            print("%-9s %-23s %6s %7s %7s %7s" % (split, model, epoch, value(line, "ACC"), value(line, "AUC"),
                                                  value(line, "DOA")))
            if "DOA by practice:" in line:
                pairs = re.findall(r"([A-Z][A-Za-z ]+?):([\d.]+)", line.split("DOA by practice:")[1])
                by_practice.append((split, model, pairs))
        print()

    if by_practice:
        names = [name for name, _ in by_practice[0][2]]
        print("DOA by practice")
        print("%-9s %-23s " % ("split", "model") + " ".join("%8s" % name.split()[0][:8] for name in names))
        for split, model, pairs in by_practice:
            values = dict(pairs)
            print("%-9s %-23s " % (split, model) + " ".join("%8s" % values.get(name, "-") for name in names))
        print("(columns: " + ", ".join(names) + ")")


if __name__ == "__main__":
    main()
