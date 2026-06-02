"""
File encryption module for hybrid cryptosystem.

Encrypts arbitrary files using hybrid approach:
- RSA-2048 decrypts the stored symmetric key
- SEED-128 in CBC mode encrypts the actual file content
"""

from asymmetric_crypto import load_private_key, rsa_decrypt
from symmetric_crypto import seed_encrypt
from file_utils import load_bytes, save_bytes
from config import IV_SIZE
from exceptions import KeyLoadError, DecryptionError, EncryptionError, FileOperationError


def encrypt_file(
    input_path,
    private_key_path,
    encrypted_symmetric_key_path,
    output_path,
):
    """
    Encrypt a file using hybrid cryptosystem.

    Workflow:
        1. Load RSA private key and decrypt the stored symmetric key
        2. Read plaintext from input file
        3. Encrypt plaintext with SEED-CBC (generates random IV)
        4. Save IV + ciphertext to output file

    Args:
        input_path (str): Path to plaintext file to encrypt.
        private_key_path (str): Path to RSA private key (.pem) for decrypting symmetric key.
        encrypted_symmetric_key_path (str): Path to file containing RSA-encrypted symmetric key.
        output_path (str): Path where encrypted file (IV + ciphertext) will be saved.

    Raises:
        KeyLoadError: If RSA private key cannot be loaded.
        DecryptionError: If symmetric key decryption fails.
        EncryptionError: If SEED encryption fails.
        FileOperationError: If input/output files cannot be read/written.

    Example:
        >>> encrypt_file(
        ...     'plain.txt',
        ...     'private.pem',
        ...     'encrypted_sym.key',
        ...     'ciphertext.bin'
        ... )
        Starting encryption...
        Loading and decrypting symmetric key...
        Symmetric key decrypted.
        ...
    """
    print("Starting encryption...")

    print("Loading and decrypting symmetric key...")
    private_key = load_private_key(private_key_path)
    encrypted_key = load_bytes(encrypted_symmetric_key_path)
    symmetric_key = rsa_decrypt(private_key, encrypted_key)
    print("Symmetric key decrypted.")

    print(f"Reading plaintext from: {input_path}")
    plaintext = load_bytes(input_path)
    print(f"Read {len(plaintext)} bytes.")

    print(f"Encrypting with SEED-CBC and saving to: {output_path}")
    iv, ciphertext = seed_encrypt(symmetric_key, plaintext)
    output_data = iv + ciphertext
    save_bytes(output_data, output_path)
    print(f"Encrypted {len(plaintext)} bytes -> {len(output_data)} bytes.")
    print("Encryption completed successfully.\n")