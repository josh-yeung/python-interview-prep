from typing import Dict, Iterable, List, Tuple

from metrics_store.types import MetricKey, Snapshot


def sum_namespace(snapshot: Snapshot, namespace: str) -> int:
    total = 0
    for key, count in snapshot.counts.items():
        if key.namespace == namespace:
            total += count
    return total


def merge_snapshots(snapshots: Iterable[Snapshot]) -> Snapshot:
    merged: Dict[MetricKey, int] = {}
    for snapshot in snapshots:
        for key, count in snapshot.counts.items():
            merged[key] = merged.get(key, 0) + count
    return Snapshot(counts=merged)


def top_keys(snapshot: Snapshot, limit: int = 5) -> List[Tuple[MetricKey, int]]:
    ranked = sorted(snapshot.counts.items(), key=lambda item: item[1], reverse=True)
    return ranked[:limit]
