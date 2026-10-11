import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class ClickLogFormatter(logging.Formatter):
    """Custom log formatter with status symbols for click automation events."""

    SYMBOLS = {
        logging.DEBUG: "[DEBUG]",
        logging.INFO: "[CLICK]",
        logging.WARNING: "[WARN] ",
        logging.ERROR: "[FAIL] ",
        logging.CRITICAL: "[CRIT] ",
    }

    def format(self, record: logging.LogRecord) -> str:
        symbol = self.SYMBOLS.get(record.levelno, "[LOG]  ")
        record.symbol = symbol
        return super().format(record)


def setup_autoclick_logger(
    log_dir: str = "logs",
    log_filename: str = "autoclicker.log",
    max_bytes: int = 512 * 1024,
    backup_count: int = 3,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures and returns a rotating logger setup for click actions."""
    target_dir = Path(log_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / log_filename

    logger = logging.getLogger("pyautogui_tools.autoclicker")
    logger.setLevel(level)

    if logger.handlers:
        return logger

    file_handler = RotatingFileHandler(
        file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )

    fmt = "%(asctime)s %(symbol)s - %(message)s"
    date_fmt = "%H:%M:%S"
    formatter = ClickLogFormatter(fmt=fmt, datefmt=date_fmt)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("rotating logger system initialized")
    return logger


def log_click_action(logger: logging.Logger, x: int, y: int, button: str, cps: float) -> None:
    """Helper to record automated coordinate clicks with performance statistics."""
    logger.info(f"Pos: ({x}, {y}) | Key: {button} | Rate: {cps:.1f} CPS")
