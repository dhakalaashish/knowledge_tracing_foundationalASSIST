// List every skill code with the practices of its problems (Qwen v3 and v4 top practice), and whether one practice
// could stand for the whole skill. Writes Results/skills_and_practices.md and Results/skills_and_practices.csv.
// Usage (from the repo root): node Code/practice_analysis/skills_by_practice.js
// A problem with several skill codes counts once under each of them. Responses come from the cleaned data
// (Results/practice_analysis/cleaned_responses.tsv, made by clean_responses.js), if present.

const fs = require("fs");
const { readTable, canon, csvField, PRACTICES } = require("../generate_practice_reasoning/tools/csv.js");
const SH = ["REP", "A&G", "J&P", "MOD", "COL", "PF"];
const COLS = [["qwen3_30b_v3_top_practice", "v3"], ["qwen3_30b_v4_top_practice", "v4"]];

const P = readTable("Data/Problems.csv"), S = readTable("Data/Skills.csv");
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
    const lab = COLS.map(([c]) => PRACTICES.indexOf(canon(r[P.h[c]])));
    for (const c of codes.get(pid) || []) {
        if (!per.has(c)) per.set(c, { code: c, name: names.get(c), n: 0, resp: 0, mix: COLS.map(() => Array(6).fill(0)) });
        const x = per.get(c); x.n++; x.resp += resp.get(pid) || 0;
        lab.forEach((p, j) => { if (p >= 0) x.mix[j][p]++; });
    }
}
const rows = [...per.values()].sort((a, b) => a.code.localeCompare(b.code, undefined, { numeric: true }));
for (const x of rows) {
    x.maj = x.mix.map(m => { const v = Math.max(...m); return { p: m.indexOf(v), share: x.n ? v / x.n : 0 }; });
    const [a, b] = x.maj;
    x.verdict = x.n < 3 ? "too few problems"
        : a.p === b.p && a.share >= 0.8 && b.share >= 0.8 ? `one practice (${SH[a.p]})`
        : a.p === b.p && a.share >= 0.6 && b.share >= 0.6 ? `mostly ${SH[a.p]}`
        : "mixed";
}
const count = v => rows.filter(x => x.verdict.startsWith(v));
const sumN = a => a.reduce((s, x) => s + x.n, 0), sumR = a => a.reduce((s, x) => s + x.resp, 0);
const links = sumN(rows), allR = sumR(rows);
const acc = j => rows.reduce((s, x) => s + Math.max(...x.mix[j]), 0) / links;

const L = [];
L.push("# FoundationalASSIST skills and their practices", "");
L.push(`${rows.length} skill codes (Data/Skills.csv) over ${seen.size} problems; a problem with several codes counts once under each (${links} problem–skill links). ` +
    `Practices: each problem's top practice from Qwen v3 and Qwen v4. Responses: the cleaned MACA-CD data. Made by \`Code/practice_analysis/skills_by_practice.js\`.`, "");
L.push("## Can a skill stand for a practice?", "");
L.push("| Verdict (both v3 and v4 agree on the majority practice) | Skills | Problems | Share of responses |", "|---|---:|---:|---:|");
for (const v of ["one practice", "mostly", "mixed", "too few problems"]) { const a = count(v); L.push(`| ${v === "one practice" ? "One practice (≥ 80% of problems)" : v === "mostly" ? "Mostly one practice (60–80%)" : v === "mixed" ? "Mixed (< 60%, or v3 and v4 disagree)" : "Fewer than 3 problems"} | ${a.length} | ${sumN(a)} | ${allR ? (100 * sumR(a) / allR).toFixed(1) + "%" : "–"} |`); }
L.push("", `Giving every problem its skill's most common practice would label ${(100 * acc(0)).toFixed(1)}% of problems correctly with the v3 labels and ${(100 * acc(1)).toFixed(1)}% with v4 (in sample, so optimistic; always guessing Procedural gets about 48%).`, "");
L.push("## All skills", "");
L.push("Mix = number of problems with each top practice (v3), in the order REP / A&G / J&P / MOD / COL / PF. Majority = most common practice and its share.", "");
L.push("| Skill | Name | Problems | Responses | Mix v3 | Majority v3 | Majority v4 | Verdict |", "|---|---|---:|---:|---|---|---|---|");
for (const x of rows) L.push(`| ${x.code} | ${x.name.replace(/\|/g, "/")} | ${x.n} | ${x.resp.toLocaleString("en-US")} | ${x.mix[0].join(" / ")} | ${SH[x.maj[0].p]} ${Math.round(100 * x.maj[0].share)}% | ${SH[x.maj[1].p]} ${Math.round(100 * x.maj[1].share)}% | ${x.verdict} |`);
fs.writeFileSync("Results/skills_and_practices.md", L.join("\n") + "\n");

const C = [["skill_code", "skill_name", "problems", "responses", ...COLS.flatMap(([, v]) => SH.map(s => `${v}_${s}`)), "majority_v3", "majority_v3_share", "majority_v4", "majority_v4_share", "verdict"].join(",")];
for (const x of rows) C.push([x.code, x.name, x.n, x.resp, ...x.mix.flat(), PRACTICES[x.maj[0].p], x.maj[0].share.toFixed(3), PRACTICES[x.maj[1].p], x.maj[1].share.toFixed(3), x.verdict].map(csvField).join(","));
fs.writeFileSync("Results/skills_and_practices.csv", C.join("\n") + "\n");
console.log(`skills ${rows.length}; acc v3 ${acc(0).toFixed(3)} v4 ${acc(1).toFixed(3)}`);
for (const v of ["one practice", "mostly", "mixed", "too few"]) { const a = count(v); console.log(v, a.length, sumN(a), allR ? (sumR(a) / allR).toFixed(3) : ""); }
