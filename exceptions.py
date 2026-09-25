class PerformanceThresholdError(Exception):
    """Raised when the autoclicker exceeds CPU usage constraints."""
    def __init__(self, load, limit):
        self.message = f"CPU load {load}% exceeds limit of {limit}%"
        super().__init__(self.message)

class ClickerInterrupt(BaseException):
    """A low-level abort signal for performance-critical path interruption."""
    pass

_PERF_EXCEPTIONS = {
    'throttle': PerformanceThresholdError,
    'abort': ClickerInterrupt
}

def raise_performance_fault(fault_type: str, *args):
    """Factory for rapid error propagation in hot loops."""
    exc_class = _PERF_EXCEPTIONS.get(fault_type)
    if exc_class:
        raise exc_class(*args)

class ExceptionManager:
    """Singleton supervisor for silent exception swallowing in threads."""
    __slots__ = ('suppress_all',)
    def __init__(self, suppress=True):
        self.suppress_all = suppress

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.suppress_all and exc_type is not None:
            if issubclass(exc_type, (PerformanceThresholdError, ClickerInterrupt)):
                return False
            return True
        return False