import json
import os
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CONFIG: Dict[str, Any] = {
    "cps": 10.0,
    "button": "left",
    "hotkey": "f6",
    "jitter_ms": 15,
    "click_type": "single",
    "max_clicks": 0,
    "safe_mode": True,
    "target_region": None,
}


class ConfigProxy:
    """Dynamic configuration wrapper with fallback defaults and env overrides."""

    def __init__(self, config_path: Union[str, Path] = "autoclick_config.json"):
        self._path = Path(config_path)
        self._store: Dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        raw_data = {}
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
            except (json.JSONDecodeError, OSError):
                raw_data = {}
        self._store = {**DEFAULT_CONFIG, **raw_data}

    def __getattr__(self, name: str) -> Any:
        env_key = f"AUTOCLICK_{name.upper()}"
        if env_key in os.environ:
            val = os.environ[env_key]
            if val.isdigit():
                return int(val)
            try:
                return float(val)
            except ValueError:
                if val.lower() in ("true", "false"):
                    return val.lower() == "true"
                return val

        if name in self._store:
            return self._store[name]
        raise AttributeError(f"Configuration option '{name}' not found")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._store[name] = value

    def save(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._store, f, indent=2)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._store)


config = ConfigProxy()
