import time
import random
import math
from typing import Generator, Tuple, Callable
from functools import wraps


def humanized_delay(base_interval: float, variance: float = 0.2) -> Generator[float, None, None]:
    """Generator producing human-like click delays using skewed normal distribution."""
    while True:
        u1 = random.random() or 1e-10
        u2 = random.random()
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        delay = max(0.001, base_interval + (z * variance * base_interval))
        yield delay


def jitter_point(point: Tuple[int, int], radius: int = 3) -> Tuple[int, int]:
    """Applies non-uniform radial jitter to a target coordinate tuple."""
    angle = random.uniform(0, 2 * math.pi)
    distance = random.triangular(0, radius, radius * 0.3)
    dx = int(round(distance * math.cos(angle)))
    dy = int(round(distance * math.sin(angle)))
    return (point[0] + dx, point[1] + dy)


def click_burst(count: int, cps: float) -> Callable:
    """Decorator to turn any click callback into a paced burst execution."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            interval = 1.0 / max(cps, 0.1)
            jitter_gen = humanized_delay(interval, variance=0.15)
            results = []
            for _ in range(count):
                start = time.perf_counter()
                results.append(func(*args, **kwargs))
                elapsed = time.perf_counter() - start
                target_delay = next(jitter_gen)
                time.sleep(max(0.0, target_delay - elapsed))
            return results
        return wrapper
    return decorator


def clamp_to_screen(x: int, y: int, bounds: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """Clamps (x, y) coordinates within specified screen bounds (min_x, min_y, max_x, max_y)."""
    min_x, min_y, max_x, max_y = bounds
    return (max(min_x, min(x, max_x)), max(min_y, min(y, max_y)))
