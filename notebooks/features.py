import os
import numpy as np
import pandas as pd

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

FILE_IN  = os.path.join(DATA_DIR, "mobile_q4_2024.parquet")
FILE_OUT = os.path.join(DATA_DIR, "mobile_q4_2024_features.parquet")

# ─── Speed Tier Thresholds (locked — do not change) ──────────────────────────
TIER_BINS   = [0, 5_000, 25_000, 100_000, float("inf")]
TIER_LABELS = ["Poor", "Fair", "Good", "Excellent"]

# ─── Feature Engineering ──────────────────────────────────────────────────────
def engineer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Log transforms
    df["log_d_kbps"] = np.log1p(df["avg_d_kbps"].clip(lower=1))
    df["log_u_kbps"] = np.log1p(df["avg_u_kbps"].clip(lower=1))
    df["log_lat_ms"] = np.log1p(df["avg_lat_ms"].clip(lower=1))

    # Speed tier (classification target)
    df["speed_tier"] = pd.cut(
        df["avg_d_kbps"],
        bins=TIER_BINS,
        labels=TIER_LABELS,
        right=False
    )
    df["speed_tier_int"] = df["speed_tier"].cat.codes

    # Derived features
    df["tests_per_device"] = (df["tests"] / df["devices"].clip(lower=1)).round(2)
    df["dl_ul_ratio"]      = (df["avg_d_kbps"] / df["avg_u_kbps"].clip(lower=1)).round(2)

    return df


def report(df: pd.DataFrame):
    print("=" * 60)
    print("SPEED TIER DISTRIBUTION")
    print("=" * 60)
    counts = df["speed_tier"].value_counts().sort_index()
    pct    = (counts / len(df) * 100).round(1)
    for tier in TIER_LABELS:
        if tier in counts.index:
            bar = "█" * int(pct[tier] / 2)
            print(f"  {tier:<10} {counts[tier]:>8,}  ({pct[tier]:>5.1f}%)  {bar}")

    print("\n" + "=" * 60)
    print("LOG TRANSFORM EFFECT")
    print("=" * 60)
    for raw, log in [("avg_d_kbps", "log_d_kbps"), ("avg_u_kbps", "log_u_kbps"), ("avg_lat_ms", "log_lat_ms")]:
        print(f"  {raw:<15} skew: {df[raw].skew():>6.2f}  →  {log:<15} skew: {df[log].skew():>6.2f}")


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[→] Loading data ...")
    df = pd.read_parquet(FILE_IN)
    print(f"[✓] {len(df):,} rows loaded\n")

    df = engineer(df)
    report(df)

    df.to_parquet(FILE_OUT, index=False)
    print(f"\n[✓] Saved to {FILE_OUT}")
    print(f"    Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")