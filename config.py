import json
import os
from pathlib import Path
from typing import Any, Dict

class AutoClickerConfig:
    DEFAULTS: Dict[str, Any] = {
        "click_interval": 0.1,
        "button": "left",
        "clicks_count": 0,
        "hotkey_start": "f6",
        "hotkey_stop": "f7",
        "random_delay_range": [0.0, 0.05],
        "double_click": False
    }

    def __init__(self, filepath: str = "config.json"):
        self._filepath = Path(filepath)
        self._data = self.DEFAULTS.copy()
        self._load()

    def _load(self) -> None:
        if self._filepath.exists():
            try:
                with open(self._filepath, "r") as f:
                    loaded_data = json.load(f)
                    for key, default_val in self.DEFAULTS.items():
                        if key in loaded_data:
                            val = loaded_data[key]
                            try:
                                if isinstance(default_val, list) and isinstance(val, list):
                                    self._data[key] = [type(default_val[0])(v) for v in val] if default_val else val
                                else:
                                    self._data[key] = type(default_val)(val)
                            except (ValueError, TypeError):
                                self._data[key] = default_val
            except (json.JSONDecodeError, IOError):
                self._save()
        else:
            self._save()

    def _save(self) -> None:
        try:
            with open(self._filepath, "w") as f:
                json.dump(self._data, f, indent=4)
        except IOError:
            pass

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'AutoClickerConfig' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ["_filepath", "_data"]:
            super().__setattr__(name, value)
            return
        if name in self.DEFAULTS:
            expected_type = type(self.DEFAULTS[name])
            try:
                self._data[name] = expected_type(value)
                self._save()
            except (ValueError, TypeError):
                raise ValueError(f"Invalid type for {name}. Expected {expected_type.__name__}")
        else:
            raise AttributeError(f"Cannot set undefined option: {name}")

    def reset(self) -> None:
        self._data = self.DEFAULTS.copy()
        self._save()