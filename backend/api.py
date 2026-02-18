from fastapi import FastAPI
from backend.db import get_connection

app = FastAPI()


@app.get("/energy/daily")
def get_daily_energy():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT day, energy, is_anomaly FROM daily_energy")
    row = cursor.fetchall()
    conn.close()

    return [
        {
            "day": day,
            "energy": energy,
            "is_anomaly": bool(is_anomaly)
        }
        for day, energy, is_anomaly in row
    ]

# API endpoint (metrics + anomalies)


@app.get("/energy/metrics")
def energy_metrics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) AS days, AVG(energy) AS avg_energy, MIN(energy) AS min_energy, MAX(energy) AS max_energy, SUM(energy) AS sum_energy FROM daily_energy")
    days, avg_e, min_e, max_e, sum_e = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM daily_energy WHERE is_anomaly = 1")
    anomaly_days = cur.fetchone()[0]

    conn.close()

    return {
        "day": int(days or 0),
        "avg_energy": float(avg_e or 0),
        "min_energy": float(min_e or 0),
        "max_energy": float(max_e or 0),
        "total_energy": float(sum_e or 0),
        "anomaly_days": int(anomaly_days or 0),
        "anomaly_pct": float((anomaly_days / days * 100) if days else 0.0)
    }


@app.get("/energy/anomalies")
def energy_anomalies():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT day, energy FROM daily_energy WHERE is_anomaly = 1 ORDER BY day")
    rows = cur.fetchall()
    conn.close()

    return [{"day": d, "energy": e} for d, e in rows]
