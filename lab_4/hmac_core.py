import hashlib
import hmac
from typing import Optional

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


def validate_text(value: Optional[str], field_name: str) -> None:
    """
    Проверить, что текстовое поле не пустое.
    Args:
        value: Проверяемое значение.
        field_name: Название поля для сообщения об ошибке.
    """
    if value is None:
        raise ValueError(f"{field_name} не должен быть None")
    
    if value == "":
        raise ValueError(f"{field_name} не должен быть пустым")
    

def generate_hmac(message: str, secret_key: str) -> str:
    """
    Сформировать HMAC-SHA256 для сообщения.
    Args:
        message: Исходное сообщение.
        secret_key: Секретный ключ.
    Returns:
        HMAC-SHA256 в виде hex-строки.
    """
    validate_text(message,"Сообщение")
    validate_text(secret_key, "Секретный ключ")
    mac = hmac.new(key=secret_key.encode("utf-8"), msg=message.encode("utf-8"), digestmod=hashlib.sha256)
    return mac.hexdigest()


def verify_hmac(message: str, secret_key: str, received_hmac: str) -> bool:
    """
    Проверить корректность HMAC-SHA256.
    Args:
        message: Полученное сообщение.
        secret_key: Секретный ключ.
        received_hmac: HMAC, полученный вместе с сообщением.
    Returns:
        True, если HMAC корректен, иначе False.
    """
    validate_text(message, "Сообщение")
    validate_text(secret_key, "Секретный ключ")
    validate_text(received_hmac, "Полученный HMAC")
    calculated_hmac = generate_hmac(message, secret_key)
    return hmac.compare_digest(calculated_hmac, received_hmac.strip().lower())