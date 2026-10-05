import functools
import time

class ClickOptimizer:
    def __init__(self, cache_size=1024):
        self._cache = {}
        self._limit = cache_size
        self._hits = 0

    def fast_throttle(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in self._cache and (now - self._cache[key][1]) < 0.01:
                self._hits += 1
                return self._cache[key][0]
            
            result = func(*args, **kwargs)
            
            if len(self._cache) > self._limit:
                self._cache.clear()
            
            self._cache[key] = (result, now)
            return result
        return wrapper

optimizer = ClickOptimizer()

def validate_coordinate(func):
    @optimizer.fast_throttle
    @functools.wraps(func)
    def checker(x, y):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            raise ValueError("coordinates must be numeric")
        return func(x, y)
    return checker

@validate_coordinate
def secure_click_coords(x, y):
    return (float(x), float(y))