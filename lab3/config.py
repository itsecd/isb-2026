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
        DEFAULT_CONFIG_PATH (str): Путь к конфигу по умолчанию.
    """

    DEFAULT_CONFIG_PATH: str = "settings.json"

    REQUIRED_KEYS: tuple = (
        'initial_file',
        'encrypted_file',
        'decrypted_file',
        'symmetric_key',
        'public_key',
        'private_key',
        'seed_block_size',
        'seed_key_size',
        'seed_iv_size',
        'rsa_key_size',
        'rsa_public_exponent',
        'encoding'
    )

    def __init__(self, config_path: str = None) -> None:
        """
        Инициализирует менеджер конфигурации и загружает настройки.

        Аргументы:
            config_path: Путь к JSON-файлу с настройками.
                         Если None, используется DEFAULT_CONFIG_PATH.

        Исключения:
            ConfigError: Если файл не найден, повреждён или неполон.
        """
        if config_path is None:
            config_path = self.DEFAULT_CONFIG_PATH
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
                f"Файл конфигурации '{self._config_path}' не найден."
            )
        except json.JSONDecodeError as exc:
            raise ConfigError(
                f"Файл '{self._config_path}' содержит некорректный JSON: {exc}"
            )

        missing = [key for key in self.REQUIRED_KEYS if key not in settings]
        if missing:
            raise ConfigError(
                f"Отсутствуют обязательные ключи: {', '.join(missing)}"
            )

        return settings

    @property
    def settings(self) -> dict:
        """
        Возвращает все настройки словарём.

        Возвращает:
            dict: Полный словарь настроек.
        """
        return self._settings

    @property
    def initial_file(self) -> str:
        """Возвращает путь к исходному файлу."""
        return self._settings['initial_file']

    @property
    def encrypted_file(self) -> str:
        """Возвращает путь к зашифрованному файлу."""
        return self._settings['encrypted_file']

    @property
    def decrypted_file(self) -> str:
        """Возвращает путь к расшифрованному файлу."""
        return self._settings['decrypted_file']

    @property
    def symmetric_key(self) -> str:
        """Возвращает путь к зашифрованному симметричному ключу."""
        return self._settings['symmetric_key']

    @property
    def public_key(self) -> str:
        """Возвращает путь к публичному RSA-ключу."""
        return self._settings['public_key']

    @property
    def private_key(self) -> str:
        """Возвращает путь к приватному RSA-ключу."""
        return self._settings['private_key']

    @property
    def seed_block_size(self) -> int:
        """Возвращает размер блока SEED в битах."""
        return self._settings['seed_block_size']

    @property
    def seed_key_size(self) -> int:
        """Возвращает размер ключа SEED в байтах."""
        return self._settings['seed_key_size']

    @property
    def seed_iv_size(self) -> int:
        """Возвращает размер IV SEED в байтах."""
        return self._settings['seed_iv_size']

    @property
    def rsa_key_size(self) -> int:
        """Возвращает размер RSA-ключа в битах."""
        return self._settings['rsa_key_size']

    @property
    def rsa_public_exponent(self) -> int:
        """Возвращает публичную экспоненту RSA."""
        return self._settings['rsa_public_exponent']

    @property
    def encoding(self) -> str:
        """Возвращает кодировку для текстовых файлов."""
        return self._settings['encoding']

    def ensure_directories(self) -> None:
        """
        Создаёт все необходимые директории для файлов из конфигурации.

        Если директория уже существует, ничего не делает.
        """
        for key in ('initial_file', 'encrypted_file', 'decrypted_file',
                    'symmetric_key', 'public_key', 'private_key'):
            Path(self._settings[key]).parent.mkdir(parents=True, exist_ok=True)