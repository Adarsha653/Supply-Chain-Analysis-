"""Quick local check before uploading to Databricks."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "Dataset" / "DataCoSupplyChainDataset.csv"


def main() -> None:
    print(f"Reading {CSV_PATH} ...")
    df = pd.read_csv(CSV_PATH, encoding="latin-1", low_memory=False)
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Date range: {df['order date (DateOrders)'].min()} -> {df['order date (DateOrders)'].max()}")
    print(f"Late delivery rate: {df['Late_delivery_risk'].mean():.1%}")
    print(f"Total sales: ${df['Sales'].sum():,.0f}")
    print(f"Total profit: ${df['Order Profit Per Order'].sum():,.0f}")
    print("\nLocal validation OK — ready to upload to Databricks.")


if __name__ == "__main__":
    main()
