import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from utils import write_file

def serialize_public_key(public_key) -> bytes:
    """Сериализовать открытый RSA-ключ в формат PEM.
    Args:
        public_key: Объект открытого RSA-ключа (cryptography).
    Returns:
        Байтовое представление ключа в формате PEM.
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def serialize_private_key(private_key) -> bytes:
    """Сериализовать закрытый RSA-ключ в формат PEM.
    Args:
        private_key: Объект закрытого RSA-ключа (cryptography).
    Returns:
        Байтовое представление ключа в формате PEM (без парольной защиты).
    """
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

def generate_rsa_keys(key_size: int = 2048):
    """Сгенерировать пару RSA-ключей.
    Args:
        key_size: Размер ключа в битах (по умолчанию 2048).
    Returns:
        Кортеж (private_key, public_key) объектов ключей.
    Raises:
        RuntimeError: При ошибках генерации ключей.
    """
    print(f"Генерация RSA-ключей ({key_size} бит).")
    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        print("RSA-ключи сгенерированы")
        return private_key, public_key
    except Exception as e:
        raise RuntimeError(f"Ошибка при генерации RSA-ключей: {e}") from e

def save_rsa_keys(private_key, public_key, private_path: str, public_path: str) -> None:
    """Сохранить пару RSA-ключей в PEM-файлы.
    Args:
        private_key: Объект закрытого ключа.
        public_key:  Объект открытого ключа.
        private_path: Путь для сохранения закрытого ключа.
        public_path:  Путь для сохранения открытого ключа.
    Raises:
        RuntimeError: При ошибках сериализации или записи файлов.
    """
    public_bytes = serialize_public_key(public_key)
    write_file(public_path, public_bytes)
    print(f"Открытый ключ сохранён: {public_path}")

    private_bytes = serialize_private_key(private_key)
    write_file(private_path, private_bytes)
    print(f"Закрытый ключ сохранён: {private_path}")

def generate_aes_key(key_size_bits: int) -> bytes:
    """Сгенерировать случайный симметричный AES-ключ.
    Args:
        key_size_bits: Длина ключа в битах (128, 192 или 256).
    Returns:
        Случайные байты ключа (16, 24 или 32 байта).
    Raises:
        ValueError: Если указана недопустимая длина ключа.
    """
    match key_size_bits:
        case 128 | 192 | 256:
            key_size_bytes = key_size_bits // 8
            key = os.urandom(key_size_bytes)
            print(f"Симметричный ключ AES-{key_size_bits} сгенерирован ({key_size_bytes} байт)")
            return key
        case _:
            raise ValueError(f"Некорректная длина ключа AES: {key_size_bits}. Допустимые значения: 128, 192, 256.")
