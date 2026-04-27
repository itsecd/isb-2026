import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


def _create_directory(path: str) -> None:
    """Создание директории, если её нет"""
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)


def _read_binary_file(filepath: str) -> bytes:
    """Чтение файла с данными бинарного(байтового) типа"""
    with open(filepath, "rb") as f:
        return f.read()


def _write_binary_file(filepath: str, data: bytes) -> None:
    """Запись в файл бинарных данных"""
    _create_directory(filepath)
    with open(filepath, "wb") as f:
        f.write(data)


def create_symmetric_key(key_size: int = 16) -> bytes:
    """Создание случайного ключа для симметричного шифрования"""
    return os.urandom(key_size)


def create_initial_vector(iv_size: int = 16) -> bytes:
    """Создание мусорного значения для CBC режима"""
    return os.urandom(iv_size)


def _add_padding(data: bytes, block_size_bits: int = 128) -> bytes:
    """Добавление паддинга для блочного шифрования"""
    padder = padding.ANSIX923(block_size_bits).padder()
    return padder.update(data) + padder.finalize()


def _remove_padding(data: bytes, block_size_bits: int = 128) -> bytes:
    """Удаление паддинга после расшифровки"""
    unpadder = padding.ANSIX923(block_size_bits).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def symmetric_encrypt(key: bytes, iv: bytes, plaintext: bytes, block_size_bits: int = 128) -> bytes:
    """Шифрование данных алгоритмом SEED в режиме CBC"""
    cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_data = _add_padding(plaintext, block_size_bits)
    return encryptor.update(padded_data) + encryptor.finalize()


def symmetric_decrypt(key: bytes, iv: bytes, ciphertext: bytes, block_size_bits: int = 128) -> bytes:
    """Расшифрование данных алгоритмом SEED в режиме CBC"""
    cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    return _remove_padding(decrypted_padded, block_size_bits)


def create_asymmetric_pair(key_size: int = 2048, exponent: int = 65537) -> tuple:
    """Создание ключей RSA двух типов для шифрования"""
    private_key = rsa.generate_private_key(public_exponent=exponent, key_size=key_size)
    public_key = private_key.public_key()
    return (private_key, public_key)


def asymmetric_encrypt(data: bytes, public_key) -> bytes:
    """Шифрование данных открытым ключом RSA"""
    return public_key.encrypt(data, asymmetric_padding.OAEP(
        mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None))


def asymmetric_decrypt(data: bytes, private_key) -> bytes:
    """Расшифрование данных с помощью закрытого ключа RSA"""
    return private_key.decrypt(data, asymmetric_padding.OAEP(
        mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None))


def store_private_key(private_key, filepath: str) -> None:
    """Сохранение закрытого ключа в файл разрешения .pem без пароля"""
    _create_directory(filepath)
    pem_data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())
    _write_binary_file(filepath, pem_data)


def store_public_key(public_key, filepath: str) -> None:
    """Сохранение открытого ключа в файл разрешения .pem"""
    _create_directory(filepath)
    pem_data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    _write_binary_file(filepath, pem_data)


def load_private_key(filepath: str):
    """Загрузка закрытого ключа из незапароленного файла с разрешением .pem"""
    data = _read_binary_file(filepath)
    return load_pem_private_key(data, password=None)


def load_public_key(filepath: str):
    """Загрузка открытого ключа из файла с разрешением .pem"""
    data = _read_binary_file(filepath)
    return load_pem_public_key(data)