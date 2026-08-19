from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Config:
    interval: float  # time interval between clicks in seconds
    button: str      # mouse button to click
    repetitions: int  # number of clicks to perform
    timeout: float   # timeout for the clicking session

    def to_dict(self) -> Dict[str, Any]:
        """Convert the config to a dictionary."""
        return {
            'interval': self.interval,
            'button': self.button,
            'repetitions': self.repetitions,
            'timeout': self.timeout
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create a Config instance from a dictionary."""
        return cls(
            interval=config_dict.get('interval', 0.1),
            button=config_dict.get('button', 'left'),
            repetitions=config_dict.get('repetitions', 10),
            timeout=config_dict.get('timeout', 10)
        )

config = Config(interval=0.1, button='left', repetitions=10, timeout=10)
