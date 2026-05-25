"""
Модуль для вычисления и проверки HMAC-SHA256.

Функции:
- build_hmac() — создание HMAC;
- check_hmac() — проверка подлинности сообщения.
"""

import hashlib
import hmac

from settings import TEXT_ENCODING


def build_hmac(text: str, secret: str) -> str:
    """
    Создаёт HMAC-SHA256 для переданного сообщения.

    Args:
        text (str):
            Исходное сообщение.

        secret (str):
            Секретный ключ.

    Returns:
        str:
            HMAC в шестнадцатеричном формате.

    Raises:
        TypeError:
            Если параметры не являются строками.

        RuntimeError:
            Если произошла ошибка при вычислении HMAC.
    """

    if not isinstance(text, str):
        raise TypeError("Сообщение должно быть строкой")

    if not isinstance(secret, str):
        raise TypeError("Ключ должен быть строкой")

    try:
        text_bytes = text.encode(TEXT_ENCODING)
        key_bytes = secret.encode(TEXT_ENCODING)

        signature = hmac.new(key_bytes, text_bytes, hashlib.sha256)

        return signature.hexdigest()

    except Exception as error:
        raise RuntimeError(f"Ошибка вычисления HMAC: {error}")


def check_hmac(text: str, secret: str, original_hmac: str) -> bool:
    """
    Проверяет корректность HMAC.

    Args:
        text (str):
            Проверяемое сообщение.

        secret (str):
            Секретный ключ.

        original_hmac (str):
            Исходный HMAC для сравнения.

    Returns:
        bool:
            True — если HMAC совпадает.
            False — если данные были изменены.

    Raises:
        TypeError:
            Если аргументы имеют неверный тип.

        RuntimeError:
            При ошибке проверки.
    """

    if not all(isinstance(value, str) for value in [text, secret, original_hmac]):
        raise TypeError("Все параметры должны быть строками")

    try:
        calculated = build_hmac(text, secret)

        return hmac.compare_digest(calculated, original_hmac)

    except Exception as error:
        raise RuntimeError(f"Ошибка проверки HMAC: {error}")
