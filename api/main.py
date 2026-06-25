import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import PredictRequest, PredictResponse, StatsResponse
from predictor import predictor

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "mobile_q4_2024_features.parquet"

app = FastAPI(
    title="SignalScope API",
    description="Mobile network performance prediction API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://signalscope.vercel.app"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

TIER_LABELS = {0: "Poor", 1: "Fair", 2: "Good", 3: "Excellent"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    try:
        result = predictor.predict(
            avg_lat_ms=request.avg_lat_ms,
            avg_u_kbps=request.avg_u_kbps,
            tests=request.tests,
            devices=request.devices,
            tile_x=request.tile_x,
            tile_y=request.tile_y,
        )
        return PredictResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=StatsResponse)
def stats():
    try:
        df = pd.read_parquet(DATA_PATH, columns=["avg_d_kbps", "speed_tier_int"])
        tier_counts = df["speed_tier_int"].value_counts().to_dict()
        tier_distribution = {
            TIER_LABELS[k]: int(v)
            for k, v in sorted(tier_counts.items())
        }
        return StatsResponse(
            total_tiles=len(df),
            tier_distribution=tier_distribution,
            median_download_kbps=round(float(df["avg_d_kbps"].median()), 2),
            mean_download_kbps=round(float(df["avg_d_kbps"].mean()), 2),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))