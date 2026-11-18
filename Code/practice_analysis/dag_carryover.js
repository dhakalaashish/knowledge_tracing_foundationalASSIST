// Carry-over and transfer along the MACA-CD skill graph (prerequisite DAG), by practice.
// Question: does success on a prerequisite (or dependent) skill predict, or help, success on the linked skill, and
// more so in the same practice (e.g. a Representing problem of the child, then a Representing problem of the parent)?
//
// Usage (from the repo root): node --max-old-space-size=8000 Code/practice_analysis/dag_carryover.js [prefix] [out.json]
//   defaults: qwen35_122b_ch3, Results/practice_analysis/qwen35_122b_ch3_dag.json
//
// Graph: Code/maca_cd/data/graph/DAG_edges.json ([a, b] = a is a prerequisite of b) with the ids of
// concept_data.json (code2id: skill code -> id). A problem's skills are its skill codes (Data/Skills.csv) that are in
// the graph; its practice is its top practice in the labeling run.
// Relation of an earlier problem E to a later problem L (strongest that holds over their skill pairs):
//   same skill > prerequisite (E has a direct prerequisite of L's skill) > dependent (E has a skill that directly
//   depends on L's skill) > 2 steps up / 2 steps down (grandparent / grandchild) > unrelated, same domain >
//   unrelated, other domain.
// Score: "adjusted" = score minus the problem's leave-one-out mean, minus the student's mean of that residual on
// their other answers (as in analyze.js), so neither problem difficulty nor student ability explains differences.
// Carry-over (lift): for every later answer L and every earlier answer E of the same student up to WINDOW answers
// back: mean adjusted score of L after E was correct minus after E was wrong, by relation, distance and whether E and
// L have the same top practice. Pairs overlap (one answer pairs with many earlier ones); counts of answers are given.
// Transfer: a student's first answer on a skill, by what they did before on its prerequisites (or dependents).

const fs = require("fs");
const path = require("path");
const { readTable, canon } = require("../generate_practice_reasoning/tools/csv.js");
const PREFIX = process.argv[2] || "qwen35_122b_ch3";
const OUT = process.argv[3] || path.join("Results", "practice_analysis", `${PREFIX}_dag.json`);
const WINDOW = 300;
const PR = ["Representing", "Abstracting and Generalizing", "Justifying and Proving", "Mathematical Modeling",
    "Collaborative Mathematics", "Procedural Fluency"];
const SH = ["REP", "A&G", "J&P", "MOD", "COL", "PF"];
const REL = ["unrelated, other domain", "unrelated, same domain", "same skill", "prerequisite", "dependent", "2 steps up", "2 steps down"];
const BK = [[1, 5], [6, 20], [21, 100], [101, WINDOW]];
const bucketOf = d => d <= 5 ? 0 : d <= 20 ? 1 : d <= 100 ? 2 : 3;

// ---------------------------------------------------------------- graph
const cd = JSON.parse(fs.readFileSync("Code/maca_cd/data/graph/concept_data.json", "utf8"));
const E = JSON.parse(fs.readFileSync("Code/maca_cd/data/graph/DAG_edges.json", "utf8")).DAG;
const code2id = cd.code2id;
const id2code = Object.fromEntries(Object.entries(code2id).map(([c, i]) => [i, c]));
const par = new Map(), ch = new Map();
for (const [a, b] of E) { (par.get(b) || par.set(b, new Set()).get(b)).add(a); (ch.get(a) || ch.set(a, new Set()).get(a)).add(b); }
const gpar = new Map(), gch = new Map();   // two steps
for (const [b, ps] of par) { const g = new Set(); for (const p of ps) for (const q of par.get(p) || []) g.add(q); gpar.set(b, g); }
for (const [a, cs] of ch) { const g = new Set(); for (const c of cs) for (const d of ch.get(c) || []) g.add(d); gch.set(a, g); }

// ---------------------------------------------------------------- problems
const P = readTable("Data/Problems.csv"), S = readTable("Data/Skills.csv");
const top = new Map();
for (const r of P.rows) { const pid = r[P.h.problem_id].trim(); if (!top.has(pid)) top.set(pid, PR.indexOf(canon(r[P.h[`${PREFIX}_top_practice`]] || ""))); }
const pskills = new Map(), pdoms = new Map();
for (const r of S.rows) {
    const pid = r[0], id = code2id[r[2]];
    (pdoms.get(pid) || pdoms.set(pid, new Set()).get(pid)).add((r[2] || "").split(".")[1]);
    if (id !== undefined) (pskills.get(pid) || pskills.set(pid, new Set()).get(pid)).add(id);
}

// ---------------------------------------------------------------- responses (file is in time order across students)
const lines = fs.readFileSync("Results/practice_analysis/cleaned_responses.tsv", "utf8").split("\n");
const pidx = new Map(), plist = [];
const stu = new Map();
const R = [];  // {s, p (problem index), y}
for (let i = 1; i < lines.length; i++) {
    const L = lines[i]; if (!L) continue;
    const f = L.split("\t"); const pid = f[1];
    if (!(top.get(pid) >= 0) || !pskills.has(pid)) continue;   // needs a practice label and a skill in the graph
    if (!pidx.has(pid)) { pidx.set(pid, plist.length); plist.push(pid); }
    if (!stu.has(f[0])) stu.set(f[0], stu.size);
    R.push({ s: stu.get(f[0]), p: pidx.get(pid), y: Number(f[2]) });
}
lines.length = 0;
const NP = plist.length, NS = stu.size;
const ptop = Int8Array.from(plist.map(pid => top.get(pid)));
// adjusted scores
const pS = new Float64Array(NP), pN = new Float64Array(NP);
for (const x of R) { pS[x.p] += x.y; pN[x.p]++; }
for (const x of R) x.res = pN[x.p] > 1 ? x.y - (pS[x.p] - x.y) / (pN[x.p] - 1) : 0;
const sR = new Float64Array(NS), sN = new Float64Array(NS);
for (const x of R) { sR[x.s] += x.res; sN[x.s]++; }
for (const x of R) x.adj = sN[x.s] > 1 ? x.res - (sR[x.s] - x.res) / (sN[x.s] - 1) : 0;
const byStu = Array.from({ length: NS }, () => []);
for (const x of R) byStu[x.s].push(x);

// relation between problems (earlier e, later l), precomputed
const rel = new Int8Array(NP * NP);
const skillsOf = plist.map(pid => [...pskills.get(pid)]), domsOf = plist.map(pid => pdoms.get(pid));
for (let e = 0; e < NP; e++) for (let l = 0; l < NP; l++) {
    const A = skillsOf[e], B = skillsOf[l]; let r = -1;
    for (const b of B) {
        if (A.includes(b)) { r = 2; break; }
        for (const a of A) {
            if ((par.get(b) || new Set()).has(a)) r = Math.max(r, 30);      // ranks: same 2 handled; then 30 > 20 > 12 > 11
            else if ((ch.get(b) || new Set()).has(a)) r = Math.max(r, 20);
            else if ((gpar.get(b) || new Set()).has(a)) r = Math.max(r, 12);
            else if ((gch.get(b) || new Set()).has(a)) r = Math.max(r, 11);
        }
    }
    const code = r === 2 ? 2 : r === 30 ? 3 : r === 20 ? 4 : r === 12 ? 5 : r === 11 ? 6
        : [...domsOf[e]].some(d => domsOf[l].has(d)) ? 1 : 0;
    rel[e * NP + l] = code;
}

// ---------------------------------------------------------------- carry-over (lift) over pairs
// acc[rel][bucket][match] = [sumAdjAfterCorrect, nCorrect, sumAdjAfterWrong, nWrong]; match: 0 other practice, 1 same
const mk = () => [0, 0, 0, 0];
const acc = REL.map(() => BK.map(() => [mk(), mk()]));
const accP = REL.map(() => SH.map(() => mk()));     // same practice, by the practice (any distance up to WINDOW)
const accPo = REL.map(() => SH.map(() => mk()));    // other practice, by the later answer's practice
const answersWith = REL.map(() => [0, 0]);          // later answers with at least one such earlier answer (other / same practice)
for (const seq of byStu) {
    for (let i = 0; i < seq.length; i++) {
        const L = seq[i], seen = REL.map(() => [false, false]);
        for (let j = i - 1, d = 1; j >= 0 && d <= WINDOW; j--, d++) {
            const Ea = seq[j], r = rel[Ea.p * NP + L.p], m = ptop[Ea.p] === ptop[L.p] ? 1 : 0, b = bucketOf(d);
            const a = acc[r][b][m];
            if (Ea.y) { a[0] += L.adj; a[1]++; } else { a[2] += L.adj; a[3]++; }
            const t = m ? accP[r][ptop[L.p]] : accPo[r][ptop[L.p]];
            if (Ea.y) { t[0] += L.adj; t[1]++; } else { t[2] += L.adj; t[3]++; }
            seen[r][m] = true;
        }
        seen.forEach((v, r) => { if (v[0]) answersWith[r][0]++; if (v[1]) answersWith[r][1]++; });
    }
}
const lift = a => a[1] >= 30 && a[3] >= 30 ? a[0] / a[1] - a[2] / a[3] : null;
const r4 = x => x === null || !isFinite(x) ? null : Math.round(x * 10000) / 10000;

// ---------------------------------------------------------------- transfer: first answer on a skill
// For each student and skill, the first answer on a problem with that skill; what had the student done before on its
// prerequisites (P) or dependents (D)? Groups: none; same practice as this answer; only other practices. Plus: were
// those earlier linked answers mostly right?
const tr = { prerequisite: {}, dependent: {} };
const G = ["no earlier answer on a linked skill", "earlier linked answer in the same practice", "earlier linked answers only in other practices"];
for (const k of Object.keys(tr)) tr[k] = { groups: G.map(() => ({ n: 0, sum: 0 })), right: { n: 0, sum: 0 }, wrong: { n: 0, sum: 0 },
    by_practice: SH.map(() => G.map(() => ({ n: 0, sum: 0 }))) };
for (const seq of byStu) {
    const hist = new Map();   // skill id -> list of {top, y}
    for (const x of seq) {
        const pid = plist[x.p], tp = ptop[x.p];
        for (const b of pskills.get(pid)) {
            if (hist.has(b)) continue;   // not the first answer on b
            for (const [k, links] of [["prerequisite", par.get(b)], ["dependent", ch.get(b)]]) {
                const prev = []; for (const a of links || []) for (const h of hist.get(a) || []) prev.push(h);
                const g = !prev.length ? 0 : prev.some(h => h.top === tp) ? 1 : 2;
                const T = tr[k]; T.groups[g].n++; T.groups[g].sum += x.adj; T.by_practice[tp][g].n++; T.by_practice[tp][g].sum += x.adj;
                if (prev.length) { const m = prev.reduce((s, h) => s + h.y, 0) / prev.length; const o = m >= 0.5 ? T.right : T.wrong; o.n++; o.sum += x.adj; }
            }
        }
        for (const b of pskills.get(pid)) (hist.get(b) || hist.set(b, []).get(b)).push({ top: tp, y: x.y });
    }
}
const mean = o => o.n ? r4(o.sum / o.n) : null;

// ---------------------------------------------------------------- write
const out = {
    meta: { prefix: PREFIX, window: WINDOW, graph: { skills: Object.keys(code2id).length, edges: E.length,
        skills_with_prerequisite: par.size, skills_with_dependent: ch.size },
        responses: R.length, students: NS, problems: NP, relations: REL, buckets: BK.map(([a, b]) => `${a}–${b}`), practices: SH },
    answers_with: REL.map((r, i) => ({ relation: r, other_practice: answersWith[i][0], same_practice: answersWith[i][1] })),
    lift: REL.map((r, i) => ({ relation: r, by_bucket: BK.map((_, b) => ({ other: r4(lift(acc[i][b][0])), same: r4(lift(acc[i][b][1])),
        pairs_other: acc[i][b][0][1] + acc[i][b][0][3], pairs_same: acc[i][b][1][1] + acc[i][b][1][3] })) })),
    lift_by_practice: REL.map((r, i) => ({ relation: r, same: SH.map((_, p) => r4(lift(accP[i][p]))), other: SH.map((_, p) => r4(lift(accPo[i][p]))),
        pairs_same: SH.map((_, p) => accP[i][p][1] + accP[i][p][3]), pairs_other: SH.map((_, p) => accPo[i][p][1] + accPo[i][p][3]) })),
    transfer: Object.fromEntries(Object.entries(tr).map(([k, T]) => [k, { groups: G.map((g, i) => ({ group: g, n: T.groups[i].n, adjusted: mean(T.groups[i]) })),
        earlier_mostly_right: { n: T.right.n, adjusted: mean(T.right) }, earlier_mostly_wrong: { n: T.wrong.n, adjusted: mean(T.wrong) },
        by_practice: SH.map((p, pi) => ({ practice: p, groups: G.map((_, gi) => ({ n: T.by_practice[pi][gi].n, adjusted: mean(T.by_practice[pi][gi]) })) })) }])),
};
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.error(`wrote ${OUT}: ${R.length} responses, ${NS} students, ${NP} problems`);
