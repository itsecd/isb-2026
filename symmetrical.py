import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.primitives.ciphers.algorithms import SEED


def generate_sym_key() -> bytes:
    """Генерация симметричного ключа для SEED.
    возвращает симметричный ключ"""
    print("Ключ для симметричного шифрования создан")
    return os.urandom(16)


def encryption_data(data: bytes, key: bytes) -> bytes:
    """Шифрование данных при помощи SEED с использованием режима CBC
    принимает данные и ключ
    возвращает зашифрованные данные с векторной инициализацией"""
    iv = os.urandom(16)
    cipher = Cipher(SEED(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    pad_data = padder.update(data) + padder.finalize()

    e_data = encryptor.update(pad_data) + encryptor.finalize()

    print("Данные при помощи симметричного ключа успешно зашифрованны")
    return iv + e_data


def decryption_data(data: bytes, key: bytes) -> bytes:
    """Дешифрование данных, зашифрованных с успользованием SEED в режиме CBC
    принимает зашифрованные данные и симметричный ключ
    возвращает зашифрованные данные"""
    iv = data[:16]
    cipher_data = data[16:]

    cipher = Cipher(SEED(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    d_data = decryptor.update(cipher_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpad_d_data = unpadder.update(d_data) + unpadder.finalize()

    print("Данные при помощи симметричного ключа успешно дешифрованны")
    return unpad_d_data
