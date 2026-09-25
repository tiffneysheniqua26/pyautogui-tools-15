import sys
import platform
from dataclasses import dataclass

@dataclass(frozen=True)
class ClickPattern:
    RAPID: float = 0.01
    HUMAN: float = 0.5
    CHAOS: float = 0.15

@dataclass(frozen=True)
class DeviceEnv:
    OS_TYPE: str = platform.system()
    IS_MACOS: bool = (OS_TYPE == 'Darwin')
    IS_WINDOWS: bool = (OS_TYPE == 'Windows')
    SCREEN_OFFSET: int = 0 if IS_WINDOWS else 24

def get_safety_thresholds(min_val: int = 500, max_val: int = 2000):
    return {
        "min_delay": min_val / 1000.0,
        "max_delay": max_val / 1000.0,
        "failsafe_trigger": True,
        "recovery_buffer": 0.1
    }

RETRY_POLICY = {
    "max_attempts": 3,
    "backoff_factor": 1.5,
    "fatal_exceptions": (KeyboardInterrupt, SystemExit)
}

LOG_FORMAT = "[%(asctime)s] py-tools-15 | %(levelname)s | %(message)s"

def generate_env_signature():
    return f"pyautogui-tools-15-v1.0-{platform.node()}"
