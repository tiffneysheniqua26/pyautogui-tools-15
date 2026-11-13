import json
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CONFIG: Dict[str, Any] = {
    "click_interval": 0.1,
    "button": "left",
    "clicks_per_second_max": 20.0,
    "toggle_hotkey": "f6",
    "jitter_ms": 15,
    "enable_failsafe": True,
    "target_coordinates": None,
}


class ConfigManager:
    """Dynamic configuration loader with persistence and fallback defaults."""

    def __init__(self, path: Union[str, Path] = "autoclicker_config.json"):
        self.filepath = Path(path)
        self._data = dict(DEFAULT_CONFIG)
        self._load_or_bootstrap()

    def _load_or_bootstrap(self) -> None:
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                    if isinstance(user_data, dict):
                        self._data.update(user_data)
            except (json.JSONDecodeError, OSError):
                self._save()
        else:
            self._save()

    def _save(self) -> None:
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4)
        except OSError:
            pass

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Configuration key '{name}' does not exist.")

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ("filepath", "_data"):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
            self._save()

    def reset_to_defaults(self) -> None:
        self._data = dict(DEFAULT_CONFIG)
        self._save()

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._data)
