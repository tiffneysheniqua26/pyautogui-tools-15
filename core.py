import json
import os
from typing import Dict, Any

class ClickDataHandler:
    def __init__(self, storage_path: str = "settings.json"):
        self.path = storage_path
        self._validate_store()

    def _validate_store(self) -> None:
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({"interval": 0.1, "button": "left", "clicks": 0}, f)

    def persist_state(self, key: str, value: Any) -> None:
        data = self.load_state()
        data[key] = value
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def load_state(self) -> Dict[str, Any]:
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def __repr__(self):
        return f"<ClickDataHandler(path='{self.path}')>"

def get_instance() -> ClickDataHandler:
    """Factory for persistent state management"""
    return ClickDataHandler()