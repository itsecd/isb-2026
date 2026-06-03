import argparse
import json
import os
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
    if not file_path:
        print("Error: file path is empty")
        return b''
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: file not found - {file_path}")
        return b''
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return b''


def write_txt_file(data: bytes, file_path: str) -> None:
    """
    Записывает байтовые данные в файл (бинарный режим).

    Args:
        data (bytes): данные для записи.
        file_path (str): путь к файлу.

    Raises:
        ValueError: если data пустое или file_path не указан.
    """
    if not file_path:
        raise ValueError("File path is empty")
    if not data:
        raise ValueError("No data to write")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")


def serialize_private_key(private_pem: str, private_key) -> None:
    """
    Сохраняет приватный RSA-ключ в формате PEM (без шифрования).

    Args:
        private_pem (str): путь для сохранения.
        private_key: объект приватного ключа.

    Raises:
        ValueError: если private_key None или private_pem пуст.
    """
    if not private_pem:
        raise ValueError("Private key path is empty")
    if private_key is None:
        raise ValueError("Private key is None")
    os.makedirs(os.path.dirname(private_pem), exist_ok=True)
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

    Raises:
        ValueError: если public_key None или public_pem пуст.
    """
    if not public_pem:
        raise ValueError("Public key path is empty")
    if public_key is None:
        raise ValueError("Public key is None")
    os.makedirs(os.path.dirname(public_pem), exist_ok=True)
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
        public_key: загруженный ключ или None при ошибке.
    """
    if not public_pem:
        print("Error: public key path is empty")
        return None
    if not os.path.exists(public_pem):
        print(f"Error: public key file not found - {public_pem}")
        return None
    try:
        with open(public_pem, 'rb') as pem_in:
            public_bytes = pem_in.read()
        return load_pem_public_key(public_bytes)
    except Exception as e:
        print(f"Error loading public key from {public_pem}: {e}")
        return None


def deserialize_private_key(private_pem: str):
    """
    Загружает приватный RSA-ключ из PEM-файла (без пароля).

    Args:
        private_pem (str): путь к файлу.

    Returns:
        private_key: загруженный ключ или None при ошибке.
    """
    if not private_pem:
        print("Error: private key path is empty")
        return None
    if not os.path.exists(private_pem):
        print(f"Error: private key file not found - {private_pem}")
        return None
    try:
        with open(private_pem, 'rb') as pem_in:
            private_bytes = pem_in.read()
        return load_pem_private_key(private_bytes, password=None)
    except Exception as e:
        print(f"Error loading private key from {private_pem}: {e}")
        return None


def read_json(file_name: str) -> dict:
    """
    Чтение файла настроек JSON.

    Args:
        file_name (str): путь к JSON-файлу.

    Returns:
        dict: словарь с путями из конфигурации или пустой словарь при ошибке.
    """
    if not file_name:
        print("Error: JSON file name is empty")
        return {}
    if not os.path.exists(file_name):
        print(f"Error: JSON file not found - {file_name}")
        return {}
    try:
        with open(file_name, 'r', encoding='utf-8') as json_file:
            paths = json.load(json_file)
            print("Пути к файлам считаны из", file_name)
            return paths
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {file_name}: {e}")
        return {}
    except Exception as e:
        print(f"Error reading JSON file {file_name}: {e}")
        return {}
