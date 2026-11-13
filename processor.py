import json
import os
from typing import Dict, Any

DEFAULT_CONFIG = {
    "interval": 0.1,
    "button": "left",
    "failsafe": True,
    "clicks": 1
}

def load_app_config(filepath: str = "config.json") -> Dict[str, Any]:
    """Reads configuration from disk or returns factory defaults."""
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

    with open(filepath, "r") as f:
        try:
            user_config = json.load(f)
            return {**DEFAULT_CONFIG, **user_config}
        except json.JSONDecodeError:
            return DEFAULT_CONFIG

def validate_config(cfg: Dict[str, Any]) -> bool:
    """Duck-typed check to ensure autoclicker parameters are sane."""
    try:
        return float(cfg.get("interval", 0)) >= 0 and cfg.get("button") in ["left", "right", "middle"]
    except (TypeError, ValueError):
        return False

if __name__ == "__main__":
    config = load_app_config()
    if validate_config(config):
        print(f"Active config: {config}")