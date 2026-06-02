"""
File encryption module for hybrid cryptosystem.

Encrypts arbitrary files using hybrid approach:
- RSA-2048 decrypts the stored symmetric key
- SEED-128 in CBC mode encrypts the actual file content
"""

from asymmetric_crypto import load_private_key, rsa_decrypt
from symmetric_crypto import seed_encrypt
from file_utils import load_bytes, save_bytes
from config import config
from exceptions import KeyLoadError, DecryptionError, EncryptionError, FileOperationError


def encrypt_file():
    """
    Encrypt a file using hybrid cryptosystem.

    Workflow:
        1. Load RSA private key and decrypt the stored symmetric key
        2. Read plaintext from input file
        3. Encrypt plaintext with SEED-CBC (generates random IV)
        4. Save IV + ciphertext to output file

    Raises:
        KeyLoadError: If RSA private key cannot be loaded.
        DecryptionError: If symmetric key decryption fails.
        EncryptionError: If SEED encryption fails.
        FileOperationError: If input/output files cannot be read/written.

    Example:
        >>> encrypt_file()
        Starting encryption...
        Loading and decrypting symmetric key...
        Symmetric key decrypted.
        ...
    """
    print("Starting encryption...")

    config.ensure_directories()

    print("Loading and decrypting symmetric key...")
    private_key = load_private_key(config.private_key)
    encrypted_key = load_bytes(config.symmetric_key)
    symmetric_key = rsa_decrypt(private_key, encrypted_key)
    print("Symmetric key decrypted.")

    print(f"Reading plaintext from: {config.initial_file}")
    plaintext = load_bytes(config.initial_file)
    print(f"Read {len(plaintext)} bytes.")

    print(f"Encrypting with SEED-CBC and saving to: {config.encrypted_file}")
    iv, ciphertext = seed_encrypt(symmetric_key, plaintext)
    output_data = iv + ciphertext
    save_bytes(output_data, config.encrypted_file)
    print(f"Encrypted {len(plaintext)} bytes -> {len(output_data)} bytes.")
    print("Encryption completed successfully.\n")