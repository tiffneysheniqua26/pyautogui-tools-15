import sys
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


class PulseTelemetryFilter(logging.Filter):
    """Injects auto-incrementing click telemetry into log records."""

    def __init__(self, pulse_icon: str = "⚡"):
        super().__init__()
        self.pulse_icon = pulse_icon
        self._sequence = 0

    def filter(self, record: logging.LogRecord) -> bool:
        self._sequence += 1
        click_id = getattr(record, "click_id", self._sequence)
        record.telemetry = f"{self.pulse_icon} [SEQ:{click_id:08d}]"
        return True


def setup_rotating_logger(
    name: str = "autoclicker",
    log_dir: str = "logs",
    max_bytes: int = 1024 * 1024,
    backup_count: int = 3,
) -> logging.Logger:
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    log_filepath = path / f"{name}.log"

    logger = logging.getLogger(f"pyautogui_tools.{name}")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    file_handler = RotatingFileHandler(
        filename=log_filepath,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )

    fmt = "%(asctime)s | %(telemetry)s | %(levelname)-7s | %(message)s"
    formatter = logging.Formatter(fmt, datefmt="%H:%M:%S")

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    filter_instance = PulseTelemetryFilter()
    logger.addFilter(filter_instance)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_autoclick_action(
    logger: logging.Logger, action: str, x: int, y: int, seq: int | None = None
) -> None:
    extra = {"click_id": seq} if seq is not None else {}
    logger.info(f"Target [{x}, {y}] -> {action.upper()}", extra=extra)
