
from pathlib import Path
from kcsv.processing import process_csv

def test_process_csv(tmp_path: Path):
    sample = tmp_path / "s.csv"
    sample.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    out = tmp_path / "out"
    summary = process_csv(sample, out, delimiter=",", chunksize=None, sample_rows=1)
    assert summary["rows"] == 2
    assert summary["columns"] == 2
    assert (out / "summary.json").exists()
    assert (out / "columns.csv").exists()
