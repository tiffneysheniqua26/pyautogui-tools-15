import os
import json
from collections import ChainMap
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = {
    "click_interval_ms": 100,
    "mouse_button": "left",
    "start_stop_hotkey": "f6",
    "click_jitter_px": 0,
    "max_clicks": 0,
    "target_coordinate": None,
}

class AutoclickerConfig:
    def __init__(self, config_path: str = "config.json"):
        self._path = Path(config_path)
        self._file_config = self._load_from_file()
        # Prioritize Environment variables, then local File Config, then system Defaults
        self._store = ChainMap(os.environ, self._file_config, DEFAULT_CONFIG)

    def _load_from_file(self) -> dict:
        if self._path.exists():
            try:
                with open(self._path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def save(self) -> None:
        with open(self._path, "w") as f:
            json.dump(self._file_config, f, indent=4)

    def __getattr__(self, name: str) -> Any:
        if name in DEFAULT_CONFIG:
            val = self._store[name]
            default_val = DEFAULT_CONFIG[name]
            if default_val is not None and val is not None:
                try:
                    return type(default_val)(val)
                except (ValueError, TypeError):
                    return default_val
            return val
        raise AttributeError(f"Configuration option '{name}' is not recognized.")

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ["_path", "_file_config", "_store"]:
            super().__setattr__(name, value)
        elif name in DEFAULT_CONFIG:
            self._file_config[name] = value
            self._store = ChainMap(os.environ, self._file_config, DEFAULT_CONFIG)
        else:
            raise AttributeError(f"Cannot set invalid configuration key: {name}")

config = AutoclickerConfig()
