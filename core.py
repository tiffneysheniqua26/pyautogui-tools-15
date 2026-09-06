import pyautogui
import time
import threading

class AutoClicker:
    def __init__(self, interval=0.1):
        self.interval = interval
        self.running = False
        self._lock = threading.Lock()

    def _perform_click(self):
        while self.running:
            pyautogui.click()
            time.sleep(self.interval)

    def toggle(self):
        with self._lock:
            self.running = not self.running
            if self.running:
                threading.Thread(target=self._perform_click, daemon=True).start()

class ClickManager:
    @staticmethod
    def execute_sequence(coords_list):
        for x, y in coords_list:
            pyautogui.moveTo(x, y)
            pyautogui.click()

def emergency_stop():
    pyautogui.FAILSAFE = True

if __name__ == '__main__':
    emergency_stop()
    clicker = AutoClicker(0.5)
    clicker.toggle()
    time.sleep(2)
    clicker.toggle()