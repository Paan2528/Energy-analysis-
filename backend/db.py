import sqlite3
from pathlib import Path
from backend.config import settings

DB_PATH = Path(settings.db_path).resolve()


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_energy (
            day TEXT PRIMARY KEY,
            energy REAL NOT NULL,
            is_anomaly INTEGER NOT NULL 
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("✓ Database initialized at:", DB_PATH)
