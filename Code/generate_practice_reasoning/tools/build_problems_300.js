// Build Data/problems_300.csv: Claude's and an LLM's labels for rows 1-300, plus Aashish's review columns.
//
// Usage (from the repo root):
//   node Code/generate_practice_reasoning/tools/build_problems_300.js \
//       --ordering Code/generate_practice_reasoning/tools/claude_ordering.tsv \
//       --answers <folder with Claude's r<row>_q2.md> [--llm qwen3_30b_v2] [--reviews reviews.jsonl]
//
//   --ordering  output of claude_ordering.awk (row <TAB> source <TAB> ordering ...)
//   --answers   folder with Claude's answer 2 files (the reason for its top practice)
//   --llm       column prefix of the second labeler in Problems.csv (default qwen3_30b_v2)
//   --reviews   optional: the review page's saved documents, one JSON object per line
//               ({"data": {...}} as the artifact database lists them, or the bare data). They fill the aashish_* columns.
// Aashish's columns already in Data/problems_300.csv are kept (matched by row) unless --reviews has that row.
// aashish_*_choice: both (Claude and the LLM agree and so does Aashish) | claude | <llm> | neither.

const fs = require("fs");
const path = require("path");
const { readTable, csvField, canon, llmOrdering } = require("./csv");

const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, "")] = process.argv[i + 1];
const LLM = args.llm || "qwen3_30b_v2";
const LLM_SHORT = LLM.split(/[_\d]/)[0];           // "qwen" for the choice values
const N = 300;
const OUT = "Data/problems_300.csv";
if (!args.ordering || !args.answers) { console.error("need --ordering and --answers"); process.exit(1); }

const slurp = f => fs.existsSync(f) ? fs.readFileSync(f, "utf8").replace(/\r/g, "").replace(/\n+$/, "") : "";
const ord = {};
for (const line of fs.readFileSync(args.ordering, "utf8").split(/\r?\n/)) {
    const f = line.split("\t"); if (f.length >= 3 && f[2]) ord[+f[0]] = f[2];
}

const P = readTable("Data/Problems.csv");
for (const col of ["problem_id", "predicted_practice", "claude_top_practice", `${LLM}_reasoning`, `${LLM}_top_practice`, `${LLM}_top_practice_reasoning`])
    if (!(col in P.h)) { console.error(`Problems.csv has no column ${col}`); process.exit(1); }

// Aashish's answers: from the existing CSV, then from --reviews
const mine = {};
if (fs.existsSync(OUT)) {
    const old = readTable(OUT);
    for (const r of old.rows) {
        const g = c => (c in old.h ? r[old.h[c]] : "") || "";
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
const choice = (mineVal, c, l) => !mineVal ? "" : mineVal === c && mineVal === l ? "both" : mineVal === c ? "claude" : mineVal === l ? LLM_SHORT : "neither";

const head = ["row", "problem_id", "predicted_practice", "claude_ordering", "claude_top_practice", "claude_top_practice_reasoning",
    `${LLM}_ordering`, `${LLM}_top_practice`, `${LLM}_top_practice_reasoning`,
    "aashish_ordering_choice", "aashish_ordering", "aashish_top_practice_choice", "aashish_top_practice", "aashish_note", "aashish_updated"];
const lines = [head.join(",")];
let filled = 0;
for (let r = 1; r <= N; r++) {
    const p = P.rows[r - 1], g = c => (p[P.h[c]] || "").trim();
    const pid = g("problem_id");
    if (!ord[r]) { console.error(`no claude_ordering for row ${r}`); process.exit(1); }
    const why = slurp(path.join(args.answers, `r${r}_q2.md`));
    if (!why) { console.error(`no Claude answer 2 for row ${r}`); process.exit(1); }
    const l = llmOrdering(p[P.h[`${LLM}_reasoning`]]);
    if (!l) { console.error(`row ${r}: ${LLM}_reasoning is not JSON`); process.exit(1); }
    const cOrd = ord[r], cTop = canon(g("claude_top_practice"));
    const lOrd = l.order.join(" > "), lTop = canon(g(`${LLM}_top_practice`));
    const m = mine[r];
    if (m && m.problem_id && String(m.problem_id) !== pid) { console.error(`row ${r}: review is for problem ${m.problem_id}, not ${pid}`); process.exit(1); }
    if (m) filled++;
    lines.push([r, pid, canon(g("predicted_practice")), cOrd, cTop, why, lOrd, lTop, g(`${LLM}_top_practice_reasoning`),
        m ? choice(m.aashish_ordering, cOrd, lOrd) : "", m ? m.aashish_ordering : "",
        m ? choice(m.aashish_top_practice, cTop, lTop) : "", m ? m.aashish_top_practice : "",
        m ? m.note || "" : "", m ? m.updated || "" : ""].map(csvField).join(","));
}
fs.writeFileSync(OUT, lines.join("\n") + "\n");
console.error(`${N} rows written to ${OUT}; ${filled} with Aashish's review`);
