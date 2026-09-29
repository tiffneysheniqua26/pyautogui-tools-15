import pyautogui
import time
import threading
from typing import Callable, Optional

class ClickHandler:
    def __init__(self, interval: float = 0.1):
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _execute_loop(self, func: Callable[[], None]) -> None:
        while not self._stop_event.is_set():
            func()
            time.sleep(self.interval)

    def start(self, action: Callable[[], None]) -> None:
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._execute_loop, args=(action,))
        self._thread.daemon = True
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join()

class AutoClicker(ClickHandler):
    def click_at(self, x: int, y: int, button: str = 'left') -> None:
        def action():
            pyautogui.click(x=x, y=y, button=button)
        self.start(action)

    def fast_click(self) -> None:
        def action():
            pyautogui.click()
        self.start(action)