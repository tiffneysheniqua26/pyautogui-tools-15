import time
import random
import urllib.request
import urllib.error

try:
    import pyautogui
except ImportError:
    class MockPyAutoGUI:
        def position(self):
            return (100, 100)
        def moveTo(self, x, y, duration=0):
            pass
    pyautogui = MockPyAutoGUI()

class NetworkRetryProcessor:
    """Handles retries for remote click instruction dispatches."""
    def __init__(self, max_retries: int = 3, base_delay: float = 1.5):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def active_retry(self, func):
        """
        Decorator that retries network operations. During backoff delays, 
        it subtly moves the mouse cursor to prevent screen sleep or locking.
        """
        def wrapper(*args, **kwargs):
            retries = 0
            delay = self.base_delay
            while retries <= self.max_retries:
                try:
                    return func(*args, **kwargs)
                except (urllib.error.URLError, ConnectionError) as e:
                    retries += 1
                    if retries > self.max_retries:
                        raise RuntimeError(f"Network operation failed: {e}")
                    
                    # Active anti-sleep micro-jiggles during backoff delay
                    end_time = time.time() + delay
                    while time.time() < end_time:
                        x, y = pyautogui.position()
                        pyautogui.moveTo(x + random.choice([-1, 1]), y + random.choice([-1, 1]), duration=0.05)
                        time.sleep(0.5)
                    
                    delay = (self.base_delay * (2 ** retries)) + random.uniform(0.1, 1.0)
        return wrapper

@NetworkRetryProcessor(max_retries=3, base_delay=2.0).active_retry
def fetch_coordinate_payload(url: str) -> str:
    """Fetches remote click coordinates from the control server."""
    req = urllib.request.Request(url, headers={'User-Agent': 'pyautogui-tools-15'})
    with urllib.request.urlopen(req, timeout=3) as response:
        return response.read().decode('utf-8')
