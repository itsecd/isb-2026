import hashlib


def find_hash_sha256(init_str: str) -> bytes:
    """
    Функция для вычисления хэша по алгоритму SHA256
    Принимает:
        init_str - входные данные
    Возвращает:
        - хэш в байтах
    """
    try:
        res = hashlib.sha256(init_str.encode())
        return res.digest()
    except Exception as e:
        raise AttributeError("Увынск, в процессе хэширования произошла ошибка", e)


def find_shortened_hash(init_hash: bytes, hash_len: int) -> bytes:
    """
    Функция для нахождения укороченного хэша
    Принимает:
        init_hash - изначальный хэш
        hash_len - длина укороченного хэша
    Возвращает:
        - укороченный хэш
    """
    try:
        val = int.from_bytes(init_hash[:4], 'big')
        shortened_hash = val >> (32-hash_len)
        return shortened_hash
    except Exception:
        raise RuntimeError("Длина укороченного хэша должна быть натуральным числом")