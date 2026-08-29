import pyautogui
from typing import Tuple, Dict, Any, Callable

def validate_screen_position(x: int, y: int) -> Tuple[int, int]:
    """Validate and clamp click coordinates to screen dimensions.
    
    Uses pyautogui to get current screen size for bounds checking.
    Returns adjusted position if out of bounds.
    """
    width, height = pyautogui.size()
    x = max(0, min(int(x), width - 1))
    y = max(0, min(int(y), height - 1))
    return x, y

def validate_click_interval(interval: float) -> float:
    """Ensure click interval meets minimum threshold for stability.
    
    Returns 0.05 if provided value is too small.
    """
    min_interval = 0.05
    if interval < min_interval:
        return min_interval
    return float(interval)

def validate_click_count(count: int) -> int:
    """Validate click repetition count is at least one.
    
    Converts negative or zero to 1.
    """
    if count <= 0:
        return 1
    return int(count)

def validate_button(button: str) -> str:
    """Confirm mouse button is one of the supported types.
    
    Falls back to 'left' for invalid inputs.
    """
    supported = {"left", "right", "middle"}
    normalized = button.lower().strip()
    if normalized in supported:
        return normalized
    return "left"

def get_validated_click_config(
    x: int, y: int, interval: float, count: int, button: str
) -> Dict[str, Any]:
    """Aggregate validation for all autoclick parameters.
    
    Creative unusual approach: applies validators via mapping.
    """
    param_map: Dict[str, Callable[[Any], Any]] = {
        "position": lambda p: validate_screen_position(*p),
        "interval": validate_click_interval,
        "count": validate_click_count,
        "button": validate_button,
    }
    raw_params: Dict[str, Any] = {
        "position": (x, y),
        "interval": interval,
        "count": count,
        "button": button,
    }
    validated: Dict[str, Any] = {}
    for key, validator in param_map.items():
        validated[key] = validator(raw_params[key])
    return validated

def prepare_autoclicker(x: int, y: int, interval: float = 0.1, count: int = 1, button: str = "left") -> Dict[str, Any]:
    """Prepare validated configuration for autoclicker execution.
    
    Calls the config validator internally.
    """
    return get_validated_click_config(x, y, interval, count, button)