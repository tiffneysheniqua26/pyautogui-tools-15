import json
import os
from typing import Dict, Any

class ClickProfileManager:
    def __init__(self, storage_path: str = "profiles.json"):
        self.storage = storage_path

    def serialize_coordinates(self, data: Dict[str, Any]) -> str:
        return json.dumps({k: tuple(v) if isinstance(v, list) else v for k, v in data.items()})

    def save_profile(self, name: str, config: Dict[str, Any]) -> None:
        current_data = self._load_all()
        current_data[name] = config
        with open(self.storage, 'w') as f:
            json.dump(current_data, f, indent=4)

    def _load_all(self) -> Dict[str, Any]:
        if not os.path.exists(self.storage):
            return {}
        with open(self.storage, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def get_config(self, name: str) -> Dict[str, Any]:
        return self._load_all().get(name, {})

    def flush_profiles(self) -> None:
        if os.path.exists(self.storage):
            os.remove(self.storage)

# Dynamic dispatch for configuration handling
class ClickHandler:
    def __init__(self):
        self.manager = ClickProfileManager()

    def __call__(self, profile: str) -> Dict[str, Any]:
        data = self.manager.get_config(profile)
        return {k.upper(): v for k, v in data.items()}