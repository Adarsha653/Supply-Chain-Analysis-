"""Fake product catalog — HTML table + JSON API with all columns (Step 1)."""
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template_string

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from products import CSV_PATH, column_names, load_dataframe, load_products, warm_cache  # noqa: E402

PORT = int(os.getenv("FLASK_PORT", "5001"))
SAMPLE_FRAC = float(os.getenv("SAMPLE_FRAC", "0.10"))
DISPLAY_MAX_ROWS = int(os.getenv("DISPLAY_MAX_ROWS", "200"))

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>DataCo Supply Catalog</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 1rem; }
    h1 { color: #1a365d; }
    .meta { color: #4a5568; margin-bottom: 1rem; }
    .table-wrap { overflow: auto; max-height: 80vh; border: 1px solid #e2e8f0; }
    table { border-collapse: collapse; min-width: 100%; font-size: 12px; }
    th, td { border: 1px solid #ccc; padding: 6px 8px; text-align: left; white-space: nowrap; }
    th { background: #edf2f7; position: sticky; top: 0; z-index: 1; }
    tr:nth-child(even) { background: #f7fafc; }
  </style>
</head>
<body>
  <h1>DataCo Live Product Feed</h1>
  <p class="meta">
    Showing {{ rows|length }} of {{ total_rows }} rows &times; {{ columns|length }} columns
    ({{ (sample_frac * 100)|int }}% sample) —
    full dataset: <a href="/api/products">/api/products</a>
  </p>
  <div class="table-wrap">
    <table id="products">
      <thead>
        <tr>
          {% for col in columns %}
          <th>{{ col }}</th>
          {% endfor %}
        </tr>
      </thead>
      <tbody>
        {% for r in rows %}
        <tr>
          {% for col in columns %}
          <td>{{ r[col] }}</td>
          {% endfor %}
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</body>
</html>
"""


@app.route("/")
def catalog():
    df = load_dataframe()
    all_rows = df.to_dict(orient="records")
    display_rows = all_rows[:DISPLAY_MAX_ROWS]
    return render_template_string(
        HTML,
        rows=display_rows,
        total_rows=len(all_rows),
        columns=column_names(),
        sample_frac=SAMPLE_FRAC,
    )


@app.route("/api/products")
def api_products():
    rows = load_products()
    return jsonify(
        {
            "count": len(rows),
            "columns": column_names(),
            "sample_frac": SAMPLE_FRAC,
            "products": rows,
        }
    )


@app.route("/health")
def health():
    df = load_dataframe()
    return jsonify(
        {
            "status": "ok",
            "port": PORT,
            "rows": len(df),
            "columns": len(column_names()),
            "sample_frac": SAMPLE_FRAC,
            "csv_file": CSV_PATH.name,
            "display_max_rows": DISPLAY_MAX_ROWS,
        }
    )


warm_cache()

if __name__ == "__main__":
    df = load_dataframe()
    print(f"Loaded {len(df):,} rows x {len(column_names())} columns ({SAMPLE_FRAC:.0%} sample)")
    print(f"HTML catalog: http://127.0.0.1:{PORT}/")
    print(f"JSON API:     http://127.0.0.1:{PORT}/api/products")
    app.run(host="127.0.0.1", port=PORT, debug=True)
