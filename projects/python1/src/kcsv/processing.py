from __future__ import annotations
import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import matplotlib.pyplot as plt

from .utils import ensure_dir, sniff_delimiter


# ===================== helpers =====================

try:
    import pyarrow  # noqa: F401
    _HAS_PYARROW = True
except Exception:
    _HAS_PYARROW = False


def _pick_engine(pref: str) -> tuple[str, Optional[str]]:
    """
    Вернёт (engine, dtype_backend) для pd.read_csv.
    Если pyarrow недоступен — откат на 'c'.
    """
    pref = (pref or "").lower()
    if pref == "pyarrow" and _HAS_PYARROW:
        return "pyarrow", "pyarrow"
    if pref in {"c", "python"}:
        return pref, None
    return ("pyarrow", "pyarrow") if _HAS_PYARROW else ("c", None)


# ===================== stats =====================

@dataclass
class ColumnStats:
    name: str
    dtype: str
    non_nulls: int
    nulls: int
    nunique: int
    min: Optional[float]
    max: Optional[float]
    mean: Optional[float]


def _is_numeric(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series.dtype)


def summarize_dataframe(df: pd.DataFrame) -> Dict:
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(map(str, df.columns)),
    }


def column_stats(df: pd.DataFrame) -> List[ColumnStats]:
    stats: List[ColumnStats] = []
    for col in df.columns:
        s = df[col]
        nn = int(s.notna().sum())
        na = int(s.isna().sum())
        nunique = int(s.nunique(dropna=True))
        if _is_numeric(s) and nn:
            desc = s.describe()
            stats.append(
                ColumnStats(
                    str(col),
                    str(s.dtype),
                    nn,
                    na,
                    nunique,
                    float(desc.get("min", float("nan"))),
                    float(desc.get("max", float("nan"))),
                    float(desc.get("mean", float("nan"))),
                )
            )
        else:
            stats.append(ColumnStats(str(col), str(s.dtype), nn, na, nunique, None, None, None))
    return stats


def save_histograms(df: pd.DataFrame, out_dir: Path) -> List[Path]:
    plots_dir = out_dir / "plots"
    ensure_dir(plots_dir)
    paths: List[Path] = []
    for col in df.columns:
        s = df[col]
        if pd.api.types.is_numeric_dtype(s.dtype):
            fig = plt.figure()
            s.dropna().plot(kind="hist", bins=30, title=str(col))
            plot_path = plots_dir / f"{col}.png"
            fig.savefig(plot_path, bbox_inches="tight")
            plt.close(fig)
            paths.append(plot_path)
    return paths


# ===================== main =====================

def process_csv(
    in_path: Path,
    out_dir: Path,
    delimiter: Optional[str] = None,
    chunksize: Optional[int] = None,
    engine: str = "pyarrow",
    sample_rows: Optional[int] = None,
) -> Dict:
    ensure_dir(out_dir)

    # logging
    log_path = out_dir / "kcsv.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
    )
    logger = logging.getLogger("kcsv")

    if delimiter is None:
        delimiter = sniff_delimiter(in_path)

    eng, dtype_backend = _pick_engine(engine)
    logger.info("Reading %s with delimiter '%s' (engine=%s)", in_path, delimiter, eng)

    # Аргументы чтения без конфликтов для pyarrow
    read_kwargs: dict = {"sep": delimiter, "engine": eng, "chunksize": chunksize}
    if eng != "pyarrow":
        read_kwargs["low_memory"] = False
    if dtype_backend is not None:
        read_kwargs["dtype_backend"] = dtype_backend

    reader = pd.read_csv(in_path, **read_kwargs)

    summary = {"rows": 0, "columns": 0, "column_names": []}
    accum_df: Optional[pd.DataFrame] = None
    first_chunk = True

    if chunksize:
        # потоковая обработка
        for chunk in reader:  # type: ignore
            if first_chunk:
                summary = summarize_dataframe(chunk)
                first_chunk = False
            summary["rows"] += int(chunk.shape[0])

            if sample_rows:
                take = min(sample_rows, len(chunk))
                if take > 0:
                    part = chunk.sample(n=take, random_state=42)
                    accum_df = part if accum_df is None else pd.concat([accum_df, part], ignore_index=True)
                    if len(accum_df) > sample_rows:
                        accum_df = accum_df.sample(n=sample_rows, random_state=42).reset_index(drop=True)

        if accum_df is not None:
            df_for_stats = accum_df
        else:
            # перечитываем голову для статов
            head_kwargs = {"sep": delimiter, "engine": eng, "nrows": 50_000}
            if eng != "pyarrow":
                head_kwargs["low_memory"] = False
            if dtype_backend is not None:
                head_kwargs["dtype_backend"] = dtype_backend
            df_for_stats = pd.read_csv(in_path, **head_kwargs)
    else:
        # без чанков
        if isinstance(reader, pd.DataFrame):
            df_full = reader
        else:
            df_full = pd.concat(list(reader), ignore_index=True)  # type: ignore
        summary = summarize_dataframe(df_full)
        if sample_rows:
            accum_df = df_full.sample(n=min(sample_rows, len(df_full)), random_state=42)
        df_for_stats = df_full

    # sample сохранить при запросе
    if accum_df is not None and sample_rows:
        (out_dir / "sample.csv").write_text(accum_df.to_csv(index=False), encoding="utf-8")

    # столбцовая статистика
    cols = column_stats(df_for_stats)
    pd.DataFrame([asdict(c) for c in cols]).to_csv(out_dir / "columns.csv", index=False)

    # гистограммы best-effort
    try:
        save_histograms(df_for_stats.select_dtypes("number"), out_dir)
    except Exception as e:
        logger.warning("Failed to plot histograms: %s", e)

    summary_out = {
        "input": str(in_path),
        "rows": summary["rows"],
        "columns": summary["columns"],
        "column_names": summary["column_names"],
        "delimiter": delimiter,
        "engine": eng,
    }
    with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary_out, f, ensure_ascii=False, indent=2)

    logger.info("Done. Rows: %s, Cols: %s", summary_out["rows"], summary_out["columns"])
    return summary_out
