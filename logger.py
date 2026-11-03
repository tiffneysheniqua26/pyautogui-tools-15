import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class AutoClickFormatter(logging.Formatter):
    """Custom log formatter decorating entries with click-action symbols."""

    SYMBOLS = {
        logging.DEBUG: "⚡",
        logging.INFO: "🎯",
        logging.WARNING: "⚠️",
        logging.ERROR: "💥",
        logging.CRITICAL: "☠️",
    }

    def format(self, record: logging.LogRecord) -> str:
        record.symbol = self.SYMBOLS.get(record.levelno, "•")
        return super().format(record)


def setup_logger(
    log_dir: str = "logs",
    max_bytes: int = 512 * 1024,  # 512 KB per file
    backup_count: int = 5,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures dual-handler rotating logger for automation tracking."""
    target_dir = Path(log_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("pyautogui_tools")
    logger.setLevel(level)
    logger.handlers.clear()

    fmt_pattern = "%(asctime)s [%(symbol)s] [%(filename)s:%(lineno)d] %(message)s"
    time_fmt = "%H:%M:%S"
    formatter = AutoClickFormatter(fmt_pattern, datefmt=time_fmt)

    file_handler = RotatingFileHandler(
        filename=target_dir / "autoclicker.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Rotating log system ready for click automation")
    return logger


main_logger = setup_logger()
