import pyautogui
import time
import random
from typing import Tuple

def jitter_click(x: int, y: int, intensity: int = 2) -> None:
    pyautogui.moveTo(x + random.randint(-intensity, intensity), y + random.randint(-intensity, intensity))
    pyautogui.click()

def safe_sequence(coords: list[Tuple[int, int]], delay: float = 0.5) -> None:
    for x, y in coords:
        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.click()
        time.sleep(delay)

def hold_key_pattern(key: str, interval: float, duration: int) -> None:
    end_time = time.time() + duration
    while time.time() < end_time:
        pyautogui.press(key)
        time.sleep(interval)

def screen_search(image_path: str, confidence: float = 0.8) -> Tuple[int, int]:
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if location:
        return pyautogui.center(location)
    return (-1, -1)

def emergency_stop() -> None:
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1