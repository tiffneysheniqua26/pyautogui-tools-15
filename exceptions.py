class AutoClickerError(Exception):
    """Base exception for pyautogui-tools-15."""

class CoordinateOutOfBoundsError(AutoClickerError):
    """Raised when click targets fall outside monitor geometry."""

class SafetyTriggerViolation(AutoClickerError):
    """Raised when fail-safe mouse movement is detected."""

class ConfigurationError(AutoClickerError):
    """Raised for malformed user settings or invalid input ranges."""

class HardwareAbstractionError(AutoClickerError):
    """Raised when input injection modules fail to initialize."""

def raise_if_invalid(condition: bool, message: str, exception_type=AutoClickerError):
    if condition:
        raise exception_type(message)

class ExceptionReporter:
    def __init__(self, context: str):
        self.context = context

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[!] Error in {self.context}: {exc_val}")
        return False