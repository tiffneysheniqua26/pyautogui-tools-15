import pyautogui
import time
import logging

class ClickError(Exception): pass

def execute_safe_click(x, y, interval=0.1):
    """Attempts to click, gracefully yielding on failures."""
    try:
        if not (0 <= x <= pyautogui.size().width and 0 <= y <= pyautogui.size().height):
            raise ValueError('Coordinates outside screen boundaries')
        
        pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.click()
        time.sleep(interval)
        
    except pyautogui.FailSafeException:
        logging.critical('Panic triggered: aborting click sequence')
        raise
    except Exception as e:
        logging.error(f'Runtime glitch: {e}')
        return False
    return True

def batch_process_clicks(coords):
    """Iterative processing with fault tolerance."""
    results = []
    for i, (x, y) in enumerate(coords):
        try:
            status = execute_safe_click(x, y)
            results.append(status)
        except Exception:
            logging.warning(f'Skipping point {i} due to instability')
            continue
    return all(results)