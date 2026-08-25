import pyautogui
from typing import Dict, Any, Tuple, Optional
class AutoclickerValidationError(Exception):
    pass
def validate_click_interval(interval: Any) -> float:
    if not isinstance(interval, (int, float)):
        raise TypeError("Click interval must be numeric")
    if interval <= 0:
        raise ValueError("Click interval must be positive")
    return float(interval)
def validate_click_count(count: Any) -> int:
    if not isinstance(count, int):
        raise TypeError("Click count must be integer")
    if count < 1:
        raise ValueError("Must click at least once")
    return count
def validate_mouse_button(button: Any) -> str:
    allowed = ("left", "right", "middle")
    if not isinstance(button, str):
        raise TypeError("Mouse button must be string")
    button_lower = button.lower().strip()
    if button_lower not in allowed:
        raise ValueError(f"Button must be one of {allowed}, got {button}")
    return button_lower
def validate_screen_position(x: Any, y: Any) -> Tuple[int, int]:
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Coordinates must be numeric")
    x_int = int(x)
    y_int = int(y)
    try:
        width, height = pyautogui.size()
    except Exception as exc:
        raise RuntimeError("Unable to determine screen dimensions") from exc
    if x_int < 0 or x_int >= width or y_int < 0 or y_int >= height:
        raise ValueError(f"Position ({x_int}, {y_int}) outside screen bounds 0-{width}x0-{height}")
    return (x_int, y_int)
def validate_autoclick_config(config: Dict[str, Any]) -> Dict[str, Any]:
    errors = []
    validated_config = {}
    required_fields = ['interval', 'clicks', 'button']
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    if errors:
        raise AutoclickerValidationError("; ".join(errors))
    try:
        validated_config['interval'] = validate_click_interval(config['interval'])
    except Exception as e:
        errors.append(f"interval: {str(e)}")
    try:
        validated_config['clicks'] = validate_click_count(config['clicks'])
    except Exception as e:
        errors.append(f"clicks: {str(e)}")
    try:
        validated_config['button'] = validate_mouse_button(config['button'])
    except Exception as e:
        errors.append(f"button: {str(e)}")
    if 'x' in config and 'y' in config:
        try:
            validated_config['x'], validated_config['y'] = validate_screen_position(config['x'], config['y'])
        except Exception as e:
            errors.append(f"position: {str(e)}")
    if errors:
        raise AutoclickerValidationError("Validation failed: " + "; ".join(errors))
    for k, v in config.items():
        if k not in validated_config:
            validated_config[k] = v
    return validated_config