from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from constants import RSA_KEY_SIZE


def generate_rsa_keys(key_size: int = RSA_KEY_SIZE) -> tuple:
    """
    Генерирует пару RSA-ключей.

    Args:
        key_size: Размер ключа в битах (по умолчанию из констант).

    Returns:
        tuple: (закрытый_ключ_pem, открытый_ключ_pem)
    """
    key = RSA.generate(key_size)
    return key.export_key(), key.publickey().export_key()


def load_rsa_private_key(key_data: bytes) -> object:
    """
    Загружает закрытый RSA ключ из байтовых данных.

    Args:
        key_data: Байтовые данные ключа в формате PEM.

    Returns:
        object: Объект RSA ключа.
    """
    if not key_data:
        raise ValueError("Нет данных для загрузки ключа")
    return RSA.import_key(key_data)


def load_rsa_public_key(key_data: bytes) -> object:
    """
    Загружает открытый RSA ключ из байтовых данных.

    Args:
        key_data: Байтовые данные ключа в формате PEM.

    Returns:
        object: Объект RSA ключа.
    """
    if not key_data:
        raise ValueError("Нет данных для загрузки ключа")
    return RSA.import_key(key_data)


def encrypt_with_rsa_public_key(data: bytes, public_key_pem: bytes) -> bytes:
    """
    Шифрует данные открытым ключом RSA (OAEP).

    Args:
        data: Данные для шифрования.
        public_key_pem: Открытый ключ в формате PEM.

    Returns:
        bytes: Зашифрованные данные.
    """
    if not data:
        raise ValueError("Нет данных для шифрования")
    if not public_key_pem:
        raise ValueError("Нет открытого ключа")

    pub_key = load_rsa_public_key(public_key_pem)
    return PKCS1_OAEP.new(pub_key).encrypt(data)


def decrypt_with_rsa_private_key(encrypted_data: bytes, private_key_pem: bytes) -> bytes:
    """
    Расшифровывает данные закрытым ключом RSA.

    Args:
        encrypted_data: Зашифрованные данные.
        private_key_pem: Закрытый ключ в формате PEM.

    Returns:
        bytes: Расшифрованные данные.
    """
    if not encrypted_data:
        raise ValueError("Нет данных для расшифрования")
    if not private_key_pem:
        raise ValueError("Нет закрытого ключа")

    priv_key = load_rsa_private_key(private_key_pem)
    return PKCS1_OAEP.new(priv_key).decrypt(encrypted_data)