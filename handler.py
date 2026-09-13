import sys
import time
from typing import Callable, Any, Tuple, Optional, Dict
import pyautogui


class ScreenBoundaryError(Exception):
    """Raised when target coordinates fall outside detectable display bounds."""
    pass


class AutoclickFailSafeTriggered(Exception):
    """Raised when pyautogui failsafe is tripped by user intervention."""
    pass


class ResilientActionHandler:
    """Creative dynamic wrapper catching PyAutoGUI edge cases during automation."""

    def __init__(self, fallback_corner: Tuple[int, int] = (10, 10)):
        self.fallback_corner = fallback_corner
        self.error_counts: Dict[str, int] = {}
        pyautogui.FAILSAFE = True

    def clamp_coordinates(self, x: int, y: int) -> Tuple[int, int]:
        """Ensures click coordinates do not trigger off-screen panic edge cases."""
        width, height = pyautogui.size()
        safe_x = max(0, min(x, width - 1))
        safe_y = max(0, min(y, height - 1))
        return safe_x, safe_y

    def execute_safely(self, action_func: Callable[..., Any], *args, **kwargs) -> Optional[Any]:
        """Executes a GUI action with layered recovery for unexpected screen states."""
        action_name = getattr(action_func, '__name__', 'unnamed_action')
        self.error_counts.setdefault(action_name, 0)

        try:
            if len(args) >= 2 and isinstance(args[0], int) and isinstance(args[1], int):
                safe_coords = self.clamp_coordinates(args[0], args[1])
                args = safe_coords + args[2:]
            elif 'x' in kwargs and 'y' in kwargs:
                kwargs['x'], kwargs['y'] = self.clamp_coordinates(kwargs['x'], kwargs['y'])

            return action_func(*args, **kwargs)

        except pyautogui.FailSafeException:
            self.error_counts[action_name] += 1
            time.sleep(0.5)
            pyautogui.moveTo(*self.fallback_corner, duration=0.1)
            raise AutoclickFailSafeTriggered("User panic trigger detected via failsafe corner.")

        except (pyautogui.ImageNotFoundException, OSError) as err:
            self.error_counts[action_name] += 1
            sys.stderr.write(f"Recovering from display interaction error in {action_name}: {err}\n")
            return None

        except Exception as unhandled:
            self.error_counts[action_name] += 1
            sys.stderr.write(f"Unhandled edge case in {action_name}: {type(unhandled).__name__}\n")
            return None

    def wrap_action(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator to automatically wrap autoclicker operations with safety handlers."""
        def wrapper(*args, **kwargs):
            return self.execute_safely(func, *args, **kwargs)
        return wrapper