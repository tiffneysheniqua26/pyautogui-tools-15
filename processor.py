import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_path: str = "settings.json"):
        self.path = config_path
        self.defaults = {
            "interval": 0.1,
            "clicks": 1,
            "button": "left",
            "jitter": False
        }

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._write_defaults()
            return self.defaults
        
        try:
            with open(self.path, "r") as f:
                user_cfg = json.load(f)
                return {**self.defaults, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def _write_defaults(self):
        try:
            with open(self.path, "w") as f:
                json.dump(self.defaults, f, indent=4)
        except IOError:
            pass

    def sync_config(self, new_data: Dict[str, Any]):
        current = self.load_config()
        current.update(new_data)
        with open(self.path, "w") as f:
            json.dump(current, f, indent=4)

config_loader = ConfigManager()