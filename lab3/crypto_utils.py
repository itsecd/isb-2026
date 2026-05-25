import os

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

from file_utils import read_bytes, write_bytes

CAST5_MIN_BITS = 40
CAST5_MAX_BITS = 128


def check_cast5_key_size(key_size_bits):
    """Validate the CAST5 key length."""
    try:
        key_size_bits = int(key_size_bits)
    except (TypeError, ValueError) as exc:
        raise ValueError("Key length must be a number") from exc

    if key_size_bits % 8 != 0:
        raise ValueError(
            f"Key length must be a multiple of 8 bits, got: {key_size_bits}"
        )
    if not (CAST5_MIN_BITS <= key_size_bits <= CAST5_MAX_BITS):
        raise ValueError(
            f"CAST5 key length must be between {CAST5_MIN_BITS} "
            f"and {CAST5_MAX_BITS} bits, got: {key_size_bits}"
        )
    return key_size_bits


def generate_rsa_keys(public_key_path, private_key_path):
    """Generate an RSA key pair and save both keys as PEM files."""
    print("[+] Generating RSA keys (2048 bits)...")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    write_bytes(
        private_key_path,
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ),
    )
    write_bytes(
        public_key_path,
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ),
    )

    print("[+] RSA keys saved")
    return private_key, public_key


def _rsa_oaep_padding():
    """Return an RSA-OAEP padding object."""
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def encrypt_symmetric_key(sym_key, public_key_path, encrypted_key_path):
    """Encrypt a symmetric key with the RSA public key and save it."""
    print("[+] Encrypting CAST5 key with RSA-OAEP...")

    public_key = serialization.load_pem_public_key(read_bytes(public_key_path))
    encrypted_key = public_key.encrypt(sym_key, _rsa_oaep_padding())
    write_bytes(encrypted_key_path, encrypted_key)

    print("[+] Symmetric key encrypted and saved")


def decrypt_symmetric_key(private_key_path, encrypted_key_path):
    """Load and decrypt the symmetric key using the RSA private key."""
    print("[+] Decrypting CAST5 key...")

    private_key = serialization.load_pem_private_key(
        read_bytes(private_key_path), password=None
    )
    encrypted_key = read_bytes(encrypted_key_path)
    sym_key = private_key.decrypt(encrypted_key, _rsa_oaep_padding())

    print("[+] Symmetric key decrypted")
    return sym_key


def generate_cast5_key(key_size_bits=128):
    """Generate a random CAST5 key of the given length (40-128 bits, step 8)."""
    checked = check_cast5_key_size(key_size_bits)
    print(f"[+] Generating CAST5 key ({checked} bits)...")
    key = os.urandom(checked // 8)
    print("[+] CAST5 key created")
    return key


def encrypt_file(input_path, output_path, key):
    """Encrypt a file using CAST5-CBC."""
    print("[+] Reading source file...")
    data = read_bytes(input_path)

    print("[+] Adding PKCS7 padding...")
    padder = PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(8)
    print("[+] Encrypting with CAST5-CBC...")
    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    write_bytes(output_path, iv + encrypted_data)
    print(f"[+] Encrypted file saved: {output_path}")


def decrypt_file(input_path, output_path, key):
    """Decrypt a file using CAST5-CBC."""
    print("[+] Reading encrypted file...")
    encrypted_data = read_bytes(input_path)

    if len(encrypted_data) < 8:
        raise ValueError("Encrypted file is too short (less than 8 bytes)")

    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]

    print("[+] Decrypting with CAST5-CBC...")
    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    print("[+] Removing PKCS7 padding...")
    unpadder = PKCS7(64).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    write_bytes(output_path, data)
    print(f"[+] Decrypted file saved: {output_path}")


def keygen_mode(args):
    """CLI key generation mode."""
    _, public_key_obj = generate_rsa_keys(args.public_key, args.private_key)
    sym_key = generate_cast5_key(args.key_size)
    encrypt_symmetric_key(sym_key, args.public_key, args.encrypted_key)
    print("[+] Key generation complete")


def _crypto_mode(args, file_fn):
    """Shared logic for encrypt/decrypt CLI modes."""
    sym_key = decrypt_symmetric_key(args.private_key, args.encrypted_key)
    file_fn(args.input_file, args.output_file, sym_key)


def encrypt_mode(args):
    """CLI file encryption mode."""
    _crypto_mode(args, encrypt_file)
    print("[+] Encryption complete")


def decrypt_mode(args):
    """CLI file decryption mode."""
    _crypto_mode(args, decrypt_file)
    print("[+] Decryption complete")
