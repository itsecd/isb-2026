import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from utils import fail, write_file


def generate_rsa_keys(key_size: int = 2048):
    """
    Сгенерировать пару RSA-ключей.

    Параметры:
        key_size: размер ключа в битах (по умолчанию 2048).

    Возвращает:
        (private_key, public_key): закрытый и открытый RSA-ключи.
    """
    print(f"Генерация RSA-ключей ({key_size} бит).")
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        public_key = private_key.public_key()
        print("RSA-ключи сгенерированы")
        return private_key, public_key
    except Exception as e:
        fail(f"Ошибка при генерации RSA-ключей: {e}")


def save_rsa_keys(private_key, public_key, private_path: str, public_path: str) -> None:
    """
    Сохранить RSA-ключи в PEM-файлы.

    Параметры:
        private_key:  закрытый RSA-ключ.
        public_key:   открытый RSA-ключ.
        private_path: путь для сохранения закрытого ключа (.pem).
        public_path:  путь для сохранения открытого ключа (.pem).
    """
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    write_file(public_path, public_bytes)
    print(f"Открытый ключ сохранён: {public_path}")

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    write_file(private_path, private_bytes)
    print(f"Закрытый ключ сохранён: {private_path}")


def generate_aes_key(key_size_bits: int) -> bytes:
    """
    Сгенерировать случайный AES-ключ.

    Параметры:
        key_size_bits: размер ключа в битах (128, 192 или 256).

    Возвращает:
        AES-ключ (16/24/32 байта).

    Исключения:
        ValueError: недопустимый размер ключа.
    """
    match key_size_bits:
        case 128 | 192 | 256:
            key_size_bytes = key_size_bits // 8
            key = os.urandom(key_size_bytes)
            print(
                f"Симметричный ключ AES-{key_size_bits} сгенерирован "
                f"({key_size_bytes} байт)"
            )
            return key
        case _:
            raise ValueError(
                f"Некорректная длина ключа AES: {key_size_bits}. "
                f"Допустимые значения: 128, 192, 256."
            )
