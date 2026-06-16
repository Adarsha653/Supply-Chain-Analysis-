"""Shared data loader — all columns, configurable sample (default 10%)."""
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

ROOT = Path(__file__).resolve().parents[1]
# Use smaller web export on Render/free hosts if present (see docs/DEPLOY_WEBSITE.md)
_WEB_CSV = ROOT / "Dataset" / "DataCoSupplyChainDataset_web.csv"
CSV_PATH = _WEB_CSV if _WEB_CSV.exists() else ROOT / "Dataset" / "DataCoSupplyChainDataset.csv"
SAMPLE_FRAC = float(os.getenv("SAMPLE_FRAC", "0.10"))
RANDOM_SEED = int(os.getenv("SAMPLE_SEED", "42"))

_df_cache: pd.DataFrame | None = None
_cols_cache: list[str] | None = None


def column_names() -> list[str]:
    global _cols_cache
    if _cols_cache is None:
        df = pd.read_csv(CSV_PATH, encoding="latin-1", nrows=0)
        _cols_cache = list(df.columns)
    return _cols_cache


def load_dataframe() -> pd.DataFrame:
    """Load SAMPLE_FRAC of CSV with all columns (cached after first read)."""
    global _df_cache
    if _df_cache is not None:
        return _df_cache

    df = pd.read_csv(CSV_PATH, encoding="latin-1", low_memory=False)
    if SAMPLE_FRAC >= 1.0:
        _df_cache = df.fillna("")
    else:
        n = max(1, int(len(df) * SAMPLE_FRAC))
        _df_cache = df.sample(n=n, random_state=RANDOM_SEED).fillna("")
    return _df_cache


def load_products() -> list[dict]:
    """Return list of row dicts with all CSV columns."""
    return load_dataframe().to_dict(orient="records")


def warm_cache() -> None:
    """Eager load at startup so Render/gunicorn serves requests immediately."""
    df = load_dataframe()
    cols = column_names()
    mb = CSV_PATH.stat().st_size / (1024 * 1024)
    print(
        f"[products] Ready: {len(df):,} rows x {len(cols)} cols "
        f"from {CSV_PATH.name} ({mb:.1f} MB, sample={SAMPLE_FRAC})",
        flush=True,
    )
