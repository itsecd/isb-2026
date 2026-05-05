import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes



def generate_symmetric_key(size: int) -> bytes:
    """
    Генерация ключа для симметричного алгоритма AES.
    :param size: размер AES-ключа в битах, допустимые значения: 128, 192 или 256
    :return: сгенерированный симметричный AES-ключ в виде байтов
    """

    if size not in [128, 192, 256]:
        raise ValueError("Key size must be one of this: 128, 192, 256")
    key_size_in_bytes = size // 8
    aes_key = os.urandom(key_size_in_bytes)
    return aes_key


def generate_asymmetric_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    """
    Генерация пары ключей для асимметричного алгоритма RSA.
    :return: кортеж из закрытого и открытого RSA-ключей
    """

    keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key


def serialize_keys(public_key: RSAPublicKey, public_pem: str, private_key: RSAPrivateKey, private_pem: str) -> None:
    """
    Сериализация открытого и закрытого RSA-ключей в PEM-файлы.
    :param public_key: открытый RSA-ключ
    :param public_pem: путь для сохранения открытого RSA-ключа
    :param private_key: закрытый RSA-ключ
    :param private_pem: путь для сохранения закрытого RSA-ключа
    :return: не возвращается
    """

    with open(public_pem, "wb") as public_out:
        public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
             format=serialization.PublicFormat.SubjectPublicKeyInfo))
    with open(private_pem, 'wb') as private_out:
        private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
              format=serialization.PrivateFormat.TraditionalOpenSSL,
              encryption_algorithm=serialization.NoEncryption()))
    return



def encrypt_symmetric_key(key: bytes, public_key: RSAPublicKey, path: str) -> bytes:
    """
    Шифрование симметричного AES-ключа открытым RSA-ключом.
    :param key: симметричный AES-ключ в виде байтов
    :param public_key: открытый RSA-ключ для шифрования симметричного ключа
    :param path: путь для сохранения зашифрованного симметричного ключа
    :return: зашифрованный симметричный ключ в виде байтов
    """

    ciphertext = public_key.encrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    with open(path, 'wb') as out:
        out.write(ciphertext)
    return ciphertext


def run_scenario1(enc_path: str, public_key_path: str, private_key_path: str, size: int) -> None:
    """
    Запуск сценария генерации ключей.
    :param enc_path: путь для сохранения зашифрованного симметричного AES-ключа
    :param public_key_path: путь для сохранения открытого RSA-ключа
    :param private_key_path: путь для сохранения закрытого RSA-ключа
    :param size: размер AES-ключа в битах, допустимые значения: 128, 192 или 256
    :return: не возвращается
    """

    symmetric_key = generate_symmetric_key(size)
    private_key, public_key = generate_asymmetric_keys()
    serialize_keys(public_key, public_key_path, private_key, private_key_path)
    encrypt_symmetric_key(symmetric_key, public_key, enc_path)
    print(f"Scenario 1 completed successfully. Keys generated and saved to {public_key_path} and {private_key_path}. Encrypted symmetric key saved to {enc_path}.")
