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
