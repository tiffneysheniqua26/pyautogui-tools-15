import random
from dataclasses import dataclass
from typing import Generator, List, Tuple


@dataclass(frozen=True)
class ClickPoint:
    x: int
    y: int
    delay_ms: float
    button: str = "left"


class ClickDataProcessor:
    """Transforms raw coordinate targets into humanized autoclicker execution payloads."""

    def __init__(self, jitter_radius: float = 3.5, curve_steps: int = 5):
        self.jitter_radius = jitter_radius
        self.curve_steps = max(1, curve_steps)

    def _apply_gaussian_offset(self, val: int) -> int:
        return max(0, int(val + random.gauss(0, self.jitter_radius / 2.0)))

    def interpolate_trajectory(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """Generates a Bezier curve trajectory between two coordinates."""
        points = []
        ctrl_x = (start[0] + end[0]) / 2 + random.uniform(-20, 20)
        ctrl_y = (start[1] + end[1]) / 2 + random.uniform(-20, 20)

        for i in range(self.curve_steps + 1):
            t = i / float(self.curve_steps)
            bx = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * ctrl_x + (t**2) * end[0]
            by = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * ctrl_y + (t**2) * end[1]
            points.append((int(bx), int(by)))
        return points

    def process_sequence(
        self, raw_points: List[Tuple[int, int, float]]
    ) -> Generator[ClickPoint, None, None]:
        """Streams jittered click points with variable human-like intervals."""
        for x, y, delay in raw_points:
            jittered_x = self._apply_gaussian_offset(x)
            jittered_y = self._apply_gaussian_offset(y)
            human_delay = max(0.01, delay + random.uniform(-0.02, 0.05))
            yield ClickPoint(
                x=jittered_x,
                y=jittered_y,
                delay_ms=round(human_delay * 1000, 2),
                button="left",
            )


def batch_encode_clicks(clicks: List[ClickPoint]) -> bytes:
    """Encodes click targets into a packed binary payload for fast replay."""
    payload = bytearray(b"AUTOCLICK_V1")
    for c in clicks:
        btn_code = 1 if c.button == "left" else 2
        payload.extend(
            int(c.x).to_bytes(2, "big")
            + int(c.y).to_bytes(2, "big")
            + int(c.delay_ms).to_bytes(4, "big")
            + btn_code.to_bytes(1, "big")
        )
    return bytes(payload)
