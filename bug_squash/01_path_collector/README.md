# Bug Squash Exercise 01 — Path Collector

A file-ingestion utility that expands user-supplied paths into files ready for processing.

## Setup

```bash
cd bug_squash/01_path_collector
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
path_collector/
  collector.py   # path expansion and directory scanning
  filters.py     # extension and hidden-file filtering
  models.py      # data structures
  exceptions.py
tests/
  test_collector.py
```

## Tips

- Start with the failing test name — it describes expected behavior.
- Compare how directories vs individual files are handled.
- A minimal fix should make every test pass without changing test code.
