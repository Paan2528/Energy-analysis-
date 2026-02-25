from fastapi import FastAPI, Query, HTTPException
from datetime import date
import logging

from backend.db import get_connection
from backend.schemas import DailyEnergy, Metrics, Health
from backend.config import settings

logging.basicConfig(level=getattr(logging, settings.log_level, logging.INFO))
logger = logging.getLogger("solar-api")

app = FastAPI(title="Solar Energy API", version="4.0")


@app.get("/health", response_model=Health)
def health():
    return {"status": "ok"}


@app.get("/energy/daily", response_model=list[DailyEnergy])
def energy_daily(
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT day, energy, is_anomaly FROM daily_energy"
    params = []

    if start and end and start > end:
        conn.close()
        raise HTTPException(status_code=400, detail="start must be <= end")

    if start and end:
        sql += " WHERE day BETWEEN ? AND ?"
        params = [str(start), str(end)]
    elif start:
        sql += " WHERE day >= ?"
        params = [str(start)]
    elif end:
        sql += " WHERE day <= ?"
        params = [str(end)]

    sql += " ORDER BY day"

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    return [{"day": d, "energy": float(e), "is_anomaly": bool(a)} for d, e, a in rows]


@app.get("/energy/metrics", response_model=Metrics)
def energy_metrics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*), AVG(energy), MIN(energy), MAX(energy), SUM(energy) FROM daily_energy")
    row = cur.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="No energy data found")

    days, avg_e, min_e, max_e, sum_e = row

    cur.execute("SELECT COUNT(*) FROM daily_energy WHERE ia_anomaly =1")
    anomaly_row = cur.fetchone()
    anomaly_days = anomaly_row[0] if anomaly_row else 0

    conn.close()

    days = int(days or 0)
    return {
        "day": days,
        "avg_energy": float(avg_e or 0),
        "min_energy": float(min_e or 0),
        "max_energy": float(max_e or 0),
        "total_energy": float(sum_e or 0),
        "anomaly_days": anomaly_days,
        "anomaly_pct": (anomaly_days / days * 100) if days > 0 else 0.0
    }


@app.get("/")
def root():
    return {"message": "Welcome to the Solar Energy API"}
