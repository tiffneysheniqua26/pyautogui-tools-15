import time
from typing import Tuple, Optional, Callable
import pyautogui

class SafeClickEngine:
    def __init__(self, fail_safe: bool = True, boundary_padding: int = 5):
        pyautogui.FAILSAFE = fail_safe
        self.padding = boundary_padding
        self._screen_size = pyautogui.size()

    def _is_within_bounds(self, x: int, y: int) -> bool:
        w, h = self._screen_size
        return self.padding <= x <= (w - self.padding) and self.padding <= y <= (h - self.padding)

    def safe_click(self, x: Optional[int] = None, y: Optional[int] = None, clicks: int = 1, interval: float = 0.1) -> bool:
        try:
            target_x, target_y = pyautogui.position() if x is None or y is None else (x, y)
            
            if not self._is_within_bounds(target_x, target_y):
                w, h = pyautogui.size()
                target_x = max(self.padding, min(w - self.padding, target_x))
                target_y = max(self.padding, min(h - self.padding, target_y))

            safe_interval = max(0.01, float(interval))
            safe_clicks = max(1, int(clicks))

            for _ in range(safe_clicks):
                pyautogui.click(x=target_x, y=target_y)
                time.sleep(safe_interval)
            return True

        except pyautogui.FailSafeException:
            return False
        except (ValueError, TypeError, pyautogui.PyAutoGUIException):
            return False

    def execute_burst(self, coords_list: list[Tuple[int, int]], on_failure: Optional[Callable] = None) -> int:
        successful = 0
        for x, y in coords_list:
            if not self.safe_click(x, y):
                if on_failure:
                    on_failure(x, y)
                break
            successful += 1
        return successful
