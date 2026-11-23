#!/usr/bin/env python3
"""
The "profile" condition of kt_practice_benchmark.py (deck: "Cognitive dimension for knowledge tracing", slides 28-31,
step 3 "the table in place of the history").

Instead of the full history, the LLM reads a student profile: a table of evidence that fixed rules update after every
answer (no LLM call builds or rewrites it), followed by the student's 10 most recent problems in full and the new
problem. The predictions are the paper's (same targets: 50 answers of history, then bins of 10, the first correct and
first incorrect answer of each bin; same prediction ids, same JSON output), so the results compare directly with the
baseline and practice runs.

What the rules keep, per student (StudentProfile.update, one call per answer, in time order):
  overall      answers, right, last 20 results, accuracy against problem difficulty
  habits       hints / answer views; wrong answers split into diagnosed common / uncommon / after help;
               slips on easy problems; right answers on hard problems
  by practice  problems needing each practice and right; problems where it is the top practice and right;
               failed steps of diagnosed wrong answers (practice error / math fact)
  by skill     answers, right, last answered, last 5 results, answers by top practice, failed steps with the most
               recent reasons, uncommon / after-help / guess counts, hardest problem solved without help
The prompt shows the new problem's skill(s) in detail, their prerequisites (skill graph) in short, and one line for
every other skill.

Sources: practices and top practice from Problems.csv qwen35_122b_noex_* and the diagnoses of common wrong answers
(wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv), both through kt_practice_benchmark.PracticeInfo; skills from
Data/Skills.csv; skill graph from Code/maca_cd/data/graph (DAG_edges.json: [a, b] = a is a prerequisite of b);
difficulty = share of students right on their first answer, from Data/Interactions.csv without the paper's 500
students (so no test student's answers are used), cached in Results/kt_profile/problem_difficulty.json.
The new problem's own common wrong answers are not shown (no lookup list).
"""

import csv
import json
import os
from collections import deque
from datetime import date

import kt_practice_benchmark as KP

B = KP.B
PRACTICES = ["Representing", "Abstracting and Generalizing", "Justifying and Proving", "Mathematical Modeling",
             "Collaborative Mathematics", "Procedural Fluency"]
GRAPH_DIR = os.path.join(KP.CODE_DIR, "maca_cd", "data", "graph")
DIFF_PATH = os.path.join(KP.REPO_DIR, "Results", "kt_profile", "problem_difficulty.json")
MIN_DIFF_STUDENTS = 10      # fewer other students than this: difficulty unknown
EASY, HARD = 0.8, 0.4       # share of other students right
RECENT_ITEMS = 10
NO_SKILL = "(no skill tag)"

# ---------------------------------------------------------------------------------------------- prompt text

PROFILE_SECTION = (
    "\n\n---\n\nStudent Profile and Mathematical Practices:\n\n"
    "Instead of the student's full history, you receive a Student Profile: a table of evidence kept by fixed rules "
    "and updated after every answer the student gave (every count is a count of the student's real answers), "
    f"followed by the student's {RECENT_ITEMS} most recent problems in full.\n"
    "- \"Right\" means the student's first answer was correct without a hint and without seeing the answer.\n"
    "- Difficulty is the share of other students (not this student) who answered the problem right on their first "
    "try.\n"
    "- Every problem is labeled with the mathematical practices a student needs to solve it, in order, and its top "
    "practice (the step where the problem's difficulty lies). \"By top practice\" counts the student's answers by "
    "the top practice of each problem.\n"
    "- A \"failed step\" comes from the diagnosis of a common wrong answer (one that several students gave): the "
    "practice step that went wrong, as a practice error or as a wrong or missing math fact. Uncommon wrong answers "
    "and answers given after a hint or after seeing the answer have no diagnosis.\n"
    "- The skill graph links a skill to the skills it builds on (its prerequisites). When the student has not yet "
    "answered the new problem's skill, use the prerequisites and the record by practice.\n"
    "Use the profile, the recent problems, and the new problem's skill, practices and difficulty to predict how the "
    "student will do. The six practices, with their definitions and descriptors:\n"
    + KP.PRACTICE_DEFINITIONS
)

# The paper's task description (kt_inference_base.create_user_prompt), with "Provided Data" describing the profile
USER_INTRO = """Task Description:

Your task is to model a single student's learning process and predict how they will respond to a new mathematics problem based on their prior work.

You will produce three coordinated predictions:

    1) **Skill-level knowledge tracing (0 or 1):** Predict whether this student has mastered the underlying skill involved in the new problem.
    2) **Question-level knowledge tracing (0 or 1):** Predict whether this student will answer this specific problem correctly.
    3) **Cognitive-level prediction (string):** Generate the exact answer the student would most likely produce.
       - For Multiple Choice (select 1): Predict a single letter (e.g., "A" or "B")
       - For Multiple Choice (select all): Predict comma-separated letters (e.g., "A, C" or "B, D")
       - For Fill-in problems: Predict the exact text the student would write
    ---

    Provided Data:

    You will receive:
    - A Student Profile built from all of this student's previous answers: counts by skill and by practice, the failed steps of their diagnosed wrong answers, habits, the hardest problem solved on each skill, and the skills the new problem's skill builds on.
    - The student's most recent problems, each with: Timestamp, Problem, Problem Type, Options, Correct Answer, Student's First Answer, UsedHint, SawAnswer, Skill, the practices it requires, its difficulty, and an analysis of the student's answer.
    - The new problem (with optional answer choices), its skill, prerequisite skills, the practices it requires and its difficulty.

    # About the context flags:
    - **UsedHint = True** → The student viewed or used a hint while solving this problem.
    - **SawAnswer = True** → The student saw the correct answer before or during the attempt.
    When either of these flags is True, treat the corresponding response as *less reliable evidence of mastery* — it indicates that the student has not fully learned the concept and required help solving the problem.
"""


def short(text, n):
    text = KP.one_line(text)
    return text if len(text) <= n else text[:n - 1].rstrip() + "…"


def to_date(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def right_of(right, n):
    return f"{right} of {n} right ({round(100 * right / n)}%)" if n else "no answers"


# ---------------------------------------------------------------------------------------------- data

def load_skills():
    """problem_id -> its skill codes (in file order), and code -> skill name."""
    by_pid, names = {}, {}
    with open(os.path.join(B.DATA_DIR, "Skills.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                pid = int(r["problem_id"])
            except (KeyError, ValueError, TypeError):
                continue
            code = (r.get("node_code") or "").strip()
            if not code:
                continue
            names.setdefault(code, KP.one_line(r.get("node_name")))
            codes = by_pid.setdefault(pid, [])
            if code not in codes:
                codes.append(code)
    return by_pid, names


def load_graph():
    """code -> its direct prerequisites (codes), and the set of codes in the graph."""
    with open(os.path.join(GRAPH_DIR, "concept_data.json"), encoding="utf-8") as f:
        code2id = json.load(f)["code2id"]
    id2code = {int(i): c for c, i in code2id.items()}
    with open(os.path.join(GRAPH_DIR, "DAG_edges.json"), encoding="utf-8") as f:
        edges = json.load(f)["DAG"]
    parents = {}
    for a, b in edges:
        a, b = id2code.get(int(a)), id2code.get(int(b))
        if a and b and a not in parents.setdefault(b, []):
            parents[b].append(a)
    return parents, set(code2id)


def load_difficulty():
    """problem_id -> (right, answers) over the students outside the paper's 500 (first answers, each interaction
    once). Computed once and cached."""
    if os.path.exists(DIFF_PATH):
        with open(DIFF_PATH, encoding="utf-8") as f:
            return {int(pid): tuple(v) for pid, v in json.load(f)["problems"].items()}
    import pandas as pd
    paper_ids = os.path.join(B.PAPER_REF_DIR, "paper_user_ids.txt")
    if not os.path.exists(paper_ids):
        raise SystemExit(f"{paper_ids} is missing: run `pick-users` first")
    paper = set(B.read_user_ids(paper_ids))
    print(f"Computing problem difficulty from Data/Interactions.csv without the paper's {len(paper)} students ...")
    df = pd.read_csv(os.path.join(B.DATA_DIR, "Interactions.csv"), usecols=["id", "problem_id", "user_id", "discrete_score"])
    df = df.drop_duplicates("id")
    df = df[~df["user_id"].isin(paper)]
    df["right"] = (df["discrete_score"] >= 1).astype(int)
    g = df.groupby("problem_id")["right"].agg(["sum", "count"])
    problems = {int(pid): (int(s), int(n)) for pid, s, n in zip(g.index, g["sum"], g["count"])}
    os.makedirs(os.path.dirname(DIFF_PATH), exist_ok=True)
    with open(DIFF_PATH, "w", encoding="utf-8") as f:
        json.dump({"meta": {"students": int(df["user_id"].nunique()), "answers": int(len(df)),
                            "excluded": "the paper's 500 students (Results/paper_reference/paper_user_ids.txt)"},
                   "problems": {str(k): list(v) for k, v in sorted(problems.items())}}, f)
    print(f"  {len(problems):,} problems, {len(df):,} answers from {df['user_id'].nunique():,} students: {DIFF_PATH}")
    return problems


class ProfileData:
    """Everything the profiles and prompts read, loaded once."""

    def __init__(self, kt_data_dir):
        self.info = KP.PracticeInfo(kt_data_dir)
        self.skills, self.names = load_skills()
        self.parents, self.in_graph = load_graph()
        self.diff = load_difficulty()

    def difficulty(self, pid):
        right, n = self.diff.get(pid, (0, 0))
        return right / n if n >= MIN_DIFF_STUDENTS else None

    def diff_text(self, pid):
        right, n = self.diff.get(pid, (0, 0))
        if n < MIN_DIFF_STUDENTS:
            return "Difficulty: unknown (too few other students answered it)"
        return f"Difficulty: {round(100 * right / n)}% of other students answered it right on the first try ({n:,} students)"

    def label(self, code):
        return "Problems with no skill tag" if code == NO_SKILL else f"{code} {self.names.get(code, '')}".strip()

    def skills_line(self, pid):
        codes = self.skills.get(pid)
        return "; ".join(self.label(c) for c in codes) if codes else "Undefined"

    def prerequisites(self, pid):
        codes = self.skills.get(pid, [])
        out = []
        for c in codes:
            for p in self.parents.get(c, []):
                if p not in codes and p not in out:
                    out.append(p)
        return out


# ---------------------------------------------------------------------------------------------- the profile

class SkillState:
    def __init__(self):
        self.n = self.right = 0
        self.last = None
        self.results = deque(maxlen=5)
        self.by_top = {}        # practice -> [answers, right]
        self.fails = {}         # practice -> {"practice": n, "math_fact": n, "recent": the last 3 reasons}
        self.uncommon = self.help_wrong = self.guess = 0
        self.best = None        # (difficulty, date, problem text) of the hardest problem solved without help


class StudentProfile:
    """One student's table of evidence. update() applies one answer; render() writes the profile text."""

    def __init__(self, data):
        self.d = data
        self.applied = 0
        self.n = self.right = self.help = 0
        self.first = self.last = None
        self.results = deque(maxlen=20)
        self.wrong = {"common": 0, "uncommon": 0, "help": 0}
        self.diff_n = self.diff_right = 0
        self.diff_sum = 0.0
        self.easy = [0, 0]      # answers, wrong
        self.hard = [0, 0]      # answers, right
        self.practice = {}
        self.skills = {}

    def _prow(self, p):
        return self.practice.setdefault(p, {"need": 0, "need_right": 0, "top": 0, "top_right": 0,
                                            "fail_practice": 0, "fail_fact": 0})

    def update(self, rec):
        info = self.d.info
        pid = int(rec["problem_id"])
        day = to_date(rec.get("end_time"))
        kind, dg = info.classify(rec)
        right = kind == "correct"
        helped = KP.used_help(rec)
        self.applied += 1
        self.n += 1
        self.right += right
        self.results.append(right)
        self.first = self.first or day
        self.last = day or self.last
        self.help += helped
        if not right:
            self.wrong[kind] += 1
        diff = self.d.difficulty(pid)
        if diff is not None:
            self.diff_n += 1
            self.diff_right += right
            self.diff_sum += diff
            if diff >= EASY:
                self.easy[0] += 1
                self.easy[1] += not right
            if diff <= HARD:
                self.hard[0] += 1
                self.hard[1] += right
        top = info.top.get(pid) or None
        for p in dict.fromkeys(p for p, _ in info.practices.get(pid, [])):
            row = self._prow(p)
            row["need"] += 1
            row["need_right"] += right
        if top:
            row = self._prow(top)
            row["top"] += 1
            row["top_right"] += right
        fail = None
        if kind == "common":
            et, fp = dg["error_type"], (dg["failed_practice"] or "").strip()
            if et in ("practice", "math_fact") and fp:
                what = f"math fact: {KP.one_line(dg['math_fact'])}" if et == "math_fact" else KP.one_line(dg["reconstruction"])
                fail = (fp, et, f"answered \"{short(dg['wrong_answer'], 40)}\": {short(what, 160)}")
                self._prow(fp)["fail_practice" if et == "practice" else "fail_fact"] += 1
        for code in self.d.skills.get(pid) or [NO_SKILL]:
            s = self.skills.setdefault(code, SkillState())
            s.n += 1
            s.right += right
            s.last = day or s.last
            s.results.append(right)
            if top:
                t = s.by_top.setdefault(top, [0, 0])
                t[0] += 1
                t[1] += right
            if fail:
                f = s.fails.setdefault(fail[0], {"practice": 0, "math_fact": 0, "recent": deque(maxlen=3)})
                f[fail[1]] += 1
                f["recent"].append(fail[2])
            elif kind == "common":
                s.guess += 1
            s.uncommon += kind == "uncommon"
            s.help_wrong += kind == "help"
            if right and not helped and diff is not None and (s.best is None or diff <= s.best[0]):
                s.best = (diff, day, short(rec.get("cleaned body"), 220))

    # ------------------------------------------------------------------ render
    def _ago(self, day, target_day):
        if day is None:
            return ""
        if target_day is None:
            return f"; last answered {day}"
        return f"; last answered {day} ({(target_day - day).days} days before the new problem)"

    def skill_lines(self, code, target_day, detail):
        s = self.skills.get(code)
        head = f"- {self.d.label(code)}"
        if s is None:
            return [f"{head}: not answered yet."]
        out = [f"{head}: {right_of(s.right, s.n)}{self._ago(s.last, target_day)}."]
        if detail:
            out.append(f"  Last {len(s.results)} results on this skill, oldest first: "
                       + ", ".join("right" if r else "wrong" for r in s.results) + ".")
        if s.by_top:
            out.append("  By top practice: " + "; ".join(
                f"{p} {r} of {n} right" for p, (n, r) in sorted(s.by_top.items(), key=lambda kv: -kv[1][0])) + ".")
        if s.fails:
            parts = []
            for p, f in sorted(s.fails.items(), key=lambda kv: -(kv[1]["practice"] + kv[1]["math_fact"])):
                part = f"{p} {f['practice'] + f['math_fact']} times ({f['practice']} practice errors, {f['math_fact']} math facts)"
                if detail and f["recent"]:
                    part += "; most recent first: " + " | ".join(reversed(f["recent"]))
                parts.append(part)
            out.append("  Failed steps in its diagnosed wrong answers: " + "; ".join(parts) + ".")
        elif s.right < s.n:
            out.append("  No diagnosed failed step.")
        other = [f"{v} {name}" for v, name in ((s.uncommon, "uncommon answers (no diagnosis)"),
                                               (s.help_wrong, "after a hint or seeing the answer"),
                                               (s.guess, "guesses (no reasonable process)")) if v]
        if other:
            out.append("  Other wrong answers: " + ", ".join(other) + ".")
        if s.best:
            diff, day, text = s.best
            if detail:
                out.append(f"  Hardest problem solved without help: \"{text}\" ({round(100 * diff)}% of other students "
                           f"right), on {day}.")
            else:
                out.append(f"  Hardest problem solved without help: one that {round(100 * diff)}% of other students get right.")
        return out

    def render(self, target_rec, target_day):
        d = self.d
        pid = int(target_rec["problem_id"])
        tcodes = d.skills.get(pid, [])
        L = [f"**Student Profile** (kept by rules from all {self.n} of this student's previous answers)", ""]
        L.append(f"Overall: {self.n} answers from {self.first} to {self.last}, {right_of(self.right, self.n)}. "
                 f"Last {len(self.results)} answers: {sum(self.results)} right.")
        if self.diff_n:
            L.append(f"Against difficulty: on the {self.diff_n} problems with a known difficulty, this student got "
                     f"{round(100 * self.diff_right / self.diff_n)}% right; other students got the same problems right "
                     f"{round(100 * self.diff_sum / self.diff_n)}% of the time on average.")
        wrong = self.n - self.right
        L += ["", "Habits:",
              f"- Asked for a hint or saw the answer on {self.help} of {self.n} answers ({round(100 * self.help / self.n)}%).",
              f"- Wrong first answers: {wrong}. Of these, {self.wrong['common']} are common wrong answers with a "
              f"diagnosis, {self.wrong['uncommon']} are uncommon answers (no diagnosis), {self.wrong['help']} came "
              f"after a hint or seeing the answer."]
        if self.easy[0]:
            L.append(f"- Easy problems ({round(100 * EASY)}% or more of other students right): {self.easy[1]} wrong of "
                     f"{self.easy[0]} (slips).")
        if self.hard[0]:
            L.append(f"- Hard problems ({round(100 * HARD)}% or fewer of other students right): {self.hard[1]} right of "
                     f"{self.hard[0]}.")
        L += ["", "By practice, over all skills:", "",
              "| Practice | Problems needing it: right / answers | Problems where it is the top practice: right / answers "
              "| Failed step in diagnosed wrong answers: practice errors / math facts |",
              "|---|---|---|---|"]
        for p in PRACTICES + sorted(set(self.practice) - set(PRACTICES)):
            r = self.practice.get(p)
            if r and (r["need"] or r["top"] or r["fail_practice"] or r["fail_fact"]):
                L.append(f"| {p} | {r['need_right']} / {r['need']} | {r['top_right']} / {r['top']} | "
                         f"{r['fail_practice']} / {r['fail_fact']} |")
        L += ["", "Skill of the new problem:" if len(tcodes) <= 1 else "Skills of the new problem:"]
        if not tcodes:
            L.append("- The new problem has no skill tag.")
        for c in tcodes:
            L += self.skill_lines(c, target_day, detail=True)
        L += ["", "Prerequisite skills (from the skill graph: skills the new problem's skill builds on):"]
        prereq = d.prerequisites(pid)
        for c in tcodes:
            if c not in d.in_graph:
                L.append(f"- {c} is not in the skill graph.")
            elif not d.parents.get(c):
                L.append(f"- {c} has no prerequisite in the skill graph.")
        for c in prereq:
            L += self.skill_lines(c, target_day, detail=False)
        others = [c for c in self.skills if c not in tcodes and c not in prereq]
        if others:
            L += ["", "Other skills this student has answered:"]
            for c in sorted(others, key=lambda c: -self.skills[c].n):
                s = self.skills[c]
                L.append(f"- {d.label(c)}: {right_of(s.right, s.n)}{self._ago(s.last, None)}.")
        return "\n".join(L)


# ---------------------------------------------------------------------------------------------- the prompt

def item_text(d, h, rec):
    """One recent problem: the paper's fields, then its skill, practices, difficulty and the answer analysis."""
    pid = int(rec["problem_id"])
    s = f"Timestamp: {h['timestamp']}\n"
    s += f"Problem: {h['problem_text']}\n"
    s += f"Problem Type: {h['problem_type']}\n"
    if h.get("answer_options_formatted"):
        s += f"Options:\n{h['answer_options_formatted']}\n"
    s += f"Correct Answer: {h['correct_answer']}\n"
    s += f"Student's First Answer: {h['student_answer']}\n"
    s += f"UsedHint: {h['used_hint']}\n"
    s += f"SawAnswer: {h['saw_answer']}\n"
    s += f"Skill: {d.skills_line(pid)}\n{d.info.required(pid)}\n{d.diff_text(pid)}\n{d.info.analysis(rec)}\n---\n\n"
    return s


def build_prompt(d, profile, student_history, records, new_problem, target, lookup=None):
    pid = int(target["problem_id"])
    p = USER_INTRO + "\n" + profile.render(target, to_date(new_problem.get("timestamp"))) + "\n\n"
    start = max(0, len(student_history) - RECENT_ITEMS)
    p += f"**Student's {len(student_history) - start} Most Recent Problems (oldest first):**\n\n"
    for i in range(start, len(student_history)):
        p += item_text(d, student_history[i], records[i])
    prereq = d.prerequisites(pid)
    p += "**New Problem to Predict:**\n\n"
    p += f"Timestamp: {new_problem['timestamp']}\n"
    p += f"Problem: {new_problem['problem_text']}\n"
    p += f"Problem Type: {new_problem['problem_type']}\n"
    if new_problem.get("answer_options_formatted"):
        p += f"Answer Options:\n{new_problem['answer_options_formatted']}\n"
    p += f"Correct Answer: {new_problem['correct_answer']}\n"
    p += f"Skill: {d.skills_line(pid)}\n"
    p += "Prerequisite skills: " + ("; ".join(d.label(c) for c in prereq) if prereq else "none in the skill graph") + "\n"
    p += f"{d.info.required(pid)}\n{d.diff_text(pid)}\n"
    if lookup is not None:
        p += lookup.text(pid) + "\n"
    return p


# The paper's make_process_single_user builds each student's prompts with a growing history and calls the module-level
# create_user_prompt; both are wrapped (as kt_practice_benchmark.install_practice does). The profile is advanced one
# answer at a time up to the history's end, so it never sees the target or anything later.
DATA = None
CURRENT_RECORDS = None
PROFILE = None
LOOKUP = None   # kt_wrong_lookup.Lookup when the condition has the common-wrong-answer lookup table


def install_profile(kt, kt_data_dir, lookup=False):
    global DATA, LOOKUP
    DATA = ProfileData(kt_data_dir)
    LOOKUP = None
    if lookup:
        import kt_wrong_lookup as WL
        LOOKUP = WL.Lookup(kt, DATA.info)
    if getattr(kt, "_profile_installed", False):
        return
    if getattr(kt, "_practice_installed", False):
        raise RuntimeError("the practice and profile conditions cannot be installed in one process")
    kt._profile_installed = True
    original_make = kt.make_process_single_user

    def find_target(new_problem, start):
        for rec in CURRENT_RECORDS[start:]:
            if str(rec.get("end_time")) == str(new_problem.get("timestamp")) and rec.get("cleaned body") == new_problem.get("problem_text"):
                return rec
        raise RuntimeError(f"target problem not found in the student's records: {new_problem.get('timestamp')}")

    def create_with_profile(student_history, new_problem, problem_df):
        global PROFILE
        n = len(student_history)
        if PROFILE is None or PROFILE.applied > n:
            PROFILE = StudentProfile(DATA)
        for i in range(PROFILE.applied, n):
            if str(CURRENT_RECORDS[i].get("end_time")) != str(student_history[i].get("timestamp")):
                raise RuntimeError("history and records out of step")
            PROFILE.update(CURRENT_RECORDS[i])
        if PROFILE.applied != n:
            raise RuntimeError("profile and history out of step")
        target = find_target(new_problem, n)
        return build_prompt(DATA, PROFILE, student_history, CURRENT_RECORDS, new_problem, target, LOOKUP)

    def make_with_profile(system_prompt):
        inner = original_make(system_prompt)

        def process(args):
            global CURRENT_RECORDS, PROFILE
            CURRENT_RECORDS, PROFILE = args[1], None
            return inner(args)
        return process

    kt.create_user_prompt = create_with_profile
    kt.make_process_single_user = make_with_profile
    kt.BASE_SYSTEM_PROMPT = kt.BASE_SYSTEM_PROMPT + PROFILE_SECTION
    if lookup:
        import kt_wrong_lookup as WL
        kt.BASE_SYSTEM_PROMPT += WL.LOOKUP_SECTION
