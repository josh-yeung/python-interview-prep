# Bug Squash Exercise 03 — Metrics Store

An in-memory metrics aggregator used by parallel pipeline workers to count per-key events.

## Setup

```bash
cd bug_squash/03_metrics_store
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
metrics_store/
  store.py       # MetricsStore counter
  worker.py      # WorkerPool and parallel helpers
  aggregator.py  # snapshot utilities
  types.py       # MetricKey, Snapshot
tests/
  test_concurrency.py
```

## Tips

- The single-threaded test passes; only parallel tests fail. That narrows the problem space.
- Look at what happens between reading a counter and writing it back.
- Workers deliberately start together (barrier) to maximize contention.
