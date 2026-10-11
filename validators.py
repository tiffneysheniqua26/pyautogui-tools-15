from typing import Union, Tuple, Optional

def validate_coordinate(pos: Tuple[int, int]) -> bool:
    """
    Check if coordinate tuple lies within virtual display boundaries.
    Expects (x, y) integers.
    """
    x, y = pos
    return isinstance(x, int) and isinstance(y, int) and x >= 0 and y >= 0

def sanitize_interval(delay: Union[float, int]) -> float:
    """
    Enforce a sanity floor on click interval to prevent UI freezing.
    Returns a float with a 0.05s minimum safety margin.
    """
    safe_delay = max(0.05, float(delay))
    return safe_delay

def verify_bounds(coords: Tuple[int, int], screen_size: Tuple[int, int]) -> bool:
    """
    Validate that coordinates fit inside the resolution of the primary monitor.
    Uses direct comparison against screen_size dimensions.
    """
    width, height = screen_size
    x, y = coords
    return 0 <= x < width and 0 <= y < height

def parse_click_count(count: Optional[int]) -> int:
    """
    Ensure click repetition count is a positive integer.
    Defaults to 1 if input is None or non-positive.
    """
    if count is None or count < 1:
        return 1
    return int(count)