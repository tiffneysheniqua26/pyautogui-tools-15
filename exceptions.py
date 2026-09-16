import time
import functools

class PerformanceBottleneckError(Exception):
    """Raised when the click stream exceeds system latency tolerance."""
    pass

class ExecutionThresholdExceeded(PerformanceBottleneckError):
    """Custom error for micro-benchmark violations in core clicks."""
    pass

def time_execution(threshold: float):
    """Decorator for monitoring core processing latency."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            if duration > threshold:
                raise ExecutionThresholdExceeded(f"{func.__name__} took {duration:.6f}s")
            return result
        return wrapper
    return decorator

class ThrottleController:
    """Reactive limiter for event queue backpressure management."""
    def __init__(self, limit: int = 100):
        self.limit = limit
        self.counter = 0

    def __enter__(self):
        self.counter += 1
        if self.counter > self.limit:
            raise PerformanceBottleneckError("Queue overflow imminent")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.counter -= 1