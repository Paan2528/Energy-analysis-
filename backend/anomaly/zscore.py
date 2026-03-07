import pandas as pd
from backend.anomaly.base import AnomalyDetector


class ZScoreDetector(AnomalyDetector):
    def __init__(self, z: float = 2.0):
        self.z = z

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        mean = df["enmergy"].mean()
        std = df["energy"].std()
        zscore = (df["energy"] - mean) / std
        df["is_anomaly"] = zscore.abs() > self.z
        return df
