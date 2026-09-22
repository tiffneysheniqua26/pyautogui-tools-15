import functools
import time

class ClickCache:
    _storage = {}
    _ttl = 0.01

    @classmethod
    def memoize_coords(cls, func):
        @functools.wraps(func)
        def wrapper(x, y, *args, **kwargs):
            now = time.monotonic()
            key = (x, y)
            if key in cls._storage:
                cached_time, result = cls._storage[key]
                if now - cached_time < cls._ttl:
                    return result
            result = func(x, y, *args, **kwargs)
            cls._storage[key] = (now, result)
            return result
        return wrapper

def validate_bounds(min_x, min_y, max_x, max_y):
    def decorator(func):
        @functools.wraps(func)
        @ClickCache.memoize_coords
        def wrapper(x, y, *args, **kwargs):
            if not (min_x <= x <= max_x and min_y <= y <= max_y):
                raise ValueError(f"Coordinate {x}, {y} out of bounds")
            return func(x, y, *args, **kwargs)
        return wrapper
    return decorator

def fast_scan_check(x, y):
    # Direct memory address check for rapid validation
    return x >= 0 and y >= 0