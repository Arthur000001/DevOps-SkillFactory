from pathlib import Path
import pytest
from kcsv.processing import process_csv


def make_csv(tmp_path: Path, content: str, name: str = "sample.csv") -> Path:
    f = tmp_path / name
    f.write_text(content, encoding="utf-8")
    return f


def test_basic_process(tmp_path: Path):
    f = make_csv(tmp_path, "a,b\n1,2\n3,4\n")
    out = tmp_path / "out"
    summary = process_csv(f, out, delimiter=",", chunksize=None, sample_rows=1)

    assert summary["rows"] == 2
    assert summary["columns"] == 2
    assert "a" in summary["column_names"]
    assert (out / "summary.json").exists()
    assert (out / "columns.csv").exists()


def test_with_semicolon_delimiter(tmp_path: Path):
    f = make_csv(tmp_path, "a;b\n1;2\n3;4\n")
    out = tmp_path / "out"
    summary = process_csv(f, out, delimiter=";", chunksize=None, sample_rows=2)
    assert summary["columns"] == 2
    assert summary["rows"] == 2


def test_with_chunksize(tmp_path: Path):
    f = make_csv(tmp_path, "a,b\n" + "\n".join(f"{i},{i*2}" for i in range(100)))
    out = tmp_path / "out"
    summary = process_csv(f, out, delimiter=",", chunksize=10, sample_rows=5)
    assert summary["rows"] == 100
    assert summary["columns"] == 2


def test_empty_file(tmp_path: Path):
    f = make_csv(tmp_path, "", "empty.csv")
    out = tmp_path / "out"
    with pytest.raises(Exception):
        process_csv(f, out, delimiter=",")
