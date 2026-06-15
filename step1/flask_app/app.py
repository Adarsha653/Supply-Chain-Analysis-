"""Fake product catalog — local scraping playground (Step 1)."""
import os
from pathlib import Path

import pandas as pd
from flask import Flask, render_template_string

PORT = int(os.getenv("FLASK_PORT", "5001"))

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "Dataset" / "DataCoSupplyChainDataset.csv"
SAMPLE_SIZE = 50

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>DataCo Supply Catalog</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    h1 { color: #1a365d; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background: #edf2f7; }
    tr:nth-child(even) { background: #f7fafc; }
  </style>
</head>
<body>
  <h1>DataCo Live Product Feed</h1>
  <p>Fake storefront for scraper practice — {{ rows|length }} products</p>
  <table id="products">
    <thead>
      <tr>
        <th>Order Item Id</th>
        <th>Product Name</th>
        <th>Department</th>
        <th>Category</th>
        <th>Market</th>
        <th>Product Price</th>
        <th>Shipping Mode</th>
        <th>Delivery Status</th>
        <th>Late Risk</th>
      </tr>
    </thead>
    <tbody>
      {% for r in rows %}
      <tr>
        <td>{{ r.order_item_id }}</td>
        <td>{{ r.product_name }}</td>
        <td>{{ r.department }}</td>
        <td>{{ r.category }}</td>
        <td>{{ r.market }}</td>
        <td>{{ r.product_price }}</td>
        <td>{{ r.shipping_mode }}</td>
        <td>{{ r.delivery_status }}</td>
        <td>{{ r.late_risk }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""


def load_products() -> list[dict]:
    df = pd.read_csv(CSV_PATH, encoding="latin-1", low_memory=False)
    subset = df.drop_duplicates(subset=["Product Name"]).head(SAMPLE_SIZE)
    return [
        {
            "order_item_id": row["Order Item Id"],
            "product_name": row["Product Name"],
            "department": row["Department Name"],
            "category": row["Category Name"],
            "market": row["Market"],
            "product_price": row["Product Price"],
            "shipping_mode": row["Shipping Mode"],
            "delivery_status": row["Delivery Status"],
            "late_risk": row["Late_delivery_risk"],
        }
        for _, row in subset.iterrows()
    ]


@app.route("/")
def catalog():
    return render_template_string(HTML, rows=load_products())


if __name__ == "__main__":
    print(f"Open http://127.0.0.1:{PORT}")
    app.run(host="127.0.0.1", port=PORT, debug=True)
