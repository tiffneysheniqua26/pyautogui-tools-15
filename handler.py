import json
import os
from typing import Dict, Any

class ClickProfileManager:
    def __init__(self, storage_path: str = "profiles.json"):
        self.storage_path = storage_path

    def serialize_coordinates(self, data: Dict[str, Any]) -> str:
        return json.dumps(data, indent=4)

    def save_profile(self, name: str, settings: Dict[str, Any]) -> bool:
        db = self._load_db()
        db[name] = settings
        with open(self.storage_path, 'w') as f:
            f.write(self.serialize_coordinates(db))
        return True

    def get_profile(self, name: str) -> Dict[str, Any]:
        return self._load_db().get(name, {})

    def _load_db(self) -> Dict[str, Any]:
        if not os.path.exists(self.storage_path):
            return {}
        with open(self.storage_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def list_profiles(self) -> list:
        return list(self._load_db().keys())

def scrub_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in settings.items() if v is not None}

if __name__ == '__main__':
    manager = ClickProfileManager()
    manager.save_profile("fast_click", {"interval": 0.01, "button": "left"})