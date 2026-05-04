import json

import argparse
import os
import re
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


def parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',help='Запускает режим дешифрования')

    args = parser.parse_args()
    if args.generation is not None:
        return gen_logic()
    elif args.encryption is not None:
    # шифруем
    else:
    # дешифруем

def json_parser() -> dict:
    try:
        with open("settings.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def get_symmetric_key(byt:int) -> bytes:
    """ключ для симметричного алгоритма"""
    key = os.urandom(byt)
    return key

def get_asymmetric_key() -> bytes:
    """ключ для ассиметричного алгоритма"""
    keys = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
    )
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key

def write_symmetric_key(symmetric_key: bytes, symmetric_path:str) -> None:
    """сериализация ссиметричного ключа в файл"""
    try:
        with open(symmetric_path, 'wb') as key_file:
            key_file.write(symmetric_key)
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def write_asymmetric_key(public_key:RSAPublicKey, private_key:RSAPrivateKey, public_path:str, private_path:str) -> None:
    """сериализация ассиметричных ключей в файл"""
    try:
        with open(public_path, 'wb') as public_out:
                public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo))
        with open(private_path, 'wb') as private_out:
                private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()))
    except Exception as ex:
        print(f"Ошибка!: {ex}")
            
def encrypt_symmetric_key(symmetric_key: bytes, public_key: RSAPublicKey) -> bytes:
    encrypted_key = public_key.encrypt(symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return encrypted_key

def gen_logic() -> tuple:
    print("Мастер генерации ключей")
    print("Ключ для 3DES алгоритма будет зашифрован с помощью RSA-OAEP")
    print("Возможная длинна ключа шифрования(в битах): 64, 128, 192")
    key_length = int(input("Выберите длинну ключа:"))
    while(key_length != 64 and key_length != 128 and key_length != 192):
        key_length = int(input("Выберите значения из списка!\n Ваш выбор:"))
    symmetric_key = get_symmetric_key(key_length // 8)
    private_key, public_key = get_asymmetric_key()
    encrypted_key = encrypt_symmetric_key(symmetric_key, public_key)
    print("Хотите использовать стандартные параметры сериализации ключей?")
    action = int(input("1 - Да=\n 2 - Нет\n Выбор:"))
    while(action != 1 and action != 2):
        action = int(input("Выберите вариант из списка!:"))
    if action == 2:
        symmetric_key_path = str(input("Введите путь(имя) файла для сохранения 3DES ключа:"))
        write_symmetric_key(encrypted_key, symmetric_key_path)
        public_key_path = str(input("Введите путь(имя) файла для сохранения RSAPublic ключа:"))
        private_key_path = str(input("Введите путь(имя) файла для сохранения RSAPrivate ключа:"))
        write_asymmetric_key(public_key, private_key, public_key_path, private_key_path)
        return symmetric_key, public_key, private_key
    else:
        settings = json_parser()
        write_symmetric_key(encrypted_key, settings["symmetric_key_path"])
        write_asymmetric_key(public_key, private_key, settings["public_key_path"], settings["private_key_path"])
        return symmetric_key, public_key, private_key