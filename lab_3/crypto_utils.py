from aes_utils import decrypt_by_aes, encrypt_by_aes, make_aes_key
from file_utils import read_bytes, write_bytes
from rsa_utils import (
    decrypt_aes_key,
    encrypt_aes_key,
    load_private_key,
    make_rsa_pair,
    save_private_key,
    save_public_key,
)


def get_aes_key(private_key_path, encrypted_key_path):
    """
    Load and decrypt the AES key using the private RSA key.

    Args:
        private_key_path: Path to the private RSA key file.
        encrypted_key_path: Path to the encrypted AES key file.

    Returns:
        bytes: Decrypted AES key.

    Raises:
        RuntimeError: If the AES key cannot be loaded or decrypted.
    """
    try:
        private_key = load_private_key(private_key_path)
        encrypted_key = read_bytes(encrypted_key_path)
        return decrypt_aes_key(encrypted_key, private_key)
    except Exception as exc:
        raise RuntimeError(f"Не удалось получить AES-ключ: {exc}") from exc


def generate_keys(
    encrypted_key_path,
    public_key_path,
    private_key_path,
    aes_key_size,
    rsa_key_size,
    rsa_public_exponent,
):
    """
    Generate RSA keys, AES key and save the encrypted AES key.

    Args:
        encrypted_key_path: Path where the encrypted AES key should be saved.
        public_key_path: Path where the public RSA key should be saved.
        private_key_path: Path where the private RSA key should be saved.
        aes_key_size: AES key size in bits.
        rsa_key_size: RSA key size in bits.
        rsa_public_exponent: RSA public exponent.

    Raises:
        RuntimeError: If key generation or saving fails.
    """
    try:
        aes_key = make_aes_key(aes_key_size)
        private_key, public_key = make_rsa_pair(
            rsa_key_size,
            rsa_public_exponent,
        )

        save_public_key(public_key, public_key_path)
        save_private_key(private_key, private_key_path)

        encrypted_key = encrypt_aes_key(aes_key, public_key)
        write_bytes(encrypted_key_path, encrypted_key)
    except Exception as exc:
        raise RuntimeError(
            f"Генерация ключей завершилась ошибкой: {exc}"
        ) from exc


def encrypt_file(input_path, private_key_path, encrypted_key_path, output_path):
    """
    Encrypt a file with AES using the decrypted symmetric key.

    Args:
        input_path: Path to the source file.
        private_key_path: Path to the private RSA key file.
        encrypted_key_path: Path to the encrypted AES key file.
        output_path: Path where the encrypted file should be saved.

    Raises:
        RuntimeError: If file encryption fails.
    """
    try:
        aes_key = get_aes_key(private_key_path, encrypted_key_path)
        source_data = read_bytes(input_path)
        encrypted_data = encrypt_by_aes(source_data, aes_key)
        write_bytes(output_path, encrypted_data)
    except Exception as exc:
        raise RuntimeError(
            f"Шифрование файла завершилось ошибкой: {exc}"
        ) from exc


def decrypt_file(input_path, private_key_path, encrypted_key_path, output_path):
    """
    Decrypt a file with AES using the decrypted symmetric key.

    Args:
        input_path: Path to the encrypted file.
        private_key_path: Path to the private RSA key file.
        encrypted_key_path: Path to the encrypted AES key file.
        output_path: Path where the decrypted file should be saved.

    Raises:
        RuntimeError: If file decryption fails.
    """
    try:
        aes_key = get_aes_key(private_key_path, encrypted_key_path)
        encrypted_data = read_bytes(input_path)
        decrypted_data = decrypt_by_aes(encrypted_data, aes_key)
        write_bytes(output_path, decrypted_data)
    except Exception as exc:
        raise RuntimeError(
            f"Дешифрование файла завершилось ошибкой: {exc}"
        ) from exc
