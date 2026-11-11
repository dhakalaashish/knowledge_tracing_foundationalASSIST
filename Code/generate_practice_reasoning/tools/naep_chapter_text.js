// Make naep_chapter3.txt (the text of NAEP Mathematics Framework 2026, Chapter 3, "NAEP Mathematical Practices")
// from the PDF, for the --framework naep_ch3 prompts.
//
// Usage (from the repo root; Node only, no packages):
//   node Code/generate_practice_reasoning/tools/naep_chapter_text.js "<path>/NAEP Math Practices Chapter 3 Only.pdf" \
//        Code/generate_practice_reasoning/naep_chapter3.txt
//
// What it does: reads every page's text (Flate streams, Tj/TJ operators; two-byte subset-font codes shifted by 29),
// maps the PDF's quote and dash codes to Unicode, drops page numbers and the lines that are fragments of figures
// (item images come out as scattered symbols), and joins words split across lines. Item figures themselves are
// images and are not in the text; their captions and the surrounding discussion are.

const fs = require("fs"), zlib = require("zlib");
const [PDF, OUT] = process.argv.slice(2);
if (!PDF || !OUT) { console.error("usage: naep_chapter_text.js <pdf> <out.txt>"); process.exit(1); }
const b = fs.readFileSync(PDF), s = b.toString("latin1");

// ---------- objects, pages, streams
const objs = new Map(); const ore = /(\d+)\s+0\s+obj\b/g; let m;
while ((m = ore.exec(s))) objs.set(+m[1], m.index + m[0].length);
const objText = n => { const st = objs.get(n); return st === undefined ? "" : s.slice(st, s.indexOf("endobj", st)); };
function streamOf(n) {
    const st = objs.get(n); if (st === undefined) return "";
    const body = s.slice(st, s.indexOf("endobj", st)); const k = body.indexOf("stream"); if (k < 0) return "";
    let a = st + k + 6; if (s[a] === "\r") a++; if (s[a] === "\n") a++;
    const e = s.indexOf("endstream", a); let data = b.subarray(a, e);
    if (/FlateDecode/.test(body.slice(0, k))) { try { data = zlib.inflateSync(data); } catch (er) { try { data = zlib.inflateSync(b.subarray(a, e - 1)); } catch (e2) { return ""; } } }
    return data.toString("latin1");
}
const pages = [];
function walk(n) {
    const t = objText(n);
    if (/\/Type\s*\/Pages\b/.test(t)) { for (const k of ((t.match(/\/Kids\s*\[([^\]]*)\]/) || [, ""])[1]).matchAll(/(\d+)\s+0\s+R/g)) walk(+k[1]); }
    else if (/\/Type\s*\/Page\b/.test(t)) {
        const c = t.match(/\/Contents\s*(\[([^\]]*)\]|(\d+)\s+0\s+R)/); const ids = [];
        if (c) { if (c[2]) for (const k of c[2].matchAll(/(\d+)\s+0\s+R/g)) ids.push(+k[1]); else ids.push(+c[3]); }
        pages.push(ids);
    }
}
walk(+(objText(+(s.match(/\/Root\s+(\d+)\s+0\s+R/) || [])[1]).match(/\/Pages\s+(\d+)\s+0\s+R/) || [])[1]);

// ---------- text operators
function readString(t, i) {
    let depth = 1, out = ""; i++;
    while (i < t.length && depth) {
        const c = t[i];
        if (c === "\\") { const n = t[i + 1];
            if (/[0-7]/.test(n)) { const o = t.slice(i + 1, i + 4).match(/^[0-7]{1,3}/)[0]; out += String.fromCharCode(parseInt(o, 8)); i += 1 + o.length; continue; }
            out += ({ n: "\n", r: "", t: " ", b: "", f: "" })[n] ?? n; i += 2; continue; }
        if (c === "(") depth++; else if (c === ")") { depth--; if (!depth) break; }
        out += c; i++;
    }
    return [out, i + 1];
}
function pageText(t) {
    const ops = []; let i = 0;
    while (i < t.length) {
        const c = t[i];
        if (c === "(") { let [str, j] = readString(t, i);
            if (str.length >= 2 && str.length % 2 === 0 && [...str].every((ch, q) => q % 2 || ch === "\0"))
                str = [...str].filter((ch, q) => q % 2).map(ch => String.fromCharCode(ch.charCodeAt(0) + 29)).join("");
            ops.push({ s: str }); i = j; continue; }
        if (c === "[" || c === "]") { i++; continue; }
        if (/[A-Za-z'"*]/.test(c)) { let j = i; while (j < t.length && /[A-Za-z'"*]/.test(t[j])) j++; ops.push({ op: t.slice(i, j) }); i = j; continue; }
        if (/[-\d.]/.test(c)) { let j = i; while (j < t.length && /[-\d.]/.test(t[j])) j++; ops.push({ num: +t.slice(i, j) }); i = j; continue; }
        i++;
    }
    let out = "", buf = [];
    for (const o of ops) {
        if (o.s !== undefined || o.num !== undefined) { buf.push(o); continue; }
        if (o.op === "Tj" || o.op === "'" || o.op === '"') { const st = buf.filter(x => x.s !== undefined).pop(); if (o.op !== "Tj") out += "\n"; if (st) out += st.s; }
        else if (o.op === "TJ") { for (const x of buf) { if (x.s !== undefined) out += x.s; else if (x.num < -180) out += " "; } }
        else if (o.op === "Td" || o.op === "TD") { const nums = buf.filter(x => x.num !== undefined); const dy = nums.length >= 2 ? nums[nums.length - 1].num : 0; out += Math.abs(dy) > 0.5 ? "\n" : ""; }
        else if (o.op === "T*" || o.op === "Tm" || o.op === "ET") out += "\n";
        buf = [];
    }
    return out;
}

// ---------- clean
const MAP = { "Ó": "’", "Ò": "‘", "Ð": "“", "Ñ": "”", "Î": "–", "Ï": "—", "\u0095": "•",
    "ċ": "×", "á": "∠", "²": ">" };
function clean(t, pageNo) {
    t = t.replace(/[ÓÒÐÑÎÏ\u0095ċá²]/g, ch => MAP[ch]).replace(/[\u0000-\u0008\u000b-\u001f\u007f-\u009f]/g, "");
    let lines = t.split("\n").map(l => l.replace(/[ \t]+/g, " ").trim());
    // fragments of figures: short lines that are mostly not letters
    lines = lines.filter(l => { if (!l) return false; const letters = (l.match(/[A-Za-z]/g) || []).length; return l.length >= 25 || letters >= Math.max(3, l.length * 0.6) || /^Exhibit/.test(l) || /^[A-Z]$/.test(l); });
    if (lines.length && /^\d{1,3}$/.test(lines[0])) lines.shift();                    // page number
    // join: small-caps initials ("C" + "HAPTER"), words split across lines, and wrapped lines of one paragraph
    const outL = [];
    for (const l of lines) {
        const prev = outL[outL.length - 1];
        if (prev !== undefined && /^[A-Z]$/.test(prev.slice(-1)) && /(^| )[A-Z]$/.test(prev) && /^[A-Z]/.test(l)) { outL[outL.length - 1] = prev + l; continue; }
        if (prev !== undefined && /[a-z,;—–-]$/.test(prev) && /^[a-z(]/.test(l)) { outL[outL.length - 1] = prev + (/[—–-]$/.test(prev) ? "" : " ") + l; continue; }
        outL.push(l);
    }
    return outL.join("\n");
}
const text = pages.map((ids, k) => clean(pageText(ids.map(streamOf).join("\n")), k + 1)).join("\n");
fs.writeFileSync(OUT, text.replace(/\n{3,}/g, "\n\n").trim() + "\n", "utf8");
console.log(`${pages.length} pages, ${text.length} characters (about ${Math.round(text.length / 4)} tokens) -> ${OUT}`);
