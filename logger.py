import datetime
import sys
from typing import Any, Optional

class ClickerLogger:
    """Centralized diagnostic stream for pyautogui-tools-15 operations."""

    def __init__(self, debug_mode: bool = False) -> None:
        self.debug_mode: bool = debug_mode

    def log(self, message: str, level: str = "INFO") -> None:
        """Formats and directs message to stdout with timestamping."""
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output: str = f"[{timestamp}] [{level}] {message}"
        print(output, file=sys.stdout)

    def debug(self, message: str) -> None:
        """Conditional debug bridge for verbose internal states."""
        if self.debug_mode:
            self.log(message, level="DEBUG")

    def warn(self, message: str, attachment: Optional[Any] = None) -> None:
        """Non-fatal warning notification helper."""
        content: str = f"{message} | Extra: {attachment}" if attachment else message
        self.log(content, level="WARN")

    @staticmethod
    def panic(message: str) -> None:
        """Abrupt termination utility for critical clicker failures."""
        print(f"!!! CRITICAL: {message} !!!", file=sys.stderr)
        sys.exit(1)