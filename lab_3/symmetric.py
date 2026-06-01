import os

from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def get_symmetric_key(byt: int) -> bytes:
    """
    Генерирует симметричный ключ для алгоритма 3DES.

    Параметры:
    byt: int - количество байт, из которых будет состоять ключ.

    Возвращает:
    bytes - сгенерированный симметричный ключ.
    """
    key = os.urandom(byt)
    return key


def padding_text(text: bytes) -> bytes:
    """
    Добавляет паддинг к тексту по стандарту ANSI X9.23 для 3DES.

    Параметры:
    text: bytes - данные, к которым нужно добавить паддинг.

    Возвращает:
    bytes - данные с добавленным паддингом.
    """
    padder = sym_padding.ANSIX923(64).padder()
    padded_text = padder.update(text) + padder.finalize()
    return padded_text


def encrypt_text(text: bytes, symmetric_key: bytes) -> bytes:
    """
    Шифрует текст с помощью алгоритма 3DES в режиме CBC.

    Параметры:
    text: bytes - данные для шифрования.
    symmetric_key: bytes - симметричный ключ шифрования.

    Возвращает:
    bytes - вектор инициализации и зашифрованные данные.
    """
    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padded_text = padding_text(text)
    encrypted_text = encryptor.update(padded_text) + encryptor.finalize()

    return iv + encrypted_text


def decrypt_text(encrypted_data: bytes, symmetric_key: bytes) -> bytes:
    """
    Расшифровывает данные и удаляет паддинг после алгоритма 3DES.

    Параметры:
    encrypted_data: bytes - данные для расшифровки, включающие IV и шифротекст.
    symmetric_key: bytes - симметричный ключ шифрования.

    Возвращает:
    bytes - расшифрованные данные без паддинга.
    """
    try:
        iv = encrypted_data[:8]
        ciphertext = encrypted_data[8:]

        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        padded_text = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = sym_padding.ANSIX923(64).unpadder()
        unpadded_text = unpadder.update(padded_text) + unpadder.finalize()

        return unpadded_text
    except Exception as ex:
        print(f"Ошибка!: {ex}")
        return b""
