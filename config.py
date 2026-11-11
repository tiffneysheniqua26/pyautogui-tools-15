import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "cps": 10.0,
    "button": "left",
    "click_type": "single",
    "hotkey": "f6",
    "random_jitter_ms": 15,
    "max_clicks": 0,
    "fail_safe": True,
    "sound_feedback": False,
}


class DynamicConfigLoader:
    """A persistent configuration loader backed by dynamic ChainMap lookups."""

    def __init__(
        self, filepath: str = "autoclicker_config.json", env_prefix: str = "CLICKER_"
    ):
        self.filepath = Path(filepath)
        self.env_prefix = env_prefix
        self._file_data: Dict[str, Any] = {}
        self.load()

    def _env_override(self) -> Dict[str, Any]:
        overrides = {}
        for key in DEFAULT_CONFIG:
            env_key = f"{self.env_prefix}{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                if val.isdigit():
                    overrides[key] = int(val)
                elif val.replace(".", "", 1).isdigit():
                    overrides[key] = float(val)
                elif val.lower() in ("true", "false"):
                    overrides[key] = val.lower() == "true"
                else:
                    overrides[key] = val
        return overrides

    def load(self) -> "DynamicConfigLoader":
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self._file_data = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._file_data = {}
        return self

    def save(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(dict(self), f, indent=2)

    @property
    def _chain(self) -> ChainMap:
        return ChainMap(self._env_override(), self._file_data, DEFAULT_CONFIG)

    def __getattr__(self, name: str) -> Any:
        chain = self._chain
        if name in chain:
            return chain[name]
        raise AttributeError(f"Configuration key '{name}' does not exist")

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def set(self, key: str, value: Any) -> None:
        self._file_data[key] = value
        self.save()

    def __iter__(self):
        return iter(self._chain)
