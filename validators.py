import pyautogui
from typing import Dict, Any, Tuple, List, Optional

def validate_click_interval(interval: float) -> bool:
    """Validate click interval.
    Args:
        interval: Delay in seconds.
    Returns:
        True if 0.001 <= interval <= 3600.
    """
    if not isinstance(interval, (int, float)) or interval <= 0:
        return False
    return interval <= 3600

def validate_coordinates(x: int, y: int) -> bool:
    """Validate screen coordinates.
    Args:
        x: X position.
        y: Y position.
    Returns:
        True if within screen.
    """
    try:
        width, height = pyautogui.size()
        return 0 <= x < width and 0 <= y < height
    except Exception:
        return False

def validate_click_count(count: int) -> bool:
    """Validate number of clicks.
    Args:
        count: Number of clicks.
    Returns:
        True if 1 <= count <= 100000.
    """
    return isinstance(count, int) and 1 <= count <= 100000

def validate_button(button: str) -> bool:
    """Validate mouse button.
    Args:
        button: 'left', 'right' or 'middle'.
    Returns:
        True if valid.
    """
    if not isinstance(button, str):
        return False
    return button.lower() in {'left', 'right', 'middle'}

def validate_config(config: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate autoclicker config dict.
    Creative: uses sequential checks.
    Args:
        config: Dict with interval, x, y, count, button.
    Returns:
        (is_valid, error or None)
    """
    if not isinstance(config, dict):
        return False, "Config must be a dictionary"
    required = ['interval', 'x', 'y', 'count', 'button']
    for key in required:
        if key not in config:
            return False, f"Missing required key: {key}"
    if not validate_click_interval(config['interval']):
        return False, "Invalid click interval"
    if not validate_coordinates(config['x'], config['y']):
        return False, "Invalid coordinates"
    if not validate_click_count(config['count']):
        return False, "Invalid click count"
    if not validate_button(config['button']):
        return False, "Invalid mouse button"
    return True, None

def batch_validate(configs: List[Dict[str, Any]]) -> List[Tuple[bool, Optional[str]]]:
    """Validate list of configs.
    Args:
        configs: List of dicts.
    Returns:
        List of (bool, str or None)
    """
    return [validate_config(cfg) for cfg in configs]