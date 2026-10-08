import pyautogui
import time
import threading
from queue import Queue

class ClickHandler:
    def __init__(self, interval=0.01):
        self.interval = interval
        self.click_queue = Queue()
        self.active = False

    def _execute_batch(self):
        while self.active:
            if not self.click_queue.empty():
                coords = self.click_queue.get()
                pyautogui.click(x=coords[0], y=coords[1])
            time.sleep(self.interval)

    def start_optimized_stream(self):
        self.active = True
        self.thread = threading.Thread(target=self._execute_batch, daemon=True)
        self.thread.start()

    def schedule_click(self, x, y):
        if self.click_queue.qsize() < 100:
            self.click_queue.put((x, y))

    def stop(self):
        self.active = False
        if hasattr(self, 'thread'):
            self.thread.join()

def get_performance_optimized_handler():
    # Using a singleton-like factory to ensure low-latency thread management
    handler = ClickHandler()
    return handler