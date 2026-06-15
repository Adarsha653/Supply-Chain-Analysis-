"""
Fetch data via REST APIs and store in MongoDB Atlas (Step 2b).

Sources:
  1. Local Flask JSON API  (/api/products)
  2. Market region metadata (DataCo market enrichment)

Usage:
  export MONGO_URI="mongodb+srv://..."
  python3 step2/api_fetch/fetch_enrichment.py
"""
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

FLASK_API_URL = os.getenv("FLASK_API_URL", "http://127.0.0.1:5001/api/products")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "supply_chain")

# Region metadata for DataCo market values (enrichment layer)
MARKET_METADATA = [
    {"market": "LATAM", "region": "Latin America", "timezone_group": "Americas"},
    {"market": "Europe", "region": "Europe", "timezone_group": "EMEA"},
    {"market": "Pacific Asia", "region": "Asia-Pacific", "timezone_group": "APAC"},
    {"market": "USCA", "region": "North America", "timezone_group": "Americas"},
    {"market": "Africa", "region": "Africa", "timezone_group": "EMEA"},
]


def fetch_flask_products() -> list[dict]:
    response = requests.get(FLASK_API_URL, timeout=10)
    response.raise_for_status()
    payload = response.json()
    products = payload.get("products", [])
    fetched_at = datetime.now(timezone.utc).isoformat()
    for row in products:
        row["source"] = "flask_api"
        row["fetched_at"] = fetched_at
        row["api_url"] = FLASK_API_URL
    return products


def fetch_market_enrichment() -> list[dict]:
    fetched_at = datetime.now(timezone.utc).isoformat()
    return [
        {**row, "source": "market_metadata", "fetched_at": fetched_at}
        for row in MARKET_METADATA
    ]


def save_to_mongo(collection: str, rows: list[dict]) -> int:
    client = MongoClient(MONGO_URI)
    coll = client[DB_NAME][collection]
    if rows:
        coll.delete_many({"source": rows[0].get("source")})
        coll.insert_many(rows)
    return len(rows)


def main() -> None:
    api_products = fetch_flask_products()
    api_count = save_to_mongo("api_products", api_products)
    print(f"API products: {api_count} rows → {DB_NAME}.api_products")

    enrichment = fetch_market_enrichment()
    enrich_count = save_to_mongo("api_enrichment", enrichment)
    print(f"Market enrichment: {enrich_count} rows → {DB_NAME}.api_enrichment")


if __name__ == "__main__":
    main()
