import sqlite3
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "energy.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_energy (
            day TEXT PRIMARY KEY,
            energy REAL NOT NULL,
            is_anomaly INTEGER NOT NULL 
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("✓ Database initialized at:", DB_PATH)
