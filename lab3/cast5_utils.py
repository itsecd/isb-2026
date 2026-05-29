import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

from exceptions import KeySizeError, EncryptionError, DecryptionError
from file_utils import read_bytes, write_bytes


def check_cast5_key_size(key_size_bits, min_bits, max_bits):
    """
    Validate CAST5 key length.

    Args:
        key_size_bits: CAST5 key length in bits.
        min_bits: Minimum allowed bits.
        max_bits: Maximum allowed bits.

    Returns:
        Validated CAST5 key length in bytes.

    Raises:
        KeySizeError: If key length is invalid.
    """
    try:
        key_size_bits = int(key_size_bits)

    except (TypeError, ValueError) as exc:
        raise KeySizeError("Key length must be a number") from exc

    if key_size_bits % 8 != 0:
        raise KeySizeError("Key length must be multiple of 8 bits")

    if not (min_bits <= key_size_bits <= max_bits):
        raise KeySizeError(
            f"CAST5 key length must be between {min_bits} and {max_bits} bits"
        )

    return key_size_bits // 8


def generate_cast5_key(key_size_bits, min_bits, max_bits):
    """
    Generate random CAST5 key.

    Args:
        key_size_bits: CAST5 key length in bits.
        min_bits: Minimum allowed bits.
        max_bits: Maximum allowed bits.

    Returns:
        Generated CAST5 key.

    Raises:
        KeySizeError: If key size is invalid.
        KeyGenerationError: If key generation fails.
    """
    from exceptions import KeyGenerationError

    key_bytes = check_cast5_key_size(key_size_bits, min_bits, max_bits)

    try:
        return os.urandom(key_bytes)
    except Exception as exc:
        raise KeyGenerationError(f"Failed to generate CAST5 key: {exc}") from exc


def encrypt_file(input_path, output_path, key, block_size, iv_size):
    """
    Encrypt file using CAST5-CBC.

    Args:
        input_path: Path to input file.
        output_path: Path to encrypted output file.
        key: CAST5 encryption key.
        block_size: CAST5 block size in bits.
        iv_size: IV size in bytes.

    Raises:
        FileOperationError: If files cannot be read/written.
        EncryptionError: If encryption fails.
    """
    data = read_bytes(input_path)

    padder = PKCS7(block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(iv_size)

    try:
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    except Exception as exc:
        raise EncryptionError(f"CAST5 encryption failed: {exc}") from exc

    write_bytes(output_path, iv + encrypted_data)


def decrypt_file(input_path, output_path, key, block_size, iv_size):
    """
    Decrypt file using CAST5-CBC.

    Args:
        input_path: Path to encrypted file.
        output_path: Path to decrypted output file.
        key: CAST5 decryption key.
        block_size: CAST5 block size in bits.
        iv_size: IV size in bytes.

    Raises:
        FileOperationError: If files cannot be read/written.
        DecryptionError: If decryption fails or file is invalid.
    """
    encrypted_data = read_bytes(input_path)

    if len(encrypted_data) < iv_size:
        raise DecryptionError("Encrypted file is too short")

    iv = encrypted_data[:iv_size]
    ciphertext = encrypted_data[iv_size:]

    try:
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    except Exception as exc:
        raise DecryptionError(f"CAST5 decryption failed: {exc}") from exc

    try:
        unpadder = PKCS7(block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
    except Exception as exc:
        raise DecryptionError(f"Padding removal failed: {exc}") from exc

    write_bytes(output_path, data)
