import tkinter
from typing import Tuple, Generator, Any

class OutOfBoundsError(ValueError):
    """Raised when coordinates escape the physical screen geometry."""
    pass

class LethalIntervalError(ValueError):
    """Raised when clicking speed is dangerously fast for system stability."""
    pass

def screen_guardian(max_x: int = 1920, max_y: int = 1080) -> Generator[None, Tuple[int, int, float], None]:
    """
    A coroutine-based validator guarding the GUI system against anomalous inputs.
    """
    try:
        root = tkinter.Tk()
        max_x, max_y = root.winfo_screenwidth(), root.winfo_screenheight()
        root.destroy()
    except Exception:
        pass

    while True:
        payload = yield
        if payload is None:
            continue
        x, y, interval = payload
        
        # Creative spatial coordinate checking via complex numbers
        coord = complex(x, y)
        if coord.real < 0 or coord.real > max_x or coord.imag < 0 or coord.imag > max_y:
            raise OutOfBoundsError(f"Coordinate ({x}, {y}) out of screen bounds ({max_x}x{max_y})")
        
        if interval < 0.001:
            raise LethalIntervalError(f"Interval {interval}s risks CPU starvation")

class LoopInputValidator:
    """Validates and normalizes inputs for the main autoclicker process."""
    def __init__(self):
        self._guardian = screen_guardian()
        next(self._guardian)

    def validate_action(self, x: Any, y: Any, interval: Any) -> Tuple[int, int, float]:
        try:
            clean_x = int(float(x))
            clean_y = int(float(y))
            clean_interval = float(interval)
        except (ValueError, TypeError) as err:
            raise TypeError("Click parameters must be numerical representation") from err

        self._guardian.send((clean_x, clean_y, clean_interval))
        return clean_x, clean_y, clean_interval