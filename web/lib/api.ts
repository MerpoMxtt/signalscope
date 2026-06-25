const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface PredictRequest {
  avg_u_kbps: number;
  avg_lat_ms: number;
  tests: number;
  devices: number;
  lat: number;
  lon: number;
  quadkey: string;
  tile_x: number;
  tile_y: number;
}

export interface PredictResponse {
  predicted_download_kbps: number;
  speed_tier: string;
  speed_tier_int: number;
  confidence: number;
}

export interface StatsResponse {
  tier_distribution: Record<string, number>;
  median_download_kbps: number;
  mean_download_kbps: number;
  total_tiles: number;
}

export async function predictSpeed(data: PredictRequest): Promise<PredictResponse> {
  const res = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`Predict failed: ${res.status}`);
  return res.json();
}

export async function fetchStats(): Promise<StatsResponse> {
  const res = await fetch(`${API_URL}/stats`);
  if (!res.ok) throw new Error(`Stats failed: ${res.status}`);
  return res.json();
}