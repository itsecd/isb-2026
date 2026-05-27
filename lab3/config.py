"""
Модуль для работы с конфигурацией приложения.

Загружает настройки из JSON-файла и проверяет
наличие всех обязательных ключей.
"""

import json
from pathlib import Path
from exceptions import ConfigError


class ConfigManager:
    """
    Класс для управления конфигурацией гибридной криптосистемы.

    Инкапсулирует логику загрузки и валидации настроек из JSON-файла,
    а также создание необходимых директорий.

    Атрибуты:
        REQUIRED_KEYS (tuple): Обязательные ключи в файле конфигурации.
    """

    REQUIRED_KEYS: tuple = (
        'initial_file', 'encrypted_file', 'decrypted_file',
        'symmetric_key', 'public_key', 'private_key'
    )

    def __init__(self, config_path: str = "settings.json") -> None:
        """
        Инициализирует менеджер конфигурации и загружает настройки.

        Аргументы:
            config_path: Путь к JSON-файлу с настройками.

        Исключения:
            ConfigError: Если файл не найден, повреждён или неполон.
        """
        self._config_path = config_path
        self._settings = self._load()

    def _load(self) -> dict:
        """
        Загружает и валидирует JSON-файл конфигурации.

        Возвращает:
            dict: Словарь с настройками.

        Исключения:
            ConfigError: При ошибках загрузки или валидации.
        """
        try:
            with open(self._config_path, 'r', encoding='utf-8') as file:
                settings = json.load(file)
        except FileNotFoundError:
            raise ConfigError(
                f"Файл конфигурации '{self._config_path}' не найден. "
                f"Убедитесь, что файл существует в корне проекта."
            )
        except json.JSONDecodeError as exc:
            raise ConfigError(
                f"Файл '{self._config_path}' содержит некорректный JSON: {exc}"
            )

        missing = [key for key in self.REQUIRED_KEYS if key not in settings]
        if missing:
            raise ConfigError(
                f"В файле '{self._config_path}'"
                f" отсутствуют обязательные ключи: "
                f"{', '.join(missing)}"
            )

        return settings

    def get(self, key: str) -> str:
        """
        Возвращает значение настройки по ключу.

        Аргументы:
            key: Ключ настройки.

        Возвращает:
            str: Значение настройки (путь к файлу).
        """
        return self._settings[key]

    def ensure_directories(self) -> None:
        """
        Создаёт все необходимые директории для файлов из конфигурации.

        Если директория уже существует, ничего не делает.
        """
        for path in self._settings.values():
            Path(path).parent.mkdir(parents=True, exist_ok=True)