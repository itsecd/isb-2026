import json

import argparse
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


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
        return enc_logic()
    else:
        return dec_logic()

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

def read_symmetric_key(symmetric_key_path:str) -> bytes:
    """чтение ключа из файла"""
    try:
        with open(symmetric_key_path, mode='rb') as key_file: 
            key = key_file.read()
            return key
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def read_asymmetric_key(public_key_path:str, private_key_path) -> tuple:
    """чтение RSA ключей из файлов"""
    try:
        with open(public_key_path, 'rb') as pem_in:
            public_bytes = pem_in.read()
            public_key = load_pem_public_key(public_bytes)
        with open(private_key_path, 'rb') as pem_in:
            private_bytes = pem_in.read()
            private_key = load_pem_private_key(private_bytes,password=None,)
        return public_key, private_key
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def read_text(initial_file_path:str) -> bytes:
    """чтение текста из файла"""
    try:
        with open(initial_file_path, 'rb') as f:
            return f.read()
    except Exception as ex:
        print(f"Ошибка!: {ex}")
        return b""
    
def write_text(text: bytes,  enc_file_path: str) -> None:
    """запись расшифрованного текста в файл"""
    try:
        with open(enc_file_path, 'wb') as f:
            f.write(text)
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def encrypt_symmetric_key(symmetric_key: bytes, public_key: RSAPublicKey) -> bytes:
    """шифрование ключа с помощью RSA-OAEP"""
    encrypted_key = public_key.encrypt(symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return encrypted_key

def decrypt_symmetric_key(encrypted_key: bytes, private_key: RSAPrivateKey) -> bytes:
    """дешифровка ключа"""
    return private_key.decrypt(encrypted_key,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

def padding_text(text:bytes) ->bytes:
    """паддинг текста под стандарты 3DES"""
    padder = sym_padding.ANSIX923(64).padder()
    padded_text = padder.update(text)+padder.finalize()
    return padded_text

def encrypt_text(text:bytes, symmetric_key:bytes) -> bytes:
    """шифрование текста помощью алгоритма 3DES"""
    iv = os.urandom(8) 
    cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_text = padding_text(text)
    encrypted_text = encryptor.update(padded_text) + encryptor.finalize()
    return iv + encrypted_text

def decrypt_text(encrypted_data: bytes, symmetric_key: bytes) -> str:
    """Дешифровка и удаление паддинга"""
    try:
        iv = encrypted_data[:8]
        ciphertext = encrypted_data[8:]
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_text = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = sym_padding.ANSIX923(64).unpadder()
        unpadded_text = unpadder.update(padded_text) + unpadder.finalize()
        return unpadded_text
    except Exception as ex:
        print(f"Ошибка!: {ex}")
        return ""

def gen_logic() -> tuple:
    """консольный интерфейс"""
    print("Мастер генерации ключей")
    print("Ключ для 3DES алгоритма будет зашифрован с помощью RSA-OAEP")
    print("Возможная длинна ключа шифрования(в битах): 64, 128, 192")
    key_length = int(input("Выберите длинну ключа:"))
    while(key_length != 64 and key_length != 128 and key_length != 192):
        key_length = int(input("Выберите значения из списка!\n Ваш выбор:"))
    symmetric_key = get_symmetric_key(key_length // 8)
    private_key, public_key = get_asymmetric_key()
    encrypted_key = encrypt_symmetric_key(symmetric_key, public_key)
    print("Ключи успешно сгенерированы")
    print("Хотите использовать стандартные параметры сериализации ключей?")
    action = str(input("Да\Нет"))
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        print("Хотите использовать стандартные параметры сериализации ключей?")
        action = str(input("Да\Нет"))
    if action == "Нет" or action == "нет":
        symmetric_key_path = str(input("Введите путь(имя) файла для сохранения 3DES ключа:"))
        write_symmetric_key(encrypted_key, symmetric_key_path)
        public_key_path = str(input("Введите путь(имя) файла для сохранения RSAPublic ключа:"))
        private_key_path = str(input("Введите путь(имя) файла для сохранения RSAPrivate ключа:"))
        write_asymmetric_key(public_key, private_key, public_key_path, private_key_path)
        print("Ключи успешно сохранены")
        return symmetric_key, public_key, private_key
    else:
        settings = json_parser()
        write_symmetric_key(encrypted_key, settings["symmetric_key_path"])
        write_asymmetric_key(public_key, private_key, settings["public_key_path"], settings["private_key_path"])
        print("Ключи успешно сохранены")
        return symmetric_key, public_key, private_key

def enc_logic():
    """консольный интерфейс"""
    settings = json_parser()
    print("Мастер шифровки текста")
    action = str(input("Желаете сгенерировать ключи шифрования?(Да\Нет)"))
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Желаете сгенерировать ключи шифрования?(Да\Нет)"))
    if action == "Да" or action == "да":
        symmetric_key, public_key, private_key = gen_logic()
    else:
        action = str(input("Ключи записаны в стандартные директории?(Да\Нет):"))
        while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
            action = str(input("Ключи записаны в стандартные директории?(Да\Нет):"))
        if action == "Да" or action == "да":
            symmetric_key = read_symmetric_key(settings["symmetric_key_path"])
            public_key, private_key = read_asymmetric_key(settings["public_key_path"], settings["private_key_path"])
            symmetric_key = decrypt_symmetric_key(symmetric_key, private_key)
            print("Ключи успешно загружены")
        else:
            symmetric_key_path = str(input("Введите путь(имя) файла 3DES ключа:"))
            symmetric_key = read_symmetric_key(symmetric_key_path)
            public_key_path = str(input("Введите путь(имя) файла для сохранения RSAPublic ключа:"))
            private_key_path = str(input("Введите путь(имя) файла для сохранения RSAPrivate ключа:"))
            public_key, private_key = read_asymmetric_key(public_key_path, private_key_path)
            symmetric_key = decrypt_symmetric_key(symmetric_key, private_key)
            print("Ключи успешно загружены")
    action = str(input("Текст записаны в стандартные директории?(Да\Нет):"))
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Ключи записаны в стандартные директории?(Да\Нет):"))
    if action == "Да" or action == "да":
        text = read_text(settings["initial_file_path"])
    else:
        initial_file_path = str(input("Введите путь(имя) к тексту:"))
        text = read_text(initial_file_path)
    enc_text = encrypt_text(text, symmetric_key)
    print("Текст успешно зашифрован")
    action = str(input("Записать хашифрованный текст в стандартные директории?(Да\Нет):"))
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Записать хашифрованный текст в стандартные директории?:"))
    if action == "Да" or action == "да":
        write_text(enc_text, settings["encrypted_file_path"])
    else:
        enc_path = str(input("Введите путь(имя) файла для сохранения зашифрованного сообщения:"))
        write_text(enc_text, enc_path)
    return enc_text, symmetric_key
    

def dec_logic():
    """консольный интерфейс"""
    settings = json_parser()
    print("Мастер дешифровки текста")
    action = str(input("Ключи записаны в стандартные директории(Да\Нет)?"))
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Ключи записаны в стандартные директории(Да\Нет)?"))
    if action == "Да" or action == "да":
        symmetric_key = read_symmetric_key(settings["symmetric_key_path"])
        public_key, private_key = read_asymmetric_key(settings["public_key_path"], settings["private_key_path"])
        symmetric_key = decrypt_symmetric_key(symmetric_key, private_key)
        print("Ключи успешно загружены")
    else:
        symmetric_key_path = str(input("Введите путь(имя) файла 3DES ключа:"))
        symmetric_key = read_symmetric_key(symmetric_key_path)
        public_key_path = str(input("Введите путь(имя) файла для сохранения RSAPublic ключа:"))
        private_key_path = str(input("Введите путь(имя) файла для сохранения RSAPrivate ключа:"))
        public_key, private_key = read_asymmetric_key(public_key_path, private_key_path)
        symmetric_key = decrypt_symmetric_key(symmetric_key, private_key)
        print("Ключи успешно загружены")
    action = str(input("Текст записаны в стандартные директории?(Да\Нет):"))
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Ключи записаны в стандартные директории?(Да\Нет):"))
    if action == "Да" or action == "да":
        text = read_text(settings["encrypted_file_path"])
    else:
        enc_path = str(input("Введите путь(имя) к тексту:"))
        text = read_text(enc_path)
    text = decrypt_text(text, symmetric_key)
    print("Текст успешно расшифрован")
    action = str(input("Записать расшифрованный текст в стандартные директории?(Да\Нет):"))
    while(action != "Да" and action != "Нет" and action != "да" and action != "нет"):
        action = str(input("Записать расшифрованный текст в стандартные директории?:"))
    if action == "Да" or action == "да":
        write_text(text, settings["decrypted_file_path"])
    else:
        enc_path = str(input("Введите путь(имя) файла для сохранения зашифрованного сообщения:"))
        write_text(text, enc_path)
    return text, symmetric_key


def main():
    parser()
    action = str(input("Выберите действие(enc/dec/gen/exit):"))
    while(action != "exit"):
        if action == "enc":
            enc_logic()
        elif action == "dec":
            dec_logic()
        elif action == "gen":
            gen_logic()
        action = str(input("Выберите действие(enc/dec/gen/exit):"))
    return 0

if __name__ == "__main__":
    main()