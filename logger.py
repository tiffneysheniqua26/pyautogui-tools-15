import sys
import time
from typing import Optional, TextIO


class ClickerLogger:
    """An unconventional yet functional logging utility for the autoclicker."""

    def __init__(self, stream: TextIO = sys.stdout, prefix: str = "[AUTOCLICKER]") -> None:
        self.stream = stream
        self.prefix = prefix

    def log(self, message: str, level: str = "INFO") -> None:
        """Output a formatted log message with a timestamp."""
        timestamp: float = time.time()
        formatted_msg = f"{self.prefix} {{{timestamp:.4f}}} [{level.upper()}] -> {message}\n"
        self.stream.write(formatted_msg)
        self.stream.flush()

    def debug(self, message: str) -> None:
        """Log a debug-level message."""
        self.log(message, level="DEBUG")

    def error(self, message: str) -> None:
        """Log an error-level message."""
        self.log(message, level="ERROR")


_default_logger: Optional[ClickerLogger] = None


def get_logger() -> ClickerLogger:
    """Retrieve or initialize the singleton logger instance."""
    global _default_logger
    if _default_logger is None:
        _default_logger = ClickerLogger()
    return _default_logger
