import pyautogui

class AutoClickerError(Exception):
    """Base exception for the toolkit"""
    pass

class SafetyTriggerViolation(AutoClickerError):
    """Raised when mouse exits the screen bounds"""
    pass

class CoordinateOutOfBounds(AutoClickerError):
    """Raised when target coordinates are invalid"""
    pass

def validate_position(x, y):
    width, height = pyautogui.size()
    if not (0 <= x <= width and 0 <= y <= height):
        raise CoordinateOutOfBounds(f"coords ({x}, {y}) exceed resolution {width}x{height}")

def check_safety_perimeter():
    x, y = pyautogui.position()
    if x <= 0 or y <= 0:
        raise SafetyTriggerViolation("emergency abort triggered by screen edge")

class FaultTolerance:
    @staticmethod
    def execute_with_guard(func, *args, **kwargs):
        try:
            check_safety_perimeter()
            return func(*args, **kwargs)
        except pyautogui.FailSafeException as e:
            raise SafetyTriggerViolation("pyautogui failsafe tripped") from e
        except Exception as e:
            raise AutoClickerError(f"unexpected operation failure: {e}") from e