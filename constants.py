import sys
import platform
from dataclasses import dataclass

@dataclass(frozen=True)
class AppConstants:
    APP_NAME: str = "pyautogui-tools-15"
    VERSION: str = "1.0.4"
    OS_TYPE: str = platform.system()
    IS_WINDOWS: bool = OS_TYPE == "Windows"
    
    # Timing jitter for human-like behavior
    CLICK_INTERVAL_MIN: float = 0.05
    CLICK_INTERVAL_MAX: float = 0.25
    
    # System safe guards
    FAILSAFE_ENABLED: bool = True
    DEFAULT_PAUSE: float = 0.1
    
    # Display scaling factors
    DPI_AWARE: bool = True
    
    # Key mapping defaults
    STOP_KEY: str = "f12"
    TRIGGER_KEY: str = "f9"

CONSTANTS = AppConstants()

# Helper for platform checks
def get_system_info():
    return {
        "system": CONSTANTS.OS_TYPE,
        "python": sys.version_info.major,
        "mode": "production" if not __debug__ else "development"
    }