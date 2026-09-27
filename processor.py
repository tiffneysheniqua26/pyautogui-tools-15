import pyautogui
import time
import collections
from threading import Thread

class EventProcessor:
    def __init__(self, buffer_size=1024):
        self.queue = collections.deque(maxlen=buffer_size)
        self.active = True

    def schedule_click(self, x, y):
        self.queue.append((x, y))

    def process_burst(self):
        while self.active and self.queue:
            pos = self.queue.popleft()
            pyautogui.click(pos[0], pos[1])

    def run_worker(self):
        while self.active:
            if self.queue:
                self.process_burst()
            else:
                time.sleep(0.001)

    def start(self):
        self.thread = Thread(target=self.run_worker, daemon=True)
        self.thread.start()

    def stop(self):
        self.active = False
        self.thread.join()

def optimized_click_factory():
    proc = EventProcessor()
    pyautogui.PAUSE = 0
    return proc