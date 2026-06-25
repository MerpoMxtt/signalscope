from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    avg_lat_ms: float = Field(..., gt=0, description="Average latency in milliseconds")
    avg_u_kbps: float = Field(..., gt=0, description="Average upload speed in kbps")
    tests: int = Field(..., gt=0, description="Number of tests run on this tile")
    devices: int = Field(..., gt=0, description="Number of unique devices on this tile")
    quadkey: str = Field(..., description="Bing Maps quadkey tile identifier")
    tile_x: int = Field(..., description="Tile X coordinate")
    tile_y: int = Field(..., description="Tile Y coordinate")


class PredictResponse(BaseModel):
    predicted_download_kbps: float = Field(..., description="Predicted download speed in kbps")
    speed_tier: str = Field(..., description="Human-readable speed tier label")
    speed_tier_int: int = Field(..., description="Numeric tier (0=Poor, 1=Fair, 2=Good, 3=Excellent)")
    confidence: float = Field(..., description="Classifier confidence for predicted tier (0–1)")


class StatsResponse(BaseModel):
    total_tiles: int
    tier_distribution: dict[str, int]
    median_download_kbps: float
    mean_download_kbps: float