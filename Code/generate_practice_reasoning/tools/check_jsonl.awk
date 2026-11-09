# Check that problems_rendered.jsonl decodes back to the rendered files byte for byte.
# Usage: LC_ALL=C gawk -b -v PDIR=<dir of p<row>.txt> -f check_jsonl.awk problems_rendered.jsonl
function unesc(s,   out, i, c, d) {
    out = ""
    for (i = 1; i <= length(s); i++) {
        c = substr(s, i, 1)
        if (c != "\\") { out = out c; continue }
        d = substr(s, ++i, 1)
        out = out (d == "n" ? "\n" : d == "t" ? "\t" : d == "r" ? "\r" : d)
    }
    return out
}
{
    match($0, /"row": [0-9]+/); r = substr($0, RSTART + 7, RLENGTH - 7)
    k = index($0, "\"text\": \""); t = substr($0, k + 9); sub(/"}$/, "", t); t = unesc(t)
    f = PDIR "/p" r ".txt"; s = ""; first = 1
    while ((getline l < f) > 0) { s = s (first ? "" : "\n") l; first = 0 }
    close(f)
    if (s != t) { bad++; if (bad <= 3) print "mismatch in row " r }
    if (r != NR) { order++ }
}
END { print "rows: " NR ", mismatches: " bad + 0 ", out of order: " order + 0 }
