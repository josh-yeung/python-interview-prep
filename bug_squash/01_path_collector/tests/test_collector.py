import pytest

from path_collector import collect_files, expand_paths
from path_collector.exceptions import InvalidPathError


@pytest.fixture
def sample_tree(tmp_path):
    root = tmp_path / "data"
    root.mkdir()
    (root / "alpha.txt").write_text("alpha")
    (root / "beta.csv").write_text("beta")
    nested = root / "nested"
    nested.mkdir()
    (nested / "gamma.json").write_text("{}")
    (root / ".hidden.log").write_text("secret")
    (root / "skip.exe").write_text("binary")
    return root


def test_collect_directory(sample_tree):
    result = collect_files(str(sample_tree))
    paths = {record.path for record in result.records}
    assert len(result.records) == 3
    assert any("alpha.txt" in path for path in paths)
    assert any("beta.csv" in path for path in paths)
    assert any("gamma.json" in path for path in paths)


def test_collect_skips_hidden_and_wrong_extension(sample_tree):
    result = collect_files(str(sample_tree))
    paths = {record.path for record in result.records}
    assert not any(".hidden.log" in path for path in paths)
    assert not any("skip.exe" in path for path in paths)
    assert result.skipped_hidden == 1
    assert result.skipped_extension == 1


def test_expand_single_file_path(sample_tree, tmp_path):
    single = tmp_path / "standalone.txt"
    single.write_text("one file")

    expanded = expand_paths([str(single)])

    assert expanded == [str(single.resolve())]


def test_expand_mixed_file_and_directory(sample_tree, tmp_path):
    single = tmp_path / "standalone.txt"
    single.write_text("one file")

    expanded = expand_paths([str(single), str(sample_tree)])

    assert str(single.resolve()) in expanded
    assert any("alpha.txt" in path for path in expanded)
    assert any("gamma.json" in path for path in expanded)


def test_missing_path_raises():
    with pytest.raises(InvalidPathError):
        expand_paths(["/no/such/path/at/all"])
