import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def volshebniy_kluch(key_length: int) -> bytes:
    """
    Генерирует ключ для алгоритма Camellia длиной 128, 192 или 256 байтов.
    На вход принимает длину ключа и возвращает ключ заданной длины.
    Для нестандартных значений длины возвращает ошибку.
    """
    if (key_length in [128,192,256]):
        return os.urandom(key_length//8)
    else:
        raise RuntimeError("Привет, я люблю числа 128, 192 и 256 и обожаю делать ключи такой длины.")


def encrypt_data(init_file: str, key: bytes) -> bytes:
    """
    Шифрует текст из файла по алгоритму Camellia.
    ASGHASFGasfgafgafhgjkd
    """
    try:
        with open(init_file, "r", encoding="utf-8") as f:
            text = f.read()
        padder = padding.ANSIX923(128).padder()
        text = bytes(text, 'UTF-8')
        padded_text = padder.update(text)+padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        return c_text
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {init_file}, увы")