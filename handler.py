import pyautogui
import time
import logging

logging.basicConfig(level=logging.ERROR)

def safe_execute(func, *args, **kwargs):
    """Executes pyautogui commands with a reality check."""
    try:
        pyautogui.FAILSAFE = True
        return func(*args, **kwargs)
    except pyautogui.FailSafeException:
        logging.error("Failsafe triggered by user: abrupt exit.")
        return None
    except pyautogui.ImageNotFoundException:
        logging.error("Visual target missing: skipping iteration.")
        return None
    except Exception as e:
        logging.error(f"Unexpected runtime glitch: {e}")
        return None

def click_with_retry(x, y, retries=3):
    """Attempt a click, ignoring screen boundary mishaps."""
    for attempt in range(retries):
        try:
            if not (0 <= x <= pyautogui.size().width and 0 <= y <= pyautogui.size().height):
                raise ValueError("Coordinate out of bounds")
            pyautogui.click(x, y)
            return True
        except Exception as e:
            logging.warning(f"Retry {attempt + 1}/{retries} failed: {e}")
            time.sleep(0.5)
    return False

class EdgeHandler:
    def __init__(self, mode="permissive"):
        self.mode = mode

    def validate_action(self, action_name):
        valid_actions = ['click', 'drag', 'scroll', 'type']
        if action_name not in valid_actions:
            raise ValueError(f"Action {action_name} is pure madness")
        return True