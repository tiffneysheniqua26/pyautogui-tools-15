from typing import Optional, Any

class PyAutoGUIError(Exception):
    """Base exception for the pyautogui-tools-15 suite."""
    pass

class ClickerRuntimeError(PyAutoGUIError):
    """Raised when the autoclicker loop enters a forbidden state."""
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        self.context = context or {}
        super().__init__(f"{message} | Context: {self.context}")

class SafetyTriggerViolation(PyAutoGUIError):
    """Raised when mouse position forces an emergency halt."""
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        super().__init__(f"Emergency halt triggered at coordinate ({x}, {y})")

class ConfigurationIntegrityError(PyAutoGUIError):
    """Raised when application settings are corrupted or invalid."""
    def __init__(self, field: str, value: Any) -> None:
        self.field = field
        self.value = value
        super().__init__(f"Invalid configuration detected: {field}={value}")

def raise_if_unsafe(x: int, y: int, boundary: int = 0) -> None:
    """Validates safety bounds for clicker operations."""
    if x <= boundary or y <= boundary:
        raise SafetyTriggerViolation(x, y)