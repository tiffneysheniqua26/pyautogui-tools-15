import time
from collections import deque
import pyautogui

class FailSafeTriggered(Exception):
    """Raised when safety monitor detects anomalous or dangerous clicking behavior."""
    pass

class SafetyMonitor:
    def __init__(self, max_clicks_per_second: int = 25, history_size: int = 15):
        self.max_rate = max_clicks_per_second
        self.history = deque(maxlen=history_size)
        try:
            self.screen_width, self.screen_height = pyautogui.size()
        except Exception:
            self.screen_width, self.screen_height = 1920, 1080

    def validate_coordinate(self, x: int, y: int) -> tuple[int, int]:
        """Clamps coordinates to screen boundaries and checks safety corners."""
        corners = [
            (0, 0),
            (0, self.screen_height - 1),
            (self.screen_width - 1, 0),
            (self.screen_width - 1, self.screen_height - 1)
        ]
        
        # Custom deadzone threshold check for rapid escapes
        if any(abs(x - cx) < 5 and abs(y - cy) < 5 for cx, cy in corners):
            raise FailSafeTriggered(f"Cursor entered safety corner zone ({x}, {y}). Aborting process.")

        clamped_x = max(0, min(int(x), self.screen_width - 1))
        clamped_y = max(0, min(int(y), self.screen_height - 1))
        return clamped_x, clamped_y

    def register_click_and_verify(self, x: int, y: int) -> bool:
        """Tracks click timing and spatial distribution to intercept UI lockups."""
        now = time.time()
        cx, cy = self.validate_coordinate(x, y)
        self.history.append((now, (cx, cy)))

        if len(self.history) < self.history.maxlen:
            return True

        elapsed = now - self.history[0][0]
        if elapsed > 0:
            rate = len(self.history) / elapsed
            if rate > self.max_rate:
                unique_positions = {pos for _, pos in self.history}
                if len(unique_positions) <= 2:
                    raise FailSafeTriggered(
                        f"Hyper-velocity localized click loop detected: {rate:.1f} Hz at {unique_positions}"
                    )
        return True