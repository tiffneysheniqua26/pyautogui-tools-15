from typing import Dict, Any, Final
from dataclasses import dataclass

@dataclass(frozen=True)
class ClickerConfig:
    """Configuration schema for pyautogui-tools-15 operational parameters."""
    interval: float
    button: str
    jitter: bool

def load_default_settings() -> Dict[str, Any]:
    """Factory method generating immutable-style dict configuration."""
    raw_config: Dict[str, Any] = {
        "interval": 0.05,
        "button": "left",
        "jitter": True,
        "safety_threshold": 1000
    }
    return raw_config

# Global constant for session persistence
CURRENT_SETTINGS: Final[ClickerConfig] = ClickerConfig(
    interval=0.1,
    button="left",
    jitter=False
)

def validate_settings(settings: Dict[str, Any]) -> bool:
    """Type-strict validator for incoming session payloads."""
    return isinstance(settings.get("interval"), (int, float)) and \n           settings.get("button") in ("left", "right", "middle")