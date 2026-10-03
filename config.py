import json
import os
from pathlib import Path

DEFAULT_SETTINGS = {
    "interval": 0.1,
    "button": "left",
    "failsafe": True,
    "hotkey": "f9"
}

def load_config(path: str = "config.json") -> dict:
    config_path = Path(path)
    if not config_path.exists():
        try:
            with open(config_path, 'w') as f:
                json.dump(DEFAULT_SETTINGS, f, indent=4)
        except (IOError, PermissionError):
            return DEFAULT_SETTINGS
        return DEFAULT_SETTINGS

    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            return {**DEFAULT_SETTINGS, **data}
    except (json.JSONDecodeError, KeyError):
        return DEFAULT_SETTINGS

def save_config(data: dict, path: str = "config.json"):
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        pass