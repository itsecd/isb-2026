"""
Symmetric encryption module using SEED algorithm (CBC mode).

Implements SEED-128 symmetric encryption with ANSI X9.23 padding.
Provides key generation, encryption, and decryption functions for
binary data with proper IV handling.
"""

import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from config import SEED_KEY_SIZE, SEED_BLOCK_SIZE, IV_SIZE
from exceptions import EncryptionError, DecryptionError, PaddingError


def generate_symmetric_key():
    """
    Generate a cryptographically secure random symmetric key for SEED-128.

    Returns:
        bytes: Random symmetric key of length SEED_KEY_SIZE (16 bytes = 128 bits).
    
    Example:
        >>> key = generate_symmetric_key()
        >>> len(key)
        16
    """
    return os.urandom(SEED_KEY_SIZE)


def pad_data(data):
    """
    Apply ANSI X9.23 padding to data for SEED block cipher.

    ANSI X9.23 padding: pads with bytes of value equal to the number of padding bytes,
    except the last byte which indicates the padding length.

    Args:
        data (bytes): Raw data to pad.

    Returns:
        bytes: Padded data with length multiple of SEED_BLOCK_SIZE.

    Raises:
        PaddingError: If padding operation fails.
    """
    try:
        padder = padding.ANSIX923(SEED_BLOCK_SIZE).padder()
        return padder.update(data) + padder.finalize()
    except Exception as e:
        raise PaddingError(f"Padding failed: {e}")


def unpad_data(padded_data):
    """
    Remove ANSI X9.23 padding from decrypted data.

    Args:
        padded_data (bytes): Data with ANSI X9.23 padding to remove.

    Returns:
        bytes: Original unpadded data.

    Raises:
        PaddingError: If unpadding fails (invalid padding detected).
    """
    try:
        unpadder = padding.ANSIX923(SEED_BLOCK_SIZE).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()
    except Exception as e:
        raise PaddingError(f"Unpadding failed: {e}")


def seed_encrypt(key, plaintext):
    """
    Encrypt plaintext using SEED algorithm in CBC mode.

    Generates a random IV, applies ANSI X9.23 padding, and encrypts the data.

    Args:
        key (bytes): Symmetric encryption key (must be exactly SEED_KEY_SIZE bytes).
        plaintext (bytes): Plaintext data to encrypt.

    Returns:
        tuple: (iv, ciphertext) where:
            - iv (bytes): Initialization vector (IV_SIZE bytes)
            - ciphertext (bytes): Encrypted data

    Raises:
        EncryptionError: If encryption operation fails.

    Example:
        >>> key = generate_symmetric_key()
        >>> iv, ciphertext = seed_encrypt(key, b'Secret message')
    """
    try:
        iv = os.urandom(IV_SIZE)
        cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_data = pad_data(plaintext)
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv, ciphertext
    except Exception as e:
        raise EncryptionError(f"SEED encryption failed: {e}")


def seed_decrypt(key, iv, ciphertext):
    """
    Decrypt ciphertext using SEED algorithm in CBC mode.

    Args:
        key (bytes): Symmetric encryption key (must be exactly SEED_KEY_SIZE bytes).
        iv (bytes): Initialization vector used during encryption (IV_SIZE bytes).
        ciphertext (bytes): Encrypted data to decrypt.

    Returns:
        bytes: Decrypted plaintext (after padding removal).

    Raises:
        DecryptionError: If decryption operation fails (including padding errors).

    Example:
        >>> plaintext = seed_decrypt(key, iv, ciphertext)
        >>> print(plaintext)
        b'Secret message'
    """
    try:
        cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        return unpad_data(padded_data)
    except Exception as e:
        raise DecryptionError(f"SEED decryption failed: {e}")