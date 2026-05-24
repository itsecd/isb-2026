import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generating_symmetric_key(size: int) -> bytes:
    """
    Генрация ключа для симметричного алгоритма AES
    
    принимает:
        size: размер ключа в байтах (16 для AES-128, 24 для AES-192, 32 для AES-256)
    
    возвращает:
        bytes: сгенерированный симметричный ключ
    """
    key = os.urandom(size)
    return key


def generating_asymmetric_key():
    """
    Генерация ключей для асимметричного алгоритма RSA
    
    возвращает:
        tuple: (private_key, public_key)
    """
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key