import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(BASE_DIR, "data")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

FILE = os.path.join(DATA_DIR, "mobile_q4_2024_features.parquet")

os.makedirs(OUTPUTS_DIR, exist_ok=True)

# ─── Distribution Plot ────────────────────────────────────────────────────────
def plot_distributions(df: pd.DataFrame):
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=[
            "Download Speed (log kbps)",
            "Upload Speed (log kbps)",
            "Latency (log ms)",
        ]
    )

    fig.add_trace(go.Histogram(x=df["log_d_kbps"], nbinsx=60,
                               marker_color="#3B82F6", name="Download"), row=1, col=1)
    fig.add_trace(go.Histogram(x=df["log_u_kbps"], nbinsx=60,
                               marker_color="#10B981", name="Upload"), row=1, col=2)
    fig.add_trace(go.Histogram(x=df["log_lat_ms"], nbinsx=60,
                               marker_color="#F59E0B", name="Latency"), row=1, col=3)

    fig.update_layout(
        title_text="SignalScope — Feature Distributions (log transformed)",
        showlegend=False,
        height=400,
        template="plotly_white",
    )

    out = os.path.join(OUTPUTS_DIR, "distributions.html")
    fig.write_html(out)
    print(f"[✓] Saved distributions → {out}")


# ─── Geographic Heatmap ───────────────────────────────────────────────────────
def plot_heatmap(df: pd.DataFrame):
    sample = df.sample(50_000, random_state=42)
    sample["mbps"] = (sample["avg_d_kbps"] / 1000).round(1)

    fig = px.scatter_mapbox(
        sample,
        lat="tile_y",
        lon="tile_x",
        color="mbps",
        color_continuous_scale=[
            [0.0,  "#EF4444"],
            [0.25, "#F59E0B"],
            [0.6,  "#3B82F6"],
            [1.0,  "#10B981"],
        ],
        range_color=[0, 150],
        zoom=1,
        center={"lat": 20, "lon": 0},
        mapbox_style="carto-positron",
        hover_data={"tile_y": False, "tile_x": False, "mbps": True},
        labels={"mbps": "Avg DL (Mbps)"},
        title="Mobile Download Speed — Q4 2024 (Mbps)",
        height=600,
    )

    out = os.path.join(OUTPUTS_DIR, "heatmap.html")
    fig.write_html(out)
    print(f"[✓] Saved heatmap → {out}")


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[→] Loading features ...")
    df = pd.read_parquet(FILE)
    print(f"[✓] {len(df):,} rows loaded\n")

    plot_distributions(df)
    plot_heatmap(df)

    print("\n✅ Visualizations complete. Open outputs/ in your browser.")