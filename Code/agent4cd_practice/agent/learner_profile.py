"""
Learner profile module (Section IV-A).

Behavioral patterns (Eq. 1), from the student's history:
    P^act = |E_s| / |E|      activity level
    P^div = |K_s| / |KC|     practice diversity
    P^suc = mean r_se        success rate
Cognitive factor: the IRT 2PL ability P^ab (Eq. 2, tools/irt.py).

Static agent configuration (Eq. 3): S_profile <- f^P(P^act, P^div, P^suc, P^ab). Each statistic is
placed in a tertile of all students of the split and translated into the behavioral tendency the
appendix-A prompt describes; P^ab becomes the good / common / poor ability level.
"""

import numpy as np

ACTIVITY_TEXT = {
    "high": "frequently engage in online practice",
    "medium": "practice online regularly, but not very often",
    "low": "rarely practice online",
}
DIVERSITY_TEXT = {
    "high": "explore a wide range of knowledge concepts",
    "medium": "cover a moderate range of knowledge concepts",
    "low": "focus on a limited set of knowledge concepts",
}
SUCCESS_TEXT = {"high": "high", "medium": "medium", "low": "low"}
ABILITY_TEXT = {"high": "good", "medium": "common", "low": "poor"}


def level(value, thresholds):
    """Tertile of value among all students: low / medium / high (None when there is no value)."""
    if value is None:
        return None
    if value <= thresholds[0]:
        return "low"
    if value <= thresholds[1]:
        return "medium"
    return "high"


def ability_thresholds(ability, history):
    """Tertiles of the IRT ability over the students that have a history."""
    seen = [s for s, records in history.items() if records]
    return [float(q) for q in np.quantile(ability[seen], [1 / 3, 2 / 3])]


def build_profile(stats, thresholds, ability, ability_cuts, concepts):
    """The profile of one student: raw statistics, their levels, and the prompt descriptions."""
    levels = {key: level(stats[key], thresholds[key]) for key in ("activity", "diversity", "success")}
    levels["ability"] = level(float(ability), ability_cuts) if stats["num_records"] else None
    preference = stats["preference_concept"]
    success = stats["success"]
    return {
        "P_act": stats["activity"],
        "P_div": stats["diversity"],
        "P_suc": success,
        "P_ab": float(ability),
        "levels": levels,
        "activity_description": ACTIVITY_TEXT[levels["activity"]],
        "diversity_description": DIVERSITY_TEXT[levels["diversity"]],
        "preference_concept": concepts[str(preference)]["name"] if preference is not None else "none yet",
        "success_level": (f"{SUCCESS_TEXT[levels['success']]} ({success:.0%} of previous answers correct)"
                          if success is not None else "unknown (no previous answers)"),
        "ability_level": ABILITY_TEXT[levels["ability"]] if levels["ability"] else "unknown",
    }


def profile_prompt(profile):
    """System prompt of appendix A (System Configuration and Profile Anchoring)."""
    return (
        "You are an intelligent learning advisor. Based on the student's profile.\n"
        f"1) They {profile['activity_description']}.\n"
        f"2) And they {profile['diversity_description']}.\n"
        f"3) Their most practiced concept is \"{profile['preference_concept']}\".\n"
        f"4) Their success rate is {profile['success_level']}.\n"
        f"5) Their problem-solving ability is rated as {profile['ability_level']}.\n"
        "Constraint: you must simulate the problem-solving process and potential errors consistent with "
        "this ability level.\n"
        "The information above is your # profile #."
    )


# Used by the w/o Prof ablation: the agent gets no profile
NO_PROFILE_PROMPT = (
    "You are an intelligent learning advisor. You simulate how a student solves math exercises and "
    "predict whether the student answers them correctly."
)
