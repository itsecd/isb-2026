from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

RSA_KEY_SIZE = 2048


def generate_keys(key_size=RSA_KEY_SIZE):
    """Генерирует пару RSA-ключей (закрытый и открытый)."""
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def load_private_key(key_data):
    """Загружает закрытый RSA ключ из байтовых данных."""
    if not key_data:
        raise ValueError("Нет данных для загрузки ключа")
    return RSA.import_key(key_data)


def load_public_key(key_data):
    """Загружает открытый RSA ключ из байтовых данных."""
    if not key_data:
        raise ValueError("Нет данных для загрузки ключа")
    return RSA.import_key(key_data)


def encrypt_with_public_key(data, public_key_pem):
    """Шифрует данные открытым ключом RSA (OAEP)."""
    if not data:
        raise ValueError("Нет данных для шифрования")
    if not public_key_pem:
        raise ValueError("Нет открытого ключа")
    
    public_key = load_public_key(public_key_pem)
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)


def decrypt_with_private_key(encrypted_data, private_key_pem):
    """Расшифровывает данные закрытым ключом RSA."""
    if not encrypted_data:
        raise ValueError("Нет данных для расшифрования")
    if not private_key_pem:
        raise ValueError("Нет закрытого ключа")
    
    private_key = load_private_key(private_key_pem)
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_data)