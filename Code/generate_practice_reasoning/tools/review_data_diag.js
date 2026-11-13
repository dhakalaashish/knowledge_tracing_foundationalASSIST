// Page data for the review page: the wrong-answer diagnoses (diagnose.py, step 6) of rows 1-300, as JavaScript
// (const DIAG = {row: [diagnosis, ...]}), most students first. Companion to review_data.awk and review_data_llm.js.
//
// Usage (from the repo root):
//   node Code/generate_practice_reasoning/tools/review_data_diag.js [diagnosis csv] > diag.js
//   default: Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv
// Each diagnosis: {key, rank, wrong, students, share, et, failed, fact, recon, expl, conf, by, steps: [{p, st, why}]}.
// Wrong answers given by at least 3 students (first attempts) that have no diagnosis yet (they failed every attempt,
// or the problem has no label in the run) are listed under PENDING: {row: [{key, wrong, students}]}.

const { readTable, canon } = require("./csv");
const FILE = process.argv[2] || "Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv";
const N = 300, MIN = 3;
const TYPES = ["Fill-in-the-blank(s)", "Multiple Choice (select 1)", "Multiple Choice (select all)", "Order / Sort"];
const pad = (n, w) => String(n).padStart(w, "0");
const keyOf = (row, rank) => `r${pad(row, 5)}_w${pad(rank, 3)}`;

const D = readTable(FILE), W = readTable("Results/practice_analysis/common_wrong_answers.csv");
const g = (r, c) => (c in D.h ? r[D.h[c]] : "") || "";
const DIAG = {}, have = new Set();
for (const r of D.rows) {
    const row = Number(g(r, "row")); if (row > N) continue;
    const a = JSON.parse(g(r, "diagnosis_json")), rank = Number(g(r, "rank"));
    const key = keyOf(row, rank); have.add(key);
    (DIAG[row] = DIAG[row] || []).push({
        key, rank, wrong: g(r, "wrong_answer"), students: Number(g(r, "students")), share: Number(g(r, "share_of_wrong")),
        et: g(r, "error_type"), failed: g(r, "failed_practice"), fact: g(r, "math_fact"), recon: g(r, "reconstruction"),
        expl: g(r, "explanation"), conf: g(r, "confidence"), by: g(r, "diagnosed_by"),
        steps: a.steps.map(s => ({ p: canon(s.practice), st: s.status, why: (s.why || "").trim() })),
    });
}
for (const row of Object.keys(DIAG)) DIAG[row].sort((x, y) => y.students - x.students || x.rank - y.rank);
const PENDING = {};
for (const r of W.rows) {
    const row = Number(r[W.h.row]); if (row > N || Number(r[W.h.students]) < MIN || !TYPES.includes(r[W.h.problem_type])) continue;
    const key = keyOf(row, Number(r[W.h.rank])); if (have.has(key)) continue;
    (PENDING[row] = PENDING[row] || []).push({ key, wrong: r[W.h.wrong_answer], students: Number(r[W.h.students]) });
}
const n = Object.values(DIAG).reduce((s, l) => s + l.length, 0), p = Object.values(PENDING).reduce((s, l) => s + l.length, 0);
console.error(`${n} diagnoses on ${Object.keys(DIAG).length} problems (rows 1-${N}); ${p} wrong answers pending`);
const js = v => JSON.stringify(v).replace(/<\//g, "<\\/");
process.stdout.write(`const DIAG_SOURCE = ${js(FILE)};\nconst DIAG = ${js(DIAG)};\nconst PENDING = ${js(PENDING)};\n`);
