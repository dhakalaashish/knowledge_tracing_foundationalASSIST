#!/bin/bash
# Benchmark MACA-CD (maca_cd) against the practice version (maca_cd_practice) on the standard,
# cold-start-student and zero-shot-concept splits: 6 training runs at once on one GPU, then the
# paper-style table of ACC, AUC and DOA (compare_maca_cd_results.py).
#
# Usage (from Code/ on the A100):
#   nohup bash run_maca_benchmark.sh > ../Data/maca_benchmark.log 2>&1 &
# Each run's epochs go to <model>/model/benchmark_<split>.log. The table is printed at the end of
# ../Data/maca_benchmark.log and saved as markdown to ../Data/maca_benchmark_table.md.
set -uo pipefail
cd "$(dirname "$0")"  # Code/
GPU=${GPU:-0}
SPLITS="standard cold zeroshot"
MODELS="maca_cd maca_cd_practice"

# Both models must train for the same number of epochs
epochs() { python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["number_epoch"])' "$1"; }
e_cd=$(epochs maca_cd/parameter.json)
e_pr=$(epochs maca_cd_practice/parameter.json)
if [ "$e_cd" != "$e_pr" ]; then
    echo "number_epoch differs (maca_cd $e_cd, maca_cd_practice $e_pr); make them equal first" >&2
    exit 1
fi
echo "== Epochs per run: $e_cd"

# Splits: maca_cd's are built once by its data/data_preprocess.py; the practice version's are rebuilt
# here because they hold the joint Q-matrix. Both use the same seed, so the train/test splits match.
for s in $SPLITS; do
    if [ ! -f "maca_cd/data/preprocessed/${s}_spilt.pkl" ]; then
        echo "maca_cd/data/preprocessed/${s}_spilt.pkl is missing; run python3 maca_cd/data/data_preprocess.py" >&2
        exit 1
    fi
done
echo "== Building the maca_cd_practice splits"
python3 maca_cd_practice/data/data_preprocess.py || exit 1

echo "== Starting 6 training runs on GPU $GPU"
pids=()
names=()
for model in $MODELS; do
    mkdir -p "$model/model/results/OurModel"
    for s in $SPLITS; do
        (cd "$model/model" && CUDA_VISIBLE_DEVICES=$GPU PYTHONUNBUFFERED=1 python3 train.py --split "$s" > "benchmark_${s}.log" 2>&1) &
        pids+=($!)
        names+=("$model $s")
        echo "   $model $s: pid $!, log $model/model/benchmark_${s}.log"
    done
done

failed=0
for i in "${!pids[@]}"; do
    if wait "${pids[$i]}"; then
        echo "== Finished: ${names[$i]}"
    else
        echo "== FAILED: ${names[$i]} (see its log; its best epoch so far is still in the results file)"
        failed=1
    fi
done

echo
echo "== Benchmark (best epoch of each run)"
python3 compare_maca_cd_results.py
python3 compare_maca_cd_results.py --format markdown > ../Data/maca_benchmark_table.md
echo
echo "Markdown table saved to Data/maca_benchmark_table.md"
exit $failed
