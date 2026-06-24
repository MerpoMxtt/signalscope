import os
import requests

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ─── Download URL ─────────────────────────────────────────────────────────────
URL = "https://ookla-open-data.s3.amazonaws.com/parquet/performance/type=mobile/year=2024/quarter=4/2024-10-01_performance_mobile_tiles.parquet"
FILENAME = "mobile_q4_2024.parquet"
DEST = os.path.join(DATA_DIR, FILENAME)

# ─── Download ─────────────────────────────────────────────────────────────────
def download():
    if os.path.exists(DEST):
        print(f"[✓] Already downloaded: {FILENAME}")
        return

    print(f"[→] Downloading {FILENAME} ...")
    response = requests.get(URL, stream=True)
    response.raise_for_status()

    total = int(response.headers.get("content-length", 0))
    downloaded = 0

    with open(DEST, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
            downloaded += len(chunk)
            pct = (downloaded / total * 100) if total else 0
            print(f"\r    {downloaded / 1024 / 1024:.1f} MB / {total / 1024 / 1024:.1f} MB ({pct:.0f}%)", end="")

    print(f"\n[✓] Saved to {DEST}")

    # ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    download()