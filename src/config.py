import os
import json
from typing import Dict, Any

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


def manage_settings(settings: Dict[str, str] = None) -> Dict[str, str]:
    """
    Загружает или сохраняет настройки в файл settings.json.
    
    Если settings не передан - загружает настройки из файла.
    Если файла настроек нет - создаёт его с пустыми настройками.
    Если settings передан - сохраняет их в файл.
    
    Args:
        settings (Dict[str, str], optional): Настройки для сохранения.
            Если None, выполняется загрузка настроек.
    
    Returns:
        Dict[str, str]: Загруженные настройки (при загрузке) или 
            пустой словарь (при сохранении)
    
    Raises:
        json.JSONDecodeError: Если файл настроек повреждён
        IOError: Если нет прав на запись/чтение файла
    """
    settings_file = 'settings.json'
    
    if settings is not None:
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        print(" Настройки сохранены в settings.json")
        return {}
    
    if not os.path.exists(settings_file):
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
        print(f" Создан пустой файл настроек: {settings_file}")
        print(" Пожалуйста, заполните настройки вручную или через режим 4")
        return {}
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        return json.load(f)