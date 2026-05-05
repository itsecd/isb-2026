from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def generate_rsa_keys():
    """
    Генерация пары RSA-ключей.

    Returns:
        Кортеж (RSAPrivateKey, RSAPublicKey).
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()


def serialize_private_rsa_key(private_key, path):
    """
    Сериализация (сохранение) приватного RSA-ключа в файл.

    Args:
        private_key: Объект приватного ключа RSA.
        path: Путь к файлу для записи.

    Raises:
        RuntimeError: Ошибка при сериализации ключа.
    """
    try:
        with open(path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    except Exception as e:
        raise RuntimeError(f"RSA serialize error: {e}")


def serialize_public_rsa_key(public_key, path):
    """
    Сериализация (сохранение) публичного RSA-ключа в файл.
    
    Args:
        public_key: Объект публичного ключа RSA.
        path: Путь к файлу для записи.

    Raises:
        RuntimeError: Ошибка при сериализации ключа.
    """
    try:
        with open(path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    except Exception as e:
        raise RuntimeError(f"RSA serialize error: {e}")


def deserialize_private_rsa_key(path):
    """
    Десериализация (загрузка) приватного RSA-ключа из файла.
    
    Args:
        path: Путь к файлу с приватным ключом.

    Returns:
        Объект RSAPrivateKey.

    Raises:
        RuntimeError: Ошибка при десериализации.
    """
    try:
        with open(path, 'rb') as f:
            return serialization.load_pem_private_key(f.read(), password=None)
    except Exception as e:
        raise RuntimeError(f"RSA deserialize error: {e}")


def deserialize_public_rsa_key(path):
    """
    Десериализация (загрузка) публичного RSA-ключа из файла.
    
    Args:
        path: Путь к файлу с публичным ключом.

    Returns:
        Объект RSAPublicKey.

    Raises:
        RuntimeError: Ошибка при десериализации.
    """
    try:
        with open(path, 'rb') as f:
            return serialization.load_pem_public_key(f.read())
    except Exception as e:
        raise RuntimeError(f"RSA deserialize error: {e}")


def encrypt_with_rsa_key(data, public_key):
    """
    Шифрование данных с использованием публичного RSA-ключа.
    
    Args:
        data: Исходные данные в байтах.
        public_key: Объект публичного ключа RSA.

    Returns:
        Зашифрованные данные в байтах.

    Raises:
        RuntimeError: Ошибка в процессе шифрования.
    """
    try:
        return public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise RuntimeError(f"RSA encryption error: {e}")


def decrypt_with_rsa_key(ciphertext, private_key):
    """
    Расшифрование данных с использованием приватного RSA-ключа.
    
    Args:
        ciphertext: Зашифрованные данные в байтах.
        private_key: Объект приватного ключа RSA.

    Returns:
        Расшифрованные данные в байтах.

    Raises:
        RuntimeError: Ошибка в процессе расшифрования.
    """
    try:
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise RuntimeError(f"RSA decryption error: {e}")