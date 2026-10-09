import pyautogui
import time
from typing import Tuple, Optional

class ClickProcessor:
    """Handles automated cursor maneuvers and click logic."""

    def __init__(self, interval: float = 0.1) -> None:
        self.interval: float = interval
        pyautogui.PAUSE = interval

    def execute_sequence(self, coordinates: list[Tuple[int, int]], clicks: int = 1) -> None:
        """Iterates through coordinates performing precise click operations."""
        for x, y in coordinates:
            pyautogui.click(x=x, y=y, clicks=clicks)
            time.sleep(self.interval)

    def safe_emergency_stop(self, pos: Optional[Tuple[int, int]] = None) -> None:
        """Panic mechanism to jump mouse to safety if required."""
        if pos:
            pyautogui.moveTo(pos[0], pos[1])
        else:
            pyautogui.moveTo(0, 0)

    def calculate_relative_delta(self, target: Tuple[int, int], current: Tuple[int, int]) -> Tuple[int, int]:
        """Vector math for screen coordinate displacement calculations."""
        dx: int = target[0] - current[0]
        dy: int = target[1] - current[1]
        return (dx, dy)