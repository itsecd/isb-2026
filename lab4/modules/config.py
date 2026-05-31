import json
import sys


def load_settings(settings_path: str = "settings.json") -> dict:
    """
    Загружает глобальные настройки приложения из JSON-файла.

    Args:
        settings_path (str): путь к файлу настроек. По умолчанию "settings.json".

    Returns:
        dict: словарь с настройками приложения.

    Если файл не найден, возвращаются настройки по умолчанию.
    """
    default_settings = {
        "users_file": "data/users.json",
        "default_hash_algorithm": "sha256",
        "salt_length": 16,
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


def load_users(users_file: str) -> dict:
    """
    Загружает базу данных пользователей из JSON-файла.

    Args:
        users_file (str): путь к файлу с данными пользователей.

    Returns:
        dict: словарь с данными пользователей. Пустой словарь если файл не найден.
    """
    try:
        with open(users_file, 'r', encoding='utf-8') as f:
            users = json.load(f)
            print(f"База пользователей загружена из {users_file}")
            return users
    except FileNotFoundError:
        print(f"Файл {users_file} не найден. Создаю новую базу.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON в файле {users_file}: {e}")
        print("База повреждена. Создаю новую.")
        return {}
    except IOError as e:
        print(f"Ошибка ввода-вывода при чтении {users_file}: {e}")
        return {}


def save_users(users: dict, users_file: str) -> None:
    """
    Сохраняет базу данных пользователей в JSON-файл.

    Args:
        users (dict): словарь с данными пользователей.
        users_file (str): путь к файлу для сохранения.

    Raises:
        IOError: если произошла ошибка при записи файла.
    """
    try:
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        print(f"База пользователей сохранена в {users_file}")
    except IOError as e:
        print(f"Ошибка при сохранении базы пользователей в {users_file}: {e}")
        raise