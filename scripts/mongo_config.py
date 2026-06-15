"""Build MongoDB URI from .env — handles special characters in passwords."""
import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

PLACEHOLDERS = ("xxxxx", "<db_password>", "<username>", "USER:PASSWORD", "YOUR_PASSWORD")


def get_mongo_uri() -> str:
    """Prefer MONGO_USER + MONGO_PASSWORD + MONGO_HOST; fallback to MONGO_URI."""
    user = os.getenv("MONGO_USER", "").strip()
    password = os.getenv("MONGO_PASSWORD", "").strip()
    host = os.getenv("MONGO_HOST", "").strip()
    app_name = os.getenv("MONGO_APP_NAME", "Cluster0").strip()

    if user and password and host:
        return (
            f"mongodb+srv://{quote_plus(user)}:{quote_plus(password)}"
            f"@{host}/?appName={quote_plus(app_name)}"
        )

    uri = os.getenv("MONGO_URI", "").strip().strip('"').strip("'")
    if not uri:
        raise ValueError(
            "MongoDB credentials missing. Set either:\n"
            "  MONGO_USER, MONGO_PASSWORD, MONGO_HOST\n"
            "or:\n"
            "  MONGO_URI"
        )
    if any(p in uri for p in PLACEHOLDERS):
        raise ValueError("MONGO_URI still contains placeholder text — update .env")
    return uri


def mask_uri(uri: str) -> str:
    """Show URI with password hidden (for safe debugging)."""
    if "@" not in uri:
        return uri
    prefix, rest = uri.split("://", 1)
    if "@" in rest:
        creds, hostpart = rest.rsplit("@", 1)
        if ":" in creds:
            user = creds.split(":", 1)[0]
            return f"{prefix}://{user}:****@{hostpart}"
    return uri
