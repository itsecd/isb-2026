import json
import os

CONFIG_FILE = "settings.json"

def _create_default_config(path: str) -> None:
    """
    Создаёт файл настроек с дефолтными значениями при первом запуске.
    """
    default_settings = {
        "public_key_path": "keys/public.pem",
        "private_key_path": "keys/private.pem",
        "enc_symmetric_key_path": "keys/aes_key.enc",
        "default_aes_key_size": 256,
        "default_input_file": "data/plaintext.txt",
        "default_encrypted_file": "data/encrypted.bin",
        "default_decrypted_file": "data/decrypted.txt"
    }
    with open(path, 'w') as f:
        json.dump(default_settings, f, indent=2)
    print(f"Создан файл настроек: {path}")

def save_settings(settings, path="settings.json"):
    """
    Сохраняет настройки в JSON-файл.
    """
    with open(path, 'w') as f:
        json.dump(settings, f, indent=2)

def load_settings(path="settings.json"):
    """
    Загружает настройки из JSON-файла.
    Если файл не найден, создаёт его с дефолтными значениями.
    """
    if not os.path.exists(path):
        _create_default_config(path)
    with open(path, 'r') as f:
        return json.load(f)