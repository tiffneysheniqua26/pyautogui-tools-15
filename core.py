import time
import ctypes
from typing import Callable, Optional

class FastClicker:
    """High-performance click engine utilizing native OS calls."""
    def __init__(self, delay: float = 0.001) -> None:
        self.delay = delay
        self._is_running = False
        self._user32 = getattr(ctypes, 'windll', None).user32 if hasattr(ctypes, 'windll') else None

    def _native_click(self) -> None:
        if self._user32:
            self._user32.mouse_event(2, 0, 0, 0, 0)
            self._user32.mouse_event(4, 0, 0, 0, 0)

    def run_burst(self, count: int, callback: Optional[Callable[[int], None]] = None) -> int:
        self._is_running = True
        performed = 0
        target_time = time.perf_counter()
        
        while self._is_running and performed < count:
            self._native_click()
            performed += 1
            if callback:
                callback(performed)
            
            target_time += self.delay
            sleep_duration = target_time - time.perf_counter()
            if sleep_duration > 0:
                time.sleep(sleep_duration)
                
        return performed

    def stop(self) -> None:
        self._is_running = False