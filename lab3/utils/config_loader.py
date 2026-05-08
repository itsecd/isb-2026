import json
import os
from typing import Dict, Any


class ConfigLoader:
    """Класс под загрузку файла настроек"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load(self, config_path: str = "config.json") -> Dict[str, Any]:
        """Загрузка файла настроек из файла"""
        if self._config is not None:
            return self._config
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            return self._config
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл настроек не найден: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Неверный json в файле настроек: {e}")
    
    def get_path(self, key: str) -> str:
        """Получение пути из конфига (относительно keys_directory)"""
        if self._config is None:
            raise ValueError("Настройки не загружены")
        
        paths = self._config.get('paths')
        if paths is None:
            raise KeyError("Секция 'paths' не найдена в настройках")
        
        keys_dir = paths.get('keys_directory')
        if keys_dir is None:
            raise KeyError("Параметр 'keys_directory' не найден в секции 'paths'")
        
        filename = paths.get(key)
        if filename is None:
            raise KeyError(f"Параметр '{key}' не найден в секции 'paths'")
        
        return os.path.join(keys_dir, filename)
    
    def get_crypto_param(self, key: str):
        """Получение криптографического параметра"""
        if self._config is None:
            raise ValueError("Настройки не загружены")
        
        crypto = self._config.get('crypto')
        if crypto is None:
            raise KeyError("Секция 'crypto' не найдена в настройках")
        
        value = crypto.get(key)
        if value is None:
            raise KeyError(f"Параметр '{key}' не найден в секции 'crypto'")
        
        return value
    
    def get_ui_param(self, key: str):
        """Получение UI параметра"""
        if self._config is None:
            raise ValueError("Настройки не загружены")
        
        ui = self._config.get('ui')
        if ui is None:
            raise KeyError("Секция 'ui' не найдена в настройках")
        
        value = ui.get(key)
        if value is None:
            raise KeyError(f"Параметр '{key}' не найден в секции 'ui'")
        
        return value