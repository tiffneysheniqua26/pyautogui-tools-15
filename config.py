import os
import json
import ast
from typing import Any, get_type_hints

class ConfigLoader:
    """Creative autoclicker config loader using type hints for auto-coercion."""
    
    delay: float = 0.1
    clicks: int = 100
    button: str = 'left'
    hotkey: str = 'f8'
    coords: tuple = (100, 100)
    
    def __init__(self, filepath: str = "autoclick_config.json"):
        self._filepath = filepath
        self._data = {}
        self.load()

    def load(self) -> None:
        if not os.path.exists(self._filepath):
            self._data = {
                k: getattr(self, k) 
                for k in get_type_hints(self).keys() 
                if not k.startswith('_')
            }
            self.save()
            return
            
        try:
            with open(self._filepath, 'r') as f:
                raw_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            raw_data = {}
            
        hints = get_type_hints(self)
        for key, expected_type in hints.items():
            if key.startswith('_'):
                continue
            val = raw_data.get(key, getattr(self.__class__, key))
            
            if isinstance(val, str) and expected_type is tuple:
                try:
                    val = ast.literal_eval(val)
                except (ValueError, SyntaxError):
                    val = getattr(self.__class__, key)
                    
            try:
                self._data[key] = expected_type(val)
            except (TypeError, ValueError):
                self._data[key] = getattr(self.__class__, key)

    def save(self) -> None:
        try:
            with open(self._filepath, 'w') as f:
                json.dump(self._data, f, indent=4)
        except IOError:
            pass

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'ConfigLoader' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
            self.save()