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
"""

import csv
import os
import random

import kt_practice_benchmark as KP

B = KP.B
SEED = 2026

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


class Lookup:
    """The lookup text for a problem: its diagnosed wrong answers, shuffled, MC as letters, without counts."""

    def __init__(self, kt, info):
        self.kt, self.info = kt, info
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

    def text(self, pid):
        rows = self.by_pid.get(pid)
        if not rows:
            return "Common wrong answers to this problem: none diagnosed."
        lines = ["Common wrong answers to this problem (in no particular order):"]
        lines += [f"  - {self.shown(pid, d['wrong_answer'])}. {self.diagnosis(d)}" for d in rows]
        return "\n".join(lines)
