# Supply Chain Analysis

Analytics project on the DataCo supply chain dataset using **Databricks Free Edition**, SQL, Power BI Desktop, and Streamlit.

## Dataset

- **File:** `Dataset/DataCoSupplyChainDataset.csv`
- **Rows:** ~180K order lines (2015–2018)
- **Encoding:** `latin-1` (required)

## Architecture

```
CSV → Databricks (Bronze → Silver → Gold) → KPI views → Power BI / Streamlit / Excel
```

## Quick start (do these in order)

### Step 1 — Local validation (5 min)

```bash
cd Supply-Chain-Analysis-
pip install -r requirements.txt
python scripts/validate_local.py
```

You should see row counts and KPIs printed. If this works, your CSV is ready.

### Step 2 — Create Databricks Free Edition account (10 min)

1. Go to [Databricks Free Edition signup](https://www.databricks.com/learn/free-edition)
2. Sign up and open your workspace
3. Wait for the workspace to finish provisioning

### Step 3 — Import project notebooks (5 min)

1. In Databricks: **Workspace** → right-click → **Import**
2. Import each file from `databricks/notebooks/`:
   - `01_load_bronze.py`
   - `02_transform_silver.py`
   - `03_build_gold_and_kpis.py`
   - `04_stream_simulator.py` (optional)

Or clone this repo and sync with Databricks Repos if you prefer.

### Step 4 — Upload the CSV (5 min)

**Option A — Unity Catalog Volume (recommended)**

1. **Catalog** → `main` → **Create schema** `default` (if needed)
2. **Catalog** → **Volumes** → **Create volume** → name: `supply_chain`
3. Open the volume → **Upload** → select `Dataset/DataCoSupplyChainDataset.csv`
4. Copy the file path (looks like `/Volumes/main/default/supply_chain/DataCoSupplyChainDataset.csv`)
5. Paste that path into `CSV_PATH` at the top of notebook `01_load_bronze`

**Option B — File Upload**

1. **Data** → **Add data** → **Upload file**
2. Note the path (often under `/FileStore/...`)
3. Update `CSV_PATH` in notebook `01_load_bronze`

### Step 5 — Run notebooks in order (30 min)

| Order | Notebook | What it does |
|-------|----------|--------------|
| 1 | `01_load_bronze` | Loads CSV → `main.supply_chain.orders_raw` |
| 2 | `02_transform_silver` | Cleans data → `orders_clean` |
| 3 | `03_build_gold_and_kpis` | Facts, dims, KPI views |
| 4 | `04_stream_simulator` | Optional live-style stream demo |

After step 3, open **SQL** in Databricks and run:

```sql
SELECT * FROM main.supply_chain.v_executive_summary;
SELECT * FROM main.supply_chain.v_late_delivery_by_mode;
SELECT * FROM main.supply_chain.v_at_risk_customers LIMIT 20;
```

### Step 6 — Power BI Desktop (later)

1. Download [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free)
2. **Get Data** → **Databricks** (or export views to CSV and import)
3. Connect to views: `v_executive_summary`, `v_late_delivery_by_mode`, `v_profit_by_market`, `v_customer_360`

### Step 7 — Document insights (later)

Write findings in a short insights doc: late delivery by shipping mode, profit by market, at-risk customers.

## Gold layer objects

| Object | Type | Purpose |
|--------|------|---------|
| `orders_raw` | Table | Bronze — raw CSV |
| `orders_clean` | Table | Silver — cleaned |
| `fact_orders` | Table | Gold — analytics fact |
| `dim_customers` | Table | Customer dimension |
| `dim_products` | Table | Product dimension |
| `v_executive_summary` | View | Top-level KPIs |
| `v_late_delivery_by_mode` | View | Shipping performance |
| `v_profit_by_market` | View | Geo + department profit |
| `v_customer_360` | View | CRM-style customer summary |
| `v_at_risk_customers` | View | High value + high late rate |
| `v_monthly_trends` | View | Time series |

## Tips for Free Edition

- Run full loads **once** — avoid re-running bronze repeatedly
- Use **serverless** compute (default on Free Edition)
- Export key views to CSV before heavy usage days as backup
- Keep notebooks in GitHub so you always have your logic

## Project structure

```
Supply-Chain-Analysis-/
├── Dataset/
├── databricks/notebooks/   # Run these in Databricks
├── scripts/                # Local validation
├── requirements.txt
└── README.md
```
