"""Scrape the fake catalog and insert rows into MongoDB Atlas (Step 1 + 2).

Requires:
  - Flask running: python3 step1/flask_app/app.py
  - MONGO_URI set (Atlas connection string)

Example:
  export MONGO_URI="mongodb+srv://USER:PASSWORD@cluster0.xxxxx.mongodb.net/"
  python3 step1/scraper/scrape_to_mongo.py
"""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pymongo import MongoClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from scripts.mongo_config import get_mongo_uri  # noqa: E402

CATALOG_URL = os.getenv("CATALOG_URL", "http://127.0.0.1:5001/")
DB_NAME = os.getenv("MONGO_DB", "supply_chain")
COLLECTION = os.getenv("MONGO_COLLECTION", "scraped_products")


def scrape_catalog(url: str) -> list[dict]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", id="products")
    if table is None:
        raise RuntimeError("Product table not found — is the Flask app running?")

    headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        row = dict(zip(headers, cells))
        row["scraped_at"] = datetime.now(timezone.utc).isoformat()
        row["source_url"] = url
        rows.append(row)
    return rows


def validate_mongo_uri(uri: str) -> None:
    if not uri.startswith(("mongodb://", "mongodb+srv://")):
        raise ValueError("Mongo URI must start with mongodb:// or mongodb+srv://")


def save_to_mongo(rows: list[dict]) -> int:
    uri = get_mongo_uri()
    validate_mongo_uri(uri)
    client = MongoClient(uri)
    collection = client[DB_NAME][COLLECTION]
    if rows:
        # Replace previous scrape so re-runs don't duplicate rows
        collection.delete_many({})
        collection.insert_many(rows)
    return len(rows)


def main() -> None:
    rows = scrape_catalog(CATALOG_URL)
    count = save_to_mongo(rows)
    print(f"Scraped {count} rows from {CATALOG_URL}")
    print(f"Inserted into {DB_NAME}.{COLLECTION}")


if __name__ == "__main__":
    main()
