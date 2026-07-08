from config_linter.parser import read_and_parse
from config_linter.reporter import LintReport
from config_linter.validators import ConfigValidator


def lint_source(source: str, filepath: str = "<config>") -> LintReport:
    from config_linter.parser import parse_config

    tree = parse_config(source, filename=filepath)
    validator = ConfigValidator()
    validator.visit(tree)
    return LintReport(filepath=filepath, issues=validator.issues)


def lint_file(filepath: str) -> LintReport:
    tree = read_and_parse(filepath)
    validator = ConfigValidator()
    validator.visit(tree)
    return LintReport(filepath=filepath, issues=validator.issues)
