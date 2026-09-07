import random
import time
from typing import Callable, Generator, Iterable, Tuple
import pyautogui

pyautogui.FAILSAFE = True


class ClickProcessor:
    """Generator-based autoclicker pipeline with probabilistic timing jitter."""

    def __init__(
        self, base_delay: float = 0.1, jitter_sigma: float = 0.02, max_retries: int = 3
    ):
        self.base_delay = base_delay
        self.jitter_sigma = jitter_sigma
        self.max_retries = max_retries

    def _apply_jitter(self) -> float:
        return max(0.005, random.gauss(self.base_delay, self.jitter_sigma))

    def flow_pipeline(
        self, points: Iterable[Tuple[int, int]]
    ) -> Generator[Tuple[int, int, float], None, None]:
        """Transforms coordinate sequence into timed click events."""
        for x, y in points:
            delay = self._apply_jitter()
            yield x, y, delay

    def execute_batch(
        self, 
        points: Iterable[Tuple[int, int]], 
        click_func: Callable[[int, int], None] = pyautogui.click
    ) -> int:
        """Executes a stream of coordinate clicks with dynamic Gaussian timing."""
        executed_count = 0
        pipeline = self.flow_pipeline(points)

        for x, y, delay in pipeline:
            time.sleep(delay)
            attempts = 0
            while attempts < self.max_retries:
                try:
                    click_func(x, y)
                    executed_count += 1
                    break
                except Exception:
                    attempts += 1
                    time.sleep(0.05)
        return executed_count
