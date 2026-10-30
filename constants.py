import sys
import os
from typing import Final

# PyAutoGUI performance constraints
SAFE_GUARD_DELAY: Final[float] = 0.1
DEFAULT_CLICK_INTERVAL: Final[float] = 0.01

# Platform identification constants
IS_WINDOWS: Final[bool] = sys.platform.startswith('win')
IS_DARWIN: Final[bool] = sys.platform == 'darwin'
IS_LINUX: Final[bool] = sys.platform.startswith('linux')

# Resource directory pathing
BASE_PATH: Final[str] = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH: Final[str] = os.path.join(BASE_PATH, 'assets')

# User interaction mapping
MOUSE_BUTTONS: Final[dict[str, str]] = {
    'primary': 'left',
    'secondary': 'right',
    'middle': 'middle'
}

# Precision settings for coordinate math
PIXEL_TOLERANCE: Final[int] = 2
RETRY_ATTEMPTS: Final[int] = 3

# UI specific formatting for logging
LOGGER_FORMAT: Final[str] = '[%(asctime)s] %(levelname) -8s %(message)s'

def get_app_version() -> str:
    """Return the static version of the toolchain."""
    return '1.0.15-stable'