"""
Background script for the Excel VBA button (Step 3 → 4).

Merges:
  - Excel 'New Orders' sheet
  - MongoDB scraped_products (web scrape)
  - MongoDB api_enrichment (REST API metadata)
Then uploads a clean CSV to AWS S3 (or exports locally if no bucket).

Env vars:
  MONGO_URI, EXCEL_PATH, AWS_BUCKET, AWS_REGION, AWS_PREFIX
"""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import boto3
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from scripts.mongo_config import get_mongo_uri  # noqa: E402

EXCEL_PATH = Path(os.getenv("EXCEL_PATH", ROOT / "step3" / "excel" / "NewOrders.xlsx"))
MONGO_DB = os.getenv("MONGO_DB", "supply_chain")
AWS_BUCKET = os.getenv("AWS_BUCKET", "")
AWS_PREFIX = os.getenv("AWS_PREFIX", "incoming/")


def load_excel_orders() -> pd.DataFrame:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(
            f"Excel file not found: {EXCEL_PATH}. "
            "Run: python3 scripts/create_new_orders_template.py"
        )
    return pd.read_excel(EXCEL_PATH, sheet_name="New Orders")


def load_mongo_collection(name: str) -> pd.DataFrame:
    client = MongoClient(get_mongo_uri())
    docs = list(client[MONGO_DB][name].find({}, {"_id": 0}))
    return pd.DataFrame(docs)


def merge_and_clean(
    orders: pd.DataFrame,
    scraped: pd.DataFrame,
    enrichment: pd.DataFrame,
) -> pd.DataFrame:
    merged = orders.copy()

    if not scraped.empty and "Product Name" in scraped.columns:
        catalog = scraped.rename(
            columns={"Product Name": "Product Name", "Market": "Market_catalog"}
        )
        if "Product Name" in merged.columns:
            merged = merged.merge(
                catalog,
                on="Product Name",
                how="left",
                suffixes=("", "_scrape"),
            )

    if not enrichment.empty and "market" in enrichment.columns:
        market_col = "Market" if "Market" in merged.columns else None
        if market_col:
            merged = merged.merge(
                enrichment.rename(columns={"market": market_col}),
                on=market_col,
                how="left",
                suffixes=("", "_api"),
            )

    merged["merged_at"] = datetime.now(timezone.utc).isoformat()
    return merged


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
    scraped = load_mongo_collection("scraped_products")
    enrichment = load_mongo_collection("api_enrichment")
    merged = merge_and_clean(orders, scraped, enrichment)
    location = upload_to_s3(merged)
    print(f"Pipeline complete → {location}")
    print(f"Rows: {len(merged):,} | Columns: {len(merged.columns)}")


if __name__ == "__main__":
    main()
