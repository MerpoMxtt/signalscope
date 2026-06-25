import numpy as np
import pandas as pd
import xgboost as xgb
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

TIER_LABELS = {
    0: "Poor",
    1: "Fair",
    2: "Good",
    3: "Excellent",
}

FEATURE_COLUMNS = [
    "log_lat_ms",
    "log_tests",
    "log_devices",
    "tile_x",
    "tile_y",
]


class Predictor:
    def __init__(self):
        self.regressor = xgb.XGBRegressor()
        self.regressor.load_model(MODELS_DIR / "regressor.json")

        self.classifier = xgb.XGBClassifier()
        self.classifier.load_model(MODELS_DIR / "classifier.json")

    def predict(self, avg_lat_ms: float, avg_u_kbps: float, tests: int,
                devices: int, tile_x: int, tile_y: int) -> dict:

        features = pd.DataFrame([{
            "log_u_kbps":  np.log1p(avg_u_kbps),
            "log_lat_ms":  np.log1p(avg_lat_ms),
            "log_tests":   np.log1p(tests),
            "log_devices": np.log1p(devices),
            "tile_x":      tile_x,
            "tile_y":      tile_y,
        }])

        # Regressor predicts log_d_kbps — reverse transform to get kbps
        log_pred = self.regressor.predict(features)[0]
        predicted_kbps = float(np.expm1(log_pred))

        # Classifier predicts tier int + probability of top class
        tier_int = int(self.classifier.predict(features)[0])
        proba = self.classifier.predict_proba(features)[0]
        confidence = float(proba[tier_int])

        return {
            "predicted_download_kbps": round(predicted_kbps, 2),
            "speed_tier": TIER_LABELS[tier_int],
            "speed_tier_int": tier_int,
            "confidence": round(confidence, 4),
        }


# Singleton — instantiated once at import time
predictor = Predictor()