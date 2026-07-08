from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class MetricKey:
    namespace: str
    name: str

    def as_tuple(self) -> Tuple[str, str]:
        return (self.namespace, self.name)


@dataclass
class Snapshot:
    counts: Dict[MetricKey, int] = field(default_factory=dict)

    def total(self) -> int:
        return sum(self.counts.values())

    def get(self, key: MetricKey) -> int:
        return self.counts.get(key, 0)
