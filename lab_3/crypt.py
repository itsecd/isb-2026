import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def encrypt_text(text, symmetric_key):
    """
    заполнение и шифрование текста с помощью алгоритма SM4
    
    аргументы: 
            text: исходный текст в байтах
            symmetric_key: расшифрованный симметричный ключ в виде 16 байт
    возвращает:
            tuple(iv, etext_in_bytes): кортеж с вектором инициализации (16 байт) и зашифрованным текстом в байтах
    """

    padder = padding.ANSIX923(128).padder()
    padded_text = padder.update(text) + padder.finalize()

    iv = os.urandom(16)

    cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    etext_in_bytes = encryptor.update(padded_text) + encryptor.finalize()

    return iv, etext_in_bytes


def decrypt_text(iv, etext_in_bytes, symmetric_key):
    """
    Расшифровывание текста, зашифрованного с помощью алгоритма SM4, и удаление заполнения.
    аргументы:
            iv: вектор инициализации (16 байт)
            etext_in_bytes: зашифрованный текст в байтах
            symmetric_key: расшифрованный симметричный ключ в виде 16 байт
    возвращает:
            decrypted_file: расшифрованный текст без заполнения в байтах
    """

    cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(etext_in_bytes) + decryptor.finalize()

    unpadder = padding.ANSIX923(128).unpadder()
    decrypted_file = unpadder.update(dc_text) + unpadder.finalize()

    return decrypted_file
