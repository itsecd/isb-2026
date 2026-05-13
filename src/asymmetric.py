from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

from .utils import read_binary_file, write_binary_file
from .config import RSA_KEY_SIZE, RSA_PUBLIC_EXPONENT


def generate_rsa_keypair():
    """
    Генерация пары RSA ключей (публичный и приватный).
    
    Returns:
        tuple: (private_key, public_key) - кортеж из приватного и публичного ключей
    
    Raises:
        ValueError: Если параметры RSA_KEY_SIZE или RSA_PUBLIC_EXPONENT некорректны
    """
    private_key = rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE
    )
    return private_key, private_key.public_key()


def save_public_key(public_key, filepath: str):
    """
    Сохранение открытого ключа в PEM файл.
    
    Args:
        public_key: Публичный RSA ключ
        filepath (str): Путь для сохранения файла
    
    Returns:
        None
    
    Raises:
        IOError: Если нет прав на запись в файл
        TypeError: Если переданный public_key имеет неверный тип
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    write_binary_file(filepath, pem)
    print(f" Открытый ключ сохранен: {filepath}")


def save_private_key(private_key, filepath: str):
    """
    Сохранение приватного ключа в PEM файл (без парольной защиты).
    
    Args:
        private_key: Приватный RSA ключ
        filepath (str): Путь для сохранения файла
    
    Returns:
        None
    
    Raises:
        IOError: Если нет прав на запись в файл
        TypeError: Если переданный private_key имеет неверный тип
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    write_binary_file(filepath, pem)
    print(f" Приватный ключ сохранен: {filepath}")


def load_public_key(filepath: str):
    """
    Загрузка открытого ключа из PEM файла.
    
    Args:
        filepath (str): Путь к файлу с публичным ключом
    
    Returns:
        PublicKey: Загруженный публичный RSA ключ
    
    Raises:
        FileNotFoundError: Если файл не существует
        ValueError: Если файл повреждён или имеет неверный формат
    """
    data = read_binary_file(filepath)
    return serialization.load_pem_public_key(data)


def load_private_key(filepath: str):
    """
    Загрузка приватного ключа из PEM файла (без пароля).
    
    Args:
        filepath (str): Путь к файлу с приватным ключом
    
    Returns:
        PrivateKey: Загруженный приватный RSA ключ
    
    Raises:
        FileNotFoundError: Если файл не существует
        ValueError: Если файл повреждён или требует пароль
    """
    data = read_binary_file(filepath)
    return serialization.load_pem_private_key(data, password=None)


def encrypt_with_rsa(key_data: bytes, public_key_path: str) -> bytes:
    """
    Шифрование данных открытым RSA ключом с использованием OAEP.
    
    Args:
        key_data (bytes): Данные для шифрования
        public_key_path (str): Путь к файлу с публичным ключом
    
    Returns:
        bytes: Зашифрованные данные
    
    Raises:
        FileNotFoundError: Если файл с ключом не существует
        ValueError: Если данные слишком большие для RSA шифрования
    """
    public_key = load_public_key(public_key_path)
    return public_key.encrypt(
        key_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_with_rsa(encrypted_data: bytes, private_key_path: str) -> bytes:
    """
    Расшифровка данных приватным RSA ключом.
    
    Args:
        encrypted_data (bytes): Зашифрованные данные
        private_key_path (str): Путь к файлу с приватным ключом
    
    Returns:
        bytes: Расшифрованные данные
    
    Raises:
        FileNotFoundError: Если файл с ключом не существует
        ValueError: Если данные повреждены или ключ не подходит
    """
    private_key = load_private_key(private_key_path)
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )