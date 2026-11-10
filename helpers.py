import random
import time
from typing import Generator, List, Tuple


def generate_human_path(
    start: Tuple[int, int], end: Tuple[int, int], steps: int = 15
) -> Generator[Tuple[int, int], None, None]:
    """Generates non-linear trajectory coordinates with organic micro-jitter."""
    x1, y1 = start
    x2, y2 = end

    cx = (x1 + x2) / 2.0 + random.randint(-35, 35)
    cy = (y1 + y2) / 2.0 + random.randint(-35, 35)

    for i in range(steps + 1):
        t = i / float(steps)
        x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t**2 * x2
        y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t**2 * y2

        jitter_x = random.uniform(-1.2, 1.2) if 0 < i < steps else 0.0
        jitter_y = random.uniform(-1.2, 1.2) if 0 < i < steps else 0.0

        yield int(round(x + jitter_x)), int(round(y + jitter_y))


def organic_delay(base_ms: float, jitter_ratio: float = 0.25) -> None:
    """Executes micro-sleep using Gaussian distribution to simulate human behavior."""
    sigma = max(1.0, (base_ms * jitter_ratio) / 3.0)
    delay_ms = max(2.0, random.gauss(base_ms, sigma))
    time.sleep(delay_ms / 1000.0)


def calculate_cps(click_timestamps: List[float], sample_size: int = 10) -> float:
    """Calculates moving clicks-per-second rate over recent execution history."""
    recent = click_timestamps[-sample_size:]
    if len(recent) < 2:
        return 0.0
    time_span = recent[-1] - recent[0]
    return (len(recent) - 1) / time_span if time_span > 0 else 0.0
