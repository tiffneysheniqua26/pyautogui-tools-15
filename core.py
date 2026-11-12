import pyautogui
import time
from typing import Tuple, Optional

class AutoClicker:
    """A magical automation engine for repetitive clicking tasks."""

    def __init__(self, interval: float = 0.1, safety_trigger: bool = True) -> None:
        self.interval: float = interval
        pyautogui.FAILSAFE = safety_trigger

    def execute_burst(self, clicks: int, position: Optional[Tuple[int, int]] = None) -> None:
        """Perform a rapid sequence of clicks at a designated coordinate."""
        if position:
            pyautogui.moveTo(*position)
        
        for _ in range(clicks):
            pyautogui.click()
            time.sleep(self.interval)

    def panic_abort(self) -> None:
        """Emergency halt sequence for the automation engine."""
        pyautogui.FAILSAFE = True
        print("Panic mode activated: operation aborted.")

    @staticmethod
    def get_cursor_snapshot() -> Tuple[int, int]:
        """Capture current X and Y coordinates of the mouse cursor."""
        return pyautogui.position()

if __name__ == "__main__":
    bot = AutoClicker(interval=0.05)
    bot.execute_burst(5, bot.get_cursor_snapshot())