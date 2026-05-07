import json
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)
from file_utils import save_bytes, load_bytes


with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
    _cfg = json.load(f)

RSA_KEY_SIZE = _cfg["rsa_key_size"]
RSA_PUBLIC_EXPONENT = _cfg["rsa_public_exponent"]


def generate_rsa_keys():
    """
    Генерирует пару RSA-ключей.

    :return: (private_key, public_key)
    :raises Exception: если не удалось сгенерировать ключи
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=RSA_PUBLIC_EXPONENT,
            key_size=RSA_KEY_SIZE,
        )
        public_key = private_key.public_key()
        print(f"[OK] Пара RSA-ключей ({RSA_KEY_SIZE} бит) сгенерирована")
        return private_key, public_key
    except Exception as e:
        print(f"[ОШИБКА] Не удалось сгенерировать RSA-ключи: {e}")
        raise


def serialize_public_key(public_key, path: str) -> None:
    """
    Сохраняет открытый RSA-ключ в PEM-формате.

    :param public_key: объект открытого ключа
    :param path: путь для сохранения
    :raises Exception: если не удалось сохранить ключ
    """
    try:
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        save_bytes(pem, path)
        print(f"[OK] Открытый RSA-ключ сохранён: {path}")
    except Exception as e:
        print(f"[ОШИБКА] Не удалось сохранить открытый ключ: {e}")
        raise


def serialize_private_key(private_key, path: str) -> None:
    """
    Сохраняет закрытый RSA-ключ в PEM-формате (без шифрования).

    :param private_key: объект закрытого ключа
    :param path: путь для сохранения
    :raises Exception: если не удалось сохранить ключ
    """
    try:
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        save_bytes(pem, path)
        print(f"[OK] Закрытый RSA-ключ сохранён: {path}")
    except Exception as e:
        print(f"[ОШИБКА] Не удалось сохранить закрытый ключ: {e}")
        raise


def load_public_key(path: str):
    """
    Загружает открытый RSA-ключ из PEM-файла.

    :param path: путь к файлу
    :return: объект открытого ключа
    :raises Exception: если не удалось загрузить ключ
    """
    try:
        pem = load_bytes(path)
        key = load_pem_public_key(pem)
        print(f"[OK] Открытый RSA-ключ загружен: {path}")
        return key
    except Exception as e:
        print(f"[ОШИБКА] Не удалось загрузить открытый ключ из {path}: {e}")
        raise


def load_private_key(path: str):
    """
    Загружает закрытый RSA-ключ из PEM-файла.

    :param path: путь к файлу
    :return: объект закрытого ключа
    :raises Exception: если не удалось загрузить ключ
    """
    try:
        pem = load_bytes(path)
        key = load_pem_private_key(pem, password=None)
        print(f"[OK] Закрытый RSA-ключ загружен: {path}")
        return key
    except Exception as e:
        print(f"[ОШИБКА] Не удалось загрузить закрытый ключ из {path}: {e}")
        raise


def rsa_encrypt(data: bytes, public_key) -> bytes:
    """
    Шифрует данные открытым RSA-ключом (OAEP).

    :param data: данные для шифрования
    :param public_key: открытый RSA-ключ
    :return: зашифрованные данные
    :raises Exception: если не удалось зашифровать
    """
    try:
        ciphertext = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        print("[OK] Данные зашифрованы RSA (OAEP)")
        return ciphertext
    except Exception as e:
        print(f"[ОШИБКА] Не удалось зашифровать данные RSA: {e}")
        raise


def rsa_decrypt(data: bytes, private_key) -> bytes:
    """
    Дешифрует данные закрытым RSA-ключом.

    :param data: зашифрованные данные
    :param private_key: закрытый RSA-ключ
    :return: расшифрованные данные
    :raises Exception: если не удалось расшифровать
    """
    try:
        plaintext = private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        print("[OK] Данные расшифрованы RSA (OAEP)")
        return plaintext
    except Exception as e:
        print(f"[ОШИБКА] Не удалось расшифровать данные RSA: {e}")
        raise