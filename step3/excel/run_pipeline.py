"""
Background script for the Excel VBA button (Step 3 → 4).

Merges:
  - Excel 'New Orders' sheet
  - MongoDB scraped product/market data
Then uploads a clean CSV to AWS S3.

Configure env vars before running:
  EXCEL_PATH, MONGO_URI, AWS_BUCKET, AWS_REGION
"""
import os
from datetime import datetime, timezone
from pathlib import Path

import boto3
import pandas as pd
from pymongo import MongoClient

ROOT = Path(__file__).resolve().parents[2]
EXCEL_PATH = Path(os.getenv("EXCEL_PATH", ROOT / "step3" / "excel" / "NewOrders.xlsx"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "supply_chain")
AWS_BUCKET = os.getenv("AWS_BUCKET", "")
AWS_PREFIX = os.getenv("AWS_PREFIX", "incoming/")


def load_excel_orders() -> pd.DataFrame:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(
            f"Excel file not found: {EXCEL_PATH}. Create NewOrders.xlsx first."
        )
    return pd.read_excel(EXCEL_PATH, sheet_name="New Orders")


def load_mongo_prices() -> pd.DataFrame:
    client = MongoClient(MONGO_URI)
    docs = list(client[MONGO_DB]["scraped_products"].find({}, {"_id": 0}))
    return pd.DataFrame(docs)


def merge_and_clean(orders: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    if prices.empty:
        return orders
    return orders.merge(
        prices,
        left_on="Product Name",
        right_on="Product Name",
        how="left",
        suffixes=("", "_catalog"),
    )


def upload_to_s3(df: pd.DataFrame) -> str:
    if not AWS_BUCKET:
        out = ROOT / "exports" / f"merged_{datetime.now(timezone.utc):%Y%m%d_%H%M%S}.csv"
        out.parent.mkdir(exist_ok=True)
        df.to_csv(out, index=False)
        return f"Local fallback (no bucket set): {out}"

    key = f"{AWS_PREFIX}merged_{datetime.now(timezone.utc):%Y%m%d_%H%M%S}.csv"
    tmp = ROOT / "exports" / "latest_merged.csv"
    tmp.parent.mkdir(exist_ok=True)
    df.to_csv(tmp, index=False)

    boto3.client("s3").upload_file(str(tmp), AWS_BUCKET, key)
    return f"s3://{AWS_BUCKET}/{key}"


def main() -> None:
    orders = load_excel_orders()
    prices = load_mongo_prices()
    merged = merge_and_clean(orders, prices)
    location = upload_to_s3(merged)
    print(f"Pipeline complete → {location}")


if __name__ == "__main__":
    main()
