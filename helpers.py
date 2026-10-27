import pyautogui
import time

def validate_coordinates(x, y):
    screen_w, screen_h = pyautogui.size()
    if not (0 <= x <= screen_w and 0 <= y <= screen_h):
        raise ValueError(f"Coordinates ({x}, {y}) out of screen bounds ({screen_w}, {screen_h})")
    return True

def validate_interval(interval):
    if not isinstance(interval, (int, float)) or interval < 0.001:
        raise ValueError(f"Interval {interval} is too fast or invalid")
    return True

def sanitized_click_params(x, y, interval):
    try:
        validate_coordinates(x, y)
        validate_interval(interval)
        return True
    except ValueError as e:
        print(f"[!] Validation failure: {e}")
        return False

def perform_safe_click(x, y, interval):
    if sanitized_click_params(x, y, interval):
        pyautogui.click(x, y)
        time.sleep(interval)
        return True
    return False

# The click loop logic for processing
def execute_click_batch(targets):
    results = []
    for target in targets:
        x, y, interval = target
        status = perform_safe_click(x, y, interval)
        results.append(status)
    return all(results)