"""
File decryption module for hybrid cryptosystem.

Decrypts files that were encrypted with the hybrid approach:
- RSA-2048 decrypts the stored symmetric key
- SEED-128 in CBC mode decrypts the file content using extracted IV
"""

from asymmetric_crypto import load_private_key, rsa_decrypt
from symmetric_crypto import seed_decrypt
from file_utils import load_bytes, save_bytes
from config import IV_SIZE
from exceptions import KeyLoadError, DecryptionError, FileOperationError


def decrypt_file(
    encrypted_input_path,
    private_key_path,
    encrypted_symmetric_key_path,
    output_path,
):
    """
    Decrypt a file encrypted with hybrid cryptosystem.

    Workflow:
        1. Load RSA private key and decrypt the stored symmetric key
        2. Read encrypted file (IV + ciphertext)
        3. Extract IV (first IV_SIZE bytes) and ciphertext (remaining bytes)
        4. Decrypt ciphertext with SEED-CBC using extracted IV
        5. Save plaintext to output file

    Args:
        encrypted_input_path (str): Path to encrypted file (IV + ciphertext).
        private_key_path (str): Path to RSA private key (.pem) for decrypting symmetric key.
        encrypted_symmetric_key_path (str): Path to file containing RSA-encrypted symmetric key.
        output_path (str): Path where decrypted plaintext will be saved.

    Raises:
        KeyLoadError: If RSA private key cannot be loaded.
        DecryptionError: If symmetric key decryption or SEED decryption fails.
        FileOperationError: If input/output files cannot be read/written.

    Example:
        >>> decrypt_file(
        ...     'ciphertext.bin',
        ...     'private.pem',
        ...     'encrypted_sym.key',
        ...     'decrypted.txt'
        ... )
        Starting decryption...
        Loading and decrypting symmetric key...
        Symmetric key decrypted.
        ...
    """
    print("Starting decryption...")

    print("Loading and decrypting symmetric key...")
    private_key = load_private_key(private_key_path)
    encrypted_key = load_bytes(encrypted_symmetric_key_path)
    symmetric_key = rsa_decrypt(private_key, encrypted_key)
    print("Symmetric key decrypted.")

    print(f"Reading ciphertext from: {encrypted_input_path}")
    data = load_bytes(encrypted_input_path)
    iv = data[:IV_SIZE]
    ciphertext = data[IV_SIZE:]
    print(f"Read {len(data)} bytes (IV: {IV_SIZE}, ciphertext: {len(ciphertext)}).")

    print(f"Decrypting with SEED-CBC and saving to: {output_path}")
    plaintext = seed_decrypt(symmetric_key, iv, ciphertext)
    save_bytes(plaintext, output_path)
    print(f"Decrypted {len(ciphertext)} bytes -> {len(plaintext)} bytes.")
    print("Decryption completed successfully.\n")