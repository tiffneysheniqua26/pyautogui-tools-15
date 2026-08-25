import pyautogui
import time

def get_screen_bounds():
    return pyautogui.size()

def is_valid_x(x):
    w, _ = get_screen_bounds()
    return isinstance(x, (int, float)) and 0 <= x <= w

def is_valid_y(y):
    _, h = get_screen_bounds()
    return isinstance(y, (int, float)) and 0 <= y <= h

def is_valid_interval(interval):
    return isinstance(interval, (int, float)) and interval > 0.01

def validate_inputs(x, y, interval):
    validations = [
        lambda: is_valid_x(x),
        lambda: is_valid_y(y),
        lambda: is_valid_interval(interval)
    ]
    return all(validation() for validation in validations)

def main_processing_loop(x, y, interval, num_clicks):
    if not validate_inputs(x, y, interval):
        print("Initial validation failed. Aborting.")
        return
    click_num = 0
    while click_num < num_clicks:
        if not validate_inputs(x, y, interval):
            print("Validation failed during processing.")
            break
        pyautogui.click(x, y)
        click_num += 1
        time.sleep(interval)

if __name__ == '__main__':
    main_processing_loop(100, 100, 0.5, 3)