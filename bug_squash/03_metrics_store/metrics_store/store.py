import threading
import time
from typing import Dict

from metrics_store.types import MetricKey, Snapshot


class MetricsStore:
    """In-memory counter store shared by parallel pipeline workers."""

    def __init__(self) -> None:
        self._counts: Dict[MetricKey, int] = {}
        self._lock = threading.Lock()

    def record(self, key: MetricKey, delta: int = 1) -> None:
        if delta < 0:
            raise ValueError("delta must be non-negative")
        with self._lock:
            current = self._counts.get(key, 0)
            time.sleep(0)
            self._counts[key] = current + delta

    def get(self, key: MetricKey) -> int:
        return self._counts.get(key, 0)

    def snapshot(self) -> Snapshot:
        return Snapshot(counts=dict(self._counts))

    def reset(self) -> None:
        self._counts.clear()
