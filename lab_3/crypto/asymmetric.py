"""
Асимметричное шифрование: RSA-2048 с OAEP-паддингом (SHA-256).
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


# Параметры RSA по умолчанию
RSA_KEY_SIZE = 2048
RSA_PUBLIC_EXPONENT = 65537


def set_parameters(key_size: int, public_exponent: int) -> None:
    """
    Устанавливает параметры RSA из конфигурации.
    
    Args:
        key_size: Размер RSA-ключа в битах.
        public_exponent: Открытая экспонента RSA.
    """
    global RSA_KEY_SIZE, RSA_PUBLIC_EXPONENT
    RSA_KEY_SIZE = key_size
    RSA_PUBLIC_EXPONENT = public_exponent


def generate_rsa_keys():
    """
    Генерирует пару RSA-2048 ключей.
    
    Returns:
        Кортеж (private_key, public_key) с парой RSA-ключей.
    """
    private_key = rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE,
    )
    return private_key, private_key.public_key()


def _oaep_padding():
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def encrypt(data: bytes, public_key) -> bytes:
    """
    Шифрует данные открытым RSA-ключом (OAEP/SHA-256).
    
    Args:
        data: Данные для шифрования (максимум 190 байт для RSA-2048).
        public_key: Открытый RSA-ключ.
    
    Returns:
        Зашифрованные данные.
    """
    return public_key.encrypt(data, _oaep_padding())


def decrypt(data: bytes, private_key) -> bytes:
    """
    Расшифровывает данные закрытым RSA-ключом (OAEP/SHA-256).
    
    Args:
        data: Зашифрованные данные.
        private_key: Закрытый RSA-ключ.
    
    Returns:
        Расшифрованные исходные данные.
    """
    return private_key.decrypt(data, _oaep_padding())
