import os

from cryptography.hazmat.primitives import hashes, padding as sym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from file_utils import read_bytes, write_bytes


def check_aes_key_size(key_size):
    """Check that the AES key size is valid."""
    try:
        key_size = int(key_size)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Размер AES-ключа должен быть числом"
        ) from exc

    match key_size:
        case 128 | 192 | 256:
            return key_size
        case _:
            raise ValueError(
                "Размер AES-ключа должен быть 128, 192 или 256 бит"
            )


def check_rsa_params(key_size, public_exponent):
    """Check that RSA parameters are suitable for key generation."""
    try:
        key_size = int(key_size)
        public_exponent = int(public_exponent)
    except (TypeError, ValueError) as exc:
        raise ValueError("Параметры RSA должны быть числами") from exc

    match key_size >= 2048:
        case True:
            pass
        case False:
            raise ValueError("Размер RSA-ключа должен быть не меньше 2048 бит")

    match public_exponent:
        case 3 | 65537:
            return key_size, public_exponent
        case _:
            raise ValueError("Открытая экспонента RSA должна быть 3 или 65537")


def make_aes_key(key_size):
    """Generate a random AES key with the selected size."""
    checked_size = check_aes_key_size(key_size)
    return os.urandom(checked_size // 8)


def make_rsa_pair(key_size, public_exponent):
    """Generate a private and public RSA key pair."""
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
        raise ValueError("Не удалось создать RSA-ключи") from exc

    return private_key, private_key.public_key()


def get_rsa_padding():
    """Create RSA-OAEP padding settings."""
    return asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def save_public_key(public_key, path):
    """Save a public RSA key in PEM format."""
    try:
        key_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Ошибка сериализации открытого RSA-ключа") from exc

    write_bytes(path, key_data)


def save_private_key(private_key, path):
    """Save a private RSA key in PEM format."""
    try:
        key_data = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Ошибка сериализации закрытого RSA-ключа") from exc

    write_bytes(path, key_data)


def load_private_key(path):
    """Load a private RSA key from a PEM file."""
    key_data = read_bytes(path)

    try:
        return serialization.load_pem_private_key(
            key_data,
            password=None,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Не удалось загрузить закрытый RSA-ключ: {path}"
        ) from exc


def encrypt_aes_key(aes_key, public_key):
    """Encrypt an AES key using the public RSA key."""
    try:
        return public_key.encrypt(
            aes_key,
            get_rsa_padding(),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Не удалось зашифровать AES-ключ") from exc


def decrypt_aes_key(encrypted_key, private_key):
    """Decrypt an AES key using the private RSA key."""
    try:
        return private_key.decrypt(
            encrypted_key,
            get_rsa_padding(),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Не удалось расшифровать AES-ключ") from exc


def add_padding(data):
    """Add PKCS7 padding before AES encryption."""
    try:
        padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
        return padder.update(data) + padder.finalize()
    except ValueError as exc:
        raise ValueError("Не удалось добавить padding") from exc


def remove_padding(data):
    """Remove PKCS7 padding after AES decryption."""
    try:
        unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(data) + unpadder.finalize()
    except ValueError as exc:
        raise ValueError(
            "Не удалось убрать padding. Возможно, неверный ключ или файл"
        ) from exc


def encrypt_by_aes(data, aes_key):
    """Encrypt bytes with AES-CBC and return IV with ciphertext."""
    iv_size = algorithms.AES.block_size // 8
    iv = os.urandom(iv_size)
    padded_data = add_padding(data)

    try:
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data)
        encrypted_data += encryptor.finalize()
    except ValueError as exc:
        raise ValueError("Ошибка AES-шифрования") from exc

    return iv + encrypted_data


def decrypt_by_aes(data, aes_key):
    """Decrypt bytes with AES-CBC using IV from the file beginning."""
    iv_size = algorithms.AES.block_size // 8

    match len(data) < iv_size:
        case True:
            raise ValueError("Зашифрованный файл слишком короткий")
        case False:
            pass

    iv = data[:iv_size]
    encrypted_data = data[iv_size:]

    try:
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
        )
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data)
        decrypted_data += decryptor.finalize()
    except ValueError as exc:
        raise ValueError("Ошибка AES-дешифрования") from exc

    return remove_padding(decrypted_data)


def get_aes_key(private_key_path, encrypted_key_path):
    """Load and decrypt the AES key using the private RSA key."""
    try:
        private_key = load_private_key(private_key_path)
        encrypted_key = read_bytes(encrypted_key_path)
        return decrypt_aes_key(encrypted_key, private_key)
    except Exception as exc:
        raise RuntimeError("Не удалось получить AES-ключ") from exc


def generate_keys(
    encrypted_key_path,
    public_key_path,
    private_key_path,
    aes_key_size,
    rsa_key_size,
    rsa_public_exponent,
):
    """Generate RSA keys, AES key and save the encrypted AES key."""
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
        raise RuntimeError("Генерация ключей завершилась ошибкой") from exc


def encrypt_file(input_path, private_key_path, encrypted_key_path, output_path):
    """Encrypt a file with AES using the decrypted symmetric key."""
    try:
        aes_key = get_aes_key(private_key_path, encrypted_key_path)
        source_data = read_bytes(input_path)
        encrypted_data = encrypt_by_aes(source_data, aes_key)
        write_bytes(output_path, encrypted_data)
    except Exception as exc:
        raise RuntimeError("Шифрование файла завершилось ошибкой") from exc


def decrypt_file(input_path, private_key_path, encrypted_key_path, output_path):
    """Decrypt a file with AES using the decrypted symmetric key."""
    try:
        aes_key = get_aes_key(private_key_path, encrypted_key_path)
        encrypted_data = read_bytes(input_path)
        decrypted_data = decrypt_by_aes(encrypted_data, aes_key)
        write_bytes(output_path, decrypted_data)
    except Exception as exc:
        raise RuntimeError("Дешифрование файла завершилось ошибкой") from exc