import time
import random
from typing import Tuple, Optional

def get_jittered_delay(base_ms: float, variance_pct: float = 0.1) -> float:
    """
    Calculate a randomized delay to prevent detection patterns.

    Args:
        base_ms: The base duration in milliseconds.
        variance_pct: The percentage of deviation allowed.

    Returns:
        A float representing the final delay in seconds.
    """
    variance = base_ms * variance_pct
    jitter = random.uniform(-variance, variance)
    return (base_ms + jitter) / 1000.0

def validate_coordinate(x: int, y: int, screen_dims: Tuple[int, int]) -> bool:
    """
    Ensure click targets reside within active monitor bounds.

    Args:
        x: Horizontal pixel coordinate.
        y: Vertical pixel coordinate.
        screen_dims: Tuple containing (width, height).

    Returns:
        True if coordinate is within bounds, False otherwise.
    """
    width, height = screen_dims
    return 0 <= x < width and 0 <= y < height

def rhythmic_sleep(duration: float) -> None:
    """
    Perform a busy-wait style sleep to maintain high precision.

    Args:
        duration: Time to sleep in seconds.
    """
    start = time.perf_counter()
    while time.perf_counter() - start < duration:
        pass
