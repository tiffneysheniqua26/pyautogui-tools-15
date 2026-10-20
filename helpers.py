import pyautogui
import time
import random
from typing import Tuple

def jitter_click(x: int, y: int, intensity: int = 3) -> None:
    """Simulates human-like jittery mouse movement before clicking."""
    dx = x + random.randint(-intensity, intensity)
    dy = y + random.randint(-intensity, intensity)
    pyautogui.moveTo(dx, dy, duration=random.uniform(0.1, 0.3))
    pyautogui.click()

def safe_zone_check(x: int, y: int, screen_width: int, screen_height: int) -> bool:
    """Checks if coordinate is within safe screen boundaries."""
    return 0 <= x < screen_width and 0 <= y < screen_height

def sequence_click(coords: list[Tuple[int, int]], delay: float = 0.5) -> None:
    """Executes a sequential list of click actions."""
    for x, y in coords:
        pyautogui.click(x, y)
        time.sleep(delay)

def panic_abort() -> None:
    """Hard reset for runaway automation scripts."""
    pyautogui.FAILSAFE = True
    pyautogui.moveTo(0, 0)

def random_wait(min_sec: float = 0.5, max_sec: float = 2.0) -> None:
    """Randomized sleep to bypass static detection patterns."""
    time.sleep(random.uniform(min_sec, max_sec))

def pixel_color_trigger(x: int, y: int, target_rgb: Tuple[int, int, int]) -> bool:
    """Checks if a pixel matches target color before action."""
    return pyautogui.pixelMatchesColor(x, y, target_rgb, tolerance=10)