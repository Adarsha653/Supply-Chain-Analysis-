# Supply Chain Analysis

End-to-end supply chain analytics on the **DataCo** dataset — multi-source ingestion (CSV, web scrape, REST APIs), cloud storage, Databricks SQL warehouse, Power BI dashboards, and SAP CRM alerts.

**Authors:** Adarsha, Aditya

---

## Business problem

- ~**180K** order lines (2015–2018), **~55% late delivery rate**
- Find where delays happen, which markets/products underperform, and which customers are at risk

---

## Architecture

```
DataCo CSV ──┬── Flask fake site (HTML + /api/products JSON)
             │
Web scraper ─┼──► MongoDB Atlas ──► Excel + VBA ──► Python merge ──► AWS S3
             │
REST APIs ───┘
                                    │
                                    ▼
                         Databricks (Bronze → Silver → Gold)
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
               Power BI        SAP CRM API      SQL views
```

---

## Tech stack (free tier)

| Layer | Tools |
|-------|-------|
| Ingestion | Python, Flask, BeautifulSoup, requests |
| Database | MongoDB Atlas |
| Spreadsheet | Excel + VBA |
| Cloud storage | AWS S3 |
| Warehouse | Databricks Free Edition |
| BI | Power BI Desktop |
| Alerts | SAP API Hub sandbox |

---

## Quick start

### 1. Install dependencies

```bash
cd Supply-Chain-Analysis-
pip3 install -r requirements.txt
cp .env.example .env   # fill in MONGO_URI and other secrets
```

### 2. Validate CSV

```bash
python3 scripts/validate_local.py
```

### 3. Day 1 — Fake website + scraper + MongoDB Atlas

**Terminal 1 — Flask (HTML + JSON API):**
```bash
python3 step1/flask_app/app.py
```
- Catalog: http://127.0.0.1:5001/ (10% sample, all 53 columns)
- API: http://127.0.0.1:5001/api/products

**Terminal 2 — Scrape → MongoDB:**
```bash
export MONGO_URI="mongodb+srv://USER:PASSWORD@cluster0.xxxxx.mongodb.net/?appName=Cluster0"
python3 step1/scraper/scrape_to_mongo.py
```

Verify in Atlas: `supply_chain.scraped_products` (~18K docs, 10% sample × 53 columns)

### 4. Day 7 — API ingestion

```bash
python3 step2/api_fetch/fetch_enrichment.py
```
→ `supply_chain.api_products` + `supply_chain.api_enrichment`

### 5. Day 2 — Excel + merge pipeline

```bash
python3 scripts/create_new_orders_template.py   # creates NewOrders.xlsx
python3 step3/excel/run_pipeline.py           # merges Excel + MongoDB → exports/
```

### 6. Days 4–6 — Databricks

1. Sign up: [Databricks Free Edition](https://www.databricks.com/learn/free-edition)
2. Import notebooks from `databricks/notebooks/`
3. Run in order: `01_load_bronze` → `02_transform_silver` → `03_build_gold_and_kpis`

### 7. Days 8–9 — Power BI

Connect to Databricks views or import from `exports/`.

---

## 10-day timeline

| Day | Focus |
|-----|-------|
| 1 | Flask + scraper → MongoDB Atlas |
| 2 | Excel + VBA + merge pipeline |
| 3 | AWS S3 upload |
| 4–6 | Databricks Bronze / Silver / Gold + SQL |
| 7 | API fetch + SAP alerts |
| 8–9 | Power BI dashboard |
| 10 | GitHub + portfolio polish |

Full checklist: **[BUILD_PLAN.md](BUILD_PLAN.md)**  
Shareable overview: **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)**

---

## Project structure

```
Supply-Chain-Analysis-/
├── Dataset/                        # DataCoSupplyChainDataset.csv
├── step1/
│   ├── flask_app/app.py            # Fake website + /api/products
│   ├── products.py                 # Shared product loader
│   └── scraper/scrape_to_mongo.py  # HTML scrape → MongoDB
├── step2/api_fetch/
│   └── fetch_enrichment.py         # REST API → MongoDB
├── step3/excel/
│   ├── run_pipeline.py             # Merge + S3 upload
│   ├── RunPipeline.bas             # VBA macro
│   └── NewOrders.xlsx              # (generated)
├── step6/sap_crm_alert.py          # SAP sandbox alerts
├── databricks/notebooks/           # Bronze → Silver → Gold
├── scripts/
│   ├── validate_local.py
│   └── create_new_orders_template.py
├── exports/                        # Local CSV outputs (gitignored)
├── .env.example
├── BUILD_PLAN.md
├── PROJECT_OVERVIEW.md
└── requirements.txt
```

---

## MongoDB Atlas collections

| Collection | Source | Step |
|------------|--------|------|
| `scraped_products` | BeautifulSoup HTML scrape | 1 | ~18K rows, 53 cols (10% sample) |
| `api_products` | Flask `/api/products` | 2b |
| `api_enrichment` | Market region metadata API | 2b |

---

## Databricks gold layer

| Object | Type | Purpose |
|--------|------|---------|
| `orders_raw` | Table | Bronze — raw CSV |
| `orders_clean` | Table | Silver — cleaned |
| `fact_orders` | Table | Gold fact |
| `dim_customers` | Table | Customer dimension |
| `dim_products` | Table | Product dimension |
| `v_executive_summary` | View | Top KPIs |
| `v_late_delivery_by_mode` | View | Shipping performance |
| `v_profit_by_market` | View | Geo + department profit |
| `v_customer_360` | View | CRM customer summary |
| `v_at_risk_customers` | View | High value + high late rate |
| `v_monthly_trends` | View | Time series |

---

## Environment variables

Copy `.env.example` → `.env`. Key vars:

| Variable | Used for |
|----------|----------|
| `MONGO_URI` | Atlas connection string |
| `FLASK_API_URL` | Local JSON API |
| `AWS_BUCKET` | S3 upload target |
| `SAP_API_URL` / `SAP_API_KEY` | CRM alerts |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 5001 in use | Flask already running — open browser only |
| `mongod` hangs on Mac | Use **MongoDB Atlas** (recommended) |
| Atlas won't connect | Add database user + Network Access `0.0.0.0/0` |
| Scraper fails | Start Flask first |
| API fetch fails | Flask must be running on :5001 |

---

## Progress

- [x] Repo structure + docs
- [x] CSV validated (~180K rows)
- [x] Flask site + JSON API
- [x] Scraper script
- [x] API enrichment script
- [x] Merge pipeline + Excel template generator
- [x] Databricks notebooks
- [x] SAP alert stub
- [ ] Scraper confirmed in Atlas
- [ ] Excel VBA button wired
- [ ] S3 upload working
- [ ] Databricks pipeline run
- [ ] Power BI dashboard
