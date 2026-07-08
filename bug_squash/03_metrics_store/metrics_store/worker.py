import threading
from typing import Callable, Iterable, List

from metrics_store.store import MetricsStore
from metrics_store.types import MetricKey


class WorkerPool:
    """Runs a callable concurrently across multiple threads."""

    def __init__(self, num_workers: int) -> None:
        if num_workers < 1:
            raise ValueError("num_workers must be at least 1")
        self.num_workers = num_workers

    def map(self, fn: Callable[[], None]) -> None:
        barrier = threading.Barrier(self.num_workers)
        errors: List[BaseException] = []

        def runner() -> None:
            try:
                barrier.wait()
                fn()
            except BaseException as exc:
                errors.append(exc)

        threads = [threading.Thread(target=runner) for _ in range(self.num_workers)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        if errors:
            raise errors[0]


def run_parallel_records(
    store: MetricsStore,
    key: MetricKey,
    num_workers: int,
    iterations_per_worker: int,
) -> None:
    def work() -> None:
        for _ in range(iterations_per_worker):
            store.record(key)

    WorkerPool(num_workers).map(work)


def run_parallel_mixed_keys(
    store: MetricsStore,
    keys: Iterable[MetricKey],
    num_workers: int,
    iterations_per_worker: int,
) -> None:
    key_list = list(keys)

    def work() -> None:
        for _ in range(iterations_per_worker):
            for key in key_list:
                store.record(key)

    WorkerPool(num_workers).map(work)
