import sys
from typing import Final, Dict

# Execution engine constraints and heartbeat pulse
MAX_CLICK_VELOCITY: Final[int] = 500
DEFAULT_SAFE_INTERVAL: Final[float] = 0.05

# Platform-specific hotkey override mapping
KEY_INTERRUPT: Final[str] = 'f12' if sys.platform != 'darwin' else 'esc'

# Precision threshold for coordinate validation
COORDINATE_DRIFT_BUFFER: Final[int] = 2

# Status codes for state machine synchronization
STATUS_MAP: Final[Dict[str, int]] = {
    'IDLE': 0,
    'PENDING': 1,
    'ACTIVE': 2,
    'HALTED': 3,
    'FAULT': 4
}

# Operational boundaries for cursor pathfinding
SCREEN_BOUNDS_PADDING: Final[int] = 10

# Versioning metadata for engine serialization
VERSION_INFO: Final[str] = '1.5.0-stable'

def get_timeout_limit(base: float) -> float:
    """Calculates effective timeout based on velocity constraints."""
    return max(base, DEFAULT_SAFE_INTERVAL * 2)

# Global flag for hot-reloading behavior
ALLOW_OVERCLOCK: Final[bool] = False