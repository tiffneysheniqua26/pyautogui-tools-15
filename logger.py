import os
import time
from typing import Generator, List, Tuple


class ClickTelemetryLogger:
    """Space-efficient log handler compressing continuous static autoclick coordinates."""

    def __init__(self, log_path: str = "autoclick_events.telemetry"):
        self.log_path = log_path
        self._cache: List[Tuple[int, int, float]] = []

    def record(self, x: int, y: int) -> None:
        """Records click coordinates into memory cache, flushing every 5 events."""
        self._cache.append((x, y, time.time()))
        if len(self._cache) >= 5:
            self.write_out()

    def write_out(self) -> None:
        """Encodes identical coordinate bursts to reduce log size."""
        if not self._cache:
            return

        encoded_blocks: List[str] = []
        anchor_x, anchor_y, anchor_t = self._cache[0]
        count = 1

        for x, y, t in self._cache[1:]:
            if x == anchor_x and y == anchor_y:
                count += 1
            else:
                encoded_blocks.append(f"{anchor_x},{anchor_y}*{count}@{anchor_t:.2f}")
                anchor_x, anchor_y, anchor_t = x, y, t
                count = 1
        encoded_blocks.append(f"{anchor_x},{anchor_y}*{count}@{anchor_t:.2f}")

        with open(self.log_path, "a", encoding="utf-8") as file_stream:
            file_stream.write(":".join(encoded_blocks) + "\n")

        self._cache.clear()

    def parse_events(self) -> Generator[Tuple[int, int, int, float], None, None]:
        """Reconstructs logged actions mapping back coordinates, counts, and stamps."""
        if not os.path.exists(self.log_path):
            return
        with open(self.log_path, "r", encoding="utf-8") as file_stream:
            for row in file_stream:
                cleaned = row.strip()
                if not cleaned:
                    continue
                for element in cleaned.split(":"):
                    if "@" in element and "*" in element:
                        spatial, timestamp = element.split("@")
                        coords, count = spatial.split("*")
                        cx, cy = map(int, coords.split(","))
                        yield cx, cy, int(count), float(timestamp)