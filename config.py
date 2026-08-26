import json
import os
from typing import Dict, Any

DEFAULT_CONFIG: Dict[str, Any] = {
    "clicks_per_second": 10.0,
    "button": "left",
    "hold_time": 0.01,
    "hotkey": "f6",
    "safe_failsafe": True,
    "jitter_px": 2
}

class ConfigLoader:
    def __init__(self, filepath: str = "autoclicker_config.json") -> None:
        self.filepath = filepath
        self.settings = self._load_with_magic()

    def _load_with_magic(self) -> Dict[str, Any]:
        config = DEFAULT_CONFIG.copy()
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                    config.update({k: v for k, v in user_data.items() if k in DEFAULT_CONFIG})
            except (json.JSONDecodeError, IOError):
                pass
        return config

    def get(self, key: str) -> Any:
        return self.settings.get(key, DEFAULT_CONFIG.get(key))

    def save(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

config = ConfigLoader()