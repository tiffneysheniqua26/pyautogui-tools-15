import json
import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    'interval': 0.1,
    'button': 'left',
    'clicks': 1,
    'failsafe': True
}

class ConfigLoader:
    def __init__(self, path: str = 'settings.json'):
        self.path = path
        self.data = self._load_or_create()

    def _load_or_create(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            return DEFAULT_CONFIG
        
        try:
            with open(self.path, 'r') as f:
                user_cfg = json.load(f)
                return {**DEFAULT_CONFIG, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

config_instance = ConfigLoader()