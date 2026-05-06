from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import os
import json


def check_file(path: str) -> None:
    """Проверяет путь к файлу и создает необходимые директории, если они не существуют.
    путь к файлу"""
    folder = os.path.dirname(path)
    if folder:
        try:
            os.makedirs(folder, exist_ok=True)
        except OSError as e:
            print(f"Ошибка при создании директории: {e}")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


def save_private_key(path: str, key: rsa.RSAPrivateKey) -> None:
    """Сохраняет приватный RSA ключ в PEM-формате.
    путь к файлу для сохранения, приватный ключ"""
    try:
        check_file(path)
        with open(path, 'wb') as file:
            file.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    except OSError as e:
        print(f"Ошибка при сохранении приватного ключа: {e}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def save_public_key(path: str, key: rsa.RSAPublicKey) -> None:
    """Сохраняет публичный RSA ключ в PEM-формате.
    путь к файлу для публичного ключа, публичный ключ"""
    try:
        check_file(path)
        with open(path, "wb") as file:
            file.write(key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    except OSError as e:
        print(f"Ошибка при сохранении публичного ключа: {e}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def open_private_key(path: str) -> rsa.RSAPrivateKey:
    """Загружает приватный RSA ключ из файла.
    путь к приватному ключу"""
    try:
        with open(path, "rb") as f:
            private_bytes = f.read()
            return load_pem_private_key(private_bytes, password=None)
    except OSError as e:
        print(f"Ошибка при чтении приватного ключа: {e}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def open_public_key(path: str) -> rsa.RSAPublicKey:
    """Загружает публичный RSA ключ из файла.
    путь к публичному ключу"""
    try:
        with open(path, "rb") as f:
            public_bytes = f.read()
            return load_pem_public_key(public_bytes)
    except OSError as e:
        print(f"Ошибка при чтении публичного ключа: {e}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def open_binary(path: str) -> bytes:
    """Считывает данные из бинарного файла.
    путь к файлу"""
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError as e:
        print(f"Ошибка при открытии бинарного файла: {e}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def save_binary(path: str, data: bytes) -> None:
    """Записывает байты в бинарный файл.
    путь к файлу, данные"""
    try:
        check_file(path)
        with open(path, "wb") as f:
            f.write(data)
    except OSError as e:
        print(f"Ошибка при записи бинарного файла: {e}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def open_json(path: str) -> dict:
    """Считывание конфигурации из JSON-файла.
    путь к файлу json"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except OSError as e:
        print(f"Ошибка при считывание json: {e}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
