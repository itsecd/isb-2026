import os
import sys

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_keys():
    print("Генерация RSA-ключей (2048 бит).")
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        print("RSA-ключи сгенерированы")
        return private_key, public_key
    except Exception as e:
        print(f"Ошибка при генерации RSA-ключей: {e}")
        sys.exit(1)


def save_rsa_keys(private_key, public_key, private_path, public_path):
    try:
        with open(public_path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        print(f"Открытый ключ сохранён: {public_path}")
    except Exception as e:
        print(f"Ошибка при сохранении открытого ключа: {e}")
        sys.exit(1)

    try:
        with open(private_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        print(f"Закрытый ключ сохранён: {private_path}")
    except Exception as e:
        print(f"Ошибка при сохранении закрытого ключа: {e}")
        sys.exit(1)


def generate_aes_key(key_size_bits):
    if key_size_bits not in (128, 192, 256):
        raise ValueError(
            f"Некорректная длина ключа AES: {key_size_bits}. "
            f"Допустимые значения: 128, 192, 256."
        )
    key_size_bytes = key_size_bits // 8
    key = os.urandom(key_size_bytes)
    print(
        f"Симметричный ключ AES-{key_size_bits} сгенерирован "
        f"({key_size_bytes} байт)"
    )
    return key