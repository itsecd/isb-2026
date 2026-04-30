import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generating_symmetric_key(size:int) -> bytes: 
    """
    Геренирование ключа для симметричного алгоритма
    """
    key = os.urandom(size)
    return key


def generating_asymmetric_key() -> bytes:
    """
    Гененирование ключей для асимметричного алгоритма
    """
    keys = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key
