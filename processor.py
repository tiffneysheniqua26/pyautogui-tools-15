import json
import base64
import zlib
from typing import Dict, Any

class ClickerDataProcessor:
    """Serialization engine for click sequences using zlib compression."""
    
    def __init__(self, secret_key: str = "pyautogui-15"):
        self._salt = secret_key.encode()

    def pack(self, data: Dict[str, Any]) -> str:
        """Compress and encode data payload for storage."""
        raw_json = json.dumps(data, sort_keys=True).encode()
        compressed = zlib.compress(raw_json + self._salt, level=9)
        return base64.urlsafe_b64encode(compressed).decode("utf-8")

    def unpack(self, payload: str) -> Dict[str, Any]:
        """Decode and decompress stored payload safely."""
        try:
            decoded = base64.urlsafe_b64decode(payload.encode())
            decompressed = zlib.decompress(decoded)
            final_data = decompressed.replace(self._salt, b"")
            return json.loads(final_data)
        except (ValueError, zlib.error, json.JSONDecodeError):
            return {}

    @staticmethod
    def validate_coordinates(coords: tuple) -> bool:
        """Sanity check for screen boundaries."""
        x, y = coords
        return isinstance(x, int) and isinstance(y, int) and x >= 0 and y >= 0