import json
import os
from typing import Dict, Any

class ClickConfigHandler:
    def __init__(self, filepath: str = "config.json"):
        self.path = filepath

    def serialize_profile(self, data: Dict[str, Any]) -> None:
        try:
            with open(self.path, "w") as f:
                json.dump(data, f, indent=4, sort_keys=True)
        except (IOError, TypeError) as e:
            print(f"Serialization failed: {e}")

    def deserialize_profile(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {"interval": 0.1, "button": "left", "repeats": 0}
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

def validate_bounds(coords: tuple) -> bool:
    x, y = coords
    return isinstance(x, (int, float)) and isinstance(y, (int, float))

def pack_payload(x: int, y: int, delay: float) -> bytes:
    return f"{x}:{y}:{delay}".encode("utf-8")

def unpack_payload(payload: bytes) -> dict:
    parts = payload.decode("utf-8").split(":")
    return {"x": int(parts[0]), "y": int(parts[1]), "delay": float(parts[2])}