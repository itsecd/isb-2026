import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def generate_symmetric_key():
    """
    генерация ключа для симметричного алгоритма

    аргументы: нету
    возвращает: ключ: 16 случайных байт
    """

    key = os.urandom(16)
    return key


def generate_asymmetric_keys():
    """
    генерация ключей для асимметричного алгоритма

    аргументы: никаких
    возвращает: 
            tuple(private_key, public_key): кортеж с объектами классов RSAPrivateKey и RSAPublicKey
    """

    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key


def write_public_key(public_key, public_pem):
    """
    добавление открытого ключа в файл
    аргументы:
            public_key: объект класса RSAPublicKey
            public_pem: путь к файлу, в который содержится публичный ключ
    возвращает: ничего
    """

    with open(public_pem, 'wb') as public_out:
        public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo))


def write_private_key(private_key, private_pem):
    """
    запись закрытого ключа в файл
    аргументы:
            private_key: объект класса RSAPrivateKey
            private_pem: путь к файлу, в который сериализован закрытый ключ, в виде строки
    возвращает: -
    """

    with open(private_pem, 'wb') as private_out:
        private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
              format=serialization.PrivateFormat.TraditionalOpenSSL,
              encryption_algorithm=serialization.NoEncryption()))


def encrypt_symmetric_key(key, public_key):
    """
    шифрование симметричного ключа шифрования с помощью открытого ключа

    аргументы:
            ключ: 16 случайных байт
            public_key: объект класса RSAPublicKey
    возвращает:
            encrypt_key: байты зашифрованного симметричного ключа
    """

    encrypt_key = public_key.encrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return encrypt_key


def write_symmetric_key(encrypt_key, file_name):
    """
    запись ключа симметричного алгоритма шифрования в файл
    аргументы: 
            encrypt_key: байты зашифрованного симметричного ключа
            file_name: путь к файлу, в который сериализован ключ шифрования, в виде строки
    возвращает: -
    """
    
    with open(file_name, 'wb') as key_file:
        key_file.write(encrypt_key)


def read_symmetric_key(symmetric_key_file):
    """
    считывание зашифрованного симметричного ключа из файла

    аргументы: 
            symmetric_key_file: путь к файлу, в котором хранится зашифрованный симметричный ключ
    возвращает:
            содержимое: байты зашифрованного симметричного ключа
    """
    try:
        with open(symmetric_key_file, 'rb') as key_file: 
                content = key_file.read()
        return content
    
    except FileNotFoundError:
        raise FileNotFoundError(f"{symmetric_key_file} такой файл не найден")


def read_private_pem(private_pem):
    """
    считывание закрытого ключа из файла

    аргументы: 
            private_pem: путь к файлу с закрытым ключом,
    возвращает:
            d_private_key: объект класса RSAPrivateKey
    """

    try:
        with open(private_pem, 'rb') as pem_in:
                private_bytes = pem_in.read()
        d_private_key = load_pem_private_key(private_bytes,password=None,)
        return d_private_key
    
    except FileNotFoundError:
        raise FileNotFoundError(f"{private_pem} нет такого файла")


def decrypt_symmetric_key(content, d_private_key):
    """
    при помощи закрытого ключа расшифровывает симметричный ключ, зашифрованный с помощью открытого ключа
    аргументы: 
            content: байты зашифрованного симметричного ключа
            d_private_key: объект класса RSAPrivateKey
    возвращает:
            dc_key: расшифрованный симметричный ключ в виде 16 байт
    """

    dc_key = d_private_key.decrypt(content,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return dc_key
