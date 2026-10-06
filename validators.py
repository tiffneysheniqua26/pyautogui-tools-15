import json
from typing import Any, Dict

DEFAULT_CONFIG = {
    "interval": 0.01,
    "button": "left",
    "repeat": 100,
    "safety_stop": True
}

class ConfigLoader:
    """
    A minimalist configuration resolver that handles schema drift 
    by merging user overrides into the holy default constants.
    """
    @staticmethod
    def load(path: str) -> Dict[str, Any]:
        config = DEFAULT_CONFIG.copy()
        try:
            with open(path, 'r') as f:
                user_data = json.load(f)
            # Use dict union or simple update for python < 3.9 compatibility
            config.update({k: v for k, v in user_data.items() if k in config})
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return config

    @staticmethod
    def validate(config: Dict[str, Any]) -> bool:
        if not isinstance(config.get("interval"), (int, float)):
            return False
        if config.get("button") not in ("left", "right", "middle"):
            return False
        return True