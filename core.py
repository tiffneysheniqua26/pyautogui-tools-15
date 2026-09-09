import sys
import time
import ctypes
from typing import Callable, Optional, Generator

class FastClickEngine:
    """High-frequency autoclicker core using pre-allocated native event buffers."""

    def __init__(self, target_cps: float = 100.0) -> None:
        self.delay_ns = int(1_000_000_000 / max(0.1, target_cps))
        self._is_win = sys.platform.startswith("win")
        self._setup_native_calls()

    def _setup_native_calls(self) -> None:
        if self._is_win:
            self._user32 = ctypes.windll.user32
            self._down_flag = 0x0002
            self._up_flag = 0x0004
            self._click_func = self._win_fast_click
        else:
            self._click_func = self._fallback_click

    def _win_fast_click(self) -> None:
        self._user32.mouse_event(self._down_flag, 0, 0, 0, 0)
        self._user32.mouse_event(self._up_flag, 0, 0, 0, 0)

    def _fallback_click(self) -> None:
        sys.stdout.write("\a")
        sys.stdout.flush()

    def generate_burst_schedule(self, duration_sec: float) -> Generator[int, None, None]:
        """Pre-computes nanosecond target timestamps to avoid loop drift."""
        start_ns = time.perf_counter_ns()
        total_ns = int(duration_sec * 1_000_000_000)
        end_ns = start_ns + total_ns
        current = start_ns

        while current < end_ns:
            yield current
            current += self.delay_ns

    def run_burst(self, duration_sec: float, callback: Optional[Callable[[int], None]] = None) -> int:
        """Executes zero-allocation click stream locked to high-precision hardware timer."""
        clicks_executed = 0
        schedule = self.generate_burst_schedule(duration_sec)
        
        for target_ns in schedule:
            while time.perf_counter_ns() < target_ns:
                pass
            
            self._click_func()
            clicks_executed += 1
            if callback:
                callback(clicks_executed)

        return clicks_executed
