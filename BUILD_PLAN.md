# Bottom-Up Build Plan (Shareable Checklist)

DataCo supply chain project — fake website → MongoDB → Excel VBA → AWS S3 → Databricks → SAP CRM → Power BI.

> **2026 note:** Databricks **Community Edition is retired**. Use **[Databricks Free Edition](https://www.databricks.com/learn/free-edition)** instead.

---

## Architecture

```
[Step 1] Flask fake site + BeautifulSoup scraper
            ↓
[Step 2] MongoDB (local)
            ↓
[Step 3] Excel + VBA macro button → triggers Python
            ↓
[Step 4] AWS S3 (cloud landing zone)
            ↓
[Step 5] Databricks + SQL (Bronze → Silver → Gold)
            ↓
[Step 6] SAP CRM sandbox alerts (HTTP POST)
            ↓
[Step 7] Power BI DirectQuery dashboard
```

---

## Step 1 — Fake website & scraper (Day 1–2)

**Goal:** Practice scraping safely on localhost.

1. `pip install -r requirements.txt`
2. Start fake site: `python3 step1/flask_app/app.py`
3. Open http://127.0.0.1:5000 — you should see a product table from DataCo
4. In a second terminal: `python3 step1/scraper/scrape_to_mongo.py` (after MongoDB is running, Step 2)

**Files:** `step1/flask_app/app.py`, `step1/scraper/scrape_to_mongo.py`

---

## Step 2 — MongoDB local (Day 2)

**Goal:** Store scraped rows before cloud upload.

1. Install [MongoDB Community Edition](https://www.mongodb.com/try/download/community)
2. Start MongoDB (`brew services start mongodb-community` on Mac)
3. Re-run scraper — rows land in `supply_chain.scraped_products`
4. Verify: `mongosh` → `use supply_chain` → `db.scraped_products.countDocuments()`

---

## Step 3 — Excel + VBA remote control (Day 3–4)

**Goal:** Warehouse manager clicks a button → pipeline runs.

1. Create `step3/excel/NewOrders.xlsx` with sheet **New Orders** (subset of DataCo columns)
2. `Alt + F11` → Insert Module → paste macro from `step3/excel/RunPipeline.bas`
3. Draw button → assign macro `RunSupplyChainPipeline`
4. Macro saves workbook and runs: `python3 step3/excel/run_pipeline.py`

---

## Step 4 — AWS S3 (Day 4–5)

**Goal:** Move merged files off your laptop.

1. Create AWS free account
2. Create S3 bucket (e.g. `supply-chain-dataco-yourname`)
3. Create IAM user with `s3:PutObject` on that bucket
4. Set env vars: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_BUCKET`, `AWS_REGION`
5. Click Excel button → merged CSV appears in `s3://your-bucket/incoming/`

---

## Step 5 — Databricks + SQL (Day 5–8)

**Goal:** Cloud warehouse + window-function analytics.

1. Sign up for **Databricks Free Edition**
2. Import notebooks from `databricks/notebooks/`
3. Configure S3 access (instance profile or access keys in cluster/notebook secrets)
4. Read from S3 → Delta tables: `orders_raw` → `orders_clean` → `fact_orders`
5. Run SQL views with window functions:
   - `AVG(days_shipping_actual) OVER (PARTITION BY market)`
   - `DENSE_RANK() OVER (ORDER BY late_rate DESC)` for worst regions
6. Export alert view for Step 6

---

## Step 6 — SAP CRM alerts (Day 8–9)

**Goal:** Auto-create urgent tasks for bad orders.

1. Register at [SAP API Business Hub](https://api.sap.com/) (sandbox key)
2. Find Sales/Service Cloud sandbox API
3. Export `v_at_risk` / fraud rows from Databricks to `exports/v_alerts.csv`
4. Run: `python3 step6/sap_crm_alert.py`
5. Schedule via cron or Databricks job for repeat runs

**Note:** Sandbox creates simulated tickets — not production CRM.

---

## Step 7 — Power BI command center (Day 9–12)

**Goal:** Executive live dashboard.

1. Install Power BI Desktop (free)
2. Get Data → Databricks connector → DirectQuery
3. Pages: Executive KPIs, Geo map (lat/long), Shipping delays, CRM at-risk table
4. Publish optional — requires Pro license; Desktop-only is free

---

## Free-tier summary

| Tool | Cost |
|------|------|
| Flask, BeautifulSoup, Python | Free |
| MongoDB Community | Free |
| Excel + VBA | Free (if you have Excel) |
| AWS S3 | Free tier (12 mo, limits apply) |
| Databricks Free Edition | Free (daily quotas) |
| SAP API Hub sandbox | Free (simulated) |
| Power BI Desktop | Free |

---

## Suggested day-by-day

| Day | Focus |
|-----|-------|
| 1 | Step 1 — Flask site + scraper |
| 2 | Step 2 — MongoDB |
| 3–4 | Step 3 — Excel + VBA |
| 5 | Step 4 — S3 upload |
| 6–8 | Step 5 — Databricks |
| 9 | Step 6 — SAP alerts |
| 10–12 | Step 7 — Power BI |
