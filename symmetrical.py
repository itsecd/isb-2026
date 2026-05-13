import os
from typing import Tuple
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


TRIPLE_DES_MODES = [64, 128, 192]


def gen_sym_key(key_length: int) -> bytes:
    '''
    Generates a symmetric key of the specified length for 3DES.

    Args:
        key_length (int): The length of the key in bits.

    Returns:
        bytes: A generated key with a length of (key_length // 8) bytes.

    Raises:
        ValueError: If the entered length does not match the possible lengths.
    '''

    if key_length in TRIPLE_DES_MODES:
        key_length_bytes = key_length // 8
        return os.urandom(key_length_bytes)
    
    else:
        raise ValueError(
            f"3DES encryption does not work with key length {key_length}."
            f"Possible lengths are 64, 128 and 192"
        )


def triple_des_encryption(text: str, key: bytes) -> Tuple[bytes, bytes]:
    '''
    Encrypts text using the method 3DES.

    Args:
        text (str): The initial text.
        key (bytes): Symmetric encryption key of 8, 16 or 24 bytes in length.

    Returns:
        Tuple[bytes, bytes]: A tuple of encrypted text and initialization vector iv.
    '''

    text_bytes = text.encode('utf-8')

    padder = padding.ANSIX923(64).padder()
    padded_text = padder.update(text_bytes) + padder.finalize()

    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    c_text = encryptor.update(padded_text) + encryptor.finalize()
    return c_text, iv


def triple_des_decryption(text_bytes: bytes, key: bytes, iv: bytes) -> str:
    '''
    Decrypts text using the method 3DES.

    Args:
        text_bytes (bytes): The encrypted text in bytes.
        key (bytes): Symmetric encryption key of 8, 16 or 24 bytes in length.
        iv (bytes): The initialization vector.


    Returns:
        str : The original, decoded text.
    '''

    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    dc_text = decryptor.update(text_bytes) + decryptor.finalize()

    unpadder = padding.ANSIX923(64).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()

    text = unpadded_dc_text.decode('utf-8')
    return text