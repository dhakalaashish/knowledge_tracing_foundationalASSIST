// How close each Qwen run is to Claude Opus 5.5 (rows 1-300), to Aashish's reviews, and to each other (all rows).
//
// Usage (from the repo root; Node only):
//   node Code/generate_practice_reasoning/tools/compare_models.js > Results/model_comparison.md
//
// Reads Data/Problems.csv (each run's <prefix>_reasoning and <prefix>_top_practice; claude_top_practice) and
// Data/problems_300.csv (claude_ordering, aashish_ordering, aashish_top_practice). A run with no answer for a row
// (it failed every attempt) counts as a disagreement for that row and is listed under the table.

const { readTable, canon, llmOrdering, PRACTICES } = require("./csv");
const RUNS = [
    { prefix: "qwen3_30b_v3", name: "Qwen3 30B, v3 prompts (no examples)" },
    { prefix: "qwen3_30b_v4", name: "Qwen3 30B, v4 prompts (with examples)" },
    { prefix: "qwen35_122b_noex", name: "Qwen3.5 122B, v3 prompts (no examples)" },
    { prefix: "qwen35_122b", name: "Qwen3.5 122B, v4 prompts (with examples)" },
    { prefix: "qwen35_122b_ch3", name: "Qwen3.5 122B, v4 prompts + NAEP Chapter 3" },
];
const N300 = 300;
const P = readTable("Data/Problems.csv"), C = readTable("Data/problems_300.csv");
const NROWS = P.rows.length;

// labels[prefix][r] = {order: [...], top} or null; Claude and Aashish for rows 1-300
const labels = {};
for (const { prefix } of RUNS) {
    labels[prefix] = P.rows.map(p => {
        const raw = (p[P.h[`${prefix}_reasoning`]] || "").trim();
        const l = raw ? llmOrdering(raw) : null;
        return l ? { order: l.order.map(canon), top: canon(p[P.h[`${prefix}_top_practice`]]) } : null;
    });
}
const split = s => (s || "").split(" > ").map(x => x.trim()).filter(Boolean).map(canon);
const claude = C.rows.map(r => ({ order: split(r[C.h.claude_ordering]), top: canon(r[C.h.claude_top_practice]) }));
const aashish = C.rows.map(r => r[C.h.aashish_top_practice] ? { order: split(r[C.h.aashish_ordering]), top: canon(r[C.h.aashish_top_practice]) } : null);

function kappa(pairs) {  // pairs: [[a, b], ...] categorical
    const n = pairs.length; if (!n) return NaN;
    const po = pairs.filter(([a, b]) => a === b).length / n;
    const ca = {}, cb = {};
    for (const [a, b] of pairs) { ca[a] = (ca[a] || 0) + 1; cb[b] = (cb[b] || 0) + 1; }
    let pe = 0; for (const k of new Set([...Object.keys(ca), ...Object.keys(cb)])) pe += ((ca[k] || 0) / n) * ((cb[k] || 0) / n);
    return pe === 1 ? 1 : (po - pe) / (1 - pe);
}
const jacc = (a, b) => { const A = new Set(a), B = new Set(b); const i = [...A].filter(x => B.has(x)).length; const u = new Set([...A, ...B]).size; return u ? i / u : 1; };
const pct = (x, n) => `${(100 * x / n).toFixed(1)}%`;
const f2 = x => x.toFixed(2), f3 = x => x.toFixed(3);
const sameSet = (a, b) => a.length === b.length && jacc(a, b) === 1;

function compare(ref, run, rows) {  // ref, run: arrays of {order, top} | null; rows: indices
    let top = 0, exact = 0, set = 0, first = 0, j = 0, lenRun = 0, lenRef = 0, n = 0, missing = 0;
    const pairs = [];
    for (const i of rows) {
        const a = ref[i]; if (!a) continue;
        n++; lenRef += a.order.length;
        const b = run[i];
        if (!b) { missing++; pairs.push([a.top, "(none)"]); continue; }
        lenRun += b.order.length;
        if (a.top === b.top) top++;
        if (a.order.join(">") === b.order.join(">")) exact++;
        if (sameSet(a.order, b.order)) set++;
        if (a.order[0] === b.order[0]) first++;
        j += jacc(a.order, b.order);
        pairs.push([a.top, b.top]);
    }
    return { n, top, exact, set, first, j: j / n, k: kappa(pairs), lenRun: lenRun / (n - missing), lenRef: lenRef / n, missing };
}
const rows300 = [...Array(N300).keys()];
const allRows = [...Array(NROWS).keys()];
const out = [];
const w = s => out.push(s);

w("# Qwen runs compared with Claude Opus 5.5, with Aashish's reviews, and with each other");
w("");
w("Made by `Code/generate_practice_reasoning/tools/compare_models.js`. Claude's labels: `claude_top_practice` and `claude_ordering` (rows 1–300). Each run's ordering is the order of `practices_used` in `<prefix>_reasoning` (answer 1 in the order of answer 2 for the three-prompt runs). v3 prompts = no example items; v4 prompts = with the NAEP example items under each practice's descriptors.");
w("");
w("## Against Claude, rows 1–300");
w("");
w("| Run | Top practice same | Cohen's κ (top) | Whole ordering same | Same set of practices | First practice same | Mean Jaccard (sets) | Practices per item (Claude: CL) |");
w("|---|---:|---:|---:|---:|---:|---:|---:|");
const vsClaude = {};
for (const R of RUNS) {
    const s = vsClaude[R.prefix] = compare(claude, labels[R.prefix], rows300);
    w(`| ${R.name} | ${s.top}/${s.n} (${pct(s.top, s.n)}) | ${f3(s.k)} | ${s.exact} (${pct(s.exact, s.n)}) | ${s.set} (${pct(s.set, s.n)}) | ${s.first} (${pct(s.first, s.n)}) | ${f2(s.j)} | ${f2(s.lenRun)} |`);
}
w("");
w(`Claude uses ${f2(vsClaude[RUNS[0].prefix].lenRef)} practices per item on average (CL).`);
const miss = RUNS.map(R => [R, rows300.filter(i => !labels[R.prefix][i])]).filter(([, m]) => m.length);
for (const [R, m] of miss) w(`- ${R.name}: no answer for row(s) ${m.map(i => i + 1).join(", ")} (failed every attempt; counted as different).`);
w("");

w("## Top practice chosen, rows 1–300");
w("");
w(`| Practice | Claude | ${RUNS.map(R => R.prefix).join(" | ")} |`);
w(`|---|---:|${RUNS.map(() => "---:").join("|")}|`);
for (const p of PRACTICES) {
    const c = claude.filter(x => x.top === p).length;
    w(`| ${p} | ${c} | ${RUNS.map(R => labels[R.prefix].slice(0, N300).filter(x => x && x.top === p).length).join(" | ")} |`);
}
w("");

w("## How often each practice is listed as used, rows 1–300");
w("");
w(`| Practice | Claude | ${RUNS.map(R => R.prefix).join(" | ")} |`);
w(`|---|---:|${RUNS.map(() => "---:").join("|")}|`);
for (const p of PRACTICES) {
    const c = claude.filter(x => x.order.includes(p)).length;
    w(`| ${p} | ${c} | ${RUNS.map(R => labels[R.prefix].slice(0, N300).filter(x => x && x.order.includes(p)).length).join(" | ")} |`);
}
w("");

w("## Orderings with Representing left out, rows 1–300");
w("");
w("The 122B runs often list only Procedural Fluency where Claude lists Representing > Procedural Fluency (reading the item's representation as a step). This table compares the orderings with Representing removed from both sides.");
w("");
w("| Run | Whole ordering same | Same with Representing left out | Differ only because Claude adds Representing | Ordering is just Procedural Fluency (Claude: 13) |");
w("|---|---:|---:|---:|---:|");
const noRep = o => o.filter(p => p !== "Representing");
const cPF = rows300.filter(i => claude[i].order.join(">") === "Procedural Fluency").length;
for (const R of RUNS) {
    let ex = 0, exNo = 0, onlyRep = 0, pf = 0, n = 0;
    for (const i of rows300) {
        const q = labels[R.prefix][i], c = claude[i]; if (!q) continue; n++;
        if (q.order.join(">") === c.order.join(">")) ex++;
        const same = noRep(q.order).join(">") === noRep(c.order).join(">");
        if (same) exNo++;
        if (same && !q.order.includes("Representing") && c.order.includes("Representing")) onlyRep++;
        if (q.order.join(">") === "Procedural Fluency") pf++;
    }
    w(`| ${R.name} | ${ex} (${pct(ex, n)}) | ${exNo} (${pct(exNo, n)}) | ${onlyRep} | ${pf} |`);
}
w("");
if (cPF !== 13) w(`(Claude's count of just-Procedural-Fluency orderings is ${cPF}.)`);

const reviewed = rows300.filter(i => aashish[i]);
w(`## Against Aashish's reviews (${reviewed.length} rows: ${reviewed.map(i => i + 1).join(", ")})`);
w("");
w("Too few rows for percentages to mean much; the counts are here so they can grow as more rows are reviewed.");
w("");
w("| Labeler | Top practice same | Whole ordering same |");
w("|---|---:|---:|");
const cA = compare(aashish, claude, rows300);
w(`| Claude Opus 5.5 | ${cA.top}/${cA.n} | ${cA.exact}/${cA.n} |`);
for (const R of RUNS) { const s = compare(aashish, labels[R.prefix], rows300); w(`| ${R.name} | ${s.top}/${s.n} | ${s.exact}/${s.n} |`); }
w("");

w(`## Runs against each other, all ${NROWS} problems`);
w("");
w("| Comparison | What changes | Top practice same | Cohen's κ (top) | Whole ordering same | Mean Jaccard (sets) |");
w("|---|---|---:|---:|---:|---:|");
const PAIRS = [
    ["qwen3_30b_v3", "qwen35_122b_noex", "model (30B → 122B), v3 prompts"],
    ["qwen3_30b_v4", "qwen35_122b", "model (30B → 122B), v4 prompts"],
    ["qwen3_30b_v3", "qwen3_30b_v4", "examples added, 30B"],
    ["qwen35_122b_noex", "qwen35_122b", "examples added, 122B"],
    ["qwen35_122b", "qwen35_122b_ch3", "NAEP Chapter 3 added, 122B"],
];
for (const [a, b, what] of PAIRS) {
    const s = compare(labels[a], labels[b], allRows);
    w(`| ${a} vs ${b} | ${what} | ${s.top}/${s.n} (${pct(s.top, s.n)}) | ${f3(s.k)} | ${s.exact} (${pct(s.exact, s.n)}) | ${f2(s.j)} |`);
}
w("");
w(`## Top practice chosen, all ${NROWS} problems`);
w("");
w(`| Practice | ${RUNS.map(R => R.prefix).join(" | ")} |`);
w(`|---|${RUNS.map(() => "---:").join("|")}|`);
for (const p of PRACTICES) w(`| ${p} | ${RUNS.map(R => { const v = labels[R.prefix].filter(x => x && x.top === p).length; return `${v} (${pct(v, NROWS)})`; }).join(" | ")} |`);
w(`| (no answer) | ${RUNS.map(R => labels[R.prefix].filter(x => !x).length).join(" | ")} |`);
w("");
w(`## How often each practice is listed as used, all ${NROWS} problems`);
w("");
w(`| Practice | ${RUNS.map(R => R.prefix).join(" | ")} |`);
w(`|---|${RUNS.map(() => "---:").join("|")}|`);
for (const p of PRACTICES) w(`| ${p} | ${RUNS.map(R => { const a = labels[R.prefix].filter(Boolean), v = a.filter(x => x.order.includes(p)).length; return `${v} (${pct(v, a.length)})`; }).join(" | ")} |`);
w(`| Practices per problem | ${RUNS.map(R => { const a = labels[R.prefix].filter(Boolean); return f2(a.reduce((s, x) => s + x.order.length, 0) / a.length); }).join(" | ")} |`);
w("");
process.stdout.write(out.join("\n") + "\n");
