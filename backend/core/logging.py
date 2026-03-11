import logging
from backend.core.config import Settings, settings


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, Settings.log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
