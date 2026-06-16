# Deploy Flask website for free (live URL)

Your fake catalog can go live on the internet for **$0**. Best option: **[Render](https://render.com)** (free tier).

---

## Important: CSV size (~91 MB)

The full CSV is large for free hosting. Before deploy:

```bash
# Creates ~9 MB file (10% sample) — easier for GitHub + Render
python3 scripts/export_web_csv.py
```

This writes `Dataset/DataCoSupplyChainDataset_web.csv`. The app uses it automatically when present.

On Render, also set env var **`SAMPLE_FRAC=0.01`** (1% ≈ 1,800 rows) so the page loads fast on free tier.

---

## Option 1 — Render (recommended)

### Step 1 — Push code to GitHub

```bash
git add .
git commit -m "Add Render deployment config"
git push origin your-branch
```

Merge to `main` if Render deploys from main.

Include either:
- `Dataset/DataCoSupplyChainDataset_web.csv` (after export script), **or**
- full CSV if your repo allows (~91 MB — GitHub may warn)

### Step 2 — Create Render account

1. Go to [https://render.com](https://render.com) → sign up with GitHub
2. **New +** → **Web Service**
3. Connect repo `Supply-Chain-Analysis-`

### Step 3 — Configure service

| Setting | Value |
|---------|--------|
| **Name** | `supply-chain-catalog` |
| **Runtime** | Python 3 |
| **Build command** | `pip install -r requirements.txt -r requirements-web.txt` |
| **Start command** | `gunicorn step1.flask_app.app:app --bind 0.0.0.0:$PORT --timeout 120` |
| **Plan** | Free |

Or use the included **`render.yaml`** (Blueprint deploy).

### Step 4 — Environment variables (Render dashboard)

| Key | Value |
|-----|--------|
| `SAMPLE_FRAC` | `0.01` (1% for faster live site) |
| `SAMPLE_SEED` | `42` |

### Step 5 — Deploy

Click **Create Web Service**. After ~5–10 min you get a URL like:

```
https://supply-chain-catalog.onrender.com
```

- Catalog: `https://your-app.onrender.com/`
- API: `https://your-app.onrender.com/api/products`

### Step 6 — Update scraper to use live URL

In `.env`:

```env
CATALOG_URL=https://your-app.onrender.com/
FLASK_API_URL=https://your-app.onrender.com/api/products
```

```bash
python3 step1/scraper/scrape_to_mongo.py
```

---

## Render free tier limits

| Limit | What it means |
|-------|----------------|
| Spins down after ~15 min idle | First visit after sleep takes ~30–60 sec |
| 512 MB RAM | Use `SAMPLE_FRAC=0.01`, web CSV export |
| 750 hours/month | Enough for a portfolio project |

---

## Option 2 — PythonAnywhere (simple, manual)

1. [https://www.pythonanywhere.com](https://www.pythonanywhere.com) → free account
2. Upload project files (or `git clone`)
3. Create Flask web app → point WSGI at `step1.flask_app.app`
4. URL: `https://youruser.pythonanywhere.com`

Good for learning; less automatic than Render.

---

## Option 3 — Streamlit Cloud

**Not for this Flask app.** Use Render or PythonAnywhere for Flask.

---

## What changes when live

| Before | After |
|--------|--------|
| `http://127.0.0.1:5001` | `https://your-app.onrender.com` |
| Only you can access | Anyone with URL can view |
| Scraper hits localhost | Scraper hits public URL |

MongoDB Atlas is already cloud — scraper → Atlas works from anywhere once `CATALOG_URL` is updated.

---

## Files added for deployment

```
Procfile              # Render / Heroku-style start
render.yaml           # Render blueprint
requirements-web.txt  # gunicorn (production server)
scripts/export_web_csv.py  # smaller CSV for deploy
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails | Check `requirements.txt` installs on Python 3.11 |
| App crashes on start | Lower `SAMPLE_FRAC`; run `export_web_csv.py` |
| Page timeout | Use 1% sample, not 10% on free tier |
| Cold start slow | Normal on Render free — wait 30–60 sec |
| CSV not found | Commit `DataCoSupplyChainDataset_web.csv` to repo |

---

## Quick checklist

- [ ] Run `python3 scripts/export_web_csv.py`
- [ ] Commit + push to GitHub
- [ ] Create Render web service
- [ ] Set `SAMPLE_FRAC=0.01`
- [ ] Open live URL in browser
- [ ] Update `CATALOG_URL` in `.env`
- [ ] Re-run scraper against live site
