import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_blowfish_key(key_length: int) -> bytes:
    """
    Generate symmetric Blowfish key.
    :param key_length: key length
    :return: symmetric key
    """
    return os.urandom(key_length // 8)


def encrypt_blowfish(key: bytes, data: bytes) -> bytes:
    """
    Encrypt data using Blowfish.
    :param key: symmetric key
    :param data: data to encrypt
    :return: encrypted data
    """
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(8)
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    return iv + cipher_text


def decrypt_blowfish(key: bytes, encrypted_data: bytes) -> bytes:
    """
    Decrypt data using RSA.
    :param key: symmetric key
    :param encrypted_data: data to decrypt
    :return: decrypted data
    """
    iv = encrypted_data[:8]
    cipher_text = encrypted_data[8:]

    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(cipher_text) + decryptor.finalize()

    unpadder = padding.PKCS7(64).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()
