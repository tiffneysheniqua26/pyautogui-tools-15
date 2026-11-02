import json
from pathlib import Path
from typing import Any, Dict

AUTOCLICKER_DEFAULTS: Dict[str, Any] = {
    "cps": 10.0,
    "button": "left",
    "hotkey": "f8",
    "jitter_px": 2,
    "max_clicks": 0,
    "target_region": None,
    "sound_feedback": True,
}


class DynamicConfigLoader:
    """Cascading configuration manager for autoclicker runtime settings."""

    def __init__(self, config_path: str = "autoclicker_config.json"):
        self._path = Path(config_path)
        self._data = dict(AUTOCLICKER_DEFAULTS)
        self.reload()

    def reload(self) -> None:
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    user_cfg = json.load(f)
                    if isinstance(user_cfg, dict):
                        self._data.update(
                            {
                                k: v
                                for k, v in user_cfg.items()
                                if k in AUTOCLICKER_DEFAULTS
                            }
                        )
            except (json.JSONDecodeError, OSError):
                pass
        self.sync()

    def sync(self) -> None:
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4)
        except OSError:
            pass

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Configuration option '{name}' is not defined.")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
        elif name in AUTOCLICKER_DEFAULTS:
            self._data[name] = value
            self.sync()
        else:
            raise KeyError(f"Invalid configuration key: '{name}'")

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._data)
