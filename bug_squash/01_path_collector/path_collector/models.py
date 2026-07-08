from dataclasses import dataclass, field
from typing import List


@dataclass
class FileRecord:
    path: str
    size_bytes: int
    extension: str


@dataclass
class ScanResult:
    records: List[FileRecord] = field(default_factory=list)
    skipped_hidden: int = 0
    skipped_extension: int = 0

    @property
    def total_files(self) -> int:
        return len(self.records)

    @property
    def total_bytes(self) -> int:
        return sum(record.size_bytes for record in self.records)
