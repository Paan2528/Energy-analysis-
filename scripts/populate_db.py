from pathlib import Path
import pandas as pd
import sqlite3

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Plant_1_Generation_Data.csv"
DB_PATH = PROJECT_ROOT / "backend" / "energy.db"

print("PROJECT_ROOT:", PROJECT_ROOT)
print("DATA_PATH:", DATA_PATH)
print("DB_PATH:", DB_PATH)
print("EXISTS?:", DATA_PATH.exists())

if not DATA_PATH.exists():
    raise FileNotFoundError(f"CSV not found: {DATA_PATH}")

# --- Load CSV ---
df = pd.read_csv(DATA_PATH)

# ensure columns exist
required = {"DATE_TIME", "DC_POWER"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns in CSV: {missing}")

# --- Convert time + numeric ---
df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])
df["DC_POWER"] = pd.to_numeric(df["DC_POWER"], errors="coerce")
df = df.dropna(subset=["DATE_TIME", "DC_POWER"])

# --- Daily aggregation ---
daily = df.groupby(df["DATE_TIME"].dt.date)["DC_POWER"].sum()

# --- Simple anomaly threshold (ต่ำกว่า 50% ของค่าเฉลี่ย) ---
threshold = daily.mean() * 0.5

# --- Insert into SQLite ---
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# create table if not exists (กันพัง)
cur.execute("""
CREATE TABLE IF NOT EXISTS daily_energy (
    day TEXT PRIMARY KEY,
    energy REAL NOT NULL,
    is_anomaly INTEGER NOT NULL
)
""")

# upsert rows
inserted = 0
for day, energy in daily.items():
    is_anomaly = 1 if energy < threshold else 0
    cur.execute(
        """
        INSERT INTO daily_energy (day, energy, is_anomaly)
        VALUES (?, ?, ?)
        ON CONFLICT(day) DO UPDATE SET
            energy=excluded.energy,
            is_anomaly=excluded.is_anomaly
        """,
        (str(day), float(energy), is_anomaly),
    )
    inserted += 1

conn.commit()
conn.close()

print(f"Inserted/updated {inserted} daily rows into DB")
