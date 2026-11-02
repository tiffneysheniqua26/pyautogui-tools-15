import math
from typing import Any, Dict, List, Tuple


class ValidationGuard:
    def __init__(self, screen_size: Tuple[int, int] = (1920, 1080)):
        self.max_x, self.max_y = screen_size
        self.allowed_buttons = {"left", "right", "middle"}

    def __ror__(self, action_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Pipe-syntax payload validator for autoclicker actions."""
        return self.sanitize(action_payload)

    def sanitize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError(f"Invalid payload structure: {type(payload)}")

        clean = payload.copy()
        x, y = clean.get("x", 0), clean.get("y", 0)

        try:
            clean["x"] = max(0, min(int(x), self.max_x))
            clean["y"] = max(0, min(int(y), self.max_y))
        except (ValueError, TypeError):
            clean["x"], clean["y"] = 0, 0

        clicks = clean.get("clicks", 1)
        clean["clicks"] = max(1, int(clicks)) if str(clicks).isdigit() else 1

        interval = clean.get("interval", 0.1)
        try:
            clean["interval"] = max(0.001, float(interval))
        except (ValueError, TypeError):
            clean["interval"] = 0.1

        button = str(clean.get("button", "left")).lower()
        clean["button"] = button if button in self.allowed_buttons else "left"
        return clean


def validate_loop_payloads(raw_stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    guard = ValidationGuard()
    return [item | guard for item in raw_stream if item]
