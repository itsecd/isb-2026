import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

def read_config(config_path: str) -> dict:
    """Загрузка конфигурационных данных из JSON файла"""
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Конфигурационный файл {config_path} не найден")

def store_asymmetric_keys(pub_path: str, priv_path: str, priv_key_obj, pub_key_obj) -> None:
    """Сохранение пары ключей RSA в файлы"""
    try:
        with open(pub_path, 'wb') as pub_file:
            pub_file.write(pub_key_obj.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        with open(priv_path, 'wb') as priv_file:
            priv_file.write(priv_key_obj.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    except IOError as err:
        print(f"Ошибка при сохранении RSA ключей: {err}")

def store_symmetric_key(file_path: str, key_data: bytes) -> None:
    """Запись симметричного ключа в файл"""
    try:
        with open(file_path, 'wb') as key_file:
            key_file.write(key_data)
    except IOError as err:
        raise IOError(f"Не удалось записать ключ в файл {file_path}: {err}")

def retrieve_symmetric_key(file_path: str) -> bytes:
    """Чтение симметричного ключа из файла"""
    try:
        with open(file_path, 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с ключом {file_path} не найден")

def retrieve_rsa_public_key(file_path: str) -> RSAPublicKey:
    """Загрузка открытого RSA ключа"""
    try:
        with open(file_path, 'rb') as pem_file:
            public_key_bytes = pem_file.read()
        return load_pem_public_key(public_key_bytes)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл открытого ключа {file_path} не найден")

def retrieve_rsa_private_key(file_path: str) -> RSAPrivateKey:
    """Загрузка закрытого RSA ключа"""
    try:
        with open(file_path, 'rb') as pem_file:
            private_key_bytes = pem_file.read()
        return load_pem_private_key(private_key_bytes, password=None)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл закрытого ключа {file_path} не найден")

def save_plaintext(content: str, file_path: str) -> None:
    """Сохранение текстового содержимого в файл"""
    try:
        with open(file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(content)
    except IOError as err:
        raise IOError(f"Ошибка записи в файл {file_path}: {err}")

def load_plaintext(file_path: str) -> str:
    """Чтение текстового файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as text_file:
            return text_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Текстовый файл {file_path} не найден")

def save_binary_data(data: bytes, file_path: str) -> None:
    """Запись бинарных данных в файл"""
    try:
        with open(file_path, 'wb') as bin_file:
            bin_file.write(data)
    except IOError as err:
        raise IOError(f"Ошибка записи бинарного файла {file_path}: {err}")

def load_binary_data(file_path: str) -> bytes:
    """Чтение бинарного файла"""
    try:
        with open(file_path, 'rb') as bin_file:
            return bin_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Бинарный файл {file_path} не найден")
