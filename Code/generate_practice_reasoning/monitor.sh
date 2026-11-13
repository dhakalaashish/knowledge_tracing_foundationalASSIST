#!/usr/bin/env bash
# Progress of run_gb300.sh (run with docker_run.sh or directly). Reading only: it never changes the run.
#
#   bash monitor.sh                 a live view, refreshed every 60 s (Ctrl-C quits the view; the run keeps going)
#   bash monitor.sh 300             refreshed every 300 s
#   bash monitor.sh once            one snapshot
#   SMOKE=1 bash monitor.sh         the smoke test instead of the real run
#   nohup bash monitor.sh log 600 >> logs/monitor.log 2>&1 &
#                                   a snapshot every 10 min appended to logs/monitor.log, kept after you log out
#
# For each step: ok / failed / retrying counts from runs/<name>/, the total from the step's log, the speed since
# the step (re)started and an estimate of the time left, vLLM's own progress line, and warnings (cut-off answers,
# Python errors). Results arrive in batches of up to 512, so the counts jump rather than climb steadily.

set -uo pipefail
cd "$(dirname "$0")"

NAME="${NAME:-practice-gb300}"
MODE=watch
INTERVAL=60
case "${1:-}" in
  once) MODE=once ;;
  log)  MODE=log; INTERVAL="${2:-600}" ;;
  [0-9]*) INTERVAL="$1" ;;
  "") ;;
  *) sed -n '2,12p' "$0"; exit 1 ;;
esac

# the same names as run_gb300.sh
T=""; LOGP=logs/step
if [ "${SMOKE:-0}" = "1" ]; then T=smoke_; LOGP=logs/smoke_step; fi
STEP_DIR=([1]=runs/${T}qwen35_122b/rows [2]=runs/${T}qwen35_122b_noex/rows [3]=runs/${T}qwen35_122b_ch3/rows
          [4]=runs/${T}qwen35_122b_diag/items [5]=runs/${T}qwen35_122b_noex_diag/items
          [6]=runs/${T}qwen35_122b_ch3_diag/items [7]=runs/${T}qwen35_122b_ch3_diag_nothink/items)
STEP_NAME=([1]="labels, standard prompts" [2]="labels, no examples (v3 prompts)" [3]="labels, Chapter 3 prompts"
           [4]="diagnosis, standard prompts" [5]="diagnosis, no examples" [6]="diagnosis, Chapter 3 prompts"
           [7]="fallback for step 6, thinking off")

hm() {  # minutes -> "2h05m"
  local m=$1
  if [ "$m" -ge 60 ]; then printf '%dh%02dm' $((m / 60)) $((m % 60)); else printf '%dm' "$m"; fi
}

# the first line matching $1 in each JSON file of $2 (the record's top-level "final" fields are indented 4 spaces)
first_lines() { find "$2" -name '*.json' -print0 2>/dev/null | xargs -0 -r grep -h -m1 "$1" 2>/dev/null; }

step_report() {
  local n=$1 dir=${STEP_DIR[$1]} log=$LOGP$1.log marker=$LOGP$1.started
  [ -e "$log" ] || [ -d "$dir" ] || { echo "step $n (${STEP_NAME[$n]}): not started"; return; }

  # The log grows across restarts. What describes the current run (its estimate, vLLM's progress bar, errors,
  # last lines) is read only from the part after the latest start marker. Markers are matched anywhere in a line:
  # in older logs a marker can follow a progress bar, which never ends its line.
  local cur off
  cur=$(mktemp)
  if [ -e "$log" ]; then
    off=$(grep -a -b -o "=== step $n started" "$log" | tail -1 | cut -d: -f1)
    if [ -n "$off" ]; then tail -c +"$((off + 1))" "$log" > "$cur"; else cp "$log" "$cur"; fi
  fi

  local state="not started" last
  last=$(grep -a -oE "=== step $n (started|finished).*" "$log" 2>/dev/null | tail -1)
  case "$last" in
    *finished*)
      state="finished ${last#*finished }"
      local first s e
      first=$(grep -a -oE "=== step $n started.*" "$log" | head -1)
      s=$(date -d "${first#*started }" +%s 2>/dev/null); e=$(date -d "${last#*finished }" +%s 2>/dev/null)
      if [ -n "$s" ] && [ -n "$e" ]; then state="$state (took $(hm $(( (e - s) / 60 ))))"; fi ;;
    *started*)  state="started ${last#*started }" ;;
  esac
  local running=0
  [[ "$state" == started* ]] && running=1

  local ok=0 failed=0 retry=0
  read -r ok failed retry < <(first_lines '^    "status": ' "$dir" |
    awk '/"ok"/{o++} /"failed"/{f++} /"pending/{p++} END{print o+0, f+0, p+0}')
  local done=$((ok + failed))
  local total
  total=$(grep -a -o -E 'of [0-9]+ (rows|wrong answers) already done' "$log" 2>/dev/null | tail -1 | awk '{print $2}')

  echo "step $n (${STEP_NAME[$n]}): $state"
  local pct="?"
  if [ -n "$total" ] && [ "$total" -gt 0 ]; then pct=$(awk -v d="$done" -v t="$total" 'BEGIN{printf "%.1f", 100*d/t}'); fi
  printf '  done %s of %s (%s%%)   ok %s   failed %s   retrying %s\n' "$done" "${total:-?}" "$pct" "$ok" "$failed" "$retry"

  if [ "$running" = 1 ] && [ -e "$marker" ]; then
    local now start mins since
    now=$(date +%s); start=$(stat -c %Y "$marker"); mins=$(( (now - start) / 60 ))
    since=$(find "$dir" -name '*.json' -newer "$marker" -print0 2>/dev/null |
            xargs -0 -r grep -l -m1 -E '^    "status": "(ok|failed)"' 2>/dev/null | wc -l)
    if [ "$since" -gt 0 ] && [ "$mins" -gt 0 ]; then
      local left=""
      if [ -n "$total" ]; then
        local lm=$(( (total - done) * mins / since ))
        left="
  time left: about $(hm "$lm") at this speed (finishing around $(date -d "+$lm min" '+%a %d %b %H:%M'))"
      fi
      echo "  speed: $since finished in $(hm "$mins") since this step (re)started ($(( since * 60 / mins ))/hour)$left"
    else
      echo "  speed: no results yet, $(hm "$mins") since this step (re)started (loading the model, or the first batch)"
    fi
  fi

  if [[ "$dir" == */items ]] && [ "$ok" -gt 0 ]; then
    echo "  error types: $(first_lines '^    "error_type": ' "$dir" |
      awk -F'"' '{c[$4]++} END{for (k in c) printf "%s %d  ", k, c[k]}')"
  fi

  if [ -e "$log" ]; then
    local cut tb est
    # the run's own estimate, written to the log every 10 minutes and at the end of each round
    est=$(grep -a -o 'PROGRESS.*' "$cur" | tail -1 | cut -c1-220)
    [ "$running" = 1 ] && [ -n "$est" ] && echo "  run's own estimate${est#PROGRESS}"
    cut=$(grep -a -c 'hit max_tokens' "$cur")
    tb=$(grep -a -c 'Traceback (most recent call last)' "$cur")
    [ "$cut" -gt 0 ] && echo "  answers cut off at MAX_TOKENS since this (re)start: $cut (each one is retried)"
    if [ "$tb" -gt 0 ]; then
      # the distinct error messages (also those of vLLM's engine process, whose lines carry a prefix); the root
      # cause is usually one of the first, the generic "Engine core initialization failed" comes last
      echo "  PYTHON ERRORS since this (re)start: $tb tracebacks; error messages:"
      grep -a -oE '\b[A-Za-z_.]*(Error|Exception): .{0,170}' "$cur" | awk '!seen[$0]++' | tail -5 | sed 's/^/    /'
    fi
    if [ "$running" = 1 ]; then
      local prog
      prog=$(tail -c 50000 "$cur" | tr '\r' '\n' | grep -a -o 'Processed prompts.*' | tail -1 | cut -c1-200)
      [ -n "$prog" ] && echo "  vLLM: $prog"
      echo "  last log lines:"
      tail -c 50000 "$cur" | tr '\r' '\n' | grep -a -v -E 'Processed prompts|^[[:space:]]*$' | tail -4 |
        cut -c1-200 | sed 's/^/    /'
    fi
  fi
  rm -f "$cur"
}

snapshot() {
  echo "================ $(date '+%Y-%m-%d %H:%M:%S') ================"
  if command -v docker >/dev/null 2>&1; then
    local s
    s=$(docker ps -a --filter "name=^${NAME}$" --format '{{.Status}}' 2>/dev/null | head -1)
    echo "container $NAME: ${s:-not found (not started with docker_run.sh, or removed)}"
  fi
  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw \
      --format=csv,noheader 2>/dev/null | sed 's/^/GPU: /'
  else  # no nvidia-smi (as on the GB300): ask the driver directly through pynvml
    python3 - <<'EOF' 2>/dev/null || echo "GPU: (no nvidia-smi or pynvml; try: nvitop -1)"
import pynvml as n
n.nvmlInit()
for i in range(n.nvmlDeviceGetCount()):
    h = n.nvmlDeviceGetHandleByIndex(i)
    name = n.nvmlDeviceGetName(h)
    name = name.decode() if isinstance(name, bytes) else name
    m = n.nvmlDeviceGetMemoryInfo(h)
    try: util = f"{n.nvmlDeviceGetUtilizationRates(h).gpu} %"
    except Exception: util = "? %"
    try: temp = f"{n.nvmlDeviceGetTemperature(h, 0)} C"
    except Exception: temp = "? C"
    try: power = f"{n.nvmlDeviceGetPowerUsage(h) / 1000:.0f} W"
    except Exception: power = "? W"
    print(f"GPU {i}: {name}, {util}, {m.used >> 20} MiB / {m.total >> 20} MiB, {temp}, {power}")
EOF
  fi
  echo "disk free here: $(df -h . | awk 'NR==2{print $4}')"
  echo
  # steps 4 and 5 (diagnoses from the standard and no-examples labels) are optional: shown only once started
  for n in 1 2 3 4 5 6 7; do
    if { [ "$n" = 4 ] || [ "$n" = 5 ] || [ "$n" = 7 ]; } && [ ! -e "$LOGP$n.log" ] && [ ! -d "${STEP_DIR[$n]}" ]; then continue; fi
    step_report "$n"
  done
  echo
}

case "$MODE" in
  once) snapshot ;;
  log)  while true; do snapshot; sleep "$INTERVAL"; done ;;
  watch)
    while true; do
      out=$(snapshot)
      clear 2>/dev/null || true
      echo "$out"
      echo "(refresh every ${INTERVAL}s; Ctrl-C quits this view, the run keeps going)"
      sleep "$INTERVAL"
    done ;;
esac
