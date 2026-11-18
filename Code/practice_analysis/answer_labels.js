// Every response labeled with what its answer shows, and analyses of those labels (insights page, Parts K-M).
//
// Each first-attempt response in the cleaned data gets one label:
//   correct | help (wrong after a hint or an answer view) | empty | key (wrong, but equal to a correct answer: a scoring issue)
//   | practice / math_fact / guess (the answer is a diagnosed common wrong answer: given by >= 3 students; step 6)
//   | rare2 (wrong answer given by exactly 2 students) | unique (given by this student only) | undiagnosed (>= 3 students, no diagnosis)
// Wrong answers are matched to the diagnoses with the same normalization as wrong_answers.js.
//
// Usage (from the repo root, after clean_responses.js, wrong_answers.js and diagnose.py):
//   node --max-old-space-size=8000 Code/practice_analysis/answer_labels.js [diagnosis csv] [labels prefix] [out.json]
//   defaults: Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv, qwen35_122b_ch3,
//             Results/practice_analysis/qwen35_122b_ch3_answers.json
//
// Adjusted scores follow analyze.js: residual = score - the problem's leave-one-out mean; adjusted = residual - the
// student's mean residual. "Same skill" = the problem's skill code (the smallest code when it has several).

const fs = require("fs");
const path = require("path");
const { readTable, canon, llmOrdering } = require("../generate_practice_reasoning/tools/csv.js");
const DIAG = process.argv[2] || "Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv";
const PREFIX = process.argv[3] || "qwen35_122b_ch3";
const OUT = process.argv[4] || path.join("Results", "practice_analysis", `${PREFIX}_answers.json`);
const PR = ["Representing", "Abstracting and Generalizing", "Justifying and Proving", "Mathematical Modeling",
    "Collaborative Mathematics", "Procedural Fluency"];
const SH = ["REP", "A&G", "J&P", "MOD", "COL", "PF"];
const PFI = 5, REPI = 0;
const LAB = ["correct", "help", "empty", "key", "practice", "math_fact", "guess", "rare2", "unique", "undiagnosed"];
const L = Object.fromEntries(LAB.map((x, i) => [x, i]));
const WRONG_UNAIDED = [L.key, L.practice, L.math_fact, L.guess, L.rare2, L.unique, L.undiagnosed];
const STATUS = ["correct", "failed", "not_reached", "cannot_tell"];

// ---------- normalization (as in wrong_answers.js)
const MON = { jan: 1, feb: 2, mar: 3, apr: 4, may: 5, jun: 6, jul: 7, aug: 8, sep: 9, oct: 10, nov: 11, dec: 12 };
const norm = a => a.replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&gt;/g, ">").replace(/&lt;/g, "<")
    .replace(/&amp;/g, "&").replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, " ").trim().toLowerCase();
const fixDate = a => a.replace(/\b(\d{1,2})-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b/g, (m, d, mo) => MON[mo] + "/" + d);
function numVal(t) {
    t = t.replace(/,/g, "").replace(/\s+/g, " ").trim();
    let m;
    if ((m = t.match(/^(-?)(\d+) (\d+)\/(\d+)$/))) return (m[1] ? -1 : 1) * (+m[2] + +m[3] / +m[4]);
    if ((m = t.match(/^(-?\d*\.?\d+)\/(-?\d*\.?\d+)$/))) return +m[2] ? +m[1] / +m[2] : null;
    if (/^-?\d*\.?\d+$/.test(t)) return +t;
    return null;
}
const key = a => { const v = numVal(a); return v === null ? "t:" + a.replace(/\s+/g, "") : "n:" + Math.round(v * 1e9) / 1e9; };

// math-fact groups (as in diagnosis_analysis.js; first match wins)
const FACTS = [
    ["Order of operations", /order of operations|pemdas|precedence/i],
    ["Units, conversions and money", /\b(km|cm|mm|kg|mg|ml)\b|kilomet|centimet|millimet|dollar|cents?\b|penn/i],
    ["Negative numbers and signs", /negative|sign|subtracting a negative|opposite|absolute value|integer/i],
    ["Exponents and roots", /exponent|power|squar|cube|root|\^/i],
    ["Percent", /percent|%/i],
    ["Fractions", /fraction|numerator|denominator|reciprocal|mixed number|improper/i],
    ["Decimals and place value", /decimal|place value|tenths|hundredths|thousandths|powers? of ten|digit/i],
    ["Ratios, rates and proportions", /ratio|rate|proportion|unit price|per\b|constant of proportionality/i],
    ["Area, perimeter, volume, circles", /area|perimeter|volume|surface|circumference|radius|diameter|\bpi\b|π/i],
    ["Angles, shapes and geometry terms", /angle|triangle|polygon|parallel|perpendicular|congruent|similar|scale|degree/i],
    ["Units, conversions and money", /unit|convert|conversion|inch|feet|foot|meter|mile|hour|minute|second|gram|liter|pound|ounce|\$/i],
    ["Algebra terms", /variable|coefficient|like terms|term|expression|equation|distribut|factor|inverse/i],
    ["Statistics and probability terms", /mean|median|mode|range|probab|sample|outcome|frequency|interquartile|mad\b/i],
    ["Number facts and operations", /multipl|divid|division|add|sum|subtract|product|quotient|times table|fact/i],
];
const FACT_NAMES = [...new Set(FACTS.map(f => f[0])), "Other"];
const factGroup = f => { for (const [n, re] of FACTS) if (re.test(f)) return FACT_NAMES.indexOf(n); return FACT_NAMES.length - 1; };
// wording of an execution slip in the model's explanation (a careless error in carrying out a step)
const SLIP_RE = /\bslip|careless|arithmetic (error|mistake|slip)|calculation (error|mistake)|computational (error|mistake)|computation (error|mistake)|miscalculat|miscount|typo|transcri|copying|copied|mis-?typed|minor error|simple error|added incorrectly|subtracted incorrectly|multiplied incorrectly|divided incorrectly|rounding error/i;

// ---------- problems
const P = readTable("Data/Problems.csv"), S = readTable("Data/Skills.csv");
const codeOf = new Map();
for (const r of S.rows) { const pid = (r[0] || "").trim(), c = (r[2] || "").trim(); if (!pid || !c) continue; if (!codeOf.has(pid) || c < codeOf.get(pid)) codeOf.set(pid, c); }
let A300 = new Map();
if (fs.existsSync("Data/problems_300.csv")) { const T = readTable("Data/problems_300.csv"); for (const r of T.rows) { const v = canon(r[T.h.aashish_top_practice] || ""); if (v) A300.set(+r[T.h.row], v); } }
const pIdx = new Map(), prob = [];
const skillIdx = new Map(), skills = [];
P.rows.forEach((r, k) => {
    const pid = r[P.h.problem_id].trim(); if (pIdx.has(pid)) return;
    const l = llmOrdering(r[P.h[`${PREFIX}_reasoning`]] || "");
    const code = codeOf.get(pid) || "";
    if (!skillIdx.has(code)) { skillIdx.set(code, skills.length); skills.push(code); }
    pIdx.set(pid, prob.length);
    prob.push({ pid, row: k + 1, type: r[P.h["Problem Type"]], top: PR.indexOf(canon(r[P.h[`${PREFIX}_top_practice`]] || "")),
        used: l ? l.order.map(n => PR.indexOf(n)).filter(i => i >= 0) : [], skill: skillIdx.get(code), grade: code.split(".")[0] || "?", domain: code.split(".")[1] || "?",
        claudeTop: k < 300 ? PR.indexOf(canon(r[P.h.claude_top_practice] || "")) : -1, aashishTop: A300.has(k + 1) ? PR.indexOf(A300.get(k + 1)) : -1,
        correct: fixDate(norm(r[P.h["Multiple Choice Answers"]] || r[P.h["Fill-in Answers"]] || "")).split(" || ").map(key),
        n: 0, ok: 0 });
});

// ---------- diagnoses
const D = readTable(DIAG);
const dg = (r, c) => r[D.h[c]];
const diag = [], diagByKey = new Map();
for (const r of D.rows) {
    let a; try { a = JSON.parse(dg(r, "diagnosis_json")); } catch (e) { continue; }
    const steps = (a.steps || []).map(s => ({ p: PR.indexOf(canon(s.practice)), st: s.status, why: s.why || "" }));
    const ff = steps.findIndex(s => s.st === "failed");
    const et = dg(r, "error_type"), fact = (dg(r, "math_fact") || "").trim();
    const allText = [dg(r, "explanation"), dg(r, "reconstruction"), ...steps.map(s => s.why)].join(" ");
    const d = { pid: dg(r, "problem_id"), row: +dg(r, "row"), wrong: dg(r, "wrong_answer"), rank: +dg(r, "rank"), students: +dg(r, "students"), et,
        steps, k: steps.length, failed: ff >= 0 ? steps[ff].p : -1, failPos: ff, nFailed: steps.filter(s => s.st === "failed").length,
        conf: dg(r, "confidence"), fact, fg: et === "math_fact" ? factGroup(fact) : -1,
        execSlip: et === "practice" && ff >= 0 && steps[ff].p === PFI && steps.slice(0, ff).every(s => s.st === "correct") && SLIP_RE.test(allText),
        slipWords: SLIP_RE.test(allText), expl: dg(r, "explanation"), recon: dg(r, "reconstruction") };
    d.id = diag.length; diag.push(d); diagByKey.set(d.pid + "|" + key(norm(d.wrong)), d.id);
}

// ---------- responses (time order)
const lines = fs.readFileSync(path.join("Results", "practice_analysis", "cleaned_responses.tsv"), "utf8").split("\n");
const N0 = lines.length;
const stu = new Int32Array(N0), pr = new Int32Array(N0), sc = new Int8Array(N0), hint = new Int8Array(N0), saw = new Int8Array(N0),
    lab = new Int8Array(N0), did = new Int32Array(N0).fill(-1), tm = new Float64Array(N0), mon = new Int8Array(N0);
const sIdx = new Map(); const akey = new Array(N0);
let N = 0;
for (let i = 1; i < lines.length; i++) {
    const f = lines[i].split("\t"); if (f.length < 7) continue;
    const p = pIdx.get(f[1]); if (p === undefined) continue;
    if (!sIdx.has(f[0])) sIdx.set(f[0], sIdx.size);
    stu[N] = sIdx.get(f[0]); pr[N] = p; sc[N] = f[2] === "1" ? 1 : 0; hint[N] = f[3] !== "0" ? 1 : 0; saw[N] = f[4] === "1" ? 1 : 0;
    const t = Date.parse(f[5].replace(" ", "T").replace(/\+00$/, "Z")); tm[N] = isNaN(t) ? NaN : t; mon[N] = isNaN(t) ? -1 : new Date(t).getUTCMonth();
    prob[p].n++; prob[p].ok += sc[N];
    if (sc[N]) lab[N] = L.correct;
    else if (hint[N] || saw[N]) lab[N] = L.help;
    else {
        const a = norm(f[6] || "");
        if (!a) lab[N] = L.empty;
        else { const k = key(a); if (prob[p].correct.includes(k)) lab[N] = L.key; else { akey[N] = k; lab[N] = -1; } }
    }
    N++;
}
lines.length = 0;
// answer counts per problem (unaided wrong answers), then the labels of the wrong answers
const cnt = new Map();
for (let i = 0; i < N; i++) if (lab[i] === -1) { const k = pr[i] + "|" + akey[i]; cnt.set(k, (cnt.get(k) || 0) + 1); }
for (let i = 0; i < N; i++) if (lab[i] === -1) {
    const d = diagByKey.get(prob[pr[i]].pid + "|" + akey[i]);
    if (d !== undefined) { did[i] = d; lab[i] = L[diag[d].et] ?? L.undiagnosed; }
    else { const c = cnt.get(pr[i] + "|" + akey[i]); lab[i] = c === 1 ? L.unique : c === 2 ? L.rare2 : L.undiagnosed; }
}
const NS = sIdx.size;
console.error(`${N} responses, ${NS} students, ${diag.length} diagnoses`);

// ---------- residuals and per-student sequences
const resid = new Float64Array(N), adj = new Float64Array(N);
const sRes = new Float64Array(NS), sN = new Int32Array(NS), sOk = new Int32Array(NS);
for (let i = 0; i < N; i++) { const p = prob[pr[i]]; const loo = p.n > 1 ? (p.ok - sc[i]) / (p.n - 1) : sc[i]; resid[i] = sc[i] - loo; sRes[stu[i]] += resid[i]; sN[stu[i]]++; sOk[stu[i]] += sc[i]; }
for (let i = 0; i < N; i++) adj[i] = resid[i] - sRes[stu[i]] / sN[stu[i]];
// previous / next response of the same student on the same skill, and the previous response of the student
const prevSk = new Int32Array(N).fill(-1), nextSk = new Int32Array(N).fill(-1), prevAny = new Int32Array(N).fill(-1), nextAny = new Int32Array(N).fill(-1);
const prev3 = new Int8Array(N).fill(-1);   // number correct among the 3 previous same-skill responses (-1: fewer than 3)
{
    const lastSk = new Map(), lastAny = new Int32Array(NS).fill(-1);
    for (let i = 0; i < N; i++) {
        const ks = stu[i] * 4096 + prob[pr[i]].skill;
        const j = lastSk.get(ks); if (j !== undefined) { prevSk[i] = j; nextSk[j] = i; }
        if (j !== undefined && prevSk[j] >= 0 && prevSk[prevSk[j]] >= 0) prev3[i] = sc[j] + sc[prevSk[j]] + sc[prevSk[prevSk[j]]];
        lastSk.set(ks, i);
        const a = lastAny[stu[i]]; if (a >= 0) { prevAny[i] = a; nextAny[a] = i; } lastAny[stu[i]] = i;
    }
}
const position = new Float32Array(N);    // position within the student's own sequence, 0..1
{ const seen = new Int32Array(NS); for (let i = 0; i < N; i++) { position[i] = sN[stu[i]] > 1 ? seen[stu[i]] / (sN[stu[i]] - 1) : 0; seen[stu[i]]++; } }

// ---------- helpers
const R = { meta: { file: DIAG, prefix: PREFIX, responses: N, students: NS, diagnoses: diag.length, labels: LAB, practices: PR, short: SH, fact_groups: FACT_NAMES } };
const mean = a => a.length ? a.reduce((s, x) => s + x, 0) / a.length : null;
const q = (a, f) => { if (!a.length) return null; const s = Float64Array.from(a).sort(); return s[Math.min(s.length - 1, Math.floor(f * s.length))]; };
const pearson = (x, y) => { const n = x.length; if (n < 3) return null; const mx = mean(x), my = mean(y); let a = 0, b = 0, c = 0;
    for (let i = 0; i < n; i++) { a += (x[i] - mx) * (y[i] - my); b += (x[i] - mx) ** 2; c += (y[i] - my) ** 2; } return b && c ? a / Math.sqrt(b * c) : null; };
const labCounts = idx => { const o = Object.fromEntries(LAB.map(l => [l, 0])); for (const i of idx) o[LAB[lab[i]]]++; return o; };
const isWrongUnaided = i => WRONG_UNAIDED.includes(lab[i]);
const hasFail = i => did[i] >= 0 && diag[did[i]].failed >= 0;
const all = Array.from({ length: N }, (_, i) => i);
const diagResp = all.filter(i => did[i] >= 0);
// a finer label for wrong answers: practice/math-fact errors split by the failed step
const fine = i => { const l = lab[i]; if ((l === L.practice || l === L.math_fact) && diag[did[i]].failed >= 0) return LAB[l] + ":" + SH[diag[did[i]].failed]; return LAB[l]; };

// ===== Part K: top practice vs the step the wrong answer shows failed
const statusOfTop = (d, top) => { const s = d.steps.find(x => x.p === top); return s ? s.st : "absent"; };
const topCat = i => { const d = diag[did[i]], top = prob[pr[i]].top;
    if (d.failed < 0) return "no_failure";
    if (d.failed === top) return d.nFailed === 1 ? "exact_only" : "exact_first";
    const st = statusOfTop(d, top);
    return st === "failed" ? "top_failed_later" : st === "correct" ? "top_correct" : st === "not_reached" ? "top_not_reached" : st === "cannot_tell" ? "top_cannot_tell" : "top_absent"; };
const CATS = ["exact_only", "exact_first", "top_failed_later", "top_correct", "top_not_reached", "top_cannot_tell", "top_absent", "no_failure"];
const catTally = idx => { const o = Object.fromEntries(CATS.map(c => [c, 0])); for (const i of idx) o[topCat(i)]++; return { n: idx.length, ...o }; };
const multi = diagResp.filter(i => diag[did[i]].k >= 2 && prob[pr[i]].top >= 0);
const withF = idx => idx.filter(i => diag[did[i]].failed >= 0);
const matchStats = idx => { const f = withF(idx); if (!f.length) return { n: idx.length, with_failure: 0, match: null, chance: null };
    const m = f.filter(i => diag[did[i]].failed === prob[pr[i]].top).length;
    const ch = mean(f.map(i => 1 / diag[did[i]].k));
    return { n: idx.length, with_failure: f.length, match: m / f.length, chance: ch, lift: ch ? (m / f.length) / ch : null,
        diagnoses: new Set(f.map(i => did[i])).size }; };
R.top_match = {
    all: { ...catTally(diagResp.filter(i => prob[pr[i]].top >= 0)), ...matchStats(diagResp.filter(i => prob[pr[i]].top >= 0)) },
    multi: { ...catTally(multi), ...matchStats(multi) },
    // the same, counted once per diagnosed wrong answer instead of once per response
    multi_by_answer: (() => { const seen = new Set(), idx = []; for (const i of multi) if (!seen.has(did[i])) { seen.add(did[i]); idx.push(i); } return { ...catTally(idx), ...matchStats(idx) }; })(),
    by_top: SH.map((p, t) => { const idx = multi.filter(i => prob[pr[i]].top === t); return { top: p, ...catTally(idx), ...matchStats(idx) }; }),
};
// K2: per problem
{
    const per = new Map();
    for (const i of diagResp) { const p = pr[i]; if (!per.has(p)) per.set(p, { fail: new Array(6).fill(0), nd: 0, nf: 0 }); const o = per.get(p); o.nd++; const f = diag[did[i]].failed; if (f >= 0) { o.fail[f]++; o.nf++; } }
    const wrongUn = new Map(); for (let i = 0; i < N; i++) if (isWrongUnaided(i)) wrongUn.set(pr[i], (wrongUn.get(pr[i]) || 0) + 1);
    const rows = [];
    for (const [p, o] of per) { const P0 = prob[p]; if (P0.top < 0 || o.nf < 5) continue;
        const modal = o.fail.indexOf(Math.max(...o.fail));
        rows.push({ p, top: P0.top, k: P0.used.length, nf: o.nf, share_top: o.fail[P0.top] / o.nf, share_top_of_wrong: o.fail[P0.top] / (wrongUn.get(p) || o.nf), modal, modal_share: o.fail[modal] / o.nf }); }
    const bins = [[0, 0, "0%"], [1e-9, 0.25, "1–25%"], [0.25 + 1e-9, 0.5, "26–50%"], [0.5 + 1e-9, 0.75, "51–75%"], [0.75 + 1e-9, 1 - 1e-9, "76–99%"], [1, 1, "100%"]];
    const hist = list => bins.map(([a, b, label]) => ({ label, n: list.filter(r => r.share_top >= a && r.share_top <= b).length }));
    const m = rows.filter(r => r.k >= 2);
    R.per_problem = { problems: rows.length, multi: m.length, min_failures: 5,
        hist_all: hist(rows), hist_multi: hist(m),
        modal_is_top: rows.filter(r => r.modal === r.top).length / rows.length, modal_is_top_multi: m.filter(r => r.modal === r.top).length / m.length,
        median_share_top_multi: q(m.map(r => r.share_top), 0.5), median_share_top_of_wrong_multi: q(m.map(r => r.share_top_of_wrong), 0.5),
        transition: SH.map((tp, t) => ({ top: tp, modal: SH.map((_, f) => m.filter(r => r.top === t && r.modal === f).length) })),
        by_top: SH.map((tp, t) => { const l = m.filter(r => r.top === t); return { top: tp, problems: l.length, modal_is_top: l.length ? l.filter(r => r.modal === r.top).length / l.length : null, median_share_top: q(l.map(r => r.share_top), 0.5) }; }),
        examples_mismatch: m.filter(r => r.modal !== r.top && r.modal_share >= 0.8 && r.nf >= 30).sort((a, b) => b.nf - a.nf).slice(0, 8)
            .map(r => ({ row: prob[r.p].row, top: SH[r.top], modal: SH[r.modal], modal_share: r.modal_share, failures: r.nf, used: prob[r.p].used.map(u => SH[u]).join(" > ") })) };
}
// K3: what the match depends on (multi-step responses)
{
    const P0 = i => prob[pr[i]];
    const groups = (name, fn, order) => { const m = new Map(); for (const i of multi) { const g = fn(i); if (g === null) continue; if (!m.has(g)) m.set(g, []); m.get(g).push(i); }
        const ks = order || [...m.keys()].sort(); return { factor: name, rows: ks.filter(k => m.has(k)).map(k => ({ group: String(k), ...matchStats(m.get(k)) })) }; };
    const diffT = (() => { const v = prob.filter(p => p.n).map(p => p.ok / p.n); return [q(v, 1 / 3), q(v, 2 / 3)]; })();
    R.match_by = [
        groups("Steps in the solution", i => Math.min(diag[did[i]].k, 4) === 4 ? "4+" : String(diag[did[i]].k), ["2", "3", "4+"]),
        groups("Where the top practice comes in the solution", i => { const u = P0(i).used, j = u.indexOf(P0(i).top); return j < 0 ? "not in the steps" : j === 0 ? "first step" : j === u.length - 1 ? "last step" : "middle step"; }, ["first step", "middle step", "last step", "not in the steps"]),
        groups("Question type", i => P0(i).type),
        groups("Problem difficulty (% correct, thirds)", i => { const v = P0(i).ok / P0(i).n; return v <= diffT[0] ? "hardest third" : v <= diffT[1] ? "middle third" : "easiest third"; }, ["hardest third", "middle third", "easiest third"]),
        groups("How common the wrong answer is in its problem", i => { const r = diag[did[i]].rank; return r === 1 ? "most common" : r === 2 ? "2nd" : r <= 4 ? "3rd–4th" : "5th or later"; }, ["most common", "2nd", "3rd–4th", "5th or later"]),
        groups("Kind of error", i => diag[did[i]].et === "guess" ? null : diag[did[i]].et, ["practice", "math_fact"]),
        groups("Model's confidence", i => diag[did[i]].conf, ["high", "medium", "low"]),
        groups("Grade", i => P0(i).grade, ["3", "4", "5", "6", "7", "8", "HSA", "HSF", "HSG", "HSN", "HSS"].filter(g => multi.some(i => P0(i).grade === g))),
    ];
}
// K4: rows 1-300: Qwen's, Claude's and Aashish's top practice against the failed step
{
    const r300 = multi.filter(i => prob[pr[i]].row <= 300 && diag[did[i]].failed >= 0);
    const m = (idx, f) => idx.length ? idx.filter(i => f(prob[pr[i]]) === diag[did[i]].failed).length / idx.length : null;
    const dis = r300.filter(i => prob[pr[i]].claudeTop >= 0 && prob[pr[i]].claudeTop !== prob[pr[i]].top);
    const aas = r300.filter(i => prob[pr[i]].aashishTop >= 0);
    R.labelers_300 = { responses: r300.length, problems: new Set(r300.map(i => pr[i])).size,
        qwen: m(r300, p => p.top), claude: m(r300.filter(i => prob[pr[i]].claudeTop >= 0), p => p.claudeTop),
        claude_in_steps: r300.filter(i => prob[pr[i]].used.includes(prob[pr[i]].claudeTop)).length / (r300.length || 1),
        disagree: { responses: dis.length, problems: new Set(dis.map(i => pr[i])).size, qwen: m(dis, p => p.top), claude: m(dis, p => p.claudeTop) },
        aashish: { responses: aas.length, problems: new Set(aas.map(i => pr[i])).size, aashish: m(aas, p => p.aashishTop), qwen: m(aas, p => p.top), claude: m(aas, p => p.claudeTop) } };
}

// ===== Part L: every answer labeled; slips and guesses
{
    const types = [...new Set(prob.map(p => p.type))].filter(t => all.some(i => prob[pr[i]].type === t)).sort();
    const byType = {}; for (const t of types) byType[t] = []; for (let i = 0; i < N; i++) byType[prob[pr[i]].type].push(i);
    const byTop = SH.map(() => []); for (let i = 0; i < N; i++) if (prob[pr[i]].top >= 0) byTop[prob[pr[i]].top].push(i);
    const fineCounts = idx => { const o = {}; for (const i of idx) if (lab[i] !== L.correct) { const k = fine(i); o[k] = (o[k] || 0) + 1; } return o; };
    R.labels = { all: labCounts(all), fine: fineCounts(all),
        by_type: types.map(t => ({ type: t, n: byType[t].length, ...labCounts(byType[t]) })),
        by_top: SH.map((p, t) => ({ top: p, n: byTop[t].length, ...labCounts(byTop[t]), fine: fineCounts(byTop[t]) })),
        undiagnosed_answers: new Set(all.filter(i => lab[i] === L.undiagnosed).map(i => pr[i] + "|" + akey[i])).size };
}
// L2: BKT-style slip and guess rates (3 previous answers on the same skill all right / all wrong)
{
    const rate = (idx, want) => { const n = idx.length; return { n, rate: n ? idx.filter(i => sc[i] === want).length / n : null }; };
    const mastered = all.filter(i => prev3[i] === 3), unmastered = all.filter(i => prev3[i] === 0);
    const by = (idx, fn, keys) => keys.map(k => ({ group: k, ...rate(idx.filter(i => fn(i) === k), idx === mastered ? 0 : 1) }));
    const types = [...new Set(prob.map(p => p.type))].sort();
    R.slip_guess = {
        slip: rate(mastered, 0), guess: rate(unmastered, 1), base_wrong: all.filter(i => !sc[i]).length / N,
        slip_by_top: by(mastered, i => SH[prob[pr[i]].top] || "?", SH), guess_by_top: by(unmastered, i => SH[prob[pr[i]].top] || "?", SH),
        slip_by_type: by(mastered, i => prob[pr[i]].type, types).filter(x => x.n), guess_by_type: by(unmastered, i => prob[pr[i]].type, types).filter(x => x.n),
        slip_by_k: by(mastered, i => String(Math.min(prob[pr[i]].used.length, 4)), ["1", "2", "3", "4"]),
        // what the wrong answers in the "mastered" context are
        slip_labels: labCounts(mastered.filter(i => !sc[i])), slip_fine: (() => { const o = {}; for (const i of mastered) if (!sc[i]) { const k = fine(i); o[k] = (o[k] || 0) + 1; } return o; })(),
        all_wrong_labels: labCounts(all.filter(i => !sc[i])),
    };
    // isolated errors: a wrong answer between a right answer just before and just after on the same skill
    const wrongU = all.filter(isWrongUnaided);
    const flank = i => prevSk[i] >= 0 && nextSk[i] >= 0 && sc[prevSk[i]] === 1 && sc[nextSk[i]] === 1;
    const haveBoth = wrongU.filter(i => prevSk[i] >= 0 && nextSk[i] >= 0);
    // baseline: a correct answer in the same position (both neighbours right), to compare how often wrong answers are "isolated"
    const corrBoth = all.filter(i => sc[i] === 1 && prevSk[i] >= 0 && nextSk[i] >= 0);
    R.isolated = { wrong_with_both: haveBoth.length, isolated: haveBoth.filter(flank).length, share: haveBoth.filter(flank).length / haveBoth.length,
        correct_with_both: corrBoth.length, correct_isolated_share: corrBoth.filter(flank).length / corrBoth.length };
    R.exec_slips = { diagnoses: diag.filter(d => d.execSlip).length, responses: diagResp.filter(i => diag[did[i]].execSlip).length,
        slip_words_any: diagResp.filter(i => diag[did[i]].slipWords).length,
        practice_pf: diagResp.filter(i => diag[did[i]].et === "practice" && diag[did[i]].failed === PFI).length,
        examples: diag.filter(d => d.execSlip).sort((a, b) => b.students - a.students).slice(0, 6).map(d => ({ row: d.row, wrong: d.wrong, students: d.students, expl: d.expl })) };
}
// L3: how each kind of wrong answer behaves (slip-like or persistent)
{
    const kinds = ["correct", "help", "empty", "key", ...SH.filter((_, i) => i !== 4).map(p => "practice:" + p), ...SH.filter((_, i) => i !== 4).map(p => "math_fact:" + p), "guess", "rare2", "unique", "exec_slip"];
    const m = new Map(kinds.map(k => [k, []]));
    for (let i = 0; i < N; i++) { const k = fine(i); if (m.has(k)) m.get(k).push(i); if (did[i] >= 0 && diag[did[i]].execSlip) m.get("exec_slip").push(i); }
    R.behaviour = kinds.map(k => { const idx = m.get(k); if (!idx.length) return { kind: k, n: 0 };
        const pv = idx.filter(i => prevSk[i] >= 0), nx = idx.filter(i => nextSk[i] >= 0), both = idx.filter(i => prevSk[i] >= 0 && nextSk[i] >= 0);
        const m3 = idx.filter(i => prev3[i] >= 0);
        return { kind: k, n: idx.length,
            prev_correct: pv.length ? pv.filter(i => sc[prevSk[i]]).length / pv.length : null,
            next_correct: nx.length ? nx.filter(i => sc[nextSk[i]]).length / nx.length : null,
            next_adj: nx.length ? mean(nx.map(i => adj[nextSk[i]])) : null,
            isolated: both.length ? both.filter(i => sc[prevSk[i]] && sc[nextSk[i]]).length / both.length : null,
            after_mastery: m3.length ? m3.filter(i => prev3[i] === 3).length / m3.length : null,
            student_acc: mean(idx.map(i => sOk[stu[i]] / sN[stu[i]])) }; });
}
// L4: strong and weak students' errors
{
    const accs = Array.from({ length: NS }, (_, s) => sOk[s] / sN[s]);
    const cut = [0.2, 0.4, 0.6, 0.8].map(f => q(accs, f));
    const qOf = s => cut.filter(c => accs[s] > c).length;
    const groups = [0, 1, 2, 3, 4].map(() => []);
    for (let i = 0; i < N; i++) groups[qOf(stu[i])].push(i);
    R.by_ability = groups.map((idx, g) => { const st = new Set(idx.map(i => stu[i]));
        const w = idx.filter(isWrongUnaided), f = w.filter(i => did[i] >= 0 && diag[did[i]].failed >= 0);
        const fc = SH.map((_, p) => f.filter(i => diag[did[i]].failed === p).length);
        return { group: ["weakest fifth", "2nd fifth", "middle fifth", "4th fifth", "strongest fifth"][g], students: st.size, responses: idx.length,
            accuracy: idx.filter(i => sc[i]).length / idx.length, labels: labCounts(idx), failed: fc,
            exec_slips: w.filter(i => did[i] >= 0 && diag[did[i]].execSlip).length,
            slip_rate: (() => { const m3 = idx.filter(i => prev3[i] === 3); return m3.length ? m3.filter(i => !sc[i]).length / m3.length : null; })(),
            guess_rate: (() => { const m0 = idx.filter(i => prev3[i] === 0); return m0.length ? m0.filter(i => sc[i]).length / m0.length : null; })() }; });
}
// L5: time before each kind of answer (gap since the student's previous response, 5 s to 30 min)
{
    const gap = i => { const j = prevAny[i]; if (j < 0) return null; const g = (tm[i] - tm[j]) / 1000; return g >= 5 && g <= 1800 ? g : null; };
    const kinds = ["correct", "help", "practice", "math_fact", "guess", "rare2", "unique", "empty", "exec_slip", "practice:REP", "practice:PF", "math_fact:PF"];
    R.time = kinds.map(k => { const g = [];
        for (let i = 0; i < N; i++) { const hit = k === "exec_slip" ? (did[i] >= 0 && diag[did[i]].execSlip) : k.includes(":") ? fine(i) === k : LAB[lab[i]] === k; if (!hit) continue; const v = gap(i); if (v !== null) g.push(v); }
        return { kind: k, n: g.length, p25: q(g, 0.25), median: q(g, 0.5), p75: q(g, 0.75) }; });
    // time relative to the student's own median gap (so fast and slow students do not drive it)
    const sg = Array.from({ length: NS }, () => []); for (let i = 0; i < N; i++) { const v = gap(i); if (v !== null) sg[stu[i]].push(v); }
    const smed = sg.map(a => q(a, 0.5));
    R.time_rel = kinds.map(k => { const r = [];
        for (let i = 0; i < N; i++) { const hit = k === "exec_slip" ? (did[i] >= 0 && diag[did[i]].execSlip) : k.includes(":") ? fine(i) === k : LAB[lab[i]] === k; if (!hit) continue; const v = gap(i); if (v !== null && smed[stu[i]]) r.push(Math.log2(v / smed[stu[i]])); }
        return { kind: k, n: r.length, median_ratio: r.length ? 2 ** q(r, 0.5) : null }; });
}

// ===== Part M: students and their errors over time
// M1: does the next diagnosed error of a student fail at the same practice? observed vs labels shuffled within each problem
{
    const seq = Array.from({ length: NS }, () => []); for (const i of diagResp) seq[stu[i]].push(i);
    const pairs = []; for (const l of seq) for (let k = 1; k < l.length; k++) pairs.push([l[k - 1], l[k]]);
    const byProb = new Map(); for (const i of diagResp) { if (!byProb.has(pr[i])) byProb.set(pr[i], []); byProb.get(pr[i]).push(i); }
    const sameSkill = ([a, b]) => prob[pr[a]].skill === prob[pr[b]].skill;
    const stats = d => { // d: Int32Array response -> diagnosis id
        const o = { fail: [0, 0], fail_same_skill: [0, 0], fail_other_skill: [0, 0], et: [0, 0], fact: [0, 0], trans: SH.map(() => new Array(6).fill(0)) };
        for (const pq of pairs) { const [a, b] = pq, A = diag[d[a]], B = diag[d[b]];
            o.et[1]++; if (A.et === B.et) o.et[0]++;
            if (A.failed >= 0 && B.failed >= 0) { const s = A.failed === B.failed ? 1 : 0; o.fail[1]++; o.fail[0] += s; o.trans[A.failed][B.failed]++;
                if (sameSkill(pq)) { o.fail_same_skill[1]++; o.fail_same_skill[0] += s; } else { o.fail_other_skill[1]++; o.fail_other_skill[0] += s; } }
            if (A.fg >= 0 && B.fg >= 0) { o.fact[1]++; if (A.fg === B.fg) o.fact[0]++; } }
        return o; };
    const base = new Int32Array(N).fill(-1); for (const i of diagResp) base[i] = did[i];
    const obs = stats(base);
    let seed = 12345; const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
    const perm = [];
    for (let rep = 0; rep < 30; rep++) { const d = new Int32Array(N).fill(-1);
        for (const l of byProb.values()) { const ids = l.map(i => did[i]); for (let k = ids.length - 1; k > 0; k--) { const j = Math.floor(rnd() * (k + 1)); [ids[k], ids[j]] = [ids[j], ids[k]]; } l.forEach((i, k) => d[i] = ids[k]); }
        perm.push(stats(d)); }
    const rr = x => x[1] ? x[0] / x[1] : null;
    const summ = keyName => { const v = perm.map(p => rr(p[keyName])); const m = mean(v), sd = Math.sqrt(mean(v.map(x => (x - m) ** 2))); return { pairs: obs[keyName][1], observed: rr(obs[keyName]), shuffled: m, sd, z: sd ? (rr(obs[keyName]) - m) / sd : null }; };
    R.repeat = { pairs: pairs.length, fail: summ("fail"), fail_same_skill: summ("fail_same_skill"), fail_other_skill: summ("fail_other_skill"), et: summ("et"), fact: summ("fact"),
        // lift: observed transitions / shuffled transitions
        trans_obs: obs.trans, trans_shuffled: SH.map((_, a) => SH.map((_, b) => mean(perm.map(p => p.trans[a][b])))) };
}
// M2: are students' error profiles stable? split-half reliability of each student's excess over what their problems predict
{
    // expected chance that a response's label is X, from the other students on the same problem (leave-one-out)
    const pc = new Map(); // problem -> counts over its unaided wrong responses
    const keyOf = i => ({ common: did[i] >= 0, fail: hasFail(i) ? diag[did[i]].failed : -1, fact: lab[i] === L.math_fact, pfail: hasFail(i) });
    for (let i = 0; i < N; i++) if (isWrongUnaided(i)) { if (!pc.has(pr[i])) pc.set(pr[i], { n: 0, common: 0, nf: 0, fail: new Array(6).fill(0), nd: 0, fact: 0 });
        const o = pc.get(pr[i]), k = keyOf(i); o.n++; if (k.common) { o.common++; o.nd++; if (k.fact) o.fact++; } if (k.pfail) { o.nf++; o.fail[k.fail]++; } }
    const measures = {
        "gives common (shared) wrong answers": { use: i => isWrongUnaided(i), obs: i => did[i] >= 0 ? 1 : 0, exp: i => { const o = pc.get(pr[i]); return o.n > 1 ? (o.common - (did[i] >= 0)) / (o.n - 1) : null; } },
        "fails at Representing": { use: hasFail, obs: i => diag[did[i]].failed === REPI ? 1 : 0, exp: i => { const o = pc.get(pr[i]); return o.nf > 1 ? (o.fail[REPI] - (diag[did[i]].failed === REPI)) / (o.nf - 1) : null; } },
        "fails at Procedural Fluency": { use: hasFail, obs: i => diag[did[i]].failed === PFI ? 1 : 0, exp: i => { const o = pc.get(pr[i]); return o.nf > 1 ? (o.fail[PFI] - (diag[did[i]].failed === PFI)) / (o.nf - 1) : null; } },
        "makes math-fact errors": { use: i => did[i] >= 0, obs: i => lab[i] === L.math_fact ? 1 : 0, exp: i => { const o = pc.get(pr[i]); return o.nd > 1 ? (o.fact - (lab[i] === L.math_fact)) / (o.nd - 1) : null; } },
    };
    R.stability = Object.entries(measures).map(([name, M]) => {
        const h = Array.from({ length: NS }, () => [[0, 0, 0], [0, 0, 0]]); // [obs, exp, n] for halves
        const cntS = new Int32Array(NS);
        for (let i = 0; i < N; i++) { if (!M.use(i)) continue; const e = M.exp(i); if (e === null) continue; const s = stu[i], half = cntS[s]++ % 2; h[s][half][0] += M.obs(i); h[s][half][1] += e; h[s][half][2]++; }
        const x = [], y = [], ex = [];
        for (let s = 0; s < NS; s++) { const [a, b] = h[s]; if (a[2] >= 5 && b[2] >= 5) { x.push((a[0] - a[1]) / a[2]); y.push((b[0] - b[1]) / b[2]); ex.push((a[0] + b[0] - a[1] - b[1]) / (a[2] + b[2])); } }
        const r = pearson(x, y);
        return { measure: name, students: x.length, r, spearman_brown: r === null ? null : 2 * r / (1 + r), sd_excess: Math.sqrt(mean(ex.map(v => v * v)) - mean(ex) ** 2),
            p10: q(ex, 0.1), p90: q(ex, 0.9) }; });
    // do a student's diagnosed failures line up with where they are weak elsewhere?
    const st = Array.from({ length: NS }, () => ({ fo: 0, fe: 0, fn: 0, rep: [], pf: [] }));
    for (let i = 0; i < N; i++) {
        const t = prob[pr[i]].top; if (t === REPI) st[stu[i]].rep.push(adj[i]); else if (t === PFI) st[stu[i]].pf.push(adj[i]);
        if (hasFail(i)) { const o = pc.get(pr[i]); if (o.nf > 1) { st[stu[i]].fo += diag[did[i]].failed === REPI; st[stu[i]].fe += (o.fail[REPI] - (diag[did[i]].failed === REPI)) / (o.nf - 1); st[stu[i]].fn++; } }
    }
    const ok = st.filter(o => o.fn >= 8 && o.rep.length >= 20 && o.pf.length >= 20);
    const exc = ok.map(o => (o.fo - o.fe) / o.fn), gapv = ok.map(o => mean(o.rep) - mean(o.pf));
    const order = exc.map((v, k) => [v, gapv[k]]).sort((a, b) => a[0] - b[0]);
    const quart = [0, 1, 2, 3].map(k => { const sl = order.slice(Math.floor(k * order.length / 4), Math.floor((k + 1) * order.length / 4)); return { quarter: ["fewest Representing failures", "2nd", "3rd", "most Representing failures"][k], students: sl.length, excess: mean(sl.map(v => v[0])), rep_minus_pf: mean(sl.map(v => v[1])) }; });
    R.profile_match = { students: ok.length, r: pearson(exc, gapv), quarters: quart };
}
// M3: what comes after each kind of answer (next answer on the same skill; next problem that needs the failed practice)
{
    const kinds = ["correct", "help", "practice", "math_fact", "guess", "rare2", "unique", "exec_slip", "practice:REP", "practice:PF", "math_fact:PF", "practice:MOD", "practice:A&G", "practice:J&P"];
    // next response of the student whose problem needs practice p (by position in time)
    const nextNeeding = new Int32Array(N).fill(-1);
    { const pend = Array.from({ length: NS }, () => []);
      for (let i = 0; i < N; i++) { const s = stu[i], u = prob[pr[i]].used; const keep = [];
          for (const j of pend[s]) { if (u.includes(diag[did[j]].failed)) nextNeeding[j] = i; else keep.push(j); } pend[s] = keep;
          if (hasFail(i)) pend[s].push(i); } }
    R.after = kinds.map(k => { const idx = [];
        for (let i = 0; i < N; i++) { const hit = k === "exec_slip" ? (did[i] >= 0 && diag[did[i]].execSlip) : k.includes(":") ? fine(i) === k : LAB[lab[i]] === k; if (hit) idx.push(i); }
        const nx = idx.filter(i => nextSk[i] >= 0).map(i => nextSk[i]);
        const nn = idx.filter(i => nextNeeding[i] >= 0).map(i => nextNeeding[i]);
        const na = idx.filter(i => nextAny[i] >= 0).map(i => nextAny[i]);
        return { kind: k, n: idx.length, next_skill_n: nx.length, next_skill_correct: nx.length ? mean(nx.map(j => sc[j])) : null, next_skill_adj: nx.length ? mean(nx.map(j => adj[j])) : null,
            next_skill_help: nx.length ? mean(nx.map(j => (hint[j] || saw[j]) ? 1 : 0)) : null,
            next_any_adj: na.length ? mean(na.map(j => adj[j])) : null, next_any_help: na.length ? mean(na.map(j => (hint[j] || saw[j]) ? 1 : 0)) : null,
            next_needing_n: nn.length, next_needing_adj: nn.length ? mean(nn.map(j => adj[j])) : null,
            // the next same-skill answer is wrong in the same way (same failed practice)
            same_failure_again: (() => { const l = idx.filter(i => hasFail(i) && nextSk[i] >= 0 && !sc[nextSk[i]]); return l.length ? l.filter(i => hasFail(nextSk[i]) && diag[did[nextSk[i]]].failed === diag[did[i]].failed).length / l.length : null; })() }; });
}
// M4: over the student's own sequence and the school year
{
    const fifth = i => Math.min(4, Math.floor(position[i] * 5));
    const seg = [0, 1, 2, 3, 4].map(() => []); for (let i = 0; i < N; i++) seg[fifth(i)].push(i);
    const comp = idx => { const w = idx.filter(isWrongUnaided), f = w.filter(hasFail); return { responses: idx.length, accuracy: idx.filter(i => sc[i]).length / idx.length, labels: labCounts(idx),
        failed: SH.map((_, p) => f.filter(i => diag[did[i]].failed === p).length), slip_rate: (() => { const m3 = idx.filter(i => prev3[i] === 3); return m3.length ? m3.filter(i => !sc[i]).length / m3.length : null; })() }; };
    R.over_sequence = seg.map((idx, k) => ({ group: ["first fifth", "2nd fifth", "3rd fifth", "4th fifth", "last fifth"][k], ...comp(idx) }));
    const months = [8, 9, 10, 11, 0, 1, 2, 3, 4, 5]; const names = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"];
    R.over_year = months.map((m, k) => { const idx = all.filter(i => mon[i] === m); return { month: names[k], ...comp(idx) }; }).filter(x => x.responses >= 1000);
}
// M5: how errors spread over students
{
    const per = new Int32Array(NS), perD = new Int32Array(NS), perW = new Int32Array(NS);
    for (let i = 0; i < N; i++) { if (isWrongUnaided(i)) perW[stu[i]]++; if (did[i] >= 0) perD[stu[i]]++; }
    const sorted = Array.from(perD).sort((a, b) => b - a), tot = sorted.reduce((s, x) => s + x, 0);
    const topShare = f => sorted.slice(0, Math.round(f * NS)).reduce((s, x) => s + x, 0) / tot;
    const shareCommon = []; for (let s = 0; s < NS; s++) if (perW[s] >= 10) shareCommon.push(perD[s] / perW[s]);
    R.spread = { students: NS, with_diagnosed: Array.from(perD).filter(x => x > 0).length, median_diagnosed: q(Array.from(perD), 0.5), p90_diagnosed: q(Array.from(perD), 0.9),
        top10_share: topShare(0.1), top25_share: topShare(0.25), median_share_common: q(shareCommon, 0.5), p10_share_common: q(shareCommon, 0.1), p90_share_common: q(shareCommon, 0.9) };
}

fs.writeFileSync(OUT, JSON.stringify(R, null, 1));
console.error(`wrote ${OUT}`);
