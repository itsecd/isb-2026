from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

from file_utils import read_bytes, write_bytes


def generate_rsa_keys() -> tuple:
    """Сгенерирование пары RSA-ключей длиной 2048 бит с экспонентой 65537.
    """
    keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key


def serialize_public_key(public_key, path: str) -> None:
    """Сериализование открытого ключа в PEM-файл.
    Args:
        public_key: Объект открытого RSA-ключа, который нужно сохранить.
        path: Путь к файлу, в который будет записан ключ в формате PEM.
    """
    write_bytes(path, public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))


def serialize_private_key(private_key, path: str) -> None:
    """Сериализование закрытого ключа в PEM-файл без шифрования.
    Args:
        private_key: Объект закрытого RSA-ключа, который нужно сохранить.
        path: Путь к файлу, в который будет записан ключ в формате PEM.
    """
    write_bytes(path, private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))


def deserialize_public_key(path: str):
    """Десериализование открытого ключа из PEM-файла.
    Args:
        path: Путь к PEM-файлу с открытым RSA-ключом.
    """
    return load_pem_public_key(read_bytes(path))


def deserialize_private_key(path: str):
    """Десериализование закрытого ключа из PEM-файла.
    Args:
        path: Путь к PEM-файлу с закрытым RSA-ключом.
    """
    return load_pem_private_key(read_bytes(path), password=None)


def oaep():
    """Настройки паддинга OAEP для RSA с SHA-256.
    """
    return asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )


def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """Зашифровка данных открытым RSA-ключом с OAEP-паддингом.
    Args:
        data: Байтовые данные, которые нужно зашифровать.
        public_key: Объект открытого RSA-ключа.
    """
    return public_key.encrypt(data, oaep())


def decrypt_with_private_key(data: bytes, private_key) -> bytes:
    """Расшифровка данных закрытым RSA-ключом с OAEP-паддингом.
    Args:
        data: Зашифрованные байтовые данные.
        private_key: Объект закрытого RSA-ключа.
    """
    return private_key.decrypt(data, oaep())


def load_symmetric_key(path_secret_key: str, path_symmetric_key: str) -> bytes:
    """Загрузка закрытого RSA-ключа и расшифровка им симметричного ключа Camellia.
    Args:
        path_secret_key: Путь к PEM-файлу с закрытым RSA-ключом.
        path_symmetric_key: Путь к файлу с зашифрованным симметричным ключом Camellia.
    """
    print("Загрузка закрытого ключа.")
    private_key = deserialize_private_key(path_secret_key)

    print("Расшифровка симметричного ключа.")
    encrypted_sym_key = read_bytes(path_symmetric_key)
    symmetric_key = decrypt_with_private_key(encrypted_sym_key, private_key)
    print(f"Симметричный ключ получен ({len(symmetric_key) * 8} бит).")

    return symmetric_key