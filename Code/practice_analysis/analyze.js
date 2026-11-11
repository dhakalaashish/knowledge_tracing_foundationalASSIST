// Practice analysis of the cleaned responses with one practice per problem (default: Qwen v3 top practice).
// Answers the 21 questions in Results/practice_analysis/README section of the page; writes one JSON file.
//
// Usage (from the repo root, after clean_responses.js):
//   node --max-old-space-size=8000 Code/practice_analysis/analyze.js [practice column] [out.json]
//   defaults: qwen3_30b_v3_top_practice, Results/practice_analysis/qwen3_30b_v3.json
//
// Conventions
//   - skill of a problem = its first skill code in sorted order (90% of problems have only one)
//   - grade and domain come from that code (6.EE.B.7 -> grade 6, domain EE)
//   - school year runs August to July
//   - "residual" = score minus the problem's leave-one-out mean score (difficulty-adjusted);
//     "adjusted residual" also subtracts the student's mean residual (ability-adjusted)
//   - when a problem_id appears on several rows of Problems.csv, its first row is used

const fs = require("fs");
const path = require("path");
const { readTable } = require("../generate_practice_reasoning/tools/csv.js");

const ROOT = process.cwd();
const COL = process.argv[2] || "qwen3_30b_v3_top_practice";
const OUT = process.argv[3] || path.join(ROOT, "Results", "practice_analysis", "qwen3_30b_v3.json");
const PR = ["Representing", "Abstracting and Generalizing", "Justifying and Proving", "Mathematical Modeling",
    "Collaborative Mathematics", "Procedural Fluency"];
const SH = ["REP", "A&G", "J&P", "MOD", "COL", "PF"];
const PF = 5, NP = 6;
const R = {};                      // results
const r3 = x => (x === null || x === undefined || !isFinite(x)) ? null : Math.round(x * 1000) / 1000;
const mean = a => a.length ? a.reduce((s, x) => s + x, 0) / a.length : null;
const quant = (a, q) => { if (!a.length) return null; const s = [...a].sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(q * s.length))]; };
const zeros = () => new Array(NP).fill(0);

// ---------------------------------------------------------------- load
const P = readTable(path.join(ROOT, "Data", "Problems.csv"));
const prob = new Map();            // pid -> info
let conflicts = 0;
P.rows.forEach((r, k) => {
    const pid = r[P.h.problem_id].trim();
    const p = PR.indexOf((r[P.h[COL]] || "").trim());
    if (prob.has(pid)) { if (prob.get(pid).p !== p) conflicts++; return; }
    prob.set(pid, { pid, row: k + 1, p, set: r[P.h["Problem Set Id"]], part: Number(r[P.h["Problem Part"]]) || 0,
        type: r[P.h["Problem Type"]], ans: r[P.h["Answer Types"]],
        correct: (r[P.h["Multiple Choice Answers"]] || r[P.h["Fill-in Answers"]] || "") });
});
const S = readTable(path.join(ROOT, "Data", "Skills.csv"));
const codes = new Map();
for (const r of S.rows) {
    const pid = (r[0] || "").trim(), code = (r[2] || "").trim(), name = (r[3] || "").trim();
    if (!pid || !code || !name) continue;
    if (!codes.has(pid)) codes.set(pid, new Map());
    codes.get(pid).set(code, name);
}
for (const [pid, info] of prob) {
    const cs = codes.has(pid) ? [...codes.get(pid).keys()].sort() : [];
    info.skill = cs[0] || null;
    info.skillName = cs[0] ? codes.get(pid).get(cs[0]) : null;
    const parts = (info.skill || "").split(".");
    info.grade = parts[0] || null; info.domain = parts[1] || null;
}
const text = new Map();
for (const line of fs.readFileSync(path.join(ROOT, "Code", "generate_practice_reasoning", "problems_rendered.jsonl"), "utf8").split("\n")) {
    if (!line.trim()) continue;
    const o = JSON.parse(line); if (!text.has(String(o.problem_id))) text.set(String(o.problem_id), o.text);
}

console.error("loading responses ...");
const lines = fs.readFileSync(path.join(ROOT, "Results", "practice_analysis", "cleaned_responses.tsv"), "utf8").split("\n");
const stuIdx = new Map(), stuIds = [];
const resp = [];                   // {s, pid, info, y, hint, saw, t(ms), day, ans}
for (let i = 1; i < lines.length; i++) {
    const L = lines[i]; if (!L) continue;
    const f = L.split("\t");
    const info = prob.get(f[1]);
    if (!info || info.p < 0) throw new Error("no practice for problem " + f[1]);
    if (!stuIdx.has(f[0])) { stuIdx.set(f[0], stuIds.length); stuIds.push(f[0]); }
    const t = Date.parse(f[5].replace(" ", "T").replace(/\+00$/, "Z"));
    resp.push({ s: stuIdx.get(f[0]), info, p: info.p, y: Number(f[2]), hint: Number(f[3]), saw: Number(f[4]), t,
        day: f[5].slice(0, 10), ans: f[6] || "" });
}
lines.length = 0;
const N = resp.length, NS = stuIds.length;
console.error(`${N} responses, ${NS} students`);
R.meta = { practice_column: COL, responses: N, students: NS, problems: new Set(resp.map(x => x.info.pid)).size,
    problem_id_label_conflicts: conflicts, practices: PR, short: SH };

// problem means (leave-one-out residuals) and student means
const pSum = new Map(), pN = new Map();
for (const x of resp) { pSum.set(x.info, (pSum.get(x.info) || 0) + x.y); pN.set(x.info, (pN.get(x.info) || 0) + 1); }
for (const x of resp) { const n = pN.get(x.info); x.res = x.y - (pSum.get(x.info) - x.y) / (n - 1); }
const sRes = new Float64Array(NS), sN = new Float64Array(NS), sY = new Float64Array(NS);
for (const x of resp) { sRes[x.s] += x.res; sN[x.s]++; sY[x.s] += x.y; }
for (const x of resp) x.adj = x.res - (sRes[x.s] - x.res) / (sN[x.s] - 1);
const byStu = Array.from({ length: NS }, () => []);
for (const x of resp) byStu[x.s].push(x);         // time order is kept (file is in time order)

// ---------------------------------------------------------------- Q1, Q2: practice combinations per student
{
    const sizeCount = new Array(7).fill(0), combos = new Map(), mixBySize = Array.from({ length: 7 }, zeros);
    for (const rs of byStu) {
        const has = zeros(); for (const x of rs) has[x.p]++;
        const set = has.map((c, i) => c ? i : -1).filter(i => i >= 0);
        sizeCount[set.length]++;
        const key = set.map(i => SH[i]).join(" + ");
        combos.set(key, (combos.get(key) || 0) + 1);
        for (let i = 0; i < NP; i++) mixBySize[set.length][i] += has[i];
    }
    R.q1 = { students_by_number_of_practices: sizeCount.map((c, k) => ({ k, students: c })).filter(x => x.k > 0),
        combinations: [...combos].sort((a, b) => b[1] - a[1]).map(([combo, students]) => ({ combo, size: combo.split(" + ").length, students })) };
    R.q2 = mixBySize.map((m, k) => { const t = m.reduce((s, x) => s + x, 0); return { k, responses: t, share: m.map(x => r3(t ? x / t : null)) }; }).filter(x => x.responses > 0);
}

// ---------------------------------------------------------------- Q3: problems per student, and per practice
{
    const tot = byStu.map(rs => rs.length);
    const per = Array.from({ length: NP }, () => []);
    for (const rs of byStu) { const c = zeros(); for (const x of rs) c[x.p]++; c.forEach((v, i) => per[i].push(v)); }
    const bins = [30, 50, 100, 200, 300, 500, 750, 1000, 1e9];
    const hist = bins.slice(0, -1).map((b, i) => ({ from: b, to: bins[i + 1], students: tot.filter(v => v >= b && v < bins[i + 1]).length }));
    R.q3 = { total: { mean: r3(mean(tot)), median: quant(tot, 0.5), p10: quant(tot, 0.1), p90: quant(tot, 0.9), max: Math.max(...tot) }, histogram: hist,
        per_practice: per.map((a, i) => ({ practice: SH[i], mean: r3(mean(a)), median: quant(a, 0.5), p90: quant(a, 0.9),
            students_with_any: a.filter(v => v > 0).length, share_of_student_work_mean: r3(mean(byStu.map((rs, s) => a[s] / rs.length))) })) };
}

// ---------------------------------------------------------------- Q4: mix over problems vs responses
{
    const overResp = zeros(); for (const x of resp) overResp[x.p]++;
    const used = new Set(resp.map(x => x.info));
    const overProb = zeros(); for (const info of used) overProb[info.p]++;
    const overAll = zeros(); for (const info of prob.values()) if (info.p >= 0) overAll[info.p]++;
    const respPerProb = zeros(); PR.forEach((_, i) => respPerProb[i] = overProb[i] ? overResp[i] / overProb[i] : null);
    R.q4 = PR.map((_, i) => ({ practice: SH[i], problems_all: overAll[i], problems_answered: overProb[i], responses: overResp[i],
        share_problems_all: r3(overAll[i] / prob.size), share_problems_answered: r3(overProb[i] / used.size), share_responses: r3(overResp[i] / N),
        responses_per_problem: r3(respPerProb[i]) }));
}

// ---------------------------------------------------------------- Q5: mix by grade, domain, question type, school year
{
    const year = x => { if (!/^[0-9]{4}-[0-9]{2}/.test(x.day)) return "unknown"; const y = Number(x.day.slice(0, 4)), m = Number(x.day.slice(5, 7)); return m >= 8 ? `${y}-${String(y + 1).slice(2)}` : `${y - 1}-${String(y).slice(2)}`; };
    const group = key => {
        const m = new Map();
        for (const x of resp) { const k = key(x); if (k === null) continue; if (!m.has(k)) m.set(k, zeros()); m.get(k)[x.p]++; }
        return [...m].map(([k, c]) => { const t = c.reduce((s, v) => s + v, 0); return { group: k, responses: t, share: c.map(v => r3(v / t)) }; })
            .sort((a, b) => String(a.group).localeCompare(String(b.group), undefined, { numeric: true }));
    };
    R.q5 = { grade: group(x => x.info.grade), domain: group(x => x.info.domain).sort((a, b) => b.responses - a.responses),
        type: group(x => x.info.type).sort((a, b) => b.responses - a.responses), year: group(year) };
}

// ---------------------------------------------------------------- Q6: does skill code or problem set predict the practice?
{
    const problems = [...new Set(resp.map(x => x.info))];
    const nResp = new Map(); for (const x of resp) nResp.set(x.info, (nResp.get(x.info) || 0) + 1);
    const glob = zeros(); problems.forEach(p => glob[p.p]++);
    const globMaj = glob.indexOf(Math.max(...glob));
    const evalKey = key => {
        const g = new Map();
        for (const p of problems) { const k = key(p); if (!g.has(k)) g.set(k, zeros()); g.get(k)[p.p]++; }
        let inS = 0, loo = 0, looW = 0, totW = 0, nonPF = 0, nonPFok = 0, singles = 0;
        for (const p of problems) {
            const c = g.get(key(p)), w = nResp.get(p);
            const maj = c.indexOf(Math.max(...c)); if (maj === p.p) inS++;
            const c2 = c.slice(); c2[p.p]--;
            const n2 = c2.reduce((s, v) => s + v, 0); if (!n2) singles++;
            const m2 = n2 ? c2.indexOf(Math.max(...c2)) : globMaj;
            if (m2 === p.p) { loo++; looW += w; }
            totW += w;
            if (p.p !== PF) { nonPF++; if (m2 === p.p) nonPFok++; }
        }
        // normalized mutual information I(practice; group) / H(practice)
        const H = c => { const t = c.reduce((s, v) => s + v, 0); return -c.reduce((s, v) => s + (v ? v / t * Math.log2(v / t) : 0), 0); };
        const Hp = H(glob); let Hcond = 0;
        for (const c of g.values()) Hcond += c.reduce((s, v) => s + v, 0) / problems.length * H(c);
        return { groups: g.size, groups_with_one_problem: singles, in_sample_accuracy: r3(inS / problems.length), leave_one_out_accuracy: r3(loo / problems.length),
            leave_one_out_accuracy_by_responses: r3(looW / totW), non_pf_recall_loo: r3(nonPF ? nonPFok / nonPF : null), nmi: r3((Hp - Hcond) / Hp) };
    };
    R.q6 = { problems: problems.length, baseline_always_pf: r3(glob[PF] / problems.length),
        skill: evalKey(p => p.skill), problem_set: evalKey(p => p.set), skill_and_type: evalKey(p => p.skill + "|" + p.type), domain: evalKey(p => p.domain) };
}

// ---------------------------------------------------------------- Q7: order of practices across the parts of a problem set
{
    const sets = new Map();
    for (const p of prob.values()) { if (p.p < 0) continue; if (!sets.has(p.set)) sets.set(p.set, []); sets.get(p.set).push(p); }
    const byPart = new Map(); const trans = Array.from({ length: NP }, zeros);
    let adj = 0, adjSame = 0, expSame = 0, multi = 0, mixed = 0;
    const before = Array.from({ length: NP }, zeros);   // before[a][b]: sets where a's first part comes before b's first part
    for (const ps of sets.values()) {
        ps.sort((a, b) => a.part - b.part);
        ps.forEach((p, i) => { const k = Math.min(i + 1, 6); if (!byPart.has(k)) byPart.set(k, zeros()); byPart.get(k)[p.p]++; });
        if (ps.length < 2) continue;
        multi++;
        const c = zeros(); ps.forEach(p => c[p.p]++);
        if (c.filter(v => v).length > 1) mixed++;
        const m = ps.length;
        const pEq = c.reduce((s, v) => s + v * (v - 1), 0) / (m * (m - 1));
        for (let i = 1; i < m; i++) { adj++; trans[ps[i - 1].p][ps[i].p]++; if (ps[i - 1].p === ps[i].p) adjSame++; expSame += pEq; }
        const firstAt = new Array(NP).fill(-1); ps.forEach((p, i) => { if (firstAt[p.p] < 0) firstAt[p.p] = i; });
        for (let a = 0; a < NP; a++) for (let b = 0; b < NP; b++) if (a !== b && firstAt[a] >= 0 && firstAt[b] >= 0 && firstAt[a] < firstAt[b]) before[a][b]++;
    }
    R.q7 = { sets: sets.size, sets_with_2plus_parts: multi, sets_with_more_than_one_practice: mixed,
        share_by_part: [...byPart].sort((a, b) => a[0] - b[0]).map(([k, c]) => { const t = c.reduce((s, v) => s + v, 0); return { part: k === 6 ? "6+" : String(k), problems: t, share: c.map(v => r3(v / t)) }; }),
        adjacent_pairs: adj, adjacent_same_practice: r3(adjSame / adj), adjacent_same_if_shuffled: r3(expSame / adj),
        transitions: trans, first_before: before };
}

// ---------------------------------------------------------------- Q8: runs and switches in a student's sequence
{
    let sw = 0, pairs = 0, expSw = 0; const runLen = Array.from({ length: NP }, () => []);
    const rates = [];
    for (const rs of byStu) {
        const n = rs.length; if (n < 2) continue;
        const c = zeros(); rs.forEach(x => c[x.p]++);
        let s = 0; for (let i = 1; i < n; i++) if (rs[i].p !== rs[i - 1].p) s++;
        const e = (1 - c.reduce((a, v) => a + v * (v - 1), 0) / (n * (n - 1))) * (n - 1);
        sw += s; expSw += e; pairs += n - 1; rates.push(s / (n - 1));
        let run = 1; for (let i = 1; i <= n; i++) { if (i < n && rs[i].p === rs[i - 1].p) run++; else { runLen[rs[i - 1].p].push(run); run = 1; } }
    }
    R.q8 = { switch_rate: r3(sw / pairs), switch_rate_if_shuffled: r3(expSw / pairs), switch_rate_median_student: r3(quant(rates, 0.5)),
        run_length: runLen.map((a, i) => ({ practice: SH[i], runs: a.length, mean: r3(mean(a)), median: quant(a, 0.5), p90: quant(a, 0.9) })) };
}

// ---------------------------------------------------------------- Q9: assignment (which problem sets) vs the student
{
    // expected practice counts per problem set, over the students who started it
    const setStu = new Map();     // set -> Map(student -> counts)
    for (const x of resp) {
        const k = x.info.set; if (!setStu.has(k)) setStu.set(k, new Map());
        const m = setStu.get(k); if (!m.has(x.s)) m.set(x.s, zeros()); m.get(x.s)[x.p]++;
    }
    const setExp = new Map();
    for (const [k, m] of setStu) { const e = zeros(); let n = 0; for (const c of m.values()) { c.forEach((v, i) => e[i] += v); n++; } setExp.set(k, e.map(v => v / n)); }
    // per student: the sets they started; expected share = what a typical student does in those sets
    const stuSets = Array.from({ length: NS }, () => new Set());
    for (const x of resp) stuSets[x.s].add(x.info.set);
    const obsShare = Array.from({ length: NP }, () => new Float64Array(NS)), expShare = Array.from({ length: NP }, () => new Float64Array(NS));
    for (let s = 0; s < NS; s++) {
        const c = zeros(); byStu[s].forEach(x => c[x.p]++); const n = byStu[s].length;
        const e = zeros(); for (const k of stuSets[s]) setExp.get(k).forEach((v, i) => e[i] += v);
        const en = e.reduce((a, v) => a + v, 0);
        for (let i = 0; i < NP; i++) { obsShare[i][s] = c[i] / n; expShare[i][s] = e[i] / en; }
    }
    const res = PR.map((_, i) => {
        const y = obsShare[i], f = expShare[i], m = mean([...y]);
        let ssT = 0, ssR = 0; for (let s = 0; s < NS; s++) { ssT += (y[s] - m) ** 2; ssR += (y[s] - f[s]) ** 2; }
        return { practice: SH[i], mean_share: r3(m), sd_share: r3(Math.sqrt(ssT / NS)), explained_by_assigned_sets: r3(1 - ssR / ssT) };
    });
    // completion of sets
    let starts = 0, complete = 0;
    const setSize = new Map(); for (const p of prob.values()) setSize.set(p.set, (setSize.get(p.set) || 0) + 1);
    const setSizeAns = new Map(); for (const info of new Set(resp.map(x => x.info))) setSizeAns.set(info.set, (setSizeAns.get(info.set) || 0) + 1);
    for (const [k, m] of setStu) for (const c of m.values()) { starts++; if (c.reduce((a, v) => a + v, 0) >= setSizeAns.get(k)) complete++; }
    R.q9 = { by_practice: res, student_set_starts: starts, share_completing_all_answered_parts: r3(complete / starts) };
}

// ---------------------------------------------------------------- Q10: bursts in time
{
    const month = new Map();
    for (const x of resp) { const k = /^[0-9]{4}-[0-9]{2}/.test(x.day) ? x.day.slice(0, 7) : null; if (k === null) continue; if (!month.has(k)) month.set(k, zeros()); month.get(k)[x.p]++; }
    // student-days: non-PF counts vs binomial with the student's own non-PF rate
    const sNon = new Float64Array(NS); for (const x of resp) if (x.p !== PF) sNon[x.s]++;
    let obsVar = 0, expVar = 0, days = 0, daysNoneObs = 0, daysNoneExp = 0;
    const perDayShare = [];
    for (let s = 0; s < NS; s++) {
        const q = sNon[s] / byStu[s].length; const dm = new Map();
        for (const x of byStu[s]) { if (!dm.has(x.day)) dm.set(x.day, [0, 0]); const d = dm.get(x.day); d[0]++; if (x.p !== PF) d[1]++; }
        for (const [n, k] of dm.values()) { days++; obsVar += (k - n * q) ** 2; expVar += n * q * (1 - q); if (k === 0) daysNoneObs++; daysNoneExp += (1 - q) ** n; }
    }
    // concentration over problem sets: share of non-PF responses in the top 10% of sets by non-PF responses
    const setNon = new Map(), setAll = new Map();
    for (const x of resp) { setAll.set(x.info.set, (setAll.get(x.info.set) || 0) + 1); if (x.p !== PF) setNon.set(x.info.set, (setNon.get(x.info.set) || 0) + 1); }
    const nonCounts = [...setAll.keys()].map(k => setNon.get(k) || 0).sort((a, b) => b - a);
    const totNon = nonCounts.reduce((a, v) => a + v, 0);
    const top = f => nonCounts.slice(0, Math.ceil(f * nonCounts.length)).reduce((a, v) => a + v, 0) / totNon;
    R.q10 = { by_month: [...month].sort().map(([k, c]) => { const t = c.reduce((s, v) => s + v, 0); return { month: k, responses: t, share: c.map(v => r3(v / t)) }; }),
        student_days: days, dispersion_ratio_non_pf_per_day: r3(obsVar / expVar),
        days_without_non_pf_observed: r3(daysNoneObs / days), days_without_non_pf_if_spread: r3(daysNoneExp / days),
        problem_sets: nonCounts.length, sets_with_any_non_pf: nonCounts.filter(v => v > 0).length,
        non_pf_share_in_top_10pct_sets: r3(top(0.1)), non_pf_share_in_top_25pct_sets: r3(top(0.25)) };
}

// ---------------------------------------------------------------- Q11: difficulty by practice
{
    const y = zeros(), n = zeros(), adj = zeros();
    const sMean = s => sY[s] / sN[s];
    for (const x of resp) { y[x.p] += x.y; n[x.p]++; adj[x.p] += x.y - sMean(x.s); }
    const probMeans = Array.from({ length: NP }, () => []);
    for (const [info, sum] of pSum) probMeans[info.p].push(sum / pN.get(info));
    R.q11 = PR.map((_, i) => ({ practice: SH[i], responses: n[i], pct_correct: r3(y[i] / n[i]), vs_student_mean: r3(adj[i] / n[i]),
        problem_median_correct: r3(quant(probMeans[i], 0.5)), problem_p25: r3(quant(probMeans[i], 0.25)), problem_p75: r3(quant(probMeans[i], 0.75)) }));
}

// helper: paired difference practice X minus PF within groups keyed by key(x)
function pairedVsPF(key) {
    const g = new Map();
    for (const x of resp) { const k = key(x); if (k === null) continue; if (!g.has(k)) g.set(k, [zeros(), zeros()]); const v = g.get(k); v[0][x.p] += x.y; v[1][x.p]++; }
    return PR.map((_, i) => {
        if (i === PF) return { practice: SH[i], pairs: null, diff: 0 };
        const d = []; for (const [sum, n] of g.values()) if (n[i] && n[PF]) d.push(sum[i] / n[i] - sum[PF] / n[PF]);
        const m = mean(d), sd = d.length > 1 ? Math.sqrt(d.reduce((a, v) => a + (v - m) ** 2, 0) / (d.length - 1)) : null;
        return { practice: SH[i], pairs: d.length, diff: r3(m), se: r3(sd !== null ? sd / Math.sqrt(d.length) : null) };
    });
}

// ---------------------------------------------------------------- Q12: harder than PF on the same skill
R.q12 = { same_student_same_skill: pairedVsPF(x => x.info.skill ? x.s + "|" + x.info.skill : null),
    same_skill_problem_level: (() => {   // mean problem difficulty X minus PF within skill (each skill weighted equally)
        const g = new Map();
        for (const [info, sum] of pSum) { if (!info.skill) continue; if (!g.has(info.skill)) g.set(info.skill, [zeros(), zeros()]); const v = g.get(info.skill); v[0][info.p] += sum / pN.get(info); v[1][info.p]++; }
        return PR.map((_, i) => { if (i === PF) return { practice: SH[i], skills: null, diff: 0 }; const d = []; for (const [s, n] of g.values()) if (n[i] && n[PF]) d.push(s[i] / n[i] - s[PF] / n[PF]); return { practice: SH[i], skills: d.length, diff: r3(mean(d)) }; });
    })() };

// ---------------------------------------------------------------- Q13: controlling for question type
{
    const cell = new Map();
    for (const x of resp) { const k = x.info.type; if (!cell.has(k)) cell.set(k, [zeros(), zeros()]); const v = cell.get(k); v[0][x.p] += x.y; v[1][x.p]++; }
    R.q13 = { same_student_same_type: pairedVsPF(x => x.s + "|" + x.info.type),
        same_student_same_skill_same_type: pairedVsPF(x => x.info.skill ? x.s + "|" + x.info.skill + "|" + x.info.type : null),
        pct_correct_by_type: [...cell].map(([type, [s, n]]) => ({ type, responses: n.reduce((a, v) => a + v, 0), n: n, pct: s.map((v, i) => n[i] >= 200 ? r3(v / n[i]) : null) }))
            .sort((a, b) => b.responses - a.responses),
        practice_mix_by_type: R.q5.type };
}

// ---------------------------------------------------------------- Q14: effort (hints, answer views, time)
{
    for (const rs of byStu) for (let i = 0; i < rs.length; i++) {
        const prev = i ? rs[i - 1] : null;
        const gap = prev && isFinite(rs[i].t) && isFinite(prev.t) ? (rs[i].t - prev.t) / 60000 : null;
        rs[i].mins = gap !== null && gap >= 0 && gap <= 30 ? gap : null;    // time since the previous answer, same sitting
    }
    const agg = PR.map(() => ({ n: 0, hint: 0, hints: 0, saw: 0, mins: [] }));
    for (const x of resp) { const a = agg[x.p]; a.n++; if (x.hint > 0) a.hint++; a.hints += x.hint; a.saw += x.saw; if (x.mins !== null) a.mins.push(x.mins); }
    // within-student differences vs PF
    const within = f => { const g = Array.from({ length: NS }, () => [zeros(), zeros()]);
        for (const x of resp) { const v = f(x); if (v === null) continue; g[x.s][0][x.p] += v; g[x.s][1][x.p]++; }
        return PR.map((_, i) => { if (i === PF) return 0; const d = []; for (const [s, n] of g) if (n[i] && n[PF]) d.push(s[i] / n[i] - s[PF] / n[PF]); return r3(mean(d)); }); };
    const dHint = within(x => x.hint > 0 ? 1 : 0), dSaw = within(x => x.saw), dMin = within(x => x.mins === null ? null : Math.log(x.mins + 0.1));
    R.q14 = PR.map((_, i) => ({ practice: SH[i], responses: agg[i].n, any_hint: r3(agg[i].hint / agg[i].n), hints_per_response: r3(agg[i].hints / agg[i].n),
        saw_answer: r3(agg[i].saw / agg[i].n), median_minutes: r3(quant(agg[i].mins, 0.5)),
        within_student_vs_pf: { any_hint: dHint[i], saw_answer: dSaw[i], log_minutes: dMin[i] } }));
}

// ---------------------------------------------------------------- Q15: common wrong answers
{
    const norm = a => a.replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&gt;/g, ">").replace(/&lt;/g, "<").replace(/&amp;/g, "&").replace(/\s+/g, " ").trim().toLowerCase();
    const wrong = new Map();
    for (const x of resp) { if (x.y === 1 || x.saw || x.info.type !== "Fill-in-the-blank(s)") continue;   // free answers only: in multiple choice a dominant wrong option is forced by the few options
        const a = norm(x.ans); if (!a) continue; if (!wrong.has(x.info)) wrong.set(x.info, new Map()); const m = wrong.get(x.info); m.set(a, (m.get(a) || 0) + 1); }
    const conc = Array.from({ length: NP }, () => []); const ex = Array.from({ length: NP }, () => []);
    for (const [info, m] of wrong) {
        const tot = [...m.values()].reduce((a, v) => a + v, 0); if (tot < 20) continue;
        const [topAns, topN] = [...m].sort((a, b) => b[1] - a[1])[0];
        conc[info.p].push(topN / tot);
        ex[info.p].push({ problem_id: info.pid, row: info.row, skill: info.skill, type: info.type, wrong_responses: tot, top_wrong: topAns.slice(0, 80), top_share: r3(topN / tot),
            second: ([...m].sort((a, b) => b[1] - a[1])[1] || [""])[0].slice(0, 60),
            correct: norm(info.correct).slice(0, 80), text: (text.get(info.pid) || "").replace(/\s+/g, " ").slice(0, 260) });
    }
    R.q15 = PR.map((_, i) => ({ practice: SH[i], problems: conc[i].length, mean_top_wrong_share: r3(mean(conc[i])),
        problems_with_dominant_wrong: conc[i].filter(v => v >= 0.4).length,
        examples: ex[i].filter(e => e.top_share >= 0.3 && e.wrong_responses >= 40).sort((a, b) => b.top_share * Math.sqrt(b.wrong_responses) - a.top_share * Math.sqrt(a.wrong_responses)).slice(0, 4) }));
}

// ---------------------------------------------------------------- Q16: improvement with practice
{
    const K = 15, curve = Array.from({ length: NP }, () => Array.from({ length: K }, () => [0, 0])), slopes = Array.from({ length: NP }, () => []);
    for (const rs of byStu) {
        const seq = Array.from({ length: NP }, () => []);
        for (const x of rs) seq[x.p].push(x.adj);
        seq.forEach((a, i) => {
            if (a.length < 5) return;
            const m = mean(a);   // within-student: deviations from the student's own mean in this practice
            a.slice(0, K).forEach((v, k) => { curve[i][k][0] += v - m; curve[i][k][1]++; });
            const n = Math.min(a.length, 30), xs = [...Array(n).keys()], mx = mean(xs), my = mean(a.slice(0, n));
            let sxy = 0, sxx = 0; for (let k = 0; k < n; k++) { sxy += (k - mx) * (a[k] - my); sxx += (k - mx) ** 2; }
            slopes[i].push(sxy / sxx);
        });
    }
    R.q16 = PR.map((_, i) => ({ practice: SH[i], students: slopes[i].length, slope_per_10_problems: r3(mean(slopes[i]) * 10),
        curve: curve[i].map(([s, n], k) => ({ k: k + 1, n, dev: n >= 30 ? r3(s / n) : null })) }));
}

// ---------------------------------------------------------------- Q17: early success predicts later success?
{
    const corr = (a, b) => { const n = a.length; if (n < 20) return null; const ma = mean(a), mb = mean(b); let sab = 0, sa = 0, sb = 0;
        for (let i = 0; i < n; i++) { sab += (a[i] - ma) * (b[i] - mb); sa += (a[i] - ma) ** 2; sb += (b[i] - mb) ** 2; } return sab / Math.sqrt(sa * sb); };
    const out = [];
    for (let i = 0; i < NP; i++) {
        const e = [], l = [], ePF = [], lPF = [];
        for (const rs of byStu) {
            const a = rs.filter(x => x.p === i).map(x => x.res); if (a.length < 6) continue;
            const h = Math.floor(a.length / 2); e.push(mean(a.slice(0, h))); l.push(mean(a.slice(h)));
            if (i !== PF) {   // the same student's PF in the later half of their time
                const tMid = rs.filter(x => x.p === i)[h].t;
                const later = rs.filter(x => x.p === PF && x.t >= tMid).map(x => x.res);
                if (later.length >= 6) { ePF.push(e[e.length - 1]); lPF.push(mean(later)); }
            }
        }
        out.push({ practice: SH[i], students: e.length, same_practice_r: r3(corr(e, l)), same_practice_r_full: corr(e, l), cross_r_full: corr(ePF, lPF), students_cross: ePF.length, early_this_later_pf_r: r3(corr(ePF, lPF)) });
    }
    R.q17 = out;
}

// ---------------------------------------------------------------- Q18-Q21: skill x practice sequences
{
    const pos = Array.from({ length: NP }, () => Array.from({ length: 6 }, () => [0, 0]));
    const firstLast = Array.from({ length: NP }, () => []);
    const lift = Array.from({ length: NP }, () => ({ c: [0, 0], w: [0, 0] }));
    // Q19: previous response in four relations, by distance bucket
    const REL = ["same skill + same practice", "same skill, other practice", "other skill, same practice", "other skill + other practice"];
    const BK = [[1, 5], [6, 20], [21, 100]];
    const car = REL.map(() => BK.map(() => ({ c: [0, 0], w: [0, 0] })));
    // Q20: first response of practice B on a skill, by the practice of the student's latest earlier response on that skill
    const tr = Array.from({ length: NP + 1 }, () => Array.from({ length: NP }, () => [0, 0]));   // [prev practice or none][B]
    const trLift = Array.from({ length: NP }, () => Array.from({ length: NP }, () => ({ c: [0, 0], w: [0, 0] })));
    // Q21: order of first exposure for (student, skill) with both practice A and PF
    const order = PR.map(() => ({ aFirst: { a: [0, 0], pf: [0, 0] }, pfFirst: { a: [0, 0], pf: [0, 0] } }));
    for (const rs of byStu) {
        const pairSeq = new Map(), lastBySkill = new Map(), lastByPair = new Map(), lastByPractice = new Map();
        const seenPracticeOnSkill = new Map();
        const firstPos = new Map();   // skill -> first index per practice
        rs.forEach((x, idx) => {
            const sk = x.info.skill; if (!sk) return;
            const pk = sk + "|" + x.p;
            // Q18
            if (!pairSeq.has(pk)) pairSeq.set(pk, []);
            const seq = pairSeq.get(pk); seq.push(x.adj);
            const k = seq.length - 1; if (k < 6) { pos[x.p][k][0] += x.adj; pos[x.p][k][1]++; }
            const prevPair = lastByPair.get(pk);
            if (prevPair) { const L = lift[x.p][prevPair.y ? "c" : "w"]; L[0] += x.adj; L[1]++; }
            // Q19
            const cands = [lastByPair.get(pk), null, null, null];
            // same skill other practice: latest response on skill with a different practice
            const ls = lastBySkill.get(sk); if (ls) { for (let q = 0; q < NP; q++) if (q !== x.p && ls[q] && (!cands[1] || ls[q].i > cands[1].i)) cands[1] = ls[q]; }
            const lp = lastByPractice.get(x.p); if (lp) { for (const [s2, r2] of lp) if (s2 !== sk && (!cands[2] || r2.i > cands[2].i)) cands[2] = r2; }
            for (let j = idx - 1; j >= Math.max(0, idx - 100); j--) { const z = rs[j]; if (z.info.skill !== sk && z.p !== x.p) { cands[3] = { i: j, y: z.y }; break; } }
            cands.forEach((c, ri) => { if (!c) return; const d = idx - c.i; const b = BK.findIndex(([lo, hi]) => d >= lo && d <= hi); if (b < 0) return; const L = car[ri][b][c.y ? "c" : "w"]; L[0] += x.adj; L[1]++; });
            // Q20
            if (!seenPracticeOnSkill.has(sk)) seenPracticeOnSkill.set(sk, new Set());
            const seenP = seenPracticeOnSkill.get(sk);
            if (!seenP.has(x.p)) {
                let latest = null; if (ls) for (let q = 0; q < NP; q++) if (ls[q] && (!latest || ls[q].i > latest.i)) latest = { ...ls[q], p: q };
                const row = latest ? latest.p : NP; tr[row][x.p][0] += x.adj; tr[row][x.p][1]++;
                if (latest && latest.p !== x.p) { const L = trLift[latest.p][x.p][latest.y ? "c" : "w"]; L[0] += x.adj; L[1]++; }
                seenP.add(x.p);
            }
            // Q21
            if (!firstPos.has(sk)) firstPos.set(sk, new Array(NP).fill(-1));
            const fp = firstPos.get(sk); if (fp[x.p] < 0) fp[x.p] = idx;
            // update state
            const rec = { i: idx, y: x.y };
            lastByPair.set(pk, rec);
            if (!lastBySkill.has(sk)) lastBySkill.set(sk, new Array(NP).fill(null)); lastBySkill.get(sk)[x.p] = rec;
            if (!lastByPractice.has(x.p)) lastByPractice.set(x.p, new Map()); lastByPractice.get(x.p).set(sk, rec);
        });
        for (const [pk, seq] of pairSeq) if (seq.length >= 3) firstLast[Number(pk.split("|").pop())].push(seq[seq.length - 1] - seq[0]);
        for (const [sk, fp] of firstPos) for (let a = 0; a < NP; a++) {
            if (a === PF || fp[a] < 0 || fp[PF] < 0) continue;
            const grp = fp[a] < fp[PF] ? order[a].aFirst : order[a].pfFirst;
            for (const x of rs) if (x.info.skill === sk) { if (x.p === a) { grp.a[0] += x.adj; grp.a[1]++; } else if (x.p === PF) { grp.pf[0] += x.adj; grp.pf[1]++; } }
        }
    }
    const m2 = ([s, n]) => n ? r3(s / n) : null;
    const lf = L => L.c[1] >= 30 && L.w[1] >= 30 ? r3(L.c[0] / L.c[1] - L.w[0] / L.w[1]) : null;
    R.q18 = PR.map((_, i) => ({ practice: SH[i], by_position: pos[i].map((v, k) => ({ k: k + 1, n: v[1], dev: v[1] >= 30 ? m2(v) : null })),
        pairs_3plus: firstLast[i].length, last_minus_first: r3(mean(firstLast[i])), lift_prev_correct_vs_wrong: lf(lift[i]), lift_n: lift[i].c[1] + lift[i].w[1] }));
    R.q19 = { relations: REL, buckets: BK.map(([a, b]) => `${a}-${b}`), lift: car.map(row => row.map(lf)), n: car.map(row => row.map(L => L.c[1] + L.w[1])) };
    R.q20 = { rows: [...SH, "none"], first_response_dev: tr.map(row => row.map(v => v[1] >= 50 ? m2(v) : null)), n: tr.map(row => row.map(v => v[1])),
        lift_prev_correct_vs_wrong: trLift.map(row => row.map(lf)) };
    R.q21 = PR.map((_, i) => i === PF ? null : ({ practice: SH[i],
        practice_first: { n_a: order[i].aFirst.a[1], dev_a: m2(order[i].aFirst.a), n_pf: order[i].aFirst.pf[1], dev_pf: m2(order[i].aFirst.pf) },
        pf_first: { n_a: order[i].pfFirst.a[1], dev_a: m2(order[i].pfFirst.a), n_pf: order[i].pfFirst.pf[1], dev_pf: m2(order[i].pfFirst.pf) } })).filter(Boolean);
}

fs.writeFileSync(OUT, JSON.stringify(R, null, 1));
console.error("wrote " + OUT);
