from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def generate_rsa_keys():
    """
    Генерирует пару RSA ключей

    Returns:
        tuple: (private_key, public_key)
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def save_private_key(private_key, path):
    """
    Сохраняет приватный ключ в файл

    Args:
        private_key: RSA приватный ключ
        path (str): путь к файлу
    """
    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def save_public_key(public_key, path):
    """
    Сохраняет публичный ключ

    Args:
        public_key: RSA публичный ключ
        path (str): путь к файлу
    """
    with open(path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def load_private_key(path):
    """
    Загружает приватный ключ

    Returns:
        private_key
    """
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def load_public_key(path):
    """
    Загружает публичный ключ

    Returns:
        public_key
    """
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def encrypt_key(public_key, key):
    """
    Шифрует симметричный ключ RSA

    Returns:
        bytes
    """
    return public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_key(private_key, encrypted_key):
    """
    Дешифрует симметричный ключ

    Returns:
        bytes
    """
    return private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
