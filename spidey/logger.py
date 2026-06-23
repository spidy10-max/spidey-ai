"""
Spidey AI — Logging System
Logs everything: errors, chats, events, debug info
"""
import logging
import os
from datetime import datetime
from spidey.config import LOGS_DIR, DEBUG, APP_NAME


def setup_logger(name=APP_NAME, log_level=None):
    """Create and configure a logger"""
    os.makedirs(LOGS_DIR, exist_ok=True)

    if log_level is None:
        log_level = logging.DEBUG if DEBUG else logging.INFO

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOGS_DIR, f"spidey_{today}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING if not DEBUG else logging.DEBUG)
    console_format = logging.Formatter(fmt="%(levelname)-8s | %(message)s")
    console_handler.setFormatter(console_format)

    error_file = os.path.join(LOGS_DIR, f"errors_{today}.log")
    error_handler = logging.FileHandler(error_file, encoding="utf-8", mode="a")
    error_handler.setLevel(logging.ERROR)
    error_format = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    error_handler.setFormatter(error_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)

    return logger


def setup_chat_logger():
    """Create logger for chat messages"""
    os.makedirs(LOGS_DIR, exist_ok=True)

    logger = logging.getLogger("spidey.chat")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    today = datetime.now().strftime("%Y-%m-%d")
    chat_file = os.path.join(LOGS_DIR, f"chats_{today}.log")

    handler = logging.FileHandler(chat_file, encoding="utf-8", mode="a")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


# Pre-configured loggers
app_logger = setup_logger("spidey.app")
brain_logger = setup_logger("spidey.brain")
chat_logger = setup_chat_logger()
provider_logger = setup_logger("spidey.provider")


def log_chat(role, message, provider=None):
    """Log a chat message"""
    if role == "user":
        chat_logger.info(f"USER: {message}")
    elif role == "assistant":
        provider_info = f" [{provider}]" if provider else ""
        chat_logger.info(f"SPIDEY{provider_info}: {message}")


def log_event(event, details=None):
    """Log an app event"""
    if details:
        app_logger.info(f"{event} — {details}")
    else:
        app_logger.info(event)


def log_error(error, context=None):
    """Log an error"""
    if context:
        app_logger.error(f"{context} — {error}")
    else:
        app_logger.error(str(error))


def log_provider_switch(old_provider, new_provider):
    """Log provider switch"""
    provider_logger.info(f"Provider switched: {old_provider} → {new_provider}")


def log_startup(provider, settings_dict):
    """Log app startup"""
    app_logger.info("=" * 50)
    app_logger.info("SPIDEY AI STARTED")
    app_logger.info(f"Provider: {provider}")
    app_logger.info(f"Temperature: {settings_dict.get('temperature', 'N/A')}")
    app_logger.info(f"Max Tokens: {settings_dict.get('max_tokens', 'N/A')}")
    app_logger.info("=" * 50)


def log_shutdown(message_count):
    """Log app shutdown"""
    app_logger.info(f"SPIDEY AI STOPPED — {message_count} messages")
    app_logger.info("=" * 50)
