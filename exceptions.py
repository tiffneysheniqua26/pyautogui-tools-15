class AutoClickerError(Exception):
    """Base exception for pyautogui-tools-15 errors."""

class CoordinateOutOfBoundsError(AutoClickerError):
    """Raised when click target is outside screen boundaries."""
    def __init__(self, x, y):
        super().__init__(f"Coordinates ({x}, {y}) are outside the active workspace.")

class ProcessInterruptedError(AutoClickerError):
    """Raised when user manually halts the click stream."""
    def __init__(self, message="Execution sequence aborted by user keyboard interrupt."):
        super().__init__(message)

class ConfigValidationError(AutoClickerError):
    """Raised when provided configuration values fail integrity checks."""
    def __init__(self, param, value):
        super().__init__(f"Invalid configuration parameter '{param}': {value} is out of bounds.")

class ExecutionTimeoutError(AutoClickerError):
    """Raised when a specific automation sequence hangs too long."""
    def __init__(self, duration):
        super().__init__(f"Sequence exceeded safety threshold of {duration} seconds.")

class SafeExit(Exception):
    """Graceful stop signal that is not caught by general error handlers."""
    pass