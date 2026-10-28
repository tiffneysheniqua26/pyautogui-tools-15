import math
import time
from typing import Generator, Callable, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class PacingCadence:
    """Calculates dynamic inter-click delays using harmonic oscillation to emulate human jitter."""
    base_interval: float = 0.1
    variance: float = 0.02
    frequency: float = 0.5
    _step: int = field(default=0, init=False, repr=False)

    def __iter__(self) -> Generator[float, None, None]:
        """Yields continuous variable delay times based on a sine wave transformation."""
        while True:
            jitter = math.sin(self._step * self.frequency) * self.variance
            yield max(0.001, self.base_interval + jitter)
            self._step += 1

class ClickSequenceEngine:
    """Orchestrates clicking cadences with customizable trigger callbacks and dynamic pacing."""

    def __init__(
        self,
        action_callback: Callable[[int, int], None],
        cadence: Optional[PacingCadence] = None
    ) -> None:
        """Initialize the engine with a targeting callback and delay cadence generator."""
        self.action_callback: Callable[[int, int], None] = action_callback
        self.cadence: PacingCadence = cadence or PacingCadence()
        self._active: bool = False

    def execute_burst(
        self,
        coordinates: Tuple[int, int],
        clicks: int = 10
    ) -> int:
        """Executes a fixed series of clicks with oscillating intervals over the target position."""
        self._active = True
        performed: int = 0
        cadence_gen = iter(self.cadence)

        for _ in range(clicks):
            if not self._active:
                break
            x, y = coordinates
            self.action_callback(x, y)
            performed += 1
            delay: float = next(cadence_gen)
            time.sleep(delay)

        self._active = False
        return performed

    def stop(self) -> None:
        """Signals the current burst execution sequence to abort gracefully."""
        self._active = False
