import time
import functools

class PerformanceThresholdExceeded(Exception):
    """Raised when the click frequency exceeds system capacity."""
    pass

def throttled_execution(limit_hz: float):
    """Dynamic delay injection using closure-based time tracking."""
    interval = 1.0 / limit_hz
    last_called = [0.0]

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.perf_counter() - last_called[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.perf_counter()
            return result
        return wrapper
    return decorator

class ExecutionMonitor:
    """
    Context manager for micro-benchmarking click operations.
    Usage: with ExecutionMonitor(): perform_click()
    """
    def __init__(self, threshold=0.01):
        self.threshold = threshold

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.perf_counter() - self.start
        if duration > self.threshold:
            raise PerformanceThresholdExceeded(f"Click latency: {duration:.4f}s")