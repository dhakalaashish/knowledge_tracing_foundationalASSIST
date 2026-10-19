"""
Prompts of Agent4CD, after the paper's appendix templates.

Prediction (appendix C; Eqs. 5, 6, 9, 10 in one call):
    Problem comprehension (Eq. 9): the exercise, its KCs, and S_state = the tool's theta (.) Q_e
        written as "concept: tier (value)", plus the latest learning status SR.
    Reasoning (Eq. 5): Task 1 infers the learner's reasoning path from the factual memory M_s, the
        profile (system prompt) and the previous reasoning result R_{i-1}.
    Affect (Eq. 6): Task 2 infers the affective state from the short-term memory M_s,short.
    Reasoning and solving (Eq. 10): Task 3 predicts Yes / No.
    The answer is a JSON object {task1, task2, task3} (schema-constrained) instead of the paper's
    "Task1: / Task2: / Task3:" lines, so it always parses.
Reflection (appendix B; Eqs. 7, 8, 11 in one call):
    Stage 1 (corrective reflection, Eq. 7): the paper's false-negative / false-positive trigger,
        inserted only when the prediction was wrong.
    Stage 2 (summary reflection, Eq. 8): summarize the # Learning Status # from the profile, short-
        and long-term memory, the previous learning status and the tool's knowledge state.
Ablations (RQ6): no_profile drops the profile, no_reasoning drops Task 1 and R_{i-1}, no_affect drops
Task 2, no_reflection drops the learning status and every reflection call.
"""

from common import tier

AFFECT_STATES = ["confident", "frustrated", "bored", "engaged"]

FALSE_NEGATIVE = ("You thought you couldn't solve this problem correctly, but in fact, you will solve it correctly. "
                  "You should also reconsider your problem-solving logic and affect state.")
FALSE_POSITIVE = ("You thought you could solve this problem correctly, but in fact, you do not answer it correctly. "
                  "You should also reconsider your problem-solving logic and affect state.")

TASK1 = ("[Task 1: Reasoning Path Generation]\n"
         "Based on the learner's factual memory of past question-solving behavior, infer the likely reasoning path "
         "or problem-solving logic the learner might adopt for this question. Use relevant prior answer patterns "
         "and cognitive tendencies to explain the expected logic step by step.")
TASK2 = ("[Task 2: Affective State Inference]\n"
         "Based on the student's recent facts, infer the affective state (e.g., confident, frustrated, bored, and "
         "engaged).\n"
         "1) Confident: stable performance aligned with ability level.\n"
         "2) Frustrated: consecutive failures or struggles with familiar concepts.\n"
         "3) Bored/Slip: high-ability student makes errors on simple tasks.\n"
         "4) Engaged/Flow: continuous correct responses on challenging tasks.")
TASK3 = ("[Task 3: Performance Prediction]\n"
         "Predict whether the student will answer correctly (\"Yes\" or \"No\").")


def clip(text, limit, flatten=True):
    """Shorten text to limit characters; flatten puts it on one line (for records in a list)."""
    text = " ".join(str(text).split()) if flatten else str(text).strip()
    return text if len(text) <= limit else text[:limit].rstrip() + " ..."


def concept_names(cids, concepts):
    return "; ".join(concepts[str(c)]["name"] for c in cids)


def render_records(facts, ctx):
    if not facts:
        return "(none)"
    limit = ctx.config["agent"]["memory_text_chars"]
    lines = []
    for i, fact in enumerate(facts, 1):
        content = clip(ctx.exercises[str(fact["exercise"])]["body"], limit)
        lines.append(f"{i}) Record {i}: Content = '{content}', Concept = {concept_names(fact['concepts'], ctx.concepts)}, "
                     f"Correct = {fact['correct']}.")
    return "\n".join(lines)


def knowledge_state(theta, cids, ctx):
    """S_state: the tool's mastery of the given concepts (theta (.) Q_e for an exercise's concepts)."""
    lines = []
    for c in cids:
        value = float(theta[c - 1])
        lines.append(f"- {ctx.concepts[str(c)]['name']}: {tier(value)} ({value:.2f})")
    return "\n".join(lines) if lines else "(none)"


def prediction_schema(ablation):
    properties = {}
    if ablation != "no_reasoning":
        properties["task1"] = {"type": "string"}
    if ablation != "no_affect":
        properties["task2"] = {"type": "string", "enum": AFFECT_STATES}
    properties["task3"] = {"type": "string", "enum": ["Yes", "No"]}
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def prediction_prompt(exercise, ctx, memory, theta, previous_reasoning):
    """User prompt of the prediction call for one exercise."""
    ablation = ctx.config["agent"]["ablation"]
    info = ctx.exercises[str(exercise)]
    cids = info["concepts"]
    parts = [
        "[Context: Current Exercise]\n"
        f"1) Current Exercise Content:\n{clip(info['text'], ctx.config['agent']['exercise_text_chars'], flatten=False)}\n"
        f"2) KC (True): {concept_names(cids, ctx.concepts)}.",
        f"[Context: Current Knowledge State (from the {ctx.tool_name} tool)]\n"
        "The student's mastery of the knowledge concepts of this exercise:\n"
        + knowledge_state(theta, cids, ctx),
    ]
    if ablation != "no_reflection":
        parts.append("[Context: Learning Status]\n" + (memory.latest_status() or "(no learning status yet)"))
    if ablation != "no_reasoning":
        facts = memory.reinforced(cids, ctx.config["agent"]["factual_k"])
        parts.append("[Context: Factual Memory (reinforced records on related concepts)]\n" + render_records(facts, ctx))
        if previous_reasoning:
            parts.append("[Context: Previous Reasoning]\n"
                         "Your reasoning about the learner on the previous exercise:\n" + clip(previous_reasoning, 1500))
        parts.append(TASK1)
    parts.append("[Context: Short-term Memory (Behavioral Sequences)]\n"
                 "Your Short-term Memory (recent facts):\n" + render_records(memory.short_term(), ctx))
    if ablation != "no_affect":
        parts.append(TASK2)
    parts.append(TASK3)

    fields = []
    if ablation != "no_reasoning":
        fields.append('"task1": "<your problem-solving logic>"')
    if ablation != "no_affect":
        fields.append('"task2": "<the affective state you identified: confident, frustrated, bored or engaged>"')
    fields.append('"task3": "<Yes/No>"')
    parts.append("[Output Constraints]\nOutput format exactly as this JSON object:\n{" + ", ".join(fields) + "}")
    return "\n\n".join(parts)


def reflection_prompt(ctx, memory, theta, step=None):
    """
    User prompt of the reflection call. step is None for the initial reflection over the history;
    otherwise it holds the exercise just predicted, the agent's answer and the revealed outcome.
    """
    agent_cfg = ctx.config["agent"]
    parts = []
    if step is not None:
        if step["prediction"] != step["truth"]:
            parts.append("[Stage 1: Corrective Feedback]\n"
                         + (FALSE_NEGATIVE if step["truth"] == 1 else FALSE_POSITIVE))
        info = ctx.exercises[str(step["exercise"])]
        lines = [f"Content: {clip(info['body'], agent_cfg['memory_text_chars'])}",
                 f"Concept: {concept_names(info['concepts'], ctx.concepts)}"]
        if step.get("task1"):
            lines.append(f"Your reasoning: {clip(step['task1'], 1500)}")
        if step.get("task2"):
            lines.append(f"The affective state you identified: {step['task2']}")
        lines.append(f"Your prediction: {'Yes' if step['prediction'] else 'No'}. "
                     f"The student's actual response: {'correct' if step['truth'] else 'incorrect'}.")
        parts.append("[The exercise you just predicted]\n" + "\n".join(lines))

    short = memory.short_term()
    current = ctx.exercises[str(step["exercise"])]["concepts"] if step is not None else None
    long_term = memory.reinforced(current, agent_cfg["factual_k"])
    shown = []
    for cid in (current or []) + [c for fact in short + long_term for c in fact["concepts"]]:
        if cid not in shown:
            shown.append(cid)
    previous = memory.latest_status() or "(none: this is your first reflection)"
    parts.append(
        "[Stage 2: Summary Instruction]\n"
        "Reflect on results, affect, and update knowledge state.\n"
        f"You should directly output your reflection and summarize your # Learning Status # within "
        f"{agent_cfg['summary_max_words']} words based on your:\n"
        "1) profile: the # profile # above;\n"
        f"2) short-term memory:\n{render_records(short, ctx)}\n"
        f"3) long-term memory:\n{render_records(long_term, ctx)}\n"
        f"4) previous learning status:\n{previous}\n"
        f"5) current knowledge state (from {ctx.tool_name} tool):\n{knowledge_state(theta, shown[:20], ctx)}\n"
        "Constraint: Do not output any other information."
    )
    return "\n\n".join(parts)
