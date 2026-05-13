"""Модуль дешифрования данных гибридной системой"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import read_binary_file, write_text_file
from src.asymmetric import decrypt_with_rsa
from src.symmetric import decrypt_with_camellia


def run_decryption(encrypted_file: str, private_key_path: str, 
                   encrypted_symmetric_key_path: str, output_file: str,
                   crypto_config: dict) -> None:
    """Режим дешифрования (п.3.1 - 3.2)"""
    print("\n" + "="*60)
    print("РЕЖИМ 3: ДЕШИФРОВАНИЕ ДАННЫХ ГИБРИДНОЙ СИСТЕМОЙ")
    print("="*60)
    
    print("\n[3.1] Расшифровка симметричного ключа...")
    encrypted_key = read_binary_file(encrypted_symmetric_key_path)
    symmetric_key = decrypt_with_rsa(encrypted_key, private_key_path)
    print(f"[OK] Симметричный ключ получен ({len(symmetric_key)} байт)")
    
    print(f"\n[3.2] Чтение зашифрованного файла: {encrypted_file}")
    encrypted_data = read_binary_file(encrypted_file)
    print(f"[OK] Прочитано {len(encrypted_data)} байт")
    
    print("[3.2] Расшифровка данных Camellia (CBC)...")
    decrypted_data = decrypt_with_camellia(encrypted_data, symmetric_key, crypto_config)
    
    print(f"[3.2] Сохранение расшифрованного файла: {output_file}")
    write_text_file(output_file, decrypted_data)
    
    print("\n" + "="*60)
    print("[ГОТОВО] Дешифрование завершено!")
    print("="*60)
    
    try:
        preview = decrypted_data[:200].decode('utf-8')
        print(f"\n[ПРЕВЬЮ РАСШИФРОВАННОГО ТЕКСТА]:")
        print("-" * 50)
        print(preview + ("..." if len(decrypted_data) > 200 else ""))
        print("-" * 50)
    except UnicodeDecodeError:
        pass