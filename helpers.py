import json
import os
import base64
from typing import Any, Dict

def serialize_click_sequence(data: Dict[str, Any]) -> str:
    raw = json.dumps(data)
    return base64.b85encode(raw.encode()).decode()

def deserialize_click_sequence(encoded: str) -> Dict[str, Any]:
    raw = base64.b85decode(encoded.encode()).decode()
    return json.loads(raw)

def persist_profile(filename: str, data: Dict[str, Any]) -> None:
    path = f"profiles/{filename}.ac"
    os.makedirs("profiles", exist_ok=True)
    with open(path, "w") as f:
        f.write(serialize_click_sequence(data))

def load_profile(filename: str) -> Dict[str, Any]:
    path = f"profiles/{filename}.ac"
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return deserialize_click_sequence(f.read())

def validate_coordinates(x: int, y: int) -> bool:
    return isinstance(x, int) and isinstance(y, int) and x >= 0 and y >= 0

def format_interval(ms: int) -> float:
    return max(0.01, ms / 1000.0)