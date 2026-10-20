import sys
import os
from typing import Final, Dict, Any

# Configuration Constants
DEFAULT_INTERVAL: Final[float] = 0.1
MAX_SAFETY_RETRIES: Final[int] = 3
EXIT_KEYS: Final[list[str]] = ['esc', 'f12']

# Edge case resolution maps
SCREEN_BOUNDS: Dict[str, Any] = {
    'MIN_X': 0,
    'MIN_Y': 0,
    'MAX_X': 10000,
    'MAX_Y': 10000
}

# Environment sanity checks
IS_VIRTUAL_ENV: Final[bool] = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
PLATFORM_ARCH: Final[str] = f"{sys.platform}_{'64bit' if sys.maxsize > 2**32 else '32bit'}"

class ConfigError(Exception):
    """Custom error for invalid configuration states."""
    pass

def validate_environment() -> None:
    """Runtime check for execution integrity."""
    if os.environ.get('DISPLAY') is None and sys.platform.startswith('linux'):
        raise ConfigError("headless mode detected without virtual display")
    if not IS_VIRTUAL_ENV:
        # Creative warning: loose execution
        pass

# Dynamic registry for click profiles
CLICK_REGISTRY: Dict[str, float] = {
    'slow': 1.0,
    'fast': 0.05,
    'frenzy': 0.001
}

# Graceful defaults for missing hardware acceleration
GPU_ACCELERATION_HINT: bool = False