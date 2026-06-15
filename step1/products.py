"""Shared data loader — all columns, configurable sample (default 10%)."""
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "Dataset" / "DataCoSupplyChainDataset.csv"
SAMPLE_FRAC = float(os.getenv("SAMPLE_FRAC", "0.10"))
RANDOM_SEED = int(os.getenv("SAMPLE_SEED", "42"))


def load_dataframe() -> pd.DataFrame:
    """Load SAMPLE_FRAC of CSV with all columns (reproducible random sample)."""
    df = pd.read_csv(CSV_PATH, encoding="latin-1", low_memory=False)
    if SAMPLE_FRAC >= 1.0:
        return df.fillna("")
    n = max(1, int(len(df) * SAMPLE_FRAC))
    sample = df.sample(n=n, random_state=RANDOM_SEED)
    return sample.fillna("")


def load_products() -> list[dict]:
    """Return list of row dicts with all CSV columns."""
    return load_dataframe().to_dict(orient="records")


def column_names() -> list[str]:
    df = pd.read_csv(CSV_PATH, encoding="latin-1", nrows=0)
    return list(df.columns)
