
from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass
class Config:
    chunksize: int = int(os.getenv("KCSV_CHUNKSIZE", "200_000").replace("_", ""))
    sample_rows: int | None = int(os.getenv("KCSV_SAMPLE", "0")) or None
    delimiter: str | None = os.getenv("KCSV_DELIM") or None
    engine: str = os.getenv("KCSV_ENGINE", "pyarrow")
    log_level: str = os.getenv("KCSV_LOG_LEVEL", "INFO")
