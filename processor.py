import math
import random
import time
from typing import Callable, Generator, List, Tuple

Point = Tuple[int, int]

class ClickProcessor:
    """Streamlined autoclick execution pipeline with procedural micro-jitter."""

    def __init__(self, base_delay: float = 0.05, variance: float = 0.01):
        self.base_delay = max(0.001, base_delay)
        self.variance = variance
        self._hooks: List[Callable[[Point], None]] = []

    def register_hook(self, hook: Callable[[Point], None]) -> None:
        if callable(hook) and hook not in self._hooks:
            self._hooks.append(hook)

    def gaussian_jitter(self, point: Point, radius: float = 3.0) -> Point:
        x, y = point
        dx = random.gauss(0, radius / 2)
        dy = random.gauss(0, radius / 2)
        return int(x + dx), int(y + dy)

    def generate_delays(self, count: int) -> Generator[float, None, None]:
        for i in range(count):
            wave = math.sin(i * 0.1) * (self.variance / 2)
            noise = random.uniform(-self.variance, self.variance)
            yield max(0.001, self.base_delay + wave + noise)

    def process_sequence(self, targets: List[Point], repeats: int = 1) -> Generator[Point, None, None]:
        total_clicks = len(targets) * repeats
        delay_gen = self.generate_delays(total_clicks)
        
        for _ in range(repeats):
            for target in targets:
                jittered = self.gaussian_jitter(target)
                for hook in self._hooks:
                    hook(jittered)
                yield jittered
                time.sleep(next(delay_gen))
