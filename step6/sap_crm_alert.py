"""
SAP CRM alert stub (Step 6).

Polls Databricks SQL results (or a local CSV export) and POSTs to SAP API Business Hub
sandbox when late delivery or fraud is detected.

Set env vars:
  SAP_API_URL, SAP_API_KEY, DATABRICKS_SQL_ENDPOINT (or ALERTS_CSV path)
"""
import os
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
ALERTS_CSV = Path(os.getenv("ALERTS_CSV", ROOT / "exports" / "v_alerts.csv"))
SAP_API_URL = os.getenv("SAP_API_URL", "")
SAP_API_KEY = os.getenv("SAP_API_KEY", "")


def load_alert_rows() -> pd.DataFrame:
    if not ALERTS_CSV.exists():
        raise FileNotFoundError(
            f"No alert file at {ALERTS_CSV}. Export v_at_risk rows from Databricks first."
        )
    df = pd.read_csv(ALERTS_CSV)
    mask = (df.get("late_delivery_risk", 0) == 1) | (
        df.get("order_status", "").astype(str).str.upper() == "SUSPECTED_FRAUD"
    )
    return df[mask]


def send_sap_alert(row: dict) -> None:
    if not SAP_API_URL or not SAP_API_KEY:
        print(f"[DRY RUN] Would alert SAP for order {row.get('order_id')}")
        return

    headers = {"APIKey": SAP_API_KEY, "Content-Type": "application/json"}
    payload = {
        "subject": f"Urgent: Order {row.get('order_id')} — delivery/fraud flag",
        "description": f"Late risk={row.get('late_delivery_risk')} status={row.get('order_status')}",
        "priority": "High",
    }
    response = requests.post(SAP_API_URL, json=payload, headers=headers, timeout=15)
    response.raise_for_status()


def main() -> None:
    alerts = load_alert_rows()
    print(f"Found {len(alerts)} rows requiring CRM alert")
    for _, row in alerts.iterrows():
        send_sap_alert(row.to_dict())


if __name__ == "__main__":
    main()
