import json
import os
from typing import Any, Dict

DEFAULT_SETTINGS = {
    "click_interval": 0.1,
    "button": "left",
    "failsafe": True,
    "hotkey": "f6",
    "repeat": 0
}

class ConfigManager:
    def __init__(self, path: str = "config.json"):
        self.path = path
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._save(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_SETTINGS

    def _save(self, data: Dict[str, Any]) -> None:
        try:
            with open(self.path, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Storage failure: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def update(self, key: str, value: Any) -> None:
        self.settings[key] = value
        self._save(self.settings)