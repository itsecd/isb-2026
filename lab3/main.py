"""
Модуль главного скрипта для гибридной криптосистемы RSA-AES.

Этот скрипт предоставляет интерфейс командной строки для:
- Генерации ключей (AES и RSA)
- Шифрования данных с использованием гибридной схемы
- Дешифрования данных
Конфигурация осуществляется через файл settings.json.
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

    Возвращает:
        dict: Словарь с настройками. Если файл не найден, возвращается пустой словарь.
    """
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("[!] Файл settings.json не найден, используются настройки по умолчанию.")
        return {}
    except json.JSONDecodeError as e:
        print(f"[!] Ошибка чтения settings.json: {e}. Используются настройки по умолчанию.")
        return {}
    except Exception as e:
        print(f"[!] Неожиданная ошибка при загрузке настроек: {e}")
        
        return {}


def main():
    """
    Основная функция приложения.

    Обрабатывает аргументы командной строки и запускает соответствующий режим работы:
    генерация ключей, шифрование или дешифрование.
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
        if args.generation:
            print("[*] Режим генерации ключей...")
            sym_key = generate_aes_key(args.key_size)
            print(f"  Сгенерирован симметричный ключ AES ({args.key_size} бит)")

            rsa_keys = RSAKeyPair()
            rsa_keys.save_to_files(
                settings.get('secret_key', 'private_key.pem'),
                settings.get('public_key', 'public_key.pem')
            )
            print(f"  Сохранены RSA-ключи")

            enc_sym_key = rsa_keys.encrypt_symmetric_key(sym_key)
            write_binary_file(settings.get('symmetric_key', 'symmetric_key.bin'), enc_sym_key)
            print(f"  Зашифрованный симметричный ключ сохранён")

        elif args.encryption:
            print("[*] Режим шифрования...")
            
            
            try:
                rsa_keys = RSAKeyPair.load_from_files(
                    settings.get('secret_key', 'private_key.pem'),
                    settings.get('public_key', 'public_key.pem')
                )
            except (FileNotFoundError, ValueError) as e: 
                print(f"[!] Ошибка загрузки RSA-ключей: {e}")
                return 
            
            
            try:
                enc_sym_key = read_binary_file(settings.get('symmetric_key', 'symmetric_key.bin'))
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
                plaintext = read_binary_file(settings.get('initial_file', 'input.txt'))
            except FileNotFoundError as e:
                print(f"[!] Ошибка чтения файла данных для шифрования: {e}")
                return
            
            print(f"  Прочитано {len(plaintext)} байт")

            
            iv = generate_random_bytes(16)
            cipher = AESCipher(sym_key)
            ciphertext = cipher.encrypt(plaintext, iv)

            
            try:
                write_binary_file(settings.get('encrypted_file', 'encrypted.bin'), iv + ciphertext)
            except Exception as e: 
                print(f"[!] Ошибка записи зашифрованных данных: {e}")
                return
            
            print("  Данные зашифрованы и сохранены")

        elif args.decryption:
            print("[*] Режим дешифрования...")

            
            try:
                rsa_keys = RSAKeyPair.load_from_files(
                    settings.get('secret_key', 'private_key.pem'),
                    settings.get('public_key', 'public_key.pem')
                )
            except (FileNotFoundError, ValueError) as e:
                print(f"[!] Ошибка загрузки RSA-ключей: {e}")
                return

            
            try:
                enc_sym_key = read_binary_file(settings.get('symmetric_key', 'symmetric_key.bin'))
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
                encrypted_data = read_binary_file(settings.get('encrypted_file', 'encrypted.bin'))
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
                write_binary_file(settings.get('decrypted_file', 'decrypted.txt'), plaintext)
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
