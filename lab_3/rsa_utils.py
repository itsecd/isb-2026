from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa

from file_utils import read_bytes, write_bytes


def check_rsa_params(key_size, public_exponent):
    """
    Check that RSA parameters are valid.

    Args:
        key_size: RSA key size in bits.
        public_exponent: RSA public exponent.

    Returns:
        tuple: Valid RSA key size and public exponent.

    Raises:
        ValueError: If RSA parameters are invalid.
    """
    try:
        key_size = int(key_size)
        public_exponent = int(public_exponent)
    except (TypeError, ValueError) as exc:
        raise ValueError("Параметры RSA должны быть числами") from exc

    if key_size < 2048:
        raise ValueError("Размер RSA-ключа должен быть не меньше 2048 бит")

    if public_exponent not in (3, 65537):
        raise ValueError("Открытая экспонента RSA должна быть 3 или 65537")

    return key_size, public_exponent


def make_rsa_pair(key_size, public_exponent):
    """
    Generate a private and public RSA key pair.

    Args:
        key_size: RSA key size in bits.
        public_exponent: RSA public exponent.

    Returns:
        tuple: Private RSA key and public RSA key.

    Raises:
        ValueError: If RSA keys cannot be generated.
    """
    checked_size, checked_exponent = check_rsa_params(
        key_size,
        public_exponent,
    )

    try:
        private_key = rsa.generate_private_key(
            public_exponent=checked_exponent,
            key_size=checked_size,
        )
    except ValueError as exc:
        raise ValueError(f"Не удалось создать RSA-ключи: {exc}") from exc

    return private_key, private_key.public_key()


def get_rsa_padding():
    """
    Create RSA-OAEP padding settings.

    Returns:
        OAEP: Padding settings for RSA encryption and decryption.
    """
    return asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def save_public_key(public_key, path):
    """
    Save a public RSA key in PEM format.

    Args:
        public_key: Public RSA key object.
        path: Path where the public key should be saved.

    Raises:
        ValueError: If the public key cannot be serialized.
        OSError: If the key file cannot be written.
    """
    try:
        key_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Ошибка сериализации открытого RSA-ключа: {exc}"
        ) from exc

    write_bytes(path, key_data)


def save_private_key(private_key, path):
    """
    Save a private RSA key in PEM format.

    Args:
        private_key: Private RSA key object.
        path: Path where the private key should be saved.

    Raises:
        ValueError: If the private key cannot be serialized.
        OSError: If the key file cannot be written.
    """
    try:
        key_data = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Ошибка сериализации закрытого RSA-ключа: {exc}"
        ) from exc

    write_bytes(path, key_data)


def load_private_key(path):
    """
    Load a private RSA key from a PEM file.

    Args:
        path: Path to the private RSA key file.

    Returns:
        RSAPrivateKey: Loaded private RSA key.

    Raises:
        ValueError: If the private key cannot be loaded.
        FileNotFoundError: If the key file does not exist.
        OSError: If the key file cannot be read.
    """
    key_data = read_bytes(path)

    try:
        return serialization.load_pem_private_key(
            key_data,
            password=None,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Не удалось загрузить закрытый RSA-ключ: {path}. {exc}"
        ) from exc


def encrypt_aes_key(aes_key, public_key):
    """
    Encrypt an AES key using the public RSA key.

    Args:
        aes_key: AES key as bytes.
        public_key: Public RSA key object.

    Returns:
        bytes: Encrypted AES key.

    Raises:
        ValueError: If AES key encryption fails.
    """
    try:
        return public_key.encrypt(
            aes_key,
            get_rsa_padding(),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Не удалось зашифровать AES-ключ: {exc}") from exc


def decrypt_aes_key(encrypted_key, private_key):
    """
    Decrypt an AES key using the private RSA key.

    Args:
        encrypted_key: Encrypted AES key as bytes.
        private_key: Private RSA key object.

    Returns:
        bytes: Decrypted AES key.

    Raises:
        ValueError: If AES key decryption fails.
    """
    try:
        return private_key.decrypt(
            encrypted_key,
            get_rsa_padding(),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Не удалось расшифровать AES-ключ: {exc}"
        ) from exc
