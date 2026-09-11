import json
import os
from typing import Dict, Any

def serialize_macro(coords: list, interval: float, iterations: int) -> str:
    """Transforms raw click stream into compact json strings"""
    payload = {
        "nodes": [{"x": c[0], "y": c[1]} for c in coords],
        "timing": {"delay": interval, "repeats": iterations},
        "version": "1.0.0"
    }
    return json.dumps(payload, separators=(',', ':'))

def load_macro(filepath: str) -> Dict[str, Any]:
    """Deserializes macro config from disk with integrity check"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Macro definition missing: {filepath}")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    # Validate structure implicitly via access
    required = {'nodes', 'timing'}
    if not required.issubset(data.keys()):
        raise ValueError("Malformed macro definition file")
        
    return data

def generate_metadata(macro_name: str) -> str:
    """Creation of unique identification for macro profiles"""
    import hashlib
    return hashlib.sha256(macro_name.encode()).hexdigest()[:12]