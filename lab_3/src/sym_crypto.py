import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers import algorithms as decrepit_algorithms
from cryptography.hazmat.primitives import padding as sym_padding

def encrypt_seed(plain_text: bytes, sym_key: bytes, block_size: int = 128) -> tuple[bytes, bytes]:
    """Data encryption using the SEED algorithm."""
    try:
        padder = sym_padding.ANSIX923(block_size).padder()
        padded_text = padder.update(plain_text) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(decrepit_algorithms.SEED(sym_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(padded_text) + encryptor.finalize()

        return iv, cipher_text
    except Exception as e:
        raise RuntimeError(f"Symmetric Encryption failure (SEED): {e}")

def decrypt_seed(cipher_text: bytes, sym_key: bytes, iv: bytes, block_size: int = 128) -> bytes:
    """Decryption of data by the SEED algorithm."""
    try:
        cipher = Cipher(decrepit_algorithms.SEED(sym_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plain_text = decryptor.update(cipher_text) + decryptor.finalize()

        unpadder = sym_padding.ANSIX923(block_size).unpadder()
        plain_text = unpadder.update(padded_plain_text) + unpadder.finalize()

        return plain_text
    except Exception as e:
        raise RuntimeError(f"Symmetric decryption failure (SEED): {e}")