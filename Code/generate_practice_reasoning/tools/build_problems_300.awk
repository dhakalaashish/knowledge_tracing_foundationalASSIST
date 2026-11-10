# Build Data/problems_300.csv: Claude's labels for rows 1-300, plus empty columns for the human review.
#
# Inputs (no --csv: in --csv mode gawk would also parse the answer files as CSV):
#   labels.tsv    row <TAB> problem_id <TAB> predicted_practice <TAB> claude_top_practice, made with
#                 gawk --csv 'NR>1 && NR<=301 {print NR-1 "\t" $10 "\t" $13 "\t" $15}' Data/Problems.csv
#   ordering.tsv  output of claude_ordering.awk (row, source, ordering, ...)
#   DIR           folder with the agents' answer 2 files r<row>_q2.md (the reason for the top practice)
# Usage:
#   gawk -F'\t' -v DIR=<answers folder> -f build_problems_300.awk ordering.tsv labels.tsv > Data/problems_300.csv
# The CSV uses minimal quoting and LF line endings, like Problems.csv.

function q(s) { if (s ~ /[",\n\r]/) { gsub(/"/, "\"\"", s); s = "\"" s "\"" } return s }
function slurp(f,   s, l, first) {
    s = ""; first = 1
    while ((getline l < f) > 0) { sub(/\r$/, "", l); s = s (first ? "" : "\n") l; first = 0 }
    close(f); sub(/\n+$/, "", s); return s
}
FNR == NR { ord[$1] = $3; next }
FNR == 1 {
    print "row,problem_id,predicted_practice,claude_ordering,claude_top_practice,claude_top_practice_reasoning," \
          "aashish_ordering_agrees,aashish_ordering,aashish_top_practice_agrees,aashish_top_practice,aashish_note,aashish_updated"
}
{
    r = $1
    if (!(r in ord) || ord[r] == "") { print "no claude_ordering for row " r > "/dev/stderr"; exit 1 }
    why = slurp(DIR "/r" r "_q2.md")
    if (why == "") { print "no answer 2 for row " r > "/dev/stderr"; exit 1 }
    print q(r) "," q($2) "," q($3) "," q(ord[r]) "," q($4) "," q(why) ",,,,,,"
    n++
}
END { print n " rows" > "/dev/stderr" }
