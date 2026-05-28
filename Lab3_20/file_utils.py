"""Модуль для работы с файлами"""

import os
import json
from typing import Any, Dict


def read_binary_file(file_path: str) -> bytes:
    """Читает данные из бинарного файла."""
    try:
        match os.path.exists(file_path):
            case False:
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            case _:
                pass
        
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise
    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла: {file_path}")
    except Exception as e:
        raise Exception(f"Ошибка чтения файла {file_path}: {str(e)}")


def write_binary_file(file_path: str, data: bytes) -> bool:
    """Записывает байтовые данные в бинарный файл."""
    try:
        directory = os.path.dirname(file_path)
        match directory:
            case "":
                pass
            case _:
                os.makedirs(directory, exist_ok=True)
        
        with open(file_path, 'wb') as f:
            f.write(data)
        return True
    except PermissionError:
        raise PermissionError(f"Нет прав на запись в файл: {file_path}")
    except Exception as e:
        raise Exception(f"Ошибка записи файла {file_path}: {str(e)}")


def read_text_file(file_path: str, encoding: str = 'utf-8') -> str:
    """Читает данные из текстового файла."""
    try:
        match os.path.exists(file_path):
            case False:
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            case _:
                pass
        
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise
    except Exception as e:
        raise Exception(f"Ошибка чтения файла {file_path}: {str(e)}")


def write_text_file(file_path: str, data: str, encoding: str = 'utf-8') -> bool:
    """Записывает текстовые данные в файл."""
    try:
        directory = os.path.dirname(file_path)
        match directory:
            case "":
                pass
            case _:
                os.makedirs(directory, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(data)
        return True
    except Exception as e:
        raise Exception(f"Ошибка записи файла {file_path}: {str(e)}")


def load_json_settings(file_path: str, default_settings: Dict[str, Any] = None) -> Dict[str, Any]:
    """Загружает настройки из JSON файла."""
    required_fields = [
        "initial_file", "encrypted_file", "decrypted_file",
        "symmetric_key_encrypted", "public_key", "private_key"
    ]
    
    default = default_settings or {
        "initial_file": "data/input.txt",
        "encrypted_file": "data/encrypted.bin",
        "decrypted_file": "data/decrypted.txt",
        "symmetric_key_encrypted": "keys/symmetric.key.enc",
        "public_key": "keys/public.pem",
        "private_key": "keys/private.pem"
    }
    
    try:
        match os.path.exists(file_path):
            case True:
                with open(file_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                for key in required_fields:
                    match key in settings:
                        case False:
                            settings[key] = default.get(key, "")
                        case _:
                            pass
                
                return settings
            case False:
                write_text_file(file_path, json.dumps(default, indent=4))
                return default.copy()
                
    except json.JSONDecodeError as e:
        raise Exception(f"Ошибка парсинга JSON файла {file_path}: {str(e)}")
    except Exception as e:
        raise Exception(f"Ошибка загрузки настроек: {str(e)}")


def save_json_settings(file_path: str, settings: Dict[str, Any]) -> bool:
    """Сохраняет настройки в JSON файл."""
    try:
        write_text_file(file_path, json.dumps(settings, indent=4, ensure_ascii=False))
        return True
    except Exception as e:
        raise Exception(f"Ошибка сохранения настроек: {str(e)}")


def get_file_size_str(file_path: str) -> str:
    """Возвращает размер файла в удобочитаемом формате."""
    try:
        match os.path.exists(file_path):
            case False:
                return "Не указан"
            case _:
                pass
        
        size = os.path.getsize(file_path)
        
        match size:
            case n if n < 1024:
                return f"{size} B"
            case n if n < 1024 * 1024:
                return f"{size / 1024:.2f} KB"
            case _:
                return f"{size / (1024 * 1024):.2f} MB"
    except Exception:
        return "Ошибка"