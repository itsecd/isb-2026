import argparse
import os

from config_manager import load_settings
from key_generation import generate_aes_key, generate_rsa_keys
from crypto_RSA import encrypt_rsa
from crypto_AES import encrypt_aes, decrypt_aes
from file_utils import (
    save_bytes,
    load_bytes,
    save_public_key,
    save_private_key,
    load_aes_key
)


def parse_arguments():
    """Разбор аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default="settings.json", help='Файл настроек')
    
    parser.add_argument('--own-priv', help='Путь к своему закрытому ключу')
    parser.add_argument('--own-aes', help='Путь к своему зашифрованному AES ключу')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Генерация ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Шифрование')
    group.add_argument('-dec', '--decryption', action='store_true', help='Дешифрование')
    
    return parser.parse_args()


def mode_generation(enc_sym_key_path, pub_key_path, priv_key_path, aes_size=256):
    """
    Генерация ключей гибридной системы
    
    Args:
        enc_sym_key_path: путь для сохранения зашифрованного симметричного ключа
        pub_key_path: путь для сохранения открытого ключа
        priv_key_path: путь для сохранения закрытого ключа
        aes_size: длина AES ключа в битах (128, 192, 256)
    """
    aes_key = generate_aes_key(aes_size)
    priv_key, pub_key = generate_rsa_keys()
    
    save_public_key(pub_key, pub_key_path)
    save_private_key(priv_key, priv_key_path)
    
    encrypted_aes_key = encrypt_rsa(aes_key, pub_key)
    save_bytes(encrypted_aes_key, enc_sym_key_path)


def mode_encryption(input_file, priv_key_path, enc_sym_key_path, output_file):
    """
    Шифрование данных гибридной системой
    
    Args:
        input_file: путь к шифруемому файлу
        priv_key_path: путь к закрытому ключу RSA
        enc_sym_key_path: путь к зашифрованному AES ключу
        output_file: путь для сохранения зашифрованного файла
    """
    aes_key = load_aes_key(enc_sym_key_path, priv_key_path)
    
    plaintext = load_bytes(input_file)
    ciphertext = encrypt_aes(plaintext, aes_key)
    save_bytes(ciphertext, output_file)


def mode_decryption(enc_file_path, priv_key_path, enc_sym_key_path, dec_output_path):
    """
    Дешифрование данных гибридной системой
    
    Args:
        enc_file_path: путь к зашифрованному файлу
        priv_key_path: путь к закрытому ключу RSA
        enc_sym_key_path: путь к зашифрованному AES ключу
        dec_output_path: путь для сохранения расшифрованного файла
    """
    aes_key = load_aes_key(enc_sym_key_path, priv_key_path)
    
    ciphertext = load_bytes(enc_file_path)
    plaintext = decrypt_aes(ciphertext, aes_key)
    save_bytes(plaintext, dec_output_path)


def main():
    args = parse_arguments()
    
    if not os.path.exists(args.config):
        print(f"[-] Файл не найден: {args.config}")
        return
    
    try:
        settings = load_settings(args.config)
    except Exception as e:
        print(f"[-] Ошибка загрузки настроек: {e}")
        return
    
    try:
        match args:
            case _ if args.generation:
                print("\n=== ГЕНЕРАЦИЯ КЛЮЧЕЙ ===\n")
                mode_generation(
                    settings['symmetric_key'],
                    settings['public_key'],
                    settings['secret_key'],
                    settings.get('aes_key_size', 256)
                )
                print("Ключи сохранены")
                
            case _ if args.encryption:
                print("\n=== ШИФРОВАНИЕ ===\n")
                priv_path = args.own_priv or settings['secret_key']
                aes_path = args.own_aes or settings['symmetric_key']
                
                mode_encryption(
                    settings['initial_file'],
                    priv_path,
                    aes_path,
                    settings['encrypted_file']
                )
                print(f"Файл зашифрован: {settings['encrypted_file']}")
                
            case _ if args.decryption:
                print("\n=== ДЕШИФРОВАНИЕ ===\n")
                priv_path = args.own_priv or settings['secret_key']
                aes_path = args.own_aes or settings['symmetric_key']
                
                mode_decryption(
                    settings['encrypted_file'],
                    priv_path,
                    aes_path,
                    settings['decrypted_file']
                )
                print(f"Файл расшифрован: {settings['decrypted_file']}")
                
    except KeyError as e:
        print(f"[-] Ошибка: В settings.json отсутствует поле {e}")
    except FileNotFoundError as e:
        print(f"[-] Ошибка: Файл не найден - {e}")
    except Exception as e:
        print(f"[-] Непредвиденная ошибка: {e}")


if __name__ == '__main__':
    main()