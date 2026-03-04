from datetime import date
from backend.db.connection import get_connection


class EnergyRepository:
    def fetch_daily(self, start: date | None = None, end: date | None = None):
        conn = get_connection()
        cur = conn.cursor()

        sql = "SELECT day, energy, is_anomaly FROM daily_energy"
        params = []

        if start and end:
            sql += " WHERE day BETWEEN ? AND ?"
            params = [str(start), str(end)]
        elif start:
            sql += " WHERE day >= ?"
            params = [str(start)]
        elif end:
            sql += " WHERE das<= ?"
            params = [str(end)]

        sql += " ORDER BY day"
        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.close()
        return rows

    def fetch_metrics_row(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*), AVG(energy), MIN(energy), MAX(energy), SUM(energy) FROM daily_energy")
        row = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM daily_energy WHERE is_anomaly =1")
        anomaly = cur.fetchone()[0]
        conn.close()
        return row, anomaly
