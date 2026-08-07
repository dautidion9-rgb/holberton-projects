# project 02 notes

## which structure felt most natural

dicts. the records already come as dicts from json so it fit — `t["userId"]`
reads better than `row[0]` and doesnt break if field order changes.

sets clicked late but were the best part. `all_users - users_with_pending`
replaced the whole counting loop from task 1. one line instead of two count
dicts and a comparison.

lists were the least interesting here, just the container.

## where i switched to an index

`get_todos_by_user` scanned all 200 records every call. `build_user_index`
scans once and stores `{userId: [todos]}`, so after that its a dict lookup.

what changed: pay once upfront instead of every query. benchmark on 200k
records was 23x faster, break-even around 8 lookups. under that scanning wins
because you built the index for nothing.

kept both versions and asserted they match. that was useful — if id got the
argument order wrong the assert would catch it instead of silently returning
an empty list.

## how this shows up later

- train/test split leakage. `train_ids & test_ids` should be empty. same
  operator i used today
- `json.load()` gives a list of dicts. so did `load_orders()` in project01.
  thats what goes into `pd.DataFrame()`
- pandas groupby is `build_user_index` with a nicer api
- unique labels / classes are a set

## debugging notes

better today. things i actually did:
- output stopped with no traceback = code isnt there, not code is broken
- `wc -l` to catch a truncated paste instead of trusting the editor
- IndentationError "unexpected indent" → problem is usually the line above
- traceback said queries.py line 12 but the real error was indexing.py line
  105. read it bottom up, the last frame is where it broke
- grep reads the file on disk, editor shows a buffer. when they disagree
  grep is right

## environment

- vs code paste truncates past ~70 lines. cost me a lot of time. split long
  files in two and check `wc -l`
- check `pwd` before making files. got this wrong 4 times across both projects