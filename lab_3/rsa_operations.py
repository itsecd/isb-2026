"""
Модуль для работы с асимметричным шифрованием алгоритмом RSA.

RSA (Rivest-Shamir-Adleman) - один из первых алгоритмов асимметричного
шифрования, опубликованный в 1977 году. Основан на вычислительной
сложности задачи факторизации больших целых чисел.

Характеристики:
- Размер ключа: 2048 бит (рекомендуемый минимум)
- Публичная экспонента: 65537 (стандартное значение)
- Схема шифрования: OAEP с SHA-256
"""

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


def encrypt_session_key(pub_key: RSAPublicKey, session_key: bytes) -> bytes:
    """
    Шифрование сессионного ключа асимметричным алгоритмом RSA-OAEP.
    
    Args:
        pub_key: Публичный RSA ключ для шифрования.
        session_key: Симметричный сессионный ключ для шифрования.
        
    Returns:
        bytes: Зашифрованный сессионный ключ.
        
    Note:
        Использует схему OAEP с MGF1 и хеш-функцией SHA-256.
        Максимальный размер данных зависит от размера ключа RSA.
    """
    encrypted_key = pub_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key


def decrypt_session_key(priv_key: RSAPrivateKey, encrypted_session_key: bytes) -> bytes:
    """
    Расшифровка сессионного ключа асимметричным алгоритмом RSA-OAEP.
    
    Args:
        priv_key: Приватный RSA ключ для расшифровки.
        encrypted_session_key: Зашифрованный сессионный ключ.
        
    Returns:
        bytes: Расшифрованный сессионный ключ.
        
    Note:
        Использует схему OAEP с MGF1 и хеш-функцией SHA-256.
    """
    decrypted_key = priv_key.decrypt(
        encrypted_session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key