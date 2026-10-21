import logging
import sys
from typing import Optional

class ClickerLogger:
    """Custom logger facade for pyautogui-tools-15 operations."""

    def __init__(self, name: str = "autoclicker") -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s | %(message)s", 
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, message: str, level: str = "info") -> None:
        """Dynamic dispatch logging to standard output."""
        method = getattr(self.logger, level.lower(), self.logger.info)
        method(message)

    def critical_fail(self, reason: str) -> None:
        """Abrupt termination helper for catastrophic events."""
        self.logger.critical(f"CRASH_EVENT: {reason}")
        sys.exit(1)

logger: ClickerLogger = ClickerLogger()