# Extract claude_ordering (the practices Claude says a student needs, in order) from the Claude agents'
# free-text answer 1 files, r<row>_q1.md.
#
# Rule:
#   1. If the answer has a summary line with arrows ("Representing → Procedural Fluency", or "->"),
#      that line decides the ordering.
#   2. Otherwise the step structure decides: numbered items ("1. **Representing**"), "Step N",
#      "### N." headings, or "| N | **Practice** |" table rows, in the part about practices used.
#   In both, a step is left out when it is in parentheses or marked optional, conditional ("if stuck",
#   "only if") or check-only ("as a check", "reasonableness check"). Steps marked "minor" or "light use"
#   stay, since Claude still lists them as used. A practice used twice is listed once, where it is
#   first needed. Practice names outside the six (e.g. "Communicating", "Problem Solving") are ignored.
#   3. Rows in the overrides file (row <TAB> ordering) are decided by hand and win over 1 and 2.
#
# Usage:
#   LC_ALL=C gawk -b -v DIR=<folder with r<row>_q1.md> -v OVERRIDES=claude_ordering_overrides.tsv \
#       -v FROM=1 -v TO=300 -f claude_ordering.awk
# Output (TSV): row <TAB> source (arrow|steps|override|none) <TAB> ordering <TAB> arrow <TAB> steps

function canon(s,   t, i, p, best, bp) {
    t = tolower(s); gsub(/\*|`|_/, "", t)
    best = ""; bp = 1e9
    for (i = 1; i <= NA; i++) { p = index(t, ALIAS[i]); if (p && p < bp) { bp = p; best = ANAME[i] } }
    return best
}
function not_needed(s,   t) {
    t = tolower(s); gsub(/\*|`|_/, "", t)
    return (t ~ /optional|if stuck|gets stuck|only if|barely|as a check|light check|quick check|sense[- ]check|reasonableness|double[- ]check|to check|\(check\)|\(checking\)|\(verify\)|minor check/)
}
function add(name, list) {
    if (name == "" || index(" > " list " > ", " > " name " > ")) return list
    return list (list == "" ? "" : " > ") name
}
function trim(s) { sub(/^[ \t\r]+/, "", s); sub(/[ \t\r]+$/, "", s); return s }
function arrows_outside_parens(s,   out, i, c, depth) {
    out = ""; depth = 0
    for (i = 1; i <= length(s); i++) {
        c = substr(s, i, 1)
        if (c == "(") depth++
        else if (c == ")" && depth > 0) depth--
        if (depth > 0 && substr(s, i, 3) == ARROW) { out = out " "; i += 2; continue }
        out = out c
    }
    return out
}

BEGIN {
    na = split("abstracting and generalizing|Abstracting and Generalizing;justifying and proving|Justifying and Proving;" \
               "collaborative mathematics|Collaborative Mathematics;mathematical model|Mathematical Modeling;" \
               "procedural fluency|Procedural Fluency;representing|Representing;representation|Representing;" \
               "abstracting|Abstracting and Generalizing;generalizing|Abstracting and Generalizing;" \
               "justifying|Justifying and Proving;modeling|Mathematical Modeling;modelling|Mathematical Modeling;" \
               "procedural|Procedural Fluency", A, ";")
    NA = 0
    for (i = 1; i <= na; i++) { split(A[i], kv, "|"); NA++; ALIAS[NA] = kv[1]; ANAME[NA] = kv[2] }
    ARROW = "\342\206\222"
    if (OVERRIDES != "") while ((getline line < OVERRIDES) > 0) {
        if (line ~ /^#/ || line !~ /\t/) continue
        split(line, kv, "\t"); OV[kv[1] + 0] = kv[2]
    }

    for (r = FROM; r <= TO; r++) {
        f = DIR "/r" r "_q1.md"
        n = 0; delete L
        while ((getline line < f) > 0) { sub(/\r$/, "", line); gsub(/->/, ARROW, line); L[++n] = line }
        close(f)

        # ---------- 1. arrow line (prefer summary / order / sequence; never a "when stuck" path)
        aline = ""; apref = ""
        for (i = 1; i <= n; i++) {
            if (index(L[i], ARROW) == 0 || tolower(L[i]) ~ /stuck/) continue
            t = L[i]
            # a parenthesis that opens with an arrow is an optional extra step: "PF (→ optional Justifying check)"
            gsub("\\([ *]*" ARROW "[^)]*\\)", "", t)
            t = arrows_outside_parens(t)
            if (index(t, ARROW) == 0 || canon(t) == "") continue
            aline = t
            if (tolower(L[i]) ~ /summary|sequence|order|short|overall|in brief|key practices|main practices|core/) apref = t
        }
        if (apref != "") aline = apref
        arrow = ""
        if (aline != "") {
            np = split(aline, part, ARROW)
            for (k = 1; k <= np; k++) {
                p = trim(part[k]); gsub(/^\*+/, "", p); p = trim(p)
                if (k > 1 && p ~ /^\(/) continue
                # the step itself ends where a new clause starts ("..., with an optional ...", ". Procedural ...")
                head = p
                if (match(head, /[ (]with |, plus|\. |; /)) head = substr(head, 1, RSTART - 1)
                if (not_needed(head)) continue
                nm = head; sub(/\(.*$/, "", nm)
                if (k == 1) { nm = head; sub(/^.*: */, "", nm); sub(/\(.*$/, "", nm) }   # drop a "Summary order:" label
                nm = canon(nm)
                if (nm != "") arrow = add(nm, arrow)
            }
        }

        # ---------- 2. step structure
        steps = ""; inblock = 0; skipblock = 0; stop = 0; lastheading = ""
        i0 = 1
        for (i = 1; i <= n; i++) {
            low = tolower(L[i])
            if (L[i] ~ /^[ \t]*(\*\*)?[0-9]+[.)][ \t]/ || L[i] ~ /^\|[ \t]*(\*\*)?[0-9]/ || L[i] ~ /^#+[ \t]*[0-9]+\./) continue
            if (low ~ /practice/ && low ~ /order|used|needed|sequence|use them|step/ && low !~ /not (used|needed)|unused/) { i0 = i; break }
            if (low ~ /^\|[ ]*step[ ]*\|/) { i0 = i; break }
        }
        for (i = i0; i <= n && !stop; i++) {
            s = L[i]; low = tolower(s)
            isstep = (s ~ /^[ \t]*(\*\*)?[0-9]+[.)][ \t]/ || low ~ /^[ \t]*(\*\*)?step [0-9]+/ || s ~ /^\|[ \t]*(\*\*)?[0-9]+/ || s ~ /^#+[ \t]*[0-9]+\./)
            if (!isstep) {
                if (trim(s) == "") continue
                if (steps != "" && low ~ /^(#+|\*\*|- \*\*)?[ ]*(practices )?(that )?(are |play )?(not|unused|optional or not|less relevant|little or no|practices not|not needed|not used|not really|don.t|do not)/) { stop = 1; continue }
                if (low ~ /^(#+|\*\*)/ || low ~ /:\**[ ]*$/) { lastheading = low; inblock = 0 }
                continue
            }
            if (!inblock) {
                inblock = 1
                skipblock = (lastheading ~ /available|practice set|practices i.m using|(five|six)( mathematical| naep| math)? practices|the practices are|for reference|definitions|strands|framework/ \
                             && lastheading !~ /order|used|needed|step|sequence|solve/)
            }
            if (skipblock) continue
            if (s ~ /^\|/) { split(s, cell, "|"); seg = cell[2] " " cell[3]; whole = s }
            else { whole = s; if (match(s, /\*\*[^*]+\*\*/)) seg = substr(s, RSTART, RLENGTH); else seg = substr(s, 1, 90)
                   if (canon(seg) == "") seg = substr(s, 1, 90) }
            nm = canon(seg)
            if (nm == "") continue
            if (not_needed(seg) || not_needed(substr(whole, 1, 120))) continue
            steps = add(nm, steps)
        }

        if (r in OV) { src = "override"; ord = OV[r] }
        else if (arrow != "") { src = "arrow"; ord = arrow }
        else if (steps != "") { src = "steps"; ord = steps }
        else { src = "none"; ord = "" }
        printf "%d\t%s\t%s\t%s\t%s\n", r, src, ord, arrow, steps
    }
}
