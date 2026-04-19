from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
import os


def generate_rsa_keys():
    """
    Генерирует пару RSA ключей.

    :return: (private_key, public_key)
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def save_private_key(private_key, path: str) -> None:
    """
    Сохраняет приватный ключ в файл.

    :param private_key: объект приватного ключа
    :param path: путь к файлу
    """
    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def save_public_key(public_key, path: str) -> None:
    """
    Сохраняет публичный ключ в файл.

    :param public_key: объект публичного ключа
    :param path: путь к файлу
    """
    with open(path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def load_private_key(path: str):
    """
    Загружает приватный ключ из файла.

    :param path: путь к файлу
    :return: объект приватного ключа
    """
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


# --- RSA (пример из методички) --- #


def rsa_encrypt_text(public_key, text: bytes) -> bytes:
    """
    Шифрует текст с помощью RSA (как в методичке).

    :param public_key: публичный ключ
    :param text: байтовая строка
    :return: зашифрованный текст (bytes)
    """
    return public_key.encrypt(
        text,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt_text(private_key, ciphertext: bytes) -> bytes:
    """
    Расшифровывает текст RSA.

    :param private_key: приватный ключ
    :param ciphertext: зашифрованные данные
    :return: исходный текст (bytes)
    """
    return private_key.decrypt(
        ciphertext,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def generate_idea_key() -> bytes:
    """
    Генерирует ключ IDEA (128 бит).

    :return: случайный ключ (16 байт)
    """
    return os.urandom(16)


def encrypt_key(public_key, sym_key: bytes) -> bytes:
    """
    Шифрует симметричный ключ RSA.

    :param public_key: публичный ключ
    :param sym_key: симметричный ключ
    :return: зашифрованный ключ
    """
    return public_key.encrypt(
        sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_key(private_key, enc_key: bytes) -> bytes:
    """
    Расшифровывает симметричный ключ RSA.

    :param private_key: приватный ключ
    :param enc_key: зашифрованный ключ
    :return: исходный симметричный ключ
    """
    return private_key.decrypt(
        enc_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def encrypt_data(key: bytes, data: bytes) -> bytes:
    """
    Шифрует данные алгоритмом IDEA.

    :param key: симметричный ключ
    :param data: исходные данные
    :return: зашифрованные данные (iv + ciphertext)
    """
    iv = os.urandom(8)

    padder = padding.PKCS7(64).padder()
    padded = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    return iv + encryptor.update(padded) + encryptor.finalize()


def decrypt_data(key: bytes, data: bytes) -> bytes:
    """
    Расшифровывает данные IDEA.

    :param key: симметричный ключ
    :param data: зашифрованные данные
    :return: исходные данные
    """
    iv = data[:8]
    ciphertext = data[8:]

    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(64).unpadder()
    return unpadder.update(padded) + unpadder.finalize()
