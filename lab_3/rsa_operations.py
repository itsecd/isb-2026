from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Стандартный размер RSA ключа (2048 бит)
RSA_KEY_SIZE = 2048


def generate_keys(key_size: int = RSA_KEY_SIZE) -> tuple:
    """
    Генерирует пару RSA-ключей (закрытый и открытый).

    Args:
        key_size (int): Размер ключа в битах. По умолчанию 2048.

    Returns:
        tuple: (закрытый_ключ_pem, открытый_ключ_pem) в формате PEM.
    """
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def load_private_key(key_data: bytes) -> object:
    """
    Загружает закрытый RSA ключ из байтовых данных.

    Args:
        key_data (bytes): Байтовые данные ключа в формате PEM.

    Returns:
        object: Объект RSA ключа для использования в шифровании/расшифровании.
    """
    if not key_data:
        raise ValueError("Нет данных для загрузки ключа")
    return RSA.import_key(key_data)


def load_public_key(key_data: bytes) -> object:
    """
    Загружает открытый RSA ключ из байтовых данных.

    Args:
        key_data (bytes): Байтовые данные ключа в формате PEM.

    Returns:
        object: Объект RSA ключа для использования в шифровании/расшифровании.
    """
    if not key_data:
        raise ValueError("Нет данных для загрузки ключа")
    return RSA.import_key(key_data)


def encrypt_with_public_key(data: bytes, public_key_pem: bytes) -> bytes:
    """
    Шифрует данные открытым ключом RSA с использованием OAEP.

    Args:
        data (bytes): Данные для шифрования.
        public_key_pem (bytes): Открытый ключ в формате PEM.

    Returns:
        bytes: Зашифрованные данные.
    """
    if not data:
        raise ValueError("Нет данных для шифрования")
    if not public_key_pem:
        raise ValueError("Нет открытого ключа")

    public_key = load_public_key(public_key_pem)
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)


def decrypt_with_private_key(encrypted_data: bytes, private_key_pem: bytes) -> bytes:
    """
    Расшифровывает данные закрытым ключом RSA.

    Args:
        encrypted_data (bytes): Зашифрованные данные.
        private_key_pem (bytes): Закрытый ключ в формате PEM.

    Returns:
        bytes: Расшифрованные данные.
    """
    if not encrypted_data:
        raise ValueError("Нет данных для расшифрования")
    if not private_key_pem:
        raise ValueError("Нет закрытого ключа")

    private_key = load_private_key(private_key_pem)
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_data)