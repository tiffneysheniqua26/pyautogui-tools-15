import random
from typing import Generator, Tuple, List

Coordinate = Tuple[int, int]
TargetDelayPair = Tuple[Coordinate, float]

class ClickingPathProcessor:
    """
    A processor that generates click paths with organic human-like micro-jitters.

    Transforms strict coordinate pathways into slightly randomized coordinates
    and interval delays to mimic organic manual interactions, bypassing basic
    bot-detection patterns during pyautogui automation cycles.
    """

    def __init__(self, raw_points: List[Coordinate], base_delay: float = 0.1) -> None:
        """
        Initialize the path processor with designated targets and baseline delay.

        :param raw_points: A list of exact (x, y) coordinates to click.
        :param base_delay: Minimum sleep duration (in seconds) between calculated actions.
        """
        self.raw_points: List[Coordinate] = raw_points
        self.base_delay: float = base_delay

    def humanized_stream(self, jitter_radius: int = 3) -> Generator[TargetDelayPair, None, None]:
        """
        Generate coordinates altered by a slight, randomized Gaussian shift.

        Yields pairs containing the perturbed (x, y) coordinate pair and the
        fluctuating timing interval for the pyautogui driver to consume.

        :param jitter_radius: Standard deviation limit of the Gaussian distribution offset.
        :return: Generator yielding tuple of shifted (X, Y) and float sleep time.
        """
        for x, y in self.raw_points:
            radius = random.gauss(0, jitter_radius)
            angle = random.uniform(0, 6.28318)

            # Introduce slight organic skew on the target offsets
            jitter_x = int(round(x + radius * abs(angle - 3.14159)))
            jitter_y = int(round(y + radius * abs(angle - 1.57079)))

            # Add varying hesitation times targeting a non-linear decay distribution
            human_hesitation = abs(random.normalvariate(0.0, self.base_delay * 0.25))
            current_delay = max(0.01, self.base_delay + human_hesitation)

            yield (jitter_x, jitter_y), current_delay