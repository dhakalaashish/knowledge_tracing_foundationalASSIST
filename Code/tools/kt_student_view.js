// Read a KT benchmark run (kt_practice_benchmark.py, the A100 runs) student by student: for each prediction, the problem,
// what the student answered, what each condition predicted (right / wrong), and, for the three Qwen3-Next-80B 4-bit runs
// (baseline, practice, profile), EXACTLY what the model was given and EXACTLY what it returned.
//
// What the model saw: kt_inference_base.py sends each prompt to vLLM as plain text (llm.generate(prompt), no chat
// template), and the results file keeps that text in "prompt" (system prompt + blank line + user prompt). What it
// returned: "full_response" is the model's output text; the paper's code only removed leading and trailing whitespace.
// Both are written unchanged to text files (one per prediction and run) next to the page, and linked from it; the
// response is also shown in full on the page. The paper's own published predictions appear in the table only.
//
// Usage (from the repo root; Node only, no packages):
//   node Code/tools/kt_student_view.js [--dir Results/kt_practice_main] [--users id1,id2 | --n 2 --seed 7] [--out file.html]
//
// Reads, in --dir, for each run the first of these that exists (gz or not):
//   <run>_qwen3next80b_awq_bin10_hist50.jsonl        the full results file (prompts included)
//   <run>_view2.jsonl                                these students' lines of the full file, cut on the A100
//   <run>_qwen3next80b_awq_bin10_hist50_slim.jsonl   no prompts (the page then says the prompt is not available)
// with <run> = baseline, practice, profile; plus paper_qwen3next80b_instruct_bf16_n*.jsonl for the paper's predictions.
// Answers are matched as evaluate_kt.answers_match does (exact, MC letters in any order, numbers within 1%).

const fs = require("fs");
const path = require("path");
const zlib = require("zlib");
const readline = require("readline");

const argv = process.argv.slice(2);
const opt = (name, dflt) => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : dflt; };
const DIR = opt("--dir", path.join("Results", "kt_practice_main"));
const OUT = opt("--out", path.join(DIR, "student_view.html"));
const FILES_DIR = path.join(path.dirname(OUT), path.basename(OUT, ".html") + "_files");
const N = Number(opt("--n", 2));
const SEED = Number(opt("--seed", 7));
const USERS_ARG = opt("--users", "");

const RUNS = [
    { key: "paper", label: "Paper's published (BF16)", exact: false,
      names: [/^paper_qwen3next80b_instruct_bf16_n\d+(_slim)?\.jsonl(\.gz)?$/] },
    { key: "baseline", label: "Baseline (4-bit, paper prompts)", exact: true,
      names: ["baseline_qwen3next80b_awq_bin10_hist50.jsonl", "baseline_view2.jsonl", "baseline_qwen3next80b_awq_bin10_hist50_slim.jsonl"] },
    { key: "practice", label: "Practice (4-bit, full history + labels)", exact: true,
      names: ["practice_qwen3next80b_awq_bin10_hist50.jsonl", "practice_view2.jsonl", "practice_qwen3next80b_awq_bin10_hist50_slim.jsonl"] },
    { key: "profile", label: "Profile (4-bit, profile + last 10)", exact: true,
      names: ["profile_qwen3next80b_awq_bin10_hist50.jsonl", "profile_view2.jsonl", "profile_qwen3next80b_awq_bin10_hist50_slim.jsonl"] },
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
// Python writes NaN / Infinity, which JSON.parse refuses: replace them with null, but only outside strings, so the
// prompt and response texts stay exactly as written
function parseLine(line) {
    try { return JSON.parse(line); } catch { /* fall through */ }
    let out = "", inStr = false, esc = false;
    for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (inStr) { out += c; if (esc) esc = false; else if (c === "\\") esc = true; else if (c === '"') inStr = false; continue; }
        if (c === '"') { inStr = true; out += c; continue; }
        const m = /^-?(NaN|Infinity)/.exec(line.slice(i, i + 9));
        if (m) { out += "null"; i += m[0].length - 1; continue; }
        out += c;
    }
    return JSON.parse(out);
}
function lines(file) {
    let stream = fs.createReadStream(file);
    if (file.endsWith(".gz")) stream = stream.pipe(zlib.createGunzip());
    return readline.createInterface({ input: stream, crlfDelay: Infinity });
}
const userOf = line => { const m = /^\{"prediction_id":\s*"([^"]+)_\d+_(?:correct|incorrect)"/.exec(line.slice(0, 200)); return m && m[1]; };
function pickFile(run) {
    const have = fs.readdirSync(DIR);
    for (const n of run.names) {
        if (n instanceof RegExp) { const hit = have.filter(x => n.test(x)).sort((a, b) => a.includes("_slim") - b.includes("_slim"))[0]; if (hit) return path.join(DIR, hit); continue; }
        for (const cand of [n, n + ".gz"]) if (have.includes(cand)) return path.join(DIR, cand);
    }
    return null;
}
function seededShuffle(arr, seed) {
    let s = seed >>> 0;
    const rnd = () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
}

async function main() {
    const files = RUNS.map(r => ({ ...r, file: pickFile(r) })).filter(r => r.file);
    if (!files.length) throw new Error(`no result files found in ${DIR}`);
    let users;
    if (USERS_ARG) users = USERS_ARG.split(",").map(s => s.trim()).filter(Boolean);
    else {
        const ids = fs.readFileSync(path.join(DIR, "user_ids.txt"), "utf8").split(/\r?\n/).map(s => s.trim()).filter(Boolean);
        users = seededShuffle(ids, SEED).slice(0, N);
    }
    const want = new Set(users);
    const data = {};        // user -> prediction_id -> {run: record}
    for (const r of files) {
        process.stdout.write(`reading ${r.file} ... `);
        let n = 0, withPrompt = 0;
        for await (const line of lines(r.file)) {
            const u = userOf(line);
            if (!u || !want.has(u)) continue;
            const rec = parseLine(line);
            if (!r.exact) delete rec.prompt;
            if (rec.prompt) withPrompt++;
            ((data[u] ||= {})[rec.prediction_id] ||= {})[r.key] = rec;
            n++;
        }
        r.n = n; r.withPrompt = withPrompt;
        console.log(`${n} predictions for the chosen students` + (r.exact ? `, ${withPrompt} with their prompt` : ""));
    }
    // the exact texts, one file each (written as they are, UTF-8)
    let written = 0;
    for (const u of users) for (const [id, byRun] of Object.entries(data[u] || {})) for (const r of files) {
        const rec = byRun[r.key];
        if (!r.exact || !rec) continue;
        const dir = path.join(FILES_DIR, u.slice(0, 12));
        fs.mkdirSync(dir, { recursive: true });
        const stem = `${id.split("_").slice(-2).join("_")}_${r.key}`;
        if (typeof rec.prompt === "string") { fs.writeFileSync(path.join(dir, `${stem}_prompt.txt`), rec.prompt, "utf8"); rec._promptFile = `${path.basename(FILES_DIR)}/${u.slice(0, 12)}/${stem}_prompt.txt`; written++; }
        if (typeof rec.full_response === "string") { fs.writeFileSync(path.join(dir, `${stem}_response.txt`), rec.full_response, "utf8"); rec._responseFile = `${path.basename(FILES_DIR)}/${u.slice(0, 12)}/${stem}_response.txt`; written++; }
    }
    fs.writeFileSync(OUT, page(users, files, data), "utf8");
    console.log(`\nStudents: ${users.join(", ")}\nWrote ${OUT} and ${written} exact prompt / response files in ${FILES_DIR}`);
}

// ------------------------------------------------------------------ page
const esc = s => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const between = (text, a, b) => { const i = text.indexOf(a); if (i < 0) return ""; const j = b ? text.indexOf(b, i + a.length) : -1; return text.slice(i, j < 0 ? undefined : j).trim(); };
const ktHit = r => r && !missing(r.predicted_question_level) && Number(r.predicted_question_level) === Number(r.actual_score);
const trulyWrong = r => r.prediction_type === "incorrect" && (missing(r.correct_answer) || !answersMatch(r.actual_answer, r.correct_answer));
const mark = (ok, unparsed) => unparsed ? '<span class="na">no parse</span>' : ok ? '<span class="ok">✓</span>' : '<span class="no">✗</span>';
const kchars = n => n >= 10000 ? `${Math.round(n / 1000).toLocaleString()}k characters` : `${n.toLocaleString()} characters`;

function exactBlock(r, rec) {
    if (!rec) return "";
    const pr = typeof rec.prompt === "string"
        ? `<a href="${esc(rec._promptFile)}" target="_blank">Open the exact prompt</a> <span class="small">(${kchars(rec.prompt.length)}; what the model was given, as plain text)</span>`
        : `<span class="na">Prompt not available here: only the copy without prompts was found (cut these students' lines on the A100, see the tool's header).</span>`;
    const resp = typeof rec.full_response === "string" ? rec.full_response : "";
    return `<div class="exact"><div class="exact-head"><b>${esc(r.label)}</b> · ${pr}` +
        (rec._responseFile ? ` · <a href="${esc(rec._responseFile)}" target="_blank">response as a file</a>` : "") + `</div>` +
        `<details><summary>Its exact response (${kchars(resp.length)})</summary><pre>${esc(resp)}</pre></details></div>`;
}

function studentSection(u, files, preds) {
    const ids = Object.keys(preds).sort((a, b) => {
        const pa = a.split("_"), pb = b.split("_");
        return (Number(pa.at(-2)) - Number(pb.at(-2))) || pa.at(-1).localeCompare(pb.at(-1));
    });
    const any = id => { const p = preds[id]; return p.baseline || p.practice || p.profile || p.paper; };
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
        const anyPrompt = (p.baseline && p.baseline.prompt) || (p.practice && p.practice.prompt) || (p.profile && p.profile.prompt) || "";
        const newBlock = anyPrompt ? between(anyPrompt, "**New Problem to Predict:**", null) : "";
        const profile = p.profile?.prompt ? between(p.profile.prompt, "**Student Profile**", "**Student's ") : "";
        return `<details class="card"><summary><b>Bin ${r0.bin_number}</b> · first ${r0.prediction_type === "correct" ? "right" : "wrong"} answer of the bin · `
            + `history ${r0.history_size} · problem ${esc(r0.problem_id)} · student answered <code>${esc(r0.actual_answer)}</code> `
            + `(${Number(r0.actual_score) >= 1 ? "right" : "wrong"}) <span class="glance">KT: ${esc(glance)}</span></summary>`
            + `<div class="body">`
            + (newBlock ? `<h4>The problem to predict (end of the prompt)</h4><pre>${esc(newBlock)}</pre>` : "")
            + `<p>Student's actual answer: <code>${esc(r0.actual_answer)}</code> · correct answer: <code>${esc(r0.correct_answer)}</code>`
            + (hasWrong ? " · a truly wrong answer (counts for cognitive accuracy)" : r0.prediction_type === "incorrect" ? " · scored wrong only because of a hint or answer view" : "") + `</p>`
            + `<table><tr><th>Run</th><th>Predicted right? (question_level)</th><th>KT</th><th>Predicted answer</th><th>Exact answer</th></tr>${rows}</table>`
            + `<h4>Exactly what each 4-bit run was given, and what it returned</h4>`
            + files.filter(f => f.exact).map(f => exactBlock(f, p[f.key])).join("")
            + (profile ? `<details><summary>The student profile inside the profile prompt</summary><pre>${esc(profile)}</pre></details>` : "")
            + `</div></details>`;
    }).join("");
    return `<section id="u-${esc(u.slice(0, 12))}"><h2>Student ${esc(u.slice(0, 12))}…</h2><p class="small">${esc(u)}</p>`
        + `<table><tr><th>Run</th><th>Predictions</th><th>KT accuracy</th><th>Exact answer on truly wrong answers</th></tr>${sum}</table>`
        + (evo ? `<h3>How the profile grew, bin by bin</h3><table><tr><th>Bin</th><th>Answers in profile</th><th>Overall</th><th>Skill of the bin's first target</th></tr>${evo}</table>` : "")
        + `<h3>Every prediction (click to open)</h3>${cards || "<p>No predictions found for this student.</p>"}</section>`;
}

function page(users, files, data) {
    const nav = users.map(u => `<a href="#u-${esc(u.slice(0, 12))}">${esc(u.slice(0, 12))}…</a>`).join(" · ");
    const src = files.map(f => `${esc(f.label)}: ${esc(path.basename(f.file))}` + (f.exact ? ` (${f.withPrompt} of ${f.n} with prompts)` : "")).join("<br>");
    return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KT student view</title><style>
:root{--bg:#fbfaf7;--fg:#22211e;--muted:#6d6a62;--line:#e2ded4;--card:#ffffff;--ok:#1d7a46;--no:#b4372f;--code:#f1eee6;--accent:#2f62b3}
@media (prefers-color-scheme:dark){:root{--bg:#181816;--fg:#e9e6de;--muted:#a19d93;--line:#34322d;--card:#22211e;--ok:#5cc28a;--no:#ef7f76;--code:#2c2a26;--accent:#7ea6e8;color-scheme:dark}}
body{background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,sans-serif;margin:0;padding:24px max(16px,4vw)}
a{color:var(--accent)}h1{font-size:22px;margin:0 0 4px}h2{font-size:19px;margin:36px 0 4px;border-top:1px solid var(--line);padding-top:20px}h3{font-size:15px;margin:22px 0 8px}h4{margin:14px 0 6px}
table{border-collapse:collapse;margin:6px 0 10px;display:block;overflow-x:auto}td,th{border:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}th{color:var(--muted);font-weight:600}
pre{white-space:pre-wrap;word-break:break-word;background:var(--code);padding:10px;border-radius:6px;font-size:12.5px;max-height:620px;overflow:auto}
code{background:var(--code);padding:1px 4px;border-radius:4px}.card{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:8px 0;padding:6px 10px}
.card>summary{cursor:pointer}.body{padding:6px 0}.ok{color:var(--ok);font-weight:700}.no{color:var(--no);font-weight:700}.na,.small,.glance{color:var(--muted)}.glance{margin-left:8px;font-size:12.5px}
.exact{border-left:3px solid var(--line);padding:2px 0 2px 10px;margin:8px 0}.exact-head{margin-bottom:4px}
details details{margin:6px 0}summary{cursor:pointer}
</style></head><body><h1>KT predictions, student by student (A100 runs)</h1>
<p class="small">Students: ${nav}<br>Files read:<br>${src}</p>
<p>Each card is one prediction: the first right and the first wrong answer in each bin of 10, after 50 answers of history. KT ✓ = the run predicted right/wrong correctly; Exact answer ✓ = its predicted answer matches what the student typed (as the evaluation matches answers).</p>
<p>For the three Qwen3-Next-80B 4-bit runs, <b>“Open the exact prompt”</b> opens the complete text the model was given (the paper's code sends it to vLLM as plain text, with no chat template), and <b>“Its exact response”</b> shows everything the model wrote (the paper's code only trimmed leading and trailing whitespace). The paper's published (BF16) predictions are shown in the table only.</p>
${users.map(u => studentSection(u, files, data[u] || {})).join("")}
</body></html>`;
}

main().catch(e => { console.error(e); process.exit(1); });
