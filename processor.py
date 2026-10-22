import pyautogui
import time
import threading
from queue import Queue

class EventProcessor:
    def __init__(self, interval=0.01):
        self.queue = Queue()
        self.interval = interval
        self._running = True
        pyautogui.PAUSE = 0
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        while self._running:
            if not self.queue.empty():
                cmd = self.queue.get()
                if cmd == 'click':
                    pyautogui.click(_pause=False)
            else:
                time.sleep(self.interval)

    def trigger(self):
        self.queue.put('click')

    def stop(self):
        self._running = False
        self.thread.join()

class BatchProcessor(EventProcessor):
    def _worker(self):
        while self._running:
            batch = []
            while not self.queue.empty() and len(batch) < 10:
                batch.append(self.queue.get())
            
            if batch:
                for _ in batch:
                    pyautogui.click(_pause=False)
            else:
                time.sleep(self.interval)

# Instantiate with batch logic for performance
engine = BatchProcessor()