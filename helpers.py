import pyautogui
import time
import random
from typing import Tuple

def jitter_coordinates(x: int, y: int, intensity: int = 2) -> Tuple[int, int]:
    """Adds chaotic noise to coordinates to mimic human behavior."""
    return (x + random.randint(-intensity, intensity), y + random.randint(-intensity, intensity))

def safe_click(x: int, y: int, variation: bool = True) -> None:
    """Performs a click with optional randomization for anti-detection."""
    target_x, target_y = jitter_coordinates(x, y) if variation else (x, y)
    pyautogui.click(target_x, target_y)

def smart_sleep(base_seconds: float, variance: float = 0.2) -> None:
    """Sleeps for a base duration plus randomized jitter."""
    delay = base_seconds + random.uniform(-variance, variance)
    time.sleep(max(0, delay))

def get_screen_center() -> Tuple[int, int]:
    """Calculates visual center of primary monitor."""
    width, height = pyautogui.size()
    return (width // 2, height // 2)

def drag_to_safe(target_x: int, target_y: int, speed: float = 0.5) -> None:
    """Performs a non-linear path drag operation."""
    pyautogui.moveTo(*jitter_coordinates(target_x, target_y), duration=speed, tween=pyautogui.easeInOutQuad)
    pyautogui.click()