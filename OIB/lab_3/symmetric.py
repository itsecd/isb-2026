import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY_SIZES = {128: 16, 192: 24, 256: 32}


def generate_symmetric_key(key_bits: int) -> bytes:
    """Функция сгенерирования симметричного ключа Camellia заданной длины."""
    if key_bits not in KEY_SIZES:
        raise ValueError(f"Недопустимая длина ключа: {key_bits}. Нужно: 128, 192, 256.")
    return os.urandom(KEY_SIZES[key_bits])


def choose_key_size() -> int:
    """Запрос у пользователя длину ключа."""
    print(" Выберите длину симметричного ключа Camellia:")
    print("1) 128 бит")
    print("2) 192 бит")
    print("3) 256 бит")
    mapping = {"1": 128, "2": 192, "3": 256}
    while True:
        choice = input("Ваш выбор (1/2/3): ").strip()
        if choice in mapping:
            return mapping[choice]
        print("Введите 1, 2 или 3.")


def encrypt_text(text: bytes, symmetric_key: bytes) -> bytes:
    """
    Функция зашифровки данных алгоритмом Camellia.
    """
    padder = padding.ANSIX923(128).padder()
    padded_text = padder.update(text) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.Camellia(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()

    return iv + c_text


def decrypt_text(data: bytes, symmetric_key: bytes) -> bytes:
    """
    Функция расшифровки данных алгоритмом Camellia.
    """
    iv = data[:16]
    c_text = data[16:]

    cipher = Cipher(algorithms.Camellia(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(c_text) + decryptor.finalize()

    unpadder = padding.ANSIX923(128).unpadder()
    return unpadder.update(padded_text) + unpadder.finalize()
