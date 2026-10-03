import json
import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "interval": 0.01,
    "button": "left",
    "failsafe": True,
    "hotkey": "f6"
}

class ConfigLoader:
    def __init__(self, path: str = "settings.json"):
        self.path = path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._save(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        try:
            with open(self.path, "r") as f:
                loaded = json.load(f)
            return {**DEFAULT_CONFIG, **loaded}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def get(self, key: str) -> Any:
        return self.data.get(key, DEFAULT_CONFIG.get(key))

settings = ConfigLoader()