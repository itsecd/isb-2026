import os
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

def check_file(target_path: str) -> None:
    """
    Гарантирует наличие родительской директории для указанного пути.
    
    Args:
        target_path (str): Полный путь к целевому файлу.
        
    Raises:
        OSError: Если не удалось создать директорию.
    """
    try:
        directory = os.path.dirname(target_path)
        match directory:
            case "":
                return
            case dir_path:
                os.makedirs(dir_path, exist_ok=True)
    except Exception as exc:
        print(f"Ошибка создания директории: {exc}")
        raise

def save_private_key(destination: str, private_key: rsa.RSAPrivateKey) -> None:
    """
    Экспортирует приватный RSA ключ в PEM формат без парольной защиты.
    
    Args:
        destination (str): Путь для сохранения файла ключа.
        private_key (rsa.RSAPrivateKey): Объект приватного ключа.
        
    Raises:
        OSError: При ошибке записи или создания директории.
    """
    try:
        check_file(destination)
        with open(destination, "wb") as stream:
            stream.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    except Exception as exc:
        print(f"Ошибка сохранения приватного ключа: {exc}")
        raise

def save_public_key(destination: str, public_key: rsa.RSAPublicKey) -> None:
    """
    Экспортирует публичный RSA-ключ в PEM формат.
    
    Args:
        destination (str): Путь для сохранения файла ключа.
        public_key (rsa.RSAPublicKey): Объект публичного ключа.
        
    Raises:
        OSError: При ошибке записи или создания директории.
    """
    try:
        check_file(destination)
        with open(destination, "wb") as stream:
            stream.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    except Exception as exc:
        print(f"Ошибка сохранения публичного ключа: {exc}")
        raise

def open_private_key(source: str) -> rsa.RSAPrivateKey:
    """
    Импортирует приватный RSA-ключ из PEM файла.
    
    Args:
        source (str): Путь к файлу приватного ключа.
        
    Returns:
        rsa.RSAPrivateKey: Загруженный объект приватного ключа.
        
    Raises:
        OSError: При ошибке чтения файла.
        ValueError: При некорректном формате или повреждении ключа.
    """
    try:
        with open(source, "rb") as stream:
            return load_pem_private_key(stream.read(), password=None)
    except Exception as exc:
        print(f"Ошибка загрузки приватного ключа: {exc}")
        raise

def open_public_key(source: str) -> rsa.RSAPublicKey:
    """
    Импортирует публичный RSA-ключ из PEM файла.
    
    Args:
        source (str): Путь к файлу публичного ключа.
        
    Returns:
        rsa.RSAPublicKey: Загруженный объект публичного ключа.
        
    Raises:
        OSError: При ошибке чтения файла.
        ValueError: При некорректном формате или повреждении ключа.
    """
    try:
        with open(source, "rb") as stream:
            return load_pem_public_key(stream.read())
    except Exception as exc:
        print(f"Ошибка загрузки публичного ключа: {exc}")
        raise

def open_binary(source: str) -> bytes:
    """
    Считывает полное содержимое файла в бинарном режиме.
    
    Args:
        source (str): Путь к исходному файлу.
        
    Returns:
        bytes: Прочитанные бинарные данные.
        
    Raises:
        OSError: При ошибке открытия или чтения файла.
    """
    try:
        with open(source, "rb") as stream:
            return stream.read()
    except Exception as exc:
        print(f"Ошибка чтения бинарного файла: {exc}")
        raise

def save_binary(destination: str, payload: bytes) -> None:
    """
    Записывает бинарные данные в файл, создавая необходимые директории.
    
    Args:
        destination (str): Путь для сохранения файла.
        payload (bytes): Данные для записи.
        
    Raises:
        OSError: При ошибке записи или создания директории.
    """
    try:
        check_file(destination)
        with open(destination, "wb") as stream:
            stream.write(payload)
    except Exception as exc:
        print(f"Ошибка записи бинарных данных: {exc}")
        raise

def open_json(source: str) -> dict:
    """
    Десериализует содержимое JSON-файла в словарь Python.
    
    Args:
        source (str): Путь к конфигурационному JSON-файлу.
        
    Returns:
        dict: Распакованные данные конфигурации.
        
    Raises:
        OSError: При ошибке доступа к файлу.
        json.JSONDecodeError: При нарушении синтаксиса JSON.
    """
    try:
        with open(source, "r", encoding="utf-8") as stream:
            return json.load(stream)
    except Exception as exc:
        print(f"Ошибка загрузки JSON: {exc}")
        raise
