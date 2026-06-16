"""Export a smaller CSV for free web hosting (GitHub / Render limits)."""
import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Dataset" / "DataCoSupplyChainDataset.csv"
OUT = ROOT / "Dataset" / "DataCoSupplyChainDataset_web.csv"
FRAC = float(os.getenv("SAMPLE_FRAC", "0.10"))
SEED = int(os.getenv("SAMPLE_SEED", "42"))


def main() -> None:
    df = pd.read_csv(SRC, encoding="latin-1", low_memory=False)
    n = max(1, int(len(df) * FRAC))
    sample = df.sample(n=n, random_state=SEED)
    sample.to_csv(OUT, index=False, encoding="latin-1")
    mb = OUT.stat().st_size / (1024 * 1024)
    print(f"Wrote {OUT}")
    print(f"  Rows: {len(sample):,} | Columns: {len(sample.columns)} | Size: {mb:.1f} MB")


if __name__ == "__main__":
    main()
