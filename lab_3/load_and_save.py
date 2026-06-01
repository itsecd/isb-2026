import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


def write_symmetric_key(symmetric_key: bytes, symmetric_path: str) -> None:
    """
    Сохраняет симметричный ключ в бинарный файл.

    Параметры:
    symmetric_key: bytes - симметричный ключ шифрования.
    symmetric_path: str - путь к файлу для сохранения ключа.

    Возвращает:
    None
    """
    try:
        with open(symmetric_path, 'wb') as key_file:
            key_file.write(symmetric_key)
    except Exception as ex:
        print(f"Ошибка!: {ex}")


def write_public_key(public_key: RSAPublicKey, public_path: str) -> None:
    """
    Сохраняет открытый RSA-ключ в PEM-формате.

    Параметры:
    public_key: RSAPublicKey - открытый RSA-ключ.
    public_path: str - путь к файлу для сохранения открытого ключа.

    Возвращает:
    None
    """
    try:
        with open(public_path, 'wb') as public_out:
            public_out.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    except Exception as ex:
        print(f"Ошибка!: {ex}")


def write_private_key(private_key: RSAPrivateKey, private_path: str) -> None:
    """
    Сохраняет закрытый RSA-ключ в PEM-формате.

    Параметры:
    private_key: RSAPrivateKey - закрытый RSA-ключ.
    private_path: str - путь к файлу для сохранения закрытого ключа.

    Возвращает:
    None
    """
    try:
        with open(private_path, 'wb') as private_out:
            private_out.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    except Exception as ex:
        print(f"Ошибка!: {ex}")


def read_text(initial_file_path: str) -> bytes:
    """
    Читает данные из файла в бинарном режиме.

    Параметры:
    initial_file_path: str - путь к файлу.

    Возвращает:
    bytes - содержимое файла.
    """
    try:
        with open(initial_file_path, 'rb') as f:
            return f.read()
    except Exception as ex:
        print(f"Ошибка!: {ex}")
        return b""


def read_symmetric_key(symmetric_key_path: str) -> bytes:
    """
    Читает симметричный ключ из бинарного файла.

    Параметры:
    symmetric_key_path: str - путь к файлу с симметричным ключом.

    Возвращает:
    bytes - симметричный ключ.
    """
    return read_text(symmetric_key_path)


def read_asymmetric_key(public_key_path: str, private_key_path: str) -> tuple:
    """
    Читает открытый и закрытый RSA-ключи из PEM-файлов.

    Параметры:
    public_key_path: str - путь к файлу с открытым RSA-ключом.
    private_key_path: str - путь к файлу с закрытым RSA-ключом.

    Возвращает:
    tuple - открытый и закрытый RSA-ключи.
    """
    try:
        public_bytes = read_text(public_key_path)
        private_bytes = read_text(private_key_path)

        public_key = load_pem_public_key(public_bytes)
        private_key = load_pem_private_key(private_bytes, password=None)

        return public_key, private_key
    except Exception as ex:
        print(f"Ошибка!: {ex}")


def write_text(text: bytes, enc_file_path: str) -> None:
    """
    Записывает данные в бинарный файл.

    Параметры:
    text: bytes - данные для записи.
    enc_file_path: str - путь к файлу для сохранения данных.

    Возвращает:
    None
    """
    try:
        with open(enc_file_path, 'wb') as f:
            f.write(text)
    except Exception as ex:
        print(f"Ошибка!: {ex}")


def load_settings(settings_path: str = "settings.json") -> dict:
    """
    Загружает настройки из JSON-файла.

    Параметры:
    settings_path: str - путь к JSON-файлу с настройками.

    Возвращает:
    dict - словарь с настройками.
    """
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as ex:
        print(f"Ошибка!: {ex}")
        return {}
