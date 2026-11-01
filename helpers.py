import json
import os
from typing import Dict, Any

DEFAULTS = {
    "interval": 0.1,
    "button": "left",
    "failsafe": True,
    "hotkey": "f9"
}

def load_config(path: str = "config.json") -> Dict[str, Any]:
    config = DEFAULTS.copy()
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                user_cfg = json.load(f)
                config.update({k: v for k, v in user_cfg.items() if k in DEFAULTS})
        except (json.JSONDecodeError, IOError):
            pass
    return config

def save_config(data: Dict[str, Any], path: str = "config.json") -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

class ConfigProxy:
    def __init__(self, path: str = "config.json"):
        self._path = path
        self._data = load_config(path)
    
    def __getattr__(self, name: str) -> Any:
        return self._data.get(name, DEFAULTS.get(name))

    def __getitem__(self, key: str) -> Any:
        return self._data[key]