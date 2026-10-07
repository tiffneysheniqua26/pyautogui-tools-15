import json
import os
from typing import Any, Dict

def serialize_click_data(data: Dict[str, Any], filepath: str) -> bool:
    """serializes autoclicker configurations using a memory-efficient atomic write strategy"""
    temp_path = f"{filepath}.tmp"
    try:
        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)
        os.replace(temp_path, filepath)
        return True
    except (IOError, OSError, TypeError):
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

def deserialize_click_data(filepath: str) -> Dict[str, Any]:
    """loads click configuration with a graceful fallback to an empty profile""
    if not os.path.exists(filepath):
        return {"interval": 0.1, "button": "left", "clicks": 1}
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"error": "corrupted_config"}

class ClickProfile:
    """container for autoclicker settings with magic attribute access"""
    def __init__(self, data: Dict[str, Any]):
        self.__dict__.update(data)
    
    def __repr__(self) -> str:
        return f"ClickProfile({self.__dict__})"

def create_profile(data: Dict[str, Any]) -> ClickProfile:
    return ClickProfile(data)