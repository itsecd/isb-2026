import os

from cryptography.hazmat.primitives import padding as symmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from io_utils import load_blob, dump_blob


def make_3des_key(key_size: int) -> bytes:
    """
    Генерирует ключ 3DES.

    :param key_size: длина ключа в битах, 64, 128 или 192
    :return: ключ 3DES
    """
    if key_size not in (64, 128, 192):
        raise ValueError("Длина ключа 3DES должна быть 64, 128 или 192 бит.")

    return os.urandom(key_size // 8)


def encrypt_file_3des(input_file_path: str, output_file_path: str, key: bytes) -> None:
    """
    Шифрует файл алгоритмом 3DES-CBC.

    :param input_file_path: путь к исходному файлу
    :param output_file_path: путь для сохранения зашифрованного файла
    :param key: ключ 3DES
    :return: None
    """
    plaintext = load_blob(input_file_path)

    padder = symmetric_padding.PKCS7(64).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    dump_blob(output_file_path, iv + ciphertext)


def decrypt_file_3des(input_file_path: str, output_file_path: str, key: bytes) -> None:
    """
    Дешифрует файл алгоритмом 3DES-CBC.

    :param input_file_path: путь к зашифрованному файлу
    :param output_file_path: путь для сохранения расшифрованного файла
    :param key: ключ 3DES
    :return: None
    """
    encrypted_data = load_blob(input_file_path)

    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]

    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = symmetric_padding.PKCS7(64).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    dump_blob(output_file_path, plaintext)
