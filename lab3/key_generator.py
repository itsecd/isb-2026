from utils import (
    generate_symmetric_key,
    generate_asymmetric_keys,
    serialize_private_key,
    serialize_public_key,
    rsa_encrypt,
    save_bytes,
)


def generate_keys(
    encrypted_symmetric_key_path,
    public_key_path,
    private_key_path,
):
    print("Starting key generation...")

    print("Generating symmetric key (SEED, 128 bit)...")
    symmetric_key = generate_symmetric_key()
    print("Done.")

    print("Generating asymmetric key pair (RSA-2048)...")
    private_key, public_key = generate_asymmetric_keys()
    print(" Done.")

    print("Saving public and private keys...")
    serialize_public_key(public_key, public_key_path)
    serialize_private_key(private_key, private_key_path)
    print(f"Public key  -> {public_key_path}")
    print(f"Private key -> {private_key_path}")

    print("Encrypting symmetric key with RSA public key...")
    encrypted_key = rsa_encrypt(public_key, symmetric_key)
    save_bytes(encrypted_key, encrypted_symmetric_key_path)
    print(f"Encrypted symmetric key -> {encrypted_symmetric_key_path}")

    print("Key generation completed successfully.\n")