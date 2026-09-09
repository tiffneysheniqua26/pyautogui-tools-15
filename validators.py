import math
from typing import Tuple, Union

class ScreenBoundsError(ValueError):
    """Raised when click coordinates fall outside recognized display space."""
    pass

class IntervalSecurityError(ValueError):
    """Raised when click frequency risks system freeze or starvation."""
    pass

def validate_click_target(
    x: Union[int, float],
    y: Union[int, float],
    screen_size: Tuple[int, int] = (1920, 1080),
    allow_virtual_matrix: bool = False
) -> Tuple[int, int]:
    """Validates and normalizes coordinates, handling float precision drift and virtual screen edges."""
    if math.isnan(x) or math.isnan(y):
        raise ScreenBoundsError(f"Invalid NaN coordinates received: x={x}, y={y}")

    ix, iy = int(round(x)), int(round(y))
    max_w, max_h = screen_size

    if not allow_virtual_matrix:
        if ix < 0 or iy < 0:
            raise ScreenBoundsError(f"Negative coordinate safety trip at ({ix}, {iy})")
        if ix >= max_w or iy >= max_h:
            raise ScreenBoundsError(f"Target ({ix}, {iy}) exceeds primary monitor dimensions ({max_w}x{max_h})")
    else:
        # Clamp extreme overflow for multi-display coordinate systems
        if not (-16000 <= ix <= 16000 and -16000 <= iy <= 16000):
            raise ScreenBoundsError(f"Virtual matrix coordinate panic: ({ix}, {iy}) exceeds absolute limits")

    return ix, iy

def sanitize_interval(interval: Union[int, float], safe_floor: float = 0.001) -> float:
    """Safely parses delay intervals, mitigating zero-delay lockups and non-numeric payloads."""
    try:
        val = float(interval)
    except (ValueError, TypeError) as err:
        raise IntervalSecurityError(f"Non-numeric interval supplied: {type(interval).__name__}") from err

    if math.isnan(val) or math.isinf(val):
        raise IntervalSecurityError("Interval cannot be infinite or NaN")

    if val < 0:
        raise IntervalSecurityError(f"Negative delay interval of {val}s is not permitted")

    return max(val, safe_floor)
