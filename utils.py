import pyautogui
import logging
from functools import wraps

logger = logging.getLogger('pyautogui-tools-15')

class AutomationError(Exception):
    """Custom exception for automation failures."""
    pass

def safety_guard(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            pyautogui.FAILSAFE = True
            return func(*args, **kwargs)
        except pyautogui.FailSafeException:
            logger.critical("Failsafe triggered by user")
            raise AutomationError("Emergency stop activated")
        except Exception as e:
            logger.error(f"Unexpected automation failure: {e}")
            raise AutomationError(f"Operation failed: {e}")
    return wrapper

@safety_guard
def safe_click(x, y, duration=0.1):
    if not (0 <= x <= pyautogui.size().width and 0 <= y <= pyautogui.size().height):
        raise AutomationError("Coordinates out of screen bounds")
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.click()

def validate_screen_resolution(min_width=800, min_height=600):
    width, height = pyautogui.size()
    if width < min_width or height < min_height:
        raise AutomationError(f"Resolution {width}x{height} too small for operations")
    return True