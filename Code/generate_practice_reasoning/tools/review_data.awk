# Data for the Claude-label review page (rows 1-300), written as JavaScript.
# Three separate passes, because in --csv mode gawk would also parse the answer files as CSV:
#
#   PRACTICES (definitions and descriptors from augment_mathematical_practice.py):
#     LC_ALL=C gawk -b -v MODE=practices -f review_data.awk ../../augment_mathematical_practice.py
#   PROBLEMS (problem fields and skills for rows FROM..TO):
#     LC_ALL=C gawk -b --csv -v MODE=problems -v FROM=1 -v TO=300 -f review_data.awk Data/Skills.csv Data/Problems.csv
#   CLAUDE (ordering, top practice and both answers, from claude_ordering.tsv and the answer files):
#     LC_ALL=C gawk -b -F'\t' -v MODE=claude -v DIR=<answers folder> -f review_data.awk claude_ordering.tsv labels.tsv
#     (labels.tsv: row <TAB> problem_id <TAB> predicted_practice <TAB> claude_top_practice)

function js(s) {
    gsub(/\r/, "", s)
    gsub(/[\001-\010\013\014\016-\037]/, "", s)
    gsub(/\\/, "\\\\", s); gsub(/"/, "\\\"", s)
    gsub(/\n/, "\\n", s); gsub(/\t/, "\\t", s)
    gsub(/<\//, "<\\/", s)
    return "\"" s "\""
}
function slurp(f,   s, l, first) {
    s = ""; first = 1
    while ((getline l < f) > 0) { sub(/\r$/, "", l); s = s (first ? "" : "\n") l; first = 0 }
    close(f); sub(/\n+$/, "", s); return s
}
BEGIN {
    split("REPRESENTING ABSTRACTING JUSTIFYING MODELING COLLABORATIVE PROCEDURAL", PNAME, " ")
    split("Representing|Abstracting and Generalizing|Justifying and Proving|Mathematical Modeling|Collaborative Mathematics|Procedural Fluency", NAME, "|")
}

# ---------- PRACTICES
MODE == "practices" {
    if (match($0, /^PROMPT_([A-Z]+) = """/, m)) { cur = m[1]; mode = ""; next }
    if (cur != "" && $0 ~ /^"""/) { cur = ""; next }
    if (cur == "") next
    if (tolower($0) ~ /^practice definition:/) { mode = "def"; next }
    if (tolower($0) ~ /^practice descriptors:/) { mode = "desc"; next }
    if (mode == "def" && $0 !~ /^[[:space:]]*$/ && def[cur] == "") { def[cur] = $0; next }
    if (mode == "desc" && match($0, /^[[:space:]]*- (.*)$/, d)) desc[cur] = desc[cur] (desc[cur] == "" ? "" : "\036") d[1]
    next
}

# ---------- PROBLEMS
MODE == "problems" && FILENAME ~ /Skills/ {
    if (FNR == 1) next
    pid = $1; code = $3; nm = $4; gsub(/^ +| +$/, "", nm); gsub(/^ +| +$/, "", code)
    if (pid == "" || code == "") next
    lab = nm " (" code ")"
    if (index("\037" sk[pid] "\037", "\037" lab "\037") == 0) sk[pid] = sk[pid] (sk[pid] == "" ? "" : "\037") lab
    next
}
MODE == "problems" {
    if (FNR == 1) { for (i = 1; i <= NF; i++) h[$i] = i; next }
    row = FNR - 1
    if (row < FROM || row > TO) next
    pid = $(h["problem_id"]); gsub(/^ +| +$/, "", pid)
    rec[++n] = "{row:" row ",i:" js(pid) ",t:" js($(h["Problem Type"])) ",a:" js($(h["Answer Types"])) \
        ",b:" js($(h["Problem Body"])) ",fo:" js($(h["Fill-in Options"])) ",fa:" js($(h["Fill-in Answers"])) \
        ",mo:" js($(h["Multiple Choice Options"])) ",ma:" js($(h["Multiple Choice Answers"])) \
        ",s:" js(gensub(/\037/, "; ", "g", sk[pid])) ",pred:" js($(h["predicted_practice"])) "}"
    next
}

# ---------- CLAUDE
MODE == "claude" && FNR == NR { ord[$1] = $3; next }
MODE == "claude" {
    r = $1; n2 = split(ord[r], o, " > "); list = ""
    for (k = 1; k <= n2; k++) list = list (k > 1 ? "," : "") js(o[k])
    crec[++nc] = "{row:" r ",order:[" list "],top:" js($4) ",a1:" js(slurp(DIR "/r" r "_q1.md")) ",a2:" js(slurp(DIR "/r" r "_q2.md")) "}"
    next
}

END {
    if (MODE == "practices") {
        printf "const PRACTICES = ["
        for (j = 1; j <= 6; j++) {
            p = PNAME[j]; nd = split(desc[p], dd, "\036"); list = ""
            for (k = 1; k <= nd; k++) list = list (k > 1 ? "," : "") js(dd[k])
            printf "%s\n  {name:%s,def:%s,desc:[%s]}", (j > 1 ? "," : ""), js(NAME[j]), js(def[p]), list
            if (def[p] == "") print "missing definition for " p > "/dev/stderr"
        }
        print "\n];"
    }
    if (MODE == "problems") {
        printf "const PROBLEMS = ["
        for (k = 1; k <= n; k++) printf "%s\n%s", (k > 1 ? "," : ""), rec[k]
        print "\n];"
        print n " problems" > "/dev/stderr"
    }
    if (MODE == "claude") {
        printf "const CLAUDE = ["
        for (k = 1; k <= nc; k++) printf "%s\n%s", (k > 1 ? "," : ""), crec[k]
        print "\n];"
        print nc " Claude records" > "/dev/stderr"
    }
}
