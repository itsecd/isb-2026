import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .utils import pad_data, unpad_data
from .config import BLOCK_SIZE


def generate_camellia_key(key_size: int = 32) -> bytes:
    """
    Генерация случайного ключа для Camellia.
    
    Args:
        key_size (int): Размер ключа в байтах. По умолчанию 32 байта (256 бит)
    
    Returns:
        bytes: Случайный ключ указанного размера
    
    Raises:
        ValueError: Если key_size <= 0
    
    Example:
        >>> key = generate_camellia_key(32)
        >>> len(key)
        32
    """
    if key_size <= 0:
        raise ValueError("Размер ключа должен быть положительным числом")
    return os.urandom(key_size)


def encrypt_with_camellia(data: bytes, key: bytes) -> bytes:
    """
    Шифрование данных алгоритмом Camellia в режиме CBC.
    
    Формат выходных данных: [IV (16 байт)] + [зашифрованные данные]
    
    Процесс шифрования:
        1. Генерируется случайный инициализирующий вектор (IV)
        2. Данные дополняются до размера блока (PKCS7)
        3. Выполняется шифрование в режиме CBC
    
    Args:
        data (bytes): Исходные данные для шифрования
        key (bytes): Симметричный ключ (должен быть 16, 24 или 32 байта)
    
    Returns:
        bytes: IV + зашифрованные данные
    
    Raises:
        ValueError: Если ключ имеет неверный размер (не 16, 24 или 32 байта)
    
    Example:
        >>> key = generate_camellia_key(32)
        >>> encrypted = encrypt_with_camellia(b"Hello World", key)
        >>> len(encrypted) > len(b"Hello World")
        True
    """
    iv = os.urandom(BLOCK_SIZE)
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    padded_data = pad_data(data, BLOCK_SIZE)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted_data


def decrypt_with_camellia(encrypted_data_with_iv: bytes, key: bytes) -> bytes:
    """
    Расшифровка данных алгоритмом Camellia в режиме CBC.
    
    Ожидаемый формат входных данных: [IV (16 байт)] + [зашифрованные данные]
    
    Процесс расшифровки:
        1. Извлекается IV из первых 16 байт
        2. Выполняется расшифровка оставшихся данных
        3. Удаляется дополнение PKCS7
    
    Args:
        encrypted_data_with_iv (bytes): IV + зашифрованные данные
        key (bytes): Симметричный ключ (должен быть 16, 24 или 32 байта)
    
    Returns:
        bytes: Расшифрованные исходные данные
    
    Raises:
        ValueError: Если ключ имеет неверный размер или данные повреждены
        Exception: Если неверный ключ или нарушена целостность данных
    
    Example:
        >>> key = generate_camellia_key(32)
        >>> original = b"Secret message"
        >>> encrypted = encrypt_with_camellia(original, key)
        >>> decrypted = decrypt_with_camellia(encrypted, key)
        >>> original == decrypted
        True
    """
    iv = encrypted_data_with_iv[:BLOCK_SIZE]
    encrypted_data = encrypted_data_with_iv[BLOCK_SIZE:]
    
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
    return unpad_data(decrypted_padded, BLOCK_SIZE)