import os
import sys
import json
import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding

def read_json(path):
    """Читает файл с настройками."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
    except Exception as e:
        print(f"Ошибка чтения {path}: {e}")
    return None

def read_file(path):
    """Читает файл."""
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден: {path}")
    except Exception as e:
        print(f"Ошибка чтения файла {path}: {e}")
    return None

def write_file(path, data):
    """Записывает данные в файл. Создает директории при необходимости."""
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Ошибка записи файла {path}: {e}")
    return False

def load_settings(settings_path='settings.json'):
    """Загружает файл с настройками."""
    settings = read_json(settings_path)
    if settings is None:
        sys.exit(1)
    return settings

def generate_keys(settings):
    """Генерирует ключи и сохраняет их."""

    symmetric_key = os.urandom(settings['BLOCK_SIZE_BYTES'])
    print(f"Симметричный ключ SEED сгенерирован.")

    private_key = rsa.generate_private_key(
        public_exponent=settings['public_exponent'],
        key_size=settings['key_size'],
        backend=default_backend()
    )
    public_key = private_key.public_key()
    print("Пара асимметричных ключей сгенерирована.")

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    if not write_file(settings['private_key'], private_key_bytes):
        return
    print(f"Закрытый ключ сохранен в: {settings['private_key']}")

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    if not write_file(settings['public_key'], public_key_bytes):
        return
    print(f"Открытый ключ сохранен в: {settings['public_key']}")

    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    if not write_file(settings['symmetric_key_encrypted'], encrypted_symmetric_key):
        return
    print(f"Зашифрованный симметричный ключ сохранен в: {settings['symmetric_key_encrypted']}")

    print("Генерация ключей завершена")

def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gen', action='store_true', help='Генерация ключей')
    
    parser.add_argument('--settings', type=str, default='settings.json', help='Путь к файлу настроек JSON')

    args = parser.parse_args()
    settings = load_settings(args.settings)

    match True:
        case _ if args.gen:
            generate_keys(settings)

if __name__ == '__main__':
    main()