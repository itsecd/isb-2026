'''Модуль генерации и сохранения ключей для гибридной криптосистемы RSA + 3DES.'''

import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import des3_utils


def generate_symmetric_key(key_size: int = 192) -> bytes:
    '''Генерирует случайный ключ алгоритма 3DES.

    Args:
        key_size (int): Размер ключа в битах (64, 128 или 192).

    Returns:
        bytes: Случайный ключ 3DES.

    Raises:
        ValueError: Если key_size не равен 64, 128 или 192.
    '''
    if key_size not in (64, 128, 192):
        raise ValueError(f"Недопустимый размер ключа: {key_size}")
    return des3_utils.generate_key(key_size)


def generate_asymmetric_keys() -> tuple:
    '''Генерирует пару ключей алгоритма RSA.

    Длина ключа: 2048 бит.
    Открытая экспонента: 65537.

    Returns:
        tuple: Кортеж (закрытый_ключ: RSAPrivateKey, открытый_ключ: RSAPublicKey).

    Raises:
        Exception: Если не удалось сгенерировать ключи.
    '''
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key
    except Exception as e:
        raise Exception(f"Ошибка генерации ключей RSA: {e}")


def save_private_key(private_key, path: str) -> None:
    '''Сохраняет закрытый ключ RSA в PEM-файл.

    Папка создаётся автоматически, если её не существует.
    Ключ сохраняется без пароля (NoEncryption).

    Args:
        private_key (RSAPrivateKey): Закрытый ключ RSA.
        path (str): Путь для сохранения.

    Raises:
        OSError: Если не удалось создать папку или записать файл.
    '''
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    except OSError as e:
        raise OSError(f"Ошибка сохранения закрытого ключа: {e}")


def save_public_key(public_key, path: str) -> None:
    '''Сохраняет открытый ключ RSA в PEM-файл.

    Папка создаётся автоматически, если её не существует.

    Args:
        public_key (RSAPublicKey): Открытый ключ RSA.
        path (str): Путь для сохранения.

    Raises:
        OSError: Если не удалось создать папку или записать файл.
    '''
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    except OSError as e:
        raise OSError(f"Ошибка сохранения открытого ключа: {e}")


def save_encrypted_symmetric_key(encrypted_key: bytes, path: str) -> None:
    '''Сохраняет зашифрованный симметричный ключ в файл.

    Папка создаётся автоматически, если её не существует.

    Args:
        encrypted_key (bytes): Зашифрованный симметричный ключ.
        path (str): Путь для сохранения.

    Raises:
        OSError: Если не удалось создать папку или записать файл.
    '''
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "wb") as f:
            f.write(encrypted_key)
    except OSError as e:
        raise OSError(f"Ошибка сохранения зашифрованного ключа: {e}")