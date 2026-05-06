import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from encrypt import *

def read_encrypt_text(filepath: str) -> tuple[bytes, bytes]:
    try:
        with open(filepath, 'rb') as enc_file:
            data = enc_file.read()
        return unpack_encrypted_data(data)
    
    except Exception as error:
        print(f"Couldn't upload encrypted text  {filepath}: {error}\n")
        return None, None


def chacha20_decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("ChaCha20 key must be exactly 32 bytes (256 bits)")
    if len(nonce) != 16:
        raise ValueError("Nonce must be exactly 16 bytes (128 bits)")

    cipher = Cipher(
        algorithms.ChaCha20(key, nonce),
        mode=None
    )

    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()