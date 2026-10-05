import json
import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "interval": 0.1,
    "button": "left",
    "safety_stop": True,
    "max_clicks": 1000
}

class ConfigManager:
    def __init__(self, path: str = "config.json"):
        self.path = path
        self.settings = DEFAULT_CONFIG.copy()
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
            except (json.JSONDecodeError, IOError):
                self._save_defaults()
        else:
            self._save_defaults()

    def _save_defaults(self) -> None:
        try:
            with open(self.path, "w") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
        except IOError:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def __getattr__(self, item: str) -> Any:
        return self.settings.get(item)

if __name__ == "__main__":
    cfg = ConfigManager()
    print(f"Active interval: {cfg.interval}")