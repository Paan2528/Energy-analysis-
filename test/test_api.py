from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics():
    response = client.get("/energy/daily")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_anomaly_threshold():
    response = client.get("/energy/anomalies?method=threshold")
    assert response.status_code == 200


def test_anomaly_zscore():
    response = client.get("/energy/anomalies?method=zscore")
    assert response.status_code == 200
