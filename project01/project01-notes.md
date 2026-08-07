project01-notes.md


## Which parts felt solid, which felt rusty

Solid: loops, string splitting, type conversion, basic function structure.
Reading a file line by line and accumulating counters is straightforward to me.

Rusty: most of it, honestly. Last time I wrote Python from scratch was a few
months ago and it showed. I followed the shape of what we built — I can see
why the code is organised the way it is — but I couldn't have written the
argparse subparser dispatch or the `set_defaults(func=...)` pattern on my own.
Same for `scripts/__init__.py` and how Python resolves imports across folders.
I know what those pieces do now; I don't yet know them well enough to reach
for them unprompted.

## Reading files and handling file errors

More comfortable than at the start. Concrete things I picked up:

- `with open(...)` closes the file for me — no manual cleanup.
- `FileNotFoundError` and `PermissionError` are separate cases worth catching
  separately. `ValueError` is the one that fires when `int("abc")` fails.
- Non-zero exit codes signal failure to whatever called the script. 1 for
  file problems, 2 for bad arguments.
- Errors go to `stderr`, results go to `stdout`.
- Slicing past the end of a list (`lines[1:4]` on a short file) doesn't crash.

The `parse_order_line` → returns dict or `None` pattern makes sense to me:
one function decides if a row is usable, the caller just checks for `None`.

## What tripped me up

Debugging is my weakest area — this is the thing to work on.

I created empty `.py` files with `touch`, ran them, got no output and exit
code 0, and didn't understand why. Three times. An empty Python file runs
successfully and does nothing. That's obvious in hindsight but I had no
instinct for reading the symptom.

Also lost time on:
- Relative paths. `data/sample_orders.txt` resolves against the current
  working directory, not the script's folder. Running from the wrong
  directory breaks it.
- `ImportError: cannot import name X` means the module was found but the
  function wasn't in it — different problem from `ModuleNotFoundError`.
- Local git commits don't touch GitHub until you add a remote and push.
- My terminal mangles multi-line pastes (bracketed paste escape codes).
  Environment issue, not Python, but it cost real time.

## Before JSON and pandas

Priority is debugging. Specifically I want to be able to:
- Read a traceback and know where to look, instead of guessing.
- Use `print()` checkpoints deliberately, and try `pdb` / the VS Code debugger.
- Recognise the common error types by their message.

Also want to revisit:
- Dicts. `totals_by(orders, key)` groups revenue by any field. I want to be
  able to write that from scratch without looking, because pandas `groupby`
  is the same operation and I'd rather understand it than treat it as magic.
- Imports and package structure — `__init__.py`, `sys.path`, why a file in a
  subfolder isn't automatically importable.
- Float precision. `115.47999999999999` is normal, not a bug. `:.2f` is a
  display fix, `decimal.Decimal` is the real fix for money.

## Note on the data

`data/messy_orders.txt` is deliberate — a copy of the sample file with three
broken rows appended (bad quantity, bad price, missing column). Used to prove
the invalid-row counter works. Not stray output.