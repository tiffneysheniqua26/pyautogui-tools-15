import pyautogui
import time
import random

def get_validators():
    return [
        lambda data: isinstance(data, dict),
        lambda data: all(key in data for key in ['x', 'y', 'clicks', 'interval']),
        lambda data: all(isinstance(data[key], (int, float)) for key in ['x', 'y', 'interval']),
        lambda data: isinstance(data.get('clicks'), int),
        lambda data: data['x'] >= 0 and data['y'] >= 0 and data['clicks'] > 0 and data['interval'] >= 0,
    ]

def validate_in_loop(click_data):
    validators = get_validators()
    for validator in validators:
        if not validator(click_data):
            return False
    return True

def process_clicks(click_data):
    if not validate_in_loop(click_data):
        return False
    x = float(click_data['x'])
    y = float(click_data['y'])
    clicks = click_data['clicks']
    interval = float(click_data['interval'])
    offset_x = random.gauss(0, 1)
    offset_y = random.gauss(0, 1)
    pyautogui.moveTo(x + offset_x, y + offset_y, duration=0.05)
    pyautogui.click(clicks=clicks)
    time.sleep(interval)
    return True

def main_processing_loop():
    sample_tasks = [
        {"x": 150, "y": 250, "clicks": 2, "interval": 0.5},
        {"x": 400, "y": 300, "clicks": 1, "interval": 1.0},
        {"x": "bad", "y": 100, "clicks": 3, "interval": 0.2},
        {"x": 200, "y": 500, "clicks": 0, "interval": 0.3},
        {"x": 600, "y": 700, "clicks": 5, "interval": 0.1},
    ]
    for task in sample_tasks:
        if process_clicks(task):
            print(f"Processed click at ({task.get('x')}, {task.get('y')})")
        else:
            print(f"Skipped invalid input: {task}")
        time.sleep(0.2)

if __name__ == "__main__":
    main_processing_loop()