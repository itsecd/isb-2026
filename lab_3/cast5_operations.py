import os
from Crypto.Cipher import CAST
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Размер блока CAST-5 (8 байт = 64 бита)
BLOCK_SIZE = CAST.block_size


def validate_key_length(length_bits: int) -> None:
    """
    Проверяет допустимость длины ключа CAST-5.

    Args:
        length_bits (int): Длина ключа в битах.

    Returns:
        None
    """
    if not isinstance(length_bits, int):
        raise TypeError("Длина ключа должна быть целым числом")
    if length_bits < 40 or length_bits > 128 or length_bits % 8 != 0:
        raise ValueError(f"CAST-5: длина ключа {length_bits} бит не подходит. Нужно 40-128, кратно 8")


def generate_key(length_bits: int) -> bytes:
    """
    Генерирует случайный ключ CAST-5 заданной длины.

    Args:
        length_bits (int): Длина ключа в битах (40-128, кратно 8).

    Returns:
        bytes: Случайный ключ указанной длины.
    """
    validate_key_length(length_bits)
    key_bytes = length_bits // 8
    return get_random_bytes(key_bytes)


def encrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    Шифрует файл CAST-5 в режиме CBC с PKCS7 паддингом.

    Args:
        input_path (str): Путь к исходному файлу для шифрования.
        output_path (str): Путь для сохранения зашифрованного файла.
        key (bytes): Ключ шифрования CAST-5.

    Returns:
        None
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл для шифрования не найден: {input_path}")
    if not key:
        raise ValueError("Ключ не может быть пустым")

    cipher = CAST.new(key, CAST.MODE_CBC)
    iv = cipher.iv

    with open(input_path, 'rb') as f:
        plain_data = f.read()

    encrypted_data = cipher.encrypt(pad(plain_data, BLOCK_SIZE))

    with open(output_path, 'wb') as f:
        f.write(iv + encrypted_data)


def decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    Расшифровывает файл, зашифрованный функцией encrypt_file.

    Args:
        input_path (str): Путь к зашифрованному файлу.
        output_path (str): Путь для сохранения расшифрованного файла.
        key (bytes): Ключ расшифрования CAST-5.

    Returns:
        None
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Зашифрованный файл не найден: {input_path}")
    if not key:
        raise ValueError("Ключ не может быть пустым")

    with open(input_path, 'rb') as f:
        iv = f.read(BLOCK_SIZE)
        encrypted_data = f.read()

    if len(iv) != BLOCK_SIZE:
        raise ValueError("Неверный вектор инициализации в файле")

    cipher = CAST.new(key, CAST.MODE_CBC, iv=iv)
    decrypted_padded = cipher.decrypt(encrypted_data)
    decrypted_data = unpad(decrypted_padded, BLOCK_SIZE)

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)