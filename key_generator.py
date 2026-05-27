import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from utils import write_file

def generate_rsa_keys(key_size: int = 2048):
    """Сгенерировать пару RSA-ключей."""
    print(f"Генерация RSA-ключей ({key_size} бит).")
    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        print("RSA-ключи сгенерированы")
        return private_key, public_key
    except Exception as e:
        raise RuntimeError(f"Ошибка при генерации RSA-ключей: {e}") from e

def save_rsa_keys(private_key, public_key, private_path: str, public_path: str) -> None:
    """Сохранить RSA-ключи в PEM-файлы."""
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
    """Сгенерировать случайный AES-ключ."""
    match key_size_bits:
        case 128 | 192 | 256:
            key_size_bytes = key_size_bits // 8
            key = os.urandom(key_size_bytes)
            print(f"Симметричный ключ AES-{key_size_bits} сгенерирован ({key_size_bytes} байт)")
            return key
        case _:
            raise ValueError(f"Некорректная длина ключа AES: {key_size_bits}. Допустимые значения: 128, 192, 256.")
