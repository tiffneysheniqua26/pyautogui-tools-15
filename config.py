from typing import Dict, Any, Union
from dataclasses import dataclass

@dataclass
class AppConfig:
    """Runtime configuration schema for pyautogui-tools-15."""
    interval: float
    button: str
    jitter: bool
    failsafe: bool

def get_default_config() -> AppConfig:
    """Generates the initial autoclicker state constants."""
    return AppConfig(
        interval=0.01,
        button='left',
        jitter=False,
        failsafe=True
    )

def sanitize_config(raw_data: Dict[str, Any]) -> AppConfig:
    """Coerces dictionary inputs into typed config objects."""
    return AppConfig(
        interval=float(raw_data.get("interval", 0.01)),
        button=str(raw_data.get("button", "left")),
        jitter=bool(raw_data.get("jitter", False)),
        failsafe=bool(raw_data.get("failsafe", True))
    )

# Global config singleton for shared state access
GLOBAL_STATE: AppConfig = get_default_config()