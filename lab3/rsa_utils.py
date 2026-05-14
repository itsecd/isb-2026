'''Модуль асимметричного шифрования RSA.'''

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def load_private_key(path: str):
    '''Загружает закрытый ключ RSA из PEM-файла.

    Args:
        path (str): Путь к PEM-файлу.

    Returns:
        RSAPrivateKey: Закрытый ключ RSA.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если файл имеет неверный формат.
    '''
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def load_public_key(path: str):
    '''Загружает открытый ключ RSA из PEM-файла.

    Args:
        path (str): Путь к PEM-файлу.

    Returns:
        RSAPublicKey: Открытый ключ RSA.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если файл имеет неверный формат.
    '''
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def encrypt_key(symmetric_key: bytes, public_key) -> bytes:
    '''Шифрует симметричный ключ открытым ключом RSA.

    Используется схема OAEP с хеш-функцией SHA-256 и MGF1.

    Args:
        symmetric_key (bytes): Симметричный ключ.
        public_key (RSAPublicKey): Открытый ключ RSA.

    Returns:
        bytes: Зашифрованный симметричный ключ.
    '''
    return public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_key(encrypted_key: bytes, private_key) -> bytes:
    '''Расшифровывает симметричный ключ закрытым ключом RSA.

    Используется схема OAEP с хеш-функцией SHA-256 и MGF1.

    Args:
        encrypted_key (bytes): Зашифрованный симметричный ключ.
        private_key (RSAPrivateKey): Закрытый ключ RSA.

    Returns:
        bytes: Расшифрованный симметричный ключ.
    '''
    return private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )