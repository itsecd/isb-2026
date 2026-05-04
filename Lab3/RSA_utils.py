import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from typing import Tuple


def generate_keys(key_size: int, public_exponent: int) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Генерирует пару ключей RSA."""
    try:
        private_key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size
        )
        public_key = private_key.public_key()
        return private_key, public_key
    except ValueError as e:
        raise ValueError(f"Ошибка параметров RSA: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Не удалось сгенерировать ключи RSA: {e}") from e


def encrypt_with_public_key(data: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """Шифрует данные с использованием публичного ключа RSA."""
    try:
        encrypted_data = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_data
    except ValueError as e:
        raise ValueError(f"Ошибка шифрования RSA: {e}") from e
    except TypeError as e:
        raise TypeError(f"Неверный тип публичного ключа: {e}") from e
    except (InvalidSignature, UnsupportedAlgorithm) as e:
        raise RuntimeError(f"Криптографическая ошибка при шифровании: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Неожиданная ошибка при шифровании RSA: {e}") from e


def decrypt_with_private_key(encrypted_data: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    """Расшифровывает данные с использованием приватного ключа RSA."""
    try:
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data
    except ValueError as e:
        raise ValueError(f"Ошибка дешифрования RSA: {e}") from e
    except TypeError as e:
        raise TypeError(f"Неверный тип приватного ключа: {e}") from e
    except (InvalidSignature, UnsupportedAlgorithm) as e:
        raise RuntimeError(f"Криптографическая ошибка при дешифровании: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Неожиданная ошибка при дешифровании RSA: {e}") from e


def serialize_public_key(public_key: rsa.RSAPublicKey, file_path: str) -> None:
    """Сохраняет публичный ключ в PEM-файл."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        pem_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        _write_binary_file(file_path, pem_key)
    except OSError as e:
        raise OSError(f"Не удалось сохранить публичный ключ: {e}") from e
    except TypeError as e:
        raise TypeError(f"Неверный тип публичного ключа: {e}") from e


def serialize_private_key(private_key: rsa.RSAPrivateKey, file_path: str) -> None:
    """Сохраняет приватный ключ в PEM-файл."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        _write_binary_file(file_path, pem_key)
    except OSError as e:
        raise OSError(f"Не удалось сохранить приватный ключ: {e}") from e
    except TypeError as e:
        raise TypeError(f"Неверный тип приватного ключа: {e}") from e


def load_public_key(file_path: str) -> rsa.RSAPublicKey:
    """Загружает публичный ключ из PEM-файла."""
    try:
        pem_data = _read_binary_file(file_path)
        public_key = load_pem_public_key(pem_data)
        return public_key
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл публичного ключа не найден: {file_path}") from e
    except ValueError as e:
        raise ValueError(f"Ошибка при загрузке PEM-ключа: {e}") from e


def load_private_key(file_path: str) -> rsa.RSAPrivateKey:
    """Загружает приватный ключ из PEM-файла."""
    try:
        pem_data = _read_binary_file(file_path)
        private_key = load_pem_private_key(pem_data, password=None)
        return private_key
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл приватного ключа не найден: {file_path}") from e
    except ValueError as e:
        raise ValueError(f"Ошибка при загрузке приватного ключа: {e}") from e


def _write_binary_file(file_path: str, data: bytes) -> None:
    """Внутренняя функция для записи бинарных данных."""
    try:
        with open(file_path, "wb") as f:
            f.write(data)
    except OSError as e:
        raise OSError(f"Ошибка записи в файл {file_path}: {e}") from e


def _read_binary_file(file_path: str) -> bytes:
    """Внутренняя функция для чтения бинарных данных."""
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл не найден: {file_path}") from e
    except OSError as e:
        raise OSError(f"Ошибка чтения файла {file_path}: {e}") from e