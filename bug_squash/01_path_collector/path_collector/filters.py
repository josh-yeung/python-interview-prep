import os
from typing import Optional, Set, Tuple


DEFAULT_EXTENSIONS = {".txt", ".csv", ".json", ".log"}


def normalize_path(path: str) -> str:
    return os.path.normpath(os.path.abspath(path))


def is_hidden(name: str) -> bool:
    return name.startswith(".")


def has_allowed_extension(filename: str, allowed: Set[str]) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in allowed


def should_include_file(
    filename: str,
    allowed_extensions: Set[str],
    include_hidden: bool,
) -> Tuple[bool, Optional[str]]:
    if not include_hidden and is_hidden(filename):
        return False, "hidden"
    if not has_allowed_extension(filename, allowed_extensions):
        return False, "extension"
    return True, None
