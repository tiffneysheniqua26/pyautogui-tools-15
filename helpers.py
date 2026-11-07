import struct
from dataclasses import dataclass
from typing import Iterator, List, Tuple


@dataclass
class ClickEvent:
    x: int
    y: int
    delay: float
    button: str = "left"
    clicks: int = 1


class ClickStreamProcessor:
    """Encodes and decodes dense autoclicker event streams into compact binary chunks."""

    _BUTTON_MAP = {"left": 0, "right": 1, "middle": 2}
    _REV_BUTTON_MAP = {v: k for k, v in _BUTTON_MAP.items()}

    def __init__(self, time_precision: int = 1000):
        self.precision = time_precision

    def encode_events(self, events: List[ClickEvent]) -> bytes:
        """Packs a list of ClickEvents into a custom compact byte stream."""
        buffer = bytearray()
        for ev in events:
            scaled_delay = int(ev.delay * self.precision)
            button_code = self._BUTTON_MAP.get(ev.button.lower(), 0)
            packed = struct.pack("<HHIBB", ev.x & 0xFFFF, ev.y & 0xFFFF, scaled_delay, button_code, ev.clicks & 0xFF)
            buffer.extend(packed)
        return bytes(buffer)

    def decode_events(self, raw_data: bytes) -> Iterator[ClickEvent]:
        """Yields ClickEvent instances parsed from binary raw byte data."""
        record_size = struct.calcsize("<HHIBB")
        for offset in range(0, len(raw_data) - record_size + 1, record_size):
            chunk = raw_data[offset:offset + record_size]
            x, y, scaled_delay, button_code, clicks = struct.unpack("<HHIBB", chunk)
            yield ClickEvent(
                x=x,
                y=y,
                delay=scaled_delay / self.precision,
                button=self._REV_BUTTON_MAP.get(button_code, "left"),
                clicks=clicks
            )

    @staticmethod
    def calculate_jitter(events: List[ClickEvent]) -> Tuple[float, float]:
        """Calculates spatial variance across a recording sequence."""
        if not events:
            return (0.0, 0.0)
        avg_x = sum(e.x for e in events) / len(events)
        avg_y = sum(e.y for e in events) / len(events)
        var_x = sum((e.x - avg_x) ** 2 for e in events) / len(events)
        var_y = sum((e.y - avg_y) ** 2 for e in events) / len(events)
        return (var_x ** 0.5, var_y ** 0.5)
