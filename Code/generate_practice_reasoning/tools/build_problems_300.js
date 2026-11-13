// Build Data/problems_300.csv: Claude's and the LLMs' labels for rows 1-300, plus Aashish's review columns.
//
// Usage (from the repo root):
//   node Code/generate_practice_reasoning/tools/build_problems_300.js \
//       --ordering Code/generate_practice_reasoning/tools/claude_ordering.tsv \
//       [--answers <folder with Claude's r<row>_q2.md>] [--llm qwen3_30b_v3:qwen_v3,qwen3_30b_v4:qwen_v4] [--reviews reviews.jsonl]
//
//   --ordering  output of claude_ordering.awk (row <TAB> source <TAB> ordering ...)
//   --answers   folder with Claude's answer 2 files (the reason for its top practice); without it, that text is
//               taken from the existing Data/problems_300.csv
//   --llm       the other labelers, comma-separated prefix:key (default qwen3_30b_v3:qwen_v3,qwen3_30b_v4:qwen_v4)
//   --reviews   optional: the review page's saved documents, one JSON object per line
//               ({"data": {...}} as the artifact database lists them, or the bare data). They fill the aashish_* columns.
// Aashish's columns already in Data/problems_300.csv are kept (matched by row) unless --reviews has that row.
// aashish_*_choice: which labelers Aashish's answer matches: all | none | keys joined with + (e.g. claude+qwen_v3).

const fs = require("fs");
const path = require("path");
const { readTable, csvField, canon, llmOrdering } = require("./csv");

const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, "")] = process.argv[i + 1];
const LLMS = (args.llm || "qwen3_30b_v3:qwen_v3,qwen3_30b_v4:qwen_v4").split(",").map(x => { const [prefix, key] = x.split(":"); return { prefix, key: key || prefix }; });
const N = 300;
const OUT = "Data/problems_300.csv";
if (!args.ordering) { console.error("need --ordering"); process.exit(1); }

const slurp = f => fs.existsSync(f) ? fs.readFileSync(f, "utf8").replace(/\r/g, "").replace(/\n+$/, "") : "";
const ord = {};
for (const line of fs.readFileSync(args.ordering, "utf8").split(/\r?\n/)) {
    const f = line.split("\t"); if (f.length >= 3 && f[2]) ord[+f[0]] = f[2];
}

const P = readTable("Data/Problems.csv");
for (const col of ["problem_id", "predicted_practice", "claude_top_practice", ...LLMS.flatMap(L => [`${L.prefix}_reasoning`, `${L.prefix}_top_practice`, `${L.prefix}_top_practice_reasoning`])])
    if (!(col in P.h)) { console.error(`Problems.csv has no column ${col}`); process.exit(1); }

// Aashish's answers: from the existing CSV, then from --reviews. Without --answers, Claude's answer 2 also comes
// from the existing CSV (claude_top_practice_reasoning), so the file can be rebuilt with other LLM columns.
const mine = {}, claudeWhy = {};
if (fs.existsSync(OUT)) {
    const old = readTable(OUT);
    for (const r of old.rows) {
        const g = c => (c in old.h ? r[old.h[c]] : "") || "";
        claudeWhy[+g("row")] = g("claude_top_practice_reasoning");
        if (g("aashish_ordering") || g("aashish_top_practice"))
            mine[+g("row")] = { problem_id: g("problem_id"), aashish_ordering: g("aashish_ordering"), aashish_top_practice: g("aashish_top_practice"), note: g("aashish_note"), updated: g("aashish_updated") };
    }
}
if (args.reviews) {
    for (const line of fs.readFileSync(args.reviews, "utf8").split(/\r?\n/)) {
        if (!line.trim()) continue;
        const o = JSON.parse(line), d = o.data || o;
        if (d.row) mine[+d.row] = d;
    }
}
// vals: [[key, value], ...] for Claude and each LLM; a labeler with no answer for the row (value "") is left out
const choice = (mineVal, vals) => {
    if (!mineVal) return "";
    const have = vals.filter(([, v]) => v), ks = have.filter(([, v]) => v === mineVal).map(([k]) => k);
    return ks.length === have.length ? "all" : ks.length ? ks.join("+") : "none";
};

const head = ["row", "problem_id", "predicted_practice", "claude_ordering", "claude_top_practice", "claude_top_practice_reasoning",
    ...LLMS.flatMap(L => [`${L.prefix}_ordering`, `${L.prefix}_top_practice`, `${L.prefix}_top_practice_reasoning`]),
    "aashish_ordering_choice", "aashish_ordering", "aashish_top_practice_choice", "aashish_top_practice", "aashish_note", "aashish_updated"];
const lines = [head.join(",")];
let filled = 0;
for (let r = 1; r <= N; r++) {
    const p = P.rows[r - 1], g = c => (p[P.h[c]] || "").trim();
    const pid = g("problem_id");
    if (!ord[r]) { console.error(`no claude_ordering for row ${r}`); process.exit(1); }
    const why = args.answers ? slurp(path.join(args.answers, `r${r}_q2.md`)) : (claudeWhy[r] || "");
    if (!why) { console.error(`no Claude answer 2 for row ${r}`); process.exit(1); }
    const cOrd = ord[r], cTop = canon(g("claude_top_practice"));
    const ls = LLMS.map(L => {
        const raw = g(`${L.prefix}_reasoning`);
        if (!raw) {  // the problem failed all its attempts for this labeler (e.g. awaiting a retry): empty columns
            console.error(`row ${r}: no ${L.prefix} answer (left empty)`);
            return { key: L.key, ord: "", top: "", why: "" };
        }
        const l = llmOrdering(raw);
        if (!l) { console.error(`row ${r}: ${L.prefix}_reasoning is not JSON`); process.exit(1); }
        return { key: L.key, ord: l.order.join(" > "), top: canon(g(`${L.prefix}_top_practice`)), why: g(`${L.prefix}_top_practice_reasoning`) };
    });
    const ordVals = [["claude", cOrd], ...ls.map(x => [x.key, x.ord])], topVals = [["claude", cTop], ...ls.map(x => [x.key, x.top])];
    const m = mine[r];
    if (m && m.problem_id && String(m.problem_id) !== pid) { console.error(`row ${r}: review is for problem ${m.problem_id}, not ${pid}`); process.exit(1); }
    if (m) filled++;
    lines.push([r, pid, canon(g("predicted_practice")), cOrd, cTop, why, ...ls.flatMap(x => [x.ord, x.top, x.why]),
        m ? choice(m.aashish_ordering, ordVals) : "", m ? m.aashish_ordering : "",
        m ? choice(m.aashish_top_practice, topVals) : "", m ? m.aashish_top_practice : "",
        m ? m.note || "" : "", m ? m.updated || "" : ""].map(csvField).join(","));
}
fs.writeFileSync(OUT, lines.join("\n") + "\n");
console.error(`${N} rows written to ${OUT}; ${filled} with Aashish's review`);
