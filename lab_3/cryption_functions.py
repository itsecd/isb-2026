import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def encrypt_text(text: bytes, symmetric_key: bytes, aes_key_size: int = 256) -> tuple:
    """
    performs padding and encrypts text using AES algorithm
    
    arguments: 
            text: initial text in bytes
            symmetric_key: decrypted symmetric key
            aes_key_size: AES key size in bits (128, 192, 256)
    return:
            tuple(iv, c_text): tuple with initialization vector (16 bytes) and encrypted text in bytes
    """
    aes_block_size = 128
    
    padder = padding.ANSIX923(aes_block_size).padder()
    padded_text = padder.update(text) + padder.finalize()

    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()

    return iv, c_text


def decrypt_text(iv: bytes, c_text: bytes, symmetric_key: bytes, aes_key_size: int = 256) -> bytes:
    """
    decrypts text, encrypted using the AES algorithm, and removes padding
    
    arguments:
            iv: initialization vector (16 bytes)
            c_text: encrypted text in bytes
            symmetric_key: decrypted symmetric key
            aes_key_size: AES key size in bits (128, 192, 256)
    return:
            unpadded_dc_text: decrypted text without padding in bytes
    """
    aes_block_size = 128

    match aes_key_size:
        case 128:
            cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        case 192:
            cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        case 256:
            cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        case _:
            raise ValueError("AES key size must be 128, 192 or 256 bits")
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(c_text) + decryptor.finalize()

    unpadder = padding.ANSIX923(aes_block_size).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()

    return unpadded_dc_text