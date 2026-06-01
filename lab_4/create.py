import hashlib
import hmac

def create(text: str, secret_key: str) -> str:
    """
    Формирует HMAC-SHA256 подпись для исходного текстового сообщения.

    Args:
        text (str): Исходный текст сообщения.
        secret_key (str): Секретный ключ аутентификации.
    """
    if not isinstance(text, str) or not isinstance(secret_key, str):
        raise TypeError("Текст сообщения и секретный ключ должны быть строками.")
    
    if not text or not secret_key:
        raise ValueError("Текст сообщения или секретный ключ не могут быть пустыми.")

    text_utf = text.encode('utf-8')
    key_utf = secret_key.encode('utf-8')
    hmac_new = hmac.new(key_utf, text_utf, hashlib.sha256)
    return hmac_new.hexdigest()

def verify(text: str, secret_key: str, hmac_hex: str) -> bool:
    """
    Проверяет подлинность и соответствие HMAC подписи для текста.

    Args:
        text (str): Исходный текст сообщения.
        secret_key (str): Секретный ключ аутентификации.
        hmac_hex (str): Проверяемая hex-строка подписи.
    """
    if not isinstance(hmac_hex, str):
        raise TypeError("Переданный HMAC-хэш должен быть строкой.")
        
    hmac_h = create(text, secret_key)
    return hmac.compare_digest(hmac_hex, hmac_h)