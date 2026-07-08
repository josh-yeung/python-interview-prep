# Bug Squash Exercise 02 — Config Linter

A linter for a small Python-based pipeline configuration DSL. Config files are parsed as ASTs and validated against project rules.

## Setup

```bash
cd bug_squash/02_config_linter
python -m venv .venv
```

Windows: `.\.venv\Scripts\activate`  
macOS/Linux: `source .venv/bin/activate`

```bash
pip install -r ../requirements.txt
```

## Run tests

```bash
python -m pytest -v
```

Some tests pass and some fail. Read the traceback, find the bug, fix it, and re-run until all tests pass.

## Package layout

```
config_linter/
  linter.py      # orchestrates parse → validate → report
  parser.py      # reads files and builds ASTs
  validators.py  # ConfigValidator visitor
  rules.py       # allowed keys and action strings
  reporter.py    # formats lint results
tests/
  fixtures/      # sample config files
  test_linter.py
```

## Tips

- The failing test uses a config with a tuple literal. Compare it to the passing list config.
- Trace how nodes are visited — what happens when the walker hits an unhandled node type?
- Reuse existing validation logic where possible; don't rewrite the whole visitor.
