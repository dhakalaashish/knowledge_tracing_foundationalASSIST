// Analysis of the wrong-answer diagnoses (diagnose.py, prompt 4): which practice steps fail, what kind of error,
// whether the failed step is the problem's top practice, which math facts, and how this varies. Writes one JSON file.
//
// Usage (from the repo root):
//   node Code/practice_analysis/diagnosis_analysis.js [diagnosis csv] [labels prefix] [out.json]
//   defaults: Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv, qwen35_122b_ch3,
//             Results/practice_analysis/qwen35_122b_ch3_diagnosis.json
//
// Each row of the diagnosis CSV is one wrong answer given by at least 3 students on their first attempt. Counts are
// given two ways: by wrong answer (n), and weighted by the number of students who gave it (students). The "failed
// practice" is the first step with status "failed". The top practice comes from <prefix>_top_practice.

const fs = require("fs");
const path = require("path");
const { readTable, canon } = require("../generate_practice_reasoning/tools/csv.js");
const DIAG = process.argv[2] || "Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv";
const PREFIX = process.argv[3] || "qwen35_122b_ch3";
const OUT = process.argv[4] || path.join("Results", "practice_analysis", `${PREFIX}_diagnosis.json`);
const PR = ["Representing", "Abstracting and Generalizing", "Justifying and Proving", "Mathematical Modeling",
    "Collaborative Mathematics", "Procedural Fluency"];
const SH = ["REP", "A&G", "J&P", "MOD", "COL", "PF"];
const ET = ["practice", "math_fact", "guess"];
const ST = ["correct", "failed", "not_reached", "cannot_tell"];

const D = readTable(DIAG), P = readTable("Data/Problems.csv"), S = readTable("Data/Skills.csv");
const text = new Map();
for (const line of fs.readFileSync("Code/generate_practice_reasoning/problems_rendered.jsonl", "utf8").split("\n"))
    if (line.trim()) { const o = JSON.parse(line); text.set(o.row, o.text); }
const codeOf = new Map();
for (const r of S.rows) { const pid = r[0], c = r[2]; if (!pid || !c) continue; if (!codeOf.has(pid) || c < codeOf.get(pid)) codeOf.set(pid, c); }

const g = (r, c) => r[D.h[c]];
const items = D.rows.map(r => {
    const row = Number(g(r, "row")), a = JSON.parse(g(r, "diagnosis_json"));
    const steps = a.steps.map(s => ({ p: PR.indexOf(canon(s.practice)), st: s.status }));
    const firstFail = steps.findIndex(s => s.st === "failed");
    const code = codeOf.get(String(g(r, "problem_id"))) || "";
    return { row, pid: g(r, "problem_id"), type: g(r, "problem_type"), rank: Number(g(r, "rank")), wrong: g(r, "wrong_answer"),
        students: Number(g(r, "students")), share: Number(g(r, "share_of_wrong")), et: g(r, "error_type"),
        failed: firstFail >= 0 ? steps[firstFail].p : -1, failPos: firstFail, steps, k: steps.length,
        nFailed: steps.filter(s => s.st === "failed").length, fact: (g(r, "math_fact") || "").trim(),
        recon: g(r, "reconstruction"), expl: g(r, "explanation"), conf: g(r, "confidence"),
        top: PR.indexOf(canon(P.rows[row - 1][P.h[`${PREFIX}_top_practice`]] || "")),
        domain: code.split(".")[1] || "?", grade: code.split(".")[0] || "?", source: D.h.diagnosed_by !== undefined ? g(r, "diagnosed_by") : "" };
});
const N = items.length, W = items.reduce((s, x) => s + x.students, 0);
const tally = (list, keyFn, keys) => { const o = Object.fromEntries(keys.map(k => [k, { n: 0, students: 0 }]));
    for (const x of list) { const k = keyFn(x); if (o[k]) { o[k].n++; o[k].students += x.students; } } return o; };
const share = (o, tot) => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, { ...v, share_n: v.n / tot.n, share_students: v.students / tot.students }]));
const tot = list => ({ n: list.length, students: list.reduce((s, x) => s + x.students, 0) });
const R = { meta: { file: DIAG, prefix: PREFIX, wrong_answers: N, students: W, problems: new Set(items.map(x => x.row)).size,
    practices: PR, short: SH } };

// J1: kinds of error, overall / by question type / by confidence
R.error_type = share(tally(items, x => x.et, ET), tot(items));
const types = [...new Set(items.map(x => x.type))].sort();
R.error_type_by_type = types.map(t => { const l = items.filter(x => x.type === t); return { type: t, ...tot(l), et: share(tally(l, x => x.et, ET), tot(l)) }; });
R.confidence = share(tally(items, x => x.conf, ["high", "medium", "low"]), tot(items));
R.confidence_by_et = ET.map(e => { const l = items.filter(x => x.et === e); return { et: e, ...tot(l), conf: share(tally(l, x => x.conf, ["high", "medium", "low"]), tot(l)) }; });

// J2: which practice fails (first failed step), and how often each practice fails when it is a step
const withFail = items.filter(x => x.failed >= 0);
R.failed = share(tally(withFail, x => SH[x.failed], SH), tot(withFail));
R.failed_by_et = ["practice", "math_fact"].map(e => { const l = withFail.filter(x => x.et === e); return { et: e, ...tot(l), failed: share(tally(l, x => SH[x.failed], SH), tot(l)) }; });
R.fail_rate = SH.map((p, i) => { const present = items.filter(x => x.steps.some(s => s.p === i));
    const failedAny = present.filter(x => x.steps.some(s => s.p === i && s.st === "failed"));
    return { practice: p, present: present.length, failed: failedAny.length, rate: present.length ? failedAny.length / present.length : null,
        rate_students: present.length ? failedAny.reduce((s, x) => s + x.students, 0) / present.reduce((s, x) => s + x.students, 0) : null }; });
R.n_failed_steps = [0, 1, 2, 3].map(k => { const l = items.filter(x => Math.min(x.nFailed, 3) === k); return { k: k === 3 ? "3+" : String(k), ...tot(l) }; });

// J3: is the failed step the top practice? (observed vs chance if the failed step were any step at random)
const tf = withFail.filter(x => x.top >= 0);
const same = tf.filter(x => x.failed === x.top);
R.failed_is_top = { diagnoses: tf.length, same: same.length, share: same.length / tf.length,
    share_students: same.reduce((s, x) => s + x.students, 0) / tf.reduce((s, x) => s + x.students, 0),
    chance: tf.reduce((s, x) => s + 1 / x.k, 0) / tf.length,
    by_k: [1, 2, 3, 4].map(k => { const l = tf.filter(x => Math.min(x.k, 4) === k); const s2 = l.filter(x => x.failed === x.top);
        return { k: k === 4 ? "4+" : String(k), diagnoses: l.length, share: l.length ? s2.length / l.length : null, chance: k === 4 ? null : 1 / k }; }) };
// among multi-step analyses only (single-step ones are trivially "top")
const multi = tf.filter(x => x.k >= 2), ms = multi.filter(x => x.failed === x.top);
R.failed_is_top.multi_step = { diagnoses: multi.length, share: ms.length / multi.length, chance: multi.reduce((s, x) => s + 1 / x.k, 0) / multi.length };
R.top_vs_failed = SH.map((tp, ti) => ({ top: tp, failed: SH.map((_, fi) => tf.filter(x => x.top === ti && x.failed === fi).length) }));

// J4: where in the solution: position of the first failed step; what the steps before and after it are
R.fail_position = [0, 1, 2, 3].map(p => { const l = withFail.filter(x => Math.min(x.failPos, 3) === p); return { position: p === 3 ? "4th+" : ["1st", "2nd", "3rd"][p], ...tot(l) }; });
const before = tally(withFail.flatMap(x => x.steps.slice(0, x.failPos).map(s => ({ st: s.st, students: x.students }))), s => s.st, ST);
const after = tally(withFail.flatMap(x => x.steps.slice(x.failPos + 1).map(s => ({ st: s.st, students: x.students }))), s => s.st, ST);
R.status_before_failure = before; R.status_after_failure = after;
R.fail_position_by_k = [2, 3].map(k => { const l = withFail.filter(x => x.k === k); return { k, diagnoses: l.length,
    first: l.filter(x => x.failPos === 0).length / (l.length || 1), last: l.filter(x => x.failPos === k - 1).length / (l.length || 1) }; });

// J5: math facts, grouped by keywords (approximate: a fact can match several groups; first match wins)
const FACTS = [
    ["Order of operations", /order of operations|pemdas|precedence/i],
    ["Units, conversions and money (metric, money)", /\b(km|cm|mm|kg|mg|ml)\b|kilomet|centimet|millimet|dollar|cents?\b|penn/i],
    ["Negative numbers and signs", /negative|sign|subtracting a negative|opposite|absolute value|integer/i],
    ["Exponents and roots", /exponent|power|squar|cube|root|\^/i],
    ["Percent", /percent|%/i],
    ["Fractions", /fraction|numerator|denominator|reciprocal|mixed number|improper/i],
    ["Decimals and place value", /decimal|place value|tenths|hundredths|thousandths|powers? of ten|digit/i],
    ["Ratios, rates and proportions", /ratio|rate|proportion|unit price|per\b|constant of proportionality/i],
    ["Area, perimeter, volume, circles", /area|perimeter|volume|surface|circumference|radius|diameter|\bpi\b|π/i],
    ["Angles, shapes and geometry terms", /angle|triangle|polygon|parallel|perpendicular|congruent|similar|scale|degree/i],
    ["Units, conversions and money", /unit|convert|conversion|inch|feet|foot|meter|mile|hour|minute|second|gram|liter|pound|ounce|\b(km|cm|mm|kg|mg|ml)\b|dollar|cent|penn|\$/i],
    ["Algebra terms (variable, coefficient, term, like terms)", /variable|coefficient|like terms|term|expression|equation|distribut|factor|inverse/i],
    ["Statistics and probability terms", /mean|median|mode|range|probab|sample|outcome|frequency|interquartile|mad\b/i],
    ["Number facts and operations", /multipl|divid|division|add|sum|subtract|product|quotient|times table|fact/i],
];
const facts = items.filter(x => x.et === "math_fact");
const factGroup = x => { for (const [name, re] of FACTS) if (re.test(x.fact)) return name; return "Other"; };
const fg = new Map();
for (const x of facts) { const k = factGroup(x); const o = fg.get(k) || { group: k, n: 0, students: 0, examples: [] }; o.n++; o.students += x.students; o.examples.push(x); fg.set(k, o); }
R.math_facts = [...fg.values()].sort((a, b) => b.students - a.students).map(o => ({ group: o.group, n: o.n, students: o.students,
    examples: o.examples.sort((a, b) => b.students - a.students).slice(0, 3).map(x => ({ row: x.row, wrong: x.wrong, students: x.students, fact: x.fact, failed: SH[x.failed] || "", text: (text.get(x.row) || "").replace(/\s+/g, " ").slice(0, 170) })) }));
R.math_facts_total = tot(facts);

// J6: by domain
const doms = [...new Set(items.map(x => x.domain))];
R.by_domain = doms.map(d => { const l = items.filter(x => x.domain === d), lf = l.filter(x => x.failed >= 0);
    return { domain: d, ...tot(l), et: share(tally(l, x => x.et, ET), tot(l)), failed: share(tally(lf, x => SH[x.failed], SH), tot(lf)) }; })
    .sort((a, b) => b.students - a.students);
R.failed_by_type = types.map(t => { const l = withFail.filter(x => x.type === t); return { type: t, ...tot(l), failed: share(tally(l, x => SH[x.failed], SH), tot(l)) }; });

// J7: the most common wrong answer of a problem vs its other wrong answers
R.by_rank = [[1, 1, "most common wrong answer"], [2, 2, "2nd"], [3, 1e9, "3rd and later"]].map(([a, b, label]) => {
    const l = items.filter(x => x.rank >= a && x.rank <= b); return { rank: label, ...tot(l), et: share(tally(l, x => x.et, ET), tot(l)),
        mean_share_of_wrong: l.reduce((s, x) => s + x.share, 0) / (l.length || 1) }; });

// J8 (Q15 redone): per failed practice: kind of error, concentration of the problem's wrong answers, examples
R.by_failed_practice = SH.map((p, i) => { const l = withFail.filter(x => x.failed === i); if (!l.length) return { practice: p, n: 0 };
    const r1 = l.filter(x => x.rank === 1);
    return { practice: p, ...tot(l), et: share(tally(l, x => x.et, ET), tot(l)),
        mean_top_wrong_share: r1.length ? r1.reduce((s, x) => s + x.share, 0) / r1.length : null, top_wrong_answers: r1.length,
        examples: [...l].sort((a, b) => b.students - a.students).slice(0, 4).map(x => ({ row: x.row, type: x.type, wrong: x.wrong, students: x.students,
            et: x.et, recon: x.recon, fact: x.fact, text: (text.get(x.row) || "").replace(/\s+/g, " ").slice(0, 170) })) }; });

// diagnoses whose explanation says the student's answer is in fact correct (a scoring or answer-key issue)
const saysCorrect = /(student'?s?|this|the given|the) (final )?(answer|selection|response|choice)s? (is|are|was|were) (actually |in fact |mathematically |essentially )?(correct|right|equivalent to the correct)\b|(is|are) (actually|in fact) (the )?correct\b|matches the correct (answer|solution|set|options?|value)|is the correct (solution|answer|value)|marked (as )?(incorrect|wrong)|answer key|grading (error|issue)|scor(ing|ed) (error|issue|as (incorrect|wrong))|not (actually|really) (an? )?(wrong|incorrect|error)/i;
const sc = items.filter(x => saysCorrect.test(x.expl) || saysCorrect.test(x.recon));
R.says_correct = { n: sc.length, students: sc.reduce((s, x) => s + x.students, 0),
    by_et: Object.fromEntries(ET.map(e => [e, sc.filter(x => x.et === e).length])),
    examples: sc.sort((a, b) => b.students - a.students).slice(0, 6).map(x => ({ row: x.row, type: x.type, wrong: x.wrong, students: x.students, et: x.et,
        expl: x.expl, text: (text.get(x.row) || "").replace(/\s+/g, " ").slice(0, 150) })) };

// the guesses
R.guesses =items.filter(x => x.et === "guess").sort((a, b) => b.students - a.students).slice(0, 6)
    .map(x => ({ row: x.row, type: x.type, wrong: x.wrong, students: x.students, expl: x.expl, text: (text.get(x.row) || "").replace(/\s+/g, " ").slice(0, 150) }));
R.sources = Object.entries(items.reduce((o, x) => { if (x.source) o[x.source] = (o[x.source] || 0) + 1; return o; }, {})).map(([k, v]) => ({ run: k, n: v }));

fs.writeFileSync(OUT, JSON.stringify(R, null, 1));
console.error(`wrote ${OUT}: ${N} wrong answers, ${W} students`);
