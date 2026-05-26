import os
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


def check_file(target_path: str) -> None:
    """
    Гарантирует наличие родительской директории для указанного пути.
    Создаёт цепочку каталогов, если они отсутствуют.

    """
    directory = os.path.dirname(target_path)
    if directory:
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as exc:
            print(f"Критическая ошибка создания каталога: {exc}")
            raise


def save_private_key(destination: str, private_key: rsa.RSAPrivateKey) -> None:
    """
    Экспортирует приватный RSA-ключ в PEM-формат без парольной защиты.

    """
    check_file(destination)
    try:
        pem_payload = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(destination, "wb") as stream:
            stream.write(pem_payload)
    except OSError as exc:
        print(f"Не удалось сохранить приватный ключ: {exc}")
        raise


def save_public_key(destination: str, public_key: rsa.RSAPublicKey) -> None:
    """
    Экспортирует публичный RSA-ключ в PEM-формат (SubjectPublicKeyInfo).

    """
    check_file(destination)
    try:
        pem_payload = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(destination, "wb") as stream:
            stream.write(pem_payload)
    except OSError as exc:
        print(f"Не удалось сохранить публичный ключ: {exc}")
        raise


def open_private_key(source: str) -> rsa.RSAPrivateKey:
    """
    Импортирует приватный RSA-ключ из PEM-файла.

    """
    try:
        with open(source, "rb") as stream:
            raw_data = stream.read()
            return load_pem_private_key(raw_data, password=None)
    except OSError as exc:
        print(f"Ошибка чтения файла приватного ключа: {exc}")
        raise
    except Exception as exc:
        print(f"Непредвиденная ошибка десериализации ключа: {exc}")
        raise


def open_public_key(source: str) -> rsa.RSAPublicKey:
    """
    Импортирует публичный RSA-ключ из PEM-файла.

    """
    try:
        with open(source, "rb") as stream:
            raw_data = stream.read()
            return load_pem_public_key(raw_data)
    except OSError as exc:
        print(f"Ошибка чтения файла публичного ключа: {exc}")
        raise
    except Exception as exc:
        print(f"Непредвиденная ошибка десериализации ключа: {exc}")
        raise


def open_binary(source: str) -> bytes:
    """
    Считывает полное содержимое файла в бинарном режиме.

    """
    try:
        with open(source, "rb") as stream:
            return stream.read()
    except OSError as exc:
        print(f"Ошибка открытия бинарного файла: {exc}")
        raise


def save_binary(destination: str, payload: bytes) -> None:
    """
    Записывает бинарные данные в файл, создавая необходимые директории.

    """
    check_file(destination)
    try:
        with open(destination, "wb") as stream:
            stream.write(payload)
    except OSError as exc:
        print(f"Ошибка записи бинарных данных: {exc}")
        raise


def open_json(source: str) -> dict:
    """
    Десериализует содержимое JSON-файла в словарь Python.

    """
    try:
        with open(source, "r", encoding="utf-8") as stream:
            return json.load(stream)
    except OSError as exc:
        print(f"Ошибка доступа к JSON-файлу: {exc}")
        raise
    except json.JSONDecodeError as exc:
        print(f"Формат JSON нарушен: {exc}")
        raise