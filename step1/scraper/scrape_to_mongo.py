"""Scrape the fake catalog and insert rows into MongoDB Atlas (Step 1 + 2).

Uses FLASK_API_URL when set (recommended for Render); otherwise scrapes HTML table.

Requires:
  - Live catalog (local Flask or Render URL)
  - MongoDB Atlas credentials in .env

Example:
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
FLASK_API_URL = os.getenv("FLASK_API_URL", "")
DB_NAME = os.getenv("MONGO_DB", "supply_chain")
COLLECTION = os.getenv("MONGO_COLLECTION", "scraped_products")
REQUEST_TIMEOUT = int(os.getenv("SCRAPE_TIMEOUT", "300"))


def _stamp_rows(rows: list[dict], source: str) -> list[dict]:
    stamped = []
    now = datetime.now(timezone.utc).isoformat()
    for row in rows:
        doc = dict(row)
        doc["scraped_at"] = now
        doc["source_url"] = source
        stamped.append(doc)
    return stamped


def fetch_from_api(api_url: str) -> list[dict]:
    print(f"Fetching JSON from {api_url} (timeout={REQUEST_TIMEOUT}s)...")
    response = requests.get(api_url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    products = payload.get("products", [])
    if not products:
        raise RuntimeError("API returned no products")
    return _stamp_rows(products, api_url)


def scrape_catalog(url: str) -> list[dict]:
    print(f"Scraping HTML from {url} (timeout={REQUEST_TIMEOUT}s)...")
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
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
        rows.append(row)
    return _stamp_rows(rows, url)


def fetch_products() -> list[dict]:
    if FLASK_API_URL:
        return fetch_from_api(FLASK_API_URL)
    return scrape_catalog(CATALOG_URL)


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
    rows = fetch_products()
    count = save_to_mongo(rows)
    source = FLASK_API_URL or CATALOG_URL
    print(f"Scraped {count} rows from {source}")
    print(f"Inserted into {DB_NAME}.{COLLECTION}")


if __name__ == "__main__":
    main()
