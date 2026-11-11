// Common wrong answers per problem, as input for wrong-answer diagnosis by an LLM.
//
// Usage (from the repo root, after clean_responses.js):
//   node --max-old-space-size=8000 Code/practice_analysis/wrong_answers.js
// Writes:
//   Results/practice_analysis/common_wrong_answers.csv   one line per (problem, wrong answer) given by >= 2 students
//   Results/practice_analysis/wrong_answers_summary.json counts by question type and by threshold
//
// Rules
//   - first attempts only (cleaned data), and only those without a hint or an answer view: otherwise the logged
//     text is often not the student's first answer
//   - answers are normalized: HTML removed, entities decoded, spaces collapsed, lower case; numbers that are equal
//     (0.6, .6, 3/5; 1,000 and 1000) are merged under the most common spelling
//   - an answer equal to a correct answer of the problem is dropped (the scorer may differ from our matching)
//   - a problem's row is its first row in Problems.csv

const fs = require("fs");
const path = require("path");
const { readTable, csvField } = require("../generate_practice_reasoning/tools/csv.js");
const ROOT = process.cwd();
const OUT = path.join(ROOT, "Results", "practice_analysis");

const P = readTable(path.join(ROOT, "Data", "Problems.csv"));
const prob = new Map();
P.rows.forEach((r, k) => {
    const pid = r[P.h.problem_id].trim(); if (prob.has(pid)) return;
    prob.set(pid, { pid, row: k + 1, type: r[P.h["Problem Type"]], at: r[P.h["Answer Types"]],
        correct: r[P.h["Multiple Choice Answers"]] || r[P.h["Fill-in Answers"]] || "", n: 0, ok: 0, help: 0, empty: 0, ans: new Map() });
});

const MON = { jan: 1, feb: 2, mar: 3, apr: 4, may: 5, jun: 6, jul: 7, aug: 8, sep: 9, oct: 10, nov: 11, dec: 12 };
const norm = a => a.replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&gt;/g, ">").replace(/&lt;/g, "<")
    .replace(/&amp;/g, "&").replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, " ").trim().toLowerCase();
const fixDate = a => a.replace(/\b(\d{1,2})-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b/g, (m, d, mo) => MON[mo] + "/" + d);
function numVal(t) {                          // a number, a fraction a/b, or a mixed number "a b/c"; else null
    t = t.replace(/,/g, "").replace(/\s+/g, " ").trim();
    let m;
    if ((m = t.match(/^(-?)(\d+) (\d+)\/(\d+)$/))) return (m[1] ? -1 : 1) * (+m[2] + +m[3] / +m[4]);
    if ((m = t.match(/^(-?\d*\.?\d+)\/(-?\d*\.?\d+)$/))) return +m[2] ? +m[1] / +m[2] : null;
    if (/^-?\d*\.?\d+$/.test(t)) return +t;
    return null;
}
const key = a => { const v = numVal(a); return v === null ? "t:" + a.replace(/\s+/g, "") : "n:" + Math.round(v * 1e9) / 1e9; };

const lines = fs.readFileSync(path.join(OUT, "cleaned_responses.tsv"), "utf8").split("\n");
for (let i = 1; i < lines.length; i++) {
    const f = lines[i].split("\t"); if (f.length < 7) continue;
    const p = prob.get(f[1]); if (!p) continue;
    p.n++;
    if (f[2] === "1") { p.ok++; continue; }
    if (f[4] === "1" || f[3] !== "0") { p.help++; continue; }
    const a = norm(f[6] || ""); if (!a) { p.empty++; continue; }
    const k = key(a);
    if (!p.ans.has(k)) p.ans.set(k, { n: 0, spell: new Map() });
    const e = p.ans.get(k); e.n++; e.spell.set(a, (e.spell.get(a) || 0) + 1);
}
lines.length = 0;

const TH = [2, 3, 5, 10, 20];
const csv = [["row", "problem_id", "problem_type", "answer_type", "responses", "pct_correct", "wrong_without_help", "rank", "wrong_answer", "students", "share_of_wrong", "spellings"].join(",")];
const sum = {};                               // by type
for (const p of prob.values()) {
    if (!p.n) continue;
    const correct = fixDate(norm(p.correct)).split(" || ").map(key);
    const wrong = [...p.ans.entries()].filter(([k]) => !correct.includes(k)).map(([k, e]) => ({ k, n: e.n, spell: [...e.spell].sort((a, b) => b[1] - a[1]) }))
        .sort((a, b) => b.n - a.n);
    const nw = wrong.reduce((s, x) => s + x.n, 0);
    const t = p.type;
    if (!sum[t]) sum[t] = { problems: 0, with_wrong: 0, wrong_responses: 0, distinct_wrong: 0, singletons: 0,
        by_threshold: Object.fromEntries(TH.map(h => [h, { problems_with_any: 0, answers: 0, responses_covered: 0, per_problem: [] }])), top_share: [] };
    const S = sum[t]; S.problems++; S.wrong_responses += nw; S.distinct_wrong += wrong.length; S.singletons += wrong.filter(x => x.n === 1).length;
    if (nw) { S.with_wrong++; S.top_share.push(wrong[0].n / nw); }
    for (const h of TH) { const c = wrong.filter(x => x.n >= h); const B = S.by_threshold[h];
        if (c.length) B.problems_with_any++; B.answers += c.length; B.responses_covered += c.reduce((s, x) => s + x.n, 0); B.per_problem.push(c.length); }
    wrong.filter(x => x.n >= 2).forEach((x, i) => csv.push([p.row, p.pid, p.type, p.at, p.n, (p.ok / p.n).toFixed(3), nw, i + 1, x.spell[0][0], x.n,
        (x.n / nw).toFixed(3), x.spell.slice(0, 4).map(([s, c]) => `${s} (${c})`).join(" | ")].map(csvField).join(",")));
}
const q = (a, f) => { if (!a.length) return null; const s = [...a].sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(f * s.length))]; };
for (const S of Object.values(sum)) {
    for (const B of Object.values(S.by_threshold)) {
        B.share_of_wrong_responses = S.wrong_responses ? +(B.responses_covered / S.wrong_responses).toFixed(3) : null;
        B.median_per_problem = q(B.per_problem, 0.5); B.p90_per_problem = q(B.per_problem, 0.9); B.max_per_problem = B.per_problem.length ? Math.max(...B.per_problem) : 0;
        delete B.per_problem;
    }
    S.median_top_wrong_share = S.top_share.length ? +q(S.top_share, 0.5).toFixed(3) : null; delete S.top_share;
}
fs.writeFileSync(path.join(OUT, "common_wrong_answers.csv"), csv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "wrong_answers_summary.json"), JSON.stringify(sum, null, 1));
console.log(JSON.stringify(sum, null, 1));
