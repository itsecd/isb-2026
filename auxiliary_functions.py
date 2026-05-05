import os
import sys
import json

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

def decrypt_symmetric_key(settings):
    """Расшифровывает симметричный ключ."""
    private_key_pem = read_file(settings['private_key'])
    if private_key_pem is None:
        return None
    
    encrypted_key_data = read_file(settings['symmetric_key_encrypted'])
    if encrypted_key_data is None:
        return None

    try:
        private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        return private_key.decrypt(
            encrypted_key_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        print(f"Ошибка расшифровки симметричного ключа: {e}")
        return None