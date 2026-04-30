import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from .utils import pad_data
from .key_generator import load_private_key
from .decryptor import decrypt_symmetric_key_with_rsa

def encrypt_data_with_camellia(data: bytes, key: bytes) -> tuple:
    """
    Шифрование данных алгоритмом Camellia 
    
    """
    iv = os.urandom(16)  
    
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    padded_data = pad_data(data, block_size=16)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted_data, iv


def run_encryption(input_file: str, private_key_path: str, 
                   encrypted_symmetric_key_path: str, output_file: str) -> None:
    """
    Запуск режима шифрования
    
    Входные параметры:
        1) путь к шифруемому текстовому файлу
        2) путь к закрытому ключу ассиметричного алгоритма
        3) путь к зашифрованному ключу симметричного алгоритма
        4) путь, по которому сохранить зашифрованный текстовый файл
    """
    print("\n" + "="*60)
    print("Режим 2: Шифрование данных системой")
    print("="*60)
    
    print("\n Расшифровка симметричного ключа")
    symmetric_key = decrypt_symmetric_key_with_rsa(encrypted_symmetric_key_path, private_key_path)
    print(f" Симметричный ключ получен (длина: {len(symmetric_key)} байт)")
    
    print(f"\n Чтение исходного файла: {input_file}")
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    print(f" Размер {len(plaintext)} байт")
    
    print("\n Шифрование данных алгоритмом Camellia ")
    encrypted_data, _ = encrypt_data_with_camellia(plaintext, symmetric_key)
    
    print(f"\n Сохранение зашифрованного файла: {output_file}")
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)
    
    print("\n" + "="*60)
    print(" Шифрование завершено!")
    print(f" Исходный файл: {input_file}")
    print(f" Зашифрованный файл: {output_file}")
    print("="*60)