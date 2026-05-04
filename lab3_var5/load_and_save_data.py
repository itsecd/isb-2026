import json
from cryptography.hazmat.primitives import serialization 
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


def load_private_key(path_to_private: str) -> RSAPrivateKey:
    """
    Загрузка закрытого ключа из PEM файла
    """
    try:
        with open(path_to_private, 'rb') as pem_in:
            private_bytes = pem_in.read()
        return load_pem_private_key(private_bytes, password=None)
    except Exception as e:
        print(f"Ошибка при загрузке закрытого ключа: {e}")
        return None


def load_public_key(path_to_public: str):
    """
    Загрузка открытого ключа RSA из файла
    """
    try:
        with open(path_to_public, 'rb') as pem_in:
            public_bytes = pem_in.read()
        return load_pem_public_key(public_bytes)
    except Exception as e:
        print(f"Ошибка при загрузке открытого ключа: {e}")
        return None


def load_encrypt_symmetric_key(path_to_sym_key: str) -> bytes:
    """
    Загрузка зашифрованного симметричного ключа
    """
    try:
        with open(path_to_sym_key, mode='rb') as key_file: 
            return key_file.read()
    except Exception as e:
        print(f"Ошибка при загрузке симметричного ключа: {e}")
        return b""


def load_json(path_to_json: str) -> dict:
    """
    Загрузка настроек из json файла
    """
    try:
        with open(path_to_json) as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Ошибка при загрузке JSON: {e}")
        return {}


def read_text_file(filepath: str) -> str:
    """
    Чтение исходного текста из файла
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка при чтении текста: {e}")
        return ""


def write_text_file(text: str, filepath: str) -> None:
    """
    Запись расшифрованного текста в файл
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print(f"Ошибка при записи текста: {e}")


def read_binary_file(filepath: str) -> bytes:
    """
    Чтение бинарных данных из файла
    """
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка при чтении бинарного файла: {e}")
        return b""


def write_binary_file(data: bytes, filepath: str) -> None:
    """
    Запись бинарных данных в файл
    """
    try:
        with open(filepath, 'wb') as f:
            f.write(data)
    except Exception as e:
        print(f"Ошибка при записи бинарного файла: {e}")


def save_asym_keys(private_key, public_key, path_private: str, path_public: str) -> None:
    """
    Сохранение пары ключей RSA в PEM файлы
    """
    try:
        with open(path_private, 'wb') as priv_file:
            priv_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()  
                )
            )
        with open(path_public, 'wb') as pub_file:
            pub_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )
    except Exception as e:
        print(f"Ошибка при сохранении RSA ключей: {e}")


def save_symmetric_key(encrypted_key: bytes, output_path: str) -> None:
    """
    Сохранение зашифрованного симметричного ключа в файл
    """
    try:
        with open(output_path, 'wb') as f:
            f.write(encrypted_key)
    except Exception as e:
        print(f"Ошибка при сохранении симметричного ключа: {e}")