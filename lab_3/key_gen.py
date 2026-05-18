import os

from AES import save_symmetric_key
from RSA import (
    generate_rsa_pair,
    save_rsa_keys,
)


def generate_and_save_keys(lenght: int, public_pem: str, private_pem: str, symmetric_path: str):
    """
    Генерирует и сохраняет тройку ключей(симметричный и публичный + приватный для RSA)

    Аргументы:
        lenght: длина симметричного ключа
        public_pem: путь для сохранения публичного ключа
        private_pem: путь для сохранения приватного ключа
        symmetric_path: путь сохранения симметричного ключа
    """
    try:
        private_key, public_key = generate_rsa_pair()
        symmetric_key = os.urandom(lenght // 8)
        save_rsa_keys(public_key, public_pem, private_key, private_pem)
        save_symmetric_key(symmetric_key, symmetric_path, public_key)
    except PermissionError:
        raise PermissionError
    except FileNotFoundError:
        raise FileNotFoundError
    except Exception as e:
        raise e
