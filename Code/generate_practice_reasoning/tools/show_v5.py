"""Read a v5 run (label_v5.py) problem by problem: the item text, its correct answer and skills, then every common
wrong answer with its diagnosis (prompt 5), then the item's labels (prompt 6), and any failed attempts.

    python3 tools/show_v5.py runs/<prefix> [rows, e.g. 1,65,260]      | less -R
    python3 tools/show_v5.py runs/<prefix> --plain > v5_review.txt          (no colours, for a text file)

Reads only runs/<prefix>/rows/row_NNNNN.json (standard library only).
"""
import json
import os
import sys
import textwrap

args = [a for a in sys.argv[1:] if not a.startswith("--")]
PLAIN = "--plain" in sys.argv
if not args:
    sys.exit(__doc__)
RUN = args[0]
WANT = None
if len(args) > 1:
    WANT = set()
    for part in args[1].split(","):
        if "-" in part:
            a, b = part.split("-")
            WANT.update(range(int(a), int(b) + 1))
        elif part.strip():
            WANT.add(int(part))

B, D, Y, R, G, X = ("", "", "", "", "", "") if PLAIN else ("\033[1m", "\033[2m", "\033[33m", "\033[31m", "\033[32m", "\033[0m")
SHORT = {"Representing": "REP", "Abstracting and Generalizing": "A&G", "Justifying and Proving": "J&P",
         "Mathematical Modeling": "MOD", "Collaborative Mathematics": "COL", "Procedural Fluency": "PF"}
W = 110


def wrap(text, indent="   ", first=None):
    text = " ".join(str(text or "").split())
    return textwrap.fill(text, W, initial_indent=first if first is not None else indent, subsequent_indent=indent) if text else (first or indent).rstrip()


def failure(a):
    et, fp = a.get("error_type") or a.get("outcome"), a.get("failed_practice", "")
    if et == "correct":
        return "correct"
    if et == "practice":
        return f"practice error at {fp}"
    if et == "math_fact":
        return f"math-fact error at {fp}: {a.get('math_fact', '')}"
    if et == "comprehension":
        return f"comprehension error: {a.get('comprehension', '')}"
    if et == "stopped_early":
        return f"stopped early, before {fp}"
    return "unexplained (no reasonable process)"


def failed_attempts(part):
    out = []
    for at in part.get("earlier_failed_attempts", []) + part.get("attempts", []):
        if at.get("failure_reason"):
            out.append(f"attempt {at.get('attempt')}: {str(at['failure_reason']).splitlines()[0]}")
    return out


rows_dir = os.path.join(RUN, "rows")
names = sorted(n for n in os.listdir(rows_dir) if n.endswith(".json"))
n_shown = 0
for name in names:
    with open(os.path.join(rows_dir, name), encoding="utf-8") as f:
        rec = json.load(f)
    if WANT and rec["row"] not in WANT:
        continue
    n_shown += 1
    st = rec.get("final", {}).get("status", "?")
    print(f"\n{B}{'=' * W}{X}")
    print(f"{B}ROW {rec['row']}{X}  (problem {rec['problem_id']}, {rec.get('problem_type', '')})  status: "
          f"{G if st == 'ok' else R}{st}{X}")
    print(f"{B}{'=' * W}{X}")
    print(f"{B}ITEM{X}")
    for line in str(rec.get("problem_text", "")).splitlines():
        print(wrap(line, "   ") if line.strip() else "")
    print(f"{B}Correct answer:{X} {rec.get('correct', '')}")
    print(f"{B}Skills:{X} " + "; ".join(f"{s['code']} ({s['name']})" for s in rec.get("skills", [])))

    # ---- prompt 5: the wrong answers, most students first
    ws = sorted(rec.get("wrong", {}).values(), key=lambda w: (-w.get("students", 0), w.get("rank", 0)))
    print(f"\n{Y}{B}--- COMMON WRONG ANSWERS (prompt 5): {len(ws)} ---{X}")
    if not ws:
        print("   (none given by enough students: prompt 6 ran without evidence)")
    for i, w in enumerate(ws, 1):
        fin = w.get("final", {})
        head = f"w{i}  \"{w.get('wrong_answer')}\"  {w.get('students')} students ({round(100 * w.get('share', 0))}% of wrong answers)"
        if fin.get("status") != "ok":
            print(f"{B}{head}{X}  {R}{fin.get('status')}{X}: {fin.get('last_failure_reason', '')}")
            continue
        a = fin["answer_json"]
        print(f"{B}{head}{X}  ->  {B}{failure(a)}{X}  [confidence {a.get('confidence')}; attempt {fin.get('attempt')}]")
        print(wrap(a.get("student_process"), "      ", "   process:     "))
        print(wrap(a.get("explanation"), "      ", "   explanation: "))
        if a.get("by_skill"):
            print(wrap("; ".join(f"{b['skill']}: {failure(b)}" for b in a["by_skill"]), "      ", "   by skill:    "))
        sol = " | ".join(f"{s['step']}. {s['skill']} {SHORT.get(s['practice'], s['practice'])}: {s['does']}" for s in a.get("solution", []))
        print(D + wrap(sol, "      ", "   its solution: ") + X)
        for fa in failed_attempts(w):
            print(f"   {R}{fa}{X}")

    # ---- prompt 6: the labels
    p = rec.get("problem", {})
    pf = p.get("final", {})
    print(f"\n{G}{B}--- LABELS (prompt 6) ---{X}")
    if pf.get("status") != "ok":
        print(f"   {R}{pf.get('status')}{X}: {pf.get('last_failure_reason', '')}")
    else:
        a, d = pf["answer_json"], pf.get("derived") or {}
        print(f"   evidence used: {'yes' if pf.get('evidence_used') else 'no'};  attempt {pf.get('attempt')}")
        for s in a.get("skills", []):
            print(f"{B}   {s['skill']}{X}")
            if s.get("not_exercised"):
                print(wrap(s["not_exercised"], "        ", "      not exercised: "))
            for it in s.get("practices_used", []):
                print(f"      {it['order']}. {B}{it['practice']}{X}")
                print(wrap(it.get("why"), "           ", "         why:            "))
                print(wrap(it.get("likely_errors"), "           ", "         likely errors:  "))
        print(f"{B}   Order:{X} {' > '.join(d.get('ordering', []))}")
        print(f"{B}   Top practice:{X} {a.get('top_practice')} ({a.get('top_practice_basis')})")
        print(wrap(a.get("top_practice_why"), "      "))
        if a.get("math_facts"):
            print(f"{B}   Math facts:{X}")
            for m in a["math_facts"]:
                print(wrap(m.get("fact"), "        ", f"    - [{m.get('skill')}] "))
        if a.get("practices_not_used"):
            print(f"{B}   Not used:{X}")
            for it in a["practices_not_used"]:
                print(wrap(it.get("why"), "        ", f"    - {SHORT.get(it['practice'], it['practice'])}: "))
        if a.get("comprehension_note"):
            print(f"{B}   Comprehension note:{X} {a['comprehension_note']}")
    for fa in failed_attempts(p):
        print(f"   {R}{fa}{X}")
print(f"\n{n_shown} problems shown from {rows_dir}")
