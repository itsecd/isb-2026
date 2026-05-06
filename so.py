from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import os
import json


def check_file(path: str) -> None:
    """
    Проверяет существование директории для указанного пути и создает её при необходимости.

    Args:
        path (str): Полный путь к файлу.

    Raises:
        OSError: Если не удалось создать директории.
    """
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
    """
    Сохраняет приватный RSA ключ в файл в формате PEM без пароля.

    Args:
        path (str): Путь для сохранения файла.
        key (rsa.RSAPrivateKey): Объект приватного ключа RSA.

    Raises:
        OSError: Ошибка при записи в файл.
    """
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
    """
    Сохраняет публичный RSA ключ в файл в формате PEM (SubjectPublicKeyInfo).

    Args:
        path (str): Путь для сохранения файла.
        key (rsa.RSAPublicKey): Объект публичного ключа RSA.

    Raises:
        OSError: Ошибка при записи в файл.
    """
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
    """
    Загружает приватный RSA ключ из PEM-файла.

    Args:
        path (str): Путь к файлу приватного ключа.

    Returns:
        rsa.RSAPrivateKey: Объект загруженного приватного ключа.

    Raises:
        OSError: Ошибка при открытии или чтении файла.
    """
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
    """
    Загружает публичный RSA ключ из PEM-файла.

    Args:
        path (str): Путь к файлу публичного ключа.

    Returns:
        rsa.RSAPublicKey: Объект загруженного публичного ключа.

    Raises:
        OSError: Ошибка при открытии или чтении файла.
    """
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
    """
    Считывает всё содержимое файла в бинарном режиме.

    Args:
        path (str): Путь к файлу.

    Returns:
        bytes: Бинарные данные из файла.

    Raises:
        OSError: Ошибка при попытке чтения файла.
    """
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError as e:
        print(f"Ошибка при открытии бинарного файла: {e}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def save_binary(path: str, data: bytes) -> None:
    """
    Записывает бинарные данные в файл.

    Args:
        path (str): Путь к сохраняемому файлу.
        data (bytes): Данные для записи.

    Raises:
        OSError: Ошибка при записи в файл.
    """
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
    """
    Загружает данные из JSON-файла.

    Args:
        path (str): Путь к JSON-файлу.

    Returns:
        dict: Данные, преобразованные в словарь.

    Raises:
        OSError: Ошибка при открытии файла.
        json.JSONDecodeError: Если содержимое файла не является валидным JSON.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except OSError as e:
        print(f"Ошибка при считывании json: {e}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
