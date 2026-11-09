# Pack the rendered problem files into one JSONL file: {"row": N, "problem_id": "...", "text": "..."}
# Input: a "row<TAB>problem_id" list (not the CSV itself: in --csv mode gawk would also parse the
# problem files as CSV and join lines inside quotes).
# Usage:
#   gawk --csv 'NR>1 {print NR-1 "\t" $10}' Problems.csv > ids.tsv
#   LC_ALL=C gawk -b -F'\t' -v PDIR=<dir of p<row>.txt> -f to_jsonl.awk ids.tsv > problems_rendered.jsonl
# Byte mode: UTF-8 is copied byte by byte; backslash, quote, tab, CR and newline are escaped.
# The rendered files contain no other control characters (checked when the file was made).
function esc(s) {
    gsub(/[\\]/, "&&", s)
    gsub(/["]/, "\\\"", s)
    gsub(/\t/, "\\t", s)
    gsub(/\r/, "\\r", s)
    gsub(/\n/, "\\n", s)
    return s
}
{
    row = $1; f = PDIR "/p" row ".txt"; t = ""; first = 1
    while ((getline l < f) > 0) { t = t (first ? "" : "\n") l; first = 0 }
    close(f)
    if (first) { print "missing " f > "/dev/stderr"; exit 1 }
    printf "{\"row\": %d, \"problem_id\": \"%s\", \"text\": \"%s\"}\n", row, esc($2), esc(t)
}
