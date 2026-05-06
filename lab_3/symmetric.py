import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def generate_nonce() -> bytes:
    """
    Generates random nonce for ChaCha20.

    Returns:
        bytes: 16-byte nonce
    """
    return os.urandom(16)


def generate_symmetric_key(key_size: int) -> bytes:
    """
    Generates symmetric key.

    Args:
        key_size (int): Key size in bits (must be multiple of 8, 32–448 bits)

    Returns:
        bytes: Generated key
    """
    if key_size % 8 != 0:
        raise ValueError("key_size must be multiple of 8")
    if not 32 <= key_size <= 448:
        raise ValueError("Key size must be between 32 and 448 bits")

    return os.urandom(key_size // 8)


def _init_chacha(key: bytes, nonce: bytes):
    """
    Creates ChaCha20 cipher instance.

    Args:
        key (bytes): 32-byte key
        nonce (bytes): 16-byte nonce

    Returns:
        Cipher: initialized cipher object
    """
    if len(key) != 32:
        raise ValueError("ChaCha20 key must be exactly 32 bytes (256 bits)")
    if len(nonce) != 16:
        raise ValueError("Nonce must be exactly 16 bytes (128 bits)")

    return Cipher(
        algorithms.ChaCha20(key, nonce),
        mode=None
    )


def chacha20_encrypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """
    Encrypts data using ChaCha20.

    Args:
        data (bytes): plaintext
        key (bytes): symmetric key
        nonce (bytes): nonce

    Returns:
        bytes: ciphertext
    """
    cipher = _init_chacha(key, nonce)
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()


def chacha20_decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    """
    Decrypts ChaCha20 ciphertext.

    Args:
        ciphertext (bytes): encrypted data
        key (bytes): symmetric key
        nonce (bytes): nonce

    Returns:
        bytes: decrypted data
    """
    cipher = _init_chacha(key, nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def pack_encrypted_data(nonce: bytes, ciphertext: bytes) -> bytes:
    """
    Packs nonce and ciphertext into single byte sequence.

    Args:
        nonce (bytes): nonce
        ciphertext (bytes): encrypted data

    Returns:
        bytes: combined data
    """
    return nonce + ciphertext


def unpack_encrypted_data(packed_data: bytes) -> tuple[bytes, bytes]:
    """
    Splits packed encrypted data into nonce and ciphertext.

    Args:
        packed_data (bytes): combined data

    Returns:
        tuple[bytes, bytes]: (nonce, ciphertext)
    """
    if len(packed_data) < 16:
        raise ValueError("Not enough data to extract nonce")

    nonce = packed_data[:16]
    ciphertext = packed_data[16:]

    return nonce, ciphertext