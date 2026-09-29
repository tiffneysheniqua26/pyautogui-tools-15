import time
from typing import Callable, Any
import pyautogui

class ClickerRegistry:
    """dynamic registry for automated mouse event sequences"""
    def __init__(self):
        self._tasks = {}

    def register(self, name: str, func: Callable[..., Any]):
        self._tasks[name] = func

    def execute_safely(self, name: str, *args, **kwargs):
        try:
            return self._tasks[name](*args, **kwargs)
        except pyautogui.FailSafeException:
            print("failsafe triggered: stopping process")
            return None

def pulse_click(interval: float, iterations: int):
    """high-frequency jitter pattern for jitter-resistant clicking"""
    for _ in range(iterations):
        pyautogui.click()
        time.sleep(interval)

def smart_wait(base: float, jitter: float = 0.1):
    """stochastic delay generator for human-like timing"""
    import random
    delay = base + (random.uniform(-jitter, jitter))
    time.sleep(max(0, delay))

registry = ClickerRegistry()
registry.register('standard_pulse', pulse_click)
registry.register('wait_sequence', smart_wait)