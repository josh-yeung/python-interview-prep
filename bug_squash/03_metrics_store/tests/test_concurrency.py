from metrics_store import MetricKey, MetricsStore, run_parallel_mixed_keys, run_parallel_records


def test_single_threaded_record():
    store = MetricsStore()
    key = MetricKey(namespace="ingest", name="rows")

    for _ in range(100):
        store.record(key)

    assert store.get(key) == 100


def test_parallel_single_key():
    store = MetricsStore()
    key = MetricKey(namespace="ingest", name="events")
    workers = 20
    per_worker = 500
    expected = workers * per_worker

    run_parallel_records(store, key, num_workers=workers, iterations_per_worker=per_worker)

    assert store.get(key) == expected


def test_parallel_multiple_keys():
    store = MetricsStore()
    keys = [
        MetricKey(namespace="ingest", name="read"),
        MetricKey(namespace="ingest", name="write"),
        MetricKey(namespace="publish", name="sent"),
    ]
    workers = 16
    per_worker = 250
    expected_per_key = workers * per_worker

    run_parallel_mixed_keys(
        store, keys, num_workers=workers, iterations_per_worker=per_worker
    )

    for key in keys:
        assert store.get(key) == expected_per_key
