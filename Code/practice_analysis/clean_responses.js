// Clean Data/Interactions.csv with the same rules as Code/maca_cd/data/concept_main.py pre_process, and cache it.
//   - each interaction id once; drop rows without discrete_score, user_id or problem_id
//   - score = round(discrete_score), keep 0/1; keep problems that have a skill code in Skills.csv
//   - sort by end_time, id (missing end_time last); keep each student's first attempt at each problem
//   - keep students with >= 30 responses, then problems with >= 30 responses (in that order, once each)
// Output (TSV, one response per line, in time order):
//   Results/practice_analysis/cleaned_responses.tsv
//   student  problem_id  score  hint_count  saw_answer(0/1)  end_time  answer_text (tabs/newlines -> spaces)
// Usage (from the repo root): node Code/practice_analysis/clean_responses.js

const fs = require("fs");
const path = require("path");
const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "Results", "practice_analysis");
const MIN = 30;

// streaming RFC 4180 parser: calls onRow(fields) for every record
function parseCSVStream(file, onRow) {
    return new Promise((resolve, reject) => {
        let row = [], f = "", q = false, pendingQuote = false;
        const st = fs.createReadStream(file, { encoding: "utf8", highWaterMark: 1 << 22 });
        st.on("data", chunk => {
            for (let i = 0; i < chunk.length; i++) {
                const c = chunk[i];
                if (pendingQuote) {                 // a quote inside a quoted field: "" or end of field
                    pendingQuote = false;
                    if (c === '"') { f += '"'; continue; }
                    q = false;
                }
                if (q) { if (c === '"') pendingQuote = true; else f += c; continue; }
                if (c === '"') q = true;
                else if (c === ",") { row.push(f); f = ""; }
                else if (c === "\n") { row.push(f); onRow(row); row = []; f = ""; }
                else if (c !== "\r") f += c;
            }
        });
        st.on("end", () => { if (pendingQuote) q = false; if (f !== "" || row.length) { row.push(f); onRow(row); } resolve(); });
        st.on("error", reject);
    });
}

(async () => {
    // problems with a skill code
    const hasCode = new Set();
    let header = null;
    await parseCSVStream(path.join(ROOT, "Data", "Skills.csv"), r => {
        if (!header) { header = r; return; }
        const pid = (r[0] || "").trim(), code = (r[2] || "").trim(), name = (r[3] || "").trim();
        if (pid && code && name) hasCode.add(pid);
    });

    const seenId = new Set();
    const rows = [];
    header = null;
    let total = 0;
    await parseCSVStream(path.join(ROOT, "Data", "Interactions.csv"), r => {
        if (!header) { header = {}; r.forEach((n, i) => header[n] = i); return; }
        total++;
        const id = r[header.id], pid = (r[header.problem_id] || "").trim(), uid = r[header.user_id];
        const ds = r[header.discrete_score];
        if (!id || seenId.has(id)) return;
        seenId.add(id);
        if (ds === undefined || ds === "" || !uid || !pid) return;
        const score = Math.round(Number(ds));
        if (!(score === 0 || score === 1)) return;
        if (!hasCode.has(pid)) return;
        rows.push({ id: Number(id), pid, uid, score, hint: Number(r[header.hint_count]) || 0,
            saw: r[header.saw_answer] === "True" ? 1 : 0, t: r[header.end_time] || "",
            ans: (r[header.answer_text] || "").replace(/[\t\r\n]+/g, " ").trim() });
    });
    console.error(`interactions read: ${total}; usable: ${rows.length}`);

    rows.sort((a, b) => (a.t === "" ? 1 : 0) - (b.t === "" ? 1 : 0) || (a.t < b.t ? -1 : a.t > b.t ? 1 : 0) || a.id - b.id);
    const firstSeen = new Set(), first = [];
    for (const x of rows) { const k = x.uid + "|" + x.pid; if (!firstSeen.has(k)) { firstSeen.add(k); first.push(x); } }

    const countBy = (arr, key) => { const m = new Map(); for (const x of arr) m.set(x[key], (m.get(x[key]) || 0) + 1); return m; };
    const su = countBy(first, "uid");
    const step1 = first.filter(x => su.get(x.uid) >= MIN);
    const sp = countBy(step1, "pid");
    const clean = step1.filter(x => sp.get(x.pid) >= MIN);
    console.error(`first attempts: ${first.length}; after student filter: ${step1.length}; after problem filter: ${clean.length}`);
    console.error(`students: ${new Set(clean.map(x => x.uid)).size}; problems: ${new Set(clean.map(x => x.pid)).size}`);

    fs.mkdirSync(OUT_DIR, { recursive: true });
    const out = fs.createWriteStream(path.join(OUT_DIR, "cleaned_responses.tsv"));
    out.write("student\tproblem_id\tscore\thint_count\tsaw_answer\tend_time\tanswer_text\n");
    for (const x of clean) out.write(`${x.uid}\t${x.pid}\t${x.score}\t${x.hint}\t${x.saw}\t${x.t}\t${x.ans}\n`);
    out.end();
})();
