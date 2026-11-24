#!/usr/bin/env python3
"""
The "filtered" and "irt" conditions of kt_practice_benchmark.py.

filtered  practice + profile + lookup + filtered examples. The prompt has the student profile (kt_student_profile, kept
          by rules after every answer), the new problem's common wrong answers (kt_wrong_lookup), and, instead of the
          last 10 answers (profile) or the whole history (practice), only these previous problems of the student:
            1. matched examples: for every practice the new problem needs, the student's most recent RIGHT and most
               recent WRONG answer on a problem
                 - of the same skill that also needs that practice          (same skill + same practice)
                 - of the same skill that does not need it                  (same skill + other practice)
                 - of another skill that needs it                           (other skill + same practice)
                 - of a linked skill that needs it                          (linked skill + same practice)
               "linked": a prerequisite of the new problem's skill or a skill built on it (one edge in the skill graph,
               Code/maca_cd/data/graph); "another skill": neither the same nor linked. A problem shares the skill when
               one of its skills is one of the new problem's. Right = the first answer was correct (discrete_score 1).
               A new problem without practice labels: the most recent right and wrong answer of the same skill and of
               a linked skill.
            2. every problem of the current session: the run of answers less than SESSION_GAP_MINUTES apart that ends
               at the new problem.
          Each problem is shown once, oldest first, with why it was chosen, the practices it needs (with the reason
          for each) and its top practice, its difficulty and the analysis of the student's answer. Only the history
          the paper gives (the answers before the prediction's bin) is used, so nothing at or after the target is seen.
irt       filtered + the IRT difficulty and discrimination of the new problem and of every shown problem, each written
          out as a sentence (2PL fitted to the students outside the paper's 500: Code/tools/fit_irt.js ->
          Results/kt_profile/problem_irt.json).

Both use the common wrong answers (kt_practice_benchmark.DIAG_CSV) for the answer analyses and the lookup list.
"""

import json
import math
import os
from datetime import datetime

import kt_practice_benchmark as KP
import kt_student_profile as SP
import kt_wrong_lookup as WL

B = KP.B
IRT_PATH = os.path.join(KP.REPO_DIR, "Results", "kt_profile", "problem_irt.json")
SESSION_GAP_MINUTES = 60

# ---------------------------------------------------------------------------------------------- prompt text

SELECTION_TEXT = (
    "followed by selected previous problems of this student in full (not every previous problem):\n"
    "- Matched problems: for each practice the new problem needs, the student's most recent right answer and most "
    "recent wrong answer on a problem (1) of the same skill that also needs that practice, (2) of the same skill that "
    "does not need it, (3) of another skill that needs it, and (4) of a linked skill that needs it (linked: a "
    "prerequisite of the new problem's skill, or a skill built on it, in the skill graph).\n"
    f"- Every problem of the current session: the answers less than {SESSION_GAP_MINUTES} minutes apart that lead up "
    "to the new problem.\n"
    "Each selected problem says why it was chosen. The profile still counts all of the student's answers.\n"
)
FILTERED_SECTION = SP.PROFILE_SECTION.replace(
    f"followed by the student's {SP.RECENT_ITEMS} most recent problems in full.\n", SELECTION_TEXT).replace(
    "Use the profile, the recent problems, and", "Use the profile, the selected problems, and")
assert SELECTION_TEXT in FILTERED_SECTION and "the selected problems, and" in FILTERED_SECTION

IRT_SECTION = (
    "\n\n---\n\nItem Response Theory (IRT):\n\n"
    "The new problem and each selected problem also have IRT parameters, from a two-parameter logistic model fitted "
    "to the first answers of other students (not this student): P(right) = 1 / (1 + exp(-a * (ability - b))), with "
    "ability on a scale where the average other student is 0 and one standard deviation is 1. Difficulty b is the "
    "ability at which a student has a 50% chance of answering right; discrimination a is how sharply that chance "
    "rises with ability (high a: the problem separates stronger from weaker students well; low a: success depends "
    "little on ability). Each is also written out in words."
)

_RECENT_LINE = ("    - The student's most recent problems, each with: Timestamp, Problem, Problem Type, Options, Correct Answer, "
                "Student's First Answer, UsedHint, SawAnswer, Skill, the practices it requires, its difficulty, and an "
                "analysis of the student's answer.\n")
_NEW_LINE = ("    - The new problem (with optional answer choices), its skill, prerequisite skills, the practices it requires "
             "and its difficulty.\n")
assert _RECENT_LINE in SP.USER_INTRO and _NEW_LINE in SP.USER_INTRO


def user_intro(irt):
    extra = ", its IRT difficulty and discrimination" if irt else ""
    return SP.USER_INTRO.replace(_RECENT_LINE, (
        "    - Selected previous problems of this student (matched to the new problem by skill and practice, and every "
        "problem of the current session), each with: Timestamp, Problem, Problem Type, Options, Correct Answer, "
        "Student's First Answer, UsedHint, SawAnswer, Skill, the practices it requires (with the reason for each) and "
        f"its top practice, its difficulty{extra}, an analysis of the student's answer, and why it was selected.\n")).replace(
        _NEW_LINE, ("    - The new problem (with optional answer choices), its skill, prerequisite skills, the practices it "
                    f"requires, its difficulty{extra}, and its common wrong answers.\n"))


# ---------------------------------------------------------------------------------------------- IRT

def load_irt():
    if not os.path.exists(IRT_PATH):
        raise SystemExit(f"{IRT_PATH} is missing: run `node Code/tools/fit_irt.js` (on any machine) and commit it")
    with open(IRT_PATH, encoding="utf-8") as f:
        return {int(pid): (v[0], v[1]) for pid, v in json.load(f)["problems"].items()}


def _p(a, theta, b):
    return 1 / (1 + math.exp(-a * (theta - b)))


def _pct(x):
    return f"{round(100 * x)}%"


def _an(pct):
    """'an' before 8%, 11%, 18%, 80-89%; 'a' otherwise."""
    return "an" if pct.startswith("8") or pct in ("11%", "18%") else "a"


def difficulty_word(b):
    return ("very easy" if b <= -1.5 else "easy" if b <= -0.5 else "medium" if b < 0.5
            else "hard" if b < 1.5 else "very hard")


def discrimination_word(a):   # Baker (2001), The Basics of Item Response Theory
    return ("very low" if a < 0.35 else "low" if a < 0.65 else "moderate" if a < 1.35
            else "high" if a < 1.7 else "very high")


def irt_sentence(b, a):
    """The new problem's IRT parameters in words."""
    where = (f"{b:.2f} standard deviations above average" if b > 0.005 else
             f"{-b:.2f} standard deviations below average" if b < -0.005 else "about average")
    aw = discrimination_word(a)
    how = ("success depends little on ability, so it separates stronger from weaker students poorly"
           if aw in ("very low", "low") else
           "success depends moderately on ability" if aw == "moderate" else
           "success depends strongly on ability, so it separates stronger from weaker students well")
    avg, low, high = _pct(_p(a, 0, b)), _pct(_p(a, -1, b)), _pct(_p(a, 1, b))
    return (f"IRT difficulty b = {b:.2f} ({difficulty_word(b)}): a student of average ability has {_an(avg)} {avg} "
            f"chance of answering it right on the first try, and a 50% chance needs ability {where}. "
            f"IRT discrimination a = {a:.2f} ({aw}): {how}; a student one standard deviation below average has "
            f"{_an(low)} {low} chance and one standard deviation above average {_an(high)} {high} chance.")


def irt_short(b, a):
    """A selected problem's IRT parameters, in short."""
    return (f"IRT: {difficulty_word(b)} (b = {b:.2f}; a student of average ability {_pct(_p(a, 0, b))} right), "
            f"{discrimination_word(a)} discrimination (a = {a:.2f})")


# ---------------------------------------------------------------------------------------------- data

class FilteredData(SP.ProfileData):
    def __init__(self, kt_data_dir, irt=False):
        super().__init__(kt_data_dir, every_wrong=False)
        self.children = {}
        for child, parents in self.parents.items():
            for p in parents:
                self.children.setdefault(p, []).append(child)
        self.irt = load_irt() if irt else None

    def linked(self, codes):
        out = set()
        for c in codes:
            out.update(self.parents.get(c, []))
            out.update(self.children.get(c, []))
        return out - set(codes)

    def irt_text(self, pid, full):
        if pid not in self.irt:
            return "IRT: not estimated (too few other students answered it)"
        b, a = self.irt[pid]
        return irt_sentence(b, a) if full else irt_short(b, a)


# ---------------------------------------------------------------------------------------------- selection

def to_time(value):
    try:
        return datetime.strptime(str(value)[:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def session_start(records, n, target_time):
    """First index of the current session among records[:n]: walking back from the new problem, answers less than
    SESSION_GAP_MINUTES apart."""
    later = to_time(target_time)
    i = n - 1
    while i >= 0:
        t = to_time(records[i].get("end_time"))
        if t is None or later is None or (later - t).total_seconds() > SESSION_GAP_MINUTES * 60:
            break
        later = t
        i -= 1
    return i + 1


def select(d, records, n, target, target_time):
    """{history index: [reasons]} for the problems to show; only records[:n] (the paper's history) are read."""
    tpid = int(target["problem_id"])
    tskills = set(d.skills.get(tpid, []))
    linked = d.linked(tskills)
    tprac = list(dict.fromkeys(p for p, _ in d.info.practices.get(tpid, []))) or [None]
    reasons, taken = {}, set()
    for i in range(n - 1, -1, -1):           # newest first: the first found is the most recent
        rec = records[i]
        pid = int(rec["problem_id"])
        skills = set(d.skills.get(pid, []))
        rel = "same" if skills & tskills else "linked" if skills & linked else "other"
        prac = {p for p, _ in d.info.practices.get(pid, [])}
        right = d.info.classify(rec)[0] == "correct"
        for p in tprac:
            if p is None:                     # the new problem has no practice labels
                if rel == "other":
                    continue
                key, why = (rel, right), f"{rel} skill"
            elif rel == "same":
                key = ("same", p in prac, p, right)
                why = f"same skill, also needs {p}" if p in prac else f"same skill, does not need {p}"
            elif p in prac:
                key, why = (rel, p, right), f"{'linked skill' if rel == 'linked' else 'another skill'}, also needs {p}"
            else:
                continue
            if key in taken:
                continue
            taken.add(key)
            reasons.setdefault(i, []).append(f"{why} (most recent {'right' if right else 'wrong'} answer)")
    for i in range(session_start(records, n, target_time), n):
        reasons.setdefault(i, []).append("answered in the current session")
    assert all(0 <= i < n for i in reasons)
    return reasons


# ---------------------------------------------------------------------------------------------- the prompt

def example_text(d, h, rec, why):
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
    s += f"Skill: {d.skills_line(pid)}\n{d.info.block(pid)}\n{d.diff_text(pid)}\n"
    if d.irt is not None:
        s += d.irt_text(pid, full=False) + "\n"
    s += f"{d.info.analysis(rec)}\nWhy selected: {'; '.join(why)}.\n---\n\n"
    return s


def build_prompt(d, profile, student_history, records, new_problem, target, lookup):
    pid = int(target["problem_id"])
    n = len(student_history)
    p = user_intro(d.irt is not None) + "\n" + profile.render(target, SP.to_date(new_problem.get("timestamp"))) + "\n\n"
    picks = select(d, records, n, target, new_problem.get("timestamp"))
    in_session = sum(1 for why in picks.values() if "answered in the current session" in why)
    p += (f"**Selected Previous Problems ({len(picks)} of the student's {n} previous answers: matched problems and the "
          f"{in_session} problems of the current session; oldest first):**\n\n")
    if not picks:
        p += "None.\n\n"
    for i in sorted(picks):
        p += example_text(d, student_history[i], records[i], picks[i])
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
    if d.irt is not None:
        p += d.irt_text(pid, full=True) + "\n"
    p += lookup.text(pid, target.get("user_id")) + "\n"
    return p


# As kt_student_profile.install_profile: the paper's make_process_single_user and create_user_prompt are wrapped; the
# profile is advanced one answer at a time up to the history's end, so it never sees the target or anything later.
DATA = None
CURRENT_RECORDS = None
PROFILE = None
LOOKUP = None


def install_filtered(kt, kt_data_dir, irt=False):
    global DATA, LOOKUP
    DATA = FilteredData(kt_data_dir, irt)
    LOOKUP = WL.Lookup(kt, DATA.info)
    if getattr(kt, "_filtered_installed", False):
        return
    if getattr(kt, "_practice_installed", False) or getattr(kt, "_profile_installed", False):
        raise RuntimeError("the filtered condition cannot share a process with the practice or profile conditions")
    kt._filtered_installed = True
    original_make = kt.make_process_single_user

    def find_target(new_problem, start):
        for rec in CURRENT_RECORDS[start:]:
            if str(rec.get("end_time")) == str(new_problem.get("timestamp")) and rec.get("cleaned body") == new_problem.get("problem_text"):
                return rec
        raise RuntimeError(f"target problem not found in the student's records: {new_problem.get('timestamp')}")

    def create_filtered(student_history, new_problem, problem_df):
        global PROFILE
        n = len(student_history)
        if PROFILE is None or PROFILE.applied > n:
            PROFILE = SP.StudentProfile(DATA)
        for i in range(PROFILE.applied, n):
            if str(CURRENT_RECORDS[i].get("end_time")) != str(student_history[i].get("timestamp")):
                raise RuntimeError("history and records out of step")
            PROFILE.update(CURRENT_RECORDS[i])
        if PROFILE.applied != n:
            raise RuntimeError("profile and history out of step")
        target = find_target(new_problem, n)
        return build_prompt(DATA, PROFILE, student_history, CURRENT_RECORDS, new_problem, target, LOOKUP)

    def make_filtered(system_prompt):
        inner = original_make(system_prompt)

        def process(args):
            global CURRENT_RECORDS, PROFILE
            CURRENT_RECORDS, PROFILE = args[1], None
            return inner(args)
        return process

    kt.create_user_prompt = create_filtered
    kt.make_process_single_user = make_filtered
    kt.BASE_SYSTEM_PROMPT = kt.BASE_SYSTEM_PROMPT + FILTERED_SECTION + (IRT_SECTION if irt else "") + WL.LOOKUP_SECTION
