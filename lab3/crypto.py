import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.decrepit.ciphers.algorithms import SEED
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes


SEED_BLOCK_SIZE = 128
SEED_KEY_SIZE = 16
IV_SIZE = 16


RSA_KEY_SIZE = 2048
RSA_EXPONENT = 65537




def generate_symmetric_key() -> bytes:
    """Генерирует случайный ключ SEED (128 бит)."""
    print("Генерация ключа SEED (128 бит)")
    return os.urandom(SEED_KEY_SIZE)


def generate_iv() -> bytes:
    """Генерирует случайный вектор инициализации."""
    return os.urandom(IV_SIZE)


def pad_data(data: bytes) -> bytes:
    """Дополняет данные до размера, кратного блоку SEED."""
    padder = padding.ANSIX923(SEED_BLOCK_SIZE).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(padded_data: bytes) -> bytes:
    """Удаляет дополнение."""
    unpadder = padding.ANSIX923(SEED_BLOCK_SIZE).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()


def seed_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    """Шифрует данные алгоритмом SEED в режиме CBC."""
    try:
        cipher = Cipher(SEED(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()
    except Exception as e:
        raise RuntimeError(f"Ошибка шифрования SEED: {e}")


def seed_decrypt(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    """Расшифровывает данные алгоритмом SEED в режиме CBC."""
    try:
        cipher = Cipher(SEED(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted_data) + decryptor.finalize()
    except Exception as e:
        raise RuntimeError(f"Ошибка расшифрования SEED: {e}")



def generate_rsa_keys() -> tuple:
    """Генерирует пару ключей RSA (приватный, публичный)."""
    print(f"Генерация RSA-ключей ({RSA_KEY_SIZE} бит)...")
    try:
        private_key = rsa.generate_private_key(
            public_exponent=RSA_EXPONENT,
            key_size=RSA_KEY_SIZE
        )
        public_key = private_key.public_key()
        print("RSA-ключи сгенерированы")
        return private_key, public_key
    except Exception as e:
        raise RuntimeError(f"Ошибка генерации RSA: {e}")


def serialize_private_key(private_key) -> bytes:
    """Сериализует приватный ключ в PEM-формат."""
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )


def serialize_public_key(public_key) -> bytes:
    """Сериализует публичный ключ в PEM-формат."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def deserialize_private_key(key_bytes: bytes):
    """Восстанавливает приватный ключ из PEM-байтов."""
    try:
        return serialization.load_pem_private_key(key_bytes, password=None)
    except Exception as e:
        raise ValueError(f"Ошибка загрузки приватного ключа: {e}")


def rsa_encrypt_key(symmetric_key: bytes, public_key) -> bytes:
    """Шифрует симметричный ключ открытым RSA-ключом."""
    print("Шифрование симметричного ключа с помощью RSA")
    try:
        encrypted = public_key.encrypt(
            symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Ключ зашифрован")
        return encrypted
    except Exception as e:
        raise RuntimeError(f"Ошибка шифрования ключа RSA: {e}")


def rsa_decrypt_key(encrypted_key: bytes, private_key) -> bytes:
    """Расшифровывает симметричный ключ закрытым RSA-ключом."""
    print("Расшифрование симметричного ключа с помощью RSA")
    try:
        decrypted = private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Ключ расшифрован")
        return decrypted
    except Exception as e:
        raise RuntimeError(f"Ошибка расшифрования ключа RSA: {e}")