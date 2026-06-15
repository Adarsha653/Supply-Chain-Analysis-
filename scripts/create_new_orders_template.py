"""Create step3/excel/NewOrders.xlsx template from DataCo CSV (Day 2)."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "Dataset" / "DataCoSupplyChainDataset.csv"
OUT_PATH = ROOT / "step3" / "excel" / "NewOrders.xlsx"

COLUMNS = [
    "Order Id",
    "Product Name",
    "Market",
    "Department Name",
    "Sales",
    "Order Profit Per Order",
    "Order Status",
    "Late_delivery_risk",
    "Shipping Mode",
    "Delivery Status",
]


def main() -> None:
    df = pd.read_csv(CSV_PATH, encoding="latin-1", usecols=COLUMNS, low_memory=False)
    sample = df.drop_duplicates(subset=["Order Id"]).head(30)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sample.to_excel(OUT_PATH, sheet_name="New Orders", index=False)
    print(f"Created {OUT_PATH} with {len(sample)} rows")


if __name__ == "__main__":
    main()
