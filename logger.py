import sys
import time
from typing import Optional, TextIO

class ClickerLogger:
    """Custom creative logger for pyautogui-tools-15 autoclicker."""
    
    def __init__(self, stream: TextIO = sys.stdout, prefix: str = "[AUTO]") -> None:
        self.stream: TextIO = stream
        self.prefix: str = prefix
        self._enabled: bool = True

    def toggle(self, state: Optional[bool] = None) -> bool:
        """Toggle logging state or set it explicitly."""
        self._enabled = state if state is not None else not self._enabled
        return self._enabled

    def log(self, message: str, level: str = "INFO") -> None:
        """Emit a formatted log message if logging is enabled."""
        if not self._enabled:
            return
        timestamp: str = time.strftime("%H:%M:%S", time.localtime())
        formatted: str = f"{self.prefix} ({timestamp}) {{{level}}}: {message}\n"
        self.stream.write(formatted)
        self.stream.flush()

    def success(self, message: str) -> None:
        """Log a success event with custom flair."""
        self.log(f"✨ SUCCESS -> {message}", level="OK")

    def warning(self, message: str) -> None:
        """Log a warning event."""
        self.log(f"⚠️ WARNING -> {message}", level="WARN")

    def error(self, message: str) -> None:
        """Log a critical error event."""
        self.log(f"❌ CRITICAL -> {message}", level="ERROR")
