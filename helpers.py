import pyautogui
import time
import logging

class ClickerGuard:
    def __init__(self, failsafe=True):
        pyautogui.FAILSAFE = failsafe

    def execute_click(self, x: int, y: int):
        try:
            if not (0 <= x <= pyautogui.size().width and 0 <= y <= pyautogui.size().height):
                raise ValueError(f"Coordinates ({x}, {y}) are out of screen bounds")
            pyautogui.click(x, y)
        except pyautogui.FailSafeException:
            logging.critical("Failsafe triggered by user interrupt")
            raise
        except Exception as e:
            logging.error(f"Execution error at {x},{y}: {e}")
            return False
        return True

    def safe_interval(self, seconds: float):
        try:
            if seconds < 0:
                raise ValueError("Negative sleep time is physically impossible")
            time.sleep(seconds)
        except Exception as e:
            logging.warning(f"Sleep jitter detected: {e}")
            time.sleep(0.1)

    def validate_cursor(self):
        pos = pyautogui.position()
        if pos.x < 0 or pos.y < 0:
            logging.warning("Cursor drift detected, resetting to origin")
            pyautogui.moveTo(0, 0)