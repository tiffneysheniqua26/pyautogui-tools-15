import json
import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "click_interval": 0.1,
    "button": "left",
    "failsafe": True,
    "log_level": "INFO",
    "max_clicks": 1000
}

class ConfigLoader:
    def __init__(self, filepath: str = "config.json"):
        self.filepath = filepath

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.filepath):
            self._save(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                return {**DEFAULT_CONFIG, **data}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG

    def _save(self, data: Dict[str, Any]) -> None:
        try:
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Config save failure: {e}")

def get_app_config() -> Dict[str, Any]:
    loader = ConfigLoader()
    return loader.load()