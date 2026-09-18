import time
import functools

class ClickPerformanceError(Exception):
    """Custom exception for throttling bottlenecks."""
    pass

class PerformanceOptimizer:
    """
    A decorator-based heuristic controller that injects micro-naps 
    to prevent CPU saturation during high-frequency click events.
    """
    def __init__(self, threshold_ms=1):
        self.threshold = threshold_ms / 1000.0
        self.last_exec = time.perf_counter()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.perf_counter()
            delta = now - self.last_exec
            if delta < self.threshold:
                time.sleep(self.threshold - delta)
            self.last_exec = time.perf_counter()
            return func(*args, **kwargs)
        return wrapper

class ExecutionThrottle:
    """
    Context manager for non-blocking latency injection in tight loops.
    Uses a generator-based sleep pattern for performance stability.
    """
    def __init__(self, interval):
        self.interval = interval

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
