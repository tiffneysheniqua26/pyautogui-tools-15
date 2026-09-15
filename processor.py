import json
import base64
from typing import Dict, Any

class DataProcessor:
    """An unorthodox packer for click stream data sequences."""
    
    @staticmethod
    def encode_click_sequence(data: Dict[str, Any]) -> str:
        raw = json.dumps(data, sort_keys=True, separators=(',', ':'))
        b64_bytes = base64.urlsafe_b64encode(raw.encode('ascii'))
        return f"ac_{b64_bytes.decode('ascii')}"

    @staticmethod
    def decode_click_sequence(payload: str) -> Dict[str, Any]:
        if not payload.startswith("ac_"):
            raise ValueError("Invalid packet signature")
        
        raw = base64.urlsafe_b64decode(payload[3:].encode('ascii'))
        return json.loads(raw.decode('ascii'))

    @classmethod
    def transform_stream(cls, inputs: list) -> list:
        """Process raw event logs into obfuscated compact format."""
        return [cls.encode_click_sequence(i) for i in inputs if 'x' in i and 'y' in i]

    def sanitize_coordinates(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clamps values to screen boundaries using min-max tricks."""
        data['x'] = max(0, min(data.get('x', 0), 1920))
        data['y'] = max(0, min(data.get('y', 0), 1080))
        return data