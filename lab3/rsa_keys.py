from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import file_io


def _oaep_padding() -> padding.OAEP:
    """Возвращает параметры OAEP-дополнения."""
    return padding.OAEP(
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
        tuple[PrivateKey, PublicKey]: Пара ключей RSA.

    Raises:
        ValueError: Недопустимый размер ключа.
        RuntimeError: Ошибка при генерации.
    """
    if key_size < 512:
        raise ValueError(f"Размер RSA-ключа должен быть не менее 512 бит")
    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        print(f"RSA-ключи ({key_size} бит) сгенерированы.")
        return private_key, private_key.public_key()
    except Exception as e:
        raise RuntimeError(f"Ошибка при генерации RSA-ключей: {e}")


def save_rsa_keys(private_key, public_key, private_path: str, public_path: str) -> None:
    """
    Сохранение RSA-ключей в PEM-файлы.

    Args:
        private_key: Закрытый ключ RSA.
        public_key: Открытый ключ RSA.
        private_path: Путь для сохранения закрытого ключа.
        public_path: Путь для сохранения открытого ключа.

    Raises:
        RuntimeError: Ошибка при сериализации или записи.
    """
    try:
        pub_pem = public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        priv_pem = private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
    except Exception as e:
        raise RuntimeError(f"Ошибка при сериализации RSA-ключей: {e}")

    file_io.write_file(public_path, pub_pem)
    file_io.write_file(private_path, priv_pem)


def _load_pem_key(path: str, loader, label: str):
    """
    Вспомогательная функция: загрузка PEM-ключа из файла.

    Args:
        path: Путь к файлу с ключом.
        loader: Функция десериализации (load_pem_public_key или load_pem_private_key).
        label: Метка ключа для диагностических сообщений.

    Returns:
        Загруженный ключ.

    Raises:
        FileNotFoundError: Файл не найден.
        ValueError: Некорректный формат PEM.
        RuntimeError: Иная ошибка при загрузке.
    """
    try:
        with open(path, "rb") as f:
            key = loader(f.read())
        print(f"{label} загружен: {path}")
        return key
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {label.lower()} не найден: {path}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Некорректный формат {label.lower()} '{path}': {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке {label.lower()} '{path}': {e}")


def load_public_key(path: str):
    """
    Загрузка открытого RSA-ключа из PEM-файла.

    Args:
        path: Путь к файлу с открытым ключом.

    Returns:
        PublicKey: Загруженный открытый ключ.

    Raises:
        FileNotFoundError: Файл не найден.
        ValueError: Некорректный формат PEM.
        RuntimeError: Иная ошибка при загрузке.
    """
    return _load_pem_key(path, load_pem_public_key, "Открытый ключ")


def load_private_key(path: str):
    """
    Загрузка закрытого RSA-ключа из PEM-файла.

    Args:
        path: Путь к файлу с закрытым ключом.

    Returns:
        PrivateKey: Загруженный закрытый ключ.

    Raises:
        FileNotFoundError: Файл не найден.
        ValueError: Некорректный формат PEM.
        RuntimeError: Иная ошибка при загрузке.
    """
    return _load_pem_key(path, lambda data: load_pem_private_key(data, password=None), "Закрытый ключ")


def rsa_encrypt(public_key, data: bytes) -> bytes:
    """
    Шифрование данных открытым RSA-ключом (OAEP/SHA-256).

    Args:
        public_key: Открытый ключ RSA.
        data: Данные для шифрования.

    Returns:
        bytes: Зашифрованные данные.

    Raises:
        ValueError: Данные слишком велики для ключа.
        RuntimeError: Ошибка при шифровании.
    """
    try:
        return public_key.encrypt(data, _oaep_padding())
    except ValueError as e:
        raise ValueError(f"Данные слишком велики для RSA-шифрования: {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при RSA-шифровании: {e}")


def rsa_decrypt(private_key, data: bytes) -> bytes:
    """
    Дешифрование данных закрытым RSA-ключом (OAEP/SHA-256).

    Args:
        private_key: Закрытый ключ RSA.
        data: Зашифрованные данные.

    Returns:
        bytes: Расшифрованные данные.

    Raises:
        ValueError: Некорректные данные или несовпадение ключа.
        RuntimeError: Ошибка при дешифровании.
    """
    try:
        return private_key.decrypt(data, _oaep_padding())
    except ValueError as e:
        raise ValueError(f"Ошибка дешифрования: некорректные данные или ключ: {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при RSA-дешифровании: {e}")
