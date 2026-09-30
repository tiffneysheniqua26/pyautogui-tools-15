import pyautogui
import time
import random
from typing import Tuple, Optional

def jitter_click(x: int, y: int, intensity: int = 2) -> None:
    """Performs a click with human-like spatial jitter."""
    offset_x = random.randint(-intensity, intensity)
    offset_y = random.randint(-intensity, intensity)
    pyautogui.click(x + offset_x, y + offset_y)

def safe_sequence(coords: list[Tuple[int, int]], interval: float = 0.5) -> None:
    """Executes a sequential clicking pattern with randomization."""
    for x, y in coords:
        jitter_click(x, y)
        time.sleep(interval + random.uniform(0, 0.2))

def drag_to_target(start: Tuple[int, int], end: Tuple[int, int], duration: float = 0.3) -> None:
    """Handles dragging actions using tweening for realism."""
    pyautogui.moveTo(start[0], start[1])
    pyautogui.dragTo(end[0], end[1], duration=duration, tween=pyautogui.easeInOutQuad)

def locate_and_act(image_path: str, confidence: float = 0.9) -> bool:
    """Locates image on screen and clicks center if found."""
    target = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    if target:
        pyautogui.click(target)
        return True
    return False

def rapid_burst(x: int, y: int, count: int = 5, gap: float = 0.05) -> None:
    """Performs a high-frequency clicking burst."""
    for _ in range(count):
        pyautogui.click(x, y)
        time.sleep(gap)