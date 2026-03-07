from pydantic import BaseModel
from datetime import date


class DailyEnergy(BaseModel):
    day: date
    energy: float
    is_anomaly: bool


class Metrics(BaseModel):
    day: int
    avg_energy: float
    min_energy: float
    max_energy: float
    total_energy: float
    anomaly_days: int
    anomaly_pct: float


class Health(BaseModel):
    status: str
