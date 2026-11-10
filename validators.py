"""Validation pipeline for autoclicker target coordinates and click options."""

from typing import Any, Dict, Sequence, Union


class ClickTargetValidator:
    """Fluent validator for mouse click coordinates and trigger options."""

    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value

    def must_be_numeric(self, min_val: float = 0, max_val: float = float("inf")) -> "ClickTargetValidator":
        if not isinstance(self.value, (int, float)) or isinstance(self.value, bool):
            raise TypeError(f"Parameter '{self.key}' must be numeric, got {type(self.value).__name__}")
        if not (min_val <= self.value <= max_val):
            raise ValueError(f"Parameter '{self.key}' value {self.value} outside bound [{min_val}, {max_val}]")
        return self

    def must_be_in(self, allowed: Sequence[Any]) -> "ClickTargetValidator":
        if self.value not in allowed:
            raise ValueError(f"Parameter '{self.key}' must be one of {allowed}, got '{self.value}'")
        return self


def sanitize_click_params(x: int, y: int, button: str = "left", delay: float = 0.1, clicks: int = 1) -> Dict[str, Union[int, float, str]]:
    """Clean and validate raw execution settings for autoclicker dispatch."""
    val_x = ClickTargetValidator("x", x).must_be_numeric(0, 15360).value
    val_y = ClickTargetValidator("y", y).must_be_numeric(0, 8640).value
    btn = ClickTargetValidator("button", button).must_be_in(["left", "right", "middle"]).value
    delay_val = ClickTargetValidator("delay", delay).must_be_numeric(0.001, 3600.0).value
    count = ClickTargetValidator("clicks", clicks).must_be_numeric(1, 100000).value

    return {
        "x": int(val_x),
        "y": int(val_y),
        "button": str(btn),
        "delay": float(delay_val),
        "clicks": int(count),
    }
