from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("API_PORT", "8002"))
    db_path: str = os.getenv("DB_PATH", "backend/energy.db")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
