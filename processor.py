import pyautogui
import time
import random
from typing import Tuple

def jitter_click(x: int, y: int, intensity: int = 5) -> None:
    target = (x + random.randint(-intensity, intensity), y + random.randint(-intensity, intensity))
    pyautogui.click(target)

def smart_drag(start: Tuple[int, int], end: Tuple[int, int], duration: float = 0.5) -> None:
    pyautogui.moveTo(*start)
    pyautogui.dragTo(*end, duration=duration, button='left')

def safe_sequence(coords: list, interval: float = 0.2) -> None:
    for x, y in coords:
        pyautogui.click(x, y)
        time.sleep(interval + random.uniform(0, 0.1))

def type_string_human(text: str, speed: float = 0.05) -> None:
    for char in text:
        pyautogui.typewrite(char)
        time.sleep(speed + random.uniform(0, speed))

def emergency_abort_check(hotkey: str = 'esc') -> bool:
    if pyautogui.getActiveWindow() is not None:
        return False
    return True

def randomized_wait(min_s: float, max_s: float) -> None:
    time.sleep(random.uniform(min_s, max_s))