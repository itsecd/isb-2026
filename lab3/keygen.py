import os
from typing import Dict, Any
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from utils import get_asym_padding

def generate_keys(settings: Dict[str, Any], key_size_bits: int = 256) -> None:
    """Генерирует ключи для гибридной системы и сериализует их на диск.

    Создает случайный симметричный ключ Camellia заданной длины и пару 
    ключей RSA (2048 бит). Зашифровывает ключ Camellia открытым ключом RSA.

    Args:
        settings (Dict[str, Any]): Конфигурационный словарь с путями к файлам.
        key_size_bits (int): Длина ключа Camellia в битах (128, 192 или 256).
    """
    print("Запуск генерации ключей...")
    
    if key_size_bits not in [128, 192, 256]:
        print("Ошибка: длина ключа Camellia должна быть 128, 192 или 256 бит.")
        return
    sym_key = os.urandom(key_size_bits // 8)
    print(f"Сгенерирован симметричный ключ Camellia ({key_size_bits} бит).")

    keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = keys
    public_key = keys.public_key()
    print("Сгенерирована пара ключей RSA (2048 бит).")

    try:
        with open(settings['public_key'], 'wb') as pub_out:
            pub_out.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        
        with open(settings['secret_key'], 'wb') as priv_out:
            priv_out.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        print(f"Асимметричные ключи сохранены в: {settings['public_key']} и {settings['secret_key']}.")

        enc_sym_key = public_key.encrypt(sym_key, get_asym_padding())
        
        with open(settings['symmetric_key'], 'wb') as sym_out:
            sym_out.write(enc_sym_key)
        print(f"Симметричный ключ зашифрован RSA и сохранен в: {settings['symmetric_key']}.")
        print("Генерация ключей завершена!\n")
    except IOError as e:
        print(f"Ошибка при сохранении ключей: {e}")