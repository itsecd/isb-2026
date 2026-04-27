import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


def generate_keys() -> list:
    """Генерация двух типов ключей
    для работы алгоритма RSA
    Возврат в виде списка
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return [private_key, public_key]


def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """Шифровка некой информации при помощи
    алгоритма RSA и публичного ключа с 
    обработкой ошибок
    """
    try:
        encrypt_data = public_key.encrypt(
            data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None))
        return encrypt_data
    except ValueError as e:
        print(f"Ошибка шифрования: {e}")
        raise


def decrypt_with_private_key(data: bytes, private_key) -> bytes:
    """Дешифровка некой информации при помощи 
    алгоритмов RSA и приватного ключа с обработкой 
    ошибок на дешифровку
    """
    try:
        decrypt_data = private_key.decrypt(
            data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None))
        return decrypt_data
    except ValueError as e:
        print(f"Ошибка дешифровки: {e}")
        raise


def serialize_public_key(public_key, file: str) -> None:
    """Сброс публичного ключа в сторонний файл 
    с форматом .pem(требования)
    """
    os.makedirs(os.path.dirname(file), exist_ok=True)
    maked_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(file, "wb") as f:
        f.write(maked_public_key)


def serialize_private_key(private_key, file: str) -> None:
    """Сброс приватного ключа в сторонний файл 
    с форматом .pem(требования)
    Перенос осуществляется без пароля 
    для простоты демонстрации 
    """
    os.makedirs(os.path.dirname(file), exist_ok=True)
    maked_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())
    with open(file, "wb") as f:
        f.write(maked_private_key)


def load_public_key(file: str):
    """Подгрузка публичного ключа из 
    стороннего файла
    """
    with open(file, "rb") as f:
        public_key = load_pem_public_key(f.read())
    return public_key


def load_private_key(file: str):
    """Подгрузка приватного ключа из 
    стороннего файла
    """
    with open(file, "rb") as f:
        private_key = load_pem_private_key(f.read(), password=None)
    return private_key

