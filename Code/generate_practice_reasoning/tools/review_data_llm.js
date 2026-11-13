// Page data for the review page: one or more LLMs' labels for rows 1-300, written as JavaScript
// (const LLMS = [{key, name, prefix, data: [...]}, ...]). Companion to review_data.awk (PRACTICES, PROBLEMS, CLAUDE).
//
// Usage (from the repo root):
//   node Code/generate_practice_reasoning/tools/review_data_llm.js [prefix:key:name ...] > llm.js
//   default: qwen3_30b_v3:qwen_v3:"Qwen v3" qwen3_30b_v4:qwen_v4:"Qwen v4"
//   prefix: column prefix in Problems.csv; key: short id used in saved reviews; name: shown on the page
// Each data record: {row, order: [...], top, used: [{p, why, err}], not: [{p, why}], a2, ord}
// ord: the order answer of the three-prompt version, {steps: [{p, step}], why}, or null
// A row the labeler has no answer for (it failed every attempt) is {row, missing: true, order: [], top: "", ...}.

const { readTable, canon, llmOrdering } = require("./csv");
const SPECS = (process.argv.length > 2 ? process.argv.slice(2) : ["qwen3_30b_v3:qwen_v3:Qwen v3", "qwen3_30b_v4:qwen_v4:Qwen v4"])
    .map(s => { const [prefix, key, ...name] = s.split(":"); return { prefix, key: key || prefix, name: name.join(":") || prefix }; });
const N = 300;

const P = readTable("Data/Problems.csv");
function orderAnswer(text) {
    if (!text) return null;
    const o = JSON.parse(text);
    return { steps: (o.ordering || []).map(x => ({ p: canon(x.practice), step: (x.step || "").trim() })), why: (o.why || "").trim() };
}
const out = SPECS.map(({ prefix, key, name }) => {
    if (!(`${prefix}_reasoning` in P.h)) { console.error(`Problems.csv has no ${prefix}_reasoning`); process.exit(1); }
    const data = [];
    for (let r = 1; r <= N; r++) {
        const p = P.rows[r - 1];
        const raw = (p[P.h[`${prefix}_reasoning`]] || "").trim();
        if (!raw) {  // failed all its attempts for this labeler (e.g. awaiting a retry): the page shows "no answer"
            console.error(`row ${r}: no ${prefix} answer (marked missing)`);
            data.push({ row: r, missing: true, order: [], top: "", used: [], not: [], a2: "", ord: null });
            continue;
        }
        const l = llmOrdering(raw);
        if (!l) { console.error(`row ${r}: ${prefix}_reasoning is not JSON`); process.exit(1); }
        data.push({
            row: r, order: l.order, top: canon(p[P.h[`${prefix}_top_practice`]]),
            used: l.used.map(u => ({ p: canon(u.practice), why: (u.why || "").trim(), err: (u.likely_errors || "").trim() })),
            not: l.notUsed.map(u => ({ p: canon(u.practice), why: (u.why || "").trim() })),
            a2: (p[P.h[`${prefix}_top_practice_reasoning`]] || "").trim(),
            ord: orderAnswer(p[P.h[`${prefix}_ordering_reasoning`]]),
        });
    }
    console.error(`${data.length} ${prefix} records (${key}, ${name})`);
    return { key, name, prefix, data };
});
// "</" is escaped so the data can sit inside a <script> element
process.stdout.write("const LLMS = [\n" + out.map(m => JSON.stringify(m).replace(/<\//g, "<\\/")).join(",\n") + "\n];\n");
