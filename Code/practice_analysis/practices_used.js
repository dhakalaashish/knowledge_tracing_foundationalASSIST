// Practice analysis with ALL the practices a problem needs (the ordered practices_used of a labeling run), not only
// its top practice. Companion to analyze.js (one practice per problem). Writes one JSON file.
//
// Usage (from the repo root, after clean_responses.js):
//   node --max-old-space-size=8000 Code/practice_analysis/practices_used.js [prefix] [out.json]
//   defaults: qwen35_122b_ch3, Results/practice_analysis/qwen35_122b_ch3_used.json
//   prefix: a labeling run's column prefix in Problems.csv (<prefix>_reasoning, <prefix>_top_practice)
//
// Conventions as in analyze.js: responses are the cleaned first attempts (Results/practice_analysis/
// cleaned_responses.tsv, in time order); a problem_id on several rows of Problems.csv uses its first row; problems
// without a label in this run are left out. "Adjusted" = score minus the student's mean score on their other
// responses (removes student ability). "Within type" differences are averaged over question types, weighted by the
// smaller group, so question type does not explain them. Minutes = time since the student's previous answer when
// under 30 minutes (a proxy for time on the problem).

const fs = require("fs");
const path = require("path");
const { readTable, canon, llmOrdering } = require("../generate_practice_reasoning/tools/csv.js");

const ROOT = process.cwd();
const PREFIX = process.argv[2] || "qwen35_122b_ch3";
const OUT = process.argv[3] || path.join(ROOT, "Results", "practice_analysis", `${PREFIX}_used.json`);
const PR = ["Representing", "Abstracting and Generalizing", "Justifying and Proving", "Mathematical Modeling",
    "Collaborative Mathematics", "Procedural Fluency"];
const SH = ["REP", "A&G", "J&P", "MOD", "COL", "PF"];
const NP = 6;
const r3 = x => (x === null || x === undefined || !isFinite(x)) ? null : Math.round(x * 1000) / 1000;
const mean = a => a.length ? a.reduce((s, x) => s + x, 0) / a.length : null;
const median = a => { if (!a.length) return null; const s = Float64Array.from(a).sort(); return s[Math.floor(s.length / 2)]; };

// ---------------------------------------------------------------- problems
const P = readTable(path.join(ROOT, "Data", "Problems.csv"));
const prob = new Map();
let unlabeled = 0;
P.rows.forEach(r => {
    const pid = r[P.h.problem_id].trim(); if (prob.has(pid)) return;
    const raw = (r[P.h[`${PREFIX}_reasoning`]] || "").trim();
    const l = raw ? llmOrdering(raw) : null;
    const order = l ? l.order.map(canon).map(p => PR.indexOf(p)).filter(i => i >= 0) : null;
    if (!order || !order.length) { unlabeled++; prob.set(pid, null); return; }
    prob.set(pid, { pid, order, set: new Set(order), top: PR.indexOf(canon(r[P.h[`${PREFIX}_top_practice`]] || "")),
        type: r[P.h["Problem Type"]] || "?" });
});
const labeled = [...prob.values()].filter(Boolean);

// ---------------------------------------------------------------- responses
const lines = fs.readFileSync(path.join(ROOT, "Results", "practice_analysis", "cleaned_responses.tsv"), "utf8").split("\n");
const resp = []; const stu = new Map(); let leftOut = 0;
for (let i = 1; i < lines.length; i++) {
    const L = lines[i]; if (!L) continue;
    const f = L.split("\t"); const info = prob.get(f[1]);
    if (info === undefined) throw new Error("problem " + f[1] + " is not in Problems.csv");
    if (info === null) { leftOut++; continue; }
    if (!stu.has(f[0])) stu.set(f[0], stu.size);
    resp.push({ s: stu.get(f[0]), info, y: Number(f[2]), hint: Number(f[3]) > 0 ? 1 : 0, saw: Number(f[4]),
        t: Date.parse(f[5].replace(" ", "T").replace(/\+00$/, "Z")) });
}
lines.length = 0;
const NS = stu.size;
// adjusted score: minus the student's mean on their other responses; minutes since the previous answer
const sY = new Float64Array(NS), sN = new Float64Array(NS), last = new Float64Array(NS).fill(NaN);
for (const x of resp) { sY[x.s] += x.y; sN[x.s]++; }
for (const x of resp) {
    x.adj = x.y - (sY[x.s] - x.y) / (sN[x.s] - 1);
    const d = (x.t - last[x.s]) / 60000; x.min = d >= 0 && d < 30 ? d : null; last[x.s] = x.t;
}
const R = { meta: { prefix: PREFIX, practices: PR, short: SH, problems_labeled: labeled.length, problems_unlabeled: unlabeled,
    responses: resp.length, responses_left_out_unlabeled: leftOut, students: NS,
    problems_answered: new Set(resp.map(x => x.info.pid)).size } };
const answered = [...new Set(resp.map(x => x.info))];

// ---------------------------------------------------------------- U1: how many practices a problem needs
const K = 5;  // 1..4, 5 = "5+"
const kOf = info => Math.min(info.order.length, K);
const cnt = arr => { const c = new Array(K + 1).fill(0); arr.forEach(i => c[kOf(i)]++); return c.slice(1); };
const kResp = new Array(K + 1).fill(0); resp.forEach(x => kResp[kOf(x.info)]++);
R.u1 = { labels: ["1", "2", "3", "4", "5+"], problems_all: cnt(labeled), problems_answered: cnt(answered), responses: kResp.slice(1),
    mean_all: r3(mean(labeled.map(i => i.order.length))), mean_responses: r3(mean(resp.map(x => x.info.order.length))) };

// ---------------------------------------------------------------- U2: the most common orderings
const comb = new Map();
for (const i of labeled) { const k = i.order.map(p => SH[p]).join(" > "); const c = comb.get(k) || { ordering: k, problems: 0, responses: 0 }; c.problems++; comb.set(k, c); }
for (const x of resp) comb.get(x.info.order.map(p => SH[p]).join(" > ")).responses++;
R.u2 = { distinct: comb.size, top: [...comb.values()].sort((a, b) => b.problems - a.problems).slice(0, 15) };

// ---------------------------------------------------------------- U3: each practice: how often used, where, and as top
R.u3 = PR.map((_, p) => {
    const used = labeled.filter(i => i.set.has(p));
    const pos = { only: 0, first: 0, middle: 0, last: 0 };
    for (const i of used) { const k = i.order.indexOf(p), n = i.order.length; if (n === 1) pos.only++; else if (k === 0) pos.first++; else if (k === n - 1) pos.last++; else pos.middle++; }
    return { practice: SH[p], problems_used: used.length, share_problems: r3(used.length / labeled.length),
        responses_used: resp.filter(x => x.info.set.has(p)).length,
        share_responses: r3(resp.filter(x => x.info.set.has(p)).length / resp.length),
        top_problems: labeled.filter(i => i.top === p).length,
        top_when_used: r3(used.length ? used.filter(i => i.top === p).length / used.length : null), position: pos };
});

// ---------------------------------------------------------------- U4: which practices appear together (problems)
R.u4 = { together: PR.map((_, a) => PR.map((_, b) => labeled.filter(i => i.set.has(a) && i.set.has(b)).length)) };

// ---------------------------------------------------------------- U5: difficulty and effort by number of practices
const types = [...new Set(resp.map(x => x.info.type))].sort();
R.u5 = { by_k: R.u1.labels.map((lab, j) => {
    const g = resp.filter(x => kOf(x.info) === j + 1); const mins = g.map(x => x.min).filter(v => v !== null);
    return { k: lab, responses: g.length, pct_correct: r3(mean(g.map(x => x.y))), adjusted: r3(mean(g.map(x => x.adj))),
        any_hint: r3(mean(g.map(x => x.hint))), saw_answer: r3(mean(g.map(x => x.saw))), median_minutes: r3(median(mins)) };
}), by_type: types.map(t => ({ type: t, responses: resp.filter(x => x.info.type === t).length,
    adjusted_by_k: R.u1.labels.map((_, j) => { const g = resp.filter(x => x.info.type === t && kOf(x.info) === j + 1); return g.length >= 500 ? r3(mean(g.map(x => x.adj))) : null; }) })) };

// ---------------------------------------------------------------- U6: does needing a practice make a problem harder?
function withinType(pred) {  // adjusted difference present - absent, overall and averaged within question type
    const a = resp.filter(pred), b = resp.filter(x => !pred(x));
    let num = 0, den = 0;
    for (const t of types) {
        const at = a.filter(x => x.info.type === t), bt = b.filter(x => x.info.type === t);
        if (at.length < 200 || bt.length < 200) continue;
        const w = Math.min(at.length, bt.length); num += w * (mean(at.map(x => x.adj)) - mean(bt.map(x => x.adj))); den += w;
    }
    return { responses_with: a.length, pct_correct_with: r3(mean(a.map(x => x.y))), pct_correct_without: r3(mean(b.map(x => x.y))),
        adjusted_diff: r3(mean(a.map(x => x.adj)) - mean(b.map(x => x.adj))), adjusted_diff_within_type: den ? r3(num / den) : null };
}
R.u6 = PR.map((_, p) => ({ practice: SH[p], ...withinType(x => x.info.set.has(p)) }));
// the same, among problems whose top practice is Procedural Fluency: does an extra practice step make them harder?
R.u6_pf_top = PR.map((_, p) => p === 5 ? null : ({ practice: SH[p], ...withinType2(p) }));
function withinType2(p) {
    const base = resp.filter(x => x.info.top === 5);
    const a = base.filter(x => x.info.set.has(p)), b = base.filter(x => !x.info.set.has(p));
    return { responses_with: a.length, responses_without: b.length,
        adjusted_diff: a.length >= 200 && b.length >= 200 ? r3(mean(a.map(x => x.adj)) - mean(b.map(x => x.adj))) : null };
}

// ---------------------------------------------------------------- U7: effort when a practice is needed
R.u7 = PR.map((_, p) => {
    const a = resp.filter(x => x.info.set.has(p)), b = resp.filter(x => !x.info.set.has(p));
    const ma = a.map(x => x.min).filter(v => v !== null), mb = b.map(x => x.min).filter(v => v !== null);
    return { practice: SH[p], responses_with: a.length, any_hint_with: r3(mean(a.map(x => x.hint))), any_hint_without: r3(mean(b.map(x => x.hint))),
        saw_answer_with: r3(mean(a.map(x => x.saw))), saw_answer_without: r3(mean(b.map(x => x.saw))),
        median_minutes_with: r3(median(ma)), median_minutes_without: r3(median(mb)) };
});

// ---------------------------------------------------------------- U8: per student: how much of their work needs each practice
const sw = Array.from({ length: NS }, () => new Float64Array(NP + 1));
for (const x of resp) { for (const p of x.info.set) sw[x.s][p]++; sw[x.s][NP]++; }
R.u8 = PR.map((_, p) => { const sh = sw.map(v => v[p] / v[NP]); const met = sw.filter(v => v[p] > 0).length;
    return { practice: SH[p], students_meeting: met, mean_share_of_work: r3(mean(sh)), min_share: r3(Math.min(...sh)), max_share: r3(Math.max(...sh)) }; });

fs.writeFileSync(OUT, JSON.stringify(R, null, 1));
console.error(`wrote ${OUT}: ${resp.length} responses, ${NS} students, ${labeled.length} labeled problems (${unlabeled} without a label, ${leftOut} of their responses left out)`);
