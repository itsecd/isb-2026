import os

from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def check_aes_key_size(key_size):
    """
    Check that the AES key size is valid.

    Args:
        key_size: AES key size in bits.

    Returns:
        int: Valid AES key size.

    Raises:
        ValueError: If the key size is not a number or is not supported.
    """
    try:
        key_size = int(key_size)
    except (TypeError, ValueError) as exc:
        raise ValueError("Размер AES-ключа должен быть числом") from exc

    if key_size not in (128, 192, 256):
        raise ValueError(
            "Размер AES-ключа должен быть 128, 192 или 256 бит"
        )

    return key_size


def make_aes_key(key_size):
    """
    Generate a random AES key with the selected size.

    Args:
        key_size: AES key size in bits.

    Returns:
        bytes: Generated AES key.

    Raises:
        ValueError: If the AES key size is invalid.
    """
    checked_size = check_aes_key_size(key_size)
    return os.urandom(checked_size // 8)


def add_padding(data):
    """
    Add PKCS7 padding before AES encryption.

    Args:
        data: Source data as bytes.

    Returns:
        bytes: Data with PKCS7 padding.

    Raises:
        ValueError: If padding cannot be added.
    """
    try:
        padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
        return padder.update(data) + padder.finalize()
    except ValueError as exc:
        raise ValueError(f"Не удалось добавить padding: {exc}") from exc


def remove_padding(data):
    """
    Remove PKCS7 padding after AES decryption.

    Args:
        data: Decrypted data with PKCS7 padding.

    Returns:
        bytes: Data without padding.

    Raises:
        ValueError: If padding cannot be removed.
    """
    try:
        unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(data) + unpadder.finalize()
    except ValueError as exc:
        raise ValueError(
            f"Не удалось убрать padding. Возможно, неверный ключ или файл: {exc}"
        ) from exc


def encrypt_by_aes(data, aes_key):
    """
    Encrypt bytes with AES-CBC.

    Args:
        data: Source data as bytes.
        aes_key: AES key as bytes.

    Returns:
        bytes: IV joined with encrypted data.

    Raises:
        ValueError: If AES encryption fails.
    """
    iv_size = algorithms.AES.block_size // 8
    iv = os.urandom(iv_size)
    padded_data = add_padding(data)

    try:
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data)
        encrypted_data += encryptor.finalize()
    except ValueError as exc:
        raise ValueError(f"Ошибка AES-шифрования: {exc}") from exc

    return iv + encrypted_data


def decrypt_by_aes(data, aes_key):
    """
    Decrypt bytes with AES-CBC.

    Args:
        data: Encrypted data with IV at the beginning.
        aes_key: AES key as bytes.

    Returns:
        bytes: Decrypted data without padding.

    Raises:
        ValueError: If encrypted data is invalid or AES decryption fails.
    """
    iv_size = algorithms.AES.block_size // 8

    if len(data) < iv_size:
        raise ValueError("Зашифрованный файл слишком короткий")

    iv = data[:iv_size]
    encrypted_data = data[iv_size:]

    try:
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
        )
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data)
        decrypted_data += decryptor.finalize()
    except ValueError as exc:
        raise ValueError(f"Ошибка AES-дешифрования: {exc}") from exc

    return remove_padding(decrypted_data)
