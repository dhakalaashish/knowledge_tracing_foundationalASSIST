"""
One learner agent (Section IV): profile, memory, reflection and action modules around the LLM.

Initialization: the memory receives the learner's history (all non-test records, in time order) with
Eq. 4 reinforcement, and an initial summary reflection SR_0 summarizes it.
Each test record, in time order (action module, Section IV-D):
    1. Problem comprehension, reasoning, affect and prediction in one call (Eqs. 5, 6, 9, 10).
    2. With online_feedback (the paper's protocol): the true outcome is revealed, the record enters the
       memory (Eq. 4), and one reflection call does the corrective (Eq. 7, only if the prediction was
       wrong) and summary (Eq. 8) reflection; its output is the new learning status, and memory, CR and
       the learning status are the updated agent state (Eq. 11). No model parameters change.
       Without online_feedback no test outcome is ever revealed, so only the prediction call is made.
Every step is appended to results/<split>/<run>/students/<student>.jsonl as soon as it is done, and a
rerun replays the saved steps to rebuild the agent's state before continuing.
"""

import json
import os

from agent.learner_profile import NO_PROFILE_PROMPT, profile_prompt
from agent.llm import parse_prediction, yes_probability
from agent.memory import Memory
from agent.prompts import prediction_prompt, prediction_schema, reflection_prompt


class LearnerAgent:
    def __init__(self, student, ctx, llm, log_path):
        self.student = student
        self.ctx = ctx
        self.llm = llm
        self.log_path = log_path
        cfg = ctx.config["agent"]
        self.ablation = cfg["ablation"]
        self.online = cfg["online_feedback"]
        self.theta = ctx.proficiency[student]
        self.profile = ctx.profiles[student]
        self.system = NO_PROFILE_PROMPT if self.ablation == "no_profile" else profile_prompt(self.profile)
        self.memory = Memory(ctx.related, cfg["short_term_size"])
        for exercise, correct in ctx.history[student]:
            self.memory.add(exercise, self.concepts(exercise), correct)

    def concepts(self, exercise):
        return self.ctx.exercises[str(exercise)]["concepts"]

    def messages(self, user_prompt):
        return [{"role": "system", "content": self.system}, {"role": "user", "content": user_prompt}]

    def saved_entries(self):
        if not os.path.exists(self.log_path):
            return []
        entries, cut_off = [], False
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:  # a line cut off by a crash: redo that step
                        cut_off = True
                        break
        if cut_off:  # rewrite the file without the broken line, so new steps follow the good ones
            with open(self.log_path, "w", encoding="utf-8") as f:
                f.writelines(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries)
        return entries

    def save(self, entry):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    async def reflect(self, step=None):
        prompt = reflection_prompt(self.ctx, self.memory, self.theta, step)
        result = await self.llm.chat(self.messages(prompt), self.ctx.config["llm"]["max_tokens_reflect"])
        return result["text"].strip(), result

    async def predict(self, exercise, previous_reasoning):
        prompt = prediction_prompt(exercise, self.ctx, self.memory, self.theta, previous_reasoning)
        schema = prediction_schema(self.ablation)
        max_tokens = self.ctx.config["llm"]["max_tokens_predict"]
        tokens = [0, 0]
        for attempt in range(2):  # a cut-off answer is retried once with twice the token budget
            result = await self.llm.chat(self.messages(prompt), max_tokens * (attempt + 1), schema=schema, logprobs=True)
            tokens[0] += result["prompt_tokens"]
            tokens[1] += result["completion_tokens"]
            parsed = parse_prediction(result["text"])
            if parsed is not None and result["finish_reason"] != "length":
                break
        step = {"task1": None, "task2": None, "prompt_tokens": tokens[0], "completion_tokens": tokens[1],
                "fallback": parsed is None}
        if parsed is None:
            # No usable answer: fall back to the knowledge-state tool's own prediction
            p_tool = float(self.ctx.tool_pred[(self.student, exercise)])
            step.update(prediction=int(p_tool >= 0.5), p_yes=p_tool, raw=result["text"][-500:])
            return step
        prediction = 1 if parsed["task3"] == "Yes" else 0
        p_yes = yes_probability(result["logprobs"])
        if p_yes is None:  # no Yes/No token among the logprobs: use the answer itself
            p_yes = float(prediction)
        step.update(prediction=prediction, p_yes=p_yes, task1=parsed.get("task1"), task2=parsed.get("task2"))
        return step

    async def run(self):
        ctx = self.ctx
        entries = self.saved_entries()
        init = next((e for e in entries if e["type"] == "init"), None)
        done = [e for e in entries if e["type"] == "step"]

        if self.ablation != "no_reflection":
            if init is None:
                status, result = await self.reflect()
                init = {"type": "init", "student": self.student, "reflection": status,
                        "prompt_tokens": result["prompt_tokens"], "completion_tokens": result["completion_tokens"]}
                self.save(init)
            self.memory.learning_status.append(init["reflection"])

        previous_reasoning = None
        for index, (exercise, truth) in enumerate(ctx.test[self.student]):
            if index < len(done):  # replay a saved step
                step = done[index]
                assert step["exercise"] == exercise, f"student {self.student}: saved steps do not match the test records"
                if self.online:
                    self.memory.add(exercise, self.concepts(exercise), truth)
                    if step.get("reflection"):
                        self.memory.learning_status.append(step["reflection"])
                    self.memory.corrective = step.get("corrective")
                previous_reasoning = step.get("task1")
                continue

            step = {"type": "step", "student": self.student, "index": index, "exercise": exercise, "truth": truth}
            step.update(await self.predict(exercise, previous_reasoning))
            step["reflection"] = None
            step["corrective"] = None
            if self.online:
                self.memory.add(exercise, self.concepts(exercise), truth)
                if step["prediction"] != truth:
                    step["corrective"] = "false_negative" if truth == 1 else "false_positive"
                self.memory.corrective = step["corrective"]
                if self.ablation != "no_reflection":
                    status, result = await self.reflect(step)
                    step["reflection"] = status
                    step["prompt_tokens"] += result["prompt_tokens"]
                    step["completion_tokens"] += result["completion_tokens"]
                    self.memory.learning_status.append(status)
            self.save(step)
            previous_reasoning = step.get("task1")
            ctx.progress.update(step)

    def dry_run(self):
        """The prompts of the first calls, without calling the LLM."""
        print("=" * 30, f"student {self.student}", "=" * 30)
        print(f"Profile: {json.dumps({k: v for k, v in self.profile.items()}, default=str)}")
        print(f"History: {len(self.ctx.history[self.student])} records   test: {len(self.ctx.test[self.student])} records")
        print("\n--- SYSTEM ---\n" + self.system)
        if self.ablation != "no_reflection":
            print("\n--- USER (initial reflection SR_0) ---\n" + reflection_prompt(self.ctx, self.memory, self.theta))
            self.memory.learning_status.append("<the initial reflection would appear here>")
        exercise, truth = self.ctx.test[self.student][0]
        print("\n--- USER (prediction, first test record) ---\n"
              + prediction_prompt(exercise, self.ctx, self.memory, self.theta, None))
        print(f"\n--- JSON schema ---\n{json.dumps(prediction_schema(self.ablation))}")
        if self.online and self.ablation != "no_reflection":
            fake = {"exercise": exercise, "truth": truth, "prediction": 1 - truth,
                    "task1": "<reasoning>", "task2": "confident"}
            self.memory.add(exercise, self.concepts(exercise), truth)
            print("\n--- USER (reflection after the first test record, if the prediction were wrong) ---\n"
                  + reflection_prompt(self.ctx, self.memory, self.theta, fake))
