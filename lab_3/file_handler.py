"""
Модуль для работы с файлами: чтение, запись, сериализации.

Предоставляет функции для работы с:
- JSON конфигурационными файлами
- PEM ключами RSA
- Бинарными и текстовыми файлами
"""

import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from typing import Union


def read_config(config_path: str) -> dict:
    """
    Загрузка конфигурационных данных из JSON файла.
    
    Args:
        config_path: Путь к JSON файлу конфигурации.
        
    Returns:
        dict: Словарь с конфигурационными данными.
        
    Raises:
        FileNotFoundError: Если файл конфигурации не найден.
        json.JSONDecodeError: Если файл содержит невалидный JSON.
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Конфигурационный файл {config_path} не найден")
    except json.JSONDecodeError as err:
        raise json.JSONDecodeError(f"Ошибка парсинга JSON в файле {config_path}", err.doc, err.pos)
    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла {config_path}")
    except Exception as err:
        raise Exception(f"Неизвестная ошибка при чтении конфигурации: {err}")


def _write_binary_file(file_path: str, data: bytes, operation_description: str) -> None:
    """
    Вспомогательная функция для записи бинарных данных.
    
    Args:
        file_path: Путь к файлу.
        data: Бинарные данные для записи.
        operation_description: Описание операции для сообщения об ошибке.
        
    Raises:
        IOError: Если произошла ошибка записи.
    """
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except FileNotFoundError:
        raise IOError(f"Путь не найден при операции: {operation_description} {file_path}")
    except PermissionError:
        raise IOError(f"Нет прав на запись в файл {file_path}")
    except IsADirectoryError:
        raise IOError(f"Указан каталог вместо файла: {file_path}")
    except OSError as err:
        raise IOError(f"{operation_description} {file_path}: {err}")
    except Exception as err:
        raise IOError(f"Неизвестная ошибка при операции {operation_description} {file_path}: {err}")


def _read_binary_file(file_path: str, operation_description: str) -> bytes:
    """
    Вспомогательная функция для чтения бинарных данных.
    
    Args:
        file_path: Путь к файлу.
        operation_description: Описание операции для сообщения об ошибке.
        
    Returns:
        bytes: Прочитанные бинарные данные.
        
    Raises:
        FileNotFoundError: Если файл не найден.
        IOError: Если произошла ошибка чтения.
    """
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"{operation_description} {file_path} не найден")
    except PermissionError:
        raise IOError(f"Нет прав на чтение файла {file_path}")
    except IsADirectoryError:
        raise IOError(f"Указан каталог вместо файла: {file_path}")
    except OSError as err:
        raise IOError(f"{operation_description} {file_path}: {err}")
    except Exception as err:
        raise IOError(f"Неизвестная ошибка при операции {operation_description} {file_path}: {err}")


def store_asymmetric_keys(pub_path: str, priv_path: str, priv_key_obj, pub_key_obj) -> None:
    """
    Сохранение пары ключей RSA в файлы.
    
    Args:
        pub_path: Путь для сохранения публичного ключа.
        priv_path: Путь для сохранения приватного ключа.
        priv_key_obj: Объект приватного ключа RSA.
        pub_key_obj: Объект публичного ключа RSA.
    """
    try:
        pub_bytes = pub_key_obj.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        _write_binary_file(pub_path, pub_bytes, "Сохранение публичного ключа")
        
        priv_bytes = priv_key_obj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        _write_binary_file(priv_path, priv_bytes, "Сохранение приватного ключа")
        
    except Exception as err:
        raise IOError(f"Ошибка при сохранении RSA ключей: {err}")


def retrieve_rsa_public_key(file_path: str) -> RSAPublicKey:
    """
    Загрузка открытого RSA ключа.
    
    Args:
        file_path: Путь к файлу с публичным ключом.
        
    Returns:
        RSAPublicKey: Объект публичного ключа RSA.
    """
    try:
        public_key_bytes = _read_binary_file(file_path, "Файл открытого ключа")
        return load_pem_public_key(public_key_bytes)
    except Exception as err:
        raise Exception(f"Ошибка загрузки публичного ключа: {err}")


def retrieve_rsa_private_key(file_path: str) -> RSAPrivateKey:
    """
    Загрузка закрытого RSA ключа.
    
    Args:
        file_path: Путь к файлу с приватным ключом.
        
    Returns:
        RSAPrivateKey: Объект приватного ключа RSA.
    """
    try:
        private_key_bytes = _read_binary_file(file_path, "Файл закрытого ключа")
        return load_pem_private_key(private_key_bytes, password=None)
    except Exception as err:
        raise Exception(f"Ошибка загрузки приватного ключа: {err}")


def save_plaintext(content: str, file_path: str) -> None:
    """
    Сохранение текстового содержимого в файл.
    
    Args:
        content: Текстовое содержимое для сохранения.
        file_path: Путь к файлу для записи.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(content)
    except PermissionError:
        raise IOError(f"Нет прав на запись в файл {file_path}")
    except IsADirectoryError:
        raise IOError(f"Указан каталог вместо файла: {file_path}")
    except OSError as err:
        raise IOError(f"Ошибка записи в файл {file_path}: {err}")
    except Exception as err:
        raise IOError(f"Неизвестная ошибка при записи в файл {file_path}: {err}")


def load_plaintext(file_path: str) -> str:
    """
    Чтение текстового файла.
    
    Args:
        file_path: Путь к текстовому файлу.
        
    Returns:
        str: Содержимое файла.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as text_file:
            return text_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Текстовый файл {file_path} не найден")
    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла {file_path}")
    except IsADirectoryError:
        raise IOError(f"Указан каталог вместо файла: {file_path}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Ошибка декодирования файла {file_path}", b"", 0, 1, "utf-8")
    except Exception as err:
        raise IOError(f"Неизвестная ошибка при чтении файла {file_path}: {err}")