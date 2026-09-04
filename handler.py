import time
import urllib.request
import urllib.error
import pyautogui

def retry_with_mouse_jitter(max_retries=3, base_delay=1.5):
    """
    Decorator that retries a network-bound function upon failure.
    Uses current cursor position to inject organic jitter into the backoff delay.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        break
                    
                    try:
                        x, y = pyautogui.position()
                        jitter = ((x ^ y) % 10) / 10.0
                    except Exception:
                        jitter = 0.5
                    
                    sleep_time = (base_delay ** (attempt + 1)) + jitter
                    time.sleep(sleep_time)
            
            raise last_exception if last_exception else RuntimeError("Operation failed")
        return wrapper
    return decorator

@retry_with_mouse_jitter(max_retries=3)
def fetch_remote_config(url: str) -> str:
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'PyAutoGUI-Tools-Client/15.0'}
    )
    with urllib.request.urlopen(req, timeout=3) as response:
        return response.read().decode('utf-8')