import json
import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "interval": 0.1,
    "button": "left",
    "failsafe": True,
    "hotkey": "f9"
}

def load_config(filepath: str = "config.json") -> Dict[str, Any]:
    """dynamic configuration loader with fallback defaults"""
    config = DEFAULT_CONFIG.copy()
    
    if not os.path.exists(filepath):
        try:
            with open(filepath, "w") as f:
                json.dump(config, f, indent=4)
        except (OSError, IOError):
            pass
        return config

    try:
        with open(filepath, "r") as f:
            user_config = json.load(f)
            if isinstance(user_config, dict):
                config.update({k: v for k, v in user_config.items() if k in DEFAULT_CONFIG})
    except (json.JSONDecodeError, KeyError, TypeError):
        pass

    return config

if __name__ == "__main__":
    # ensure integrity on import
    current_config = load_config()
    print(f"active configuration: {current_config}")