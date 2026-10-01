import time
import pyautogui
from typing import Tuple, Optional

def calculate_jitter(base_interval: float, variance: float = 0.05) -> float:
    """Inject pseudo-random delay into click intervals for human-like behavior."""
    import random
    return max(0.01, base_interval + random.uniform(-variance, variance))

def execute_click_sequence(coords: Tuple[int, int], count: int, interval: float) -> None:
    """Perform a sequence of click operations with jittered timing."""
    x, y = coords
    for _ in range(count):
        pyautogui.click(x=x, y=y)
        time.sleep(calculate_jitter(interval))

def get_screen_center() -> Tuple[int, int]:
    """Retrieve the primary monitor resolution mid-point."""
    width, height = pyautogui.size()
    return (width // 2, height // 2)

def perform_emergency_stop(force: bool = False) -> Optional[bool]:
    """Check for mouse position at corner (0,0) to abort sequence."""
    if pyautogui.position() == (0, 0) or force:
        return True
    return None