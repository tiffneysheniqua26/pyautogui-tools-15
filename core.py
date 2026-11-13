import pyautogui
import time
import random
from typing import Tuple

def jitter_click(x: int, y: int, intensity: int = 2) -> None:
    """Simulates human-like clicking by adding slight positional noise."""
    offset_x = random.randint(-intensity, intensity)
    offset_y = random.randint(-intensity, intensity)
    pyautogui.click(x + offset_x, y + offset_y)

def smart_drag(start: Tuple[int, int], end: Tuple[int, int], duration: float = 0.5) -> None:
    """Bezier-curved drag simulation to bypass basic anti-bot heuristics."""
    pyautogui.moveTo(*start)
    pyautogui.mouseDown()
    pyautogui.moveTo(*end, duration=duration, tween=pyautogui.easeInOutQuad)
    pyautogui.mouseUp()

def rapid_burst(x: int, y: int, count: int = 5, interval: float = 0.05) -> None:
    """Rapid execution of clicks for high-frequency input requirements."""
    for _ in range(count):
        pyautogui.click(x, y)
        time.sleep(interval)

def screen_center() -> Tuple[int, int]:
    """Resolution-aware coordinate calculation for screen center."""
    width, height = pyautogui.size()
    return (width // 2, height // 2)

def safe_zone_click(x: int, y: int, limit: Tuple[int, int, int, int]) -> bool:
    """Boundary-aware click validation logic for safe automation."""
    left, top, right, bottom = limit
    if left <= x <= right and top <= y <= bottom:
        pyautogui.click(x, y)
        return True
    return False