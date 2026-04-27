import os
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.primitives import padding


def generate_key_for_IDEA(key_size: int = 16) -> bytes:
    """Функция создаёт ключ для использования
    в алгоритме шифрования IDEA
    """
    key = os.urandom(key_size)
    return key


def generate_IV(iv_size: int = 8) -> bytes:
    """Генерируем мусорное значение для избежания
    идентичного шифрования идентичных данных
    """
    iv = os.urandom(iv_size)
    return iv


def make_padding(data: bytes, block_size_bits: int = 64) -> bytes:
    """Функция принимает на вход некие данные в виде байт и
    дополняет их до стандартного размера блока в процессе шифрования
    """
    padder = padding.ANSIX923(block_size_bits).padder()
    data_with_padding = padder.update(data)+padder.finalize()
    return data_with_padding


def make_unpadding(data_with_padding: bytes, block_size_bits: int = 64) -> bytes:
    """Функция принимает на вход некие данные в виде байт и
    снимает паддинг для качественной расшифровки 
    """
    unpadder = padding.ANSIX923(block_size_bits).unpadder()
    original_data = unpadder.update(data_with_padding)+unpadder.finalize()
    return original_data


def encrypt_data(key: bytes, iv: bytes, plaintext: bytes, block_size_bits: int = 64) -> bytes:
    """Функция принимает на вход ключ, мусорное значение и 
    данные с паддингом и шифрует алгоритмом IDEA в режиме CBC
    """
    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_data = make_padding(plaintext, block_size_bits)
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext


def decrypt_data(key: bytes, iv: bytes, ciphertext: bytes, block_size_bits: int = 64) -> bytes:
    """Функция принимает на вход ключ, мусорное значение и 
    данные с паддингом и расшифровывает алгоритмом IDEA в режиме CBC
    """
    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    original_data = make_unpadding(decrypted_padded, block_size_bits)
    return original_data