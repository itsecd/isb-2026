"""Модуль аутентификации пользователей."""

from typing import Optional
from hash_utils import generate_salt, calculate_hash
from db_utils import safe_load, write_json


def register_user(
    login: str,
    password: str,
    db_path: str,
    use_salt: bool = True
) -> str:
    """Регистрирует нового пользователя в базе данных.

    Args:
        login (str): Логин пользователя.
        password (str): Пароль пользователя.
        db_path (str): Путь к JSON-файлу базы данных.
        use_salt (bool): Использовать соль (True — безопасный режим,
            False — небезопасный).

    Returns:
        str: Сообщение о результате регистрации.

    Raises:
        ValueError: Если логин или пароль пусты.
    """
    if not login or not password:
        raise ValueError("Логин и пароль не могут быть пустыми.")

    database = safe_load(db_path)
    if database is None:
        return "Ошибка: база данных повреждена."

    if login in database:
        return f"Пользователь '{login}' уже существует."

    match use_salt:
        case True:
            salt = generate_salt()
            password_hash = calculate_hash(password, salt)
            database[login] = {"hash": password_hash, "salt": salt}
        case False:
            password_hash = calculate_hash(password)
            database[login] = password_hash

    write_json(db_path, database)
    return f"Пользователь '{login}' успешно зарегистрирован."


def authenticate_user(
    login: str,
    password: str,
    db_path: str,
    use_salt: bool = True
) -> str:
    """Авторизует пользователя.

    Args:
        login (str): Логин пользователя.
        password (str): Пароль пользователя.
        db_path (str): Путь к JSON-файлу базы данных.
        use_salt (bool): Режим проверки (True — безопасный, False — небезопасный).

    Returns:
        str: Сообщение о результате авторизации.
    """
    if not login or not password:
        raise ValueError("Логин и пароль не могут быть пустыми.")

    database = safe_load(db_path)
    match database:
        case None:
            return "Ошибка: база данных повреждена."
        case _ if not database:
            return "В системе нет зарегистрированных пользователей."

    if login not in database:
        return f"Пользователь '{login}' не найден."

    user_data = database[login]

    match use_salt:
        case True:
            match user_data:
                case {"salt": _, "hash": _}:
                    password_hash = calculate_hash(password, user_data["salt"])
                    match password_hash == user_data["hash"]:
                        case True:
                            return f"Добро пожаловать, {login}!"
                        case False:
                            return "Неверный пароль."
                case _:
                    return "Ошибка: структура данных пользователя нарушена."
        case False:
            match user_data:
                case str():
                    password_hash = calculate_hash(password)
                    match password_hash == user_data:
                        case True:
                            return f"Добро пожаловать, {login}!"
                        case False:
                            return "Неверный пароль."
                case _:
                    return "Ошибка: структура данных пользователя нарушена."