// Compare Claude's practice labels (rows 1-300) with another labeler's (default: qwen3_30b_v2).
//
// Usage (from the repo root; Node only, no packages):
//   node Code/generate_practice_reasoning/tools/compare_labels.js [prefix] [name]
//   e.g. node Code/generate_practice_reasoning/tools/compare_labels.js qwen3_30b_v2 Qwen
//
// Reads:
//   Data/Problems.csv      rows 1-300: Problem Body, problem_id, predicted_practice, claude_practice_reasoning,
//                          claude_top_practice, <prefix>_reasoning (JSON answer 1), <prefix>_top_practice,
//                          <prefix>_top_practice_reasoning
//   Data/problems_300.csv  claude_ordering, claude_top_practice_reasoning
// Writes:
//   Results/claude_vs_<name>_summary.md      counts, agreement, Cohen's kappa, per-practice tables
//   Results/claude_vs_<name>_differences.md  every row where the top practice or the ordering differs,
//                                            with both labelers' reasoning side by side

const fs = require("fs");
const path = require("path");

const PREFIX = process.argv[2] || "qwen3_30b_v2";
const NAME = process.argv[3] || "Qwen";
const N = 300;
const ROOT = process.cwd();
const { readTable: readCSV, PRACTICES, canon, llmOrdering } = require("./csv");
const readTable = file => readCSV(path.join(ROOT, file));
const SHORT = { "Representing": "REP", "Abstracting and Generalizing": "A&G", "Justifying and Proving": "J&P",
    "Mathematical Modeling": "MOD", "Collaborative Mathematics": "COL", "Procedural Fluency": "PF" };

// ---------- load
const P = readTable("Data/Problems.csv");
const C = readTable("Data/problems_300.csv");
for (const col of ["problem_id", "claude_top_practice", `${PREFIX}_reasoning`, `${PREFIX}_top_practice`]) {
    if (!(col in P.h)) { console.error(`Problems.csv has no column ${col}`); process.exit(1); }
}
const items = [];
for (let r = 1; r <= N; r++) {
    const p = P.rows[r - 1], c = C.rows[r - 1];
    const pid = p[P.h.problem_id].trim();
    if (c[C.h.problem_id].trim() !== pid) { console.error(`problem_id mismatch at row ${r}`); process.exit(1); }
    const qa = llmOrdering(p[P.h[`${PREFIX}_reasoning`]]);
    if (!qa) console.error(`row ${r}: ${NAME} answer 1 is not JSON`);
    const used = qa ? qa.used : [], qOrder = qa ? qa.order : [];
    items.push({
        row: r, pid,
        body: p[P.h["Problem Body"]],
        pred: canon(p[P.h.predicted_practice]),
        cTop: canon(p[P.h.claude_top_practice]),
        cOrder: c[C.h.claude_ordering].split(" > ").map(canon),
        cA1: p[P.h.claude_practice_reasoning],
        cA2: c[C.h.claude_top_practice_reasoning],
        qTop: canon(p[P.h[`${PREFIX}_top_practice`]]),
        qOrder, qUsed: used, qNot: qa ? qa.notUsed : [],
        qA2: p[P.h[`${PREFIX}_top_practice_reasoning`]] || "",
    });
}

// ---------- statistics
function kappa(pairs, cats) {
    const n = pairs.length; let agree = 0;
    const a = {}, b = {}; cats.forEach(k => { a[k] = 0; b[k] = 0; });
    for (const [x, y] of pairs) { if (x === y) agree++; a[x] = (a[x] || 0) + 1; b[y] = (b[y] || 0) + 1; }
    const po = agree / n;
    let pe = 0; for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) pe += (a[k] || 0) * (b[k] || 0) / (n * n);
    return { n, agree, po, pe, k: pe === 1 ? 1 : (po - pe) / (1 - pe) };
}
const pct = (x, n) => `${(100 * x / n).toFixed(1)}%`;
const f3 = x => x.toFixed(3);
const kLabel = k => k < 0 ? "worse than chance" : k < 0.2 ? "slight" : k < 0.4 ? "fair" : k < 0.6 ? "moderate" : k < 0.8 ? "substantial" : "almost perfect";
const bar = (x, max, w = 30) => "█".repeat(Math.round(w * x / Math.max(max, 1)));
const sameList = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);
const sameSet = (a, b) => a.length === b.length && a.every(x => b.includes(x));
const jaccard = (a, b) => { const u = new Set([...a, ...b]); return a.filter(x => b.includes(x)).length / u.size; };
// share of practice pairs, among those both labelers use, that both put in the same relative order
function concord(a, b) {
    const common = a.filter(x => b.includes(x)); let ok = 0, tot = 0;
    for (let i = 0; i < common.length; i++) for (let j = i + 1; j < common.length; j++) {
        tot++; if ((b.indexOf(common[i]) < b.indexOf(common[j])) === true) ok++;
    }
    return tot ? { ok, tot } : null;
}

const topK = kappa(items.map(i => [i.cTop, i.qTop]), PRACTICES);
const firstK = kappa(items.map(i => [i.cOrder[0], i.qOrder[0]]), PRACTICES);
const cPredK = kappa(items.map(i => [i.cTop, i.pred]), PRACTICES);
const qPredK = kappa(items.map(i => [i.qTop, i.pred]), PRACTICES);

const ordExact = items.filter(i => sameList(i.cOrder, i.qOrder));
const ordSetOnly = items.filter(i => !sameList(i.cOrder, i.qOrder) && sameSet(i.cOrder, i.qOrder));
const ordCsubQ = items.filter(i => !sameSet(i.cOrder, i.qOrder) && i.cOrder.every(x => i.qOrder.includes(x)));
const ordQsubC = items.filter(i => !sameSet(i.cOrder, i.qOrder) && i.qOrder.every(x => i.cOrder.includes(x)));
const ordOther = items.length - ordExact.length - ordSetOnly.length - ordCsubQ.length - ordQsubC.length;
const meanJ = items.reduce((s, i) => s + jaccard(i.cOrder, i.qOrder), 0) / N;
let cOk = 0, cTot = 0; for (const i of items) { const c = concord(i.cOrder, i.qOrder); if (c) { cOk += c.ok; cTot += c.tot; } }

const topSame = items.filter(i => i.cTop === i.qTop);
const topDiff = items.filter(i => i.cTop !== i.qTop);
const ordDiff = items.filter(i => !sameList(i.cOrder, i.qOrder));
const bothSame = items.filter(i => i.cTop === i.qTop && sameList(i.cOrder, i.qOrder));

// ---------- summary markdown
const L = [];
const cnt = (arr, f) => { const m = {}; PRACTICES.forEach(p => m[p] = 0); arr.forEach(x => { const k = f(x); m[k] = (m[k] || 0) + 1; }); return m; };
L.push(`# Claude vs ${NAME}: practice labels on rows 1–${N}`, "");
L.push(`Claude: \`claude_top_practice\` and \`claude_ordering\` (Data/problems_300.csv, extracted from Claude's answer 1). ` +
    `${NAME}: \`${PREFIX}_top_practice\` and the order of \`practices_used\` in \`${PREFIX}_reasoning\`. ` +
    `Made by \`Code/generate_practice_reasoning/tools/compare_labels.js\`. Row-by-row differences: ` +
    `[claude_vs_${NAME.toLowerCase()}_differences.md](claude_vs_${NAME.toLowerCase()}_differences.md).`, "");

L.push("## Headline", "");
L.push("| Measure | Same | Different | Agreement | Cohen's κ |", "|---|---:|---:|---:|---:|");
L.push(`| Top practice | ${topK.agree} | ${N - topK.agree} | ${pct(topK.agree, N)} | ${f3(topK.k)} (${kLabel(topK.k)}) |`);
L.push(`| First practice in the ordering | ${firstK.agree} | ${N - firstK.agree} | ${pct(firstK.agree, N)} | ${f3(firstK.k)} (${kLabel(firstK.k)}) |`);
L.push(`| Whole ordering (exact) | ${ordExact.length} | ${N - ordExact.length} | ${pct(ordExact.length, N)} | – |`);
L.push(`| Top practice **and** ordering | ${bothSame.length} | ${N - bothSame.length} | ${pct(bothSame.length, N)} | – |`, "");
L.push(`κ for the top practice: observed agreement ${f3(topK.po)}, chance agreement ${f3(topK.pe)} (from each labeler's own practice frequencies), ` +
    `κ = (p_o − p_e)/(1 − p_e). Chance agreement is high because both labelers pick Procedural Fluency and Representing most of the time, ` +
    `so κ is much lower than the raw agreement.`, "");

L.push("## Top practice: how often each is chosen", "");
const cTopC = cnt(items, i => i.cTop), qTopC = cnt(items, i => i.qTop), predC = cnt(items, i => i.pred);
const maxTop = Math.max(...PRACTICES.map(p => Math.max(cTopC[p], qTopC[p])));
L.push(`| Practice | Claude | ${NAME} | predicted_practice | |`, "|---|---:|---:|---:|---|");
for (const p of PRACTICES) L.push(`| ${p} | ${cTopC[p]} | ${qTopC[p]} | ${predC[p] || 0} | \`C ${bar(cTopC[p], maxTop, 20).padEnd(20)}\`<br>\`${NAME[0]} ${bar(qTopC[p], maxTop, 20).padEnd(20)}\` |`);
L.push("");

L.push(`## Top practice: confusion matrix (rows = Claude, columns = ${NAME})`, "");
L.push(`| Claude ↓ / ${NAME} → | ${PRACTICES.map(p => SHORT[p]).join(" | ")} | Total |`, `|---|${PRACTICES.map(() => "---:").join("|")}|---:|`);
for (const a of PRACTICES) {
    const cells = PRACTICES.map(b => { const n = items.filter(i => i.cTop === a && i.qTop === b).length; return a === b ? `**${n}**` : (n || "·"); });
    L.push(`| ${a} | ${cells.join(" | ")} | ${cTopC[a]} |`);
}
L.push(`| **Total** | ${PRACTICES.map(p => qTopC[p]).join(" | ")} | ${N} |`, "");
L.push("Abbreviations: " + PRACTICES.map(p => `${SHORT[p]} = ${p}`).join(", ") + ".", "");
const pairCount = {};
for (const i of topDiff) { const k = `${i.cTop} → ${i.qTop}`; pairCount[k] = (pairCount[k] || 0) + 1; }
L.push(`Most common disagreements (Claude → ${NAME}):`, "");
Object.entries(pairCount).sort((a, b) => b[1] - a[1]).slice(0, 8).forEach(([k, v]) => L.push(`- ${k}: ${v}`));
L.push("");

L.push("## Per-practice agreement on the top practice", "");
L.push("Each practice as a yes/no question (\"is this the top practice?\").", "");
L.push(`| Practice | Both yes | Only Claude | Only ${NAME} | Both no | κ (yes/no) |`, "|---|---:|---:|---:|---:|---:|");
for (const p of PRACTICES) {
    const yy = items.filter(i => i.cTop === p && i.qTop === p).length, yn = items.filter(i => i.cTop === p && i.qTop !== p).length;
    const ny = items.filter(i => i.cTop !== p && i.qTop === p).length, nn = N - yy - yn - ny;
    const k = kappa(items.map(i => [i.cTop === p, i.qTop === p]), [true, false]);
    L.push(`| ${p} | ${yy} | ${yn} | ${ny} | ${nn} | ${yy + yn + ny === 0 ? "–" : f3(k.k)} |`);
}
L.push("");

L.push("## Orderings", "");
L.push("| Relation between the two orderings | Rows | Share |", "|---|---:|---:|");
L.push(`| Identical | ${ordExact.length} | ${pct(ordExact.length, N)} |`);
L.push(`| Same practices, different order | ${ordSetOnly.length} | ${pct(ordSetOnly.length, N)} |`);
L.push(`| ${NAME} adds practices to Claude's | ${ordCsubQ.length} | ${pct(ordCsubQ.length, N)} |`);
L.push(`| ${NAME} drops practices from Claude's | ${ordQsubC.length} | ${pct(ordQsubC.length, N)} |`);
L.push(`| Each has a practice the other lacks | ${ordOther} | ${pct(ordOther, N)} |`, "");
L.push(`- Mean Jaccard overlap of the practice sets: **${f3(meanJ)}** (1 = same practices).`);
L.push(`- Where both use two or more of the same practices, those pairs are in the same relative order **${cOk} of ${cTot}** times (${pct(cOk, cTot)}).`, "");

L.push("### Number of practices in the ordering", "");
const lenRange = [1, 2, 3, 4, 5, 6];
L.push(`| Practices | Claude | ${NAME} |`, "|---:|---:|---:|");
for (const n of lenRange) L.push(`| ${n} | ${items.filter(i => i.cOrder.length === n).length} | ${items.filter(i => i.qOrder.length === n).length} |`);
const avg = f => (items.reduce((s, i) => s + f(i).length, 0) / N).toFixed(2);
L.push(`| **mean** | ${avg(i => i.cOrder)} | ${avg(i => i.qOrder)} |`, "");

L.push("### How often each practice appears in the ordering (any position)", "");
L.push(`Per-practice κ: does each labeler say the practice is used at all?`, "");
L.push(`| Practice | Claude | ${NAME} | Both | Only Claude | Only ${NAME} | κ (used or not) |`, "|---|---:|---:|---:|---:|---:|---:|");
for (const p of PRACTICES) {
    const c = items.filter(i => i.cOrder.includes(p)).length, q = items.filter(i => i.qOrder.includes(p)).length;
    const both = items.filter(i => i.cOrder.includes(p) && i.qOrder.includes(p)).length;
    const k = kappa(items.map(i => [i.cOrder.includes(p), i.qOrder.includes(p)]), [true, false]);
    L.push(`| ${p} | ${c} | ${q} | ${both} | ${c - both} | ${q - both} | ${c + q === 0 ? "–" : f3(k.k)} |`);
}
L.push("");

L.push("### Which practice comes first", "");
const cF = cnt(items, i => i.cOrder[0]), qF = cnt(items, i => i.qOrder[0]);
L.push(`| Practice | Claude | ${NAME} |`, "|---|---:|---:|");
for (const p of PRACTICES) L.push(`| ${p} | ${cF[p]} | ${qF[p]} |`);
L.push("");

L.push("### Where the top practice sits in the labeler's own ordering", "");
const posTab = (getO, getT) => { const m = {}; for (const i of items) { const k = getO(i).indexOf(getT(i)); const key = k < 0 ? "not in ordering" : `step ${k + 1}`; m[key] = (m[key] || 0) + 1; } return m; };
const cPos = posTab(i => i.cOrder, i => i.cTop), qPos = posTab(i => i.qOrder, i => i.qTop);
const posKeys = [...new Set([...Object.keys(cPos), ...Object.keys(qPos)])].sort();
L.push(`| Position of the top practice | Claude | ${NAME} |`, "|---|---:|---:|");
for (const k of posKeys) L.push(`| ${k} | ${cPos[k] || 0} | ${qPos[k] || 0} |`);
L.push("");

L.push("## Agreement with the existing predicted_practice", "");
L.push("| Top practice vs predicted_practice | Same | Agreement | Cohen's κ |", "|---|---:|---:|---:|");
L.push(`| Claude | ${cPredK.agree} | ${pct(cPredK.agree, N)} | ${f3(cPredK.k)} |`);
L.push(`| ${NAME} | ${qPredK.agree} | ${pct(qPredK.agree, N)} | ${f3(qPredK.k)} |`, "");

L.push("## Agreement by row block", "");
L.push("| Rows | Top practice same | Ordering same |", "|---|---:|---:|");
for (let b = 0; b < N; b += 50) {
    const blk = items.slice(b, b + 50);
    L.push(`| ${b + 1}–${b + 50} | ${blk.filter(i => i.cTop === i.qTop).length} / 50 | ${blk.filter(i => sameList(i.cOrder, i.qOrder)).length} / 50 |`);
}
L.push("");

fs.writeFileSync(path.join(ROOT, `Results/claude_vs_${NAME.toLowerCase()}_summary.md`), L.join("\n"));

// ---------- differences markdown
function plain(html) {
    return (html || "").replace(/<sup>\s*([^<]*?)\s*<\/sup>/gi, "^$1").replace(/<sub>\s*([^<]*?)\s*<\/sub>/gi, "_$1")
        .replace(/<br\s*\/?>/gi, "\n").replace(/<\/(p|div|li|tr)>/gi, "\n")
        .replace(/<img[^>]*>/gi, "[image]").replace(/<[^>]+>/g, " ")
        .replace(/&nbsp;/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&#39;/g, "'")
        .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
        .replace(/&([a-z0-9]+);/gi, (m, e) => ({ sdot: "⋅", times: "×", divide: "÷", minus: "−", le: "≤", ge: "≥", ne: "≠", deg: "°",
            pi: "π", frac12: "½", frac14: "¼", frac34: "¾", middot: "·", rarr: "→", hellip: "…", ndash: "–", mdash: "—",
            rsquo: "’", lsquo: "‘", ldquo: "“", rdquo: "”", plusmn: "±", radic: "√", asymp: "≈", cent: "¢" })[e] || m)
        .replace(/[ \t]+/g, " ").replace(/\n\s*\n+/g, "\n").trim();
}
// Claude's markdown answers: demote headings so they don't break this file's structure
const demote = s => (s || "").replace(/\r/g, "").split("\n").map(l => l.replace(/^#{1,6}\s*(.*)$/, "**$1**")).join("\n").trim();
const quote = s => s.split("\n").map(l => "> " + l).join("\n");
const ord = o => o.join(" → ");

const D = [];
D.push(`# Claude vs ${NAME}: rows where they differ (rows 1–${N})`, "");
D.push(`Summary and counts: [claude_vs_${NAME.toLowerCase()}_summary.md](claude_vs_${NAME.toLowerCase()}_summary.md). ` +
    `Top practice differs on **${topDiff.length}** rows; ordering differs on **${ordDiff.length}** rows; ` +
    `**${N - bothSame.length}** rows differ in at least one. Part A lists rows where the top practice differs (most important), ` +
    `Part B rows with the same top practice but a different ordering. Claude's full answers are folded under "details".`, "");

D.push("## Index", "");
D.push(`| Row | problem_id | Claude top | ${NAME} top | Claude ordering | ${NAME} ordering |`, "|---:|---|---|---|---|---|");
for (const i of items.filter(i => i.cTop !== i.qTop || !sameList(i.cOrder, i.qOrder))) {
    const t = i.cTop === i.qTop ? i.cTop : `**${i.cTop}**`, u = i.cTop === i.qTop ? i.qTop : `**${i.qTop}**`;
    D.push(`| [${i.row}](#row-${i.row}) | ${i.pid} | ${t} | ${u} | ${ord(i.cOrder.map(p => SHORT[p]))} | ${ord(i.qOrder.map(p => SHORT[p]))} |`);
}
D.push("", "Abbreviations: " + PRACTICES.map(p => `${SHORT[p]} = ${p}`).join(", ") + ".", "");

function entry(i) {
    D.push(`### Row ${i.row}`, "", `<a id="row-${i.row}"></a>`, "");
    D.push(`problem_id ${i.pid} · predicted_practice: ${i.pred}`, "");
    D.push(quote(plain(i.body) || "(no problem text)"), "");
    D.push(`| | Claude | ${NAME} |`, "|---|---|---|");
    D.push(`| Top practice | ${i.cTop} | ${i.qTop}${i.cTop !== i.qTop ? " ⚠" : ""} |`);
    D.push(`| Ordering | ${ord(i.cOrder)} | ${ord(i.qOrder)}${sameList(i.cOrder, i.qOrder) ? "" : " ⚠"} |`, "");

    D.push("#### Top practice: why", "");
    D.push(`**Claude (${i.cTop}):**`, "", quote(demote(i.cA2)), "");
    D.push(`**${NAME} (${i.qTop}):**`, "", quote((i.qA2 || "").trim() || "(none)"), "");

    D.push("#### Ordering: why", "");
    D.push(`**${NAME}, practices used:**`, "");
    for (const u of i.qUsed) {
        D.push(`${u.order}. **${canon(u.practice)}**: ${(u.why || "").trim()}`);
        if (u.likely_errors) D.push(`   *Likely errors:* ${u.likely_errors.trim()}`);
    }
    D.push("", `**${NAME}, practices not used:** ` + i.qNot.map(n => `${canon(n.practice)} (${(n.why || "").trim()})`).join("; "), "");
    D.push(`<details><summary><b>Claude's full answer 1</b> (ordering extracted: ${ord(i.cOrder)})</summary>`, "", demote(i.cA1), "", "</details>", "");
    D.push("---", "");
}
D.push(`## Part A: top practice differs (${topDiff.length} rows)`, "");
topDiff.forEach(entry);
const partB = items.filter(i => i.cTop === i.qTop && !sameList(i.cOrder, i.qOrder));
D.push(`## Part B: same top practice, different ordering (${partB.length} rows)`, "");
partB.forEach(entry);

fs.writeFileSync(path.join(ROOT, `Results/claude_vs_${NAME.toLowerCase()}_differences.md`), D.join("\n"));

console.log(`top practice: same ${topK.agree}/${N} (${pct(topK.agree, N)}), kappa ${f3(topK.k)}`);
console.log(`first practice: same ${firstK.agree}/${N}, kappa ${f3(firstK.k)}`);
console.log(`ordering exact: ${ordExact.length}/${N}; same set other order ${ordSetOnly.length}; mean Jaccard ${f3(meanJ)}`);
console.log(`differences file: ${topDiff.length} top-practice rows + ${partB.length} ordering-only rows`);
