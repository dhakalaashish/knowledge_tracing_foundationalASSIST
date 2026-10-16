#!/bin/bash
# Benchmark MACA-CD (maca_cd) against the practice version (maca_cd_practice) on the standard,
# cold-start-student, zero-shot-concept and cold-start-item splits, repeated with several seeds: every
# (model, split, seed) is one training run, up to MAX_PARALLEL of them at once on one GPU. At the end it
# prints the table of mean +- standard deviation over the seeds and the paired comparison
# (compare_maca_cd_results.py).
#
# Usage (from Code/ on the A100):
#   nohup bash run_maca_benchmark.sh > ../Data/maca_benchmark.log 2>&1 &
# Settings (environment variables):
#   SEEDS="1 2 3 4 5"   seeds to run (default 1-5: 2 models x 4 splits x 5 seeds = 40 runs)
#   MAX_PARALLEL=12     runs at once; each run is one CPU core (batch loading) and about 1 GB of GPU memory
#   GPU=0               GPU to use
# e.g. SEEDS="1 2 3" MAX_PARALLEL=6 nohup bash run_maca_benchmark.sh > ../Data/maca_benchmark.log 2>&1 &
#
# Each run's epochs go to <model>/model/benchmark_<split>_seed<seed>.log and its best epochs to
# <model>/model/results/OurModel/training_logs_<split>_seed<seed>.txt. The table is printed at the end of
# ../Data/maca_benchmark.log and saved as markdown to ../Data/maca_benchmark_table.md.
set -uo pipefail
cd "$(dirname "$0")"  # Code/
GPU=${GPU:-0}
SEEDS=${SEEDS:-"1 2 3 4 5"}
MAX_PARALLEL=${MAX_PARALLEL:-12}
SPLITS="standard cold zeroshot colditem"
MODELS="maca_cd maca_cd_practice"
# Runs share the CPU: keep each one's math libraries to a couple of threads
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-2}

# Both models must train for the same number of epochs
epochs() { python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["number_epoch"])' "$1"; }
e_cd=$(epochs maca_cd/parameter.json)
e_pr=$(epochs maca_cd_practice/parameter.json)
if [ "$e_cd" != "$e_pr" ]; then
    echo "number_epoch differs (maca_cd $e_cd, maca_cd_practice $e_pr); make them equal first" >&2
    exit 1
fi
echo "== Epochs per run: $e_cd; seeds: $SEEDS; up to $MAX_PARALLEL runs at once"

# Splits: both models' splits are rebuilt here (a minute each). The split seed is fixed, so the standard,
# cold and zeroshot splits are the same as before and the two models get the same train/test data; the
# practice version's splits also hold the joint Q-matrix.
for model in $MODELS; do
    echo "== Building the $model splits"
    python3 "$model/data/data_preprocess.py" || exit 1
done

# Every run writes its exit code to STATUS_DIR, so failures can be reported at the end
STATUS_DIR=$(mktemp -d)
trap 'rm -rf "$STATUS_DIR"' EXIT
runs=()
total=0
for seed in $SEEDS; do for model in $MODELS; do for s in $SPLITS; do total=$((total + 1)); done; done; done
echo "== Starting $total training runs on GPU $GPU"
started=0
for seed in $SEEDS; do
    for model in $MODELS; do
        mkdir -p "$model/model/results/OurModel"
        for s in $SPLITS; do
            # Wait for a free slot
            while [ "$(jobs -rp | wc -l)" -ge "$MAX_PARALLEL" ]; do
                wait -n
            done
            name="${model}_${s}_seed${seed}"
            log="benchmark_${s}_seed${seed}.log"
            (cd "$model/model" && CUDA_VISIBLE_DEVICES=$GPU PYTHONUNBUFFERED=1 python3 train.py --split "$s" --seed "$seed" > "$log" 2>&1
             echo $? > "$STATUS_DIR/$name") &
            started=$((started + 1))
            runs+=("$name")
            echo "   [$started/$total] $(date +%T) started $model $s seed $seed (log $model/model/$log)"
        done
    done
done
wait

failed=0
for name in "${runs[@]}"; do
    status=$(cat "$STATUS_DIR/$name" 2>/dev/null || echo "missing")
    if [ "$status" != "0" ]; then
        echo "== FAILED: $name (exit $status; see its log; its best epoch so far is still in the results file)"
        failed=1
    fi
done
[ "$failed" = "0" ] && echo "== All $total runs finished"

echo
echo "== Benchmark (mean +- standard deviation over seeds, best epoch of each run)"
python3 compare_maca_cd_results.py
python3 compare_maca_cd_results.py --format markdown > ../Data/maca_benchmark_table.md
echo
echo "Markdown table saved to Data/maca_benchmark_table.md"
exit $failed
