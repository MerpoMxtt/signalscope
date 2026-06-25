# SignalScope

**Mobile network performance predictor** — an end-to-end ML system that ingests real-world Ookla speedtest data, trains XGBoost models to predict download throughput and signal quality tier, and surfaces predictions through a FastAPI inference API and interactive Next.js dashboard.

**Live demo:** [signalscope-seven.vercel.app](https://signalscope-seven.vercel.app)

---

## Problem

Mobile network performance varies significantly across geographies, devices, and conditions. Predicting signal quality from measurable network parameters — before a user complains — is the core challenge behind coverage planning, SLA reporting, and user experience forecasting. This project builds a system that does exactly that, using Ookla's Q4 2024 global speedtest dataset.

---

## Architecture

```
Ookla S3 (Parquet)
        │
        ▼
  Feature Engineering
  (log transforms, speed tiers, tile coordinates)
        │
        ▼
  XGBoost Models
  ├── Regressor  →  predicted download kbps
  └── Classifier →  speed tier (Poor / Fair / Good / Excellent)
        │
        ▼
  FastAPI (Render)
  ├── POST /predict
  └── GET  /stats
        │
        ▼
  Next.js Dashboard (Vercel)
  ├── Predict form + result card
  └── Dataset stats page
```

---

## Model Performance

| Model | Target | Metric | Score |
|---|---|---|---|
| XGBoost Regressor | `log_d_kbps` | R² | 0.56 |
| XGBoost Classifier | Speed tier (4-class) | Macro F1 | 0.54 |
| XGBoost Classifier | Speed tier (4-class) | Accuracy | 0.60 |

**Dataset:** 3,551,267 tiles — Q4 2024 Ookla mobile performance data

**Speed tier distribution:**
- Poor (< 5 Mbps): 7.3%
- Fair (5–25 Mbps): 22.7%
- Good (25–100 Mbps): 36.5%
- Excellent (> 100 Mbps): 33.4%

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data | Ookla Open Data, AWS S3, Parquet, pandas |
| ML | XGBoost, scikit-learn, numpy |
| API | FastAPI, uvicorn, Pydantic |
| Frontend | Next.js 16, Tailwind CSS, shadcn/ui |
| Deployment | Render (API), Vercel (frontend) |

---

## Data Contract

The `/predict` endpoint accepts six network parameters and returns a prediction:

**Input:**
```json
{
  "avg_u_kbps": 10000,
  "avg_lat_ms": 30,
  "tests": 5,
  "devices": 3,
  "tile_x": 5242,
  "tile_y": 12662,
  "quadkey": "0231230123"
}
```

**Output:**
```json
{
  "predicted_download_kbps": 33062.18,
  "speed_tier": "Good",
  "speed_tier_int": 2,
  "confidence": 0.5530
}
```

---

## Running Locally

**Prerequisites:** Python 3.11+, Node.js 18+

**1. Clone the repo**
```bash
git clone https://github.com/MerpoMxtt/signalscope.git
cd signalscope
```

**2. Set up the ML environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**3. Run the data pipeline**
```bash
python notebooks/ingest.py
python notebooks/features.py
python notebooks/train_regressor.py
python notebooks/train_classifier.py
```

**4. Start the API**
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

**5. Start the frontend**
```bash
cd web
npm install
# Create .env.local with: NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
# Dashboard at http://localhost:3000
```

---

## Key Findings

- Download speed is heavily right-skewed (median 52.8 Mbps vs mean 115.7 Mbps) — log transformation was essential before training
- Class imbalance across speed tiers (Poor at 7.3% vs Good at 36.5%) is the primary driver of the classifier's macro F1 gap
- Geographic coordinates (tile_x, tile_y) are among the most predictive features, reflecting real-world infrastructure density patterns

---

## Resume Bullet

> Engineered an end-to-end mobile network performance prediction system on Ookla's 3.5M-tile Q4 2024 global speedtest dataset; trained XGBoost regression (R² 0.56) and 4-class classification models (macro F1 0.54); deployed FastAPI inference API on Render and interactive Next.js dashboard on Vercel.

