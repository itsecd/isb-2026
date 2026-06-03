import argparse
import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


def parse_arguments() -> str:
    """
    Парсинг аргументов из командной строки.

    Returns:
        str: путь к файлу настроек (по умолчанию 'settings.json').
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--settings", default="settings.json", type=str, help="settings file path")
    args = parser.parse_args()
    return args.settings


def read_txt_file(file_path: str) -> bytes:
    """
    Читает файл в бинарном режиме.

    Args:
        file_path (str): путь к файлу.

    Returns:
        bytes: содержимое файла или b'' при ошибке.
    """
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except Exception as e:
        print(f"Error: {e}")
        return b''


def write_pem_file(file_path: str, data) -> None:
    """
    Записывает бинарные данные в PEM-файл.

    Args:
        file_path (str): путь для сохранения.
        data (bytes): данные для записи.
    """
    with open(file_path, 'wb') as file:
        file.write(data)


def write_txt_file(data: bytes, file_path: str) -> None:
    """
    Записывает байтовые данные в файл (бинарный режим).

    Args:
        data (bytes): данные для записи.
        file_path (str): путь к файлу.
    """
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f"Error: {e}")


def serialize_private_key(private_pem: str, private_key) -> None:
    """
    Сохраняет приватный RSA-ключ в формате PEM (без шифрования).

    Args:
        private_pem (str): путь для сохранения.
        private_key: объект приватного ключа.
    """
    with open(private_pem, 'wb') as private_out:
        private_out.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()))


def serialize_public_key(public_pem: str, public_key) -> None:
    """
    Сохраняет публичный RSA-ключ в формате PEM.

    Args:
        public_pem (str): путь для сохранения.
        public_key: объект публичного ключа.
    """
    with open(public_pem, 'wb') as public_out:
        public_out.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo))


def deserialize_public_key(public_pem: str):
    """
    Загружает публичный RSA-ключ из PEM-файла.

    Args:
        public_pem (str): путь к файлу.

    Returns:
        public_key: загруженный ключ.
    """
    with open(public_pem, 'rb') as pem_in:
        public_bytes = pem_in.read()
    d_public_key = load_pem_public_key(public_bytes)
    return d_public_key


def deserialize_private_key(private_pem: str):
    """
    Загружает приватный RSA-ключ из PEM-файла (без пароля).

    Args:
        private_pem (str): путь к файлу.

    Returns:
        private_key: загруженный ключ.
    """
    with open(private_pem, 'rb') as pem_in:
        private_bytes = pem_in.read()
    d_private_key = load_pem_private_key(private_bytes, password=None)
    return d_private_key


def read_json(file_name: str) -> dict[str: str]:
    """
    Чтение файла настроек JSON.

    Args:
        file_name (str): путь к JSON-файлу.

    Returns:
        dict: словарь с путями из конфигурации.
    """
    with open(file_name) as json_file:
        paths = json.load(json_file)
        print("Пути к файлам считаны из", file_name)
    return paths
