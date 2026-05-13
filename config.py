"""Конфигурация приложения - загрузка и сохранение настроек в JSON файлы"""

import os
import json

CRYPTO_CONFIG_FILE = 'crypto_config.json'
SETTINGS_FILE = 'settings.json'


def crypto_config() -> dict:
    """Загружает криптографические константы из crypto_config.json.
    
    Returns:
        dict: Словарь с параметрами из файла.
    
    Raises:
        FileNotFoundError: Если файл crypto_config.json не существует.
    """
    if not os.path.exists(CRYPTO_CONFIG_FILE):
        raise FileNotFoundError(
            f"Файл {CRYPTO_CONFIG_FILE} не найден.\n"
            f"Создайте его с содержимым:\n"
            f'{{\n'
            f'    "block_size": 16,\n'
            f'    "symmetric_key_size": 32,\n'
            f'    "rsa_key_size": 2048,\n'
            f'    "rsa_public_exponent": 65537\n'
            f'}}'
        )
    
    with open(CRYPTO_CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def settings() -> dict:
    """Загружает пользовательские настройки из settings.json.
    
    Returns:
        dict: Словарь с путями к файлам.
    
    Raises:
        FileNotFoundError: Если файл settings.json не существует.
    """
    if not os.path.exists(SETTINGS_FILE):
        raise FileNotFoundError(
            f"Файл {SETTINGS_FILE} не найден.\n"
            f"Создайте его с содержимым:\n"
            f'{{\n'
            f'    "initial_file": "data/plaintext.txt",\n'
            f'    "encrypted_file": "data/encrypted.bin",\n'
            f'    "decrypted_file": "data/decrypted.txt",\n'
            f'    "symmetric_key": "keys/symmetric.key",\n'
            f'    "encrypted_symmetric_key": "keys/encrypted_symmetric.key",\n'
            f'    "public_key": "keys/public.pem",\n'
            f'    "private_key": "keys/private.pem"\n'
            f'}}'
        )
    
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_settings(settings_dict: dict) -> None:
    """Сохраняет настройки путей в файл settings.json.
    
    Args:
        settings_dict: Словарь с настройками для сохранения
    """
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings_dict, f, indent=4, ensure_ascii=False)
    print(f"[OK] Настройки сохранены в {SETTINGS_FILE}")


_crypto_config_cache = None


def get_crypto_config() -> dict:
    """Возвращает криптографические константы (с кэшированием)."""
    global _crypto_config_cache
    if _crypto_config_cache is None:
        _crypto_config_cache = crypto_config()
    return _crypto_config_cache