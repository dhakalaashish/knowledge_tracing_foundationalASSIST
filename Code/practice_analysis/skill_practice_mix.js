// How many practices does each skill have, and which ones? Skill-level view of a labeling run's practices.
// Writes one JSON file for the insights page.
//
// Usage (from the repo root):
//   node Code/practice_analysis/skill_practice_mix.js [prefix] [out.json]
//   defaults: qwen35_122b_ch3, Results/practice_analysis/qwen35_122b_ch3_skills.json
//
// A skill is a skill code of Data/Skills.csv (node_code; the 224 skill_ids collapse to 164 codes, since ids that
// share a code share its name). A problem with several codes counts under each. Each problem has its top practice
// (<prefix>_top_practice) and the practices it needs (practices_used of <prefix>_reasoning). A skill "has" a
// practice when at least one of its problems has it ("any") or at least 10% of its problems do ("10%": ignores a
// stray label). Problems without a label in the run are left out. Responses: cleaned data, if present.

const fs = require("fs");
const path = require("path");
const { readTable, canon, llmOrdering } = require("../generate_practice_reasoning/tools/csv.js");
const PREFIX = process.argv[2] || "qwen35_122b_ch3";
const OUT = process.argv[3] || path.join("Results", "practice_analysis", `${PREFIX}_skills.json`);
const PR = ["Representing", "Abstracting and Generalizing", "Justifying and Proving", "Mathematical Modeling",
    "Collaborative Mathematics", "Procedural Fluency"];
const SH = ["REP", "A&G", "J&P", "MOD", "COL", "PF"];
const ORDER = [5, 0, 1, 2, 3, 4];     // how combinations are written: PF first, then REP, A&G, J&P, MOD, COL

const P = readTable("Data/Problems.csv"), S = readTable("Data/Skills.csv");
const lab = new Map();
for (const r of P.rows) {
    const pid = r[P.h.problem_id].trim(); if (lab.has(pid)) continue;
    const raw = (r[P.h[`${PREFIX}_reasoning`]] || "").trim(), l = raw ? llmOrdering(raw) : null;
    const top = PR.indexOf(canon(r[P.h[`${PREFIX}_top_practice`]] || ""));
    lab.set(pid, l && top >= 0 ? { top, used: new Set(l.order.map(canon).map(p => PR.indexOf(p)).filter(i => i >= 0)) } : null);
}
const resp = new Map();
const RF = "Results/practice_analysis/cleaned_responses.tsv";
if (fs.existsSync(RF)) {
    const lines = fs.readFileSync(RF, "utf8").split("\n");
    for (let i = 1; i < lines.length; i++) { const t = lines[i].indexOf("\t"); if (t < 0) continue; const pid = lines[i].slice(t + 1, lines[i].indexOf("\t", t + 1)); resp.set(pid, (resp.get(pid) || 0) + 1); }
}
const skills = new Map();
for (const r of S.rows) {
    const pid = (r[0] || "").trim(), code = (r[2] || "").trim(), name = (r[3] || "").trim();
    if (!pid || !code) continue;
    if (!skills.has(code)) skills.set(code, { code, name, pids: new Set() });
    skills.get(code).pids.add(pid);
}
const comboName = set => ORDER.filter(p => set.has(p)).map(p => SH[p]).join(" + ") || "(none)";
const rows = [];
for (const s of skills.values()) {
    const L = [...s.pids].map(p => lab.get(p)).filter(Boolean);
    if (!L.length) continue;
    const top = Array(6).fill(0), used = Array(6).fill(0);
    for (const x of L) { top[x.top]++; for (const p of x.used) used[p]++; }
    const n = L.length, has = (cnt, min) => new Set(cnt.map((c, p) => (c >= min && c > 0 ? p : -1)).filter(p => p >= 0));
    const topAny = has(top, 1), top10 = has(top, Math.ceil(0.1 * n)), usedAny = has(used, 1), used10 = has(used, Math.ceil(0.1 * n));
    const maj = top.indexOf(Math.max(...top));
    rows.push({ code: s.code, name: s.name, grade: s.code.split(".")[0], domain: s.code.split(".")[1], problems: n,
        responses: [...s.pids].reduce((a, p) => a + (resp.get(p) || 0), 0), top, used,
        top_any: comboName(topAny), top_10: comboName(top10), used_any: comboName(usedAny), used_10: comboName(used10),
        n_top_any: topAny.size, n_top_10: top10.size, n_used_any: usedAny.size, n_used_10: used10.size,
        majority: SH[maj], majority_share: top[maj] / n });
}
rows.sort((a, b) => a.code.localeCompare(b.code, undefined, { numeric: true }));
const R = { meta: { prefix: PREFIX, skills: rows.length, skill_ids: new Set(S.rows.map(r => r[1])).size,
    problems: new Set(rows.flatMap(r => [...skills.get(r.code).pids].filter(p => lab.get(p)))).size,
    responses: [...resp.values()].reduce((a, b) => a + b, 0) } };

// how many different practices a skill has, four ways
const hist = key => { const h = Array(7).fill(0); rows.forEach(r => h[r[key]]++); return h.slice(1); };
R.count = { top_any: hist("n_top_any"), top_10: hist("n_top_10"), used_any: hist("n_used_any"), used_10: hist("n_used_10") };
// which combinations, four ways: skills, problems, responses, and the skill codes
const combos = key => {
    const m = new Map();
    for (const r of rows) { const c = m.get(r[key]) || { combo: r[key], size: r[key].split(" + ").length, skills: 0, problems: 0, responses: 0, codes: [] };
        c.skills++; c.problems += r.problems; c.responses += r.responses; c.codes.push(r.code); m.set(r[key], c); }
    return [...m.values()].sort((a, b) => b.skills - a.skills || b.responses - a.responses);
};
R.combos = { top_any: combos("top_any"), top_10: combos("top_10"), used_any: combos("used_any"), used_10: combos("used_10") };
// is variety just size? number of different top practices by the skill's number of problems
const BK = [[1, 2], [3, 5], [6, 10], [11, 20], [21, 50], [51, 1e9]];
R.by_size = BK.map(([a, b]) => { const g = rows.filter(r => r.problems >= a && r.problems <= b);
    return { bucket: b > 1e8 ? `${a}+` : `${a}–${b}`, skills: g.length, mean_top_any: g.length ? g.reduce((s, r) => s + r.n_top_any, 0) / g.length : null,
        mean_top_10: g.length ? g.reduce((s, r) => s + r.n_top_10, 0) / g.length : null, only_pf: g.filter(r => r.top_10 === "PF").length }; });
// how dominant the main practice is, and which practice it is
const SB = [[0, 0.4], [0.4, 0.6], [0.6, 0.8], [0.8, 1], [1, 1.01]];
R.dominance = SB.map(([a, b]) => { const g = rows.filter(r => r.majority_share >= a && r.majority_share < b);
    return { range: b > 1 ? "100%" : `${Math.round(a * 100)}–${Math.round(b * 100)}%`, skills: g.length, responses: g.reduce((s, r) => s + r.responses, 0) }; });
R.majority = SH.map((p, i) => { const g = rows.filter(r => r.majority === p); return { practice: p, skills: g.length, responses: g.reduce((s, r) => s + r.responses, 0) }; });
// presence of each practice across skills
R.presence = SH.map((p, i) => ({ practice: p, top_any: rows.filter(r => r.top[i] > 0).length, top_10: rows.filter(r => r.top[i] >= Math.ceil(0.1 * r.problems)).length,
    used_any: rows.filter(r => r.used[i] > 0).length, used_10: rows.filter(r => r.used[i] >= Math.ceil(0.1 * r.problems)).length }));
// by domain: mean number of practices and share of pure-PF skills
const doms = [...new Set(rows.map(r => r.domain))];
R.by_domain = doms.map(d => { const g = rows.filter(r => r.domain === d);
    return { domain: d, skills: g.length, mean_top_10: g.reduce((s, r) => s + r.n_top_10, 0) / g.length, only_pf_10: g.filter(r => r.top_10 === "PF").length,
        responses: g.reduce((s, r) => s + r.responses, 0) }; }).sort((a, b) => b.responses - a.responses);
R.rows = rows.map(({ code, name, problems, responses, top, used, top_any, top_10, used_any, used_10, majority, majority_share }) =>
    ({ code, name, problems, responses, top, used, top_any, top_10, used_any, used_10, majority, majority_share: Math.round(majority_share * 1000) / 1000 }));
fs.writeFileSync(OUT, JSON.stringify(R, null, 1));
console.error(`wrote ${OUT}: ${rows.length} skills`);
