from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)


def generate_rsa_pair():
    """
    Генерирует пару ключей RSA, возвращает приватный и публичный ключи

    """
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key


def save_rsa_keys(public_key: bytes, public_pem: str, private_key: bytes, private_pem: str):
    """
    Сохраняет пару ключей RSA в файлы

    Аргументы:
        public_key: публичный ключ
        public_pem: путь для сохранения публичного ключа
        private_key: приватный ключ
        private_pem: путь для сохранения приватного ключа
    """
    try:
        with open(public_pem, "wb") as public_out:
            public_out.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
    except PermissionError:
        print("Недостаточно прав для сохранения файла публичного ключа (смените путь)")
        raise PermissionError
    except Exception as e:
        raise e

    try:
        with open(private_pem, "wb") as private_out:
            private_out.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
    except PermissionError:
        print("Недостаточно прав для сохранения приватного ключа")
        raise PermissionError
    except Exception as e:
        raise e


def load_rsa_public(public_pem: str):
    """
    Загружает публичный ключ из файла

    Аргумент:
        public_pem: путь до публичного ключа
    """
    try:
        with open(public_pem, "rb") as pem_in:
            public_bytes = pem_in.read()
            return load_pem_public_key(public_bytes)
    except PermissionError:
        print("Недостаточно прав для чтения публичного ключа")
        raise PermissionError
    except FileNotFoundError:
        print("Не найден файл с публичным ключом")
        raise FileNotFoundError
    except Exception as e:
        raise e


def load_rsa_private(private_pem: str):
    """
    Загружает приватный ключ из файла

    Аргумент:
        private_pem: путь до приватного файла
    """
    try:
        with open(private_pem, "rb") as pem_in:
            private_bytes = pem_in.read()
            return load_pem_private_key(
                private_bytes,
                password=None,
            )
    except PermissionError:
        print("Недостаточно прав для чтения приватного ключа")
        raise PermissionError
    except FileNotFoundError:
        print("Не найден файл с приватным ключом")
        raise FileNotFoundError
    except Exception as e:
        raise e


def rsa_encrypt(text: str, public_key: bytes):
    """
    Шифрует данные с помощью RSA

    Аргументы:
        text: исходные данные
        public_key: публичный ключ
    """
    c_text = public_key.encrypt(
        text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return c_text


def rsa_decrypt(c_text: str, private_key: bytes):
    """
    Дешифрует данные с помощью RSA

    Аргументы:
        c_text: зашифрованные данные
        private_key: приватный ключ
    """
    dc_text = private_key.decrypt(
        c_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return dc_text
