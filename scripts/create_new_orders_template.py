"""Create step3/excel/NewOrders.xlsx — all columns, 10% sample (Day 2)."""
import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "Dataset" / "DataCoSupplyChainDataset.csv"
OUT_PATH = ROOT / "step3" / "excel" / "NewOrders.xlsx"
SAMPLE_FRAC = float(os.getenv("SAMPLE_FRAC", "0.10"))
RANDOM_SEED = int(os.getenv("SAMPLE_SEED", "42"))


def main() -> None:
    df = pd.read_csv(CSV_PATH, encoding="latin-1", low_memory=False)
    n = max(1, int(len(df) * SAMPLE_FRAC))
    sample = df.sample(n=n, random_state=RANDOM_SEED)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sample.to_excel(OUT_PATH, sheet_name="New Orders", index=False)
    print(f"Created {OUT_PATH}")
    print(f"  Rows: {len(sample):,} | Columns: {len(sample.columns)} ({SAMPLE_FRAC:.0%} sample)")


if __name__ == "__main__":
    main()
