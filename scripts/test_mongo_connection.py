"""Test MongoDB Atlas connection — safe debug (password never printed)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pymongo import MongoClient

from scripts.mongo_config import get_mongo_uri, mask_uri


def main() -> None:
    try:
        uri = get_mongo_uri()
    except ValueError as e:
        print(f"Config error: {e}")
        sys.exit(1)

    print("Using URI:", mask_uri(uri))

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=15000)
        result = client.admin.command("ping")
        print("Ping:", result)
        print("MongoDB connection OK")
    except Exception as e:
        print("Connection FAILED:", type(e).__name__, str(e))
        print("\nFix checklist:")
        print("  1. Atlas → Database Access → user exists, password correct")
        print("  2. Atlas → Network Access → 0.0.0.0/0 allowed")
        print("  3. If password has @ # ! % — use split vars in .env:")
        print("       MONGO_USER=supply_chain_user")
        print("       MONGO_PASSWORD=your_password_here")
        print("       MONGO_HOST=cluster0.8m00iht.mongodb.net")
        print("  4. No quotes around values in .env")
        sys.exit(1)


if __name__ == "__main__":
    main()
