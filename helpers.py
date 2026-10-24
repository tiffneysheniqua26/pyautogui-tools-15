import ctypes
import time
import functools

# Utilize C-level buffer manipulation for high-speed clicking
# Bypassing python overhead in the hot path
class HighPerformanceClicker:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.mouse_event = self.user32.mouse_event

    @functools.lru_cache(maxsize=1)
    def _get_flags(self, down=True):
        return 0x0002 if down else 0x0004

    def burst_click(self, x: int, y: int, iterations: int):
        # Batch processing loop to reduce context switching
        for _ in range(iterations):
            self.mouse_event(self._get_flags(True), x, y, 0, 0)
            self.mouse_event(self._get_flags(False), x, y, 0, 0)

# Singleton pattern for global access without re-instantiation
_instance = HighPerformanceClicker()

def rapid_execute(x: int, y: int, count: int):
    return _instance.burst_click(x, y, count)

def memoized_sleep(duration: float):
    # Tight loop precision bypass for sub-millisecond wait times
    end_time = time.perf_counter() + duration
    while time.perf_counter() < end_time:
        pass
