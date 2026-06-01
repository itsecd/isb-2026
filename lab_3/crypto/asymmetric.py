"""
Асимметричное шифрование: RSA-2048 с OAEP-паддингом (SHA-256).
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


RSA_KEY_SIZE = None
RSA_PUBLIC_EXPONENT = None


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
    if RSA_KEY_SIZE is None or RSA_PUBLIC_EXPONENT is None:
        raise RuntimeError("Параметры RSA не заданы. Проверьте файл настроек.")
    try:
        private_key = rsa.generate_private_key(
            public_exponent=RSA_PUBLIC_EXPONENT,
            key_size=RSA_KEY_SIZE,
        )
    except ValueError as e:
        raise RuntimeError(f"Неверные параметры RSA: {e}")
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
    try:
        return public_key.encrypt(data, _oaep_padding())
    except Exception as e:
        raise RuntimeError(f"Ошибка RSA-шифрования: {e}")


def decrypt(data: bytes, private_key) -> bytes:
    """
    Расшифровывает данные закрытым RSA-ключом (OAEP/SHA-256).
    
    Args:
        data: Зашифрованные данные.
        private_key: Закрытый RSA-ключ.
    
    Returns:
        Расшифрованные исходные данные.
    """
    try:
        return private_key.decrypt(data, _oaep_padding())
    except Exception as e:
        raise RuntimeError(f"Ошибка RSA-дешифрования: {e}")
