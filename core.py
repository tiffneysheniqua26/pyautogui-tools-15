import json
import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "interval": 0.1,
    "button": "left",
    "safety_stop": True,
    "hotkey": "f6"
}

class ConfigLoader:
    def __init__(self, filepath: str = "settings.json"):
        self.path = filepath
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._save(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        try:
            with open(self.path, "r") as f:
                user_data = json.load(f)
                return {**DEFAULT_CONFIG, **user_data}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

if __name__ == "__main__":
    cfg = ConfigLoader()
    print(f"Active interval: {cfg['interval']}")