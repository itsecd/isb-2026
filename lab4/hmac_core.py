"""Модуль с логикой вычисления и проверки HMAC."""
import hmac
import hashlib
from constants import ENCODING


def compute_hmac(message: str, key: str) -> str:
    """Вычисляет HMAC-SHA256 для сообщения с заданным ключом
        Параметры:
        message : str(Исходное сообщение, для которого вычисляется HMAC)
        key : str(Секретный ключ, используемый для вычисления HMAC)
    вернет: str(HMAC в виде hex-строки длиной 64 символа)"""
    if not isinstance(message, str) or not isinstance(key, str):
        raise TypeError("Message and key must be strings")

    try:
        message_bytes = message.encode(ENCODING)
        key_bytes = key.encode(ENCODING)
        hmac_obj = hmac.new(key_bytes, message_bytes, hashlib.sha256)
        return hmac_obj.hexdigest()
    except Exception as e:
        raise RuntimeError(f"Failed to compute HMAC: {e}")


def verify_hmac(message: str, key: str, expected_hmac: str) -> bool:
    """Проверяет, соответствует ли HMAC сообщения ожидаемому значению.
    Использует защищённое сравнение для предотвращения атак по времени.
    Параметры:
    message : str(Исходное сообщение, для которого проверяется HMAC)
    key : str(Секретный ключ, используемый для вычисления HMAC)
    expected_hmac : str(Ожидаемое значение HMAC для сравнения)
    вернет: bool(True - если HMAC совпадает, False - если не совпадает) """
    if not all(isinstance(x, str) for x in [message, key, expected_hmac]):
        raise TypeError("All arguments must be strings")

    try:
        computed = compute_hmac(message, key)
        return hmac.compare_digest(computed, expected_hmac)
    except Exception as e:
        raise RuntimeError(f"Failed to verify HMAC: {e}")