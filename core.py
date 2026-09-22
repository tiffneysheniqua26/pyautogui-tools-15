import pyautogui
import time
import threading
from queue import Queue

class ClickEngine:
    def __init__(self, interval=0.01):
        self.interval = interval
        self.queue = Queue(maxsize=100)
        self.running = False

    def _worker(self):
        while self.running:
            try:
                x, y = self.queue.get(timeout=0.1)
                pyautogui.click(x, y, _pause=False)
            except:
                continue

    def start(self):
        self.running = True
        threading.Thread(target=self._worker, daemon=True).start()

    def stop(self):
        self.running = False

    def schedule(self, x, y):
        if not self.queue.full():
            self.queue.put((x, y))

def batch_click_processor(coords, interval=0.01):
    """High-throughput click execution using reduced overhead"""
    pyautogui.PAUSE = 0
    for x, y in coords:
        pyautogui.click(x, y)
        time.sleep(interval)

if __name__ == '__main__':
    engine = ClickEngine()
    engine.start()