from typing import Optional, Any

class PyAutoGUIError(Exception):
    """Base exception class for all custom tool errors."""
    def __init__(self, message: str, context: Optional[Any] = None) -> None:
        super().__init__(message)
        self.context = context

class ClickerInterrupt(PyAutoGUIError):
    """Exception raised when user triggers a manual stop."""
    pass

class HardwareAbstractionError(PyAutoGUIError):
    """Exception raised when mouse control fails at OS level."""
    pass

class ConfigurationIntegrityError(PyAutoGUIError):
    """Exception raised for invalid YAML or environment setups."""
    pass

def raise_with_context(exception_type: type[PyAutoGUIError], msg: str, ctx: Any = None) -> None:
    """Helper to cast and raise specific error types with debug data."""
    raise exception_type(msg, context=ctx)

# The spirit of the code: Fail loudly, fail clearly, fail with style.