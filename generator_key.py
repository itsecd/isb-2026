import os
from cryptography.hazmat.primitives.asymmetric import rsa


def creater_symmetric_key(size: int) -> bytes:
    """
    Генерация ключа для симетричного шифрования заданного размера
    """
    size_in_bytes = size // 8
    if size_in_bytes not in (16, 24, 32):
        raise ValueError("AES поддерживает только 128, 192 или 256 бит.")
    key = os.urandom(size_in_bytes)
    return key


def creater_asymmetrical_key() -> bytes:
    """
    Генерация ключей для асиметричного шифрования
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key
