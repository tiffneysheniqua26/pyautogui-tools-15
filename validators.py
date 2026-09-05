import pyautogui
import time
from typing import Tuple, Optional

def get_safe_screen_bounds() -> Tuple[int, int]:
    return pyautogui.size()

def validate_coordinates(x: int, y: int) -> bool:
    width, height = get_safe_screen_bounds()
    return 0 <= x < width and 0 <= y < height

def is_failsafe_active() -> bool:
    return pyautogui.FAILSAFE

def smart_click(x: int, y: int, interval: float = 0.1) -> bool:
    if validate_coordinates(x, y):
        pyautogui.click(x, y)
        time.sleep(interval)
        return True
    return False

def capture_mouse_sequence(duration: int = 5) -> list:
    sequence = []
    start_time = time.time()
    while time.time() - start_time < duration:
        sequence.append(pyautogui.position())
        time.sleep(0.5)
    return sequence

def enforce_boundary_sanity(x: int, y: int) -> Tuple[int, int]:
    width, height = get_safe_screen_bounds()
    return (max(0, min(x, width - 1)), max(0, min(y, height - 1)))

def verify_environment_readiness() -> bool:
    try:
        pyautogui.position()
        return True
    except Exception:
        return False