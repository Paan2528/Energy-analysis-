import sqlite3
from pathlib import Path
from backend.core.config import Settings

DB_PATH = Path(Settings().db_path).resolve()


def get_connection():
    return sqlite3.connect(DB_PATH)
