from __future__ import annotations
from pathlib import Path
import sys
import typer
from rich import print as rprint

# --- импорт, чтобы работать и как пакет, и как файл ---
if __package__ in (None, ""):
    # запущено как файл: python src/kcsv/__main__.py ...
    PKG_ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(PKG_ROOT))
    from kcsv.config import Config
    from kcsv.processing import process_csv
else:
    # запущено как пакет: python -m kcsv ...
    from .config import Config
    from .processing import process_csv

app = typer.Typer(add_help_option=True, no_args_is_help=True)

@app.command()
def run(
    path: Path = typer.Argument(..., exists=True, readable=True, help="CSV файл"),
    out: Path = typer.Option("out", "--out", "-o", help="Каталог для результатов"),
    sep: str | None = typer.Option(None, "--sep", help="Разделитель CSV"),
    chunksize: int | None = typer.Option(None, "--chunksize", help="Размер чанка"),
    engine: str = typer.Option("pyarrow", "--engine", help="pyarrow|c|python"),
    sample: int | None = typer.Option(None, "--sample", help="Сэмпл N строк"),
):
    cfg = Config()

    if chunksize is None:
        size = path.stat().st_size
        chunksize = cfg.chunksize if size > 200 * 1024 * 1024 else None

    summary = process_csv(
        in_path=path,
        out_dir=out,
        delimiter=sep or cfg.delimiter,
        chunksize=chunksize,
        engine=engine or cfg.engine,
        sample_rows=sample or cfg.sample_rows,
    )
    rprint("[bold green]Готово![/] Сводка сохранена в", out / "summary.json")
    rprint(summary)

if __name__ == "__main__":
    app()
