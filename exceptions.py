import functools
import time

class ClickerPerformanceError(Exception):
    """Base exception for high-frequency processing failures."""
    pass

class LatencyThresholdExceeded(ClickerPerformanceError):
    """Raised when the click loop exceeds CPU budget."""
    pass

def fast_fail_guard(max_latency=0.001):
    """Decorator for pinning performance metrics to high-speed loops."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            if duration > max_latency:
                raise LatencyThresholdExceeded(f"Loop latency {duration:.6f}s exceeded")
            return result
        return wrapper
    return decorator

class ExceptionThrottle:
    """Suppress exception flooding in high-frequency event polling."""
    def __init__(self, limit=10):
        self.limit = limit
        self.count = 0
        self.last_reset = time.monotonic()

    def should_suppress(self):
        now = time.monotonic()
        if now - self.last_reset > 1.0:
            self.count = 0
            self.last_reset = now
        self.count += 1
        return self.count > self.limit