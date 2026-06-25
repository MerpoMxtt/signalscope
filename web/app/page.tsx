"use client";

import { useState } from "react";
import { predictSpeed, PredictRequest, PredictResponse } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

const TIER_COLORS: Record<string, string> = {
  Poor: "bg-red-500",
  Fair: "bg-yellow-500",
  Good: "bg-blue-500",
  Excellent: "bg-green-500",
};

const DEFAULT_FORM: PredictRequest = {
  avg_u_kbps: 10000,
  avg_lat_ms: 30,
  tests: 5,
  devices: 3,
  lat: 37.77,
  lon: -122.41,
  quadkey: "0231230123",
  tile_x: 5242,
  tile_y: 12662,
};

export default function PredictPage() {
  const [form, setForm] = useState<PredictRequest>(DEFAULT_FORM);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const val = e.target.name === "quadkey" ? e.target.value : parseFloat(e.target.value);
    setForm({ ...form, [e.target.name]: val });
  }

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    try {
      const data = await predictSpeed(form);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-background p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">SignalScope</h1>
      <p className="text-muted-foreground mb-8">
        Mobile network performance predictor
      </p>

      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Network Parameters</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-4">
          {[
            { name: "avg_u_kbps", label: "Upload Speed (kbps)" },
            { name: "avg_lat_ms", label: "Latency (ms)" },
            { name: "tests", label: "Test Count" },
            { name: "devices", label: "Device Count" },
            { name: "lat", label: "Latitude" },
            { name: "lon", label: "Longitude" },
            { name: "quadkey", label: "Quadkey" },
            { name: "tile_x", label: "Tile X" },
            { name: "tile_y", label: "Tile Y" },
          ].map(({ name, label }) => (
            <div key={name} className="flex flex-col gap-1">
              <Label htmlFor={name}>{label}</Label>
              <Input
                id={name}
                name={name}
                type={name === "quadkey" ? "text" : "number"}
                value={form[name as keyof PredictRequest]}
                onChange={handleChange}
                step="any"
              />
            </div>
          ))}
        </CardContent>
      </Card>

      <Button onClick={handleSubmit} disabled={loading} className="w-full mb-6">
        {loading ? "Predicting..." : "Predict"}
      </Button>

      {error && (
        <p className="text-red-500 text-sm mb-4">Error: {error}</p>
      )}

      {result && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-3">
              Prediction Result
              <span
                className={`inline-block px-3 py-1 rounded-full text-white text-sm font-semibold ${TIER_COLORS[result.speed_tier] ?? "bg-gray-500"}`}
              >
                {result.speed_tier}
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold">
                {(result.predicted_download_kbps / 1000).toFixed(1)}
              </p>
              <p className="text-muted-foreground text-sm">Mbps download</p>
            </div>
            <div>
              <p className="text-2xl font-bold">
                {(result.confidence * 100).toFixed(1)}%
              </p>
              <p className="text-muted-foreground text-sm">Confidence</p>
            </div>
            <div>
              <p className="text-2xl font-bold">
                {result.predicted_download_kbps.toLocaleString()}
              </p>
              <p className="text-muted-foreground text-sm">kbps</p>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="mt-8 text-center">
        <a href="/stats" className="text-muted-foreground text-sm hover:underline">
          View dataset stats →
        </a>
      </div>
    </main>
  );
}