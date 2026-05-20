"""Модуль с логикой вычисления и проверки HMAC."""
import hmac
import hashlib
from constants import ENCODING


def compute_hmac(message: str, key: str) -> str:
    """Вычисляет HMAC-SHA256 для сообщения с заданным ключом."""
    if not isinstance(message, str) or not isinstance(key, str):
        raise TypeError("Message and key must be strings")

    message_bytes = message.encode(ENCODING)
    key_bytes = key.encode(ENCODING)
    hmac_obj = hmac.new(key_bytes, message_bytes, hashlib.sha256)
    return hmac_obj.hexdigest()


def verify_hmac(message: str, key: str, expected_hmac: str) -> bool:
    """Проверяет соответствие HMAC сообщения ожидаемому значению."""
    if not all(isinstance(x, str) for x in [message, key, expected_hmac]):
        raise TypeError("All arguments must be strings")

    computed = compute_hmac(message, key)
    return hmac.compare_digest(computed, expected_hmac)