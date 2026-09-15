import os
from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    APP_NAME: str = 'pyautogui-tools-15'
    CLICK_INTERVAL: float = 0.1
    DEFAULT_KEY: str = 'f9'
    LOG_FILE: str = 'automation.log'

class ConfigRegistry:
    def __init__(self):
        self._store = {k: v for k, v in AppConfig.__dict__.items() if not k.startswith('__')}

    def get(self, key: str, fallback=None):
        return self._store.get(key, fallback)

    def update_from_env(self):
        for key in self._store:
            env_val = os.getenv(f'AUTO_{key}')
            if env_val:
                self._store[key] = type(self._store[key])(env_val)

    @property
    def settings(self):
        return self._store

settings = ConfigRegistry()
settings.update_from_env()

def get_setting(key: str):
    return settings.get(key)