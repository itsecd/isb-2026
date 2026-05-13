from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def read_binary(path: str) -> bytes:
    """
    Чтение бинарных данных из файла.
    :param path: путь к файлу
    :return: данные из файла в виде байтов
    """

    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {path}") from e
    except PermissionError as e:
        raise PermissionError(f"No permission to read file: {path}") from e
    except OSError as e:
        raise OSError(f"File reading error for {path}: {e}") from e

def save_binary(data: bytes, path: str) -> None:
    """
    Сохранение бинарных данных в файл.
    :param data: данные для сохранения
    :param path: путь к файлу
    :return: не возвращается
    """
    try: 
        with open(path, "wb") as f:
            f.write(data)
    except PermissionError as e:
        raise PermissionError(f"No permission to write file: {path}") from e
    except OSError as e:
        raise OSError(f"File writing error for {path}: {e}") from e


def load_private_key(path: str) -> RSAPrivateKey:
    """
    Загрузка закрытого RSA-ключа из PEM-файла.
    :param path: путь к файлу с закрытым RSA-ключом
    :return: закрытый RSA-ключ
    """
    private_bytes = read_binary(path)
    try:
        private_key = load_pem_private_key(private_bytes, password=None)
    except ValueError as e:
        raise ValueError(
            f"Failed to load private RSA key from {path}. "
            "The file may be corrupted, have an invalid format, or be password-protected."
        ) from e
    return private_key


def load_encrypted_key(path: str) -> bytes:
    """
    Чтение зашифрованного симметричного AES-ключа из файла.
    :param path: путь к файлу с зашифрованным симметричным ключом
    :return: зашифрованный симметричный ключ в виде байтов
    """

    return read_binary(path)




def read_encrypted_key(path: str) -> bytes:
    """
    Чтение зашифрованного симметричного AES-ключа из файла.
    :param path: путь к файлу с зашифрованным симметричным ключом
    :return: зашифрованный симметричный ключ в виде байтов
    """
    return read_binary(path)


def load_ciphertext(path: str) -> bytes:
    """
    Чтение зашифрованного текста из файла.
    :param path: путь к файлу с зашифрованным текстом
    :return: зашифрованный текст в виде байтов
    """

    return read_binary(path)


def save_decrypted_text(text: bytes, path: str) -> None:
    """
    Сохранение расшифрованных данных в файл.
    :param text: расшифрованные данные в виде байтов
    :param path: путь для сохранения расшифрованных данных
    :return: не возвращается
    """

    save_binary(text, path)