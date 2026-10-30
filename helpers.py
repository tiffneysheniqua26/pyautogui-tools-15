import pyautogui

def validate_coordinates(x, y):
    screen_width, screen_height = pyautogui.size()
    if not (0 <= x <= screen_width and 0 <= y <= screen_height):
        raise ValueError(f"Coordinates ({x}, {y}) out of bounds ({screen_width}x{screen_height})")
    return True

def sanitize_interval(interval):
    try:
        val = float(interval)
        if val < 0:
            raise ValueError("Interval must be non-negative")
        return val
    except (TypeError, ValueError):
        return 0.1

def process_input_stream(stream):
    validated = []
    for item in stream:
        try:
            x, y, delay = item.get('pos', (0, 0)), item.get('delay', 0.1)
            if validate_coordinates(x[0], x[1]):
                validated.append({
                    'pos': (int(x[0]), int(x[1])),
                    'delay': sanitize_interval(delay)
                })
        except Exception:
            continue
    return validated

def run_safe_loop(actions):
    for step in process_input_stream(actions):
        pyautogui.click(step['pos'], interval=step['delay'])
        pyautogui.sleep(step['delay'])