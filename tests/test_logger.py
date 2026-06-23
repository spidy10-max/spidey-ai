"""
Test script for the Spidey AI logging subsystem.
"""
import os
from spidey.logger import get_logger, LOG_FILE


def test_logger_creates_log_file():
    """Ensure the logger writes to the expected log file."""
    logger = get_logger("tests.logger")
    logger.info("Logger test entry")

    assert os.path.exists(LOG_FILE)
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        contents = f.read()

    assert "Logger test entry" in contents


def test_logger_levels_and_handlers():
    """Verify the logger exposes both console and file handlers."""
    logger = get_logger("tests.logger.handlers")

    console_handlers = [h for h in logger.handlers if h.__class__.__name__ == "StreamHandler"]
    file_handlers = [h for h in logger.handlers if h.__class__.__name__ == "FileHandler"]

    assert len(console_handlers) >= 1
    assert len(file_handlers) >= 1


if __name__ == "__main__":
    test_logger_creates_log_file()
    test_logger_levels_and_handlers()
    print("🎉 Logger tests completed!")
