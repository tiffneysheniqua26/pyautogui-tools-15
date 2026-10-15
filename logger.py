import logging
import functools

# Configure logger for pyautogui-tools-15
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [pyautogui-tools-15] - %(levelname)s - %(message)s')
logger = logging.getLogger('autoclicker_core')

def validate_input(func):
    """Decorator that casts inputs to positive floats and sanity-checks intervals"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cleaned_args = []
        for arg in args:
            try:
                val = float(arg)
                if val < 0.001:
                    logger.warning(f'Input {val} too low, clamping to 0.001')
                    val = 0.001
                cleaned_args.append(val)
            except (ValueError, TypeError):
                logger.error(f'Invalid input detected: {arg}, defaulting to 1.0')
                cleaned_args.append(1.0)
        return func(*cleaned_args, **kwargs)
    return wrapper

@validate_input
def safe_click_loop(interval, duration):
    """Simulated clicking process with validated execution parameters"""
    logger.info(f'Starting clicker at {interval}s interval for {duration}s')
    import time
    start = time.time()
    while time.time() - start < duration:
        time.sleep(interval)
        logger.info('Click event emitted successfully')