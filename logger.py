import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = "pyautogui-tools-15", log_file: str = "app.log") -> logging.Logger:
    """
    A somewhat dramatic, rotating logger instance
    that keeps track of our autoclicker's shenanigans.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] (%(name)s) -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 5MB rotation policy to prevent disk flooding
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Instantiate the singleton instance for global module access
automation_logger = setup_logger()