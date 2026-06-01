import os

from cryptography.hazmat.primitives import serialization
from crypto_RSA import decrypt_rsa


def save_bytes(data, path):
    """
    Сохранить данные в файл
    
    Args:
        data: байты для сохранения
        path: путь к файлу
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except PermissionError as e:
        raise PermissionError(f"Write permission denied: {path}") from e
    except OSError as e:
        raise OSError(f"Failed to save bytes to {path}: {e}") from e


def load_bytes(path):
    """
    Загрузить содержимое файла
    
    Args:
        path: путь к файлу
    
    Returns:
        bytes: содержимое файла
    """
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {path}") from e
    except PermissionError as e:
        raise PermissionError(f"Read permission denied: {path}") from e
    except OSError as e:
        raise OSError(f"Failed to load bytes from {path}: {e}") from e


def save_public_key(public_key, path):
    """
    Сохранить открытый RSA ключ в PEM формате
    
    Args:
        public_key: открытый ключ RSA
        path: путь для сохранения
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    save_bytes(pem, path)


def save_private_key(private_key, path):
    """
    Сохранить закрытый RSA ключ в PEM формате
    
    Args:
        private_key: закрытый ключ RSA
        path: путь для сохранения
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    save_bytes(pem, path)


def load_private_key(path):
    """
    Загрузить закрытый RSA ключ из PEM файла
    
    Args:
        path: путь к PEM файлу
    
    Returns:
        private key: загруженный закрытый ключ
    """
    data = load_bytes(path)
    try:
        return serialization.load_pem_private_key(data, password=None)
    except ValueError as e:
        raise ValueError(f"Invalid PEM data in {path}: {e}") from e


def load_aes_key(enc_sym_key_path, priv_key_path):
    """
    Загрузить и расшифровать симметричный AES ключ
    
    Args:
        enc_sym_key_path: путь к зашифрованному AES ключу
        priv_key_path: путь к закрытому RSA ключу
    
    Returns:
        bytes: расшифрованный AES ключ
    """
    encrypted_aes_key = load_bytes(enc_sym_key_path)
    priv_key = load_private_key(priv_key_path)
    return decrypt_rsa(encrypted_aes_key, priv_key)