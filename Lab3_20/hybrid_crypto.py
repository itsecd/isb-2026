# crypto_core.py
import os
import json
import sys
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def load_settings(path):
    """
    Загружает настройки из JSON файла и проверяет наличие всех необходимых полей.
    
    Параметры:
        path (str): путь к файлу настроек settings.json
        
    Возвращает:
        dict: словарь с загруженными настройками
        
    Исключения:
        SystemExit: при ошибках чтения файла или отсутствии обязательных полей
    """
    try:
        with open(path) as f:
            s = json.load(f)
        # проверяем, что поля есть
        need = [
            "initial_file",
            "encrypted_file",
            "decrypted_file",
            "symmetric_key_encrypted",
            "public_key",
            "private_key"
        ]
        for n in need:
            if n not in s:
                raise ValueError(f"В {path} нет поля {n}")
        return s
    except FileNotFoundError:
        print(f" {path} не найден, проверь путь")
        sys.exit(1)
    except json.JSONDecodeError:
        print(" JSON кривой")
        sys.exit(1)
    except ValueError as e:
        print(f"[!] {e}")
        sys.exit(1)


def read_binary_file(file_path):
    """
    Читает данные из бинарного файла.
    
    Параметры:
        file_path (str): путь к файлу для чтения
        
    Возвращает:
        bytes: содержимое файла в виде байтов
    """
    with open(file_path, 'rb') as f:
        return f.read()


def write_binary_file(file_path, data):
    """
    Записывает байтовые данные в бинарный файл.
    
    Параметры:
        file_path (str): путь к файлу для записи
        data (bytes): данные для записи
    """
    with open(file_path, 'wb') as f:
        f.write(data)


def generate_camellia_key(key_size_bits):
    """
    Генерирует случайный ключ для Camellia заданного размера.
    
    Параметры:
        key_size_bits (int): размер ключа в битах (128, 192 или 256)
        
    Возвращает:
        bytes: сгенерированный ключ длиной key_size_bits/8 байт
    """
    print(f" Генерируем Camellia {key_size_bits} бит")
    return os.urandom(key_size_bits // 8)


def generate_rsa_keys():
    """
    Генерирует пару RSA ключей размером 2048 бит с публичной экспонентой 65537.
    
    Возвращает:
        tuple: (приватный ключ, публичный ключ) в формате объектов cryptography
    """
    print(" Генерируем RSA-2048")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()


def save_rsa_keys(private_key, public_key, private_path, public_path):
    """
    Сохраняет RSA ключи в PEM файлы без шифрования.
    
    Параметры:
        private_key: приватный ключ RSA
        public_key: публичный ключ RSA
        private_path (str): путь для сохранения приватного ключа
        public_path (str): путь для сохранения публичного ключа
    """
    print(" Сохраняем RSA ключи в файлы")
    os.makedirs(os.path.dirname(private_path), exist_ok=True)
    os.makedirs(os.path.dirname(public_path), exist_ok=True)

    with open(private_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(public_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def encrypt_symmetric_key(sym_key, public_key, output_path):
    """
    Шифрует симметричный ключ с помощью RSA-OAEP (SHA256).
    
    Параметры:
        sym_key (bytes): симметричный ключ для шифрования
        public_key: публичный ключ RSA для шифрования
        output_path (str): путь для сохранения зашифрованного ключа
    """
    print(" Шифруем симметричный ключ через RSA-OAEP ")
    enc = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    write_binary_file(output_path, enc)


def decrypt_symmetric_key(private_key, encrypted_key_path):
    """
    Расшифровывает симметричный ключ с помощью RSA-OAEP.
    
    Параметры:
        private_key: приватный ключ RSA для расшифровки
        encrypted_key_path (str): путь к файлу с зашифрованным ключом
        
    Возвращает:
        bytes: расшифрованный симметричный ключ
    """
    print(" Расшифровываем симметричный ключ обратно")
    data = read_binary_file(encrypted_key_path)
    return private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def encrypt_file_content(input_path, output_path, key):
    """
    Шифрует файл с помощью Camellia в режиме CBC с PKCS7 паддингом.
    IV (16 байт) записывается в начало выходного файла.
    
    Параметры:
        input_path (str): путь к исходному файлу
        output_path (str): путь для сохранения зашифрованного файла
        key (bytes): ключ Camellia (16/24/32 байта для 128/192/256 бит)
    """
    print(" Шифруем файл Camellia-CBC ")

    plain = read_binary_file(input_path)

    padder = sym_padding.PKCS7(128).padder()
    padded = padder.update(plain) + padder.finalize()

    iv = os.urandom(16)

    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    enc = cipher.encryptor()
    ciphertext = enc.update(padded) + enc.finalize()

    write_binary_file(output_path, iv + ciphertext)


def decrypt_file_content(input_path, output_path, key):
    """
    Расшифровывает файл, зашифрованный функцией encrypt_file_content.
    Извлекает IV из первых 16 байт, затем расшифровывает остальное.
    
    Параметры:
        input_path (str): путь к зашифрованному файлу
        output_path (str): путь для сохранения расшифрованного файла
        key (bytes): ключ Camellia (должен совпадать с ключом шифрования)
    """
    print(" Расшифровываем файл")

    data = read_binary_file(input_path)

    iv = data[:16]
    ct = data[16:]

    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    dec = cipher.decryptor()
    padded_plain = dec.update(ct) + dec.finalize()

    unpadder = sym_padding.PKCS7(128).unpadder()
    plain = unpadder.update(padded_plain) + unpadder.finalize()

    write_binary_file(output_path, plain)


def generation_mode(settings, key_size):
    """
    Режим генерации: создает симметричный ключ Camellia, пару RSA ключей
    и сохраняет зашифрованный симметричный ключ.
    
    Параметры:
        settings (dict): словарь с настройками из JSON
        key_size (int): размер ключа Camellia в битах (128/192/256)
    """
    sym_key = generate_camellia_key(key_size)
    priv, pub = generate_rsa_keys()

    save_rsa_keys(priv, pub, settings["private_key"], settings["public_key"])
    encrypt_symmetric_key(sym_key, pub, settings["symmetric_key_encrypted"])

    print(" Всё сгенерировано (ключи + зашифрованный симметричный)")


def encryption_mode(settings):
    """
    Режим шифрования: загружает приватный ключ, расшифровывает симметричный ключ,
    затем шифрует исходный файл.
    
    Параметры:
        settings (dict): словарь с настройками из JSON
    """
    with open(settings["private_key"], 'rb') as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)

    sym = decrypt_symmetric_key(priv, settings["symmetric_key_encrypted"])

    encrypt_file_content(settings["initial_file"], settings["encrypted_file"], sym)
    print(" Файл зашифрован")


def decryption_mode(settings):
    """
    Режим расшифрования: загружает приватный ключ, расшифровывает симметричный ключ,
    затем расшифровывает зашифрованный файл.
    
    Параметры:
        settings (dict): словарь с настройками из JSON
    """
    with open(settings["private_key"], 'rb') as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)

    sym = decrypt_symmetric_key(priv, settings["symmetric_key_encrypted"])

    decrypt_file_content(settings["encrypted_file"], settings["decrypted_file"], sym)
    print(" Файл расшифрован, проверь результат")