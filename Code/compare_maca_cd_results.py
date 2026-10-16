"""
Benchmark table of MACA-CD (maca_cd) against the practice version (maca_cd_practice): ACC, AUC and DOA
on the three splits, laid out like the MACA-CD paper (methods as rows, each split's metrics as columns).

Reads training_logs_<split>.txt from each model's results folder. Each train.py run appends a timestamp
line and then a line for every epoch that set a new best test AUC, so the last line of the latest run is
that run's best epoch; its ACC, AUC and DOA are reported. Older runs in the same file are ignored. While
a run is still going, its line is the best so far.

Usage (from Code/):
    python3 compare_maca_cd_results.py                  # text table
    python3 compare_maca_cd_results.py --format markdown
    python3 compare_maca_cd_results.py --format latex
"""

import argparse
import os
import re

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
# (name shown, results folder relative to Code/)
MODELS = [
    ("MACA-CD", "maca_cd/model/results/OurModel"),
    ("MACA-CD + practices", "maca_cd_practice/model/results/OurModel"),
]
# (split file name, column heading)
SPLITS = [
    ("standard", "Standard"),
    ("cold", "Cold-start students"),
    ("zeroshot", "Zero-shot concepts"),
]
METRICS = ["ACC", "AUC", "DOA"]


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
    return float(match.group(1)) if match else None


def collect():
    """results[model][split] = {"epoch", "ACC", "AUC", "DOA", "by_practice"}, or None without results."""
    results = {}
    for model, results_dir in MODELS:
        results[model] = {}
        for split, _ in SPLITS:
            line = best_line(os.path.join(CODE_DIR, results_dir, "training_logs_%s.txt" % split))
            if line is None:
                results[model][split] = None
                continue
            entry = {"epoch": int(re.match(r"epoch: (\d+)", line).group(1))}
            for metric in METRICS:
                entry[metric] = value(line, metric)
            entry["by_practice"] = []
            if "DOA by practice:" in line:
                entry["by_practice"] = [(name, float(v)) for name, v in
                                        re.findall(r"([A-Z][A-Za-z ]+?):([\d.]+)", line.split("DOA by practice:")[1])]
            results[model][split] = entry
    return results


def best_per_column(results):
    """(split, metric) -> the highest value over the models, used to mark the best method."""
    best = {}
    for split, _ in SPLITS:
        for metric in METRICS:
            values = [r[split][metric] for r in results.values() if r[split] and r[split][metric] is not None]
            best[(split, metric)] = max(values) if len(values) > 1 else None
    return best


def cell(entry, metric, best, fmt):
    if entry is None or entry[metric] is None:
        return "-"
    text = "%.4f" % entry[metric]
    if best is None or entry[metric] != best:
        return text
    if fmt == "markdown":
        return "**%s**" % text
    if fmt == "latex":
        return "\\textbf{%s}" % text
    return text + "*"


def print_text(results, best):
    name_width = max(len(model) for model, _ in MODELS) + 2
    group_width = 9 * len(METRICS)
    print(" " * name_width + "   ".join("%-*s" % (group_width, heading) for _, heading in SPLITS))
    print("%-*s" % (name_width, "Method") + "   ".join("".join("%9s" % m for m in METRICS) for _ in SPLITS))
    for model, _ in MODELS:
        row = "%-*s" % (name_width, model)
        row += "   ".join("".join("%9s" % cell(results[model][split], m, best[(split, m)], "text") for m in METRICS)
                          for split, _ in SPLITS)
        print(row)
    print("\n* best value in the column. Each value comes from the run's best epoch (highest test AUC):")
    for model, _ in MODELS:
        print("  %s: %s" % (model, ", ".join(
            "%s epoch %d" % (split, results[model][split]["epoch"]) if results[model][split] else "%s no results" % split
            for split, _ in SPLITS)))


def print_markdown(results, best):
    print("| Method | " + " | ".join("%s %s" % (heading, m) for _, heading in SPLITS for m in METRICS) + " |")
    print("|---|" + "---|" * (len(SPLITS) * len(METRICS)))
    for model, _ in MODELS:
        print("| %s | " % model + " | ".join(cell(results[model][split], m, best[(split, m)], "markdown")
                                            for split, _ in SPLITS for m in METRICS) + " |")


def print_latex(results, best):
    print("\\begin{tabular}{l" + "ccc" * len(SPLITS) + "}")
    print("\\toprule")
    print(" & " + " & ".join("\\multicolumn{3}{c}{%s}" % heading for _, heading in SPLITS) + " \\\\")
    print("Method & " + " & ".join(m for _ in SPLITS for m in METRICS) + " \\\\")
    print("\\midrule")
    for model, _ in MODELS:
        print(model + " & " + " & ".join(cell(results[model][split], m, best[(split, m)], "latex")
                                         for split, _ in SPLITS for m in METRICS) + " \\\\")
    print("\\bottomrule")
    print("\\end{tabular}")


def print_practice_doa(results):
    rows = [(model, split, results[model][split]["by_practice"]) for model, _ in MODELS for split, _ in SPLITS
            if results[model][split] and results[model][split]["by_practice"]]
    if not rows:
        return
    names = [name for name, _ in rows[0][2]]
    print("\nDOA by practice (practice version, best epoch)")
    print("%-22s %-9s " % ("model", "split") + " ".join("%9s" % name.split()[0][:9] for name in names))
    for model, split, pairs in rows:
        values = dict(pairs)
        print("%-22s %-9s " % (model, split) + " ".join("%9s" % ("%.4f" % values[n] if n in values else "-")
                                                        for n in names))
    print("(columns: " + ", ".join(names) + ")")


def main():
    parser = argparse.ArgumentParser(description="Benchmark table of MACA-CD against the practice version")
    parser.add_argument("--format", choices=["text", "markdown", "latex"], default="text")
    args = parser.parse_args()

    results = collect()
    best = best_per_column(results)
    if args.format == "markdown":
        print_markdown(results, best)
    elif args.format == "latex":
        print_latex(results, best)
    else:
        print_text(results, best)
        print_practice_doa(results)
        print("\nDOA: MACA-CD ranks students per concept; the practice version per (concept, practice) pair,")
        print("with each exercise weighted by its joint Q-matrix entry.")


if __name__ == "__main__":
    main()
