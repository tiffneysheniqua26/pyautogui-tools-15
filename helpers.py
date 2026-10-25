import pyautogui
import time
from typing import Tuple, Optional

def get_safe_coords(x: int, y: int) -> Tuple[int, int]:
    """Ensures coordinates stay within primary monitor boundaries."""
    width, height = pyautogui.size()
    return max(0, min(x, width - 1)), max(0, min(y, height - 1))

def perform_click(x: int, y: int, interval: float = 0.1) -> None:
    """Executes a guarded click operation at specific screen coordinates."""
    safe_x, safe_y = get_safe_coords(x, y)
    pyautogui.click(x=safe_x, y=safe_y)
    time.sleep(interval)

def get_mouse_position() -> Tuple[int, int]:
    """Retrieves current cursor location as a sanitized tuple."""
    pos = pyautogui.position()
    return int(pos.x), int(pos.y)

def jitter_cursor(intensity: int = 2) -> None:
    """Adds microscopic movement to prevent idle state detection."""
    x, y = get_mouse_position()
    pyautogui.moveRel(intensity, -intensity)
    pyautogui.moveRel(-intensity, intensity)

class ClickSequence:
    """Stateful executor for automated click pattern generation."""
    def __init__(self, sequence: list[Tuple[int, int]]) -> None:
        self.sequence = sequence

    def run(self, delay: float = 0.5) -> None:
        """Iterates through predefined sequence with dynamic timing."""
        for x, y in self.sequence:
            perform_click(x, y)
            time.sleep(delay)