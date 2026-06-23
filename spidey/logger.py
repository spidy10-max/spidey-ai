"""
Spidey AI — Logging System
Centralized application logger for diagnostics and debugging.
"""
import logging
import os
from logging import Logger
from spidey.config import LOGS_DIR, APP_NAME, DEBUG

LOG_FILE = os.path.join(LOGS_DIR, "spidey.log")


def _ensure_log_directory():
    os.makedirs(LOGS_DIR, exist_ok=True)


def get_logger(name: str = __name__) -> Logger:
    """Return a configured logger for the application."""
    _ensure_log_directory()

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


app_logger = get_logger("spidey")
