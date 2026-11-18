// Preview of the v5 prompts (label_v5.py) without Python: builds the system prompts from the strings in prompts.py,
// checks the shared definitions against the descriptors-only run (sha256 of its system prompt 1), and fills the user
// prompts for a few rows. Writes Results/prompt_preview/v5_prompts.txt.
//
//   node Code/generate_practice_reasoning/tools/preview_v5.js [rows, default 1,65,260,2] [out file]
//
// The evidence in prompt 6 is an ILLUSTRATION: v5's own diagnoses (prompt 5) do not exist yet, so the lines are made
// from the step-6 Chapter 3 diagnoses (Data/wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv; guess -> unexplained), in
// the format label_v5.evidence_text writes. A real run fills them from prompt 5's answers.

const fs = require("fs"), path = require("path"), crypto = require("crypto");
const { readTable } = require("./csv");
const HERE = path.join(__dirname, ".."), ROOT = path.join(HERE, "..", "..");
const ROWS = (process.argv[2] || "1,65,260,2").split(",").map(Number);
const OUT = process.argv[3] || path.join(ROOT, "Results", "prompt_preview", "v5_prompts.txt");
const NOEX_SP1_SHA = "8c12e9ed12b300b4c46ff17e67dea86f76a9a4aff720469ad4f5ebf9358df526";   // runs/qwen35_122b_noex

// ---- a small reader for the module-level string expressions of prompts.py
const src = fs.readFileSync(path.join(HERE, "prompts.py"), "utf8").replace(/\r\n/g, "\n");
const cache = {};
function expr(name) {
  if (name in cache) return cache[name];
  const start = src.indexOf("\n" + name + " = ");
  if (start < 0) throw new Error("not found in prompts.py: " + name);
  let i = start + name.length + 4, out = "";
  const ws = () => { while (i < src.length && /[ \t\n]/.test(src[i])) i++; };
  for (;;) {
    ws();
    if (src.startsWith('"""', i)) { const j = src.indexOf('"""', i + 3); out += src.slice(i + 3, j); i = j + 3; }
    else if (src[i] === "(") {          // parenthesized adjacent "..." literals
      const j = src.indexOf(")", i); const inner = src.slice(i + 1, j);
      out += [...inner.matchAll(/"((?:[^"\\]|\\.)*)"/g)].map(m => m[1]).join(""); i = j + 1;
    } else {
      const m = /^[A-Z_0-9]+/.exec(src.slice(i)); if (!m) throw new Error(`cannot read ${name} at ${src.slice(i, i + 40)}`);
      out += expr(m[0]); i += m[0].length;
    }
    let k = i; while (src[k] === " " || src[k] === "\t") k++;
    if (src[k] === "+") { i = k + 1; continue; }
    break;
  }
  return (cache[name] = out);
}
const noEx = (block, blank) => { const t = block.split("\nExample items:")[0]; return blank ? t + "\n" : t; };
const D_NOEX = expr("PROMPT_CONTEXT_NO_EXAMPLES") + noEx(expr("PROMPT_REPRESENTING"), false) + noEx(expr("PROMPT_ABSTRACTING"), true)
  + noEx(expr("PROMPT_JUSTIFYING"), true) + noEx(expr("PROMPT_MODELING"), true) + noEx(expr("PROMPT_COLLABORATIVE"), true)
  + noEx(expr("PROMPT_PROCEDURAL"), true);
const sha = s => crypto.createHash("sha256").update(s).digest("hex");
const sp1 = expr("INTRO_1") + D_NOEX + expr("PROMPT_RESPONSE_1");
if (sha(sp1) !== NOEX_SP1_SHA) throw new Error("the descriptors-only definitions no longer match run qwen35_122b_noex");
// PRACTICE_DEFINITIONS_V5: the same, with the sentence about the correct answer replaced (as in prompts.py)
const OLD = "For multiple-choice items the answer choices are listed; the correct answer is not shown.";
const NEW = "For multiple-choice items the answer choices are listed. The item's correct answer is given separately, after the item.";
const pyRepl = /PRACTICE_DEFINITIONS_V5 = PRACTICE_DEFINITIONS_NO_EXAMPLES\.replace\(\s*"([^"]+)",\s*"([^"]+)"\s*"([^"]+)"\)/.exec(src);
if (!pyRepl || pyRepl[1] !== OLD || pyRepl[2] + pyRepl[3] !== NEW) throw new Error("PRACTICE_DEFINITIONS_V5 in prompts.py differs from this preview");
const D_V5 = D_NOEX.replace(OLD, NEW);
const SYS5 = expr("INTRO_V5_WRONG") + D_V5 + expr("RESPONSE_V5_WRONG");
const SYS6 = expr("INTRO_V5_PROBLEM") + D_V5 + expr("RESPONSE_V5_PROBLEM");
const fill = (t, v) => t.replace(/\{(PROBLEM|CORRECT|SKILLS|WRONG|COUNT|SHARE|EVIDENCE|COVERAGE)\}/g, (m, k) => v[k]);

// ---- data, as label_v5.load_items reads it
const texts = new Map();
for (const l of fs.readFileSync(path.join(HERE, "problems_rendered.jsonl"), "utf8").split("\n")) if (l.trim()) { const o = JSON.parse(l); texts.set(o.row, o); }
const P = readTable(path.join(ROOT, "Data", "Problems.csv")), S = readTable(path.join(ROOT, "Data", "Skills.csv"));
const W = readTable(path.join(ROOT, "Results", "practice_analysis", "common_wrong_answers.csv"));
const DG = readTable(path.join(ROOT, "Data", "wrong_answer_diagnosis_qwen35_122b_ch3_diag.csv"));
const skills = new Map();
for (const r of S.rows) { const pid = r[0].trim(), code = (r[2] || "").trim(); if (!pid || !code) continue;
  const l = skills.get(pid) || []; if (!l.some(s => s.code === code)) l.push({ code, name: (r[3] || "").trim() }); skills.set(pid, l); }
const MON = { jan: 1, feb: 2, mar: 3, apr: 4, may: 5, jun: 6, jul: 7, aug: 8, sep: 9, oct: 10, nov: 11, dec: 12 };
const clean = t => (t || "").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&gt;/g, ">").replace(/&lt;/g, "<").replace(/&amp;/g, "&")
  .replace(/\b(\d{1,2})-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b/gi, (m, d, mo) => MON[mo.toLowerCase()] + "/" + d).replace(/\s+/g, " ").trim();
const correct = (type, mc, fi) => type === "Order / Sort" ? "(not given: work out the correct order from the item)"
  : (type.startsWith("Multiple Choice") ? clean(mc).split(" || ").join("; ") : clean(fi).split(" || ").join(" or ")) || "(not given)";
const skillsText = l => l.map(s => s.name ? `- ${s.code}: ${s.name}` : `- ${s.code}`).join("\n");
const diagOf = new Map(DG.rows.map(r => [`${r[DG.h.row]}|${r[DG.h.rank]}`, r]));
const failText = (et, fp, fact) => et === "practice" ? `practice error at ${fp}` : et === "math_fact" ? `math-fact error at ${fp}: ${fact.replace(/\.$/, "")}`
  : "unexplained: no reasonable process gives this answer";

let out = `v5 prompts (label_v5.py), built from prompts.py by tools/preview_v5.js on ${new Date().toISOString().slice(0, 10)}.\n`
  + `The definitions and descriptors are those of the descriptors-only run (qwen35_122b_noex; checked by sha256), with one sentence changed:\n  "${OLD}"\n  -> "${NEW}"\n`
  + `System prompt 5: ${SYS5.length} characters (sha256 ${sha(SYS5).slice(0, 12)}); system prompt 6: ${SYS6.length} characters (sha256 ${sha(SYS6).slice(0, 12)}).\n\n`;
const bar = t => "\n" + "=".repeat(100) + "\n" + t + "\n" + "=".repeat(100) + "\n\n";
out += bar("SYSTEM PROMPT 5: main incorrect-answer prompt (SYSTEM_PROMPT_V5_WRONG)") + SYS5 + "\n";
out += bar("SYSTEM PROMPT 6: main problem prompt (SYSTEM_PROMPT_V5_PROBLEM)") + SYS6 + "\n";
for (const row of ROWS) {
  const p = P.rows[row - 1], pid = p[P.h.problem_id].trim(), type = p[P.h["Problem Type"]].trim();
  const it = { text: texts.get(row).text, correct: correct(type, p[P.h["Multiple Choice Answers"]], p[P.h["Fill-in Answers"]]),
    skills: skills.get(pid) || [{ code: "none", name: "the item has no skill code" }] };
  const wrong = W.rows.filter(r => +r[W.h.row] === row && +r[W.h.students] >= 3).map(r => ({ rank: +r[W.h.rank], wrong: r[W.h.wrong_answer],
    students: +r[W.h.students], share: +r[W.h.share_of_wrong], total: +r[W.h.wrong_without_help] }));
  const base = { PROBLEM: it.text, CORRECT: it.correct, SKILLS: skillsText(it.skills) };
  out += bar(`ROW ${row} (problem ${pid}, ${type}; ${it.skills.length} skill${it.skills.length > 1 ? "s" : ""}; ${wrong.length} common wrong answer${wrong.length !== 1 ? "s" : ""})`);
  if (!wrong.length) {
    out += "---- USER PROMPT 6 (no common wrong answers: Q6_PROBLEM_TEMPLATE) ----\n\n" + fill(expr("Q6_PROBLEM_TEMPLATE"), base) + "\n";
    continue;
  }
  const w1 = wrong[0];
  out += `---- USER PROMPT 5 for the most common wrong answer (one such call per wrong answer; ${wrong.length} for this row) ----\n\n`
    + fill(expr("Q5_WRONG_TEMPLATE"), { ...base, WRONG: w1.wrong, COUNT: String(w1.students), SHARE: Math.round(100 * w1.share) + "%" }) + "\n\n";
  const lines = [...wrong].sort((a, b) => b.students - a.students || a.rank - b.rank).map((w, i) => {
    const d = diagOf.get(`${row}|${w.rank}`);
    const et = d ? (d[DG.h.error_type] === "guess" ? "unexplained" : d[DG.h.error_type]) : "unexplained";
    const what = d ? failText(et, d[DG.h.failed_practice], d[DG.h.math_fact]) : "unexplained: (no step-6 diagnosis)";
    const parts = [`w${i + 1}. “${w.wrong}”: ${w.students} students (${Math.round(100 * w.share)}% of the item's wrong answers). ${what[0].toUpperCase() + what.slice(1)}.`];
    const sentence = s => { s = (s || "").trim(); return !s || /[.!?]$/.test(s) ? s : s + "."; };
    if (d && et !== "unexplained") parts.push(`Student's process: ${sentence(d[DG.h.reconstruction])}`);
    if (d) parts.push(`Explanation: ${sentence(d[DG.h.explanation])}`);
    return parts.join(" ");
  });
  const students = wrong.reduce((s, w) => s + w.students, 0), total = wrong[0].total;
  const coverage = `${wrong.length} wrong answer${wrong.length !== 1 ? "s" : ""} given by ${students} students` + (total ? `, ${Math.round(100 * students / total)}% of the item's wrong first attempts without hints` : "");
  out += "---- USER PROMPT 6 with evidence (Q6_PROBLEM_EVIDENCE_TEMPLATE). ILLUSTRATION: the evidence lines here come from the step-6 Chapter 3 diagnoses;"
    + " a v5 run writes them from prompt 5's answers, with a 'By skill' part for items with 2+ skills ----\n\n"
    + fill(expr("Q6_PROBLEM_EVIDENCE_TEMPLATE"), { ...base, COVERAGE: coverage, EVIDENCE: lines.join("\n") }) + "\n";
}
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, out);
console.log(`wrote ${OUT} (${out.length} characters); system prompt 5: ${SYS5.length} chars, system prompt 6: ${SYS6.length} chars`);
