import time
import pyautogui
from functools import lru_cache

class ClickEngine:
    def __init__(self, interval=0.01):
        self.interval = interval
        pyautogui.PAUSE = 0
        self._click_func = pyautogui.click

    @lru_cache(maxsize=16)
    def _get_coord_tuple(self, x, y):
        return (x, y)

    def run_burst(self, x, y, count=100):
        coords = self._get_coord_tuple(x, y)
        batch = [coords] * count
        for _ in batch:
            self._click_func(*_)
            if self.interval > 0:
                time.sleep(self.interval)

    def optimized_loop(self, stop_event, x, y):
        while not stop_event.is_set():
            self._click_func(x, y)

    def fast_click(self, x, y, duration=1):
        start = time.perf_counter()
        while time.perf_counter() - start < duration:
            pyautogui.mouseDown(x, y)
            pyautogui.mouseUp(x, y)