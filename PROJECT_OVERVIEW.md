# Supply Chain Analytics Project — Overview

**Author:** Adarsha  
**Dataset:** DataCo Supply Chain (~180K order lines, 2015–2018)  
**Goal:** Build an end-to-end data pipeline that ingests orders from multiple sources (CSV, web scrape, APIs), stores and transforms them in the cloud, and delivers business insights through dashboards and automated alerts.

---

## The business problem

DataCo has a large order history with signs of operational stress:

- **~55% late delivery rate** across orders
- Different **shipping modes** perform very differently (e.g. First Class vs Standard)
- Revenue and profit vary by **market**, **product department**, and **customer segment**
- Some orders are **high-risk** (late delivery, suspected fraud)

The project turns raw operational data into **actionable answers**: where delays happen, which customers are at risk, and what ops/sales should fix first.

---

## What we are building (one sentence)

A **bottom-up analytics pipeline** that simulates how a real company collects supply chain data from multiple sources, lands it in the cloud, models it with SQL, visualizes it in Power BI, and triggers CRM alerts when something goes wrong.

---

## Architecture (full picture)

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
├─────────────────┬──────────────────┬────────────────────────────┤
│  DataCo CSV     │  Fake website    │  REST APIs (NEW)             │
│  (historical    │  (Flask HTML     │  e.g. exchange rates,        │
│   orders)       │   table)         │  geo/country metadata        │
└────────┬────────┴────────┬─────────┴──────────────┬─────────────┘
         │                 │                        │
         │                 ▼                        ▼
         │          BeautifulSoup scraper     Python requests
         │                 │                        │
         │                 └──────────┬─────────────┘
         │                            ▼
         │                   MongoDB Atlas (cloud)
         │                            │
         ▼                            │
   Excel + VBA button ───────────────┤
   ("New Orders" sheet)             │
         │                            │
         ▼                            ▼
   Python merge script ──────► AWS S3 (cloud landing zone)
                                       │
                                       ▼
                            Databricks Free Edition
                            Bronze → Silver → Gold
                            SQL + window functions
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                  ▼
              Power BI           SAP CRM API         (optional
              dashboard          alert on late/       Streamlit)
              executives         fraud orders
```

---

## The 7 layers (what each part does)

| # | Layer | Tool | What it does |
|---|-------|------|--------------|
| 1 | **Fake website** | Flask (Python) | Serves product rows from the CSV as a local HTML catalog — safe scraping practice |
| 2 | **Web scraper** | BeautifulSoup + requests | Reads the HTML table and extracts structured data |
| 3 | **API ingestion** | Python `requests` | Fetches supplemental data from public REST APIs (rates, geo, etc.) and merges with orders |
| 4 | **Local / staging DB** | MongoDB Atlas | Holds scraped + API-enriched records before cloud upload |
| 5 | **Business trigger** | Excel + VBA | Warehouse manager clicks a button → runs Python pipeline |
| 6 | **Cloud storage** | AWS S3 | Landing zone for merged files off the laptop |
| 7 | **Warehouse + analytics** | Databricks + SQL | Clean, model, and compute KPIs (late delivery, profit, customer 360) |
| 8 | **Automated action** | SAP API (sandbox) | POST alert when late delivery or fraud is detected |
| 9 | **Visualization** | Power BI Desktop | Executive command center — maps, trends, KPI cards |

---

## Where APIs fit in (new addition)

We are **not** only using CSV and scraping. APIs are a first-class ingestion path:

| API use | Example | Why |
|---------|---------|-----|
| **Enrich orders** | REST Countries API | Add region metadata to markets |
| **Enrich pricing** | Exchange rate API | Convert multi-currency sales to USD |
| **Our own API** | Flask `/api/products` JSON endpoint | Same data as the website, but via REST (scraper vs API pattern) |
| **Outbound alert** | SAP CRM sandbox API | Create urgent tasks for bad orders |
| **Future** | Databricks SQL API | Programmatic query access for dashboards |

**Pattern:** `requests.get(url)` → JSON → pandas DataFrame → MongoDB / S3 → Databricks.

This mirrors real data engineering: **batch files + web scrape + REST APIs** all landing in one pipeline.

---

## Data flow (simplified)

1. **Historical orders** live in `DataCoSupplyChainDataset.csv`
2. **Flask** reads a sample and publishes it as a fake storefront
3. **Scraper** pulls that page → **MongoDB Atlas**
4. **API scripts** pull external JSON → **MongoDB Atlas** (same or separate collection)
5. **Excel** holds new manual orders; button runs **Python** to merge everything
6. **Merged file** uploads to **AWS S3**
7. **Databricks** reads S3, builds Bronze/Silver/Gold tables and SQL views
8. **Power BI** connects to Databricks for live dashboards
9. **SAP script** watches for bad orders and fires API alerts

---

## Key metrics we analyze

**Supply chain**
- Late delivery rate by shipping mode, market, department
- Actual vs scheduled shipping days
- Monthly delivery trends

**Commercial**
- Total sales and profit
- Profit margin by category
- Discount impact

**CRM / customer**
- Revenue per customer
- Customer segment performance
- At-risk customers (high value + bad delivery experience)

---

## Tech stack (all free tier)

| Category | Tools |
|----------|-------|
| Language | Python |
| Web | Flask |
| Scraping | BeautifulSoup, requests |
| APIs | REST (requests), SAP API Hub sandbox |
| Database | MongoDB Atlas |
| Spreadsheet | Excel + VBA |
| Cloud storage | AWS S3 |
| Warehouse | Databricks Free Edition |
| BI | Power BI Desktop |
| Version control | GitHub |

---

## 10-day timeline

| Day | Focus |
|-----|-------|
| 1 | Flask fake site + scraper → MongoDB Atlas |
| 2 | Excel + VBA + local merge |
| 3 | AWS S3 upload |
| 4 | Databricks Bronze (raw load) |
| 5 | Silver + Gold tables |
| 6 | SQL KPIs + window functions + insights |
| 7 | API ingestion scripts + SAP alerts |
| 8 | Power BI — executive page |
| 9 | Power BI — logistics, geo, customers |
| 10 | README, GitHub, portfolio polish |

---

## What this project teaches

- **Data analyst skills:** SQL, KPIs, dashboards, business storytelling
- **Data engineer skills:** Ingestion, cloud storage, medallion architecture, orchestration
- **Integration skills:** Scraping, REST APIs, CRM webhooks, multi-source merge
- **Portfolio value:** End-to-end pipeline with a real domain (supply chain) and clear “so what”

---

## Current progress

- [x] Project repo and folder structure
- [x] DataCo CSV validated (~180K rows)
- [x] Flask fake website (localhost:5001)
- [x] Web scraper script
- [x] MongoDB Atlas cluster (Cluster0)
- [ ] Scraper confirmed in Atlas collections
- [ ] API ingestion scripts
- [ ] Excel + VBA
- [ ] AWS S3
- [ ] Databricks pipeline
- [ ] SAP alerts
- [ ] Power BI dashboard

---

## How to explain it to non-technical people

> “We’re building a mini version of how a retail company tracks orders. Data comes in from spreadsheets, a website, and APIs. It gets cleaned in the cloud, we build reports that show where deliveries are late and which customers are unhappy, and the system can automatically alert customer service when something looks wrong.”

---

## Repo structure

```
Supply-Chain-Analysis-/
├── Dataset/                    # Source CSV
├── step1/
│   ├── flask_app/              # Fake website
│   └── scraper/                # HTML → MongoDB
├── step2/                      # (API fetch scripts — coming)
├── step3/excel/                # Excel + VBA + merge pipeline
├── step6/                      # SAP CRM alert script
├── databricks/notebooks/       # Bronze → Silver → Gold
├── scripts/                    # Local validation
├── BUILD_PLAN.md               # Step-by-step checklist
└── PROJECT_OVERVIEW.md         # This file
```

---

*Questions or want to collaborate? Clone the repo and start from `BUILD_PLAN.md` Day 1.*
