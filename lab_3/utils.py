from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def read_bytes(path: str) -> bytes:
    """Читает содержимое файла в байтах по указанному пути."""
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError as e:
        raise OSError(f"Файл '{path}' не прочитался: {e}")


def write_bytes(path: str, data: bytes) -> None:
    """Записывает байты в файл по указанному пути."""
    try:
        with open(path, "wb") as f:
            f.write(data)
    except OSError as e:
        raise OSError(f"Файл '{path}' не сохранился: {e}")


def load_private_key(path: str):
    """Загружает закрытый RSA ключ из PEM файла по указанному пути."""
    try:
        private_bytes = read_bytes(path)
        return load_pem_private_key(private_bytes, password=None)
    except ValueError as e:
        raise ValueError(f"Закрытый ключ '{path}' повреждён: {e}")


def save_public_key(path: str, public_key) -> None:
    """Сохраняет открытый RSA ключ в PEM формате по указанному пути."""
    data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    write_bytes(path, data)


def save_private_key(path: str, private_key) -> None:
    """Сохраняет закрытый RSA ключ в PEM формате по указанному пути."""
    data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    write_bytes(path, data)