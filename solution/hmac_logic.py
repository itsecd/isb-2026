import hmac
import hashlib

def create_hmac(key: str, data: str) -> str:
    """
    Создание hmac подписи
    Входные данные:
    key - ключ
    data - данные
    Возвращает:
    HMAC подпись(str)
    """
    hmac_hash = hmac.new(key.encode('utf-8') , data.encode('utf-8') , hashlib.sha256).hexdigest()
    return hmac_hash

def verify_hmac(key:str, data: str, hmac_hash: str) -> bool:
    """
    Проверка hmac подписи
    Входные данные:
    key - ключ
    data - данные
    hmac_hash - переданная HMAC подпись
    Возвращает:
    bool
    """
    true_hmac = create_hmac(key, data)
    return hmac.compare_digest(true_hmac, hmac_hash)