import pathlib

import pytest

from config_linter import lint_file, lint_source

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def test_simple_scalar_and_dict_config():
    source = (FIXTURES / "simple_config.py").read_text(encoding="utf-8")
    report = lint_source(source, filepath="simple_config.py")
    assert report.ok


def test_list_config():
    report = lint_file(str(FIXTURES / "list_config.py"))
    assert report.ok


def test_tuple_config():
    report = lint_file(str(FIXTURES / "tuple_config.py"))
    assert report.ok


def test_unknown_key_reports_issue():
    report = lint_file(str(FIXTURES / "invalid_key_config.py"))
    assert not report.ok
    assert any("unknown config key" in issue.message for issue in report.issues)
