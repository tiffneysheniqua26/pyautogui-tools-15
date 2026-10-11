import pyautogui
import time
import logging
from typing import Tuple

class ClickHandler:
    def __init__(self, interval: float = 0.1):
        self.interval = interval
        self.is_active = False
        logging.basicConfig(level=logging.INFO)

    def toggle_state(self) -> None:
        self.is_active = not self.is_active
        logging.info(f"Handler state: {'Active' if self.is_active else 'Idle'}")

    def execute_click(self, coords: Tuple[int, int]) -> None:
        if self.is_active:
            pyautogui.click(x=coords[0], y=coords[1])
            time.sleep(self.interval)

    def emergency_stop(self) -> None:
        self.is_active = False
        pyautogui.FAILSAFE = True

    def run_sequence(self, path: list[Tuple[int, int]]) -> None:
        """Executes a sequential click pattern until interrupted."""
        try:
            while self.is_active:
                for pos in path:
                    if not self.is_active: break
                    self.execute_click(pos)
        except pyautogui.FailSafeException:
            self.emergency_stop()
            logging.warning("Failsafe triggered, stopping sequence")