import os
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def get_symmetric_key(byt:int) -> bytes:
    """ключ для симметричного алгоритма"""
    key = os.urandom(byt)
    return key


def padding_text(text:bytes) ->bytes:
    """паддинг текста под стандарты 3DES"""
    padder = sym_padding.ANSIX923(64).padder()
    padded_text = padder.update(text)+padder.finalize()
    return padded_text

def encrypt_text(text:bytes, symmetric_key:bytes) -> bytes:
    """
    Шифрование текста помощью алгоритма 3DES
    Входные данные:
    text - данные для шифрования
    symmetric_key - симметричный ключ шифрования
    Возвращает зашифрованные данные (bytes)
    """
    iv = os.urandom(8) 
    cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_text = padding_text(text)
    encrypted_text = encryptor.update(padded_text) + encryptor.finalize()
    return iv + encrypted_text

def decrypt_text(encrypted_data: bytes, symmetric_key: bytes) -> str:
    """
    Дешифровка и удаление паддинга с помощью алгоритма 3DES
    Входные данные:
    encrypted_text - данные для дешифрования
    symmetric_key - симметричный ключ шифрования
    Возвращает расшифрованные данные (bytes)
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
        return ""