// Small CSV helpers shared by the Node tools in this folder (no packages).
const fs = require("fs");

// RFC 4180: quoted fields may hold commas, quotes and newlines.
function parseCSV(text) {
    const rows = []; let row = [], f = "", q = false;
    for (let i = 0; i < text.length; i++) {
        const c = text[i];
        if (q) {
            if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; }
            else f += c;
        } else if (c === '"') q = true;
        else if (c === ",") { row.push(f); f = ""; }
        else if (c === "\n" || c === "\r") {
            if (c === "\r" && text[i + 1] === "\n") i++;
            row.push(f); rows.push(row); row = []; f = "";
        } else f += c;
    }
    if (f !== "" || row.length) { row.push(f); rows.push(row); }
    return rows;
}

// { h: {column name: index}, rows: [[...], ...] } without the header row
function readTable(file) {
    const rows = parseCSV(fs.readFileSync(file, "utf8").replace(/^﻿/, ""));
    const h = {}; rows[0].forEach((name, i) => { h[name] = i; });
    return { h, rows: rows.slice(1) };
}

// minimal quoting, like Problems.csv
function csvField(v) {
    const s = v === null || v === undefined ? "" : String(v);
    return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

const PRACTICES = ["Representing", "Abstracting and Generalizing", "Justifying and Proving",
    "Mathematical Modeling", "Collaborative Mathematics", "Procedural Fluency"];
const canon = s => {
    const t = (s || "").trim().toLowerCase();
    return PRACTICES.find(p => p.toLowerCase() === t) || (s || "").trim();
};

// An LLM's answer 1 (JSON) -> its ordering: practices_used sorted by "order", each practice once.
function llmOrdering(answer1) {
    let qa = null;
    try { qa = JSON.parse(answer1); } catch (e) { return null; }
    const used = [...(qa.practices_used || [])].sort((a, b) => a.order - b.order);
    const order = [];
    for (const u of used) { const n = canon(u.practice); if (!order.includes(n)) order.push(n); }
    return { order, used, notUsed: qa.practices_not_used || [] };
}

module.exports = { parseCSV, readTable, csvField, PRACTICES, canon, llmOrdering };
