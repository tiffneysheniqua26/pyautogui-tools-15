import math
import random
from typing import Tuple, Generator


def bezier_jitter(start: Tuple[int, int], end: Tuple[int, int], steps: int = 10) -> Generator[Tuple[int, int], None, None]:
    """Generates micro-movements along a randomized curve simulating human hand tremor."""
    x0, y0 = start
    x3, y3 = end
    dist = math.hypot(x3 - x0, y3 - y0)
    ctrl_offset = dist * 0.2
    x1 = x0 + (x3 - x0) * 0.3 + random.uniform(-ctrl_offset, ctrl_offset)
    y1 = y0 + (y3 - y0) * 0.3 + random.uniform(-ctrl_offset, ctrl_offset)
    x2 = x0 + (x3 - x0) * 0.7 + random.uniform(-ctrl_offset, ctrl_offset)
    y2 = y0 + (y3 - y0) * 0.7 + random.uniform(-ctrl_offset, ctrl_offset)

    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t ** 2 * x2 + t ** 3 * x3
        y = (1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3 * y3
        yield round(x), round(y)


def humanized_delay_stream(target_cps: float, burst_probability: float = 0.05) -> Generator[float, None, None]:
    """Yields sleep intervals modeled after human clicking fatigue and micro-bursts."""
    base_delay = 1.0 / max(target_cps, 0.1)
    while True:
        delay = random.gauss(base_delay, base_delay * 0.25)
        if random.random() < burst_probability:
            delay *= random.choice([0.3, 2.5])
        yield max(0.005, delay)


def area_weighted_point(box: Tuple[int, int, int, int], center_sigma: float = 0.25) -> Tuple[int, int]:
    """Returns coordinate inside bounding box (x1, y1, x2, y2) with normal distribution toward center."""
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    width_std = (x2 - x1) * center_sigma
    height_std = (y2 - y1) * center_sigma

    px = int(min(max(random.gauss(cx, width_std), x1), x2))
    py = int(min(max(random.gauss(cy, height_std), y1), y2))
    return px, py
