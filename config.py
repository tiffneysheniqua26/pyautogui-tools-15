import json
import os
from typing import Any, Dict


class _ConfigDescriptor:
    def __init__(self, key: str, default: Any, cast_type: type):
        self.key = key
        self.default = default
        self.cast_type = cast_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        raw_val = instance._data.get(self.key, self.default)
        try:
            return self.cast_type(raw_val)
        except (ValueError, TypeError):
            return self.default

    def __set__(self, instance, value):
        instance._data[self.key] = self.cast_type(value)


class ClickerConfig:
    clicks_per_second = _ConfigDescriptor("cps", 10.0, float)
    target_button = _ConfigDescriptor("button", "left", str)
    hold_duration = _ConfigDescriptor("hold", 0.0, float)
    hotkey = _ConfigDescriptor("hotkey", "f6", str)
    max_clicks = _ConfigDescriptor("max_clicks", 0, int)

    def __init__(self, filepath: str = "autoclicker_config.json"):
        self.filepath = filepath
        self._data: Dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        self._data.clear()
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        self._data = loaded
            except (json.JSONDecodeError, IOError):
                pass

    def export_sanitized(self) -> Dict[str, Any]:
        valid_buttons = ("left", "right", "middle")
        btn = self.target_button.lower()
        return {
            "cps": max(0.1, min(self.clicks_per_second, 1000.0)),
            "button": btn if btn in valid_buttons else "left",
            "hold": max(0.0, self.hold_duration),
            "hotkey": self.hotkey.lower(),
            "max_clicks": max(0, self.max_clicks),
        }

    def save(self) -> bool:
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.export_sanitized(), f, indent=2)
            return True
        except IOError:
            return False
