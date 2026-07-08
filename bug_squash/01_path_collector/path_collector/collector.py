import os
from typing import Iterable, List, Optional, Set

from path_collector.exceptions import InvalidPathError
from path_collector.filters import normalize_path, should_include_file
from path_collector.models import FileRecord, ScanResult

DEFAULT_EXTENSIONS = {".txt", ".csv", ".json", ".log"}


def _build_record(path: str) -> FileRecord:
    _, ext = os.path.splitext(path)
    return FileRecord(
        path=normalize_path(path),
        size_bytes=os.path.getsize(path),
        extension=ext.lower(),
    )


def _scan_directory(
    directory: str,
    allowed_extensions: Set[str],
    include_hidden: bool,
    result: ScanResult,
) -> None:
    for entry in os.scandir(directory):
        if entry.is_dir(follow_symlinks=False):
            _scan_directory(entry.path, allowed_extensions, include_hidden, result)
            continue
        if not entry.is_file(follow_symlinks=False):
            continue

        include, reason = should_include_file(
            entry.name, allowed_extensions, include_hidden
        )
        if not include:
            if reason == "hidden":
                result.skipped_hidden += 1
            elif reason == "extension":
                result.skipped_extension += 1
            continue

        result.records.append(_build_record(entry.path))


def collect_files(
    root: str,
    allowed_extensions: Optional[Set[str]] = None,
    include_hidden: bool = False,
) -> ScanResult:
    """Collect files under root, applying extension and hidden-file filters."""
    allowed = allowed_extensions or DEFAULT_EXTENSIONS
    normalized = normalize_path(root)

    if not os.path.exists(normalized):
        raise InvalidPathError(f"Path does not exist: {root}")

    result = ScanResult()
    _scan_directory(normalized, allowed, include_hidden, result)
    return result


def expand_paths(paths: Iterable[str]) -> List[str]:
    """Expand a list of user-supplied paths into individual file paths."""
    expanded: List[str] = []

    for raw_path in paths:
        path = normalize_path(raw_path)
        if not os.path.exists(path):
            raise InvalidPathError(f"Path does not exist: {raw_path}")

        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                expanded.append(normalize_path(entry.path))
            elif entry.is_dir(follow_symlinks=False):
                scan = collect_files(entry.path)
                expanded.extend(record.path for record in scan.records)

    return expanded


def stats(result: ScanResult) -> dict:
    by_extension: dict[str, int] = {}
    for record in result.records:
        by_extension[record.extension] = by_extension.get(record.extension, 0) + 1

    return {
        "total_files": result.total_files,
        "total_bytes": result.total_bytes,
        "skipped_hidden": result.skipped_hidden,
        "skipped_extension": result.skipped_extension,
        "by_extension": by_extension,
    }
