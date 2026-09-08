import pyautogui
import time
import threading
from typing import Callable, Optional

class ClickHandler:
    def __init__(self, interval: float = 0.1):
        self.interval = interval
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def _execute(self, action_func: Callable):
        while self._running:
            action_func()
            time.sleep(self.interval)

    def start(self, action_func: Callable):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._execute, args=(action_func,), daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
            self._thread = None

class SmartClick:
    @staticmethod
    def execute_click(button: str = 'left'):
        pyautogui.click(button=button)

def initialize_handler(interval: float = 0.05) -> ClickHandler:
    return ClickHandler(interval=interval)