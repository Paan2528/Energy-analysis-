from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)


def test_metrics_ok():
    r = client.get("/energy/metrics")
    assert r.status_code in (200, 404)  # 404 if no data yet
    if r.status_code == 200:
        data = r.json()
        assert "day" in data
        assert "avg_energy" in data
