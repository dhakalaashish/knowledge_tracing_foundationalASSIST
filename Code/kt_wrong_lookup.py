#!/usr/bin/env python3
"""
The common-wrong-answer lookup table for kt_practice_benchmark.py (deck idea 2: "the prediction is a choice from a
short list"): the problem to predict also lists its common wrong answers, each with its diagnosis (the step that went
wrong and how students most likely got it). If the model predicts a wrong answer, it chooses the listed one that best
fits the student (or writes another when none fits); the output format and the scoring stay the paper's.

The list: every wrong answer to the problem that has a diagnosis in the Chapter 3 diagnosis file
(kt_practice_benchmark.DIAG_CSV: first tries without help, given by 3 or more students, counted over all students).
No counts or shares are shown, so the model is not pushed toward the most frequent answer, and the order is shuffled
(the same order for a problem every time: seeded by its id), so it carries no frequency either. Multiple-choice
answers are shown as their letters, with the option text.

The "_all" conditions (every_wrong): every wrong answer given by 1 or more students, diagnosed the same way
(kt_practice_benchmark.DIAG_CSV_ALL, run_gb300.sh step 9). An answer given by exactly one student is left out of
the list when that student is the one being predicted: it is only there because of the answer being predicted
(Results/practice_analysis/all_wrong_answers.csv, column only_student). The student's past answers keep theirs.
"""

import csv
import os
import random
import re

import kt_practice_benchmark as KP

B = KP.B
SEED = 2026
ALL_WRONG_CSV = os.path.join(KP.REPO_DIR, "Results", "practice_analysis", "all_wrong_answers.csv")

LOOKUP_SECTION = (
    "\n\n---\n\nCommon Wrong Answers:\n\n"
    "The new problem also lists its common wrong answers: wrong answers that several students in the dataset gave on "
    "their first try without help, in no particular order, each with a diagnosis of the step that went wrong and how "
    "students most likely got it. The list describes students in general, not this student, so it says nothing by "
    "itself about whether this student will answer correctly. If you predict that this student will answer "
    "incorrectly (question_level 0), choose as student_answer the listed wrong answer that best fits this student "
    "(their failed practices and math facts, their past wrong answers and their habits), written exactly as listed "
    "(for multiple choice, the letter or letters); write a different wrong answer only if none of the listed ones "
    "fits this student."
)
LOOKUP_SECTION_ALL = LOOKUP_SECTION.replace(
    "lists its common wrong answers: wrong answers that several students in the dataset gave on their first try "
    "without help",
    "lists its wrong answers: every wrong answer that other students in the dataset gave on their first try without "
    "help, however rare").replace("Common Wrong Answers:", "Wrong Answers:")
assert "however rare" in LOOKUP_SECTION_ALL


class Lookup:
    """The lookup text for a problem: its diagnosed wrong answers, shuffled, MC as letters, without counts."""

    def __init__(self, kt, info, every_wrong=False):
        self.kt, self.info, self.every_wrong = kt, info, every_wrong
        self.only = {}   # (problem_id, rank) -> the one student who gave that wrong answer
        if every_wrong:
            with open(ALL_WRONG_CSV, newline="", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    if r.get("only_student"):
                        self.only[(int(r["problem_id"]), int(r["rank"]))] = r["only_student"].strip()
        self.by_pid = {}
        for (pid, _key), d in info.diag.items():
            self.by_pid.setdefault(pid, []).append(d)
        for pid, rows in self.by_pid.items():
            rows.sort(key=lambda d: int(d.get("rank") or 0))         # a fixed start, then a seeded shuffle
            random.Random(f"{SEED}-{pid}").shuffle(rows)
        self.options = {}
        B.csv.field_size_limit(10 ** 9)
        seen = set()
        with open(os.path.join(B.DATA_DIR, "Problems.csv"), newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                pid = int(r["problem_id"])
                if pid in seen:
                    continue
                seen.add(pid)
                if (r.get("Problem Type") or "") in B.MC_TYPES:
                    self.options[pid] = kt.label_answer_options(r.get("Multiple Choice Options") or "") or {}

    def shown(self, pid, text):
        """The answer as the student would write it in the paper's format. The diagnosis file has MC answers as the
        option text in lower case (several options joined by ' , '): matched to the options without case."""
        opts = self.options.get(pid)
        if not opts:
            return f"\"{text}\""
        norm_opts = {letter: KP.norm_answer(t) for letter, t in opts.items()}
        letters = []
        for part in (p.strip() for p in str(text).split(" , ")):
            hit = next((l for l, t in norm_opts.items() if t == KP.norm_answer(part)), None)
            if hit is None:
                hit = next((l for l, t in norm_opts.items() if part and (part in t or t in part)), None)
            if hit is None:
                return f"\"{text}\""          # an option not found: show the text
            letters.append(hit)
        letters = sorted(set(letters))
        texts = "; ".join(KP.one_line(opts[l])[:80] for l in letters)
        return f"\"{', '.join(letters)}\" (option text: {texts})"

    @staticmethod
    def diagnosis(d):
        et, fp, fact = d["error_type"], d["failed_practice"], KP.one_line(d["math_fact"])
        if et == "practice":
            what = f"the {fp} step went wrong"
        elif et == "math_fact":
            what = f"a wrong or missing math fact at the {fp} step: {fact.rstrip('.')}"
        else:
            what = "no reasonable process gives this answer (a guess)"
        return f"Error: {what}. How students most likely got it: {KP.one_line(d['reconstruction'])[:220]}"

    def listed(self, pid, user=None):
        """The diagnosed wrong answers the list shows for a problem (rows of the diagnosis file)."""
        rows = self.by_pid.get(pid) or []
        if self.every_wrong and user is not None:
            rows = [d for d in rows if self.only.get((pid, int(d["rank"]))) != str(user)]
        return rows

    def text(self, pid, user=None):
        rows = self.listed(pid, user)   # _all: not an answer only this student gave
        if not rows:
            return ("Wrong answers to this problem: none diagnosed." if self.every_wrong
                    else "Common wrong answers to this problem: none diagnosed.")
        lines = ["Wrong answers other students gave to this problem (in no particular order):" if self.every_wrong
                 else "Common wrong answers to this problem (in no particular order):"]
        lines += [f"  - {self.shown(pid, d['wrong_answer'])}. {self.diagnosis(d)}" for d in rows]
        return "\n".join(lines)


# ---------------------------------------------------------------------------------------------- evaluation
# Is a student's wrong answer (or a predicted one) one of a problem's common wrong answers? Needs no staged data and
# no model: the diagnosis file and Problems.csv only. Multiple-choice answers are compared as sets of letters (the
# results hold letters, or the option text as the student entered it; the diagnosis file holds the option text in
# lower case, several options joined by " , "); fill-in answers by their normalized text (as kt_practice_benchmark).

class ListedAnswers:
    def __init__(self, diag_csv=None):
        diag_csv = diag_csv or KP.DIAG_CSV
        B.csv.field_size_limit(10 ** 9)
        self.options = {}   # MC problem id -> {letter: option text}
        seen = set()
        with open(os.path.join(B.DATA_DIR, "Problems.csv"), newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                pid = int(r["problem_id"])
                if pid in seen:
                    continue
                seen.add(pid)
                if (r.get("Problem Type") or "") in B.MC_TYPES and (r.get("Multiple Choice Options") or "").strip():
                    opts = [o.strip() for o in r["Multiple Choice Options"].split("||")]
                    self.options[pid] = {"ABCDEFGHIJ"[i]: o for i, o in enumerate(opts[:10])}
        self.listed = {}    # problem id -> set of canonical answers
        with open(diag_csv, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                pid = int(r["problem_id"])
                self.listed.setdefault(pid, set()).add(self.canon(pid, r["wrong_answer"]))

    @staticmethod
    def _clean(text):
        """kt_inference_base.clean_html_and_normalize, without case (the diagnosis file is in lower case)."""
        text = re.sub(r"<[^>]+>", "", str(text))
        text = " ".join(text.split())
        return re.sub(r"\s*:\s*", ":", text).strip().lower()

    def canon(self, pid, answer):
        """MC: the letters the paper's match_student_answer_to_letters gives (each part matched to an option exactly,
        else by substring; the matched letters, or the text when none matches), so an answer compares the way the
        paper scores it; otherwise, and for fill-in, the normalized text."""
        a = str(answer if answer is not None else "").strip()
        opts = self.options.get(pid)
        if opts:
            if re.fullmatch(r"[A-J](\s*,\s*[A-J])*", a):
                return frozenset(re.findall(r"[A-J]", a))
            norm = {l: self._clean(t) for l, t in opts.items()}
            letters = set()
            for part in (p.strip() for p in a.split(" , ")):
                s = self._clean(part)
                hit = next((l for l, t in norm.items() if t == s), None)
                if hit is None:
                    hit = next((l for l, t in norm.items() if s in t or t in s), None)
                if hit is not None:
                    letters.add(hit)
            if letters:
                return frozenset(letters)
        return KP.answer_key(KP.norm_answer(a))

    def is_listed(self, pid, answer):
        try:
            pid = int(float(pid))
        except (TypeError, ValueError):
            return False
        return pid in self.listed and self.canon(pid, answer) in self.listed[pid]
