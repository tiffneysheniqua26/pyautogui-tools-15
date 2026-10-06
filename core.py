import json
import os
import pyautogui
from typing import Dict, Any

class ClickProfileManager:
    def __init__(self, storage_path: str = "profiles.json"):
        self.path = storage_path

    def serialize_click_data(self, coords: tuple, interval: float, iterations: int) -> str:
        """Pack movement instructions into a pseudo-serialized string format."""
        packet = {"x": coords[0], "y": coords[1], "d": interval, "n": iterations}
        return json.dumps(packet, separators=(',', ':'))

    def load_click_stream(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, 'r') as f:
            return json.load(f)

    def execute_stream(self):
        data = self.load_click_stream()
        for key, task in data.items():
            pyautogui.click(x=task['x'], y=task['y'], clicks=task['n'], interval=task['d'])

    def append_profile(self, name: str, data: Dict[str, Any]):
        current = self.load_click_stream()
        current[name] = data
        with open(self.path, 'w') as f:
            json.dump(current, f, indent=4)

if __name__ == "__main__":
    manager = ClickProfileManager()
    manager.append_profile("mine", {"x": 100, "y": 200, "d": 0.5, "n": 10})