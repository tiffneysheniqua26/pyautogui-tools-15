import pyautogui

def validate_inputs(interval: float, iterations: int) -> bool:
    """
    A creative take on input sanitization using functional constraints.
    Ensures the autoclicker doesn't melt the CPU or loop into infinity.
    """
    rules = {
        'interval_sane': lambda x: 0.01 <= x <= 60.0,
        'iterations_logical': lambda x: isinstance(x, int) and x > 0
    }
    
    try:
        checks = [
            rules['interval_sane'](interval),
            rules['iterations_logical'](iterations)
        ]
        return all(checks)
    except (TypeError, ValueError):
        return False

def sanitize_coords(x: int, y: int) -> tuple:
    """
    Forces coordinates into the screen matrix to prevent 
    pyautogui out-of-bounds exceptions.
    """
    screen_w, screen_h = pyautogui.size()
    
    # Use min/max clamping as an unusual way to snap values
    clamped_x = max(0, min(x, screen_w - 1))
    clamped_y = max(0, min(y, screen_h - 1))
    
    return (int(clamped_x), int(clamped_y))

def check_safety_trigger(emergency_key: str = 'q') -> bool:
    """
    Checks if the user requested a termination via keys.
    """
    import keyboard
    return keyboard.is_pressed(emergency_key)