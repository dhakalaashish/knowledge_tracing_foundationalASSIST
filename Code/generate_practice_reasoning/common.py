"""Shared pieces: paths, prompts, problem loading, answer checking, run logs and the CSV merge."""

import csv
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

import prompts as P

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DEFAULT_PROBLEMS_CSV = os.path.join(REPO_ROOT, "Data", "Problems.csv")
RENDERED_JSONL = os.path.join(HERE, "problems_rendered.jsonl")
RUNS_DIR = os.path.join(HERE, "runs")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_prompts():
    """The three system prompts and the three user prompt templates, all from prompts.py."""
    if "{PROBLEM}" not in P.Q1_TEMPLATE:
        raise ValueError("prompts.Q1_TEMPLATE must contain {PROBLEM}")
    if "{PROBLEM}" not in P.Q2_TEMPLATE or "{PRACTICES}" not in P.Q2_TEMPLATE:
        raise ValueError("prompts.Q2_TEMPLATE must contain {PROBLEM} and {PRACTICES}")
    if "{PROBLEM}" not in P.Q3_TEMPLATE or "{ANALYSIS}" not in P.Q3_TEMPLATE:
        raise ValueError("prompts.Q3_TEMPLATE must contain {PROBLEM} and {ANALYSIS}")
    return {"system_1": P.SYSTEM_PROMPT_1, "system_2": P.SYSTEM_PROMPT_2, "system_3": P.SYSTEM_PROMPT_3,
            "q1_template": P.Q1_TEMPLATE, "q2_template": P.Q2_TEMPLATE, "q3_template": P.Q3_TEMPLATE}


PLACEHOLDER_RE = re.compile(r"\{(PROBLEM|PRACTICES|ANALYSIS)\}")


def fill(template, **values):
    """Fill {PROBLEM} / {PRACTICES} / {ANALYSIS} in one pass (not str.format: problem texts contain
    braces, and text that was filled in is never searched again)."""
    return PLACEHOLDER_RE.sub(lambda m: values[m.group(1)], template)


def build_prompt1(prompts, problem_text):
    return fill(prompts["q1_template"], PROBLEM=problem_text)


def practices_for_ordering(answer1):
    """The practices answer 1 lists as used, one line each ("- <practice>: <why>"), in the fixed order of
    prompts.PRACTICES, so prompt 2 does not see answer 1's order."""
    why = {it["practice"]: " ".join(it["why"].split()) for it in answer1["practices_used"]}
    return "\n".join(f"- {p}: {why[p]}" for p in P.PRACTICES if p in why)


def build_prompt2(prompts, problem_text, answer1):
    """Prompt 2 (order) gets the problem and the practices answer 1 lists as used."""
    return fill(prompts["q2_template"], PROBLEM=problem_text, PRACTICES=practices_for_ordering(answer1))


def combine(answer1, answer2):
    """Answer 1 with its practices_used put in answer 2's order and renumbered (why and likely_errors
    from answer 1); practices_not_used unchanged."""
    by_name = {it["practice"]: it for it in answer1["practices_used"]}
    used = []
    for i, step in enumerate(answer2["ordering"], 1):
        it = by_name[step["practice"]]
        used.append({"order": i, "practice": it["practice"], "why": it["why"], "likely_errors": it["likely_errors"]})
    return {"practices_used": used, "practices_not_used": answer1["practices_not_used"]}


def build_prompt3(prompts, problem_text, combined):
    """Prompt 3 (top practice) gets the problem and the combined analysis as JSON, indented."""
    analysis = json.dumps(combined, ensure_ascii=False, indent=2)
    return fill(prompts["q3_template"], PROBLEM=problem_text, ANALYSIS=analysis)


def load_problems(path=RENDERED_JSONL):
    """row (1-based data row of Problems.csv) -> {"row", "problem_id", "text"}."""
    problems = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                problems[rec["row"]] = rec
    return problems


def parse_rows(spec, n_max):
    """'1-300,450,500-510' -> sorted list of rows. None means all rows."""
    if not spec:
        return list(range(1, n_max + 1))
    rows = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            rows.update(range(int(a), int(b) + 1))
        else:
            rows.add(int(part))
    bad = [r for r in rows if r < 1 or r > n_max]
    if bad:
        raise ValueError(f"rows out of range 1-{n_max}: {sorted(bad)[:10]}")
    return sorted(rows)


# ---------------------------------------------------------------- checking the answers

FENCE_RE = re.compile(r"^```[A-Za-z]*\s*\n(.*?)\n?```$", re.S)


def parse_json_answer(text):
    """Parse an answer that should be exactly one JSON object.

    Returns (obj, how) where how is "exact" (the whole answer parsed as JSON) or "fenced" (the
    whole answer was one ```json ... ``` block). Anything else, including text before or after
    the object, raises ValueError.
    """
    s = (text or "").strip()
    how = "exact"
    m = FENCE_RE.match(s)
    if m:
        s, how = m.group(1).strip(), "fenced"
    try:
        obj = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"not valid JSON: {e}") from None
    if not isinstance(obj, dict):
        raise ValueError(f"expected a JSON object, got {type(obj).__name__}")
    return obj, how


def _why(item, where, key="why"):
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}: \"{key}\" must be a non-empty string")


def check_answer1(obj):
    """Rules for answer 1 (see prompts.PROMPT_RESPONSE_1). Raises ValueError on the first problem."""
    for key in ("practices_used", "practices_not_used"):
        if not isinstance(obj.get(key), list):
            raise ValueError(f"\"{key}\" must be a list")
    used, not_used = obj["practices_used"], obj["practices_not_used"]
    if not used:
        raise ValueError("\"practices_used\" is empty")
    seen = []
    for i, item in enumerate(used, 1):
        where = f"practices_used[{i}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where} must be an object")
        if item.get("practice") not in P.PRACTICES:
            raise ValueError(f"{where}: unknown practice {item.get('practice')!r}")
        if item.get("order") != i or isinstance(item.get("order"), bool):
            raise ValueError(f"{where}: \"order\" must be {i}")
        _why(item, where)
        _why(item, where, "likely_errors")
        seen.append(item["practice"])
    for i, item in enumerate(not_used, 1):
        where = f"practices_not_used[{i}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where} must be an object")
        if item.get("practice") not in P.PRACTICES:
            raise ValueError(f"{where}: unknown practice {item.get('practice')!r}")
        _why(item, where)
        seen.append(item["practice"])
    dup = sorted({p for p in seen if seen.count(p) > 1})
    missing = [p for p in P.PRACTICES if p not in seen]
    if dup:
        raise ValueError(f"listed more than once: {', '.join(dup)}")
    if missing:
        raise ValueError(f"missing: {', '.join(missing)}")


def check_answer2(obj, answer1):
    """Rules for answer 2, the order (see prompts.PROMPT_RESPONSE_2): exactly the practices answer 1
    lists as used, each once, numbered 1, 2, 3..., each with a non-empty step, and a non-empty why."""
    steps = obj.get("ordering")
    if not isinstance(steps, list) or not steps:
        raise ValueError("\"ordering\" must be a non-empty list")
    got = []
    for i, item in enumerate(steps, 1):
        where = f"ordering[{i}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where} must be an object")
        if item.get("practice") not in P.PRACTICES:
            raise ValueError(f"{where}: unknown practice {item.get('practice')!r}")
        if item.get("order") != i or isinstance(item.get("order"), bool):
            raise ValueError(f"{where}: \"order\" must be {i}")
        _why(item, where, "step")
        got.append(item["practice"])
    used = [it["practice"] for it in answer1["practices_used"]]
    if sorted(got) != sorted(used) or len(set(got)) != len(got):
        raise ValueError(f"\"ordering\" must list exactly the practices of answer 1 ({', '.join(used)}) once each, "
                         f"got {', '.join(got)}")
    _why(obj, "answer 2")


def check_answer3(obj, combined):
    """Rules for answer 3, the top practice (see prompts.PROMPT_RESPONSE_3): one of the six practices,
    one that the analysis lists as used, and a non-empty why."""
    top = obj.get("top_practice")
    if top not in P.PRACTICES:
        raise ValueError(f"\"top_practice\" must be one of the six practices, got {top!r}")
    used = [it["practice"] for it in combined["practices_used"]]
    if top not in used:
        raise ValueError(f"\"top_practice\" {top!r} is not in practices_used of the analysis ({', '.join(used)})")
    _why(obj, "answer 3")


class AnswerChecker:
    """Checks the three answers of one problem as they arrive.

    check(step, text) returns None if the answer is valid (and keeps the parsed object in
    .parsed), or a message saying what is wrong. Each prompt is only sent after the answer before it
    passes, because it is built from it. After answer 2 passes, .combined holds answer 1 in answer 2's
    order (the analysis prompt 3 gets).
    """

    def __init__(self):
        self.parsed = []
        self.how = []
        self.combined = None

    def check(self, turn, text):
        try:
            obj, how = parse_json_answer(text)
            if turn == 1:
                check_answer1(obj)
            elif turn == 2:
                check_answer2(obj, self.parsed[0])
            else:
                check_answer3(obj, self.combined)
        except ValueError as e:
            return f"answer {turn}: {e}"
        self.parsed.append(obj)
        self.how.append(how)
        if turn == 2:
            self.combined = combine(self.parsed[0], obj)
        return None


# ---------------------------------------------------------------- run directory and row logs

def row_path(run_dir, row):
    return os.path.join(run_dir, "rows", f"row_{row:05d}.json")


def load_row(run_dir, row):
    p = row_path(run_dir, row)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def write_json_atomic(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=str)
    os.replace(tmp, path)


def package_versions(names):
    from importlib import metadata
    out = {}
    for n in names:
        try:
            out[n] = metadata.version(n)
        except metadata.PackageNotFoundError:
            out[n] = None
    return out


def git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=HERE, capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def environment_info():
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "git_commit": git_commit(),
        "packages": package_versions(["anthropic", "openai", "google-genai", "vllm", "transformers", "torch"]),
    }


# ---------------------------------------------------------------- merge into Problems.csv

def _raise_field_limit():
    limit = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limit)
            return
        except OverflowError:
            limit //= 10


OUTPUT_SUFFIXES = ["reasoning", "ordering_reasoning", "top_practice", "top_practice_reasoning"]


def output_columns(prefix):
    return [f"{prefix}_{s}" for s in OUTPUT_SUFFIXES]


def merge_into_csv(run_dir, prefix, csv_path, backup_dir, replace_prefix=None):
    """Write the output columns for every row of the run that finished with status "ok".

    <prefix>_reasoning:              answer 1 reordered as answer 2 says (compact JSON; its practices_used
                                     order is the final ordering)
    <prefix>_ordering_reasoning:     answer 2, the order, as compact JSON (each step, and why this order)
    <prefix>_top_practice:           answer 3's top_practice
    <prefix>_top_practice_reasoning: answer 3's why
    (Logs of the two-prompt version have no answer 2 order: <prefix>_reasoning is answer 1 and
    <prefix>_ordering_reasoning stays empty.)

    replace_prefix: the columns <replace_prefix>_* are renamed to <prefix>_* in place (same position) and
    emptied first, so they hold only this run's values. Without it, rows not in the run keep whatever the
    columns already held, and new columns are added after the existing ones.

    Rows are matched by position (data row number), because some problem_ids repeat. The CSV is
    written with the same dialect as the original (minimal quoting, LF line endings, UTF-8).
    """
    _raise_field_limit()
    with open(csv_path, encoding="utf-8", newline="") as f:
        table = list(csv.reader(f))
    header, body = table[0], table[1:]
    width = len(header)
    for r in body:
        r.extend([""] * (width - len(r)))
    pid_col = header.index("problem_id")
    cols = output_columns(prefix)
    replaced = []
    if replace_prefix and replace_prefix != prefix:
        old = [f"{replace_prefix}_{s}" for s in OUTPUT_SUFFIXES if f"{replace_prefix}_{s}" in header]
        if old and any(c in header for c in cols):
            raise ValueError(f"{csv_path} has both {replace_prefix}_* and {prefix}_* columns; remove one set first")
        for j, name in enumerate(header):
            if name in old:
                header[j] = prefix + name[len(replace_prefix):]
                replaced.append(name)
        # (no old columns: an earlier merge already replaced them; the columns are still rewritten in full)
    for c in cols:
        if c not in header:
            # put a missing column right after the output column before it, if that one exists
            prev = [header.index(p) for p in cols[:cols.index(c)] if p in header]
            at = prev[-1] + 1 if prev else len(header)
            header.insert(at, c)
            for r in body:
                r.insert(at, "")
    idx = [header.index(c) for c in cols]
    if replace_prefix:
        for r in body:
            for j in idx:
                r[j] = ""

    rows_dir = os.path.join(run_dir, "rows")
    written, skipped = 0, 0
    for name in sorted(os.listdir(rows_dir)) if os.path.isdir(rows_dir) else []:
        if not name.endswith(".json"):
            continue
        with open(os.path.join(rows_dir, name), encoding="utf-8") as f:
            rec = json.load(f)
        final = rec.get("final") or {}
        if final.get("status") != "ok":
            skipped += 1
            continue
        i = rec["row"] - 1
        if str(body[i][pid_col]) != str(rec["problem_id"]):
            raise ValueError(f"row {rec['row']}: problem_id {body[i][pid_col]} in CSV, "
                             f"{rec['problem_id']} in the run log")
        if "answer3_json" in final:          # three prompts
            body[i][idx[0]] = json.dumps(final["combined_json"], ensure_ascii=False)
            body[i][idx[1]] = json.dumps(final["answer2_json"], ensure_ascii=False)
            top = final["answer3_json"]
        else:                                # two-prompt logs (e.g. qwen3_30b_v2)
            body[i][idx[0]] = json.dumps(final["answer1_json"], ensure_ascii=False)
            top = final["answer2_json"]
        body[i][idx[2]] = top["top_practice"]
        body[i][idx[3]] = top["why"]
        written += 1

    os.makedirs(backup_dir, exist_ok=True)
    backup = os.path.join(backup_dir, f"Problems.before_{prefix}.csv")
    with open(csv_path, "rb") as src, open(backup, "wb") as dst:
        dst.write(src.read())
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(csv_path), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        w.writerows(body)
    os.replace(tmp, csv_path)
    return {"written": written, "skipped_unfinished": skipped, "columns": cols, "backup": backup,
            "replaced": replaced}
