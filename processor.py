import time
from typing import List, Tuple, Optional


class TargetBoundsError(Exception):
    """Raised when coordinates remain out of bounds after adjustment."""


class SafeClickProcessor:
    def __init__(self, max_retries: int = 3, safety_padding: int = 10):
        self.max_retries = max_retries
        self.safety_padding = safety_padding

    def _get_screen_dimensions(self) -> Tuple[int, int]:
        try:
            import pyautogui
            return pyautogui.size()
        except Exception:
            return (1920, 1080)

    def clamp_coords(self, x: int, y: int) -> Tuple[int, int]:
        width, height = self._get_screen_dimensions()
        clamped_x = max(self.safety_padding, min(x, width - self.safety_padding))
        clamped_y = max(self.safety_padding, min(y, height - self.safety_padding))
        return clamped_x, clamped_y

    def execute_click(self, x: int, y: int, clicks: int = 1) -> bool:
        cx, cy = self.clamp_coords(x, y)
        
        for attempt in range(1, self.max_retries + 1):
            try:
                import pyautogui
                pyautogui.moveTo(cx, cy, duration=0.02)
                pyautogui.click(clicks=clicks)
                return True
            except Exception as exc:
                if "FailSafe" in type(exc).__name__:
                    cx = max(cx + 15, self.safety_padding)
                    cy = max(cy + 15, self.safety_padding)
                time.sleep(0.05 * attempt)
        
        return False

    def batch_process(self, points: List[Tuple[int, int]]) -> int:
        completed = 0
        for pt_x, pt_y in points:
            if self.execute_click(pt_x, pt_y):
                completed += 1
        return completed
