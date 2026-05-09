import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def encrypt_text(text, symmetric_key):
    """
    performs padding and encrypts text using SM4 algorithm
    
    arguments: 
            text: initial text in bytes
            symmetric_key: decrypted symmetric key in form of 16 bytes
    return:
            tuple(iv, c_text): tuple with initialization vector (16 bytes) and encrypted text in bytes
    """

    padder = padding.ANSIX923(128).padder()
    padded_text = padder.update(text) + padder.finalize()

    iv = os.urandom(16)

    cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()

    return iv, c_text


def decrypt_text(iv, c_text, symmetric_key):
    """
    decrypts text, encrypted using the SM4 algorithm, and removes padding

    arguments:
            iv: initialization vector (16 bytes)
            c_text: encrypted text in bytes
            symmetric_key: decrypted symmetric key in form of 16 bytes
    return:
            unpadded_dc_text: decrypted text without padding in bytes
    """

    cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(c_text) + decryptor.finalize()

    unpadder = padding.ANSIX923(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()

    return unpadded_dc_text