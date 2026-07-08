import ast
from typing import List, Optional

from config_linter import rules
from config_linter.reporter import LintIssue


class ConfigValidator(ast.NodeVisitor):
    """Validates pipeline config assignments against project rules."""

    def __init__(self) -> None:
        self.issues: List[LintIssue] = []
        self._current_key: Optional[str] = None

    def visit(self, node: ast.AST) -> None:
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self._missing_visitor)
        return visitor(node)

    def _missing_visitor(self, node: ast.AST) -> None:
        raise NotImplementedError(
            f"No visitor for {node.__class__.__name__}"
        )

    def visit_Module(self, node: ast.Module) -> None:
        for child in node.body:
            self.visit(child)

    def visit_Assign(self, node: ast.Assign) -> None:
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            self.issues.append(
                LintIssue(node.lineno, "assignments must target a simple name")
            )
            return

        key = node.targets[0].id
        if key not in rules.ALLOWED_TOP_LEVEL_KEYS:
            self.issues.append(
                LintIssue(node.lineno, f"unknown config key: {key}")
            )
            return

        previous_key = self._current_key
        self._current_key = key
        self.visit(node.value)
        self._current_key = previous_key

    def visit_Constant(self, node: ast.Constant) -> None:
        if self._current_key == "ACTIONS" and isinstance(node.value, str):
            if node.value not in rules.ALLOWED_ACTIONS:
                self.issues.append(
                    LintIssue(node.lineno, f"unknown action: {node.value!r}")
                )
        elif self._current_key == "RETRIES":
            if not isinstance(node.value, int) or not (
                0 <= node.value <= rules.MAX_RETRIES
            ):
                self.issues.append(
                    LintIssue(
                        node.lineno,
                        f"RETRIES must be an integer between 0 and {rules.MAX_RETRIES}",
                    )
                )

    def visit_List(self, node: ast.List) -> None:
        for element in node.elts:
            self.visit(element)

    def visit_Dict(self, node: ast.Dict) -> None:
        for key_node, value_node in zip(node.keys, node.values):
            if key_node is not None:
                self.visit(key_node)
            if value_node is not None:
                self.visit(value_node)
