"""
Spidey AI - Logger Utility
Logs likhne ke liye helper
"""

import logging
from datetime import datetime


def get_logger(name: str = "spidey"):
    """
    Logger banata hai jo terminal aur file dono mein logs likhe
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Agar pehle se handlers hain to dobara add na karein
    if not logger.handlers:
        # Terminal pe log dikhane ke liye
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


# Default logger
spidey_logger = get_logger()