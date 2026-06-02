"""
File decryption module for hybrid cryptosystem.

Decrypts files that were encrypted with the hybrid approach:
- RSA-2048 decrypts the stored symmetric key
- SEED-128 in CBC mode decrypts the file content using extracted IV
"""

from asymmetric_crypto import load_private_key, rsa_decrypt
from symmetric_crypto import seed_decrypt
from file_utils import load_bytes, save_bytes
from config import config
from exceptions import KeyLoadError, DecryptionError, FileOperationError


def decrypt_file():
    """
    Decrypt a file encrypted with hybrid cryptosystem.

    Workflow:
        1. Load RSA private key and decrypt the stored symmetric key
        2. Read encrypted file (IV + ciphertext)
        3. Extract IV (first IV_SIZE bytes) and ciphertext (remaining bytes)
        4. Decrypt ciphertext with SEED-CBC using extracted IV
        5. Save plaintext to output file

    Raises:
        KeyLoadError: If RSA private key cannot be loaded.
        DecryptionError: If symmetric key decryption or SEED decryption fails.
        FileOperationError: If input/output files cannot be read/written.

    Example:
        >>> decrypt_file()
        Starting decryption...
        Loading and decrypting symmetric key...
        Symmetric key decrypted.
        ...
    """
    print("Starting decryption...")

    print("Loading and decrypting symmetric key...")
    private_key = load_private_key(config.private_key)
    encrypted_key = load_bytes(config.symmetric_key)
    symmetric_key = rsa_decrypt(private_key, encrypted_key)
    print("Symmetric key decrypted.")

    print(f"Reading ciphertext from: {config.encrypted_file}")
    data = load_bytes(config.encrypted_file)
    iv = data[:config.seed_iv_size]
    ciphertext = data[config.seed_iv_size:]
    print(f"Read {len(data)} bytes (IV: {config.seed_iv_size}, ciphertext: {len(ciphertext)}).")

    print(f"Decrypting with SEED-CBC and saving to: {config.decrypted_file}")
    plaintext = seed_decrypt(symmetric_key, iv, ciphertext)
    save_bytes(plaintext, config.decrypted_file)
    print(f"Decrypted {len(ciphertext)} bytes -> {len(plaintext)} bytes.")
    print("Decryption completed successfully.\n")