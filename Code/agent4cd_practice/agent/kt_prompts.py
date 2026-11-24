"""
Agent4CD's prompts (agent/prompts.py, after the paper's appendix) for the FoundationalASSIST KT benchmark, with
cognitive student modeling added:
  - the exercise is shown in the benchmark's format (problem type, problem, lettered answer options, correct answer);
  - every memory record also shows the student's answer and whether they used a hint or saw the answer;
  - Task 3b asks for the exact answer the student will give (multiple choice: letters; fill-in: the exact text), and
    the JSON answer becomes {task1, task2, student_answer, task3}: task3 (Yes/No) stays last, so llm.yes_probability
    still reads P(Yes) from its token;
  - the per-answer reflection: after a predicted target, the agent sees its own prediction (correctness and answer)
    next to the student's real answer, with the paper's corrective trigger when the Yes/No was wrong; after any other
    answer of the bin, it sees the student's answer and outcome (no trigger: nothing was predicted).
"""

from common import tier
from agent.prompts import AFFECT_STATES, FALSE_NEGATIVE, FALSE_POSITIVE, TASK1, TASK2, TASK3, clip

NO_SKILL = "(no skill tag)"

TASK3B = ("[Task 3b: Answer Prediction]\n"
          "Predict the exact answer the student will give on the first try. For Multiple Choice (select 1), a single "
          "letter (e.g., \"B\"); for Multiple Choice (select all), the letters separated by commas (e.g., \"A, C\"); "
          "for fill-in problems, the exact text the student would write. If you predict that the student answers "
          "correctly (Yes), give the correct answer; if you predict No, give the wrong answer this student would most "
          "likely give.")


def concept_names(cids, ctx):
    return "; ".join(ctx.concepts[str(c)]["name"] for c in cids) if cids else NO_SKILL


def render_records(facts, ctx):
    if not facts:
        return "(none)"
    limit = ctx.config["agent"]["memory_text_chars"]
    lines = []
    for i, fact in enumerate(facts, 1):
        info = ctx.exercises[fact["exercise"]]
        content = clip(info["body"], limit)
        answer = clip(fact.get("answer", ""), 120)
        help_used = (", used a hint" if fact.get("hint") else "") + (", saw the answer" if fact.get("saw") else "")
        lines.append(f"{i}) Record {i}: Content = '{content}', Type = {info['problem_type']}, "
                     f"Concept = {concept_names(fact['concepts'], ctx)}, Student's answer = '{answer}', "
                     f"Correct = {fact['correct']}{help_used}.")
    return "\n".join(lines)


def knowledge_state(theta, cids, ctx, memory):
    """S_state: the tool's mastery of the given concepts; a concept the student has not answered yet says so (its
    value is the tool's neutral 0.5, not evidence)."""
    seen = {c for fact in memory.facts for c in fact["concepts"]}
    lines = []
    for c in cids:
        value = float(theta[c - 1])
        note = "" if c in seen else " (no answers on this concept yet)"
        lines.append(f"- {ctx.concepts[str(c)]['name']}: {tier(value)} ({value:.2f}){note}")
    return "\n".join(lines) if lines else "(the exercise has no skill tag)"


def prediction_schema():
    properties = {"task1": {"type": "string"}, "task2": {"type": "string", "enum": AFFECT_STATES},
                  "student_answer": {"type": "string"}, "task3": {"type": "string", "enum": ["Yes", "No"]}}
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def prediction_prompt(pid, ctx, memory, theta, previous_reasoning):
    info = ctx.exercises[pid]
    cids = ctx.q.get(pid, [])
    agent = ctx.config["agent"]
    parts = [
        "[Context: Current Exercise]\n"
        f"1) Current Exercise Content:\n{clip(info['text'], agent['exercise_text_chars'], flatten=False)}\n"
        f"2) KC (True): {concept_names(cids, ctx)}.",
        "[Context: Current Knowledge State (from the NCDM tool)]\n"
        "The student's mastery of the knowledge concepts of this exercise:\n" + knowledge_state(theta, cids, ctx, memory),
        "[Context: Learning Status]\n" + (memory.latest_status() or "(no learning status yet)"),
        "[Context: Factual Memory (reinforced records on related concepts)]\n"
        + render_records(memory.reinforced(cids, agent["factual_k"]), ctx),
    ]
    if previous_reasoning:
        parts.append("[Context: Previous Reasoning]\nYour reasoning about the learner on the previous exercise:\n"
                     + clip(previous_reasoning, 1500))
    parts += [TASK1,
              "[Context: Short-term Memory (Behavioral Sequences)]\nYour Short-term Memory (recent facts):\n"
              + render_records(memory.short_term(), ctx),
              TASK2, TASK3, TASK3B,
              "[Output Constraints]\nOutput format exactly as this JSON object:\n"
              '{"task1": "<your problem-solving logic>", '
              '"task2": "<the affective state you identified: confident, frustrated, bored or engaged>", '
              '"student_answer": "<the exact answer the student will give>", "task3": "<Yes/No>"}']
    return "\n\n".join(parts)


def reflection_prompt(ctx, memory, theta, event=None):
    """event None: the initial reflection over the history. Otherwise the answer just revealed: exercise, truth,
    answer, hint, saw, and (for a predicted target) prediction, predicted_answer, task1, task2."""
    agent = ctx.config["agent"]
    parts = []
    if event is not None:
        predicted = event.get("prediction") is not None
        if predicted and event["prediction"] != event["truth"]:
            parts.append("[Stage 1: Corrective Feedback]\n" + (FALSE_NEGATIVE if event["truth"] == 1 else FALSE_POSITIVE))
        info = ctx.exercises[event["exercise"]]
        lines = [f"Content: {clip(info['body'], agent['memory_text_chars'])}",
                 f"Type: {info['problem_type']}", f"Concept: {concept_names(ctx.q.get(event['exercise'], []), ctx)}"]
        if predicted:
            if event.get("task1"):
                lines.append(f"Your reasoning: {clip(event['task1'], 1500)}")
            if event.get("task2"):
                lines.append(f"The affective state you identified: {event['task2']}")
            lines.append(f"Your prediction: {'Yes' if event['prediction'] else 'No'}, answer "
                         f"'{clip(event.get('predicted_answer') or '', 120)}'.")
        help_used = (" (after a hint)" if event.get("hint") else "") + (" (after seeing the answer)" if event.get("saw") else "")
        lines.append(f"The student's actual answer: '{clip(event.get('answer', ''), 120)}', "
                     f"{'correct' if event['truth'] else 'incorrect'}{help_used}.")
        parts.append(("[The exercise you just predicted]\n" if predicted else "[The exercise the student just answered]\n")
                     + "\n".join(lines))
    short = memory.short_term()
    current = ctx.q.get(event["exercise"], []) if event is not None else None
    long_term = memory.reinforced(current, agent["factual_k"])
    shown = []
    for c in (current or []) + [c for fact in short + long_term for c in fact["concepts"]]:
        if c not in shown:
            shown.append(c)
    previous = memory.latest_status() or "(none: this is your first reflection)"
    parts.append(
        "[Stage 2: Summary Instruction]\n"
        "Reflect on results, affect, and update knowledge state.\n"
        f"You should directly output your reflection and summarize your # Learning Status # within "
        f"{agent['summary_max_words']} words based on your:\n"
        "1) profile: the # profile # above;\n"
        f"2) short-term memory:\n{render_records(short, ctx)}\n"
        f"3) long-term memory:\n{render_records(long_term, ctx)}\n"
        f"4) previous learning status:\n{previous}\n"
        f"5) current knowledge state (from NCDM tool):\n{knowledge_state(theta, shown[:20], ctx, memory)}\n"
        "Also keep track of the kinds of wrong answers this student gives, so you can predict their exact answers.\n"
        "Constraint: Do not output any other information."
    )
    return "\n\n".join(parts)
