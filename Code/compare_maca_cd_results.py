"""
Benchmark table of MACA-CD (maca_cd) against the practice version (maca_cd_practice): ACC, AUC and DOA
on the four splits, laid out like the MACA-CD paper (methods as rows, each split's metrics as columns),
as mean +- standard deviation over seeds, plus a paired comparison over the seeds both models ran.

Each train.py run appends a timestamp line and then a line for every epoch that set a new best test AUC
to its results file, so the last line of the file's latest run is that run's best epoch; its ACC, AUC
and DOA are used. Seeded runs (train.py --seed, run_maca_benchmark.sh) write
training_logs_<split>_seed<seed>.txt; a model/split without seeded runs falls back to the unseeded
training_logs_<split>.txt (one run). While a run is still going, its line is the best so far.

Usage (from Code/):
    python3 compare_maca_cd_results.py                  # text table + paired comparison
    python3 compare_maca_cd_results.py --format markdown
    python3 compare_maca_cd_results.py --format latex
"""

import argparse
import glob
import math
import os
import re

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
# (name shown, results folder relative to Code/); the paired comparison is MODELS[1] minus MODELS[0]
MODELS = [
    ("MACA-CD", "maca_cd/model/results/OurModel"),
    ("MACA-CD + practices", "maca_cd_practice/model/results/OurModel"),
]
# (split file name, column heading)
SPLITS = [
    ("standard", "Standard"),
    ("cold", "Cold-start students"),
    ("zeroshot", "Zero-shot concepts"),
    ("colditem", "Cold-start items"),
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


def parse_line(line):
    entry = {"epoch": int(re.match(r"epoch: (\d+)", line).group(1))}
    for metric in METRICS:
        match = re.search(metric + r":([\d.]+)", line)
        entry[metric] = float(match.group(1)) if match else None
    entry["by_practice"] = {}
    if "DOA by practice:" in line:
        entry["by_practice"] = {name: float(v) for name, v in
                                re.findall(r"([A-Z][A-Za-z ]+?):([\d.]+)", line.split("DOA by practice:")[1])}
    return entry


def collect():
    """runs[model][split] = {seed: entry}; seed None is an unseeded run."""
    runs = {}
    for model, results_dir in MODELS:
        runs[model] = {}
        for split, _ in SPLITS:
            seeded = {}
            for path in glob.glob(os.path.join(CODE_DIR, results_dir, "training_logs_%s_seed*.txt" % split)):
                line = best_line(path)
                if line is not None:
                    seeded[int(re.search(r"_seed(\d+)\.txt$", path).group(1))] = parse_line(line)
            if not seeded:
                line = best_line(os.path.join(CODE_DIR, results_dir, "training_logs_%s.txt" % split))
                if line is not None:
                    seeded[None] = parse_line(line)
            runs[model][split] = seeded
    return runs


def mean_std(values):
    """(mean, sample standard deviation or None, n) of the values that are not None."""
    values = [v for v in values if v is not None]
    if not values:
        return None, None, 0
    mean = sum(values) / len(values)
    if len(values) < 2:
        return mean, None, len(values)
    std = math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1))
    return mean, std, len(values)


def summarize(runs):
    """stats[model][split][metric] = (mean, std, n)."""
    return {model: {split: {metric: mean_std([e[metric] for e in runs[model][split].values()]) for metric in METRICS}
                    for split, _ in SPLITS} for model, _ in MODELS}


def best_per_column(stats):
    best = {}
    for split, _ in SPLITS:
        for metric in METRICS:
            means = [stats[model][split][metric][0] for model, _ in MODELS if stats[model][split][metric][0] is not None]
            best[(split, metric)] = max(means) if len(means) > 1 else None
    return best


def cell(stat, best, fmt):
    mean, std, n = stat
    if mean is None:
        return "-"
    is_best = best is not None and mean == best
    if fmt == "latex":
        text = "%.4f" % mean if std is None else "%.4f $\\pm$ %.4f" % (mean, std)
        return "\\textbf{%s}" % text if is_best else text
    text = "%.4f" % mean if std is None else "%.4f±%.4f" % (mean, std)
    if fmt == "markdown":
        return "**%s**" % text if is_best else text
    return text + ("*" if is_best else " ")


def print_text(runs, stats, best):
    name_width = max(len(model) for model, _ in MODELS) + 2
    col = 15
    group_width = col * len(METRICS)
    print(" " * name_width + "  ".join("%-*s" % (group_width, heading) for _, heading in SPLITS))
    print("%-*s" % (name_width, "Method") + "  ".join("".join("%*s" % (col, m) for m in METRICS) for _ in SPLITS))
    for model, _ in MODELS:
        print("%-*s" % (name_width, model) + "  ".join(
            "".join("%*s" % (col, cell(stats[model][split][m], best[(split, m)], "text")) for m in METRICS)
            for split, _ in SPLITS))
    print("\nmean±std over seeds (sample standard deviation); * higher mean in the column.")
    print("Runs (seed: best epoch):")
    for model, _ in MODELS:
        for split, _ in SPLITS:
            seeds = runs[model][split]
            text = ", ".join("%s: %d" % ("unseeded" if seed is None else seed, seeds[seed]["epoch"])
                             for seed in sorted(seeds, key=lambda s: -1 if s is None else s)) or "no results"
            print("  %-22s %-9s %s" % (model, split, text))


def paired_t_p_value(t, df):
    """Two-sided p-value of a t statistic (scipy if available)."""
    try:
        from scipy import stats as scipy_stats
        return 2 * scipy_stats.t.sf(abs(t), df)
    except ImportError:
        return None


def print_paired(runs):
    (base, _), (ours, _) = MODELS[0], MODELS[1]
    rows = []
    for split, _ in SPLITS:
        common = sorted(s for s in set(runs[base][split]) & set(runs[ours][split]) if s is not None)
        for metric in METRICS:
            diffs = [runs[ours][split][s][metric] - runs[base][split][s][metric] for s in common
                     if runs[ours][split][s][metric] is not None and runs[base][split][s][metric] is not None]
            rows.append((split, metric, diffs))
    if not any(len(diffs) >= 2 for _, _, diffs in rows):
        print("\nPaired comparison: needs at least 2 seeds run by both models (run_maca_benchmark.sh).")
        return
    print("\nPaired comparison over seeds (%s minus %s, same seed)" % (ours, base))
    print("%-9s %-6s %3s %11s %9s %8s %8s  %s" % ("split", "metric", "n", "mean diff", "sd diff", "t", "p", "seeds better"))
    for split, metric, diffs in rows:
        n = len(diffs)
        if n < 2:
            print("%-9s %-6s %3d  (fewer than 2 paired seeds)" % (split, metric, n))
            continue
        mean, std, _ = mean_std(diffs)
        if std == 0:
            t_text, p_text = "-", "-"
        else:
            t = mean / (std / math.sqrt(n))
            p = paired_t_p_value(t, n - 1)
            t_text, p_text = "%.2f" % t, ("%.3f" % p if p is not None else "n/a")
        better = sum(d > 0 for d in diffs)
        print("%-9s %-6s %3d %+11.4f %9.4f %8s %8s  %d of %d" % (split, metric, n, mean, std, t_text, p_text, better, n))
    print("Paired t-test across seeds (two-sided). With 3-5 seeds only consistent differences reach p < 0.05;")
    print("p > 0.05 means no evidence of a difference, not evidence that the methods are equal.")


def print_practice_doa(runs):
    ours = MODELS[1][0]
    lines = []
    names = []
    for split, _ in SPLITS:
        entries = [e for e in runs[ours][split].values() if e["by_practice"]]
        if not entries:
            continue
        names = list(entries[0]["by_practice"])
        lines.append((split, {n: mean_std([e["by_practice"].get(n) for e in entries]) for n in names}, len(entries)))
    if not lines:
        return
    print("\nDOA by practice (%s, mean over seeds)" % ours)
    print("%-9s %3s " % ("split", "n") + " ".join("%9s" % name.split()[0][:9] for name in names))
    for split, values, n in lines:
        print("%-9s %3d " % (split, n) + " ".join("%9s" % ("%.4f" % values[name][0] if values[name][0] is not None else "-")
                                                  for name in names))
    print("(columns: " + ", ".join(names) + ")")


def print_markdown(stats, best):
    print("| Method | " + " | ".join("%s %s" % (heading, m) for _, heading in SPLITS for m in METRICS) + " |")
    print("|---|" + "---|" * (len(SPLITS) * len(METRICS)))
    for model, _ in MODELS:
        print("| %s | " % model + " | ".join(cell(stats[model][split][m], best[(split, m)], "markdown")
                                            for split, _ in SPLITS for m in METRICS) + " |")


def print_latex(stats, best):
    print("\\begin{tabular}{l" + "ccc" * len(SPLITS) + "}")
    print("\\toprule")
    print(" & " + " & ".join("\\multicolumn{3}{c}{%s}" % heading for _, heading in SPLITS) + " \\\\")
    print("Method & " + " & ".join(m for _ in SPLITS for m in METRICS) + " \\\\")
    print("\\midrule")
    for model, _ in MODELS:
        print(model + " & " + " & ".join(cell(stats[model][split][m], best[(split, m)], "latex")
                                         for split, _ in SPLITS for m in METRICS) + " \\\\")
    print("\\bottomrule")
    print("\\end{tabular}")


def main():
    parser = argparse.ArgumentParser(description="Benchmark table of MACA-CD against the practice version")
    parser.add_argument("--format", choices=["text", "markdown", "latex"], default="text")
    args = parser.parse_args()

    runs = collect()
    stats = summarize(runs)
    best = best_per_column(stats)
    if args.format == "markdown":
        print_markdown(stats, best)
    elif args.format == "latex":
        print_latex(stats, best)
    else:
        print_text(runs, stats, best)
        print_paired(runs)
        print_practice_doa(runs)
        print("\nDOA: MACA-CD ranks students per concept; the practice version per (concept, practice) pair,")
        print("with each exercise weighted by its joint Q-matrix entry.")


if __name__ == "__main__":
    main()
