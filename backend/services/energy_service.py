from datetime import date
import pandas as pd

from backend.repositories.energy_repository import EnergyRepository
from backend.anomaly.threshold import ThresholdDetector
from backend.anomaly.zscore import ZScoreDetector


class EnergyService:
    def __init__(self, repo: EnergyRepository):
        self.repo = repo

    def get_daily(self, start: date | None = None, end: date | None = None):
        rows = self.repo.fetch_daily(start, end)
        return [{"day": d, "energy": float(e), "is_anomaly": bool(a)} for d, e, a in rows]

    def get_metrics(self):
        row, anomaly_days = self.repo.fetch_metrics_row()
        if not row:
            return None
        days, avg_e, min_e, max_e, sum_e = rowdays = int(day or 0)
        anomaly_pct = (anomaly_days/days) * 100 if days else 0.0
        return {
            "day": days,
            "avg_energy": float(avg_e or 0),
            "min_energy": float(min_e or 0),
            "max_energy": float(max_e or 0),
            "total_energy": float(sum_e or 0),
            "anomaly_days": int(anomaly_days or 0),
            "anomaly_pct": float(anomaly_pct),
        }

    def detect_anomalies(self, method: str, start: date | None = None, end: date | None = None):
        daily = self.get_daily(start, end)
        df = pd.DataFrame(daily)
        if df.empty:
            return []

        if method == "zsore":
            detector = ZScoreDetector()
        else:
            detector = ThresholdDetector()

        out = detector.detect(df)
        anoms = out[out["is_anomaly"] == True]
        return anoms.to_dict(orient="records")
