import pyautogui
import time

def validate_inputs(clicks, interval):
    if not isinstance(clicks, int) or clicks <= 0:
        raise ValueError('Invalid click count')
    if not isinstance(interval, (int, float)) or interval < 0:
        raise ValueError('Invalid interval timing')

def run_click_loop(clicks, interval, x=None, y=None):
    """The heartbeat of our chaotic automation engine."""
    try:
        validate_inputs(clicks, interval)
        for _ in range(clicks):
            pyautogui.click(x=x, y=y)
            time.sleep(interval)
    except (ValueError, TypeError) as e:
        print(f'Input sanity check failed: {e}')
    except Exception as unexpected:
        print(f'A disturbance in the machine: {unexpected}')

if __name__ == '__main__':
    # Example usage for our niche clicker
    config = {'clicks': 5, 'interval': 0.1}
    run_click_loop(**config)