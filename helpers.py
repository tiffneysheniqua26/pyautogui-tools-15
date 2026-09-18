import random
import time
from contextlib import contextmanager
import pyautogui

def jitter_coordinate(coord: tuple, offset: int = 3) -> tuple:
    """Applies a random normal-like distribution offset to a coordinate."""
    x, y = coord
    dx = int(random.gauss(0, offset / 2))
    dy = int(random.gauss(0, offset / 2))
    return (x + dx, y + dy)

def human_delay_generator(base_delay: float, variance: float = 0.15):
    """Generates variable delay intervals to simulate human click pauses."""
    while True:
        actual_delay = max(0.01, random.normalvariate(base_delay, variance))
        yield actual_delay

@contextmanager
def temporary_settings(pause: float = None, failsafe: bool = None):
    """Context manager to temporarily modify PyAutoGUI global safety configurations."""
    original_pause = pyautogui.PAUSE
    original_failsafe = pyautogui.FAILSAFE
    try:
        if pause is not None:
            pyautogui.PAUSE = pause
        if failsafe is not None:
            pyautogui.FAILSAFE = failsafe
        yield
    finally:
        pyautogui.PAUSE = original_pause
        pyautogui.FAILSAFE = original_failsafe

def click_sequence_generator(coords: list, loop: bool = False):
    """Yields target coordinates sequentially, optionally looping infinitely."""
    while True:
        for coord in coords:
            yield coord
        if not loop:
            break
