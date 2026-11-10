// Page data for the review page: an LLM's labels for rows 1-300, written as JavaScript (const LLM = [...]).
// Companion to review_data.awk (PRACTICES, PROBLEMS, CLAUDE).
//
// Usage (from the repo root):
//   node Code/generate_practice_reasoning/tools/review_data_llm.js [prefix] > llm.js
//   prefix: column prefix in Problems.csv (default qwen3_30b_v3)
// Each record: {row, order: [...], top, used: [{p, why, err}], not: [{p, why}], a2, ord}
// ord: the order answer of the three-prompt version, {steps: [{p, step}], why}, or null

const { readTable, canon, llmOrdering } = require("./csv");
const PREFIX = process.argv[2] || "qwen3_30b_v3";
const N = 300;

const P = readTable("Data/Problems.csv");
function orderAnswer(text) {
    if (!text) return null;
    const o = JSON.parse(text);
    return { steps: (o.ordering || []).map(x => ({ p: canon(x.practice), step: (x.step || "").trim() })), why: (o.why || "").trim() };
}
const recs = [];
for (let r = 1; r <= N; r++) {
    const p = P.rows[r - 1];
    const l = llmOrdering(p[P.h[`${PREFIX}_reasoning`]]);
    if (!l) { console.error(`row ${r}: ${PREFIX}_reasoning is not JSON`); process.exit(1); }
    recs.push({
        row: r, order: l.order, top: canon(p[P.h[`${PREFIX}_top_practice`]]),
        used: l.used.map(u => ({ p: canon(u.practice), why: (u.why || "").trim(), err: (u.likely_errors || "").trim() })),
        not: l.notUsed.map(u => ({ p: canon(u.practice), why: (u.why || "").trim() })),
        a2: (p[P.h[`${PREFIX}_top_practice_reasoning`]] || "").trim(),
        ord: orderAnswer(p[P.h[`${PREFIX}_ordering_reasoning`]]),
    });
}
// "</" is escaped so the data can sit inside a <script> element
process.stdout.write("const LLM_PREFIX = " + JSON.stringify(PREFIX) + ";\nconst LLM = [\n" +
    recs.map(x => JSON.stringify(x).replace(/<\//g, "<\\/")).join(",\n") + "\n];\n");
console.error(`${recs.length} ${PREFIX} records`);
