"""
Модуль главного скрипта для гибридной криптосистемы RSA-AES.
"""

import argparse
import json
import sys
from file_utils import read_binary_file, write_binary_file, generate_random_bytes
from symmetric_crypto import AESCipher, generate_aes_key, SymmetricCryptoError
from asymmetric_crypto import RSAKeyPair, AsymmetricCryptoError

def load_settings():
    """
    Загружает настройки из файла settings.json.
    Возвращает словарь с настройками или безопасные значения по умолчанию.
    """
    default_settings = {
        'secret_key': 'private_key.pem',
        'public_key': 'public_key.pem',
        'symmetric_key': 'symmetric_key.bin',
        'initial_file': 'input.txt',
        'encrypted_file': 'encrypted.bin',
        'decrypted_file': 'decrypted.txt'
    }
    
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            loaded_settings = json.load(f)
            
            return {**default_settings, **loaded_settings}
    except FileNotFoundError:
        print("[!] Файл settings.json не найден. Используются стандартные имена файлов.")
        return default_settings
    except json.JSONDecodeError as e:
        print(f"[!] Ошибка чтения settings.json: {e}. Используются стандартные имена файлов.")
        return default_settings
    except Exception as e:
        print(f"[!] Неожиданная ошибка при загрузке настроек: {e}. Используются стандартные имена файлов.")
        return default_settings


def main():
    """
    Основная функция приложения.
    """
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA-AES.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Генерация ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Шифрование')
    group.add_argument('-dec', '--decryption', action='store_true', help='Дешифрование')
    
    parser.add_argument('--key-size', type=int, default=256, choices=[128, 192, 256],
                        help='Размер ключа AES в битах (по умолчанию 256)')
    
    args = parser.parse_args()
    settings = load_settings()

    try:
        
        match True:
            case _ if args.generation:
                print("[*] Режим генерации ключей...")
                
                sym_key = generate_aes_key(args.key_size)
                print(f"  Сгенерирован симметричный ключ AES ({args.key_size} бит)")

                rsa_keys = RSAKeyPair()
                rsa_keys.save_to_files(
                    settings['secret_key'],
                    settings['public_key']
                )
                print("  Сохранены RSA-ключи")

                enc_sym_key = rsa_keys.encrypt_symmetric_key(sym_key)
                write_binary_file(settings['symmetric_key'], enc_sym_key)
                print("  Зашифрованный симметричный ключ сохранён")

            case _ if args.encryption:
                print("[*] Режим шифрования...")
                
                try:
                    rsa_keys = RSAKeyPair.load_from_files(
                        settings['secret_key'],
                        settings['public_key']
                    )
                except (FileNotFoundError, ValueError, AsymmetricCryptoError) as e: 
                    print(f"[!] Ошибка загрузки RSA-ключей: {e}")
                    return 
                
                try:
                    enc_sym_key = read_binary_file(settings['symmetric_key'])
                except FileNotFoundError as e:
                    print(f"[!] Ошибка чтения файла симметричного ключа: {e}")
                    return

                try:
                    sym_key = rsa_keys.decrypt_symmetric_key(enc_sym_key)
                except AsymmetricCryptoError as e: 
                    print(f"[!] Ошибка расшифровки симметричного ключа: {e}")
                    return

                print("  Симметричный ключ расшифрован")
        
                try:
                    plaintext = read_binary_file(settings['initial_file'])
                except FileNotFoundError as e:
                    print(f"[!] Ошибка чтения файла данных для шифрования: {e}")
                    return
                
                print(f"  Прочитано {len(plaintext)} байт")

                iv = generate_random_bytes(16)
                cipher = AESCipher(sym_key)
                ciphertext = cipher.encrypt(plaintext, iv)

                try:
                    write_binary_file(settings['encrypted_file'], iv + ciphertext)
                except Exception as e: 
                    print(f"[!] Ошибка записи зашифрованных данных: {e}")
                    return
                
                print("  Данные зашифрованы и сохранены")

            case _ if args.decryption:
                print("[*] Режим дешифрования...")

                try:
                    rsa_keys = RSAKeyPair.load_from_files(
                        settings['secret_key'],
                        settings['public_key']
                    )
                except (FileNotFoundError, ValueError, AsymmetricCryptoError) as e:
                    print(f"[!] Ошибка загрузки RSA-ключей: {e}")
                    return

                try:
                    enc_sym_key = read_binary_file(settings['symmetric_key'])
                except FileNotFoundError as e:
                    print(f"[!] Ошибка чтения файла симметричного ключа: {e}")
                    return

                try:
                    sym_key = rsa_keys.decrypt_symmetric_key(enc_sym_key)
                except AsymmetricCryptoError as e:
                    print(f"[!] Ошибка расшифровки симметричного ключа: {e}")
                    return

                print("  Симметричный ключ расшифрован")

                try:
                    encrypted_data = read_binary_file(settings['encrypted_file'])
                except FileNotFoundError as e:
                    print(f"[!] Ошибка чтения файла зашифрованных данных: {e}")
                    return

                if len(encrypted_data) < 16:
                     print("[!] Ошибка: файл зашифрованных данных слишком короткий (менее 16 байт IV).")
                     return
                     
                iv = encrypted_data[:16]
                ciphertext = encrypted_data[16:]
                
                cipher = AESCipher(sym_key)
                try:
                    plaintext = cipher.decrypt(ciphertext, iv)
                except SymmetricCryptoError as e: 
                    print(f"[!] Ошибка дешифрования данных: {e}")
                    return

                try:
                    write_binary_file(settings['decrypted_file'], plaintext)
                except Exception as e:
                    print(f"[!] Ошибка записи расшифрованных данных: {e}")
                    return
                
                print("  Данные расшифрованы и сохранены")

    except KeyboardInterrupt:
        print("\n[*] Операция прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Непредвиденная ошибка в основном процессе: {e}")
        sys.exit(1) 

if __name__ == "__main__":
    main()
