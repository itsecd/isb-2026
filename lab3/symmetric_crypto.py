import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from config import SEED_KEY_SIZE, SEED_BLOCK_SIZE, IV_SIZE


def generate_symmetric_key():
    return os.urandom(SEED_KEY_SIZE)


def pad_data(data):
    try:
        padder = padding.ANSIX923(SEED_BLOCK_SIZE).padder()
        return padder.update(data) + padder.finalize()
    except Exception as e:
        raise RuntimeError(f"Padding failed: {e}")


def unpad_data(padded_data):
    try:
        unpadder = padding.ANSIX923(SEED_BLOCK_SIZE).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()
    except Exception as e:
        raise RuntimeError(f"Unpadding failed: {e}")


def seed_encrypt(key, plaintext):
    try:
        iv = os.urandom(IV_SIZE)
        cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_data = pad_data(plaintext)
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv, ciphertext
    except Exception as e:
        raise RuntimeError(f"SEED encryption failed: {e}")


def seed_decrypt(key, iv, ciphertext):
    try:
        cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        return unpad_data(padded_data)
    except Exception as e:
        raise RuntimeError(f"SEED decryption failed: {e}")
