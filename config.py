import json
import os
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "click_interval_ms": 100,
    "mouse_button": "left",
    "hotkey": "f8",
    "clicks_per_trigger": 1,
    "random_delay_range_ms": (0, 15),
    "fail_safe_enabled": True
}

class MagicConfig(dict):
    """Dictionary subclass allowing attribute access and autosave on change."""
    def __init__(self, filepath: str = "clicker_config.json"):
        super().__init__(DEFAULT_CONFIG)
        self._filepath = filepath
        self.load()

    def load(self) -> None:
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.update_safely(data)
            except (json.JSONDecodeError, IOError):
                self.save()
        else:
            self.save()

    def update_safely(self, incoming: dict) -> None:
        for key, val in incoming.items():
            if key in DEFAULT_CONFIG:
                expected_type = type(DEFAULT_CONFIG[key])
                if expected_type is tuple and isinstance(val, list):
                    self[key] = tuple(val)
                else:
                    try:
                        self[key] = expected_type(val)
                    except (ValueError, TypeError):
                        pass

    def save(self) -> None:
        try:
            with open(self._filepath, 'w', encoding='utf-8') as f:
                json.dump(dict(self), f, indent=4)
        except IOError:
            pass

    def __getattr__(self, item: str) -> Any:
        try:
            return self[item]
        except KeyError as err:
            raise AttributeError(f"'MagicConfig' has no attribute '{item}'") from err

    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith('_'):
            super().__setattr__(key, value)
        else:
            self[key] = value
            self.save()