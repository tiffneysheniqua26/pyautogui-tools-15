import logging
import sys
from typing import Any

class ClickerLogger:
    """Custom handler orchestrating application event telemetry."""

    def __init__(self, name: str = "pyautogui-tools-15") -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_action(self, msg: str, level: int = logging.INFO) -> None:
        """Dispatches categorized event messages to stdout."""
        self.logger.log(level, msg)

    def critical_fail(self, context: Any) -> None:
        """Unexpected execution halts with diagnostic dump."""
        self.logger.critical(f"Fatal clicker interruption: {str(context)}")

def get_logger() -> ClickerLogger:
    """Singleton-ish access to global logging state."""
    return ClickerLogger()