"""Fake product catalog — HTML table + JSON API (Step 1)."""
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template_string

# Allow import from step1/products.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from products import load_products  # noqa: E402

PORT = int(os.getenv("FLASK_PORT", "5001"))

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
    .api-link { margin-top: 1rem; }
  </style>
</head>
<body>
  <h1>DataCo Live Product Feed</h1>
  <p>Fake storefront for scraper practice — {{ rows|length }} products</p>
  <p class="api-link">JSON API: <a href="/api/products">/api/products</a></p>
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


@app.route("/")
def catalog():
    rows = load_products()
    return render_template_string(HTML, rows=rows)


@app.route("/api/products")
def api_products():
    rows = load_products()
    return jsonify({"count": len(rows), "products": rows})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "port": PORT})


if __name__ == "__main__":
    print(f"HTML catalog: http://127.0.0.1:{PORT}/")
    print(f"JSON API:     http://127.0.0.1:{PORT}/api/products")
    app.run(host="127.0.0.1", port=PORT, debug=True)
