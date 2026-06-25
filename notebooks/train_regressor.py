import json
from pathlib import Path

import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score

# ── Paths ────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent
DATA_PATH = BASE / "data" / "mobile_q4_2024_features.parquet"
MODEL_PATH = BASE / "models" / "regressor.json"
METRICS_PATH = BASE / "outputs" / "regression_metrics.json"

# ── Config ───────────────────────────────────────────────────────────────────
FEATURES = [
    "log_u_kbps",
    "log_lat_ms",
    "log_tests",
    "log_devices",
    "tile_x",
    "tile_y",
]
TARGET = "log_d_kbps"
TEST_SIZE = 0.2
RANDOM_STATE = 42

# ── Load ─────────────────────────────────────────────────────────────────────
print("[→] Loading features ...")
df = pd.read_parquet(DATA_PATH)
print(f"[✓] {len(df):,} rows loaded")

# ── Prepare ──────────────────────────────────────────────────────────────────
df = df[FEATURES + [TARGET]].dropna()
print(f"[✓] {len(df):,} rows after dropping nulls")

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)
print(f"[✓] Train: {len(X_train):,} rows | Test: {len(X_test):,} rows")

# ── Train ────────────────────────────────────────────────────────────────────
print("[→] Training XGBoost regressor ...")
model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=RANDOM_STATE,
    n_jobs=-1,
)
model.fit(X_train, y_train)
print("[✓] Training complete")

# ── Evaluate ─────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
rmse_log = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Convert RMSE back to kbps space for interpretability
rmse_kbps = float(np.expm1(rmse_log))

print(f"[✓] RMSE (log space): {rmse_log:.4f}")
print(f"[✓] RMSE (kbps):      {rmse_kbps:,.0f}")
print(f"[✓] R²:               {r2:.4f}")

# ── Save ─────────────────────────────────────────────────────────────────────
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

model.save_model(MODEL_PATH)
print(f"[✓] Model saved → {MODEL_PATH}")

metrics = {
    "rmse_log": round(float(rmse_log), 4),
    "rmse_kbps": round(rmse_kbps, 0),
    "r2": round(float(r2), 4),
}
with open(METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=2)
print(f"[✓] Metrics saved → {METRICS_PATH}")
print("Regression training complete.")