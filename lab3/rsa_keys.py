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


def _serialize_public_key(public_key) -> bytes:
    """
    Сериализация открытого ключа в PEM-формат.

    Args:
        public_key: Открытый ключ RSA.

    Returns:
        bytes: PEM-представление открытого ключа.

    Raises:
        RuntimeError: Ошибка при сериализации.
    """
    try:
        return public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    except Exception as e:
        raise RuntimeError(f"Ошибка при сериализации открытого ключа: {e}")


def _serialize_private_key(private_key) -> bytes:
    """
    Сериализация закрытого ключа в PEM-формат (без шифрования).

    Args:
        private_key: Закрытый ключ RSA.

    Returns:
        bytes: PEM-представление закрытого ключа.

    Raises:
        RuntimeError: Ошибка при сериализации.
    """
    try:
        return private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
    except Exception as e:
        raise RuntimeError(f"Ошибка при сериализации закрытого ключа: {e}")


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
    file_io.write_file(public_path, _serialize_public_key(public_key))
    file_io.write_file(private_path, _serialize_private_key(private_key))


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
    try:
        key = load_pem_public_key(file_io.read_file(path))
        print(f"Открытый ключ загружен: {path}")
        return key
    except FileNotFoundError:
        raise
    except (ValueError, TypeError) as e:
        raise ValueError(f"Некорректный формат открытого ключа '{path}': {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке открытого ключа '{path}': {e}")


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
    try:
        key = load_pem_private_key(file_io.read_file(path), password=None)
        print(f"Закрытый ключ загружен: {path}")
        return key
    except FileNotFoundError:
        raise
    except (ValueError, TypeError) as e:
        raise ValueError(f"Некорректный формат закрытого ключа '{path}': {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке закрытого ключа '{path}': {e}")


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
