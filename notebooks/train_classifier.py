import json
from pathlib import Path

import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

# ── Paths ────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent
DATA_PATH = BASE / "data" / "mobile_q4_2024_features.parquet"
MODEL_PATH = BASE / "models" / "classifier.json"
METRICS_PATH = BASE / "outputs" / "classification_metrics.json"

# ── Config ───────────────────────────────────────────────────────────────────
FEATURES = [
    "log_u_kbps",
    "log_lat_ms",
    "log_tests",
    "log_devices",
    "tile_x",
    "tile_y",
]
TARGET = "speed_tier_int"
TIER_LABELS = ["Poor", "Fair", "Good", "Excellent"]
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
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)
print(f"[✓] Train: {len(X_train):,} rows | Test: {len(X_test):,} rows")

# ── Train ────────────────────────────────────────────────────────────────────
print("[→] Training XGBoost classifier ...")
model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    eval_metric="mlogloss",
)
model.fit(X_train, y_train)
print("[✓] Training complete")

# ── Evaluate ─────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
f1_macro = f1_score(y_test, y_pred, average="macro")
f1_per_class = f1_score(y_test, y_pred, average=None).tolist()
cm = confusion_matrix(y_test, y_pred).tolist()

print(f"[✓] Accuracy:       {accuracy:.4f}")
print(f"[✓] F1 (macro):     {f1_macro:.4f}")
print(f"[✓] F1 per class:")
for label, score in zip(TIER_LABELS, f1_per_class):
    print(f"      {label:<12} {score:.4f}")

# ── Save ─────────────────────────────────────────────────────────────────────
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

model.save_model(MODEL_PATH)
print(f"[✓] Model saved → {MODEL_PATH}")

metrics = {
    "accuracy": round(float(accuracy), 4),
    "f1_macro": round(float(f1_macro), 4),
    "f1_per_class": {
        label: round(score, 4)
        for label, score in zip(TIER_LABELS, f1_per_class)
    },
    "confusion_matrix": cm,
}
with open(METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=2)
print(f"[✓] Metrics saved → {METRICS_PATH}")
print("✅ Classification training complete.")