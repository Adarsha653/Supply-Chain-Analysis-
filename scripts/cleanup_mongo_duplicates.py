"""Remove duplicate scraped rows from MongoDB Atlas (one-time cleanup)."""
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "supply_chain")
COLLECTION = os.getenv("MONGO_COLLECTION", "scraped_products")


def main() -> None:
    client = MongoClient(MONGO_URI)
    coll = client[DB_NAME][COLLECTION]

    before = coll.count_documents({})
    print(f"Before: {before} documents")

    # Keep one doc per Order Item Id (newest scraped_at wins)
    seen: set[str] = set()
    dup_ids = []
    for doc in coll.find().sort("scraped_at", -1):
        key = doc.get("Order Item Id", doc.get("_id"))
        key = str(key)
        if key in seen:
            dup_ids.append(doc["_id"])
        else:
            seen.add(key)

    if dup_ids:
        result = coll.delete_many({"_id": {"$in": dup_ids}})
        print(f"Removed {result.deleted_count} duplicates")
    else:
        print("No duplicates found by Order Item Id")

    after = coll.count_documents({})
    print(f"After: {after} documents")


if __name__ == "__main__":
    main()
