class AutoClickerError(Exception):
    """Base exception for pyautogui-tools-15."""
    pass

class CoordinateOutOfBoundsError(AutoClickerError):
    """Raised when click targets are outside monitor bounds."""
    def __init__(self, x, y):
        super().__init__(f"Target ({x}, {y}) exceeds screen resolution boundaries.")

class HotkeyRegistrationError(AutoClickerError):
    """Raised when keyboard hooks fail to initialize."""
    def __init__(self, key):
        super().__init__(f"Failed to register global hotkey: {key}.")

class ScriptInterruption(AutoClickerError):
    """Custom signal for user-requested emergency stops."""
    pass

class ExecutionTimeoutError(AutoClickerError):
    """Raised when click sequences exceed permitted time frames."""
    def __init__(self, duration):
        super().__init__(f"Execution exceeded maximum duration of {duration} seconds.")

class ConfigurationError(AutoClickerError):
    """Raised during invalid user settings loading."""
    def __init__(self, field, reason):
        super().__init__(f"Config field '{field}' is invalid: {reason}.")