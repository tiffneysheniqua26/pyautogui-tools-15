import pyautogui
import time
import threading

class ClickHandler:
    def __init__(self, interval=0.1):
        self.interval = interval
        self.running = False
        self._thread = None

    def _click_loop(self):
        while self.running:
            pyautogui.click()
            time.sleep(self.interval)

    def start(self):
        if not self.running:
            self.running = True
            self._thread = threading.Thread(target=self._click_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()

    def update_speed(self, new_interval):
        self.interval = max(0.01, float(new_interval))

def execute_emergency_stop():
    pyautogui.FAILSAFE = True
    pyautogui.mouseInfo()