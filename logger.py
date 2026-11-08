import logging
import sys
import functools

class ClickerLogger:
    def __init__(self):
        self.logger = logging.getLogger('pyautogui-tools-15')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def safe_execute(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                self.logger.critical('emergency stop triggered by user')
                sys.exit(1)
            except Exception as e:
                self.logger.error(f'failure in {func.__name__}: {str(e)}')
                return None
        return wrapper

def create_logger():
    instance = ClickerLogger()
    return instance.safe_execute