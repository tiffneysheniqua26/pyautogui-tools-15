import pyautogui
import time
from typing import Tuple, Optional

def get_mouse_coordinates() -> Tuple[int, int]:
    """Fetches the current X and Y coordinates of the cursor.
    Returns a tuple containing current screen positions."""
    return pyautogui.position()

def execute_click(x: Optional[int] = None, y: Optional[int] = None, interval: float = 0.1) -> None:
    """Perform a click at specified coordinates.
    If coordinates are omitted, performs click at current position.
    Utilizes internal pyautogui click handler with a safe buffer."""
    pyautogui.click(x=x, y=y)
    time.sleep(interval)

def screen_safety_check(x: int, y: int) -> bool:
    """Validates coordinates against current screen resolution boundaries.
    Ensures the autoclicker doesn't attempt out-of-bounds maneuvers."""
    width, height = pyautogui.size()
    return 0 <= x < width and 0 <= y < height

def panic_mode_trigger() -> None:
    """Hard-resets pyautogui failsafe protocols.
    Aborts active execution cycles by dumping the failsafe exception."""
    pyautogui.FAILSAFE = True
    pyautogui.FAILSAFE_POINTS = [(0, 0)]

def rapid_click_sequence(iterations: int, delay: float = 0.05) -> None:
    """Execution engine for high-frequency click simulation.
    Maintains constant pressure on target indices via procedural loops."""
    for _ in range(iterations):
        pyautogui.click()
        time.sleep(delay)