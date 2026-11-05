import random
import time
from typing import List, Tuple
import pyautogui


class SafeClickerEngine:
    """Resilient autoclicker engine dealing with edge cases like resolution shifts and failsafes."""

    def __init__(self, retries: int = 3, safety_margin: int = 5):
        self.retries = retries
        self.safety_margin = safety_margin
        pyautogui.FAILSAFE = True

    def sanitize_coordinates(self, x: int, y: int) -> Tuple[int, int]:
        screen_w, screen_h = pyautogui.size()
        clamped_x = max(self.safety_margin, min(x, screen_w - self.safety_margin))
        clamped_y = max(self.safety_margin, min(y, screen_h - self.safety_margin))
        return clamped_x, clamped_y

    def safe_click(
        self, x: int, y: int, button: str = "left", delay: float = 0.05
    ) -> bool:
        for attempt in range(self.retries):
            try:
                cx, cy = self.sanitize_coordinates(x, y)
                pyautogui.moveTo(cx, cy, duration=0.01)
                pyautogui.click(button=button)
                time.sleep(delay + random.uniform(0.001, 0.01))
                return True
            except pyautogui.FailSafeException:
                # Corner trigger fail-safe protection recovery
                time.sleep(0.5)
                screen_w, screen_h = pyautogui.size()
                pyautogui.moveTo(screen_w // 2, screen_h // 2)
                return False
            except Exception as exc:
                if attempt == self.retries - 1:
                    print(f"Failed click execution at ({x}, {y}): {exc}")
                    return False
                time.sleep(0.1 * (attempt + 1))
        return False


def run_click_batch(points: List[Tuple[int, int]], count: int = 10) -> int:
    engine = SafeClickerEngine()
    completed = 0
    for _ in range(count):
        for px, py in points:
            if engine.safe_click(px, py):
                completed += 1
    return completed
