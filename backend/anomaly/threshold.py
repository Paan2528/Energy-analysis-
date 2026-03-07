import pandas as pd
from backend.anomaly.base import AnomalyDetector


class ThresholdDetector(AnomalyDetector):
    def __init__(self, ratio: float = 0.6):
        self.ratio = ratio

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        threshold = df["energy"].mean() * self.ratio
        df = df.copy()
        df["is_anomaly"] = df["energy"] < threshold
        return df
