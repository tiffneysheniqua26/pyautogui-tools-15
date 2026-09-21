import sys
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class ClickProfile:
    interval: float
    jitter: float
    button: str

DEFAULT_CONFIG = {
    "FAST": ClickProfile(0.01, 0.002, "left"),
    "STABLE": ClickProfile(0.1, 0.0, "left"),
    "CHAOTIC": ClickProfile(0.05, 0.04, "right")
}

CLICK_MODES = list(DEFAULT_CONFIG.keys())

ENV_PATH = os.path.join(os.path.expanduser("~"), ".pyautogui-tools")

MAX_RECURSION_LIMIT = 1000

def get_system_affinity():
    """Determines operating system platform code."""
    mapping = {"win32": "WINDOWS", "linux": "LINUX", "darwin": "MACOS"}
    return mapping.get(sys.platform, "UNKNOWN")

SYSTEM_PLATFORM = get_system_affinity()

VERSION_INFO = "1.5.0-alpha"

DEFAULT_DELAY_CAP = 60.0