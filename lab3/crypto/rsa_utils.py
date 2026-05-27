from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key



def generate_rsa_keys():
    """
    Генерирует пару RSA ключей.

    Returns:
        tuple: Приватный и публичный RSA ключи.

    Raises:
        RuntimeError: Если генерация ключей завершилась ошибкой.
    """

    try:
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()

        return private_key, public_key

    except Exception as err:
        raise RuntimeError(f"Ошибка генерации RSA ключей: {err}")


def save_public_key(public_key, path):
    """
    Сохраняет публичный RSA ключ в PEM-файл.

    Args:
        public_key: Публичный RSA ключ.
        path (str): Путь сохранения.

    Raises:
        OSError: Если файл не удалось сохранить.
    """

    try:
        with open(path, 'wb') as file:
            file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo))

    except OSError as e:
        raise OSError(f"Ошибка сохранения публичного ключа: {e}")


def save_private_key(private_key, path):
    """
    Сохраняет приватный RSA ключ в PEM-файл.

    Args:
        private_key: Приватный RSA ключ.
        path (str): Путь сохранения.

    Raises:
        OSError: Если файл не удалось сохранить.
    """

    try:
        with open(path, 'wb') as file:
            file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()))

    except OSError as e:
        raise OSError(f"Ошибка сохранения приватного ключа: {e}")


def load_public_key(path):
    """
    Загружает публичный RSA ключ из PEM-файла.

    Args:
        path (str): Путь к PEM-файлу.

    Returns:
        rsa.RSAPublicKey: Публичный RSA ключ.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если ключ поврежден.
    """

    try:
        with open(path, 'rb') as file:
            return load_pem_public_key(file.read())

    except FileNotFoundError:
        raise FileNotFoundError(f"Публичный ключ не найден: {path}")

    except ValueError as err:
        raise ValueError(f"Ошибка загрузки публичного ключа: {err}")


def load_private_key(path):
    """
    Загружает приватный RSA ключ из PEM-файла.

    Args:
        path (str): Путь к PEM-файлу.

    Returns:
        rsa.RSAPrivateKey: Приватный RSA ключ.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если ключ поврежден.
    """

    try:
        with open(path, 'rb') as file:
            return load_pem_private_key(file.read(), password=None)

    except FileNotFoundError:
        raise FileNotFoundError(f"Приватный ключ не найден: {path}")

    except ValueError as err:
        raise ValueError(f"Ошибка загрузки приватного ключа: {err}")


def rsa_encrypt(public_key, data):
    """
    Шифрует данные с помощью RSA-OAEP.

    Args:
        public_key: Публичный RSA ключ.
        data (bytes): Данные для шифрования.

    Returns:
        bytes: Зашифрованные данные.

    Raises:
        ValueError: Если шифрование не удалось.
    """

    try:
        return public_key.encrypt(
            data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))

    except Exception as err:
        raise ValueError(f"Ошибка RSA шифрования: {err}")


def rsa_decrypt(private_key, encrypted_data):
    """
    Расшифровывает данные с помощью RSA-OAEP.

    Args:
        encrypted_data (bytes): Зашифрованные данные.
        private_key: Приватный RSA ключ.

    Returns:
        bytes: Расшифрованные данные.

    Raises:
        ValueError: Если дешифрование не удалось.
    """

    try:
        return private_key.decrypt(
            encrypted_data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))

    except Exception as err:
        raise ValueError(f"Ошибка RSA дешифрования: {err}")