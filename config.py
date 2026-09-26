import json
import os
from typing import Dict, Any

DEFAULT_CONFIG = {
    "interval": 0.1,
    "button": "left",
    "failsafe": True,
    "hotkey": "f6"
}

class ConfigLoader:
    def __init__(self, path: str = "settings.json"):
        self.path = path

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._write_defaults()
            return DEFAULT_CONFIG
        try:
            with open(self.path, "r") as f:
                user_cfg = json.load(f)
                return {**DEFAULT_CONFIG, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG

    def _write_defaults(self) -> None:
        try:
            with open(self.path, "w") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
        except IOError:
            pass

    def __getitem__(self, key: str) -> Any:
        return self.load().get(key, DEFAULT_CONFIG.get(key))

config = ConfigLoader()