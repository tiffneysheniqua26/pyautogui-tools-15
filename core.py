import time
import pyautogui
from functools import lru_cache

class ClickEngine:
    def __init__(self, throttle=0.01):
        self.throttle = throttle
        pyautogui.PAUSE = 0
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.MINIMUM_SLEEP = 0

    @lru_cache(maxsize=128)
    def _get_coordinates(self, x: int, y: int):
        return x, y

    def rapid_fire(self, x: int, y: int, iterations: int):
        coord = self._get_coordinates(x, y)
        safe_click = pyautogui.click
        sleep = time.sleep
        
        for _ in range(iterations):
            safe_click(*coord)
            if self.throttle > 0:
                sleep(self.throttle)

    def batch_execute(self, actions: list):
        """
        Optimized bulk processing using internal coordinate caching
        and local function lookups to minimize lookup overhead.
        """
        for action in actions:
            self.rapid_fire(*action)

if __name__ == '__main__':
    engine = ClickEngine(throttle=0.001)
    engine.rapid_fire(100, 100, 50)