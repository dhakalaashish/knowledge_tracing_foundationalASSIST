#!/usr/bin/env bash
# Summary of the smoke test (SMOKE=1 bash run_gb300.sh, or SMOKE=1 bash docker_run.sh). Reading only.
#   bash smoke_check.sh
# Shows, for each step that ran: whether it finished without Python errors, ok / failed counts and why
# anything failed, token use per prompt (and how close it came to MAX_TOKENS), the labels and the diagnoses of
# each problem (standard, no examples and Chapter 3 side by side), and whether the outputs were written.
# Needs only the host's python3 (standard library).
cd "$(dirname "$0")"
python3 - "$@" <<'EOF'
import csv, glob, json, os, re, sys
csv.field_size_limit(sys.maxsize)

RUNS = {1: "runs/smoke_qwen35_122b", 2: "runs/smoke_qwen35_122b_noex", 3: "runs/smoke_qwen35_122b_ch3",
        4: "runs/smoke_qwen35_122b_diag", 5: "runs/smoke_qwen35_122b_noex_diag", 6: "runs/smoke_qwen35_122b_ch3_diag"}
NAMES = {1: "labels, standard", 2: "labels, no examples", 3: "labels, Chapter 3",
         4: "diagnosis, standard", 5: "diagnosis, no examples", 6: "diagnosis, Chapter 3"}
LABEL_STEPS = (1, 2, 3)
DIAG_STEPS = (4, 5, 6)
SUFFIXES = ("reasoning", "ordering_reasoning", "top_practice", "top_practice_reasoning")
problems = []

def load(d, sub):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, sub, "*.json"))):
        with open(p, encoding="utf-8") as f:
            r = json.load(f)
        out[r.get("row") if sub == "rows" else r.get("key")] = r
    return out

def max_tokens(recs):
    for r in recs.values():
        s = (r.get("generation_params") or {}).get("sampling") or {}
        if s.get("max_tokens"):
            return s["max_tokens"]
    return None

data = {}
for n, d in RUNS.items():
    print(f"=== step {n} ({NAMES[n]})")
    log = f"logs/smoke_step{n}.log"
    text = open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
    started = re.findall(rf"=== step {n} started (.*)", text)
    finished = re.findall(rf"=== step {n} finished (.*)", text)
    tb = text.count("Traceback (most recent call last)")
    print(f"  log: {'finished' if finished else ('started, not finished' if started else 'not started')}"
          + (f"  ({started[-1].strip()} -> {finished[-1].strip()})" if finished and started else "")
          + (f"  PYTHON ERRORS: {tb}" if tb else ""))
    if tb:
        last = [l for l in text.splitlines() if re.match(r"^[A-Za-z_.]*(Error|Exception)\b", l)]
        if last:
            print(f"  last error: {last[-1][:300]}")
        problems.append(f"step {n}: Python error in {log}")
    recs = load(d, "rows" if n in LABEL_STEPS else "items")
    data[n] = recs
    if not recs:
        print("  no results")
        problems.append(f"step {n}: no results")
        continue
    st = {}
    for r in recs.values():
        st[r["final"]["status"]] = st.get(r["final"]["status"], 0) + 1
    print("  status: " + ", ".join(f"{k} {v}" for k, v in sorted(st.items())))
    for k, r in recs.items():
        f = r["final"]
        if f["status"] != "ok":
            problems.append(f"step {n}: {k} is {f['status']}")
            why = ((f.get("last_failure_reason") or "-").splitlines() or ["-"])[0]
            print(f"  NOT OK {k}: {f['status']}: {why[:250]}")
        for a in r["attempts"]:
            if a.get("failure_reason"):
                print(f"  retry note {k}, attempt {a['attempt']}: {a['failure_reason'].splitlines()[0][:200]}")
    mt = max_tokens(recs)
    by_step = {}
    for r in recs.values():
        for a in r["attempts"]:
            for c in a.get("calls", []):
                u = c.get("usage") or {}
                s = by_step.setdefault(c.get("step", "?"), {"n": 0, "out": [], "inp": [], "cut": 0})
                s["n"] += 1
                s["out"].append(u.get("completion_tokens") or 0)
                s["inp"].append(u.get("prompt_tokens") or 0)
                s["cut"] += c.get("stop_reason") == "length"
    for s, v in sorted(by_step.items(), key=lambda kv: str(kv[0])):
        print(f"  prompt {s}: {v['n']} calls; input up to {max(v['inp']):,} tokens; output mean "
              f"{sum(v['out']) // max(1, len(v['out'])):,}, max {max(v['out']):,}"
              + (f" of {mt:,} allowed" if mt else "") + (f"; {v['cut']} cut off" if v["cut"] else ""))

print("\n=== labels (standard | no examples | Chapter 3)")
for row in sorted(set().union(*(data.get(n, {}) for n in LABEL_STEPS))):
    print(f"  row {row}:")
    for n in LABEL_STEPS:
        r = data.get(n, {}).get(row)
        f = r["final"] if r else {}
        if f.get("status") == "ok":
            print(f"    {NAMES[n]:<20} {' > '.join(f['ordering'])}   | top: {f['top_practice']}")
        else:
            print(f"    {NAMES[n]:<20} {f.get('status', 'missing')}")

print("\n=== diagnoses (standard | no examples | Chapter 3)")
diag_keys = set().union(*(data.get(n, {}) for n in DIAG_STEPS))
for key in sorted(diag_keys, key=lambda k: [int(x) for x in re.findall(r"\d+", k)]):
    r = next(data[n][key] for n in DIAG_STEPS if key in data.get(n, {}))
    print(f"  {key} row {r['row']} wrong answer {r['wrong_answer'][:40]!r} ({r['students']} students):")
    for n in DIAG_STEPS:
        x = data.get(n, {}).get(key)
        f = x["final"] if x else {}
        if f.get("status") == "ok":
            a = f["answer_json"]
            print(f"    {NAMES[n]:<20} {a['error_type']:<9} failed at: {f.get('failed_practice') or '-':<30} "
                  f"confidence {a['confidence']}; {a['reconstruction'][:80]}")
        else:
            print(f"    {NAMES[n]:<20} {f.get('status', 'missing')}")

print("\n=== outputs")
p = "runs/smoke/Problems.csv"
if os.path.exists(p):
    with open(p, encoding="utf-8", newline="") as f:
        rd = csv.reader(f)
        head = next(rd)
        rows = list(rd)
    for n in LABEL_STEPS:
        prefix = os.path.basename(RUNS[n])
        col = f"{prefix}_top_practice"
        if col not in head:
            print(f"  {p}: no column {col}")
            problems.append(f"step {n}: labels not written into {p}")
            continue
        i = head.index(col)
        filled = sum(1 for r in rows if i < len(r) and r[i])
        cols = [f"{prefix}_{s}" for s in SUFFIXES if f"{prefix}_{s}" in head]
        print(f"  {p}: {', '.join(cols)}; {filled} rows filled")
for n in DIAG_STEPS:
    p = f"runs/smoke/wrong_answer_diagnosis_{os.path.basename(RUNS[n])}.csv"
    if os.path.exists(p):
        with open(p, encoding="utf-8", newline="") as f:
            print(f"  {p}: {sum(1 for _ in f) - 1} diagnoses")
    else:
        print(f"  {p}: missing")
        problems.append(f"step {n}: {p} missing")

print()
if problems:
    print("SMOKE TEST: check these (send me this whole output):")
    for x in problems:
        print("  - " + x)
else:
    print("SMOKE TEST PASSED: every step finished, every item ok, outputs written.")
EOF
