import pyautogui
import time
import logging

class ClickerEngine:
    def __init__(self, interval=0.1):
        self.interval = interval
        self.active = False
        pyautogui.FAILSAFE = True

    def run(self, iterations=100):
        self.active = True
        try:
            for i in range(iterations):
                if not self.active:
                    break
                x, y = pyautogui.position()
                pyautogui.click(x, y)
                time.sleep(self.interval)
        except pyautogui.FailSafeException:
            logging.warning('Failsafe triggered by user cursor movement')
        except pyautogui.PyAutoGUIException as e:
            logging.error(f'System constraint violation: {e}')
        except KeyboardInterrupt:
            logging.info('Manual abort signal received')
        finally:
            self.active = False

    def emergency_stop(self):
        self.active = False

def perform_click(x, y):
    try:
        if x < 0 or y < 0:
            raise ValueError('Coordinates outside screen bounds')
        pyautogui.click(x, y)
    except (pyautogui.ImageNotFoundException, ValueError) as e:
        logging.error(f'Click operation failure: {e}')