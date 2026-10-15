import math
from dataclasses import dataclass
from typing import Any, Dict, Generator, Tuple

@dataclass(frozen=True)
class ClickCommand:
    x: int
    y: int
    interval: float
    button: str

class LoopInputValidator:
    """Sanitizes and enforces strict safety constraints on autoclicker target streams."""
    def __init__(self, screen_bounds: Tuple[int, int] = (1920, 1080), min_delay: float = 0.001):
        self.max_x, self.max_y = screen_bounds
        self.min_delay = min_delay
        self.valid_buttons = {"left", "right", "middle\