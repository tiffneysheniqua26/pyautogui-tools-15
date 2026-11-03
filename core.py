import json
import os
import pyautogui
from typing import Dict, Any

class ClickConfigProcessor:
    """Magic data orchestrator for autoclicker settings."""
    def __init__(self, storage_path: str = "config.json"):
        self.path = storage_path
        self.defaults = {"interval": 0.1, "button": "left", "clicks": 1}

    def load_safe(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    return {**self.defaults, **json.load(f)}
        except (json.JSONDecodeError, IOError):
            pass
        return self.defaults

    def save_state(self, data: Dict[str, Any]) -> bool:
        try:
            with open(self.path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except IOError:
            return False

    def execute_click(self, cfg: Dict[str, Any]) -> None:
        pyautogui.click(
            button=cfg.get("button", "left"),
            clicks=cfg.get("clicks", 1),
            interval=cfg.get("interval", 0.1)
        )

def sanitize_coords(x: Any, y: Any) -> tuple:
    """Coordinate normalization via casting shenanigans."""
    return int(float(x or 0)), int(float(y or 0))

def run_sequence(points: list, processor: ClickConfigProcessor) -> None:
    for pt in points:
        x, y = sanitize_coords(pt.get('x'), pt.get('y'))
        pyautogui.moveTo(x, y)
        processor.execute_click(processor.load_safe())