"""
Key generation module for hybrid cryptosystem.

Orchestrates generation of both symmetric (SEED) and asymmetric (RSA) keys,
then securely encrypts the symmetric key with RSA public key for storage.
"""

from symmetric_crypto import generate_symmetric_key
from asymmetric_crypto import (
    generate_asymmetric_keys,
    serialize_private_key,
    serialize_public_key,
    rsa_encrypt,
)
from file_utils import save_bytes
from config import config
from exceptions import KeyGenerationError, EncryptionError, FileOperationError


def generate_keys():
    """
    Generate complete key set for hybrid cryptosystem.

    Workflow:
        1. Generate random SEED-128 symmetric key
        2. Generate RSA-2048 key pair
        3. Save RSA keys to PEM files
        4. Encrypt symmetric key with RSA public key
        5. Save encrypted symmetric key to file

    Raises:
        KeyGenerationError: If key generation fails.
        EncryptionError: If symmetric key encryption fails.
        FileOperationError: If file writing fails.

    Example:
        >>> generate_keys()
        Starting key generation...
        Generating symmetric key (SEED, 128 bit)...
        Done.
        Generating asymmetric key pair (RSA-2048)...
        Done.
        ...
    """
    print("Starting key generation...")

    config.ensure_directories()

    print("Generating symmetric key (SEED, 128 bit)...")
    symmetric_key = generate_symmetric_key()
    print("Done.")

    print("Generating asymmetric key pair (RSA-2048)...")
    private_key, public_key = generate_asymmetric_keys()
    print("Done.")

    print("Saving public and private keys...")
    serialize_public_key(public_key, config.public_key)
    serialize_private_key(private_key, config.private_key)
    print(f"Public key  -> {config.public_key}")
    print(f"Private key -> {config.private_key}")

    print("Encrypting symmetric key with RSA public key...")
    encrypted_key = rsa_encrypt(public_key, symmetric_key)
    save_bytes(encrypted_key, config.symmetric_key)
    print(f"Encrypted symmetric key -> {config.symmetric_key}")

    print("Key generation completed successfully.\n")