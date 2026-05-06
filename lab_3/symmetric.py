import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def generate_nonce() -> bytes:
    return os.urandom(16)


def generate_symmetric_key(key_size: int) -> bytes:
    if key_size % 8 != 0:
        raise ValueError("key_size must be multiple of 8")
    if not 32 <= key_size <= 448:
        raise ValueError("Key size must be between 32 and 448 bits")
    return os.urandom(key_size//8)


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


def chacha20_encrypt(text: bytes, key: bytes, nonce: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("ChaCha20 key must be exactly 32 bytes (256 bits)")
    if len(nonce) != 16:
        raise ValueError("Nonce must be exactly 16 bytes (128 bits)")

    cipher = Cipher(
        algorithms.ChaCha20(key, nonce),
        mode=None
    )

    encryptor = cipher.encryptor()
    return encryptor.update(text) + encryptor.finalize()


def pack_encrypted_data(nonce: bytes, ciphertext: bytes) -> bytes:
    return nonce + ciphertext


def unpack_encrypted_data(packed_data: bytes) -> tuple[bytes, bytes]:
    if len(packed_data) < 16:
        raise ValueError("Not enough data to extract nonce")
    
    nonce = packed_data[:16]
    ciphertext = packed_data[16:]
    return nonce, ciphertext

