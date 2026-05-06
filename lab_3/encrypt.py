import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

from gen_key import read_file


def generate_nonce() -> bytes:
    return os.urandom(16)


def chacha20_encrypt(text: bytes, key: bytes, nonce: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("ChaCha20 key must be exactly 32 bytes (256 bits)")
    if len(nonce) != 16:
        raise ValueError("Nonce must be exactly 16 bytes (128 bits)")

    cipher = Cipher(
        algorithms.ChaCha20(key, text),
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


def write_encrypted_file(filepath: str, nonce: bytes, ciphertext: bytes) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    packed = pack_encrypted_data(nonce, ciphertext)
    
    with open(filepath, 'wb') as f:
        f.write(packed)