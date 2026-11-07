import pyautogui
import time
import random
from typing import Tuple, Callable

def jitter_click(x: int, y: int, intensity: int = 2) -> None:
    """Simulates human-like click drift by applying random offset."""
    dx, dy = random.randint(-intensity, intensity), random.randint(-intensity, intensity)
    pyautogui.click(x + dx, y + dy)

def smart_drag(start: Tuple[int, int], end: Tuple[int, int], steps: int = 10) -> None:
    """Bezier-style interpolation for drag operations."""
    pyautogui.moveTo(*start)
    pyautogui.mouseDown()
    for i in range(1, steps + 1):
        progress = i / steps
        curr_x = start[0] + (end[0] - start[0]) * progress
        curr_y = start[1] + (end[1] - start[1]) * progress
        pyautogui.moveTo(int(curr_x), int(curr_y))
        time.sleep(0.01)
    pyautogui.mouseUp()

def batch_sequence(tasks: list[Callable]) -> None:
    """Chain executable tasks with randomized inter-action delay."""
    for task in tasks:
        task()
        time.sleep(random.uniform(0.1, 0.5))

def safety_break(threshold: int = 500) -> None:
    """Emergency halt triggers based on cursor velocity metrics."""
    pos_a = pyautogui.position()
    time.sleep(0.1)
    pos_b = pyautogui.position()
    dist = ((pos_b[0] - pos_a[0])**2 + (pos_b[1] - pos_a[1])**2)**0.5
    if dist > threshold:
        raise InterruptedError("Cursor movement threshold exceeded")