from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


def generate_key_pair() -> tuple:
    """
    Генерирует пару асимметричных ключей RSA длиной 2048 бит.
    
    Returns:
        tuple: (приватный_ключ, публичный_ключ)
    
    Raises:
        Exception: Ошибки при генерации ключей
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()


def save_public_key(path: str, public_key) -> None:
    """
    Сохраняет публичный ключ RSA в файл в формате PEM.
    
    Args:
        path (str): Путь для сохранения файла ключа
        public_key: Публичный ключ RSA
    
    Raises:
        FileUtilsError: Ошибки при записи в файл
        Exception: Ошибки при сериализации ключа
    """
    with open(path, 'wb') as public_out:
        public_out.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def save_private_key(path: str, private_key) -> None:
    """
    Сохраняет приватный ключ RSA в файл в формате PEM без шифрования.
    
    Args:
        path (str): Путь для сохранения файла ключа
        private_key: Приватный ключ RSA
    
    Raises:
        FileUtilsError: Ошибки при записи в файл
        Exception: Ошибки при сериализации ключа
    """
    with open(path, 'wb') as private_out:
        private_out.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))


def load_private_key(path: str):
    """
    Загружает приватный ключ RSA из PEM файла.
    
    Args:
        path (str): Путь к файлу приватного ключа
    
    Returns:
        Загруженный приватный ключ RSA
    
    Raises:
        FileUtilsError: Ошибки при чтении файла
        Exception: Ошибки при десериализации ключа
    """
    with open(path, 'rb') as private_file:
        return load_pem_private_key(private_file.read(), password=None)


def load_public_key(path: str):
    """
    Загружает публичный ключ RSA из PEM файла.
    
    Args:
        path (str): Путь к файлу публичного ключа
    
    Returns:
        Загруженный публичный ключ RSA
    
    Raises:
        FileUtilsError: Ошибки при чтении файла
        Exception: Ошибки при десериализации ключа
    """
    with open(path, 'rb') as public_file:
        return load_pem_public_key(public_file.read())


def encrypt_rsa(public_key, data: bytes) -> bytes:
    """
    Шифрует данные с использованием алгоритма RSA и OAEP паддинга.
    
    Args:
        public_key: Публичный ключ RSA
        data (bytes): Данные для шифрования (максимум 190 байт для ключа 2048 бит)
    
    Returns:
        bytes: Зашифрованные данные
    
    Raises:
        ValueError: Если данные слишком большие для шифрования RSA
        Exception: Ошибки при шифровании
    """
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_rsa(private_key, data: bytes) -> bytes:
    """
    Дешифрует данные с использованием алгоритма RSA и OAEP паддинга.
    
    Args:
        private_key: Приватный ключ RSA
        data (bytes): Зашифрованные данные
    
    Returns:
        bytes: Расшифрованные данные
    
    Raises:
        ValueError: Если данные повреждены или ключ не подходит
        Exception: Ошибки при дешифровании
    """
    return private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
