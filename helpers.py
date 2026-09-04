import json
import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "click_delay_ms": 100,
    "button": "left",
    "clicks": 1,
    "hotkey": "f10",
    "random_jitter_px": 5,
    "failsafe_enabled": True
}

class SelfHealingConfig:
    """A configuration loader that restores missing keys and casts env overrides dynamically."""
    def __init__(self, filepath: str = "~/.pyautogui_autoclicker.json"):
        self._filepath = os.path.expanduser(filepath)
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self._filepath):
            return DEFAULT_CONFIG.copy()
        try:
            with open(self._filepath, "r") as f:
                loaded = json.load(f)
                return {**DEFAULT_CONFIG, **loaded}
        except (json.JSONDecodeError, PermissionError):
            return DEFAULT_CONFIG.copy()

    def save(self) -> None:
        try:
            with open(self._filepath, "w") as f:
                json.dump(self._data, f, indent=4)
        except PermissionError:
            pass

    def __getattr__(self, item: str) -> Any:
        if item in self._data:
            env_val = os.getenv(f"AUTOCLICKER_{item.upper()}")
            if env_val is not None:
                default_type = type(DEFAULT_CONFIG.get(item, ""))
                try:
                    if default_type is bool:
                        return env_val.lower() in ("true", "1", "yes")
                    return default_type(env_val)
                except ValueError:
                    return self._data[item]
            return self._data[item]
        raise AttributeError(f"Configuration option '{item}' is unrecognized")

    def __setattr__(self, key: str, value: Any) -> None:
        if key in ("_filepath", "_data"):
            super().__setattr__(key, value)
        elif key in DEFAULT_CONFIG:
            expected_type = type(DEFAULT_CONFIG[key])
            if not isinstance(value, expected_type):
                try:
                    value = expected_type(value)
                except (ValueError, TypeError):
                    raise TypeError(f"Key '{key}' must be of type {expected_type.__name__}")
            self._data[key] = value
            self.save()
        else: 
            raise KeyError(f"Cannot add unknown configuration options dynamic key '{key}'")

    def __repr__(self) -> str:
        return f"SelfHealingConfig({self._data})"