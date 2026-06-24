import os
import pandas as pd

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE = os.path.join(DATA_DIR, "mobile_q4_2024.parquet")

# ─── Load ─────────────────────────────────────────────────────────────────────
def load() -> pd.DataFrame:
    print(f"[→] Loading {FILE} ...")
    df = pd.read_parquet(FILE)
    print(f"[✓] Loaded {len(df):,} rows × {df.shape[1]} columns\n")
    return df

# ─── Explore ──────────────────────────────────────────────────────────────────
def explore(df: pd.DataFrame):
    print("=" * 60)
    print("COLUMNS & TYPES")
    print("=" * 60)
    print(df.dtypes)

    print("\n" + "=" * 60)
    print("FIRST 5 ROWS")
    print("=" * 60)
    print(df.head().to_string())

    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(df.describe().round(1).to_string())

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    print(nulls.to_string() if len(nulls) else "None — clean dataset ✓")

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load()
    explore(df)