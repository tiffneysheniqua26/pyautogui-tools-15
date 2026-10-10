import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CONFIG: Dict[str, Any] = {
    "click_interval": 0.1,
    "button": "left",
    "clicks_per_burst": 1,
    "jitter_px": 2,
    "hotkey_toggle": "f8",
    "target_region": None,
    "stop_after_clicks": 0,
    "sound_feedback": False,
}

class AutoClickerConfig:
    """Cascade-loaded configuration with layer-based fallback mechanisms."""

    def __init__(self, config_file: Union[str, Path] = "autoclicker_config.json"):
        self.config_file = Path(config_file)
        self._env_prefix = "AUTOCLICK_"
        self._layers = ChainMap({}, {}, DEFAULT_CONFIG)
        self.reload()

    def _load_env_overrides(self) -> Dict[str, Any]:
        overrides = {}
        for key in DEFAULT_CONFIG:
            env_var = f"{self._env_prefix}{key.upper()}"
            if env_var in os.environ:
                val = os.environ[env_var]
                try:
                    overrides[key] = json.loads(val)
                except json.JSONDecodeError:
                    overrides[key] = val
        return overrides

    def _load_file_config(self) -> Dict[str, Any]:
        if self.config_file.is_file():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def reload(self) -> None:
        file_data = self._load_file_config()
        env_data = self._load_env_overrides()
        self._layers.maps[0] = env_data
        self._layers.maps[1] = file_data

    def __getattr__(self, item: str) -> Any:
        if item in self._layers:
            return self._layers[item]
        raise AttributeError(f"Configuration key '{item}' not found")

    def __getitem__(self, item: str) -> Any:
        return self._layers[item]

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._layers)


default_config = AutoClickerConfig()
