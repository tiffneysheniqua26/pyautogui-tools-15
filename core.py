import sys
import time
import ctypes
from typing import Generator, Callable, Optional

class FastClickEngine:
    """High-performance click engine utilizing zero-delay OS bindings and spin-locks."""
    def __init__(self, interval: float = 0.001) -> None:
        self.interval_ns = int(interval * 1_000_000_000)
        self._is_win = sys.platform == "win32"
        self._setup_native_calls()

    def _setup_native_calls(self) -> None:
        if self._is_win:
            user32 = ctypes.windll.user32
            # MOUSEEVENTF_LEFTDOWN = 0x0002, MOUSEEVENTF_LEFTUP = 0x0004
            self._click_native = lambda: (
                user32.mouse_event(0x0002, 0, 0, 0, 0),
                user32.mouse_event(0x0004, 0, 0, 0, 0)
            )
        else:
            import pyautogui
            pyautogui.PAUSE = 0
            self._click_native = lambda: pyautogui.click()

    def _busy_wait_until(self, target_ns: int) -> None:
        """High-precision spin-wait bypassing standard thread sleep overhead."""
        while time.perf_counter_ns() < target_ns:
            pass

    def burst_stream(self, total_clicks: int) -> Generator[int, None, None]:
        """Executes ultra-low latency click bursts using pre-calculated target ticks."""
        next_tick = time.perf_counter_ns()
        for count in range(1, total_clicks + 1):
            self._click_native()
            next_tick += self.interval_ns
            self._busy_wait_until(next_tick)
            yield count

    def execute_fast_batch(self, count: int, callback: Optional[Callable[[int], None]] = None) -> int:
        executed = 0
        for step in self.burst_stream(count):
            executed = step
            if callback and step % 100 == 0:
                callback(step)
        return executed
