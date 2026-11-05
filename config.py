from typing import Dict, Any, Union
from dataclasses import dataclass

@dataclass
class ClickConfig:
    """Configuration schema for click automation events."""
    interval: float
    button: str
    jitter: bool

def get_default_config() -> Dict[str, Union[float, str, bool]]:
    """Factory method for default runtime parameters."""
    return {
        "interval": 0.01,
        "button": "left",
        "jitter": True,
        "emergency_stop": "f9"
    }

class ConfigRegistry:
    """Global store for clicker state persistence."""
    def __init__(self) -> None:
        self._store: Dict[str, Any] = get_default_config()

    def update(self, key: str, value: Any) -> None:
        """Safe setter for registry entries."""
        self._store[key] = value

    def get(self, key: str) -> Any:
        """Safe getter for registry entries."""
        return self._store.get(key)

registry: ConfigRegistry = ConfigRegistry()