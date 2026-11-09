# Render Problems.csv rows as the plain text a student sees, one file per row: OUT/p<row>.txt
# Usage: LC_ALL=C gawk -b --csv -v FROM=6 -v TO=105 -v OUT=dir -f render.awk Problems.csv
# Byte mode: UTF-8 characters are written byte by byte (u8), so the locale does not matter.
# Not included: the correct answer, and (for text blanks) Fill-in Options, which hold the answer.
# Ordering problems store their items in the correct order, so the items are shuffled.
BEGIN {
    split("nbsp 160 amp 38 lt 60 gt 62 quot 34 apos 39 times 215 divide 247 minus 8722 sdot 8901 middot 183 " \
          "le 8804 ge 8805 ne 8800 plusmn 177 deg 176 frac12 189 frac14 188 frac34 190 pi 960 hellip 8230 " \
          "rsquo 8217 lsquo 8216 ldquo 8220 rdquo 8221 ndash 8211 mdash 8212 cent 162 radic 8730 infin 8734 " \
          "asymp 8776 prime 8242 Prime 8243 sup2 178 sup3 179 laquo 171 raquo 187 uml 168 hyphen 8208 lowast 8727 " \
          "bull 8226 rarr 8594 larr 8592 harr 8596 theta 952 alpha 945 beta 946 Delta 916 ang 8736 perp 8869 " \
          "cong 8773 sim 8764 there4 8756 thinsp 8201 ensp 8194 emsp 8195 zwj 8205 zwnj 8204 shy 173 " \
          "copy 169 reg 174 trade 8482 euro 8364 pound 163 yen 165 micro 181 para 182 sect 167 ordm 186 " \
          "iexcl 161 iquest 191 eacute 233 ntilde 241 aacute 225 oacute 243 uacute 250 iacute 237", E, " ")
    for (i = 1; i < length(E); i += 2) ENT[E[i]] = E[i + 1]
    NBSP = u8(160); MINUS = u8(8722); HYPH = u8(8208); LAQ = u8(171); RAQ = u8(187); UML = u8(168); SECT = u8(167)
}
NR == 1 { next }
{
    row = NR - 1
    if (row < FROM || row > TO) next
    body = $5; type = $3; ans_type = $4
    text = html(body)
    if (ans_type == "Drop Down" || body ~ /type="dropdown"/) {
        n = opts($6, O)
        ch = ""
        for (i = 1; i <= n; i++) ch = ch (i > 1 ? " / " : "") html(O[i])
        if (gsub(/\[dropdown\]/, "&", text) == 1) sub(/\[dropdown\]/, "[dropdown: " ch "]", text)
        else text = text "\n\nDropdown choices: " ch
    }
    if (type ~ /Order/) {
        n = opts($6, O)
        for (i = 1; i <= n; i++) { O[i] = html(O[i]); gsub(/\n/, " ", O[i]) }
        shuffle(O, n, $10)
        text = text "\n\nItems to put in order:"
        for (i = 1; i <= n; i++) text = text "\n- " O[i]
    }
    if ($8 != "") {
        n = opts($8, O)
        text = text "\n\nAnswer choices:"
        for (i = 1; i <= n; i++) text = text "\n" sprintf("%c", 64 + i) ". " html(O[i])
    }
    f = OUT "/p" row ".txt"
    printf "%s\n", text > f; close(f)
    printf "===== row %d | pid %s | %s / %s\n%s\n", row, $10, type, ans_type, text
}

# --- options --------------------------------------------------------------------------
# Options are joined by ", ". HTML options are split only between a closing and an opening block tag,
# because the option text itself can contain commas.
function opts(s, O,   n) {
    delete O
    if (s ~ /</) {
        s = gensub(/(<\/(p|div)>)[ \t\r\n]*,[ \t\r\n]*(<(p|div))/, "\\1\001\\3", "g", s)
        return split(s, O, "\001")
    }
    return split(s, O, ", ")
}
# Fixed shuffle (seeded by problem_id) that differs from the stored (correct) order and its reverse.
function shuffle(O, n, seed,   i, j, t, tries, same, rev, S) {
    if (n < 2) return
    for (i = 1; i <= n; i++) S[i] = O[i]
    srand(seed + 0)
    for (tries = 0; tries < 50; tries++) {
        for (i = n; i > 1; i--) { j = int(rand() * i) + 1; t = O[i]; O[i] = O[j]; O[j] = t }
        same = 1; rev = 1
        for (i = 1; i <= n; i++) { if (O[i] != S[i]) same = 0; if (O[i] != S[n + 1 - i]) rev = 0 }
        if (!same && !rev || n == 2 && !same) return
    }
}

# --- HTML -----------------------------------------------------------------------------
function html(s,   out, tag, alt, mm, m, lines, n, i, k) {
    s = gensub(/<ast-r[^>]*type="dropdown"[^>]*>[ \t\r\n]*(<\/ast-r>)?/, " [dropdown] ", "g", s)
    s = gensub(/<ast-r[^>]*>[ \t\r\n]*(<\/ast-r>)?/, " ____ ", "g", s)
    # images: formula images (Wiris) become their math; others their alt text or [image]
    out = ""
    while (match(s, /<img[^>]*>/)) {
        tag = substr(s, RSTART, RLENGTH); out = out substr(s, 1, RSTART - 1); s = substr(s, RSTART + RLENGTH)
        alt = attr(tag, "alt"); mm = attr(tag, "data-mathml")
        if (mm != "") {
            mm = decode(mm); gsub(LAQ, "<", mm); gsub(RAQ, ">", mm); gsub(UML, "\"", mm); gsub(SECT "#", "\\&#", mm)
            out = out " " math(mm) " "
        } else if (tag ~ /wiris/) out = out (alt != "" ? " [" decode(alt) "] " : " [math] ")
        else if (alt != "" && alt !~ /^(NO ALT|NONE)$/) out = out " [Image: " decode(alt) "] "
        else out = out " [image] "
    }
    s = out s
    # inline MathML
    out = ""
    while (match(s, /<math[^>]*>/)) {
        out = out substr(s, 1, RSTART - 1); s = substr(s, RSTART)
        k = index(s, "</math>"); if (!k) break
        out = out " " math(substr(s, 1, k + 6)) " "; s = substr(s, k + 7)
    }
    s = out s
    # tables
    s = gensub(/<\/t[dh]>[ \t\r\n]*<t[dh][^>]*>/, " | ", "g", s)
    s = gensub(/<table[^>]*>/, "\n[Table:\n", "g", s)
    s = gensub(/<\/table>/, "\n]\n", "g", s)
    s = gensub(/<tr[^>]*>/, "\n", "g", s)
    # HTML superscripts and subscripts: 10<sup>3</sup> -> 10^3
    s = script(s, "sup", "^"); s = script(s, "sub", "_")
    # blocks, list items, other tags
    s = gensub(/<li[^>]*>/, "\n- ", "g", s)
    s = gensub(/<(br|\/p|p|\/div|div|\/li|\/ul|ul|\/ol|ol|h[1-6]|\/h[1-6])( [^>]*)?\/?>/, "\n", "g", s)
    gsub(/<[^>]*>/, "", s)
    s = decode(s)
    gsub(NBSP, " ", s); gsub(/\r/, "", s); gsub(/\t/, " ", s)
    n = split(s, lines, "\n"); s = ""
    for (i = 1; i <= n; i++) {
        gsub(/ +/, " ", lines[i]); sub(/^ /, "", lines[i]); sub(/ $/, "", lines[i])
        lines[i] = gensub(/ ([:,;?]|\.)( |$)/, "\\1\\2", "g", lines[i])
        if (lines[i] != "") s = s (s != "" ? "\n" : "") lines[i]
    }
    gsub(/\n\]/, "]", s)
    return s
}
function script(s, tag, mark,   out, k, inner, close_tag) {
    out = ""; close_tag = "</" tag ">"
    while (match(s, "<" tag "( [^>]*)?>")) {
        out = out substr(s, 1, RSTART - 1); s = substr(s, RSTART + RLENGTH)
        k = index(s, close_tag); if (!k) break
        inner = substr(s, 1, k - 1); gsub(/<[^>]*>/, "", inner); inner = trim(decode(inner))
        # an image placed inside <sup> is not an exponent
        out = out (inner == "" ? "" : inner ~ /\[(Image|image|math)/ ? " " inner " " : mark wrap(inner)); s = substr(s, k + length(close_tag))
    }
    return out s
}
function attr(tag, name,   re) {
    re = "[ \t\n]" name "=\"[^\"]*\""
    if (!match(tag, re)) return ""
    return substr(tag, RSTART + length(name) + 3, RLENGTH - length(name) - 4)
}
function u8(c) {
    if (c < 128) return sprintf("%c", c)
    if (c < 2048) return sprintf("%c%c", 192 + int(c / 64), 128 + c % 64)
    if (c < 65536) return sprintf("%c%c%c", 224 + int(c / 4096), 128 + int(c / 64) % 64, 128 + c % 64)
    return sprintf("%c%c%c%c", 240 + int(c / 262144), 128 + int(c / 4096) % 64, 128 + int(c / 64) % 64, 128 + c % 64)
}
function decode(s,   out, e, c) {
    out = ""
    while (match(s, /&(#[0-9]+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);/)) {
        e = substr(s, RSTART + 1, RLENGTH - 2)
        if (e ~ /^#[xX]/) c = strtonum("0x" substr(e, 3)); else if (e ~ /^#/) c = substr(e, 2) + 0
        else if (e in ENT) c = ENT[e]; else c = -1
        out = out substr(s, 1, RSTART - 1) (c >= 0 ? u8(c) : substr(s, RSTART, RLENGTH)); s = substr(s, RSTART + RLENGTH)
    }
    return out s
}

# --- MathML ---------------------------------------------------------------------------
function math(x,   j, t, root) {
    delete TOK; delete NAME; delete NCH; delete CH; delete TXT
    NTOK = 0
    while (x != "") {
        if (substr(x, 1, 1) == "<") { j = index(x, ">"); if (!j) break; TOK[++NTOK] = substr(x, 1, j); x = substr(x, j + 1) }
        else { j = index(x, "<"); if (!j) j = length(x) + 1; t = substr(x, 1, j - 1); if (t ~ /[^ \t\r\n]/) TOK[++NTOK] = t; x = substr(x, j) }
    }
    POS = 1; NN = 0; root = node("row")
    parse(root)
    t = render(root); gsub(NBSP, " ", t); gsub(/ +/, " ", t); sub(/^ /, "", t); sub(/ $/, "", t)
    return t
}
function node(nm) { NN++; NAME[NN] = nm; NCH[NN] = 0; TXT[NN] = ""; return NN }
function tagname(t) { sub(/^<\/?/, "", t); sub(/[ \t\r\n\/>].*$/, "", t); sub(/^.*:/, "", t); return tolower(t) }
function parse(par,   t, id) {
    while (POS <= NTOK) {
        t = TOK[POS]
        if (t ~ /^<\//) { POS++; return }
        if (t ~ /^<[!?]/) { POS++; continue }
        if (t ~ /^</) {
            id = node(tagname(t)); CH[par, ++NCH[par]] = id; POS++
            if (t !~ /\/>$/) parse(id)
        } else { id = node("#text"); TXT[id] = t; CH[par, ++NCH[par]] = id; POS++ }
    }
}
function simple(s) { return s ~ /^[A-Za-z0-9.]+$/ || s ~ /^\(.*\)$/ || s ~ /^[)\]}|]$/ }
function wrap(s) { return simple(s) ? s : "(" s ")" }
function isop(s) {
    return s == "=" || s == "+" || s == "-" || s == "<" || s == ">" || s == MINUS || s == HYPH || s == u8(215) || s == u8(247) || \
           s == u8(8804) || s == u8(8805) || s == u8(8800) || s == u8(183) || s == u8(8901) || s == u8(177) || s == u8(8776)
}
function render(id,   nm, i, out, c, r, prevop, n) {
    nm = NAME[id]
    if (nm == "#text") { r = decode(TXT[id]); gsub(/[\r\n\t]/, " ", r); return r }
    if (nm == "mfrac") return wrap(trim(render(CH[id, 1]))) "/" wrap(trim(render(CH[id, 2])))
    if (nm == "msup") return wrap(trim(render(CH[id, 1]))) "^" wrap(trim(render(CH[id, 2])))
    if (nm == "msub") return wrap(trim(render(CH[id, 1]))) "_" wrap(trim(render(CH[id, 2])))
    if (nm == "msubsup") return wrap(trim(render(CH[id, 1]))) "_" wrap(trim(render(CH[id, 2]))) "^" wrap(trim(render(CH[id, 3])))
    if (nm == "msqrt") return u8(8730) "(" trim(seq(id)) ")"
    if (nm == "mroot") return wrap(trim(render(CH[id, 2]))) u8(8730) "(" trim(render(CH[id, 1])) ")"
    if (nm == "mspace") return " "
    if (nm == "annotation" || nm == "annotation-xml") return ""
    if (nm == "semantics") return render(CH[id, 1])
    if (nm == "mfenced") { out = ""; for (i = 1; i <= NCH[id]; i++) out = out (i > 1 ? ", " : "") trim(render(CH[id, i])); return "(" out ")" }
    if (nm == "mtr") { out = ""; for (i = 1; i <= NCH[id]; i++) out = out (i > 1 ? "  " : "") trim(render(CH[id, i])); return out }
    if (nm == "mtable") { out = ""; for (i = 1; i <= NCH[id]; i++) out = out (i > 1 ? "; " : "") trim(render(CH[id, i])); return out }
    if (nm == "mtext" || nm == "ms") return seq(id)
    if (nm == "mn" || nm == "mi" || nm == "mo") return trim(seq(id))
    return seq(id)
}
# children in sequence: binary operators get spaces, a leading or repeated minus stays unary,
# and a fraction right after a whole number is a mixed number (3 1/4)
function seq(id,   i, c, r, out, prevop, op) {
    out = ""; prevop = 1
    for (i = 1; i <= NCH[id]; i++) {
        c = CH[id, i]; r = render(c)
        if (NAME[c] == "mo") {
            op = trim(r)
            if (op == "" ) { out = out " "; continue }
            if (isop(op)) {
                if ((op == "-" || op == MINUS || op == HYPH) && prevop) out = out op
                else out = out " " op " "
                prevop = 1; continue
            }
            out = out op; prevop = (op == "(" || op == "[" || op == ","); continue
        }
        if (NAME[c] == "mfrac" && out ~ /[0-9]$/) out = out " "
        out = out r; if (r ~ /[^ ]/) prevop = 0
    }
    return out
}
function trim(s) { gsub(NBSP, " ", s); sub(/^[ \t\r\n]+/, "", s); sub(/[ \t\r\n]+$/, "", s); return s }
