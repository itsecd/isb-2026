import os
from typing import Dict, Any
from cryptography.hazmat.primitives import serialization, padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from utils import get_asym_padding

def encrypt_data(settings: Dict[str, Any]) -> None:
    """Выполняет гибридное шифрование текстового файла.

    Расшифровывает сессионный ключ Camellia с помощью закрытого ключа RSA,
    дополняет исходный текст паддингом ANSIX923 и шифрует его в режиме CBC.
    Вектор инициализации (IV) сохраняется в первые 16 байт итогового файла.

    Args:
        settings (Dict[str, Any]): Конфигурационный словарь с путями к файлам.
    """
    print("Запуск режима шифрования...")
    
    try:
        with open(settings['secret_key'], 'rb') as pem_in:
            private_bytes = pem_in.read()
        private_key = serialization.load_pem_private_key(private_bytes, password=None)
    except FileNotFoundError:
        print(f"Файл {settings['secret_key']} не найден!")
        return
    
    try:
        with open(settings['symmetric_key'], 'rb') as sym_in:
            enc_sym_key = sym_in.read()
        
        sym_key = private_key.decrypt(enc_sym_key, get_asym_padding())
        print("Симметричный ключ успешно расшифрован.")
    except FileNotFoundError:
        print(f"Файл {settings['symmetric_key']} не найден!")
        return
    
    try:
        with open(settings['initial_file'], 'rb') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Файл {settings['initial_file']} не найден!")
        return

    padder = sym_padding.ANSIX923(128).padder() 
    padded_text = padder.update(text) + padder.finalize()

    iv = os.urandom(16) 
    cipher = Cipher(algorithms.Camellia(sym_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()

    try:
        with open(settings['encrypted_file'], 'wb') as f:
            f.write(iv + c_text)
        
        print(f"Данные зашифрованы алгоритмом Camellia (с IV) и сохранены в: {settings['encrypted_file']}.")
        print("Шифрование завершено!\n")
    except IOError as e:
        print(f"Ошибка при сохранении зашифрованного файла: {e}")