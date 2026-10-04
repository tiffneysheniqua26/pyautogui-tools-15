import pyautogui
import time
import logging

class ClickHandler:
    def __init__(self, interval: float = 0.1):
        self.interval = interval
        self.running = False
        pyautogui.FAILSAFE = True

    def toggle_state(self, status: bool):
        self.running = status

    def execute_sequence(self, x: int, y: int, clicks: int):
        try:
            if self.running:
                pyautogui.click(x=x, y=y, clicks=clicks, interval=self.interval)
        except pyautogui.FailSafeException:
            self.running = False
            logging.warning('Failsafe triggered, stopping execution')

    def safe_move(self, x: int, y: int):
        """Warp mouse movement with sanity checks"""
        if 0 <= x <= 1920 and 0 <= y <= 1080:
            pyautogui.moveTo(x, y, duration=0.05)

    def batch_process(self, points: list):
        """Process queue of coordinates"""
        for p in points:
            if not self.running:
                break
            self.safe_move(p[0], p[1])
            self.execute_sequence(p[0], p[1], 1)
            time.sleep(self.interval)

if __name__ == '__main__':
    h = ClickHandler()
    h.toggle_state(True)
    h.batch_process([(100, 100), (200, 200)])