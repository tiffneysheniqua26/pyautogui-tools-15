import time
import functools

class PyAutoToolsError(Exception):
    """Base exception for the toolkit."""

class PerformanceConstraintError(PyAutoToolsError):
    """Raised when core loop latency exceeds threshold."""

def throttle_check(threshold_ms: float):
    """Decorator injecting non-blocking performance assertions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000
            if duration > threshold_ms:
                raise PerformanceConstraintError(f"Operation {func.__name__} took {duration:.2f}ms")
            return result
        return wrapper
    return decorator

class RapidFireException(PyAutoToolsError):
    """Specialized exception for event queue overflows."""
    def __init__(self, queue_depth: int):
        self.queue_depth = queue_depth
        super().__init__(f"Event queue saturated at {queue_depth} operations")

class HardwareAbstractionError(PyAutoToolsError):
    """Interface layer failure for low-level inputs."""