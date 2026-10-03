import json
import os
from typing import Dict, Any

DEFAULT_CONFIG = {
    "interval": 0.1,
    "button": "left",
    "failsafe": True,
    "hotkey": "f9"
}

def load_config(filepath: str = "config.json") -> Dict[str, Any]:
    try:
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            return DEFAULT_CONFIG
        
        with open(filepath, "r") as f:
            user_config = json.load(f)
            
        return {**DEFAULT_CONFIG, **user_config}
    except (IOError, json.JSONDecodeError):
        return DEFAULT_CONFIG

def validate_interval(value: Any) -> float:
    try:
        interval = float(value)
        return max(0.01, interval)
    except (ValueError, TypeError):
        return DEFAULT_CONFIG["interval"]

def validate_button(value: Any) -> str:
    allowed = ("left", "right", "middle")
    return str(value).lower() if str(value).lower() in allowed else DEFAULT_CONFIG["button"]