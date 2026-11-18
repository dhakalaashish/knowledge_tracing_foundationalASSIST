// List every skill code with the practices of its problems (top practice of one or more labeling runs), and whether
// one practice could stand for the whole skill. Writes <out>.md and <out>.csv (and <out>.json for the insights page).
//
// Usage (from the repo root):
//   node Code/practice_analysis/skills_by_practice.js [column:label ...] [--out <path without extension>]
//   default: qwen3_30b_v3_top_practice:v3 qwen3_30b_v4_top_practice:v4 --out Results/skills_and_practices
//   e.g.     node Code/practice_analysis/skills_by_practice.js qwen35_122b_ch3_top_practice:ch3 --out Results/skills_and_practices_qwen35_122b_ch3
// Verdict: "one practice" when every run gives the same majority practice for at least 80% of the skill's problems,
// "mostly" at 60-80%, otherwise "mixed" (also when the runs disagree on the majority); fewer than 3 problems: too few.
// A problem with several skill codes counts once under each of them. Problems a run has no label for are left out
// of that run's mix. Responses come from the cleaned data (Results/practice_analysis/cleaned_responses.tsv), if present.

const fs = require("fs");
const { readTable, canon, csvField, PRACTICES } = require("../generate_practice_reasoning/tools/csv.js");
const SH = ["REP", "A&G", "J&P", "MOD", "COL", "PF"];
const argv = process.argv.slice(2);
let OUT = "Results/skills_and_practices";
const specs = [];
for (let i = 0; i < argv.length; i++) { if (argv[i] === "--out") OUT = argv[++i]; else specs.push(argv[i]); }
const COLS = (specs.length ? specs : ["qwen3_30b_v3_top_practice:v3", "qwen3_30b_v4_top_practice:v4"]).map(s => { const [c, l] = s.split(":"); return [c, l || c]; });
const LAB = COLS.map(([, l]) => l);
const both = COLS.length === 1 ? LAB[0] : LAB.slice(0, -1).join(", ") + " and " + LAB[LAB.length - 1];

const P = readTable("Data/Problems.csv"), S = readTable("Data/Skills.csv");
for (const [c] of COLS) if (!(c in P.h)) { console.error(`Problems.csv has no column ${c}`); process.exit(1); }
const codes = new Map(), names = new Map();
for (const r of S.rows) {
    const pid = (r[0] || "").trim(), c = (r[2] || "").trim(), n = (r[3] || "").trim();
    if (!pid || !c || !n) continue;
    if (!codes.has(pid)) codes.set(pid, new Set()); codes.get(pid).add(c); names.set(c, n);
}
const resp = new Map();
const RF = "Results/practice_analysis/cleaned_responses.tsv";
if (fs.existsSync(RF)) {
    const lines = fs.readFileSync(RF, "utf8").split("\n");
    for (let i = 1; i < lines.length; i++) { const t = lines[i].indexOf("\t"); if (t < 0) continue; const pid = lines[i].slice(t + 1, lines[i].indexOf("\t", t + 1)); resp.set(pid, (resp.get(pid) || 0) + 1); }
}
const per = new Map(), seen = new Set();
for (const r of P.rows) {
    const pid = r[P.h.problem_id].trim(); if (seen.has(pid)) continue; seen.add(pid);
    const lab = COLS.map(([c]) => PRACTICES.indexOf(canon(r[P.h[c]] || "")));
    for (const c of codes.get(pid) || []) {
        if (!per.has(c)) per.set(c, { code: c, name: names.get(c), n: 0, resp: 0, mix: COLS.map(() => Array(6).fill(0)) });
        const x = per.get(c); x.n++; x.resp += resp.get(pid) || 0;
        lab.forEach((p, j) => { if (p >= 0) x.mix[j][p]++; });
    }
}
const rows = [...per.values()].sort((a, b) => a.code.localeCompare(b.code, undefined, { numeric: true }));
for (const x of rows) {
    x.maj = x.mix.map(m => { const v = Math.max(...m), t = m.reduce((s, y) => s + y, 0); return { p: m.indexOf(v), share: t ? v / t : 0 }; });
    const same = x.maj.every(m => m.p === x.maj[0].p);
    x.verdict = x.n < 3 ? "too few problems"
        : same && x.maj.every(m => m.share >= 0.8) ? `one practice (${SH[x.maj[0].p]})`
        : same && x.maj.every(m => m.share >= 0.6) ? `mostly ${SH[x.maj[0].p]}`
        : "mixed";
}
const count = v => rows.filter(x => x.verdict.startsWith(v));
const sumN = a => a.reduce((s, x) => s + x.n, 0), sumR = a => a.reduce((s, x) => s + x.resp, 0);
const links = sumN(rows), allR = sumR(rows);
const acc = j => rows.reduce((s, x) => s + Math.max(...x.mix[j]), 0) / rows.reduce((s, x) => s + x.mix[j].reduce((a, b) => a + b, 0), 0);
const pfShare = j => rows.reduce((s, x) => s + x.mix[j][5], 0) / rows.reduce((s, x) => s + x.mix[j].reduce((a, b) => a + b, 0), 0);
const VERDICTS = [["one practice", "One practice (≥ 80% of problems)"], ["mostly", "Mostly one practice (60–80%)"],
    ["mixed", COLS.length > 1 ? `Mixed (< 60%, or ${both} disagree)` : "Mixed (< 60%)"], ["too few problems", "Fewer than 3 problems"]];

const L = [];
L.push("# FoundationalASSIST skills and their practices", "");
L.push(`${rows.length} skill codes (Data/Skills.csv) over ${seen.size} problems; a problem with several codes counts once under each (${links} problem–skill links). ` +
    `Practices: each problem's top practice from ${COLS.map(([c, l]) => `${l} (\`${c}\`)`).join(" and ")}. Responses: the cleaned MACA-CD data. Made by \`Code/practice_analysis/skills_by_practice.js\`.`, "");
L.push("## Can a skill stand for a practice?", "");
L.push(`| Verdict (${COLS.length > 1 ? `${both} agree on the majority practice` : `majority practice of ${both}`}) | Skills | Problems | Share of responses |`, "|---|---:|---:|---:|");
for (const [v, name] of VERDICTS) { const a = count(v); L.push(`| ${name} | ${a.length} | ${sumN(a)} | ${allR ? (100 * sumR(a) / allR).toFixed(1) + "%" : "–"} |`); }
L.push("", `Giving every problem its skill's most common practice would label ${COLS.map((_, j) => `${(100 * acc(j)).toFixed(1)}% of problems correctly with the ${LAB[j]} labels`).join(" and ")} (in sample, so optimistic; always guessing Procedural gets ${COLS.map((_, j) => `${(100 * pfShare(j)).toFixed(0)}%`).join(" / ")}).`, "");
L.push("## All skills", "");
L.push(`Mix = number of problems with each top practice (${LAB[0]}), in the order REP / A&G / J&P / MOD / COL / PF. Majority = most common practice and its share.`, "");
L.push(`| Skill | Name | Problems | Responses | Mix ${LAB[0]} | ${LAB.map(l => `Majority ${l}`).join(" | ")} | Verdict |`, `|---|---|---:|---:|---|${LAB.map(() => "---").join("|")}|---|`);
for (const x of rows) L.push(`| ${x.code} | ${x.name.replace(/\|/g, "/")} | ${x.n} | ${x.resp.toLocaleString("en-US")} | ${x.mix[0].join(" / ")} | ${x.maj.map(m => `${SH[m.p]} ${Math.round(100 * m.share)}%`).join(" | ")} | ${x.verdict} |`);
fs.writeFileSync(OUT + ".md", L.join("\n") + "\n");

const C = [["skill_code", "skill_name", "problems", "responses", ...LAB.flatMap(v => SH.map(s => `${v}_${s}`)), ...LAB.flatMap(v => [`majority_${v}`, `majority_${v}_share`]), "verdict"].join(",")];
for (const x of rows) C.push([x.code, x.name, x.n, x.resp, ...x.mix.flat(), ...x.maj.flatMap(m => [PRACTICES[m.p], m.share.toFixed(3)]), x.verdict].map(csvField).join(","));
fs.writeFileSync(OUT + ".csv", C.join("\n") + "\n");

// summary for the insights page
fs.writeFileSync(OUT + ".json", JSON.stringify({
    runs: COLS.map(([c, l]) => ({ column: c, label: l })), skills: rows.length, problems: seen.size, links, responses: allR,
    verdicts: VERDICTS.map(([v, name]) => { const a = count(v); return { verdict: name, skills: a.length, problems: sumN(a), share_responses: allR ? sumR(a) / allR : null }; }),
    accuracy: COLS.map((_, j) => acc(j)), always_pf: COLS.map((_, j) => pfShare(j)),
    largest: [...rows].sort((a, b) => b.resp - a.resp).slice(0, 25).map(x => ({ code: x.code, name: x.name, problems: x.n, responses: x.resp, mix: x.mix[0], majority: SH[x.maj[0].p], share: x.maj[0].share, verdict: x.verdict })),
}, null, 1));
console.log(`skills ${rows.length}; ${COLS.map((_, j) => `acc ${LAB[j]} ${acc(j).toFixed(3)}`).join(" ")}`);
for (const [v] of VERDICTS) { const a = count(v); console.log(v, a.length, sumN(a), allR ? (sumR(a) / allR).toFixed(3) : ""); }
