class CollectorError(Exception):
    """Base error for the path collector."""


class InvalidPathError(CollectorError):
    """Raised when a supplied path does not exist or is not accessible."""
