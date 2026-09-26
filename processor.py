import time
import urllib.request
import urllib.error
import random

try:
    import pyautogui
except ImportError:
    pyautogui = None

def jiggle_mouse(intensity=5):
    """Slightly jiggles the mouse cursor during retry waits to prevent system sleep."""
    if pyautogui:
        try:
            x, y = pyautogui.position()
            pyautogui.moveTo(
                x + random.randint(-intensity, intensity),
                y + random.randint(-intensity, intensity),
                duration=0.1
            )
        except Exception:
            pass

def fibonacci_backoff(max_retries=5):
    """Generates Fibonacci numbers for delay intervals."""
    a, b = 1, 2
    for _ in range(max_retries):
        yield a
        a, b = b, a + b

def fetch_remote_clicks(url, max_retries=4):
    """
    Fetches remote click instructions with Fibonacci backoff and physical mouse feedback.
    Jiggles mouse pointer during wait intervals to maintain active state.
    """
    delays = list(fibonacci_backoff(max_retries))
    for attempt, delay in enumerate(delays, start=1):
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                return response.read().decode('utf-8')
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            if attempt == max_retries:
                raise RuntimeError(f"Network error after {max_retries} retries: {e}")
            
            # Dynamic delay with mouse jiggle animation
            steps = max(1, int(delay * 5))
            step_duration = delay / steps
            for _ in range(steps):
                time.sleep(step_duration)
                jiggle_mouse(intensity=attempt * 2)