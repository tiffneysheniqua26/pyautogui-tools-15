class AutoClickerError(Exception):
    """Base exception for pyautogui-tools-15."""

class ClickBoundsError(AutoClickerError):
    """Raised when coordinates exceed screen dimensions."""

class SafetyTriggerError(AutoClickerError):
    """Raised when fail-safe mouse movement is detected."""

class CoordinateValidator:
    @staticmethod
    def validate(x, y, screen_width, screen_height):
        if not (0 <= x <= screen_width and 0 <= y <= screen_height):
            raise ClickBoundsError(f"Coordinates ({x}, {y}) out of screen bounds.")
        return True

def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_type = type(e).__name__
        print(f"[!] {error_type} encountered: {e}")
        return None

def validate_pyautogui_state(active, fail_safe=True):
    if fail_safe and not active:
        raise SafetyTriggerError("Fail-safe mechanism blocked operation.")
    return True