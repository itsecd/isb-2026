import json
import sys


def load_settings(settings_path: str = "settings.json") -> dict:
    """
    Загружает глобальные настройки приложения из JSON-файла.

    Args:
        settings_path (str): путь к файлу настроек. По умолчанию "settings.json".

    Returns:
        dict: словарь с настройками приложения.

    Raises:
        FileNotFoundError: если файл настроек не найден.
        json.JSONDecodeError: если файл содержит некорректный JSON.

    Если файл не найден, возвращаются настройки по умолчанию.
    """
    default_settings = {
        "default_symmetric_key_size": 256,
        "default_rsa_key_size": 2048,
        "rsa_public_exponent": 65537,
        "symmetric_padding": "ANSIX923",
        "hash_algorithm": "SHA256",
        "encoding": "utf-8"
    }
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            print(f"Настройки загружены из {settings_path}")
            return settings
    except FileNotFoundError:
        print(f"Файл настроек {settings_path} не найден. Использую настройки по умолчанию.")
        return default_settings
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON в файле {settings_path}: {e}")
        print("Использую настройки по умолчанию.")
        return default_settings
    except IOError as e:
        print(f"Ошибка ввода-вывода при чтении {settings_path}: {e}")
        print("Использую настройки по умолчанию.")
        return default_settings


def read_config(config_path: str) -> dict:
    """
    Читает конфигурационный JSON-файл для определённого режима работы.

    Args:
        config_path (str): путь к JSON-файлу конфигурации.

    Returns:
        dict: словарь с параметрами конфигурации.

    Raises:
        SystemExit: если файл не найден или содержит некорректный JSON.
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"Конфигурация загружена из {config_path}")
            return config
    except FileNotFoundError:
        print(f"Ошибка: файл конфигурации {config_path} не найден.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Ошибка: некорректный JSON в файле {config_path}: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка ввода-вывода при чтении {config_path}: {e}")
        sys.exit(1)


def validate_symmetric_key_size(bits: int) -> int:
    """
    Проверяет корректность выбранной длины симметричного ключа.

    Args:
        bits (int): желаемая длина ключа в битах.

    Returns:
        int: корректная длина ключа (128, 192 или 256).

    Если передано некорректное значение, возвращается 256 (по умолчанию).
    """
    allowed_sizes = (128, 192, 256)
    if bits in allowed_sizes:
        return bits
    print(f"Некорректная длина ключа {bits} бит. Использую 256 бит.")
    return 256