import os
import hashlib


def generate_salt(length: int = 16) -> str:
    """Генерирует случайную соль.

    Args:
        length (int): Длина соли в байтах.

    Returns:
        str: Соль в виде шестнадцатеричной строки.

    Raises:
        ValueError: Если длина соли не положительна.
    """
    if length <= 0:
        raise ValueError("Длина соли должна быть положительной.")
    return os.urandom(length).hex()


def calculate_hash(password: str, salt: str = None) -> str:
    """Вычисляет SHA-256 хеш пароля с опциональной солью.

    Args:
        password (str): Пароль пользователя.
        salt (str, optional): Соль в виде шестнадцатеричной строки.

    Returns:
        str: 64-символьная шестнадцатеричная строка хеша.
    """
    data = password if salt is None else password + salt
    return hashlib.sha256(data.encode('utf-8')).hexdigest()