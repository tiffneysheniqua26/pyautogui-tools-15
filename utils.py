import math
from collections import namedtuple
from typing import Generator, List, Tuple

ClickEvent = namedtuple("ClickEvent", ["x", "y", "delay", "button"])


def coalesce_click_stream(
    raw_clicks: List[Tuple[int, int, float, str]], jitter_threshold: float = 5.0
) -> Generator[ClickEvent, None, None]:
    """Filters and aggregates rapid micro-movements and redundant clicks.

    Merges sequential coordinates within a spatial jitter threshold into a single
    weighted centroid, combining their delays for stabilized autoclicker simulation.
    """
    if not raw_clicks:
        return

    accumulator_x = 0.0
    accumulator_y = 0.0
    accumulated_delay = 0.0
    current_button = raw_clicks[0][3]
    cluster_size = 0

    for x, y, delay, button in raw_clicks:
        if cluster_size == 0:
            accumulator_x = float(x)
            accumulator_y = float(y)
            accumulated_delay = delay
            current_button = button
            cluster_size = 1
            continue

        centroid_x = accumulator_x / cluster_size
        centroid_y = accumulator_y / cluster_size
        distance = math.hypot(x - centroid_x, y - centroid_y)

        if distance <= jitter_threshold and button == current_button:
            accumulator_x += x
            accumulator_y += y
            accumulated_delay += delay
            cluster_size += 1
        else:
            yield ClickEvent(
                x=int(round(centroid_x)),
                y=int(round(centroid_y)),
                delay=round(accumulated_delay, 4),
                button=current_button,
            )
            accumulator_x = float(x)
            accumulator_y = float(y)
            accumulated_delay = delay
            current_button = button
            cluster_size = 1

    if cluster_size > 0:
        yield ClickEvent(
            x=int(round(accumulator_x / cluster_size)),
            y=int(round(accumulator_y / cluster_size)),
            delay=round(accumulated_delay, 4),
            button=current_button,
        )
