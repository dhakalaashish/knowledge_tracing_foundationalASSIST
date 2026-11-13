"""Check the answer checker's handling of the order prompt (prompt 2), without any model.

    python3 tools/test_single_order.py        (from Code/generate_practice_reasoning; prints OK or fails)

One practice in answer 1: prompt 2 is skipped and answer 2 is filled in ("auto": true), so prompt 3 can follow.
Two practices: prompt 2 is still needed. --order-single-practice behaviour (skip_single_order=False): never skipped.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import common          # noqa: E402
import prompts as P    # noqa: E402


def answer1(used):
    return {"practices_used": [{"order": i, "practice": p, "why": f"why {p}", "likely_errors": f"errors {p}"}
                               for i, p in enumerate(used, 1)],
            "practices_not_used": [{"practice": p, "why": "not needed"} for p in P.PRACTICES if p not in used]}


# one practice: answer 2 filled in, the combined analysis ready for prompt 3
ck = common.AnswerChecker()
assert ck.check(1, json.dumps(answer1(["Representing"]))) is None
assert ck.order_skipped and len(ck.parsed) == 2 and ck.parsed[1]["auto"] is True
assert [it["practice"] for it in ck.combined["practices_used"]] == ["Representing"]
assert ck.check(3, json.dumps({"top_practice": "Representing", "why": "the only step"})) is None
assert len(ck.parsed) == 3

# two practices: prompt 2 still asked
ck2 = common.AnswerChecker()
assert ck2.check(1, json.dumps(answer1(["Representing", "Procedural Fluency"]))) is None
assert not ck2.order_skipped and len(ck2.parsed) == 1 and ck2.combined is None

# old behaviour on request
ck3 = common.AnswerChecker(skip_single_order=False)
assert ck3.check(1, json.dumps(answer1(["Procedural Fluency"]))) is None
assert not ck3.order_skipped and len(ck3.parsed) == 1

# the record written for a skipped row (generate.finish_attempt)
import generate        # noqa: E402
rec = {"attempts": []}
calls = [{"response_text": "answer 1 text"}, {"response_text": "answer 3 text"}]
assert generate.finish_attempt(rec, calls, None, None, None, ck, 3) is False
f = rec["final"]
assert f["status"] == "ok" and f["order_prompt_skipped"] is True and f["answer3"] == "answer 3 text"
assert json.loads(f["answer2"])["auto"] is True and f["ordering"] == ["Representing"]
print("OK: one-practice answers skip the order prompt; two-practice answers still get it")
