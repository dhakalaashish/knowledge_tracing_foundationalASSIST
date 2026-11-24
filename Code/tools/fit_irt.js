// Fit a two-parameter logistic IRT model (2PL) to the first answers of the students OUTSIDE the paper's 500, so no
// test student's answers are used (the same students as Results/kt_profile/problem_difficulty.json). The "irt"
// condition of kt_practice_benchmark.py reads the result.
//
//   P(right) = 1 / (1 + exp(-a * (theta - b)))
//   theta: student ability, b: item difficulty, a: item discrimination
//
// One answer per (student, problem): the earliest; right = discrete_score >= 1 (as the difficulty file).
// MAP fit by full-batch Adam with priors theta ~ N(0, 1), b ~ N(0, 2^2), log a ~ N(0, 0.7^2); afterwards the scale
// is fixed so that the abilities of the fitted students have mean 0 and standard deviation 1 (b and a rescaled
// with them), so "average student" and "one standard deviation" mean exactly that.
// Problems with fewer than MIN_RESPONSES answers get no parameters.
//
//   node Code/tools/fit_irt.js            -> Results/kt_profile/problem_irt.json
//
// (The paper's own IRT file, Results/pedagogical_grounding/output/irt_parameters.json, was fitted on all students,
// the paper's 500 included, with py-irt's vague priors and no fixed ability scale, so it is not used here.)

const fs = require("fs");
const path = require("path");

const REPO = path.resolve(__dirname, "..", "..");
const INTERACTIONS = path.join(REPO, "Data", "Interactions.csv");
const PAPER_IDS = path.join(REPO, "Results", "paper_reference", "paper_user_ids.txt");
const OUT = path.join(REPO, "Results", "kt_profile", "problem_irt.json");
const MIN_RESPONSES = 30;
const ITERS = 600, LR = 0.05;
const SD_B = 2, SD_LOGA = 0.7;

// ------------------------------------------------------------------ CSV (quoted fields, commas and newlines inside)
function* csvRows(text) {
  let i = 0, field = "", row = [], q = false;
  const n = text.length;
  while (i < n) {
    const c = text[i];
    if (q) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i += 2; continue; }
        q = false; i++; continue;
      }
      field += c; i++; continue;
    }
    if (c === '"') { q = true; i++; continue; }
    if (c === ",") { row.push(field); field = ""; i++; continue; }
    if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); field = ""; yield row; row = []; i++; continue;
    }
    field += c; i++;
  }
  if (field !== "" || row.length) { row.push(field); yield row; }
}

const paper = new Set(fs.readFileSync(PAPER_IDS, "utf8").split(/\r?\n/).map(s => s.trim()).filter(Boolean));
console.log(`paper students excluded: ${paper.size}`);

const text = fs.readFileSync(INTERACTIONS, "utf8");
const rows = csvRows(text);
const header = rows.next().value;
const col = name => { const k = header.indexOf(name); if (k < 0) throw new Error("no column " + name); return k; };
const cPid = col("problem_id"), cUser = col("user_id"), cScore = col("discrete_score"), cTime = col("end_time");

const first = new Map();   // user \t pid -> [time, right]
let total = 0;
for (const r of rows) {
  if (r.length < header.length) continue;
  const user = r[cUser].trim();
  if (!user || paper.has(user)) continue;
  const s = r[cScore].trim();
  if (s === "" || s.toLowerCase() === "nan") continue;
  total++;
  const key = user + "\t" + r[cPid].trim();
  const t = r[cTime];
  const prev = first.get(key);
  if (!prev || t < prev[0]) first.set(key, [t, parseFloat(s) >= 1 ? 1 : 0]);
}
console.log(`answers outside the paper's students: ${total.toLocaleString()}; first answers per (student, problem): ${first.size.toLocaleString()}`);

// items with enough answers
const itemCount = new Map();
for (const key of first.keys()) { const pid = key.split("\t")[1]; itemCount.set(pid, (itemCount.get(pid) || 0) + 1); }
const items = [...itemCount].filter(([, c]) => c >= MIN_RESPONSES).map(([p]) => p);
const itemIdx = new Map(items.map((p, i) => [p, i]));
const userIdx = new Map();
const S = [], I = [], Y = [];
for (const [key, [, y]] of first) {
  const [user, pid] = key.split("\t");
  const j = itemIdx.get(pid);
  if (j === undefined) continue;
  let u = userIdx.get(user);
  if (u === undefined) { u = userIdx.size; userIdx.set(user, u); }
  S.push(u); I.push(j); Y.push(y);
}
const N = S.length, NU = userIdx.size, NI = items.length;
console.log(`fitting on ${N.toLocaleString()} answers: ${NU.toLocaleString()} students, ${NI.toLocaleString()} problems (>= ${MIN_RESPONSES} answers each)`);

const s = Int32Array.from(S), it = Int32Array.from(I), y = Float64Array.from(Y);
const theta = new Float64Array(NU), b = new Float64Array(NI), la = new Float64Array(NI);
// start b at -logit(share right)
{
  const right = new Float64Array(NI), cnt = new Float64Array(NI);
  for (let k = 0; k < N; k++) { right[it[k]] += y[k]; cnt[it[k]]++; }
  for (let j = 0; j < NI; j++) { const p = Math.min(0.99, Math.max(0.01, right[j] / cnt[j])); b[j] = Math.log((1 - p) / p); }
}
const params = [theta, b, la];
const m = params.map(p => new Float64Array(p.length)), v = params.map(p => new Float64Array(p.length));
const g = params.map(p => new Float64Array(p.length));
const B1 = 0.9, B2 = 0.999, EPS = 1e-8;

function logLik() {
  let ll = 0;
  for (let k = 0; k < N; k++) {
    const z = Math.exp(la[it[k]]) * (theta[s[k]] - b[it[k]]);
    ll += y[k] ? -Math.log1p(Math.exp(-z)) : -Math.log1p(Math.exp(z));
  }
  return ll / N;
}

for (let step = 1; step <= ITERS; step++) {
  for (const x of g) x.fill(0);
  for (let k = 0; k < N; k++) {
    const u = s[k], j = it[k], a = Math.exp(la[j]);
    const d = theta[u] - b[j];
    const p = 1 / (1 + Math.exp(-a * d));
    const r = y[k] - p;
    g[0][u] += r * a;
    g[1][j] -= r * a;
    g[2][j] += r * a * d;
  }
  for (let u = 0; u < NU; u++) g[0][u] -= theta[u];
  for (let j = 0; j < NI; j++) { g[1][j] -= b[j] / (SD_B * SD_B); g[2][j] -= la[j] / (SD_LOGA * SD_LOGA); }
  // Adam, ascent; per-parameter step (counts differ a lot between students and items)
  for (let q = 0; q < 3; q++) {
    const P = params[q], G = g[q], M = m[q], V = v[q];
    for (let k = 0; k < P.length; k++) {
      M[k] = B1 * M[k] + (1 - B1) * G[k];
      V[k] = B2 * V[k] + (1 - B2) * G[k] * G[k];
      const mh = M[k] / (1 - B1 ** step), vh = V[k] / (1 - B2 ** step);
      P[k] += LR * mh / (Math.sqrt(vh) + EPS);
    }
  }
  if (step % 100 === 0 || step === 1) console.log(`  step ${step}: mean log-likelihood ${logLik().toFixed(5)}`);
}

// fix the scale: abilities mean 0, sd 1
let mean = 0; for (const t of theta) mean += t; mean /= NU;
let sd = 0; for (const t of theta) sd += (t - mean) ** 2; sd = Math.sqrt(sd / NU);
const out = {};
const right = new Float64Array(NI), cnt = new Float64Array(NI);
for (let k = 0; k < N; k++) { right[it[k]] += y[k]; cnt[it[k]]++; }
for (let j = 0; j < NI; j++) {
  const bb = (b[j] - mean) / sd, aa = Math.exp(la[j]) * sd;
  out[items[j]] = [+bb.toFixed(4), +aa.toFixed(4), cnt[j], +(right[j] / cnt[j]).toFixed(4)];
}

// checks: predicted vs observed share right for an average student is not the same thing, so compare the
// model's mean predicted share right per item (over its own answerers) with the observed share
let err = 0;
const predRight = new Float64Array(NI);
for (let k = 0; k < N; k++) {
  const j = it[k];
  const t = (theta[s[k]] - mean) / sd;
  const [bb, aa] = out[items[j]];
  predRight[j] += 1 / (1 + Math.exp(-aa * (t - bb)));
}
for (let j = 0; j < NI; j++) err += Math.abs(predRight[j] / cnt[j] - right[j] / cnt[j]);
const as = Object.values(out).map(o => o[1]).sort((x, z) => x - z);
const bs = Object.values(out).map(o => o[0]).sort((x, z) => x - z);
const q = (arr, f) => arr[Math.floor(f * (arr.length - 1))].toFixed(2);
console.log(`mean |predicted - observed share right| per problem: ${(err / NI).toFixed(4)}`);
console.log(`b quartiles: ${q(bs, 0.05)} / ${q(bs, 0.25)} / ${q(bs, 0.5)} / ${q(bs, 0.75)} / ${q(bs, 0.95)} (5%,25%,50%,75%,95%)`);
console.log(`a quartiles: ${q(as, 0.05)} / ${q(as, 0.25)} / ${q(as, 0.5)} / ${q(as, 0.75)} / ${q(as, 0.95)}`);

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify({
  meta: {
    model: "2PL: P(right) = 1 / (1 + exp(-a * (theta - b))); theta of the fitted students has mean 0 and sd 1",
    fit: `MAP, full-batch Adam, ${ITERS} steps, lr ${LR}; priors theta ~ N(0,1), b ~ N(0,${SD_B}^2), log a ~ N(0,${SD_LOGA}^2)`,
    answers: N, students: NU, problems: NI, min_responses: MIN_RESPONSES,
    first_answer: "the earliest answer per (student, problem); right = discrete_score >= 1",
    excluded: "the paper's 500 students (Results/paper_reference/paper_user_ids.txt)",
    columns: ["b (difficulty)", "a (discrimination)", "answers", "share right"],
    script: "Code/tools/fit_irt.js",
  },
  problems: out,
}));
console.log(`wrote ${OUT}`);
