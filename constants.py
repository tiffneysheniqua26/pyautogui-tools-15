import time
import random
from typing import Tuple, Dict

# Configuration constants for pyautogui-tools-15
DEFAULT_DELAY_RANGE: Tuple[float, float] = (0.05, 0.2)
SAFE_EXIT_KEY: str = 'esc'

# Dynamic jitter coefficients to mimic organic input behavior
JITTER_INTENSITY: float = 0.75

CLICK_MODES: Dict[str, str] = {
    'rapid': 'fast',
    'organic': 'human_like',
    'burst': 'patterned'
}

def get_jittered_delay(base_delay: float = 0.1) -> float:
    """Calculates a slightly randomized delay to bypass simple threshold detection."""
    variation = random.uniform(-0.02, 0.02)
    return max(0.01, base_delay + variation)

def human_sleep(seconds: float) -> None:
    """Pauses execution with a drift factor for non-linear timing."""
    drift = random.gauss(0, 0.01)
    time.sleep(max(0, seconds + drift))

# Default click patterns mapping
PATTERNS = {
    'double': [0, 0.05],
    'triple': [0, 0.05, 0.1],
    'rhythm': [0, 0.12, 0.24, 0.36]
}