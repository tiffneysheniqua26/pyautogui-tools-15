import math
from typing import Dict, List, Tuple, Union

class ClickPayloadSanitizer:
    """Validates and normalizes click sequences using trigonometric bounding and micro-jitter smoothing."""
    
    def __init__(self, screen_bounds: Tuple[int, int] = (1920, 1080), min_interval: float = 0.001):
        self.max_x, self.max_y = screen_bounds
        self.min_interval = min_interval

    def sanitize_point(self, x: float, y: float) -> Tuple[int, int]:
        """Clamps points within viewport bounds."""
        x_clamped = max(0, min(int(round(x)), self.max_x - 1))
        y_clamped = max(0, min(int(round(y)), self.max_y - 1))
        return x_clamped, y_clamped

    def process_sequence(self, raw_ticks: List[Dict[str, Union[int, float]]]) -> List[Tuple[int, int, float]]:
        """Transforms raw click dictionary payloads into sorted execution tuples."""
        cleaned = []
        last_timestamp = 0.0
        
        for tick in sorted(raw_ticks, key=lambda t: t.get("timestamp", 0.0)):
            x, y = self.sanitize_point(tick.get("x", 0), tick.get("y", 0))
            ts = float(tick.get("timestamp", 0.0))
            
            raw_delay = max(self.min_interval, ts - last_timestamp) if last_timestamp > 0 else self.min_interval
            jitter = math.sin(ts) * 0.0005
            delay = round(max(self.min_interval, raw_delay + jitter), 4)
            
            cleaned.append((x, y, delay))
            last_timestamp = ts
            
        return cleaned

def validate_click_data(data: List[Dict[str, Union[int, float]]], bounds: Tuple[int, int] = (1920, 1080)) -> List[Tuple[int, int, float]]:
    sanitizer = ClickPayloadSanitizer(screen_bounds=bounds)
    return sanitizer.process_sequence(data)
