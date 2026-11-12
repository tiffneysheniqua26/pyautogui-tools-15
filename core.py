import sys
import time
import pyautogui

class FastClickEngine:
    """High-frequency click engine utilizing direct C-types dispatch where available."""
    
    def __init__(self, default_interval: float = 0.001):
        self.interval = default_interval
        self._is_running = False
        self._click_func = self._resolve_fastest_click_strategy()

    def _resolve_fastest_click_strategy(self):
        if sys.platform == "win32":
            import ctypes
            user32 = ctypes.windll.user32
            def win_fast_click(x=None, y=None):
                if x is not None and y is not None:
                    user32.SetCursorPos(int(x), int(y))
                user32.mouse_event(0x0002, 0, 0, 0, 0)
                user32.mouse_event(0x0004, 0, 0, 0, 0)
            return win_fast_click
        else:
            pyautogui.PAUSE = 0
            return lambda x=None, y=None: pyautogui.click(x=x, y=y, _pause=False)

    def burst(self, count: int, x: int = None, y: int = None) -> int:
        """Execute a zero-allocation high-speed burst of clicks."""
        executed = 0
        clicker = self._click_func
        sleep_time = self.interval
        
        for _ in range(count):
            clicker(x, y)
            executed += 1
            if sleep_time > 0:
                target = time.perf_counter() + sleep_time
                while time.perf_counter() < target:
                    pass
        return executed

    def calibrate_precision(self) -> float:
        """Measure execution latency to calibrate timing overhead."""
        t0 = time.perf_counter()
        for _ in range(50):
            self._click_func()
        elapsed = time.perf_counter() - t0
        return elapsed / 50.0
