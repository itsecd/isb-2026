import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from exceptions import KeyGenerationError, KeyLoadError, EncryptionError, DecryptionError, FileProcessingError

_SETTINGS_PATH = "settings.json"

def _load_rsa_constants():
    """
    Загружает константы для RSA из файла settings.json.

    :return: Словарь с параметрами RSA (public exponent, key size).
    :raises FileProcessingError: Если файл не найден или содержит некорректный JSON.
    """
    try:
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise FileProcessingError(f"Не удалось загрузить {_SETTINGS_PATH}: {e}") from e

_constants = _load_rsa_constants()

RSA_PUBLIC_EXPONENT = _constants["rsa_public_exponent"]
RSA_KEY_SIZE = _constants["rsa_key_size"]


def generate_rsa_keys():
    """
    Генерирует пару ключей RSA (приватный и публичный).

    :return: Кортеж (private_key, public_key) объектов криптографии.
    :raises KeyGenerationError: При сбое генерации ключей.
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=RSA_PUBLIC_EXPONENT,
            key_size=RSA_KEY_SIZE
        )
        return private_key, private_key.public_key()
    except Exception as error:
        raise KeyGenerationError(f"Ошибка генерации RSA: {error}") from error


def save_private_key(private_key, path: str) -> None:
    """
    Сохраняет приватный ключ RSA в файл в формате PEM (без шифрования паролем).

    :param private_key: Приватный ключ (объект, полученный из generate_rsa_keys).
    :param path: Путь к файлу для сохранения.
    :raises FileProcessingError: При ошибке записи в файл.
    """
    try:
        with open(path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    except Exception as error:
        raise FileProcessingError(f"Ошибка сохранения private key: {error}") from error


def save_public_key(public_key, path: str) -> None:
    """
    Сохраняет публичный ключ RSA в файл в формате PEM.

    :param public_key: Публичный ключ (объект).
    :param path: Путь к файлу для сохранения.
    :raises FileProcessingError: При ошибке записи в файл.
    """
    try:
        with open(path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    except Exception as error:
        raise FileProcessingError(f"Ошибка сохранения public key: {error}") from error


def load_private_key(path: str):
    """
    Загружает приватный ключ RSA из PEM-файла (без пароля).

    :param path: Путь к файлу с приватным ключом.
    :return: Объект приватного ключа.
    :raises KeyLoadError: При ошибке чтения файла или загрузки ключа.
    """
    try:
        with open(path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)
    except Exception as error:
        raise KeyLoadError(f"Ошибка загрузки private key: {error}") from error


def load_public_key(path: str):
    """
    Загружает публичный ключ RSA из PEM-файла.

    :param path: Путь к файлу с публичным ключом.
    :return: Объект публичного ключа.
    :raises KeyLoadError: При ошибке чтения файла или загрузки ключа.
    """
    try:
        with open(path, "rb") as f:
            return serialization.load_pem_public_key(f.read())
    except Exception as error:
        raise KeyLoadError(f"Ошибка загрузки public key: {error}") from error


def encrypt_symmetric_key(key: bytes, public_key) -> bytes:
    """
    Шифрует симметричный ключ с помощью RSA (схема OAEP, хеш SHA-256).

    :param key: Симметричный ключ (байты, например, ключ CAST5).
    :param public_key: Публичный ключ RSA (объект).
    :return: Зашифрованный ключ в виде байтов.
    :raises EncryptionError: При ошибке шифрования.
    """
    try:
        return public_key.encrypt(
            key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as error:
        raise EncryptionError(f"Ошибка шифрования ключа: {error}") from error


def decrypt_symmetric_key(encrypted_key: bytes, private_key) -> bytes:
    """
    Расшифровывает симметричный ключ, зашифрованный функцией encrypt_symmetric_key.

    :param encrypted_key: Зашифрованный ключ (байты).
    :param private_key: Приватный ключ RSA (объект).
    :return: Расшифрованный симметричный ключ (байты).
    :raises DecryptionError: При ошибке расшифрования.
    """
    try:
        return private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as error:
        raise DecryptionError(f"Ошибка дешифрования ключа: {error}") from error