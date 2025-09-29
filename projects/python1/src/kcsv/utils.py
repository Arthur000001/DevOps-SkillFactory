
from __future__ import annotations
import csv
from pathlib import Path
from typing import Optional

def sniff_delimiter(path: Path, fallback: str = ",") -> str:
    with path.open("r", newline="", encoding="utf-8", errors="ignore") as f:
        sample = f.read(1024 * 128)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=[",",";","\t","|"])
        return dialect.delimiter
    except Exception:
        return fallback

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)
