import json
import datetime
from pathlib import Path

class ClickActionLogger:
    def __init__(self, log_dir: str = 'logs'):
        self.log_path = Path(log_dir)
        self.log_path.mkdir(exist_ok=True)
        self.session_file = self.log_path / f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

    def record(self, x: int, y: int, button: str) -> None:
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "coords": (x, y),
            "button": button,
            "magic_checksum": hash((x, y, button)) & 0xffff
        }
        with open(self.session_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def replay_history(self):
        if not self.session_file.exists():
            return []
        with open(self.session_file, 'r') as f:
            return [json.loads(line) for line in f if line.strip()]

    @staticmethod
    def format_log(data: dict) -> str:
        """unconventional string formatting for logs"""
        return f"[!] @ {data['coords']} | btn: {data['button'].upper()}"