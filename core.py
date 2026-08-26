import time
import functools

class ClickOptimizer:
    def __init__(self, target_cps: int = 100):
        self.delay = 1.0 / max(target_cps, 1)
        self._last_click = time.perf_counter()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.perf_counter()
            elapsed = now - self._last_click
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
            result = func(*args, **kwargs)
            self._last_click = time.perf_counter()
            return result
        return wrapper

@ClickOptimizer(target_cps=250)
def hyper_click(x: int, y: int) -> tuple:
    return (x, y)