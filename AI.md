# AI.md — dictodot

History lives in `AI_CHANGELOG.md` (append-only; read it for *why* something changed).
This file is present tense: a change rewrites its sentence here and appends an entry
there, in the same commit.

## What this repo is

Single-purpose utility: dot-notation access on top of `dict`/`OrderedDict`. One real
source file, `src/dictodot/main.py`, re-exported wholesale by `src/dictodot/__init__.py`
(`from dictodot.main import *`).

```
src/dictodot/main.py   # DotDict + dd_zeros/dd_empty/dd_full/df2dd
tests/test_numpy_optional.py
```

## API

- `DotDict(OrderedDict)`: `d.key` reads/writes/deletes as `d["key"]`/`d["key"] = v`/
  `del d["key"]`, raising `AttributeError` (not `KeyError`) on a missing key so it
  behaves like a normal object from the caller's point of view.
- `DotDict.Recursive(dct)`: recursively wraps nested plain dicts into `DotDict` too —
  used throughout this project's pipeline configs, e.g.
  `DotDict.Recursive(config)` in `ionmaidentools/pipelines.py` to turn a parsed job
  TOML into dotted-attribute config (`cfg.fragpipe.workflow_path` etc.).
- `DotDict.FromFrame(df)` / `df2dd`: DataFrame columns → `DotDict` of `numpy` arrays
  (`{col: df[col].to_numpy()}`).
- `dd_zeros`/`dd_empty`/`dd_full(shape, **name2dtype)`: build a `DotDict` of
  pre-allocated numpy arrays, one per kwarg (`dd_zeros((10,), mz=np.float64)`).

## Conventions

- **NumPy is optional and lazily imported.** `DotDict`/`Recursive`/`FromFrame` have no
  numpy dependency; only `dd_zeros`/`dd_empty`/`dd_full` need it, and they `import numpy`
  inside the function body precisely so the base package works without numpy installed
  (`pip install dictodot` vs `dictodot[numpy]`). `tests/test_numpy_optional.py` enforces
  this by importing `dictodot` in a subprocess with `-S` (no site-packages) and asserting
  it still works. Keep any new numpy-dependent helper's import inside the function, not
  at module level.
- `pyproject.toml` declares a `project.scripts` entry `example_shell_script =
  dictodot.cli.example_shell_script:example_shell_script` — there is no `dictodot.cli`
  module in this repo. Stale/dead entry point; don't rely on it, and don't be surprised
  if `pip install`-ing this package fails to expose that console script.
- Design rationale belongs here and history in `AI_CHANGELOG.md`, not in code
  docstrings — keep `main.py` comments about what the code does now, not why it changed.
