import os 
import json

def load_config(path='settings.json') -> dict:
    """
    Загружает конфигурационные данные из JSON-файла.
    Args:
        path (str): Путь к файлу конфигурации. По умолчанию 'settings.json'.
    Returns:
        dict: Словарь с настройками программы. Возвращает пустой словарь {}, 
              если файл не найден или поврежден.
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: settings.json not found")
        return {}
    except json.JSONDecodeError:
        print("Error: settings.json is corrupted or empty")
        return {}
    

def load_user_database(file_name) -> dict:
    """
    Загружает базу данных зарегистрированных пользователей из JSON-файла.
    Args:
        file_name (str): Путь к файлу базы данных пользователей.
    Returns:
        dict: Словарь с данными пользователей, где ключи — имена пользователей.
              Возвращает пустой словарь {}, если файл отсутствует или поврежден.
    """
    if not os.path.exists(file_name):
        return {}
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)  
    except json.JSONDecodeError:
        return {}


def add_user_to_file(file_name, user_name, user_password_hash, user_salt):
    """
    Добавляет нового пользователя или обновляет существующего в JSON-файле базы данных.

    Args:
        file_name (str): Путь к файлу базы данных.
        user_name (str): Имя (логин) пользователя.
        user_password_hash (str): Хэшированный пароль пользователя в виде hex-строки.
        user_salt (str): Сгенерированная соль пользователя в виде hex-строки.
    Returns:
        None: Функция ничего не возвращает, записывает данные напрямую в файл.
    """
    users = load_user_database(file_name)
    # Шаг 2: Добавляем или обновляем пользователя в словаре
    users[user_name] = {
        "salt": user_salt,
        "hash": user_password_hash
    }
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    except PermissionError:
        print(f"Error: Access denied to write to {file_name}.")
    except OSError as e:
        print(f"OS Error occurred during saving: {e}")
