class AutoClickerError(Exception):
    """Base exception for the pyautogui-tools-15 suite."""

class CoordinateOutOfBoundsError(AutoClickerError):
    """Raised when click target exceeds screen dimensions."""

class SafetyTriggerViolation(AutoClickerError):
    """Raised when the failsafe mechanism is engaged."""

class ConfigurationError(AutoClickerError):
    """Raised when application settings are invalid or missing."""

class ClickRateLimitExceeded(AutoClickerError):
    """Raised when clicks per second exceed allowed threshold."""

class HandlerInitializationError(AutoClickerError):
    """Raised when input listeners fail to bind."""

def raise_if_out_of_bounds(x, y, screen_w, screen_h):
    if not (0 <= x <= screen_w and 0 <= y <= screen_h):
        raise CoordinateOutOfBoundsError(f"Coordinates ({x}, {y}) outside resolution {screen_w}x{screen_h}")

def validate_click_interval(interval):
    if interval < 0.01:
        raise ClickRateLimitExceeded(f"Interval {interval} is too fast for hardware safety")