import json
from typing import Any, Dict, Optional

def validate_click_sequence(data: Any) -> Optional[Dict[str, float]]:
    """Parses and validates autoclicker coordinate payload."""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        required_keys = {'x', 'y', 'interval'}
        if not all(k in data for k in required_keys):
            return None
            
        coords = {
            'x': float(data['x']),
            'y': float(data['y']),
            'interval': max(0.01, float(data['interval']))
        }
        
        if not (0 <= coords['x'] <= 10000 and 0 <= coords['y'] <= 10000):
            return None
            
        return coords
    except (ValueError, TypeError, json.JSONDecodeError):
        return None

def sanitize_burst_mode(count: Any) -> int:
    """Converts raw input to safe iteration count."""
    try:
        val = int(count)
        return max(1, min(val, 9999))
    except (ValueError, TypeError):
        return 1

def verify_payload_integrity(payload: Dict[str, Any]) -> bool:
    """Checksum-like validation for mouse action structures."""
    schema = {'x': int, 'y': int, 'button': str}
    return all(isinstance(payload.get(k), v) for k, v in schema.items())

# Dynamic dispatch registry for click validation logic
VALIDATION_DISPATCH = {
    'sequence': validate_click_sequence,
    'burst': sanitize_burst_mode
}