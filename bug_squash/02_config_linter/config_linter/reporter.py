import ast
from dataclasses import dataclass
from typing import List


@dataclass
class LintIssue:
    lineno: int
    message: str

    def format(self) -> str:
        return f"line {self.lineno}: {self.message}"


@dataclass
class LintReport:
    filepath: str
    issues: List[LintIssue]

    @property
    def ok(self) -> bool:
        return len(self.issues) == 0

    def formatted(self) -> str:
        if self.ok:
            return f"{self.filepath}: OK"
        lines = [f"{self.filepath}:"]
        lines.extend(issue.format() for issue in self.issues)
        return "\n".join(lines)
