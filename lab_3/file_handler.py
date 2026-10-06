import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey,
)
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def load_config(file_path: str) -> dict:
    """
    Читает JSON-файл конфигурации.

    :param file_path: путь к JSON-файлу
    :return: словарь с настройками
    """

    try:
        with open(file_path, "r", encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Файл конфигурации {file_path} не найден"
        ) from err
    except PermissionError as err:
        raise PermissionError(
            f"Нет прав на чтение файла {file_path}"
        ) from err
    except json.JSONDecodeError as err:
        raise ValueError(
            f"Файл конфигурации {file_path} повреждён: {err}"
        ) from err
    except OSError as err:
        raise OSError(
            f"Не удалось прочитать {file_path}: {err}"
        ) from err


def read_binary_file(file_path: str) -> bytes:
    """
    Читает файл в бинарном режиме.

    :param file_path: путь к файлу
    :return: содержимое файла в виде байтов
    """

    try:
        with open(file_path, "rb") as bin_file:
            return bin_file.read()
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Бинарный файл {file_path} не найден"
        ) from err
    except PermissionError as err:
        raise PermissionError(
            f"Нет прав на чтение файла {file_path}"
        ) from err
    except OSError as err:
        raise OSError(
            f"Не удалось прочитать {file_path}: {err}"
        ) from err


def write_binary_file(file_path: str, data: bytes) -> None:
    """
    Записывает данные в бинарный файл.

    :param file_path: путь к файлу
    :param data: данные для записи
    """

    try:
        with open(file_path, "wb") as bin_file:
            bin_file.write(data)
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Каталог для {file_path} не найден"
        ) from err
    except PermissionError as err:
        raise PermissionError(
            f"Нет прав на запись в файл {file_path}"
        ) from err
    except OSError as err:
        raise OSError(
            f"Не удалось записать {file_path}: {err}"
        ) from err


def load_private_key(file_path: str) -> RSAPrivateKey:
    """
    Загружает закрытый RSA-ключ из PEM-файла.

    :param file_path: путь к PEM-файлу с закрытым ключом
    :return: объект закрытого RSA-ключа
    """

    private_bytes = read_binary_file(file_path)
    try:
        return load_pem_private_key(private_bytes, password=None)
    except ValueError as err:
        raise ValueError(
            f"Закрытый ключ {file_path} повреждён: {err}"
        ) from err


def save_public_key(file_path: str, public_key: RSAPublicKey) -> None:
    """
    Сериализует открытый RSA-ключ в PEM и сохраняет на диск.

    :param file_path: путь для сохранения ключа
    :param public_key: открытый RSA-ключ
    """

    key_data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    write_binary_file(file_path, key_data)


def save_private_key(file_path: str, private_key: RSAPrivateKey) -> None:
    """
    Сериализует закрытый RSA-ключ в PEM и сохраняет на диск.

    :param file_path: путь для сохранения ключа
    :param private_key: закрытый RSA-ключ
    """

    key_data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    write_binary_file(file_path, key_data)