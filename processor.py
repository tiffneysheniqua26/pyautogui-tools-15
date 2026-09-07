import random
import time
from typing import List, Tuple, Generator, Dict, Any

class ClickSequenceProcessor:
    """Processes click coordinate streams with randomized timing jitter."""
    def __init__(self, base_delay: float = 0.1, jitter_factor: float = 0.05):
        self.base_delay = base_delay
        self.jitter_factor = jitter_factor

    def add_jitter(self, delay: float) -> float:
        variation = random.uniform(-self.jitter_factor, self.jitter_factor)
        return max(0.01, delay + variation)

    def process_targets(self, targets: List[Tuple[int, int]]) -> Generator[Dict[str, Any], None, None]:
        for idx, (x, y) in enumerate(targets):
            delay = self.add_jitter(self.base_delay)
            yield {
                "sequence_id": idx + 1,
                "x": x,
                "y": y,
                "delay_after": round(delay, 4),
                "timestamp": round(time.time(), 2)
            }

    def filter_out_of_bounds(self, targets: List[Tuple[int, int]], screen_size: Tuple[int, int]) -> List[Tuple[int, int]]:
        max_x, max_y = screen_size
        return [(x, y) for x, y in targets if 0 <= x <= max_x and 0 <= y <= max_y]
