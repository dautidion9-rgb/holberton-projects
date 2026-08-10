# project 03 notes

## how the etl split affected organisation

made it clearer. each file has one job so i knew where to put things —
reading goes in extract, cleaning in transform, writing in load, and
pipeline just calls them in order.

pipeline.py has no logic of its own, same as toolbox.py in project01.

## which step needed the most decisions

pipeline. the individual steps were each simple but wiring them took the
most thinking — what paths to default to, what order, what to print at the
end, whether the counts at each stage should match.

the count check (extracted vs written) came from that. if the pipeline
silently drops records the output still looks fine, so comparing both ends
catches it.

transform had the most small choices even if they were easy — strip the
title, keep original case, add completed_int and title_length, and build a
new dict instead of modifying the input so the function stays pure.

## plugging in a different json dataset

would change:
- FIELDS in extract.py (which fields to keep)
- transform_todo (different cleaning rules and derived fields)
- FIELDNAMES and to_csv_row in load.py (csv schema)

would not change:
- pipeline.py
- the function signatures. extract returns a list of dicts, transform takes
  a list and returns a list, load writes a list

so a new dataset changes what's inside the functions, not the structure.
thats the point of splitting it up.

## things i noticed

- csv has no types. True comes out as the string "True", and bool("False")
  is True in python, so completed_int exists to avoid that
- newline="" when opening a csv or you get blank lines between rows
- DictWriter validates against fieldnames, so an unexpected key raises
  instead of silently writing a wrong column
- titles with commas get quoted automatically. thats why you use the csv
  module instead of ",".join()

## still to work on

pure functions made sense here — transform takes data and returns data, no
file access, so it can be tested with a couple of dicts typed by hand
instead of needing the real file.

still leaning on being given the code rather than writing it. thats the
main thing to fix before the program starts.
