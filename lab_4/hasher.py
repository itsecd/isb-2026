import hashlib
import os
import bcrypt

def hash_simple(password : str) -> dict:
    """
    Принимает: пароль
    Возвращает: словарь с алгоритмом и значением хэша
    """
    digest =  hashlib.sha256(password.encode('utf-8')).hexdigest()
    return {"algo": "sha256", "hash": digest}

def generate_salt() -> bytes:
    """
    Генерирует соль (случайные 16 байт)
    """
    salt = os.urandom(16)
    return salt

def hash_salted(password : str) -> dict:
    """
    генерирует хэш пароля с солью, использует алгоритм SHA-256
    Принимает : пароль
    Возвращает : словарь с алгоритмом и значением хэша
    """
    salt = generate_salt()
    salt_hex = salt.hex()
    digest = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()

    return {"algo": "sha256_salted", "salt": salt_hex, "hash": digest}

def hash_bcrypt(password : str) -> dict:
    """
    Генерирует bcrypt хэш пароля
    Принимает: Пароль
    Возвращает:  словарь с алгоритмом и значением хэша
    """

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

    return {"algo": "bcrypt", "hash": hashed.decode('utf-8')}

def get_hasher(algo: str):
    """
    Получает нужный алгоритм хэширования
    Принимает: Строку с алгоритмом
    Возвращает: Фунцию хэширования
    """
    if algo == "sha256":
        return hash_simple
    elif algo == "sha256_salted":
        return hash_salted
    elif algo == "bcrypt":
        return hash_bcrypt
    raise ValueError(f"Неизвестный алгоритм: {algo}")

def verify_password(password: str, record: dict) -> bool:
    """
    Проверяет пароль на основе существующей записи
    Принимает: Пароль и запись
    Возвращает: True если пароль валидный, False иначе
    """
    algo = record.get("algo")
    
    if algo == "sha256":
        return hash_simple(password)["hash"] == record["hash"]
        
    elif algo == "sha256_salted":
        current_salt = bytes.fromhex(record["salt"])
        calculated_hash = hashlib.sha256(current_salt + password.encode('utf-8')).hexdigest()
        return calculated_hash == record["hash"]
        
    elif algo == "bcrypt":
        return bcrypt.checkpw(password.encode('utf-8'), record["hash"].encode('utf-8'))
        
    return False
