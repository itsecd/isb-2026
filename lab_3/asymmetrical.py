from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from file_utils import write_file, read_file

def generate_rsa_keypair():
    """
    Генерирует пару RSA-ключей (приватный и публичный) с длиной 2048 бит.

    Выходные данные:
        tuple: (private_key, public_key)
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()

def save_private_key(private_key, path):
    """
    Сохраняет приватный RSA-ключ в файл в формате PEM (без шифрования).

    Входные данные:
        private_key: Приватный ключ.
        path (str): Путь для сохранения.
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    write_file(path, pem)

def save_public_key(public_key, path):
    """
    Сохраняет публичный RSA-ключ в файл в формате PEM.

    Входные данные:
        public_key: Публичный ключ.
        path (str): Путь для сохранения.
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    write_file(path, pem)

def load_private_key(path):
    """
    Загружает приватный RSA-ключ из PEM-файла.

    Входные данные:
        path (str): Путь к файлу с ключом.

    Выходные данные:
        private_key: Приватный ключ, или None в случае ошибки.
    """
    data = read_file(path)
    if data is None:
        return None
    try:
        return serialization.load_pem_private_key(data, password=None)
    except Exception as e:
        print(f"Ошибка загрузки приватного ключа: {e}")
        return None

def load_public_key(path):
    """
    Загружает публичный RSA-ключ из PEM-файла.

    Входные данные:
        path (str): Путь к файлу с ключом.

    Выходные данные:
        public_key: Публичный ключ, или None в случае ошибки.
    """
    data = read_file(path)
    if data is None:
        return None
    try:
        return serialization.load_pem_public_key(data)
    except Exception as e:
        print(f"Ошибка загрузки публичного ключа: {e}")
        return None

def encrypt_symmetric_key(public_key, sym_key):
    """
    Шифрует симметричный ключ с помощью публичного RSA-ключа (OAEP).

    Входные данные:
        public_key: Публичный ключ RSA.
        sym_key (bytes): Симметричный ключ (16 байт).

    Выходные данные:
        bytes: Зашифрованный симметричный ключ.
    """
    return public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_symmetric_key(private_key, encrypted_key):
    """
    Расшифровывает симметричный ключ с помощью приватного RSA-ключа.

    Входные данные:
        private_key: Приватный ключ RSA.
        encrypted_key (bytes): Зашифрованный симметричный ключ.

    Выходные данные:
        bytes: Расшифрованный симметричный ключ.
    """
    return private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )