from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def read_bytes(path: str) -> bytes:
    """
    Читает содержимое файла в байтах.

    Args:
        path: путь к файлу для чтения
    """
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл '{path}' не найден: {e}")
    except PermissionError as e:
        raise PermissionError(f"Нет доступа к файлу '{path}': {e}")
    except OSError as e:
        raise OSError(f"Ошибка при чтении файла '{path}': {e}")


def write_bytes(path: str, data: bytes) -> None:
    """
    Записывает байты в файл.

    Args:
        path: путь к файлу для записи
        data: данные для записи
    """
    try:
        with open(path, "wb") as f:
            f.write(data)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Папка для файла '{path}' не найдена: {e}")
    except PermissionError as e:
        raise PermissionError(f"Нет доступа к файлу '{path}': {e}")
    except OSError as e:
        raise OSError(f"Ошибка при записи файла '{path}': {e}")


def load_private_key(path: str) -> RSAPrivateKey:
    """
    Загружает закрытый RSA ключ из файла.

    Args:
        path: путь к PEM файлу с закрытым ключом
    """
    try:
        private_bytes = read_bytes(path)
        return load_pem_private_key(private_bytes, password=None)
    except ValueError as e:
        raise ValueError(f"Закрытый ключ '{path}' повреждён: {e}")


def save_public_key(path: str, public_key: RSAPublicKey) -> None:
    """
    Сохраняет открытый RSA ключ.

    Args:
        path: путь для сохранения ключа
        public_key: открытый RSA ключ
    """
    data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    write_bytes(path, data)


def save_private_key(path: str, private_key: RSAPrivateKey) -> None:
    """
    Сохраняет закрытый RSA ключ.

    Args:
        path: путь для сохранения ключа
        private_key: закрытый RSA ключ
    """
    data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    write_bytes(path, data)