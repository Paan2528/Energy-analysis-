from fastapi.params import Depends
import pandas as pd
from backend.anomaly.threshold import ThresholdDetector
from backend.anomaly.zscore import ZScoreDetector
from backend.api.routes import get_service
from backend.services.energy_service import EnergyService

service: EnergyService = Depends(get_service)


def sample_data():
    return pd.DataFrame({
        "energy": [100, 110, 90, 5000, 105]
    })


def test_threshold_detector():
    df = sample_data()
    detector = ThresholdDetector()
    result = detector.detect(df)

    assert "is_anomaly" in result.columns


def test_zscore_detector():
    df = sample_data()
    detector = ZScoreDetector()
    result = detector.detect(df)

    assert "is_anomaly" in result.columns
