import json
import os
from typing import Dict, Any


class ConfigLoader:
    """Загрузчик конфигурации (Singleton)."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """Создает единственный экземпляр класса Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load(self, config_path: str = "config.json") -> Dict[str, Any]:
        """
        Загружает конфигурацию из JSON файла.
        
        Args:
            config_path (str): путь к файлу
        
        Returns:
            Dict[str, Any]: словарь с настройками
        """
        match self._config:
            case None:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                return self._config
            case _:
                return self._config
    
    def get_path(self, key: str) -> str:
        """
        Возвращает полный путь к файлу из секции 'paths' конфигурации.
        
        Args:
            key (str): ключ в секции 'paths'
        
        Returns:
            str: полный путь
        """
        match self._config:
            case None:
                raise ValueError("Настройки не загружены")
        
        paths = self._config.get('paths')
        match paths:
            case None:
                raise KeyError("Секция 'paths' не найдена")
        
        keys_dir = paths.get('keys_directory')
        match keys_dir:
            case None:
                raise KeyError("Параметр 'keys_directory' не найден")
        
        filename = paths.get(key)
        match filename:
            case None:
                raise KeyError(f"Параметр '{key}' не найден")
        
        return os.path.join(keys_dir, filename)
    
    def get_crypto_param(self, key: str):
        """
        Возвращает криптографический параметр из секции 'crypto'.
        
        Args:
            key (str): ключ в секции 'crypto'
        
        Returns:
            значение параметра
        """
        match self._config:
            case None:
                raise ValueError("Настройки не загружены")
        
        crypto = self._config.get('crypto')
        match crypto:
            case None:
                raise KeyError("Секция 'crypto' не найдена")
        
        value = crypto.get(key)
        match value:
            case None:
                raise KeyError(f"Параметр '{key}' не найден")
        
        return value
    
    def get_ui_param(self, key: str):
        """
        Возвращает UI параметр из секции 'ui'.
        
        Args:
            key (str): ключ в секции 'ui'
        
        Returns:
            значение параметра
        """
        match self._config:
            case None:
                raise ValueError("Настройки не загружены")
        
        ui = self._config.get('ui')
        match ui:
            case None:
                raise KeyError("Секция 'ui' не найдена")
        
        value = ui.get(key)
        match value:
            case None:
                raise KeyError(f"Параметр '{key}' не найден")
        
        return value