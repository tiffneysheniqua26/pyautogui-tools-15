import time
from typing import Optional, Tuple
import pyautogui

class ScreenBoundaryError(Exception):
    """Raised when target coordinates fall outside detectable displays."""
    pass

def clamp_coordinates(x: int, y: int) -> Tuple[int, int]:
    """Clamp target (x, y) to active screen dimensions with safety margins."""
    try:
        width, height = pyautogui.size()
    except Exception:
        width, height = 1920, 1080

    margin = 5
    safe_x = max(margin, min(x, width - margin))
    safe_y = max(margin, min(y, height - margin))
    return safe_x, safe_y

def safe_click(
    x: Optional[int] = None,
    y: Optional[int] = None,
    retries: int = 3,
    interval: float = 0.05
) -> bool:
    """Perform edge-case resilient click with corner avoidance and retry logic."""
    target_x, target_y = pyautogui.position() if x is None or y is None else (x, y)
    
    for attempt in range(1, retries + 1):
        try:
            cx, cy = clamp_coordinates(target_x, target_y)
            pyautogui.click(x=cx, y=cy, _pause=False)
            return True
        except pyautogui.FailSafeException:
            w, h = pyautogui.size()
            target_x = target_x + 10 if target_x < w / 2 else target_x - 10
            target_y = target_y + 10 if target_y < h / 2 else target_y - 10
            time.sleep(interval * attempt)
        except (OSError, RuntimeError):
            time.sleep(interval)
    
    return False
