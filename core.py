import pyautogui
import time
from typing import Tuple, Optional

def execute_click(coords: Tuple[int, int], interval: float = 0.1) -> None:
    """Perform a targeted mouse click sequence at specified screen coordinates."""
    pyautogui.moveTo(coords[0], coords[1])
    pyautogui.click()
    time.sleep(interval)

def pulse_automation(duration: int, speed: float) -> None:
    """Run a high-frequency clicking loop based on a provided temporal pulse."""
    end_time: float = time.time() + duration
    while time.time() < end_time:
        pyautogui.click()
        time.sleep(speed)

def get_safety_bounds() -> Tuple[int, int]:
    """Retrieve the current display resolution boundaries for coordinate validation."""
    return pyautogui.size()

def emergency_stop(key: str = 'esc') -> bool:
    """Check for an abort signal to terminate ongoing automation routines."""
    return pyautogui.is_pressed(key)

class ClickEngine:
    """The central processing unit for hardware-simulated click operations."""
    def __init__(self, sensitivity: float = 0.05) -> None:
        self.sensitivity: float = sensitivity

    def run_burst(self, clicks: int) -> None:
        """Execute a defined burst of rapid clicks with engine-level pacing."""
        for _ in range(clicks):
            pyautogui.click()
            time.sleep(self.sensitivity)