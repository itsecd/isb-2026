import os
import json

DEFAULT_SETTINGS = {
    'initial_file': 'data/plaintext.txt',
    'encrypted_file': 'data/encrypted.bin',
    'decrypted_file': 'data/decrypted.txt',
    'symmetric_key': 'keys/symmetric.key',
    'encrypted_symmetric_key': 'keys/encrypted_symmetric.key',
    'public_key': 'keys/public.pem',
    'private_key': 'keys/private.pem'
}

BLOCK_SIZE = 16  # 128 бит для Camellia
SYMMETRIC_KEY_SIZE = 32  # 256 бит для Camellia
RSA_KEY_SIZE = 2048
RSA_PUBLIC_EXPONENT = 65537

HELP_DESCRIPTION = 'Гибридная криптосистема (RSA + Camellia) - Лабораторная работа №3'
HELP_EPILOG = '''
Примеры использования:

  # Генерация ключей
  python main.py --gen --public keys/public.pem --private keys/private.pem --symmetric keys/symmetric.key

  # Шифрование данных
  python main.py --enc --input data/plaintext.txt --private keys/private.pem --encrypted-symmetric keys/encrypted_symmetric.key

  # Дешифрование данных
  python main.py --dec --input data/encrypted.bin --private keys/private.pem --encrypted-symmetric keys/encrypted_symmetric.key

  # Интерактивный режим
  python main.py --interactive
'''


def load_settings():
    """Загрузка настроек из settings.json"""
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4, ensure_ascii=False)
        print(" Создан файл настроек: settings.json")
        return DEFAULT_SETTINGS.copy()
    
    with open('settings.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def save_settings(settings):
    """Сохранение настроек в settings.json"""
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
    print(" Настройки сохранены в settings.json")