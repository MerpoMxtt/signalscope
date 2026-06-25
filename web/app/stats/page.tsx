"use client";

import { useEffect, useState } from "react";
import { fetchStats, StatsResponse } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const TIER_COLORS: Record<string, string> = {
  Poor: "bg-red-500",
  Fair: "bg-yellow-500",
  Good: "bg-blue-500",
  Excellent: "bg-green-500",
};

export default function StatsPage() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStats()
      .then(setStats)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <main className="min-h-screen bg-background p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Dataset Stats</h1>
      <p className="text-muted-foreground mb-8">
        Q4 2024 Ookla mobile network dataset summary
      </p>

      {error && <p className="text-red-500 text-sm mb-4">Error: {error}</p>}

      {!stats && !error && (
        <p className="text-muted-foreground">Loading...</p>
      )}

      {stats && (
        <>
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Tier Distribution</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {Object.entries(stats.tier_distribution).map(([tier, count]) => {
                const pct = ((count / stats.total_tiles) * 100).toFixed(1);
                return (
                  <div key={tier}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="font-medium">{tier}</span>
                      <span className="text-muted-foreground">
                        {pct}% ({count.toLocaleString()} tiles)
                      </span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${TIER_COLORS[tier] ?? "bg-gray-500"}`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Download Speed Summary</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold">
                  {(stats.median_download_kbps / 1000).toFixed(1)}
                </p>
                <p className="text-muted-foreground text-sm">Median Mbps</p>
              </div>
              <div>
                <p className="text-2xl font-bold">
                  {(stats.mean_download_kbps / 1000).toFixed(1)}
                </p>
                <p className="text-muted-foreground text-sm">Mean Mbps</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6 text-center">
              <p className="text-4xl font-bold">
                {stats.total_tiles.toLocaleString()}
              </p>
              <p className="text-muted-foreground">total tiles in dataset</p>
            </CardContent>
          </Card>
        </>
      )}

      <div className="mt-8 text-center">
        <a href="/" className="text-muted-foreground text-sm hover:underline">
          ← Back to predictor
        </a>
      </div>
    </main>
  );
}