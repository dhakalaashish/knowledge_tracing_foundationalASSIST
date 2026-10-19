"""
Memory module (Section IV-B) and the agent-level state the reflection module updates (Eq. 11).

Factual memory (Eq. 4): M <- M U {l_si};  f_sj <- f_sj + I(R(C_ei, C_ej) = 1).
    Every stored record j whose KC set is related to the new record's KC set is reinforced. R is the
    statistical KC relation of prepare_data.py (shared concept, or a transition edge either way).
    The memory starts empty and receives the learner's history in time order; with online feedback,
    each test record is added after its outcome is revealed.
Short-term memory: the d most recent records M_s,short (the affect module's input, Eq. 6).
Reinforced facts: the records related to the current exercise with the highest reinforcement count
    f_sj (ties: most recent first), shown to the reasoning module as the learner's factual memory.
Learning status: the summary reflections SR (Eq. 8), the agent-level interpretation of the
    learner's knowledge state; the latest one is shown in the next prediction.
Corrective state CR: the last corrective trigger (FN / FP / None) from Eq. 7.
"""


class Memory:
    def __init__(self, related, short_term_size):
        # related: concept id -> set of related concept ids; every concept is related to itself
        self.related = {c: set(r) | {c} for c, r in related.items()}
        self.short_term_size = short_term_size
        self.facts = []
        self.learning_status = []
        self.corrective = None

    def neighborhood(self, concepts):
        """All concepts related to any concept of the set (R is symmetric)."""
        near = set()
        for c in concepts:
            near |= self.related.get(c, {c})
        return near

    def is_related(self, concepts_a, concepts_b):
        """R(C_a, C_b) = 1."""
        return not self.neighborhood(concepts_a).isdisjoint(concepts_b)

    def add(self, exercise, concepts, correct):
        """Eq. 4: reinforce the related records, then store the new one (count 1)."""
        near = self.neighborhood(concepts)
        for fact in self.facts:
            if not near.isdisjoint(fact["concepts"]):
                fact["count"] += 1
        self.facts.append({"exercise": exercise, "concepts": list(concepts), "correct": int(correct),
                           "count": 1, "step": len(self.facts)})

    def short_term(self):
        return self.facts[-self.short_term_size:] if self.short_term_size > 0 else []

    def reinforced(self, concepts, k):
        """
        The k most reinforced records related to concepts (all records when concepts is None),
        leaving out the short-term records, which the prompt shows separately.
        """
        recent = len(self.facts) - len(self.short_term())
        near = None if concepts is None else self.neighborhood(concepts)
        candidates = [fact for fact in self.facts[:recent]
                      if near is None or not near.isdisjoint(fact["concepts"])]
        candidates.sort(key=lambda fact: (fact["count"], fact["step"]), reverse=True)
        return candidates[:k]

    def latest_status(self):
        return self.learning_status[-1] if self.learning_status else None
