import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def generate_sym_key() -> bytes:
    """
    Генерирует случайный 256-битный ключ для алгоритма ChaCha20.
    Returns:
        bytes: Симметричный ключ длиной 32 байта.
    """
    print("Ключ для симметричного шифрования создан")
    return os.urandom(32)


def generate_nonce() -> bytes:
    """
    Генерирует случайное 128-битное одноразовое число (nonce) для ChaCha20.
    Returns:
        bytes: Nonce длиной 16 байт.
    """
    return os.urandom(16)


def serialize_nonce(nonce: bytes) -> bytes:
    """
    Сериализует nonce для сохранения в файл.
    Args:
        nonce (bytes): Nonce длиной 16 байт.
    Returns:
        bytes: Сериализованный nonce.
    """
    if len(nonce) != 16:
        raise ValueError(f"Nonce должен быть 16 байт, получено {len(nonce)}")
    return nonce


def deserialize_nonce(data: bytes) -> bytes:
    """
    Десериализует nonce из файла.
    Args:
        data (bytes): Данные, содержащие nonce.
    Returns:
        bytes: Nonce длиной 16 байт.
    Raises:
        ValueError: Если данные некорректной длины.
    """
    if len(data) < 16:
        raise ValueError(f"Недостаточно данных для извлечения nonce: {len(data)} байт")
    return data[:16]


def encryption_data(data: bytes, key: bytes) -> bytes:
    """
    Шифрует данные алгоритмом ChaCha20 с использованием случайного nonce.
    Args:
        data (bytes): Исходные данные для шифрования.
        key (bytes): Симметричный ключ (32 байта).
    Returns:
        bytes: Конкатенация nonce и зашифрованных данных.
    Raises:
        ValueError: Если ключ некорректной длины.
    """
    if len(key) != 32:
        raise ValueError(f"Ключ должен быть 32 байта, получено {len(key)}")

    nonce = generate_nonce()
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()

    e_data = encryptor.update(data) + encryptor.finalize()

    print("Данные при помощи симметричного ключа успешно зашифрованы")
    return serialize_nonce(nonce) + e_data


def decryption_data(data: bytes, key: bytes) -> bytes:
    """
    Расшифровывает данные, защищенные алгоритмом ChaCha20.
    Args:
        data (bytes): Зашифрованные данные, начинающиеся с 16-байтного nonce.
        key (bytes): Симметричный ключ, использованный при шифровании (32 байта).
    Returns:
        bytes: Исходные расшифрованные данные.
    Raises:
        ValueError: Если ключ или данные некорректной длины.
    """
    if len(key) != 32:
        raise ValueError(f"Ключ должен быть 32 байта, получено {len(key)}")

    nonce = deserialize_nonce(data)
    cipher_data = data[16:]

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()

    d_data = decryptor.update(cipher_data) + decryptor.finalize()

    print("Данные при помощи симметричного ключа успешно дешифрованы")
    return d_data