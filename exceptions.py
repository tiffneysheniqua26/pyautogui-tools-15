from typing import Optional

class PyAutoGUIError(Exception):
    """Base exception for the pyautogui-tools-15 suite."""
    pass

class ConfigurationError(PyAutoGUIError):
    """Raised when the autoclicker configuration is invalid."""
    def __init__(self, message: str, config_key: Optional[str] = None) -> None:
        self.config_key = config_key
        super().__init__(f"Invalid config '{config_key}': {message}" if config_key else message)

class ClickerExecutionError(PyAutoGUIError):
    """Raised during unexpected runtime failures of the autoclicker."""
    def __init__(self, code: int, context: str) -> None:
        self.code = code
        self.context = context
        super().__init__(f"Execution failed at {context} (Exit Code: {code})")

class SafetyTriggerViolation(PyAutoGUIError):
    """Raised when the fail-safe mechanism is forcibly invoked."""
    def __init__(self, panic_message: str = "Safety override initiated") -> None:
        self.panic_message = panic_message
        super().__init__(panic_message)

def raise_if_unstable(status: bool) -> None:
    """Checks if the system state is suitable for clicking."""
    if not status:
        raise ClickerExecutionError(500, "system unstable")