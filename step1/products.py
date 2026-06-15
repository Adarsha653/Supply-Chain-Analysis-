"""Shared product loader — used by Flask HTML + JSON API."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "Dataset" / "DataCoSupplyChainDataset.csv"
SAMPLE_SIZE = 50


def load_products() -> list[dict]:
    df = pd.read_csv(CSV_PATH, encoding="latin-1", low_memory=False)
    subset = df.drop_duplicates(subset=["Product Name"]).head(SAMPLE_SIZE)
    return [
        {
            "order_item_id": int(row["Order Item Id"]),
            "product_name": str(row["Product Name"]).strip(),
            "department": str(row["Department Name"]).strip(),
            "category": str(row["Category Name"]).strip(),
            "market": str(row["Market"]).strip(),
            "product_price": float(row["Product Price"]),
            "shipping_mode": str(row["Shipping Mode"]).strip(),
            "delivery_status": str(row["Delivery Status"]).strip(),
            "late_risk": int(row["Late_delivery_risk"]),
        }
        for _, row in subset.iterrows()
    ]
