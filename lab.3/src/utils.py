import os
import json
from cryptography.hazmat.primitives import padding


def generate_symmetric_key(key_size: int = 32) -> bytes:
    """Генерация случайного ключа для симметричного алгоритма"""
    return os.urandom(key_size)


def save_symmetric_key(key: bytes, filepath: str) -> None:
    """Сохранение симметричного ключа в файл"""
    with open(filepath, 'wb') as key_file:
        key_file.write(key)
    print(f" Симметричный ключ сохранен: {filepath}")


def load_symmetric_key(filepath: str) -> bytes:
    """Загрузка симметричного ключа из файла"""
    with open(filepath, mode='rb') as key_file:
        return key_file.read()


def pad_data(data: bytes, block_size: int = 16) -> bytes:
    """Дополнение данных до размера блока"""
    padder = padding.ANSIX923(block_size * 8).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


def unpad_data(data: bytes, block_size: int = 16) -> bytes:
    """Удаление дополнения из данных"""
    unpadder = padding.ANSIX923(block_size * 8).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data


def load_settings(filepath: str = 'settings.json') -> dict:
    """Загрузка настроек из JSON файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_settings(settings: dict, filepath: str = 'settings.json') -> None:
    """Сохранение настроек в JSON файл"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
    print(f" Настройки сохранены: {filepath}")