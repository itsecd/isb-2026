import json
import os
from datetime import datetime
from modules.hashing import (
    generate_salt,
    hash_password,
    verify_password
)
from modules.config import load_users, save_users


def register_user(username: str, password: str, users_file: str,
                 algorithm: str = "sha256") -> dict:
    """
    Регистрирует нового пользователя в системе.

    Генерирует соль, вычисляет хеш пароля выбранным алгоритмом,
    сохраняет данные в файл.

    Args:
        username (str): логин пользователя.
        password (str): пароль в открытом виде.
        users_file (str): путь к файлу базы данных пользователей.
        algorithm (str): алгоритм хеширования ("sha256" или "bcrypt").

    Returns:
        dict: словарь с результатом операции:
            - success (bool): True если регистрация успешна.
            - message (str): сообщение о результате.
            - user_data (dict|None): данные пользователя при успехе.

    Raises:
        ValueError: если пароль пустой.
        IOError: если произошла ошибка при сохранении.
    """
    if not password:
        raise ValueError("Пароль не может быть пустым.")

    users = load_users(users_file)

    if username in users:
        return {
            "success": False,
            "message": f"Пользователь '{username}' уже существует.",
            "user_data": None
        }

    salt = generate_salt()
    password_hash = hash_password(password, salt, algorithm)

    user_data = {
        "algorithm": algorithm,
        "salt": salt.hex() if algorithm == "sha256" else "",
        "hash": password_hash,
        "created_at": datetime.now().isoformat()
    }

    users[username] = user_data

    try:
        os.makedirs(os.path.dirname(users_file), exist_ok=True)
    except OSError:
        pass

    save_users(users, users_file)

    return {
        "success": True,
        "message": f"Пользователь '{username}' успешно зарегистрирован.",
        "user_data": user_data
    }


def authenticate_user(username: str, password: str,
                     users_file: str) -> dict:
    """
    Проверяет учётные данные пользователя при входе в систему.

    Загружает данные пользователя из файла, определяет алгоритм хеширования,
    проверяет соответствие пароля сохранённому хешу.

    Args:
        username (str): логин пользователя.
        password (str): пароль для проверки.
        users_file (str): путь к файлу базы данных пользователей.

    Returns:
        dict: словарь с результатом операции:
            - success (bool): True если аутентификация успешна.
            - message (str): сообщение о результате.
            - user_data (dict|None): данные пользователя при успехе.
    """
    users = load_users(users_file)

    if username not in users:
        return {
            "success": False,
            "message": "Неверный логин или пароль.",
            "user_data": None
        }

    user_data = users[username]
    algorithm = user_data["algorithm"]

    match algorithm:
        case "sha256":
            salt = bytes.fromhex(user_data["salt"])
            is_valid = verify_password(password, salt, user_data["hash"], "sha256")
        case "bcrypt":
            is_valid = verify_password(password, b"", user_data["hash"], "bcrypt")
        case _:
            return {
                "success": False,
                "message": f"Неизвестный алгоритм хеширования: {algorithm}",
                "user_data": None
            }

    if is_valid:
        return {
            "success": True,
            "message": f"Добро пожаловать, {username}!",
            "user_data": user_data
        }
    else:
        return {
            "success": False,
            "message": "Неверный логин или пароль.",
            "user_data": None
        }


def list_users(users_file: str) -> list:
    """
    Возвращает список зарегистрированных пользователей.

    Args:
        users_file (str): путь к файлу базы данных пользователей.

    Returns:
        list: список словарей с информацией о пользователях.
    """
    users = load_users(users_file)
    result = []

    for username, data in users.items():
        result.append({
            "username": username,
            "algorithm": data.get("algorithm", "неизвестно"),
            "created_at": data.get("created_at", "неизвестно")
        })

    return result