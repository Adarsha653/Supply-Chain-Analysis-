# Bottom-Up Build Plan (Shareable Checklist)

DataCo supply chain project — fake website → scrape + APIs → MongoDB Atlas → Excel VBA → AWS S3 → Databricks → SAP CRM → Power BI.

> **2026 notes:**
> - Databricks **Community Edition is retired** → use **[Databricks Free Edition](https://www.databricks.com/learn/free-edition)**
> - Flask runs on **port 5001** (port 5000 is often taken by macOS AirPlay)
> - Use **MongoDB Atlas** (free cloud) if local `mongod` hangs on Apple Silicon

See also: **`PROJECT_OVERVIEW.md`** for the full story to share with friends.

---

## Architecture

```
[Step 1] Flask fake site + BeautifulSoup scraper
            ↓
[Step 2] MongoDB Atlas (cloud)
            ↓
[Step 2b] REST API ingestion (enrichment data)
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

## 10-day timeline

| Day | Focus | Step |
|-----|-------|------|
| **1** | Flask site + scraper → MongoDB Atlas | 1 + 2 |
| **2** | Excel + VBA + local merge | 3 |
| **3** | AWS S3 upload | 4 |
| **4** | Databricks Bronze (raw load) | 5 |
| **5** | Silver + Gold tables | 5 |
| **6** | SQL KPIs + window functions + insights | 5 |
| **7** | REST API ingestion + SAP alerts | 2b + 6 |
| **8** | Power BI — executive page | 7 |
| **9** | Power BI — logistics, geo, customers | 7 |
| **10** | README, GitHub, portfolio polish | — |

---

## Step 1 — Fake website & scraper (Day 1)

**Goal:** Practice scraping safely on localhost.

1. `pip install -r requirements.txt`
2. `pip install "pymongo[srv]"`  ← required for MongoDB Atlas
3. Start fake site: `python3 step1/flask_app/app.py`
4. Open **http://127.0.0.1:5001** — product table from DataCo
5. Set up MongoDB Atlas (Step 2), then run scraper:

```bash
export MONGO_URI="mongodb+srv://USER:PASSWORD@cluster0.xxxxx.mongodb.net/?appName=Cluster0"
python3 step1/scraper/scrape_to_mongo.py
```

**Files:** `step1/flask_app/app.py`, `step1/scraper/scrape_to_mongo.py`

**Done when:** ~18K rows (10% sample) × 53 columns in Atlas → `supply_chain.scraped_products`

---

## Step 2 — MongoDB Atlas (Day 1)

**Goal:** Store scraped rows in the cloud (no local `mongod` required).

1. Sign up: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create free **M0** cluster (e.g. Cluster0)
3. **Database Access** → create user (e.g. `supply_chain_user`)
4. **Network Access** → Allow access from anywhere (`0.0.0.0/0`) for learning
5. **Connect** → Drivers → Python → copy connection string
6. Run scraper with `MONGO_URI` (see Step 1)
7. Verify in Atlas: **Browse Collections** → `supply_chain` → `scraped_products`

**Optional local fallback:** Docker Desktop → `docker run -d --name supply-chain-mongo -p 27017:27017 mongo:7`

---

## Step 2b — REST API ingestion (Day 7)

**Goal:** Fetch supplemental data via APIs and store alongside scraped data.

**Inbound APIs (examples — all free):**

| API | URL | Use |
|-----|-----|-----|
| Our Flask JSON endpoint | `http://127.0.0.1:5001/api/products` | Same catalog as API (vs HTML scrape) |
| REST Countries | `https://restcountries.com/v3.1/all` | Enrich market/country metadata |
| Exchange rates | exchangerate-api.com free tier | Optional currency normalization |

**Tasks:**
1. Flask `/api/products` is live — test: http://127.0.0.1:5001/api/products
2. Run: `python3 step2/api_fetch/fetch_enrichment.py`
3. Verify Atlas collections: `api_products`, `api_enrichment`
4. `run_pipeline.py` already merges enrichment data before S3 upload

**Pattern:**
```python
import requests
data = requests.get(API_URL, timeout=10).json()
# → pandas DataFrame → MongoDB or CSV
```

**Outbound API (Step 6):** SAP CRM sandbox — POST alerts for late/fraud orders.

---

## Step 3 — Excel + VBA remote control (Day 2)

**Goal:** Warehouse manager clicks a button → pipeline runs.

1. Generate Excel template: `python3 scripts/create_new_orders_template.py`
   (or create `step3/excel/NewOrders.xlsx` manually with sheet **New Orders**)
2. `Alt + F11` → Insert Module → paste macro from `step3/excel/RunPipeline.bas`
3. Update `pythonPath` and `scriptPath` in the macro for your machine
4. Draw button → assign macro `RunSupplyChainPipeline`
5. Macro saves workbook and runs: `python3 step3/excel/run_pipeline.py`
6. Confirm merged CSV in `exports/` (before S3 is configured)

---

## Step 4 — AWS S3 (Day 3)

**Goal:** Move merged files off your laptop.

1. Create AWS free account
2. Create S3 bucket (e.g. `supply-chain-dataco-yourname`)
3. Create IAM user with `s3:PutObject` on that bucket
4. Set env vars: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_BUCKET`, `AWS_REGION`
5. Upload full DataCo CSV to S3 once (for Databricks)
6. Click Excel button → merged CSV appears in `s3://your-bucket/incoming/`

---

## Step 5 — Databricks + SQL (Days 4–6)

**Goal:** Cloud warehouse + window-function analytics.

1. Sign up for **Databricks Free Edition**
2. Import notebooks from `databricks/notebooks/`
3. Configure S3 access (secrets or notebook config)
4. Run notebooks in order:
   - `01_load_bronze` → `orders_raw`
   - `02_transform_silver` → `orders_clean`
   - `03_build_gold_and_kpis` → facts, dims, views
5. Advanced SQL (window functions):
   - `AVG(days_shipping_actual) OVER (PARTITION BY market)`
   - `DENSE_RANK() OVER (ORDER BY late_rate DESC)` for worst regions
   - `ROW_NUMBER() OVER (PARTITION BY customer_segment ORDER BY total_revenue DESC)`
6. Write 3 business insights (late rate, shipping modes, at-risk customers)
7. Export alert rows to `exports/v_alerts.csv` for Step 6

---

## Step 6 — SAP CRM alerts (Day 7)

**Goal:** Auto-create urgent tasks for bad orders via API.

1. Register at [SAP API Business Hub](https://api.sap.com/) (sandbox key)
2. Find Sales/Service Cloud sandbox API
3. Export `v_at_risk` / fraud rows from Databricks to `exports/v_alerts.csv`
4. Set env vars: `SAP_API_URL`, `SAP_API_KEY`
5. Run: `python3 step6/sap_crm_alert.py`
6. Optional: schedule via cron or Databricks job

**Note:** Sandbox creates simulated tickets — not production CRM.

---

## Step 7 — Power BI command center (Days 8–9)

**Goal:** Executive live dashboard.

1. Install [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free)
2. Get Data → Databricks connector → DirectQuery (or import CSV exports)
3. Build pages:

| Page | Visuals |
|------|---------|
| Executive | KPI cards: revenue, profit, late %, orders |
| Logistics | Late rate by shipping mode; monthly trend |
| Geography | Map by market (lat/long) |
| Customers | At-risk table; segment breakdown |

4. Add slicers: Market, Department
5. Save `supply_chain.pbix`; export PDF screenshots for portfolio

---

## Step 8 — Portfolio polish (Day 10)

1. Update `README.md` with architecture diagram and how to run
2. Push to GitHub
3. Write 3 resume bullets (emphasize S3, Databricks, SQL, APIs, Power BI)
4. Optional: 3-min Loom walkthrough

---

## Free-tier summary

| Tool | Cost |
|------|------|
| Flask, BeautifulSoup, requests, Python | Free |
| MongoDB Atlas M0 | Free |
| Public REST APIs | Free |
| Excel + VBA | Free (if you have Excel) |
| AWS S3 | Free tier (12 mo, limits apply) |
| Databricks Free Edition | Free (daily quotas) |
| SAP API Hub sandbox | Free (simulated) |
| Power BI Desktop | Free |

---

## Progress checklist

- [ ] Step 1 — Flask site live on :5001
- [ ] Step 2 — Scraper → MongoDB Atlas (`scraped_products`)
- [ ] Step 2b — API fetch scripts → MongoDB (`api_enrichment`)
- [ ] Step 3 — Excel + VBA button works
- [ ] Step 4 — Files landing in S3
- [ ] Step 5 — Databricks Bronze / Silver / Gold + SQL views
- [ ] Step 6 — SAP alert script runs
- [ ] Step 7 — Power BI dashboard (4 pages)
- [ ] Step 8 — GitHub + README + resume bullets

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 5000/5001 in use | Site already running — use browser only, or kill process |
| `mongod` hangs on Mac | Use **MongoDB Atlas** or **Docker** instead |
| Atlas "can't connect" | Create database user + Network Access (`0.0.0.0/0`) |
| `brew services` bootstrap error | Skip — use Atlas or `docker run mongo:7` |
| Password special chars in MONGO_URI | URL-encode or use simpler password |
