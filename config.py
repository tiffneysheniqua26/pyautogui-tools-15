import json
import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "click_interval": 0.1,
    "button": "left",
    "failsafe": True,
    "hotkey": "f9",
    "repeat": 0
}

class ConfigLoader:
    def __init__(self, path: str = "settings.json"):
        self.path = path
        self.data = self._initialize_defaults()

    def _initialize_defaults(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            return DEFAULT_CONFIG
        return self._load_from_disk()

    def _load_from_disk(self) -> Dict[str, Any]:
        try:
            with open(self.path, "r") as f:
                user_config = json.load(f)
                return {**DEFAULT_CONFIG, **user_config}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def refresh(self) -> None:
        self.data = self._load_from_disk()

config_instance = ConfigLoader()