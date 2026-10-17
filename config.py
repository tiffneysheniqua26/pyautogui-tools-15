import json
import os
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CONFIG: Dict[str, Any] = {
    "click_interval": 0.1,
    "mouse_button": "left",
    "double_click": False,
    "hotkey_start": "f6",
    "hotkey_stop": "f7",
    "max_clicks": 0,
    "random_jitter_ms": 15,
    "fail_safe": True,
}


class ConfigLoader:
    """Autoclicker configuration manager with dynamic attributes and file persistence."""

    def __init__(self, config_path: Union[str, Path] = "autoclicker_config.json"):
        self.path = Path(config_path)
        self._store: Dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        """Load configuration from disk, overlaying defaults."""
        file_data = {}
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
            except (json.JSONDecodeError, OSError):
                file_data = {}
        self._store = {**DEFAULT_CONFIG, **file_data}

    def save(self) -> None:
        """Persist settings back to file."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._store, f, indent=2)

    def __getattr__(self, name: str) -> Any:
        if name in self._store:
            return self._store[name]
        raise AttributeError(f"Configuration option '{name}' is not defined")

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ("path", "_store"):
            super().__setattr__(name, value)
        else:
            self._store[name] = value

    def reset_defaults(self) -> None:
        """Reset configuration to hardcoded defaults."""
        self._store = DEFAULT_CONFIG.copy()
        self.save()

    def as_dict(self) -> Dict[str, Any]:
        return self._store.copy()
