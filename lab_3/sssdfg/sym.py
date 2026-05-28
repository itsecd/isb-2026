import os
import util
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_data_camellia(init_file: str, key: bytes) -> bytes:
    """
    Шифрует текст из файла по алгоритму Camellia.
    На вход принимает путь до .txt файла с открытым текстом и ключ симметричного алгоритма.
    Принимает:
        init_file - путь до файла с открытым текстом
        key - ключ симметричного алгоритма
    Возвращает зашифрованный текст.
    """
    try:
        text = util.read_file(init_file)
        padder = padding.ANSIX923(128).padder()   
        padded_text = padder.update(text)+padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        return iv + c_text
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {init_file}, увы")
    

def decrypt_data_camellia(init_file: str, key: bytes) -> bytes:
    """
    Расшифровывает бинарный файл, зашифрованный алгоритмом Camellia.
    На вход принимает путь до файла с шифротекстом  и ключ симметричного алгоритма.
    Принимает:
        init_file - путь до файла с шифротекстом
        key - ключ симметричного алгоритма
    Возвращает расшифрованный текст.    
    """
    try:
        iv_c_text = util.read_file(init_file)
        iv = iv_c_text[:16]
        c_text = iv_c_text[16:]
        cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        dc_text = decryptor.update(c_text) + decryptor.finalize()
        unpadder = padding.ANSIX923(128).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        return unpadded_dc_text
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {init_file}, увы")


def encrypt_data_aes(init_file: str, key: bytes) -> bytes:
    """
    Шифрует текст из файла по алгоритму AES.
    На вход принимает путь до .txt файла с открытым текстом и ключ симметричного алгоритма.
    Принимает:
        init_file - путь до файла с открытым текстом
        key - ключ симметричного алгоритма
    Возвращает зашифрованный текст.
    """
    try:
        text = util.read_file(init_file)
        padder = padding.ANSIX923(128).padder()   
        padded_text = padder.update(text)+padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        return iv + c_text
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {init_file}, увы")
    

def decrypt_data_aes(init_file: str, key: bytes) -> bytes:
    """
    Расшифровывает бинарный файл, зашифрованный алгоритмом AES.
    На вход принимает путь до файла с шифротекстом  и ключ симметричного алгоритма.
    Принимает:
        init_file - путь до файла с шифротекстом
        key - ключ симметричного алгоритма
    Возвращает расшифрованный текст.    
    """
    try:
        iv_c_text = util.read_file(init_file)
        iv = iv_c_text[:16]
        c_text = iv_c_text[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        dc_text = decryptor.update(c_text) + decryptor.finalize()
        unpadder = padding.ANSIX923(128).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        return unpadded_dc_text
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {init_file}, увы")
