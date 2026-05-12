from utils import (
    load_private_key,
    rsa_decrypt,
    load_bytes,
    seed_decrypt,
    IV_SIZE,
)


def decrypt_file(
    encrypted_input_path,
    private_key_path,
    encrypted_symmetric_key_path,
    output_path,
):
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
    print(f" Read {len(data)} bytes (IV: {IV_SIZE}, ciphertext: {len(ciphertext)}).")

    print(f"Decrypting with SEED-CBC and saving to: {output_path}")
    plaintext = seed_decrypt(symmetric_key, iv, ciphertext)
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    print(f"Decrypted {len(ciphertext)} bytes -> {len(plaintext)} bytes.")
    print("Decryption completed successfully.\n")