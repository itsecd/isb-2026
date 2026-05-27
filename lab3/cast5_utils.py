import os

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes,
)
from cryptography.hazmat.primitives.padding import PKCS7

from config_loader import load_crypto_config
from file_utils import read_bytes, write_bytes


CONFIG = load_crypto_config()

CAST5_MIN_BITS = CONFIG["cast5_min_bits"]
CAST5_MAX_BITS = CONFIG["cast5_max_bits"]

CAST5_BLOCK_SIZE = CONFIG["cast5_block_size"]
CAST5_IV_SIZE = CONFIG["cast5_iv_size"]


def check_cast5_key_size(key_size_bits):
    """
    Validate CAST5 key length.

    args:
        key_size_bits:
            CAST5 key length in bits

    return:
        validated CAST5 key length

    raises:
        ValueError:
            if key length is invalid
    """

    try:
        key_size_bits = int(key_size_bits)

    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Key length must be a number"
        ) from exc

    if key_size_bits % 8 != 0:
        raise ValueError(
            "Key length must be multiple of 8 bits"
        )

    if not (
        CAST5_MIN_BITS <= key_size_bits <= CAST5_MAX_BITS
    ):
        raise ValueError(
            f"CAST5 key length must be between "
            f"{CAST5_MIN_BITS} and "
            f"{CAST5_MAX_BITS} bits"
        )

    return key_size_bits


def generate_cast5_key(
    key_size_bits=CAST5_MAX_BITS,
):
    """
    Generate random CAST5 key.

    args:
        key_size_bits:
            CAST5 key length in bits

    return:
        generated CAST5 key
    """

    checked_key_size = check_cast5_key_size(
        key_size_bits
    )

    return os.urandom(checked_key_size // 8)


def encrypt_file(
    input_path,
    output_path,
    key,
):
    """
    Encrypt file using CAST5-CBC.

    args:
        input_path:
            path to input file

        output_path:
            path to encrypted output file

        key:
            CAST5 encryption key
    """

    data = read_bytes(input_path)

    padder = PKCS7(CAST5_BLOCK_SIZE).padder()

    padded_data = (
        padder.update(data) +
        padder.finalize()
    )

    iv = os.urandom(CAST5_IV_SIZE)

    cipher = Cipher(
        algorithms.CAST5(key),
        modes.CBC(iv),
    )

    encryptor = cipher.encryptor()

    encrypted_data = (
        encryptor.update(padded_data) +
        encryptor.finalize()
    )

    write_bytes(
        output_path,
        iv + encrypted_data,
    )


def decrypt_file(
    input_path,
    output_path,
    key,
):
    """
    Decrypt file using CAST5-CBC.

    args:
        input_path:
            path to encrypted file

        output_path:
            path to decrypted output file

        key:
            CAST5 decryption key

    raises:
        ValueError:
            if encrypted file is invalid
    """

    encrypted_data = read_bytes(input_path)

    if len(encrypted_data) < CAST5_IV_SIZE:
        raise ValueError(
            "Encrypted file is too short"
        )

    iv = encrypted_data[:CAST5_IV_SIZE]

    ciphertext = encrypted_data[CAST5_IV_SIZE:]

    cipher = Cipher(
        algorithms.CAST5(key),
        modes.CBC(iv),
    )

    decryptor = cipher.decryptor()

    padded_data = (
        decryptor.update(ciphertext) +
        decryptor.finalize()
    )

    unpadder = PKCS7(CAST5_BLOCK_SIZE).unpadder()

    data = (
        unpadder.update(padded_data) +
        unpadder.finalize()
    )

    write_bytes(output_path, data)
