import sys
from typing import Any, Dict, Optional


class AutoClickerError(Exception):
    """Base exception class for pyautogui-tools click automation errors."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.message = message
        self.context = context or {}
        self.formatted_details = self._build_telemetry()
        super().__init__(self.formatted_details)

    def _build_telemetry(self) -> str:
        frame = sys._getframe(2)
        scope = frame.f_code.co_name if frame else "unknown"
        ctx_str = " | ".join(f"{k}={v}" for k, v in self.context.items())
        return f"[{scope.upper()}] {self.message}" + (
            f" ({ctx_str})" if ctx_str else ""
        )


class TargetNotFoundException(AutoClickerError):
    """Raised when visual target or coordinate cluster cannot be located."""

    def __init__(self, target_name: str, region: Optional[tuple] = None):
        super().__init__(
            f"Failed to locate target '{target_name}'",
            {"target": target_name, "region": region or "fullscreen"},
        )


class CoordinateOutOfBoundsError(AutoClickerError):
    """Raised when click target falls outside display safety bounds."""

    def __init__(self, x: int, y: int, bounds: tuple):
        super().__init__(
            "Click coordinate exceeds safe display viewport",
            {"x": x, "y": y, "max_bounds": bounds},
        )


class SafetyInterruptedException(AutoClickerError):
    """Raised when fail-safe trigger or manual break terminates clicking."""

    def __init__(self, trigger_key: str = "ESC"):
        super().__init__(
            "Autoclick loop aborted by safety trigger",
            {"key": trigger_key, "emergency": True},
        )


def purge_exception_traceback(exc: Exception) -> None:
    """Utility to clean frame references from active exception instances."""
    if hasattr(exc, "__traceback__") and exc.__traceback__:
        tb = exc.__traceback__
        while tb:
            tb.tb_frame.f_locals.clear()
            tb = tb.tb_next
