import pyautogui
import time
import random
from typing import Tuple

def get_jitter_coords(x: int, y: int, intensity: int = 2) -> Tuple[int, int]:
    """Calculates coordinates with human-like jitter"""
    return (
        x + random.randint(-intensity, intensity),
        y + random.randint(-intensity, intensity)
    )

def safe_click(x: int, y: int, duration: float = 0.1) -> None:
    """Performs a click with built-in fail-safe delay"""
    pos = get_jitter_coords(x, y)
    pyautogui.moveTo(*pos, duration=duration)
    pyautogui.click()

def batch_click(targets: list, interval: float = 0.5) -> None:
    """Iterates through screen targets with pauses"""
    for target in targets:
        safe_click(*target)
        time.sleep(interval + random.uniform(0, 0.2))

def drag_to_relative(dx: int, dy: int) -> None:
    """Relative mouse dragging for UI interactions"""
    curr_x, curr_y = pyautogui.position()
    pyautogui.dragTo(curr_x + dx, curr_y + dy, duration=0.3, tween=pyautogui.easeInOutQuad)

def pulse_click(x: int, y: int, count: int = 3) -> None:
    """Multi-tap execution for unresponsive elements"""
    for _ in range(count):
        pyautogui.click(x, y)
        time.sleep(0.05)