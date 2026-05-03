from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from file_utils import  write_binary_file, read_binary_file

def generate_rsa_key() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """
    Генерирует пару RSA-ключей.

    :return: закрытый и открытый RSA-ключи
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    public_key=private_key.public_key()

    return private_key, public_key

def save_public_key(public_key: rsa.RSAPublicKey, public_key_path: str) -> None:
    """
    Сохраняет открытый RSA-ключ.

    :param public_key: открытый RSA-ключ
    :param public_key_path: путь для сохранения открытого ключа
    :return: None
    """
    with open(public_key_path, "wb") as public_file:
        public_file.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

def save_private_key(private_key: rsa.RSAPrivateKey, private_key_path: str) -> None:
    """
    Сохраняет закрытый RSA-ключ.
    
    :param private_key: закрытый RSA-ключ
    :param private_key_path: путь для сохранения закрытого ключа
    :return: None
    """
    with open(private_key_path, "wb") as private_file:
        private_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
            )
        )

def load_private_key(private_key_path: str) -> rsa.RSAPrivateKey:
    """
    Загружает закрытый RSA-ключ.

    :param private_key_path: путь к файлу закрытого ключа
    :return: закрытый RSA-ключ
    """
    try:
        private_key_data = read_binary_file(private_key_path)

        private_key = load_pem_private_key(private_key_data,password=None)

        return private_key

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Файл закрытого ключа не найден: {private_key_path}"
        )


def load_public_key(public_key_path: str) -> rsa.RSAPublicKey:
    """
    Загружает открытый RSA-ключ.

    :param public_key_path: путь к файлу открытого ключа
    :return: открытый RSA-ключ
    """
    with open(public_key_path, "rb") as public_file:
        public_key_data = public_file.read()

    public_key = load_pem_public_key(public_key_data)

    return public_key


def encrypt_symmetric_key(symmetric_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """
    Шифрует AES-ключ открытым RSA-ключом.

    :param symmetric_key: симметричный AES-ключ
    :param public_key: открытый RSA-ключ
    :return: зашифрованный AES-ключ
    """
    encrypt_symmetric_key = public_key.encrypt(symmetric_key,
                                               asymmetric_padding.OAEP(
                                                   mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                                                   algorithm=hashes.SHA256(),
                                                   label=None
                                               )
                                            )
    
    return encrypt_symmetric_key

def decrypt_symmetric_key(encrypted_symmetric_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    """
    Расшифровывает AES-ключ закрытым RSA-ключом.

    :param encrypted_symmetric_key: зашифрованный AES-ключ
    :param private_key: закрытый RSA-ключ
    :return: расшифрованный AES-ключ
    """
    symmetric_key = private_key.decrypt(encrypted_symmetric_key,
                                        asymmetric_padding.OAEP(
                                            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                                            algorithm=hashes.SHA256(),
                                            label=None
                                        )
                                    )
    
    return symmetric_key


def save_encrypted_symmetric_key(encrypted_key: bytes,symmetric_key_path: str) -> None:
    """
    Сохраняет зашифрованный AES-ключ.

    :param encrypted_key: зашифрованный симметричный ключ
    :param symmetric_key_path: путь для сохранения ключа
    :return: None
    """
    try:
        write_binary_file(symmetric_key_path, encrypted_key)

    except OSError as error:
        raise OSError(
            f"Ошибка сохранения зашифрованного симметричного ключа: {symmetric_key_path}"
        ) from error