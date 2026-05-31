import json
import os


class FileUtilsError(Exception):
    """Исключение для ошибок при работе с файлами и директориями"""
    pass


def read_bytes(path: str) -> bytes:
    """
    Считывает данные из файла.
    
    Args:
        path (str): Путь к файлу для чтения
    
    Returns:
        bytes: Содержимое файла в виде байтов
    
    Raises:
        FileUtilsError: Если файл не найден, недостаточно прав или другая ошибка ввода/вывода
    """
    try:
        with open(path, 'rb') as file:
            return file.read()
    except FileNotFoundError as err:
        raise FileUtilsError(f"Файл не найден: {path}") from err
    except PermissionError as err:
        raise FileUtilsError(f"Недостаточно прав для чтения файла: {path}") from err
    except Exception as err:
        raise FileUtilsError(f"Ошибка при чтении файла {path}: {err}") from err


def write_bytes(path: str, data: bytes) -> None:
    """
    Записывает данные в файл.
    
    Args:
        path (str): Путь к файлу для записи
        data (bytes): Данные для записи
    
    Raises:
        FileUtilsError: Если директория не найдена, недостаточно прав или другая ошибка ввода/вывода
    """
    try:
        with open(path, 'wb') as file:
            file.write(data)
    except FileNotFoundError as err:
        raise FileUtilsError(f"Путь не найден: {path}") from err
    except PermissionError as err:
        raise FileUtilsError(f"Недостаточно прав для записи в файл: {path}") from err
    except Exception as err:
        raise FileUtilsError(f"Ошибка при записи в файл {path}: {err}") from err


def load_settings(setting_file: str = 'settings.json') -> dict:
    """
    Загружает настройки из JSON файла. Если файл не существует, создаёт его с настройками по умолчанию.
    
    Args:
        setting_file (str): Путь к JSON файлу с настройками. По умолчанию 'settings.json'
    
    Returns:
        dict: Словарь с настройками
    
    Raises:
        FileUtilsError: Если файл JSON повреждён или произошла ошибка при чтении/записи
    """
    if not os.path.exists(setting_file):
        default_settings = {
            'initial_file': 'test.txt',
            'encrypted_file': 'encrypted.bin',
            'decrypted_file': 'decrypted.txt',
            'symmetric_key': 'symmetric_key.bin',
            'public_key': 'public_key.pem',
            'secret_key': 'secret_key.pem',
            'symmetric_key_length': 128
        }
        save_settings(setting_file, default_settings)
        return default_settings
    
    try:
        with open(setting_file, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except Exception as err:
        raise FileUtilsError(f"Ошибка при чтении JSON файла {setting_file}: {err}") from err


def save_settings(path: str, data: dict) -> None:
    """
    Сохраняет настройки в JSON файл.
    
    Args:
        path (str): Путь для сохранения JSON файла
        data (dict): Словарь с настройками для сохранения
    
    Raises:
        FileUtilsError: Если произошла ошибка при сериализации или записи в файл
    """
    try:
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)
    except Exception as err:
        raise FileUtilsError(f"Ошибка при записи JSON файла {path}: {err}") from err
