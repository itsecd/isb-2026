import json
import os


def load_settings(config_path):
    """
    Загрузить настройки из JSON файла
    
    Args:
        config_path: путь к JSON файлу
    
    Returns:
        dict: загруженные настройки
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {config_path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {config_path}: {e}") from e
    except PermissionError as e:
        raise PermissionError(f"Read permission denied: {config_path}") from e
    except OSError as e:
        raise OSError(f"Failed to load config from {config_path}: {e}") from e
    
    print(f"[+] Настройки загружены из {config_path}")
    return settings


def save_settings(settings, config_path):
    """
    Сохранить настройки в JSON файл
    
    Args:
        settings: словарь с настройками
        config_path: путь для сохранения JSON файла
    """
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except PermissionError as e:
        raise PermissionError(f"Write permission denied: {config_path}") from e
    except OSError as e:
        raise OSError(f"Failed to save config to {config_path}: {e}") from e
    
    print(f"[+] Настройки сохранены в {config_path}")