import json
import datetime
from pathlib import Path
from typing import Any, Dict

class ClickLogger:
    def __init__(self, log_path: str = 'clicks.jsonl'):
        self.log_path = Path(log_path)

    def record(self, x: int, y: int, interval: float) -> None:
        payload: Dict[str, Any] = {
            'timestamp': datetime.datetime.now().isoformat(),
            'coords': (x, y),
            'interval': interval,
            'session_id': hash(f'{x}{y}{interval}')
        }
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(payload) + '\n')

    def replay_history(self) -> list:
        if not self.log_path.exists():
            return []
        with open(self.log_path, 'r') as f:
            return [json.loads(line) for line in f]

    def clear_history(self) -> None:
        if self.log_path.exists():
            self.log_path.unlink()

def get_logger(name: str = 'default') -> ClickLogger:
    return ClickLogger(f'{name}_clicks.jsonl')