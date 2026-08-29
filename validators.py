import pyautogui
from typing import Tuple, Any, Optional, Dict, Callable

def validate_positive(value: Any) -> bool:
    if isinstance(value, (int, float)):
        return value > 0
    return False

def validate_non_negative(value: Any) -> bool:
    if isinstance(value, (int, float)):
        return value >= 0
    return False

def validate_integer(value: Any) -> bool:
    return isinstance(value, int)

def validate_string_in_set(value: Any, valid_set: set) -> bool:
    if isinstance(value, str):
        return value.lower() in valid_set
    return False

def validate_tuple_of_ints(value: Any, length: int = 2) -> bool:
    if isinstance(value, (tuple, list)) and len(value) == length:
        return all(isinstance(item, int) for item in value)
    return False

def validate_screen_bounds(position: Tuple[int, int]) -> bool:
    if not validate_tuple_of_ints(position):
        return False
    x, y = position
    width, height = pyautogui.size()
    return 0 <= x < width and 0 <= y < height

def validate_button(button: str) -> bool:
    return validate_string_in_set(button, {'left', 'right', 'middle'})

def validate_click_count(count: int) -> bool:
    return validate_integer(count) and validate_positive(count)

def validate_interval(interval: float) -> bool:
    return validate_non_negative(interval)

def validate_duration(duration: Optional[float]) -> bool:
    if duration is None:
        return True
    return validate_non_negative(duration)

def validate_autoclicker_settings(
    position: Tuple[int, int],
    clicks: int = 1,
    interval: float = 0.1,
    button: str = 'left',
    duration: Optional[float] = None
) -> bool:
    validation_map: Dict[str, Callable] = {
        'position': lambda p: validate_tuple_of_ints(p) and validate_screen_bounds(p),
        'clicks': lambda c: validate_click_count(c),
        'interval': lambda i: validate_interval(i),
        'button': lambda b: validate_button(b),
        'duration': lambda d: validate_duration(d)
    }
    settings: Dict[str, Any] = {
        'position': position,
        'clicks': clicks,
        'interval': interval,
        'button': button,
        'duration': duration
    }
    validation_results = [validation_map[key](val) for key, val in settings.items() if key in validation_map]
    return all(validation_results)