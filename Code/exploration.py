#!/usr/bin/env python3
"""
Two research questions about the mathematical practices of FoundationalASSIST problems.

RQ1  Students meet some practices much less often than others. Do they struggle more with them?
RQ2  Does mastery of a practice transfer across concepts?

A problem's practice is the one with the highest probability in Problems.csv
['mathematical_practice'] (the same labels as the practice prompts; ties give several). A
concept is the Common Core domain of the problem's skill codes (6.RP.A.1 -> RP), or the whole
code with --concept standard. Struggle = discrete_score 0 (not correct on the first try without
help); hint use and answer requests are secondary outcomes.

RQ1 in three steps:
  1. Exposure: how unevenly students meet each practice.
  2. Difficulty on equal footing: logistic model of correctness on practice, controlling for
     answer format (two-option multiple choice is 50% guessable), grade, domain, time of year
     and student ability. Reported as percentage-point gaps against Procedural Fluency.
  3. Is it because of rarity? If it were, students who had met a practice more often would do
     better on the same problem. The slope of success on earlier encounters with the practice
     is estimated beyond problem difficulty, prior accuracy and general progress, and turned
     into percentage points over the exposure range students actually have. (Comparing
     practices "at the same encounter number" is not used: for Procedural, the k-th encounter
     is almost the k-th problem of the course, so it would mix up exposure and time of year.)

RQ2 splits each student's earlier attempts, relative to the attempt being predicted, into
  A same practice + same concept     B same practice + other concept  (practice transfer)
  C other practice + same concept    D other practice + other concept (general ability)
  E earlier parts of the same multi-part problem (shared scenario; kept apart)
  1. All attempts: does accuracy in B predict success beyond accuracy in D?
  2. Cold start: the first attempt of a practice in a concept (A is empty). Accuracy in B is
     compared with a placebo, the accuracy on an equally large random sample of D problems,
     so both predictors are equally noisy.
  3. Source -> target matrix: does accuracy on source practice q (3 problems, other concepts)
     predict the first attempt of target practice p?
  4. Predictive value: held-out AUC of a knowledge-tracing model with and without the
     same-practice history.

Standard errors are clustered by both student and problem (practice is a property of the
problem, and some practices have few problems). Practices with fewer than 20 problems
(Modeling, Collaborative) are described but left out of the models.

Outputs (Results/exploration[_variant]/): CSV tables, PNG figures and report.md.

Usage (from the Code/ directory; CPU only, a few minutes):
    python exploration.py                       # both research questions, all 5,000 students
    python exploration.py --rq 2 --concept standard
    python exploration.py --confident-labels    # only problems with a clear top practice
    python exploration.py --self-test           # check the statistics code on synthetic data
"""

import argparse
import json
import os
import time

import numpy as np
import pandas as pd
from scipy.special import expit

import qwen3_30b_benchmark as B
import qwen3_30b_benchmark_practice as PR

SHORT = {
    "Representing": "Representing",
    "Abstracting and Generalizing": "Abstracting",
    "Justifying and Proving": "Justifying",
    "Mathematical Modeling": "Modeling",
    "Collaborative Mathematics": "Collaborative",
    "Procedural Fluency": "Procedural",
}
PRACTICES = [SHORT[name] for name in PR.PRACTICE_NAMES]
REFERENCE = "Procedural"
MIN_PROBLEMS = 20        # fewer problems than this: descriptive only
SMOOTH = 5               # pseudo-responses when shrinking item/student accuracy to the mean
FORMATS = ["Fill-in/Order", "MC 2 options", "MC 3+ options", "Select all"]
CELLS = ["A", "B", "C", "D", "E"]
CELL_NAMES = {
    "A": "same practice, same concept",
    "B": "same practice, other concept",
    "C": "other practice, same concept",
    "D": "other practice, other concept",
    "E": "earlier part of the same problem",
}
MATRIX_SAMPLE = 3        # problems per source practice in the transfer matrix
MATCHED_MAX = 20         # cold start: at most this many problems in each matched sample (B and placebo)

# Chart styling (reference palette of the dataviz guidance; validated for 4 adjacent series)
SURFACE, INK, INK_2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
PRACTICE_COLORS = {"Procedural": "#2a78d6", "Representing": "#eb6834", "Abstracting": "#1baf7a",
                   "Justifying": "#eda100"}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load_problems(args):
    """One row per problem: practice membership, primary practice, format, grade, concepts."""
    problems = pd.read_csv(os.path.join(B.DATA_DIR, "Problems.csv"), dtype=str, keep_default_na=False)
    problems = problems.drop_duplicates("problem_id").reset_index(drop=True)
    problems["problem_id"] = problems["problem_id"].astype(int)
    labels = PR.practice_labels()
    problems = problems[problems["problem_id"].isin(labels)].reset_index(drop=True)

    scores = np.array([json.loads(cell) for cell in problems["mathematical_practice"]])
    ordered = np.sort(scores, axis=1)
    problems["top_score"], problems["margin"] = ordered[:, -1], ordered[:, -1] - ordered[:, -2]
    if args.confident_labels:
        problems = problems[(problems["top_score"] >= 0.7) & (problems["margin"] >= 0.2)].reset_index(drop=True)
    names = [labels[pid].split("; ") for pid in problems["problem_id"]]
    member = np.array([[name in n for name in PR.PRACTICE_NAMES] for n in names])
    problems["practice"] = [SHORT[n[0]] for n in names]  # first in list order on ties

    options = problems["Multiple Choice Options"].map(lambda x: len([o for o in x.split("||") if o.strip()]))
    kind = problems["Problem Type"]
    problems["format"] = np.select(
        [kind.eq("Multiple Choice (select 1)") & options.eq(2), kind.eq("Multiple Choice (select 1)"),
         kind.eq("Multiple Choice (select all)")],
        FORMATS[1:], FORMATS[0])
    problems["problem_set"] = pd.factorize(problems["Problem Set Id"])[0]

    skills = pd.read_csv(os.path.join(B.DATA_DIR, "Skills.csv"), dtype=str)
    skills["problem_id"] = skills["problem_id"].astype(int)
    skills["domain"] = skills["node_code"].str.split(".").str[1]
    skills["grade"] = skills["node_code"].str.split(".").str[0].map(lambda g: g if g in ("6", "7", "8") else "5 or lower")
    skills["concept"] = skills["domain"] if args.concept == "domain" else skills["node_code"]
    first = skills.drop_duplicates("problem_id").set_index("problem_id")
    problems["domain"] = problems["problem_id"].map(first["domain"]).fillna("none")
    problems["grade"] = problems["problem_id"].map(first["grade"]).fillna("6")

    concept_codes, concept_names = pd.factorize(skills["concept"])
    row_of = {pid: i for i, pid in enumerate(problems["problem_id"])}
    concepts = np.zeros((len(problems), len(concept_names)), dtype=np.float32)
    for pid, code in zip(skills["problem_id"], concept_codes):
        if pid in row_of:
            concepts[row_of[pid], code] = 1
    return problems, member.astype(np.float32), concepts


def load_attempts(args, problems, member):
    """Attempts in time order per student, with prior counts and difficulty controls."""
    attempts = pd.read_csv(os.path.join(B.DATA_DIR, "Interactions.csv"),
                           usecols=["id", "problem_id", "user_id", "discrete_score", "hint_count", "saw_answer"])
    attempts = attempts.drop_duplicates("id").dropna(subset=["discrete_score"])
    if args.students == "paper" or args.user_ids_file:
        if args.user_ids_file:
            users = set(B.read_user_ids(args.user_ids_file))
        else:
            from qwen3_30b_all_practice_both import paper_user_ids
            users = paper_user_ids()
        attempts = attempts[attempts["user_id"].isin(users)]
    row_of = pd.Series(np.arange(len(problems)), index=problems["problem_id"])
    attempts = attempts[attempts["problem_id"].isin(row_of.index)]
    attempts = attempts.sort_values(["user_id", "id"]).reset_index(drop=True)

    a = pd.DataFrame({"user_id": attempts["user_id"].values})
    a["student"] = pd.factorize(a["user_id"])[0]
    a["prob"] = row_of[attempts["problem_id"]].values
    a["y"] = attempts["discrete_score"].round().astype(int).values
    a["hint"] = (attempts["hint_count"].fillna(0) > 0).astype(int).values
    a["answer"] = attempts["saw_answer"].astype(str).str.lower().eq("true").astype(int).values
    for column in ("practice", "format", "grade", "domain", "problem_set"):
        a[column] = problems[column].values[a["prob"]]

    mean = a["y"].mean()
    # Leave-one-out item difficulty and student ability, shrunk toward the overall mean
    for key, name in (("prob", "item_logit"), ("student", "ability_logit")):
        total = a.groupby(key)["y"].transform("sum")
        count = a.groupby(key)["y"].transform("size")
        a[name] = logit((total - a["y"] + SMOOTH * mean) / (count - 1 + SMOOTH))

    by_student = a.groupby("student")
    a["prior_total"] = by_student.cumcount()
    # When in the course a problem is usually done: mean progress (0 = a student's first
    # attempt, 1 = last) over everyone who attempted it. Controls for the time of year.
    progress = a["prior_total"] / (by_student["y"].transform("size") - 1).clip(lower=1)
    a["item_position"] = progress.groupby(a["prob"]).transform("mean")
    a["item_position_sq"] = a["item_position"] ** 2
    a["prior_correct"] = by_student["y"].cumsum() - a["y"]
    a["prior_acc_logit"] = logit((a["prior_correct"] + 1) / (a["prior_total"] + 2))
    counts = pd.DataFrame(member[a["prob"]], columns=PRACTICES)
    prior = counts.groupby(a["student"]).cumsum() - counts
    for practice in PRACTICES:
        a[f"prior_{practice}"] = prior[practice].values.astype(int)
    a["k"] = a[[f"prior_{p}" for p in PRACTICES]].values[np.arange(len(a)), a["practice"].map(PRACTICES.index)] + 1
    return a


def logit(p):
    p = np.clip(np.asarray(p, dtype=float), 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def inferential_practices(problems):
    counts = problems["practice"].value_counts()
    return [p for p in PRACTICES if counts.get(p, 0) >= MIN_PROBLEMS]


# ---------------------------------------------------------------------------
# Logistic regression with standard errors clustered by student and problem
# ---------------------------------------------------------------------------

def fit_logit(X, y, names, clusters=(), **kwargs):
    """Logistic regression (see _fit_logit). Columns that are constant apart from the
    intercept (e.g. a history cell that is always empty in a subset) are dropped and get
    NaN estimates, so a subset model never fails on a singular matrix."""
    X = np.asarray(X, dtype=np.float32)
    keep = np.r_[True, X[:, 1:].std(axis=0) > 1e-9]
    if keep.all():
        return _fit_logit(X, y, names, clusters, **kwargs)
    result = _fit_logit(X[:, keep], y, [n for n, k in zip(names, keep) if k], clusters, **kwargs)
    k = len(names)
    beta = np.full(k, np.nan)
    beta[keep] = result["beta"]
    result.update(names=list(names), beta=beta)
    if "cov" in result:
        cov = np.full((k, k), np.nan)
        cov[np.ix_(keep, keep)] = result["cov"]
        result.update(cov=cov, se=np.sqrt(np.diag(cov)))
    result["dropped"] = [n for n, k_ in zip(names, keep) if not k_]
    return result


def _fit_logit(X, y, names, clusters=(), chunk=250_000, max_iter=40, tol=1e-8):
    """Newton-Raphson logistic regression. With clusters (a list of integer code arrays),
    returns multi-way cluster-robust covariance (Cameron, Gelbach and Miller 2011)."""
    X = np.asarray(X, dtype=np.float32)
    y = np.asarray(y, dtype=np.float64)
    n, k = X.shape
    beta = np.zeros(k)

    def passes(beta):
        grad, hess, loglik = np.zeros(k), np.zeros((k, k)), 0.0
        for start in range(0, n, chunk):
            Xc = X[start:start + chunk].astype(np.float64)
            p = np.clip(expit(Xc @ beta), 1e-12, 1 - 1e-12)
            yc = y[start:start + chunk]
            grad += Xc.T @ (yc - p)
            hess += (Xc * (p * (1 - p))[:, None]).T @ Xc
            loglik += np.sum(yc * np.log(p) + (1 - yc) * np.log(1 - p))
        return grad, hess, loglik

    grad, hess, loglik = passes(beta)
    for _ in range(max_iter):
        step = np.linalg.lstsq(hess + 1e-9 * np.eye(k), grad, rcond=None)[0]
        new_beta = beta + step
        new_grad, new_hess, new_loglik = passes(new_beta)
        while new_loglik < loglik - 1e-9:  # step halving; rarely needed for a logit
            step /= 2
            new_beta = beta + step
            new_grad, new_hess, new_loglik = passes(new_beta)
        beta, grad, hess, loglik = new_beta, new_grad, new_hess, new_loglik
        if np.max(np.abs(step)) < tol:
            break

    result = {"names": list(names), "beta": beta, "loglik": loglik, "n": n}
    if not clusters:
        return result

    bread = np.linalg.pinv(hess)

    def meat(codes):
        codes = np.asarray(codes)
        groups = codes.max() + 1
        sums = np.zeros((groups, k))
        for start in range(0, n, chunk):
            Xc = X[start:start + chunk].astype(np.float64)
            residual = y[start:start + chunk] - expit(Xc @ beta)
            cc = codes[start:start + chunk]
            for j in range(k):
                sums[:, j] += np.bincount(cc, weights=Xc[:, j] * residual, minlength=groups)
        return groups / max(groups - 1, 1) * (bread @ (sums.T @ sums) @ bread)

    one_way = [meat(c) for c in clusters]
    cov = sum(one_way)
    if len(clusters) == 2:
        both = pd.factorize(pd.Series(clusters[0]).astype(np.int64) * (int(np.max(clusters[1])) + 1)
                            + pd.Series(clusters[1]).astype(np.int64))[0]
        cov = cov - meat(both)
        # The two-way estimate can have negative variances in rare cases; fall back per entry
        bad = np.diag(cov) <= 0
        if bad.any():
            fallback = np.maximum(*[np.diag(v) for v in one_way])
            cov[np.diag_indices(k)] = np.where(bad, fallback, np.diag(cov))
    result["cov"] = cov
    result["se"] = np.sqrt(np.diag(cov))
    return result


def coef(model, name):
    """(estimate, lower, upper) of one coefficient, 95% interval."""
    i = model["names"].index(name)
    b, se = model["beta"][i], model["se"][i]
    return b, b - 1.96 * se, b + 1.96 * se


def contrast(model, plus=None, minus=None, weights=None):
    """(estimate, lower, upper) of beta[plus] - beta[minus], or of sum(weight * beta[name])."""
    weights = weights or {plus: 1.0, minus: -1.0}
    c = np.zeros(len(model["names"]))
    for name, weight in weights.items():
        c[model["names"].index(name)] = weight
    if np.isnan(model["beta"][c != 0]).any():  # a term of the contrast was dropped
        return np.nan, np.nan, np.nan
    # Dropped columns have weight 0; zero their NaNs so they don't spread
    b, se = c @ np.nan_to_num(model["beta"]), np.sqrt(c @ np.nan_to_num(model["cov"]) @ c)
    return b, b - 1.96 * se, b + 1.96 * se


def predict(model, X, chunk=250_000):
    X = np.asarray(X, dtype=np.float32)
    beta = np.nan_to_num(model["beta"])  # dropped (constant) columns contribute nothing
    return np.concatenate([expit(X[s:s + chunk].astype(np.float64) @ beta) for s in range(0, len(X), chunk)])


def marginal_gap(model, X, dummy_cols, target_col, chunk=250_000):
    """Average marginal effect, in percentage points, of switching every row from the reference
    category (all dummies 0) to target_col, with a delta-method 95% interval."""
    X = np.asarray(X, dtype=np.float32)
    beta = np.nan_to_num(model["beta"])
    effect, gradient = 0.0, np.zeros(len(beta))
    for start in range(0, len(X), chunk):
        Xc = X[start:start + chunk].astype(np.float64)
        Xc[:, dummy_cols] = 0
        p0 = expit(Xc @ beta)
        g0 = (p0 * (1 - p0))[:, None] * Xc
        Xc[:, target_col] = 1
        p1 = expit(Xc @ beta)
        g1 = (p1 * (1 - p1))[:, None] * Xc
        effect += np.sum(p1 - p0)
        gradient += (g1 - g0).sum(axis=0)
    effect, gradient = effect / len(X), gradient / len(X)
    se = np.sqrt(gradient @ np.nan_to_num(model["cov"]) @ gradient)
    return 100 * effect, 100 * (effect - 1.96 * se), 100 * (effect + 1.96 * se)


def design(df, numeric, categorical=None):
    """Design matrix: intercept, numeric columns, then dummies for each categorical column
    (dict column -> reference level, or a list of levels to include)."""
    columns, names = [np.ones(len(df), dtype=np.float32)], ["intercept"]
    for name in numeric:
        columns.append(df[name].to_numpy(dtype=np.float32))
        names.append(name)
    for column, levels in (categorical or {}).items():
        for level in levels:
            columns.append((df[column].to_numpy() == level).astype(np.float32))
            names.append(f"{column}={level}")
    return np.column_stack(columns), names


def levels_except(df, column, reference):
    return [level for level in sorted(df[column].unique()) if level != reference]


# ---------------------------------------------------------------------------
# RQ1: exposure and struggle
# ---------------------------------------------------------------------------

def rq1_exposure(a, problems):
    per_student = pd.crosstab(a["student"], a["practice"]).reindex(columns=PRACTICES, fill_value=0)
    rows = []
    for practice in PRACTICES:
        sub = a[a["practice"] == practice]
        rows.append({
            "practice": practice,
            "problems": int((problems["practice"] == practice).sum()),
            "attempts": len(sub),
            "share_of_attempts_pct": 100 * len(sub) / len(a),
            "students_ever_pct": 100 * (per_student[practice] > 0).mean(),
            "per_student_p10": per_student[practice].quantile(0.1),
            "per_student_median": per_student[practice].median(),
            "per_student_p90": per_student[practice].quantile(0.9),
            "correct_pct": 100 * sub["y"].mean() if len(sub) else np.nan,
            "hint_pct": 100 * sub["hint"].mean() if len(sub) else np.nan,
            "answer_revealed_pct": 100 * sub["answer"].mean() if len(sub) else np.nan,
            "mc_2_options_pct": 100 * (sub["format"] == "MC 2 options").mean() if len(sub) else np.nan,
            "in_models": (problems["practice"] == practice).sum() >= MIN_PROBLEMS,
        })
    by_format = a.pivot_table(index="practice", columns="format", values="y", aggfunc=["mean", "size"])
    return pd.DataFrame(rows), by_format


def rq1_difficulty(a, practices):
    """Practice gaps against Procedural: raw, and adjusted for format, grade, domain, time of
    year (the problem's usual position in the course) and student ability."""
    sub = a[a["practice"].isin(practices)]
    others = [p for p in practices if p != REFERENCE]
    categorical = {"practice": others, "format": FORMATS[1:],
                   "grade": levels_except(sub, "grade", "6"),
                   "domain": levels_except(sub, "domain", sub["domain"].mode()[0])}
    X, names = design(sub, ["ability_logit", "item_position", "item_position_sq"], categorical)
    dummy_cols = [names.index(f"practice={p}") for p in others]
    clusters = (sub["student"].to_numpy(), sub["prob"].to_numpy())
    rows = []
    for outcome in ("y", "hint", "answer"):
        model = fit_logit(X, sub[outcome], names, clusters)
        reference_rate = sub.loc[sub["practice"] == REFERENCE, outcome].mean()
        for practice in others:
            gap = marginal_gap(model, X, dummy_cols, names.index(f"practice={practice}"))
            raw = 100 * (sub.loc[sub["practice"] == practice, outcome].mean() - reference_rate)
            rows.append({"outcome": {"y": "correct", "hint": "hint used", "answer": "answer revealed"}[outcome],
                         "practice": practice, "raw_gap_pp": raw,
                         "adjusted_gap_pp": gap[0], "adjusted_low": gap[1], "adjusted_high": gap[2]})
    return pd.DataFrame(rows)


def rq1_learning(a, practices):
    """Practice-specific learning: slope of success on log(1 + earlier encounters of the
    practice), beyond item difficulty, prior accuracy and general progress."""
    sub = a[a["practice"].isin(practices)].copy()
    sub["log_prior_total"] = np.log1p(sub["prior_total"])
    slopes = []
    for practice in practices:
        column = f"slope_{practice}"
        sub[column] = np.where(sub["practice"] == practice, np.log1p(sub[f"prior_{practice}"]), 0.0)
        slopes.append(column)
    others = [p for p in practices if p != REFERENCE]
    X, names = design(sub, ["item_logit", "prior_acc_logit", "log_prior_total"] + slopes, {"practice": others})
    model = fit_logit(X, sub["y"], names, (sub["student"].to_numpy(), sub["prob"].to_numpy()))
    eta = X.astype(np.float64) @ np.nan_to_num(model["beta"])

    rows = []
    for practice in practices:
        b, low, high = coef(model, f"slope_{practice}")
        rows_p = (sub["practice"] == practice).to_numpy()
        base = eta[rows_p] - b * sub.loc[rows_p, f"slope_{practice}"].to_numpy()
        # Earlier encounters with the practice at the time of its attempts: 10th and 90th percentile
        before = sub.loc[rows_p, f"prior_{practice}"]
        p10, p90 = before.quantile(0.1), before.quantile(0.9)

        def change(g, start, end):  # percentage points, averaged over this practice's attempts
            return 100 * np.mean(expit(base + g * np.log1p(end)) - expit(base + g * np.log1p(start)))

        rows.append({"practice": practice, "slope": b, "slope_low": low, "slope_high": high,
                     "pp_1st_to_5th_encounter": change(b, 0, 4),  # 0 before the 1st, 4 before the 5th
                     "pp_low": change(low, 0, 4), "pp_high": change(high, 0, 4),
                     "encounters_before_p10": p10, "encounters_before_p90": p90,
                     "pp_p10_to_p90": change(b, p10, p90),
                     "pp_p10_to_p90_low": change(low, p10, p90), "pp_p10_to_p90_high": change(high, p10, p90)})
    general = coef(model, "log_prior_total")
    rows.append({"practice": "(any problem: general progress)", "slope": general[0],
                 "slope_low": general[1], "slope_high": general[2]})
    return pd.DataFrame(rows)


def rq1_learning_curves(a, practices):
    """Accuracy relative to the problem's difficulty and the student's ability, by encounter
    number with the practice (1 = first time). Item difficulty is controlled so that the
    curve is not confounded by which problems come early in the course."""
    sub = a[a["practice"].isin(practices)].copy()
    sub["log_prior_total"] = np.log1p(sub["prior_total"])
    X, names = design(sub, ["item_logit", "ability_logit", "log_prior_total"])
    model = fit_logit(X, sub["y"], names)
    sub["resid"] = sub["y"] - predict(model, X)

    rows = []
    for practice in practices:
        pr = sub[sub["practice"] == practice]
        counts = pr["k"].value_counts()
        k_max = int(min(40, max([k for k, c in counts.items() if c >= 300], default=1)))
        for k in range(1, k_max + 1):
            cell = pr[pr["k"] == k]
            deviation = cell["resid"] - cell["resid"].mean()
            se = np.sqrt((deviation.groupby(cell["prob"]).sum() ** 2).sum()) / len(cell)  # clustered by problem
            rows.append({"practice": practice, "encounter": k, "attempts": len(cell),
                         "residual_pp": 100 * cell["resid"].mean(), "se_pp": 100 * se})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# RQ2: transfer across concepts
# ---------------------------------------------------------------------------

def history_cells(a, member, concepts, practices, rng, check_students=2):
    """For every attempt, counts and successes of earlier attempts in cells A-E, plus
    cold-start features (placebo and per-source-practice samples)."""
    n = len(a)
    counts = np.zeros((n, 5), dtype=np.int32)
    successes = np.zeros((n, 5), dtype=np.int32)
    prob = a["prob"].to_numpy()
    y = a["y"].to_numpy().astype(np.float32)
    problem_set = a["problem_set"].to_numpy()
    target_practice = a["practice"].to_numpy()
    source_columns = [PRACTICES.index(p) for p in practices]
    bounds = np.flatnonzero(np.diff(a["student"].to_numpy())) + 1
    starts, ends = np.r_[0, bounds], np.r_[bounds, n]
    cold_rows = []
    tri_cache = {}

    for number, (s, e) in enumerate(zip(starts, ends)):
        m = e - s
        if m not in tri_cache:
            tri_cache[m] = np.tri(m, m, -1, dtype=bool)
        prior = tri_cache[m]
        pm_rows, cm_rows = member[prob[s:e]], concepts[prob[s:e]]
        same_practice = (pm_rows @ pm_rows.T) > 0
        same_concept = (cm_rows @ cm_rows.T) > 0
        same_set = problem_set[s:e, None] == problem_set[None, s:e]
        yy = y[s:e]
        other = prior & ~same_set
        cells = [other & same_practice & same_concept, other & same_practice & ~same_concept,
                 other & ~same_practice & same_concept, other & ~same_practice & ~same_concept,
                 prior & same_set]
        for c, cell in enumerate(cells):
            counts[s:e, c] = cell.sum(axis=1)
            successes[s:e, c] = cell.astype(np.float32) @ yy

        if number < check_students:  # verify the vectorized cells against a plain loop
            check_counts, check_successes = brute_force_cells(pm_rows, cm_rows, problem_set[s:e], yy)
            assert np.array_equal(check_counts, counts[s:e]) and np.array_equal(check_successes, successes[s:e]), \
                "history cells differ from the brute-force check"

        # Cold start: first attempt of the practice in this concept (nothing earlier matches both)
        cold = ~(prior & same_practice & same_concept).any(axis=1)
        cold &= np.isin(target_practice[s:e], practices) & (counts[s:e, 1] >= 3)
        rows = np.flatnonzero(cold)
        if not len(rows):
            continue
        keys = rng.random(m)
        # Equal-size random samples from B (same practice, other concepts) and from D (the
        # placebo: other practices, other concepts), so both predictors are equally noisy
        size = np.minimum(np.minimum(counts[s:e, 1][rows], counts[s:e, 3][rows]), MATCHED_MAX)
        record = {"row": s + rows, "matched_n": size,
                  "b_sample_s": sample_successes(cells[1][rows], keys, size, yy),
                  "placebo_s": sample_successes(cells[3][rows], keys, size, yy)}
        other_concept = other[rows] & ~same_concept[rows]
        for q, column in zip(practices, source_columns):
            mask = other_concept & (pm_rows[:, column] > 0)[None, :]
            record[f"src_{q}"] = sample_successes(mask, keys, np.full(len(rows), MATRIX_SAMPLE), yy)
        cold_rows.append(pd.DataFrame(record))

    cold = pd.concat(cold_rows, ignore_index=True)
    return counts, successes, cold


def sample_successes(mask, keys, sizes, yy):
    """Successes among a random sample of `sizes[i]` problems from each row of `mask`
    (NaN where fewer are available). Keys fix the random order per student."""
    ranked = np.sort(np.where(mask, keys[None, :], np.inf), axis=1)
    idx = np.minimum(sizes, mask.shape[1]) - 1
    threshold = ranked[np.arange(len(sizes)), idx]
    chosen = mask & (keys[None, :] <= threshold[:, None])
    result = (chosen.astype(np.float32) @ yy).astype(float)
    result[~np.isfinite(threshold) | (sizes < 1)] = np.nan
    return result


def brute_force_cells(pm_rows, cm_rows, problem_set, yy):
    m = len(yy)
    counts = np.zeros((m, 5), dtype=np.int32)
    successes = np.zeros((m, 5), dtype=np.int32)
    for i in range(m):
        for j in range(i):
            if problem_set[j] == problem_set[i]:
                c = 4
            else:
                practice_match = float(pm_rows[i] @ pm_rows[j]) > 0
                concept_match = float(cm_rows[i] @ cm_rows[j]) > 0
                c = {(True, True): 0, (True, False): 1, (False, True): 2, (False, False): 3}[(practice_match, concept_match)]
            counts[i, c] += 1
            successes[i, c] += int(yy[j])
    return counts, successes


def add_cell_features(df, counts, successes, prefix=""):
    for c, cell in enumerate(CELLS):
        n_, s_ = counts[:, c], successes[:, c]
        df[f"{prefix}acc_{cell}"] = np.log((s_ + 1) / (n_ - s_ + 1))
        df[f"{prefix}log_n_{cell}"] = np.log1p(n_)


def rq2_transfer(a, counts, successes, cold, practices, rng):
    sub_mask = a["practice"].isin(practices).to_numpy()
    sub = a.loc[sub_mask, ["student", "prob", "y", "practice", "item_logit"]].copy()
    add_cell_features(sub, counts[sub_mask], successes[sub_mask])
    clusters = (sub["student"].to_numpy(), sub["prob"].to_numpy())
    results = {}

    # 1. All attempts
    numeric = ["item_logit"] + [f"acc_{c}" for c in CELLS] + [f"log_n_{c}" for c in CELLS]
    X, names = design(sub, numeric)
    model = fit_logit(X, sub["y"], names, clusters)
    rows = [{"model": "all attempts", "term": f"accuracy {c}: {CELL_NAMES[c]}", **dict(zip(("estimate", "low", "high"), coef(model, f"acc_{c}")))} for c in CELLS]
    rows.append({"model": "all attempts", "term": "B minus D (transfer beyond general ability)",
                 **dict(zip(("estimate", "low", "high"), contrast(model, "acc_B", "acc_D")))})
    results["all_attempts"] = pd.DataFrame(rows)

    # 2. Cold start: equal-size samples from B and from D (placebo)
    rows_cold = cold["row"].to_numpy()
    cs = a.loc[rows_cold, ["student", "prob", "y", "practice", "item_logit"]].reset_index(drop=True)
    add_cell_features(cs, counts[rows_cold], successes[rows_cold])
    size = cold["matched_n"].to_numpy().astype(float)
    for column, source in (("acc_B_matched", "b_sample_s"), ("acc_placebo", "placebo_s")):
        s_ = cold[source].to_numpy()
        cs[column] = np.log((s_ + 1) / (size - s_ + 1))
    cs["log_n_matched"] = np.log(size.clip(min=1))
    for q in practices:
        cs[f"src_{q}"] = np.log((cold[f"src_{q}"].to_numpy() + 1) / (MATRIX_SAMPLE - cold[f"src_{q}"].to_numpy() + 1))
    usable = (size >= 3) & np.isfinite(cs["acc_B_matched"]) & np.isfinite(cs["acc_placebo"])
    cs = cs[usable].reset_index(drop=True)
    cs_clusters = (cs["student"].to_numpy(), cs["prob"].to_numpy())

    fair = ["item_logit", "acc_B_matched", "acc_placebo", "acc_C", "acc_E", "log_n_matched", "log_n_C", "log_n_E"]
    full = ["item_logit", "acc_B", "acc_C", "acc_D", "acc_E", "log_n_B", "log_n_C", "log_n_D", "log_n_E"]

    def cold_start_row(label, part, clusters):
        X, names = design(part, fair)
        m_fair = fit_logit(X, part["y"], names, clusters)
        X, names = design(part, full)
        m_full = fit_logit(X, part["y"], names, clusters)
        return {"practice": label, "targets": len(part),
                "B_estimate": coef(m_fair, "acc_B_matched")[0], "placebo_estimate": coef(m_fair, "acc_placebo")[0],
                **dict(zip(("B_minus_placebo", "low", "high"), contrast(m_fair, "acc_B_matched", "acc_placebo"))),
                **dict(zip(("B_beyond_all_of_D", "B_beyond_low", "B_beyond_high"), coef(m_full, "acc_B")))}

    rows = [cold_start_row("all", cs, cs_clusters)]
    for practice in practices:
        part = cs[cs["practice"] == practice]
        rows.append(cold_start_row(practice, part, (part["student"].to_numpy(), part["prob"].to_numpy())))
    results["cold_start"] = pd.DataFrame(rows)

    # Figure data: residual success by general-ability decile, strong vs weak at the practice elsewhere
    cs["expected"] = expit(cs["item_logit"])
    cs["ability_decile"] = pd.qcut(cs["acc_D"].rank(method="first"), 10, labels=False) + 1
    cs["strong_elsewhere"] = cs.groupby(["practice", "ability_decile"])["acc_B"].transform(
        lambda x: x > x.median())
    results["cold_start_curves"] = (cs.assign(residual_pp=100 * (cs["y"] - cs["expected"]))
                                    .groupby(["practice", "ability_decile", "strong_elsewhere"])["residual_pp"]
                                    .agg(["mean", "size"]).reset_index())

    # 3. Source -> target matrix (3 problems per source practice, other concepts)
    sources = [f"src_{q}" for q in practices]
    rows, diagonal = [], []
    for target in practices:
        part = cs[(cs["practice"] == target) & cs[sources].notna().all(axis=1)]
        X, names = design(part, ["item_logit"] + sources + ["acc_C", "log_n_C"])
        m = fit_logit(X, part["y"], names, (part["student"].to_numpy(), part["prob"].to_numpy()))
        for q in practices:
            b, low, high = coef(m, f"src_{q}")
            rows.append({"target": target, "source": q, "estimate": b, "low": low, "high": high, "targets": len(part)})
        # Own practice's history vs the average of the other practices' histories (same sample size)
        weights = {f"src_{q}": (1.0 if q == target else -1.0 / (len(practices) - 1)) for q in practices}
        diagonal.append({"target": target, "targets": len(part),
                         **dict(zip(("own_minus_others", "low", "high"), contrast(m, weights=weights)))})
    results["matrix"] = pd.DataFrame(rows)
    results["matrix_diagonal"] = pd.DataFrame(diagonal)

    # 4. Predictive value of same-practice history (held-out students)
    union = lambda cols: (counts[sub_mask][:, cols].sum(axis=1), successes[sub_mask][:, cols].sum(axis=1))
    for name, cols in (("all", [0, 1, 2, 3, 4]), ("concept", [0, 2]), ("practice", [0, 1])):
        n_, s_ = union(cols)
        sub[f"u_acc_{name}"] = np.log((s_ + 1) / (n_ - s_ + 1))
        sub[f"u_log_n_{name}"] = np.log1p(n_)
    base = ["item_logit", "u_acc_all", "u_log_n_all", "u_acc_concept", "u_log_n_concept", "acc_E", "log_n_E"]
    with_practice = base + ["u_acc_practice", "u_log_n_practice"]
    students = sub["student"].unique()
    test_students = rng.choice(students, size=len(students) // 5, replace=False)
    test = sub["student"].isin(test_students).to_numpy()
    from sklearn.metrics import log_loss, roc_auc_score
    rows = []
    scores = {}
    for label, features in (("baseline (difficulty, overall and same-concept history)", base),
                            ("baseline + same-practice history", with_practice)):
        X, names = design(sub, features)
        m = fit_logit(X[~test], sub["y"].to_numpy()[~test], names)
        p = predict(m, X[test])
        scores[label] = p
        rows.append({"model": label, "test_auc": roc_auc_score(sub["y"].to_numpy()[test], p),
                     "test_log_loss": log_loss(sub["y"].to_numpy()[test], p)})
    # Bootstrap over test students for the AUC difference
    y_test = sub["y"].to_numpy()[test]
    test_student = sub["student"].to_numpy()[test]
    base_p, prac_p = scores.values()
    diffs = []
    uniq = np.unique(test_student)
    pos = {s: i for i, s in enumerate(uniq)}
    idx_by = np.array([pos[s] for s in test_student])
    for _ in range(50):
        w = rng.poisson(1.0, len(uniq))[idx_by]
        keep = w > 0
        rep = np.repeat(np.flatnonzero(keep), w[keep])
        diffs.append(roc_auc_score(y_test[rep], prac_p[rep]) - roc_auc_score(y_test[rep], base_p[rep]))
    rows.append({"model": "difference (AUC gain)", "test_auc": rows[1]["test_auc"] - rows[0]["test_auc"],
                 "test_log_loss": rows[1]["test_log_loss"] - rows[0]["test_log_loss"],
                 "auc_gain_low": np.percentile(diffs, 2.5), "auc_gain_high": np.percentile(diffs, 97.5)})
    results["predictive"] = pd.DataFrame(rows)
    return results


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def setup_matplotlib():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Segoe UI", "Helvetica", "Arial", "DejaVu Sans"],
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.labelcolor": INK_2, "text.color": INK,
        "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID,
        "grid.linewidth": 0.8, "grid.linestyle": "-", "axes.spines.top": False, "axes.spines.right": False,
        "legend.frameon": False, "font.size": 10,
    })
    return plt


def figure_gaps(plt, difficulty, exposure, path):
    """Per practice: raw and adjusted gap in first-try correctness against Procedural."""
    correct = difficulty[difficulty["outcome"] == "correct"].set_index("practice")
    share = exposure.set_index("practice")["share_of_attempts_pct"]
    practices = list(correct.index)
    fig, ax = plt.subplots(figsize=(7.5, 1.3 + 0.75 * len(practices)))
    for i, practice in enumerate(practices):
        row = correct.loc[practice]
        ax.plot(row["raw_gap_pp"], i - 0.12, "o", mfc=SURFACE, mec=MUTED, mew=1.6, ms=7,
                label="Raw gap" if i == 0 else None)
        ax.errorbar(row["adjusted_gap_pp"], i + 0.12, xerr=[[row["adjusted_gap_pp"] - row["adjusted_low"]],
                    [row["adjusted_high"] - row["adjusted_gap_pp"]]], fmt="o", color=INK_2, ms=7,
                    elinewidth=1.5, capsize=0,
                    label="Adjusted: same format, grade, domain, time of year, student ability" if i == 0 else None)
    ax.axvline(0, color=AXIS, lw=1)
    ax.set_yticks(range(len(practices)))
    ax.set_yticklabels([f"{p}  ({share[p]:.1f}% of attempts)" for p in practices], color=INK_2)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Correct on first try vs Procedural Fluency (percentage points)")
    ax.set_title("RQ1: How much harder is each practice than Procedural?", loc="left", color=INK, fontsize=11)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=2, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def figure_curves(plt, curves, path):
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for practice, part in curves.groupby("practice", sort=False):
        color = PRACTICE_COLORS.get(practice, MUTED)
        ax.plot(part["encounter"], part["residual_pp"], color=color, lw=2, solid_capstyle="round", label=practice)
        ax.fill_between(part["encounter"], part["residual_pp"] - 1.96 * part["se_pp"],
                        part["residual_pp"] + 1.96 * part["se_pp"], color=color, alpha=0.10, lw=0)
    # No end labels: the lines converge near 0, so labels would collide; the legend and
    # rq1_learning_curves.csv identify the series
    ax.axhline(0, color=AXIS, lw=1)
    ax.set_xlabel("Encounter number with the practice (1 = first time)")
    ax.set_ylabel("Accuracy vs problem difficulty and ability (pp)")
    ax.set_title("RQ1: Does meeting a practice more often help with it?", loc="left", color=INK, fontsize=11)
    ax.legend(loc="lower right", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def figure_cold_start(plt, curves, practices, path):
    fig, axes = plt.subplots(1, len(practices), figsize=(3.0 * len(practices), 3.4), sharey=True)
    for ax, practice in zip(np.atleast_1d(axes), practices):
        part = curves[curves["practice"] == practice]
        for strong, color, label in ((True, PRACTICE_COLORS.get(practice, INK_2), "Strong at it elsewhere"),
                                     (False, MUTED, "Weak at it elsewhere")):
            line = part[part["strong_elsewhere"] == strong]
            ax.plot(line["ability_decile"], line["mean"], color=color, lw=2, marker="o", ms=4, label=label)
        ax.axhline(0, color=AXIS, lw=1)
        ax.set_title(practice, loc="left", color=INK, fontsize=10)
        ax.set_xlabel("General ability decile")
        ax.set_xticks([1, 5, 10])
        ax.legend(loc="upper left", fontsize=7.5)
    np.atleast_1d(axes)[0].set_ylabel("First try in a new concept, vs expectation (pp)")
    fig.suptitle("RQ2: First attempt of a practice in a new concept", x=0.01, ha="left", color=INK, fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def figure_transfer(plt, cold_start, path):
    fig, ax = plt.subplots(figsize=(7.5, 0.9 + 0.7 * len(cold_start)))
    for i, row in cold_start.reset_index(drop=True).iterrows():
        color = PRACTICE_COLORS.get(row["practice"], INK_2)
        ax.errorbar(row["B_minus_placebo"], i, xerr=[[row["B_minus_placebo"] - row["low"]],
                    [row["high"] - row["B_minus_placebo"]]], fmt="o", color=color, ms=7, elinewidth=1.5, capsize=0)
    ax.axvline(0, color=AXIS, lw=1)
    ax.set_yticks(range(len(cold_start)))
    ax.set_yticklabels([f"{p} (n={n:,})" for p, n in zip(cold_start["practice"], cold_start["targets"])], color=INK_2)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Extra predictive weight of same-practice history vs an equally large placebo (log-odds)")
    ax.set_title("RQ2: Does being good at a practice elsewhere help in a new concept?", loc="left", color=INK, fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def figure_matrix(plt, matrix, practices, path):
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
    table = matrix.pivot(index="target", columns="source", values="estimate").reindex(index=practices, columns=practices)
    limit = max(np.nanmax(np.abs(table.values)), 1e-6)
    cmap = LinearSegmentedColormap.from_list("div", ["#e34948", "#f0efec", "#2a78d6"])
    norm = TwoSlopeNorm(0, -limit, limit)
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    image = ax.imshow(table.values, cmap=cmap, norm=norm)
    for i in range(len(practices)):
        for j in range(len(practices)):
            value = table.values[i, j]
            # Ink or white, whichever contrasts more with this cell's fill (WCAG contrast ratio)
            r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in cmap(norm(value))[:3]]
            luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
            ink_contrast = (luminance + 0.05) / (0.0033 + 0.05)  # INK #0b0b0b has luminance ~0.0033
            white_contrast = 1.05 / (luminance + 0.05)
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=9,
                    color="white" if white_contrast > ink_contrast else INK)
    ax.set_xticks(range(len(practices)), practices, rotation=20, color=INK_2)
    ax.set_yticks(range(len(practices)), practices, color=INK_2)
    ax.grid(False)
    ax.set_xlabel("Source: accuracy on this practice in other concepts (3 problems)")
    ax.set_ylabel("Target: first attempt in a new concept")
    ax.set_title("RQ2: Which practice's history predicts which?", loc="left", color=INK, fontsize=11)
    fig.colorbar(image, ax=ax, shrink=0.8, label="log-odds per logit of accuracy")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def fmt_ci(estimate, low, high, digits=1, unit=""):
    return f"{estimate:+.{digits}f}{unit} (95% CI {low:+.{digits}f} to {high:+.{digits}f})"


def markdown(df, digits=2):
    df = df.copy()
    for column in df.columns:
        if pd.api.types.is_float_dtype(df[column]):
            df[column] = df[column].map(lambda v: "" if pd.isna(v) else f"{v:.{digits}f}")
    header = "| " + " | ".join(map(str, df.columns)) + " |"
    lines = [header, "|" + "|".join("---" for _ in df.columns) + "|"]
    lines += ["| " + " | ".join(map(str, row)) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines)


def rq1_verdicts(exposure, difficulty, learning):
    """One line per practice: is it harder, and can rarity explain it?"""
    correct = difficulty[difficulty["outcome"] == "correct"].set_index("practice")
    learning = learning.set_index("practice")
    share = exposure.set_index("practice")["share_of_attempts_pct"]
    lines = []
    for practice in correct.index:
        adj, s = correct.loc[practice], learning.loc[practice]
        harder, easier, helps = adj["adjusted_high"] < 0, adj["adjusted_low"] > 0, s["slope_low"] > 0
        gap = adj["adjusted_gap_pp"]
        dose = (f"{s['pp_p10_to_p90']:+.1f} pp going from {s['encounters_before_p10']:.0f} to "
                f"{s['encounters_before_p90']:.0f} earlier encounters, the 10th to 90th percentile")
        text = (f"- **{practice}** ({share[practice]:.1f}% of attempts): adjusted gap "
                f"{fmt_ci(gap, adj['adjusted_low'], adj['adjusted_high'], unit=' pp')}. ")
        if harder and helps and s["pp_p10_to_p90"] >= abs(gap):
            text += f"Harder, and **rarity could explain it**: more encounters help ({dose}), as much as the gap."
        elif harder and helps:
            text += (f"Harder, and **rarity explains only part of it** (at most about "
                     f"{100 * s['pp_p10_to_p90'] / abs(gap):.0f}%): more encounters help ({dose}), "
                     f"less than the {abs(gap):.1f} pp gap.")
        elif harder:
            text += (f"Harder, and **not because of rarity**: on the same problem, students who had met this practice "
                     f"more often did not do better ({dose}; slope CI includes 0).")
        elif easier:
            text += "Easier than Procedural despite being met less often."
        else:
            text += f"**Not clearly harder** than Procedural, although it is met less often ({dose})."
        lines.append(text)
    return "\n".join(lines)


def rq2_verdicts(t):
    """Answer to RQ2 from the fair (equal-size) tests, then per practice, then practical value."""
    overall = t["cold_start"].iloc[0]
    per_practice = t["cold_start"].iloc[1:].set_index("practice")
    diagonal = t["matrix_diagonal"].set_index("target")
    all_attempts = t["all_attempts"].set_index("term")
    b_minus_d = all_attempts.loc["B minus D (transfer beyond general ability)"]
    gain = t["predictive"].iloc[-1]

    lines = []
    if overall["low"] > 0:
        lines.append(f"- **Yes, overall**: on the first attempt of a practice in a new concept, same-practice history from "
                     f"other concepts predicts success better than an equally large sample of other-practice history "
                     f"({fmt_ci(overall['B_minus_placebo'], overall['low'], overall['high'], digits=3)} log-odds).")
    else:
        lines.append(f"- **Not in general**: being good at a practice in other concepts predicts the first attempt in a new "
                     f"concept (coefficient {overall['B_beyond_all_of_D']:.2f} even beyond general ability), but an equally "
                     f"large sample of *other*-practice history predicts about as well "
                     f"({fmt_ci(overall['B_minus_placebo'], overall['low'], overall['high'], digits=3)} log-odds). So it "
                     f"mostly reflects being a strong student, not a skill in that practice.")
    lines.append(f"- Over all attempts, same-practice history in other concepts is slightly more predictive than other-practice "
                 f"history ({fmt_ci(b_minus_d['estimate'], b_minus_d['low'], b_minus_d['high'], digits=3)} log-odds), "
                 f"but this comparison does not equalize sample sizes.")
    for practice in per_practice.index:
        cold, diag = per_practice.loc[practice], diagonal.loc[practice]
        evidence = []
        if cold["low"] > 0:
            evidence.append("cold-start test")
        if diag["low"] > 0:
            evidence.append("source-target matrix")
        text = (f"- **{practice}**: cold start {fmt_ci(cold['B_minus_placebo'], cold['low'], cold['high'], digits=3)}; "
                f"own practice vs others in the matrix {fmt_ci(diag['own_minus_others'], diag['low'], diag['high'], digits=3)}. ")
        text += (f"**Practice-specific transfer** ({' and '.join(evidence)})." if evidence
                 else "No practice-specific transfer beyond general ability.")
        lines.append(text)
    lines.append(f"- **Practical value**: adding same-practice history to a knowledge-tracing model changes held-out AUC by "
                 f"{fmt_ci(gain['test_auc'], gain['auc_gain_low'], gain['auc_gain_high'], digits=4)}.")
    return "\n".join(lines)


def write_report(out_dir, args, parts):
    lines = [f"# Mathematical practices: exploration report", "",
             f"Students: {parts['n_students']:,}; attempts: {parts['n_attempts']:,}; concept level: {args.concept}; "
             f"labels: {'confident only' if args.confident_labels else 'all (top practice, ties listed)'}.",
             f"Practices in the models (at least {MIN_PROBLEMS} problems): {', '.join(parts['practices'])}. "
             "Struggle = not correct on the first try without help (`discrete_score` 0).", ""]
    if "exposure" in parts:
        exposure = parts["exposure"]
        lines += ["## RQ1: Do students struggle more with practices they meet less often?", "",
                  "### 1. Exposure", "",
                  markdown(exposure[["practice", "problems", "share_of_attempts_pct", "students_ever_pct",
                                     "per_student_median", "correct_pct", "hint_pct", "mc_2_options_pct"]], 1), "",
                  "### 2. Difficulty on equal footing (gap vs Procedural, percentage points)", "",
                  "Adjusted = average marginal effect from a logistic model with answer format (two-option multiple "
                  "choice is 50% guessable), grade, domain, time of year (the problem's usual position in the course) and "
                  "student ability; 95% intervals clustered by student and problem. Raw and adjusted gaps can differ in "
                  "sign when a practice comes mostly in an easy format (Simpson's paradox).", "",
                  markdown(parts["difficulty"], 1), "",
                  "![gaps](rq1_practice_gaps.png)", "",
                  "### 3. Is it because of rarity?", "",
                  "If rarity caused the struggle, students who had met a practice more often would do better on the *same* "
                  "problem. `slope` is the effect of log(1 + earlier encounters with the practice) on success, controlling "
                  "for the problem's difficulty, the student's prior accuracy and their overall progress. It is converted to "
                  "percentage points for the 1st vs 5th encounter and for the 10th vs 90th percentile of earlier "
                  "encounters actually seen for that practice (no extrapolation).", "",
                  markdown(parts["learning"], 3), "",
                  "![curves](rq1_learning_curves.png)", "",
                  "### Answer to RQ1", "", rq1_verdicts(parts["exposure"], parts["difficulty"], parts["learning"]), ""]
    if "transfer" in parts:
        t = parts["transfer"]
        lines += ["## RQ2: Does mastery of a practice transfer across concepts?", "",
                  "Earlier attempts are split into A same practice + same concept, B same practice + other concept, "
                  "C other practice + same concept, D other practice + other concept, E earlier part of the same problem.", "",
                  "### 1. All attempts (log-odds per logit of smoothed accuracy)", "", markdown(t["all_attempts"], 3), "",
                  "### 2. Cold start: first attempt of a practice in a new concept", "",
                  f"`B_minus_placebo` compares two equal-size random samples (up to {MATCHED_MAX} problems) from the "
                  "student's history: same practice in other concepts (B) versus other practices in other concepts (D, "
                  "the placebo). Equal sizes mean equal measurement noise, so a positive difference means the practice "
                  "itself carries over. `B_beyond_all_of_D` is the coefficient of all same-practice history when all of D "
                  "(general ability) is controlled.", "",
                  markdown(t["cold_start"], 3), "", "![transfer](rq2_transfer.png)", "",
                  "The next figure shows the raw association behind `B_beyond_all_of_D`: within each general-ability decile, "
                  "students who were strong at the practice in other concepts do better on its first attempt in a new "
                  "concept. On its own this does not show a *practice-specific* skill. The equal-size placebo test above "
                  "asks whether other-practice history of the same size predicts just as well.", "",
                  "![cold start](rq2_cold_start.png)", "",
                  "### 3. Source -> target matrix", "",
                  f"Each target practice's first attempt in a new concept, predicted from {MATRIX_SAMPLE} random problems of "
                  "each source practice in other concepts (equal sizes, so the entries are comparable). "
                  "`own_minus_others` tests the diagonal: the target's own practice minus the average of the others.", "",
                  markdown(t["matrix"], 3), "", markdown(t["matrix_diagonal"], 3), "",
                  "![matrix](rq2_transfer_matrix.png)", "",
                  "### 4. Predictive value for knowledge tracing (held-out students)", "", markdown(t["predictive"], 4), "",
                  "### Answer to RQ2", "", rq2_verdicts(t), ""]
    lines += ["## Limitations", "",
              "- Practice labels come from an LLM (Qwen3-30B), not from expert raters; rerun with `--confident-labels` to "
              "check the results on problems with a clear top practice.",
              "- Observational data: teachers choose assignments, so exposure is not randomized. The models compare "
              "equally able students on the same problems, but unmeasured differences (e.g. classes) can remain.",
              "- `discrete_score` counts hint use as a failure; hint and answer outcomes are reported separately.",
              f"- Practices with fewer than {MIN_PROBLEMS} problems (Modeling, Collaborative) are only described.", ""]
    with open(os.path.join(out_dir, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ---------------------------------------------------------------------------
# Self-test and main
# ---------------------------------------------------------------------------

def self_test():
    """fit_logit recovers known coefficients and matches sklearn without regularization."""
    from sklearn.linear_model import LogisticRegression
    rng = np.random.default_rng(0)
    n, students, items = 200_000, 2_000, 400
    student = rng.integers(0, students, n)
    item = rng.integers(0, items, n)
    x = rng.normal(size=(n, 3))
    true = np.array([-0.3, 0.8, -0.5, 0.2])
    eta = true[0] + x @ true[1:] + rng.normal(0, 0.5, students)[student] + rng.normal(0, 0.5, items)[item]
    y = (rng.random(n) < expit(eta)).astype(float)
    X = np.column_stack([np.ones(n), x])
    model = fit_logit(X, y, ["intercept", "x1", "x2", "x3"], (student, item))
    reference = LogisticRegression(penalty=None, tol=1e-10, max_iter=1000).fit(x, y)
    ours = model["beta"]
    theirs = np.r_[reference.intercept_, reference.coef_[0]]
    print("fit_logit:", np.round(ours, 4), "sklearn:", np.round(theirs, 4), "SE:", np.round(model["se"], 4))
    assert np.allclose(ours, theirs, atol=1e-3), "fit_logit disagrees with sklearn"
    # Random effects attenuate the marginal coefficients; the signs and rough sizes must match
    assert np.all(np.sign(ours[1:]) == np.sign(true[1:])), "fit_logit got a sign wrong"
    assert np.all(model["se"] > 0), "non-positive standard error"
    print("Self-test passed.")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rq", nargs="+", type=int, choices=[1, 2], default=[1, 2], help="Research questions to run")
    parser.add_argument("--students", choices=["all", "paper"], default="all",
                        help="all 5,000 students (default) or only the paper's 500")
    parser.add_argument("--user-ids-file", default=None, help="Only the students in this file")
    parser.add_argument("--concept", choices=["domain", "standard"], default="domain",
                        help="Concept = Common Core domain (default) or full standard code")
    parser.add_argument("--confident-labels", action="store_true",
                        help="Only problems whose top practice scores >= 0.7 and >= 0.2 above the next")
    parser.add_argument("--out-dir", default=None, help="Output folder (default: Results/exploration[_variant])")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-plots", action="store_true")
    parser.add_argument("--self-test", action="store_true", help="Check the statistics code and exit")
    args = parser.parse_args()
    if args.out_dir is None:
        suffix = ("_paper" if args.students == "paper" else "") \
            + (f"_{os.path.splitext(os.path.basename(args.user_ids_file))[0]}" if args.user_ids_file else "") \
            + ("_standard" if args.concept == "standard" else "") + ("_confident" if args.confident_labels else "")
        args.out_dir = os.path.join(B.REPO_DIR, "Results", "exploration" + suffix)
    return args


def main():
    args = parse_args()
    if args.self_test:
        self_test()
        return
    started = time.time()
    rng = np.random.default_rng(args.seed)
    os.makedirs(args.out_dir, exist_ok=True)

    print("Loading data ...")
    problems, member, concepts = load_problems(args)
    a = load_attempts(args, problems, member)
    practices = inferential_practices(problems)
    print(f"  {a['student'].nunique():,} students, {len(a):,} attempts, {len(problems):,} problems; "
          f"practices in the models: {', '.join(practices)}")
    parts = {"n_students": a["student"].nunique(), "n_attempts": len(a), "practices": practices}
    plt = None if args.no_plots else setup_matplotlib()

    if 1 in args.rq:
        print("RQ1: exposure ...")
        exposure, by_format = rq1_exposure(a, problems)
        exposure.to_csv(os.path.join(args.out_dir, "rq1_exposure.csv"), index=False)
        by_format.to_csv(os.path.join(args.out_dir, "rq1_correct_by_format.csv"))
        print("RQ1: difficulty on equal footing ...")
        difficulty = rq1_difficulty(a, practices)
        difficulty.to_csv(os.path.join(args.out_dir, "rq1_adjusted_difficulty.csv"), index=False)
        print("RQ1: practice-specific learning ...")
        learning = rq1_learning(a, practices)
        learning.to_csv(os.path.join(args.out_dir, "rq1_learning_rates.csv"), index=False)
        print("RQ1: learning curves ...")
        curves = rq1_learning_curves(a, practices)
        curves.to_csv(os.path.join(args.out_dir, "rq1_learning_curves.csv"), index=False)
        parts.update(exposure=exposure, difficulty=difficulty, learning=learning)
        if plt:
            figure_gaps(plt, difficulty, exposure, os.path.join(args.out_dir, "rq1_practice_gaps.png"))
            figure_curves(plt, curves, os.path.join(args.out_dir, "rq1_learning_curves.png"))

    if 2 in args.rq:
        print("RQ2: splitting each student's history into cells A-E ...")
        counts, successes, cold = history_cells(a, member, concepts, practices, rng)
        print(f"  {len(cold):,} cold-start targets with at least 3 same-practice problems in other concepts")
        print("RQ2: transfer models ...")
        transfer = rq2_transfer(a, counts, successes, cold, practices, rng)
        transfer["all_attempts"].to_csv(os.path.join(args.out_dir, "rq2_transfer_model.csv"), index=False)
        transfer["cold_start"].to_csv(os.path.join(args.out_dir, "rq2_cold_start.csv"), index=False)
        transfer["cold_start_curves"].to_csv(os.path.join(args.out_dir, "rq2_cold_start_curves.csv"), index=False)
        transfer["matrix"].to_csv(os.path.join(args.out_dir, "rq2_transfer_matrix.csv"), index=False)
        transfer["matrix_diagonal"].to_csv(os.path.join(args.out_dir, "rq2_transfer_matrix_diagonal.csv"), index=False)
        transfer["predictive"].to_csv(os.path.join(args.out_dir, "rq2_predictive_value.csv"), index=False)
        parts["transfer"] = transfer
        if plt:
            figure_transfer(plt, transfer["cold_start"], os.path.join(args.out_dir, "rq2_transfer.png"))
            figure_cold_start(plt, transfer["cold_start_curves"], practices, os.path.join(args.out_dir, "rq2_cold_start.png"))
            figure_matrix(plt, transfer["matrix"], practices, os.path.join(args.out_dir, "rq2_transfer_matrix.png"))

    write_report(args.out_dir, args, parts)
    print(f"Done in {time.time() - started:.0f}s. Report: {os.path.join(args.out_dir, 'report.md')}")


if __name__ == "__main__":
    main()
