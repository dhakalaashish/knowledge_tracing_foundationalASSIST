// Read a KT benchmark run (kt_practice_benchmark.py) student by student: for each prediction, the problem, what the
// student answered, what each condition predicted, the student profile the profile model read, and every model's
// reasoning. Writes one self-contained HTML page.
//
// Usage (from the repo root; Node only, no packages):
//   node Code/tools/kt_student_view.js [--dir Results/kt_practice_main] [--users id1,id2 | --n 2 --seed 7] [--out file.html]
//
// Reads, in --dir, whichever of these exist (plain .jsonl or .jsonl.gz; *_slim.* files have no prompts):
//   paper_qwen3next80b_instruct_bf16_n*.jsonl   the paper's published predictions (BF16)
//   baseline_qwen3next80b_awq_bin10_hist50[_slim].jsonl
//   practice_qwen3next80b_awq_bin10_hist50[_slim].jsonl
//   profile_qwen3next80b_awq_bin10_hist50.jsonl   (with prompts: the profile text comes from them)
// Answers are matched as evaluate_kt.answers_match does (exact, MC letters in any order, numbers within 1%).

const fs = require("fs");
const path = require("path");
const zlib = require("zlib");
const readline = require("readline");

const argv = process.argv.slice(2);
const opt = (name, dflt) => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : dflt; };
const DIR = opt("--dir", path.join("Results", "kt_practice_main"));
const OUT = opt("--out", path.join(DIR, "student_view.html"));
const N = Number(opt("--n", 2));
const SEED = Number(opt("--seed", 7));
const USERS_ARG = opt("--users", "");

const RUNS = [
    ["paper", "Paper (BF16, published)", /^paper_qwen3next80b_instruct_bf16_n\d+(_slim)?\.jsonl(\.gz)?$/],
    ["baseline", "Baseline (paper prompts)", /^baseline_qwen3next80b_awq_bin10_hist50(_slim)?\.jsonl(\.gz)?$/],
    ["practice", "Practice (+ labels, full history)", /^practice_qwen3next80b_awq_bin10_hist50(_slim)?\.jsonl(\.gz)?$/],
    ["profile", "Profile (profile + last 10)", /^profile_qwen3next80b_awq_bin10_hist50(_slim)?\.jsonl(\.gz)?$/],
];

// ------------------------------------------------------------------ answer matching (evaluate_kt.answers_match)
function normMcq(s) {
    const parts = s.split(",").map(p => p.trim().toUpperCase()).filter(Boolean);
    return parts.length && parts.every(p => /^[A-Z]$/.test(p)) ? [...new Set(parts)].sort().join(", ") : s;
}
const FLOAT = /^[+-]?(\d+(_\d+)*\.?(\d+(_\d+)*)?|\.\d+)([eE][+-]?\d+)?$/;
function numMatch(a, b) {
    a = a.trim(); b = b.trim();
    if (!FLOAT.test(a) || !FLOAT.test(b)) return false;
    const x = Number(a.replace(/_/g, "")), y = Number(b.replace(/_/g, ""));
    return Math.abs(x - y) <= Math.max(0.01 * Math.max(Math.abs(x), Math.abs(y)), 0.01);
}
function answersMatch(pred, actual) {
    if (pred === null || pred === undefined || actual === null || actual === undefined) return false;
    const p = String(pred).trim(), a = String(actual).trim();
    return p === a || normMcq(p) === normMcq(a) || numMatch(p, a);
}
const missing = v => v === null || v === undefined || (typeof v === "number" && Number.isNaN(v)) || String(v) === "nan" || String(v) === "";

// ------------------------------------------------------------------ reading
function lines(file) {
    let stream = fs.createReadStream(file);
    if (file.endsWith(".gz")) stream = stream.pipe(zlib.createGunzip());
    return readline.createInterface({ input: stream, crlfDelay: Infinity });
}
const userOf = line => { const m = /^\{"prediction_id":\s*"([^"]+)_\d+_(?:correct|incorrect)"/.exec(line.slice(0, 200)); return m && m[1]; };

function pickFile(re) {
    const names = fs.readdirSync(DIR).filter(n => re.test(n));
    // prefer a full file (with prompts) over a slim one, plain over gz
    names.sort((a, b) => (a.includes("_slim") - b.includes("_slim")) || (a.endsWith(".gz") - b.endsWith(".gz")));
    return names[0] ? path.join(DIR, names[0]) : null;
}

function seededShuffle(arr, seed) {
    let s = seed >>> 0;
    const rnd = () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
}

async function main() {
    const files = RUNS.map(([key, label, re]) => ({ key, label, file: pickFile(re) })).filter(r => r.file);
    if (!files.length) throw new Error(`no result files found in ${DIR}`);
    let users;
    if (USERS_ARG) users = USERS_ARG.split(",").map(s => s.trim()).filter(Boolean);
    else {
        const ids = fs.readFileSync(path.join(DIR, "user_ids.txt"), "utf8").split(/\r?\n/).map(s => s.trim()).filter(Boolean);
        users = seededShuffle(ids, SEED).slice(0, N);
    }
    const want = new Set(users);
    const data = {};        // user -> prediction_id -> {key: record}
    for (const r of files) {
        process.stdout.write(`reading ${r.file} ... `);
        let n = 0;
        for await (const line of lines(r.file)) {
            const u = userOf(line);
            if (!u || !want.has(u)) continue;
            let rec;
            try { rec = JSON.parse(line); }   // Python writes NaN / Infinity, which JSON.parse refuses
            catch { rec = JSON.parse(line.replace(/([:\[,]\s*)-?(NaN|Infinity)(?=\s*[,}\]])/g, "$1null")); }
            if (r.key !== "profile") delete rec.prompt;
            ((data[u] ||= {})[rec.prediction_id] ||= {})[r.key] = rec;
            n++;
        }
        console.log(`${n} predictions for the chosen students`);
    }
    fs.writeFileSync(OUT, page(users, files, data), "utf8");
    console.log(`\nStudents: ${users.join(", ")}\nWrote ${OUT}`);
}

// ------------------------------------------------------------------ page
const esc = s => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const between = (text, a, b) => { const i = text.indexOf(a); if (i < 0) return ""; const j = b ? text.indexOf(b, i + a.length) : -1; return text.slice(i, j < 0 ? undefined : j).trim(); };
const ktHit = r => r && !missing(r.predicted_question_level) && Number(r.predicted_question_level) === Number(r.actual_score);
const trulyWrong = r => r.prediction_type === "incorrect" && (missing(r.correct_answer) || !answersMatch(r.actual_answer, r.correct_answer));

function mark(ok, unparsed) { return unparsed ? '<span class="na">no parse</span>' : ok ? '<span class="ok">✓</span>' : '<span class="no">✗</span>'; }

function studentSection(u, files, preds) {
    const ids = Object.keys(preds).sort((a, b) => {
        const pa = a.split("_"), pb = b.split("_");
        return (Number(pa.at(-2)) - Number(pb.at(-2))) || pa.at(-1).localeCompare(pb.at(-1));
    });
    const any = id => { const p = preds[id]; return p.profile || p.baseline || p.practice || p.paper; };
    // summary per condition
    const sum = files.map(f => {
        let n = 0, kt = 0, wn = 0, cog = 0;
        for (const id of ids) {
            const r = preds[id][f.key];
            if (!r) continue;
            n++; kt += ktHit(r);
            if (trulyWrong(r)) { wn++; cog += answersMatch(r.predicted_student_answer, r.actual_answer); }
        }
        return `<tr><td>${esc(f.label)}</td><td>${n}</td><td>${n ? Math.round(100 * kt / n) : "–"}% (${kt}/${n})</td>`
            + `<td>${wn ? Math.round(100 * cog / wn) : "–"}% (${cog}/${wn})</td></tr>`;
    }).join("");
    // the profile over time: one row per bin (from the profile prompts)
    const seenBins = new Set();
    const evo = ids.filter(id => preds[id].profile?.prompt).filter(id => {
        const b = id.split("_").at(-2); if (seenBins.has(b)) return false; seenBins.add(b); return true;
    }).map(id => {
        const r = preds[id].profile, prof = between(r.prompt, "**Student Profile**", "**Student's ");
        const overall = (prof.match(/^Overall: .*$/m) || [""])[0].replace(/^Overall: /, "");
        const skill = (between(prof, "Skill of the new problem:", "Prerequisite skills") || between(prof, "Skills of the new problem:", "Prerequisite skills"))
            .split("\n").slice(1, 2).join(" ").replace(/^- /, "");
        return `<tr><td>${r.bin_number}</td><td>${r.history_size}</td><td>${esc(overall)}</td><td>${esc(skill)}</td></tr>`;
    }).join("");
    const cards = ids.map(id => {
        const p = preds[id], r0 = any(id);
        const hasWrong = trulyWrong(r0);
        const rows = files.map(f => {
            const r = p[f.key];
            if (!r) return `<tr><td>${esc(f.label)}</td><td colspan="4" class="na">not in this run</td></tr>`;
            const un = missing(r.predicted_question_level);
            const cog = answersMatch(r.predicted_student_answer, r.actual_answer);
            return `<tr><td>${esc(f.label)}</td><td>${un ? "–" : esc(r.predicted_question_level)}</td><td>${mark(ktHit(r), un)}</td>`
                + `<td><code>${esc(r.predicted_student_answer)}</code></td><td>${un ? "" : mark(cog, false)}</td></tr>`;
        }).join("");
        const glance = files.map(f => `${f.key} ${p[f.key] ? (missing(p[f.key].predicted_question_level) ? "?" : ktHit(p[f.key]) ? "✓" : "✗") : "·"}`).join(" · ");
        const prompt = p.profile?.prompt || "";
        const newBlock = prompt ? between(prompt, "**New Problem to Predict:**", null) : "";
        const profile = prompt ? between(prompt, "**Student Profile**", "**Student's ") : "";
        const recent = prompt ? between(prompt, "**Student's ", "**New Problem to Predict:**") : "";
        const responses = files.map(f => p[f.key] ? `<details><summary>${esc(f.label)}: model's reasoning and answer</summary><pre>${esc(p[f.key].full_response)}</pre></details>` : "").join("");
        return `<details class="card"><summary><b>Bin ${r0.bin_number}</b> · first ${r0.prediction_type === "correct" ? "right" : "wrong"} answer of the bin · `
            + `history ${r0.history_size} · problem ${esc(r0.problem_id)} · student answered <code>${esc(r0.actual_answer)}</code> `
            + `(${Number(r0.actual_score) >= 1 ? "right" : "wrong"}) <span class="glance">KT: ${esc(glance)}</span></summary>`
            + `<div class="body">`
            + (newBlock ? `<h4>The problem (as the profile model saw it)</h4><pre>${esc(newBlock)}</pre>`
                : `<p>Correct answer: <code>${esc(r0.correct_answer)}</code> · type: ${esc(r0.problem_type)}</p>`)
            + `<p>Student's actual answer: <code>${esc(r0.actual_answer)}</code> · correct answer: <code>${esc(r0.correct_answer)}</code>`
            + (hasWrong ? " · a truly wrong answer (counts for cognitive accuracy)" : r0.prediction_type === "incorrect" ? " · scored wrong only because of a hint or answer view" : "") + `</p>`
            + `<table><tr><th>Condition</th><th>Predicted right? (question_level)</th><th>KT</th><th>Predicted answer</th><th>Exact answer</th></tr>${rows}</table>`
            + (profile ? `<details open><summary>Student profile the profile model read</summary><pre>${esc(profile)}</pre></details>` : "")
            + (recent ? `<details><summary>Last 10 answers it read</summary><pre>${esc(recent)}</pre></details>` : "")
            + responses + `</div></details>`;
    }).join("");
    return `<section id="u-${esc(u.slice(0, 12))}"><h2>Student ${esc(u.slice(0, 12))}…</h2><p class="small">${esc(u)}</p>`
        + `<table><tr><th>Condition</th><th>Predictions</th><th>KT accuracy</th><th>Exact answer on truly wrong answers</th></tr>${sum}</table>`
        + (evo ? `<h3>How the profile grew, bin by bin</h3><table><tr><th>Bin</th><th>Answers in profile</th><th>Overall</th><th>Skill of the bin's first target</th></tr>${evo}</table>` : "")
        + `<h3>Every prediction (click to open)</h3>${cards || "<p>No predictions found for this student.</p>"}</section>`;
}

function page(users, files, data) {
    const nav = users.map(u => `<a href="#u-${esc(u.slice(0, 12))}">${esc(u.slice(0, 12))}…</a>`).join(" · ");
    return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KT student view</title><style>
:root{--bg:#fbfaf7;--fg:#22211e;--muted:#6d6a62;--line:#e2ded4;--card:#ffffff;--ok:#1d7a46;--no:#b4372f;--code:#f1eee6}
@media (prefers-color-scheme:dark){:root{--bg:#181816;--fg:#e9e6de;--muted:#a19d93;--line:#34322d;--card:#22211e;--ok:#5cc28a;--no:#ef7f76;--code:#2c2a26;color-scheme:dark}}
body{background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,sans-serif;margin:0;padding:24px max(16px,4vw)}
h1{font-size:22px;margin:0 0 4px}h2{font-size:19px;margin:36px 0 4px;border-top:1px solid var(--line);padding-top:20px}h3{font-size:15px;margin:22px 0 8px}h4{margin:12px 0 4px}
table{border-collapse:collapse;margin:6px 0 10px;display:block;overflow-x:auto}td,th{border:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}th{color:var(--muted);font-weight:600}
pre{white-space:pre-wrap;word-break:break-word;background:var(--code);padding:10px;border-radius:6px;font-size:12.5px;max-height:560px;overflow:auto}
code{background:var(--code);padding:1px 4px;border-radius:4px}.card{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:8px 0;padding:6px 10px}
.card>summary{cursor:pointer}.body{padding:6px 0}.ok{color:var(--ok);font-weight:700}.no{color:var(--no);font-weight:700}.na,.small,.glance{color:var(--muted)}.glance{margin-left:8px;font-size:12.5px}
details details{margin:6px 0}summary{cursor:pointer}
</style></head><body><h1>KT predictions, student by student</h1>
<p class="small">Runs: ${files.map(f => esc(f.label) + " (" + esc(path.basename(f.file)) + ")").join("; ")}. Students: ${nav}</p>
<p>Each card is one prediction: the paper's targets are the first right and the first wrong answer in each bin of 10, after 50 answers of history. KT ✓ = the condition predicted right/wrong correctly; Exact answer ✓ = its predicted answer matches what the student typed (as the evaluation matches answers). The profile is shown as the profile model read it at that point.</p>
${users.map(u => studentSection(u, files, data[u] || {})).join("")}
</body></html>`;
}

main().catch(e => { console.error(e); process.exit(1); });
