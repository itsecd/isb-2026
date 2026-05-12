import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

_OAEP = lambda: padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)


def generate_rsa_keys(key_size: int = 2048):
    """
    Генерация пары RSA-ключей.

    Args:
        key_size: Размер ключа в битах (по умолчанию 2048).

    Returns:
        tuple: (private_key, public_key) - пара ключей RSA.

    Raises:
        RuntimeError: Ошибка при генерации ключей.
    """
    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        print(f"RSA-ключи ({key_size} бит) сгенерированы.")
        return private_key, private_key.public_key()
    except Exception as e:
        raise RuntimeError(f"Ошибка при генерации ключей: {e}")


def save_rsa_keys(private_key, public_key, private_path: str, public_path: str) -> None:
    """
    Сохранение RSA-ключей в PEM-файлы.

    Args:
        private_key: Закрытый ключ RSA.
        public_key: Открытый ключ RSA.
        private_path: Путь для сохранения закрытого ключа.
        public_path: Путь для сохранения открытого ключа.

    Raises:
        RuntimeError: Ошибка при сохранении ключей.
    """
    try:
        for path, data in [
            (public_path,  public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo)),
            (private_path, private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption())),
        ]:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "wb") as f:
                f.write(data)
            print(f"Ключ сохранён: {path}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при сохранении ключей: {e}")


def load_public_key(path: str):
    """
    Загрузка открытого RSA-ключа из PEM-файла.

    Args:
        path: Путь к файлу с открытым ключом.

    Returns:
        PublicKey: Загруженный открытый ключ.

    Raises:
        RuntimeError: Ошибка при загрузке открытого ключа.
    """
    try:
        with open(path, "rb") as f:
            key = load_pem_public_key(f.read())
        print(f"Открытый ключ загружен: {path}")
        return key
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке открытого ключа: {e}")


def load_private_key(path: str):
    """
    Загрузка закрытого RSA-ключа из PEM-файла.

    Args:
        path: Путь к файлу с закрытым ключом.

    Returns:
        PrivateKey: Загруженный закрытый ключ.

    Raises:
        RuntimeError: Ошибка при загрузке закрытого ключа.
    """
    try:
        with open(path, "rb") as f:
            key = load_pem_private_key(f.read(), password=None)
        print(f"Закрытый ключ загружен: {path}")
        return key
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке закрытого ключа: {e}")


def rsa_encrypt(public_key, data: bytes) -> bytes:
    """
    Шифрование данных с помощью открытого RSA-ключа.

    Args:
        public_key: Открытый ключ RSA.
        data: Данные для шифрования.

    Returns:
        bytes: Зашифрованные данные.

    Raises:
        RuntimeError: Ошибка при выполнении шифрования.
    """
    try:
        return public_key.encrypt(data, _OAEP())
    except Exception as e:
        raise RuntimeError(f"Ошибка при шифровании: {e}")


def rsa_decrypt(private_key, data: bytes) -> bytes:
    """
    Дешифрование данных с помощью закрытого RSA-ключа.

    Args:
        private_key: Закрытый ключ RSA.
        data: Зашифрованные данные в байтовом формате.

    Returns:
        bytes: Расшифрованные данные.

    Raises:
        ValueError: Ошибка при дешифровании (неверные данные или ключ).
        RuntimeError: Ошибка при выполнении дешифрования.
    """
    try:
        return private_key.decrypt(data, _OAEP())
    except Exception as e:
        raise RuntimeError(f"Ошибка при дешифровании: {e}")