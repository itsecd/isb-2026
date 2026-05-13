from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def read_binary(path: str) -> bytes:
    """
    Чтение бинарных данных из файла.
    :param path: путь к файлу
    :return: данные из файла в виде байтов
    """
    with open(path, "rb") as f:
        return f.read()


def save_binary(data: bytes, path: str) -> None:
    """
    Сохранение бинарных данных в файл.
    :param data: данные для сохранения
    :param path: путь к файлу
    :return: не возвращается
    """
    with open(path, "wb") as f:
        f.write(data)



def load_private_key(path: str) -> RSAPrivateKey:
    """
    Загрузка закрытого RSA-ключа из PEM-файла.
    :param path: путь к файлу с закрытым RSA-ключом
    :return: закрытый RSA-ключ
    """
    private_bytes = read_binary(path)
    private_key = load_pem_private_key(private_bytes,password=None)
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