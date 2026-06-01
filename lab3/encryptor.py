from asymmetric_crypto import load_private_key, rsa_decrypt
from symmetric_crypto import seed_encrypt
from file_utils import load_bytes, save_bytes


def encrypt_file(
    input_path,
    private_key_path,
    encrypted_symmetric_key_path,
    output_path,
):
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
