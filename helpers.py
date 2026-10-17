import pyautogui
import time
import random
from typing import Tuple, Optional

def secure_click(coords: Tuple[int, int], jitter: int = 2) -> None:
    """Adds micro-randomness to coordinate clicking to evade basic detection."""
    x, y = coords
    offset_x = random.randint(-jitter, jitter)
    offset_y = random.randint(-jitter, jitter)
    pyautogui.click(x + offset_x, y + offset_y)

def safe_sleep(base: float, variation: float = 0.2) -> None:
    """Sleep with Gaussian-ish noise to prevent predictable timing patterns."""
    drift = random.uniform(-variation, variation)
    time.sleep(max(0, base + drift))

def locate_and_center(image_path: str, confidence: float = 0.9) -> Optional[Tuple[int, int]]:
    """Attempts to find screen elements and returns center coordinate point."""
    try:
        loc = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if loc:
            return pyautogui.center(loc)
    except pyautogui.ImageNotFoundException:
        pass
    return None

def panic_check(key: str = 'esc') -> None:
    """Emergency halt if specific hotkey is detected in buffer."""
    if pyautogui.is_pressed(key):
        raise KeyboardInterrupt('Emergency shutdown requested by user')

def rapid_burst(coords: Tuple[int, int], count: int, interval: float) -> None:
    """Executes quick sequence of clicks without blocking event loop."""
    for _ in range(count):
        secure_click(coords)
        safe_sleep(interval)