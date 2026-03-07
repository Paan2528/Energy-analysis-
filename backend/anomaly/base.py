from abc import ABC, abstractmethod
import pandas as pd


class AnomalyDetector(ABC):
    @abstractmethod
    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
