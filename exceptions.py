import sys
import logging
from functools import wraps

class PyAutoGUIError(Exception):
    pass

class ClickerConfigurationError(PyAutoGUIError):
    pass

class CoordinateOutOfBoundsError(PyAutoGUIError):
    pass

def robust_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError) as e:
            logging.error(f"Invalid operation parameter: {e}")
            raise ClickerConfigurationError("Check your click coordinates")
        except Exception as e:
            logging.critical(f"Uncaught critical failure: {e}")
            sys.exit(1)
    return wrapper

def validate_screen_bounds(x, y, screen_size):
    w, h = screen_size
    if not (0 <= x <= w and 0 <= y <= h):
        raise CoordinateOutOfBoundsError(f"Point ({x}, {y}) exceeds screen {screen_size}")
    return True