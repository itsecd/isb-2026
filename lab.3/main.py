"""
Режимы работы:
  --gen    - Генерация ключей
  --enc    - Шифрование данных
  --dec    - Дешифрование данных
"""

import argparse
import json
import os
import sys

from src.key_generator import run_key_generation
from src.encryptor import run_encryption
from src.decryptor import run_decryption
from src.utils import load_settings, save_settings


DEFAULT_SETTINGS = {
    'initial_file': 'data/plaintext.txt',
    'encrypted_file': 'data/encrypted.bin',
    'decrypted_file': 'data/decrypted.txt',
    'symmetric_key': 'keys/symmetric.key',
    'encrypted_symmetric_key': 'keys/encrypted_symmetric.key',
    'public_key': 'keys/public.pem',
    'private_key': 'keys/private.pem'
}


def create_directories():
    """Создание необходимых директорий"""
    dirs = ['data', 'keys']
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def print_menu():
    """Вывод меню интерактивного режима"""
    print("\n" + "="*60)
    print("Гибридная криптосистема (RSA + Camellia)")
    print("Лабораторная работа №3")
    print("="*60)
    print("\nРежимы работы:")
    print("  1 - Генерация ключей ")
    print("  2 - Шифрование данных ")
    print("  3 - Дешифрование данных ")
    print("  4 - Настройка путей к файлам")
    print("  0 - Выход")
    print("-"*60)


def configure_paths(settings):
    """Настройка путей к файлам"""
    print("\n Настройки ")
    for key, value in settings.items():
        print(f"  {key}: {value}")
    
    print("\n Введите новые значения (Enter - оставить без изменений) ")
    for key in DEFAULT_SETTINGS.keys():
        new_value = input(f"{key} [{settings[key]}]: ").strip()
        if new_value:
            settings[key] = new_value
    
    save_settings(settings)
    return settings


def interactive_mode():
    """Интерактивный режим ввода параметров """
    create_directories()
    settings = load_settings()
    
    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value
    
    while True:
        print_menu()
        choice = input("\nВаш выбор: ").strip()
        
        if choice == '1':
            print("\n Генерирование ключей... ")
            run_key_generation(
                public_key_path=settings['public_key'],
                private_key_path=settings['private_key'],
                symmetric_key_path=settings['symmetric_key'],
                encrypted_symmetric_key_path=settings['encrypted_symmetric_key']
            )
            input("\nНажмите Enter для продолжения...")
        
        elif choice == '2':
            print("\n Шифрование ")
            
            if not os.path.exists(settings['encrypted_symmetric_key']):
                print(f"\n Зашифрованный симметричный ключ не найден: {settings['encrypted_symmetric_key']}")
                print("Сначала выполните режим 1 (Генерация ключей).")
                input("\nНажмите Enter для продолжения...")
                continue
            
            if not os.path.exists(settings['initial_file']):
                print(f"\n Исходный файл не найден: {settings['initial_file']}")
                create_sample = input("Создать пример файла для тестирования? (y/n): ").strip().lower()
                if create_sample == 'y':
                    os.makedirs(os.path.dirname(settings['initial_file']), exist_ok=True)
                    with open(settings['initial_file'], 'w', encoding='utf-8') as f:
                        f.write("Это тестовое сообщение для проверки работоспособности системы.\n")
                        f.write("Используются алгоритмы: RSA (асимметричный) и Camellia (симметричный).\n")
                    print(f" Создан пример файла: {settings['initial_file']}")
                else:
                    print("Отмена.")
                    input("\nНажмите Enter для продолжения...")
                    continue
            
            run_encryption(
                input_file=settings['initial_file'],
                private_key_path=settings['private_key'],
                encrypted_symmetric_key_path=settings['encrypted_symmetric_key'],
                output_file=settings['encrypted_file']
            )
            input("\nНажмите Enter для продолжения...")
        
        elif choice == '3':
            print("\n Дешифрование")
            
            if not os.path.exists(settings['encrypted_symmetric_key']):
                print(f"\n Зашифрованный симметричный ключ не найден: {settings['encrypted_symmetric_key']}")
                print("Сначала выполните режим 1 (Генерация ключей).")
                input("\nНажмите Enter для продолжения...")
                continue
            
            if not os.path.exists(settings['encrypted_file']):
                print(f"\n Зашифрованный файл не найден: {settings['encrypted_file']}")
                print("Сначала выполните режим 2 (Шифрование).")
                input("\nНажмите Enter для продолжения...")
                continue
            
            run_decryption(
                encrypted_file=settings['encrypted_file'],
                private_key_path=settings['private_key'],
                encrypted_symmetric_key_path=settings['encrypted_symmetric_key'],
                output_file=settings['decrypted_file']
            )
            input("\nНажмите Enter для продолжения...")
        
        elif choice == '4':
            settings = configure_paths(settings)
        
        elif choice == '0':
            print("\nДо свидания!")
            break
        
        else:
            print("\n Неверный выбор. Пожалуйста, выберите 0-4.")
            input("Нажмите Enter для продолжения...")


def main():
    """Основная функция с поддержкой аргументов командной строки"""
    
    parser = argparse.ArgumentParser(
        description='Гибридная криптосистема (RSA + Camellia)',
        epilog='''
Примеры использования(используется для самостоятельного ввода):
  # Генерация ключей 
  python main.py --gen --public keys/public.pem --private keys/private.pem --symmetric keys/symmetric.key --encrypted-symmetric keys/encrypted_symmetric.key

  # Шифрование данных 
  python main.py --enc --input data/plaintext.txt --private keys/private.pem --encrypted-symmetric keys/encrypted_symmetric.key --output data/encrypted.bin

  # Дешифрование данных 
  python main.py --dec --input data/encrypted.bin --private keys/private.pem --encrypted-symmetric keys/encrypted_symmetric.key --output data/decrypted.txt

  # Интерактивный режим(режим "приложения")
  python main.py --interactive
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--gen', action='store_true', help='Режим генерации ключей (п.1.1-1.4)')
    group.add_argument('--enc', action='store_true', help='Режим шифрования (п.2.1-2.2)')
    group.add_argument('--dec', action='store_true', help='Режим дешифрования (п.3.1-3.2)')
    group.add_argument('--interactive', action='store_true', help='Интерактивный режим с меню')
    
    parser.add_argument('--public', dest='public_key', help='Путь для сохранения открытого ключа RSA')
    parser.add_argument('--private', dest='private_key', help='Путь для сохранения закрытого ключа RSA')
    parser.add_argument('--symmetric', dest='symmetric_key', help='Путь для сохранения симметричного ключа Camellia')
    parser.add_argument('--encrypted-symmetric', dest='encrypted_symmetric_key', 
                        help='Путь для сохранения зашифрованного симметричного ключа')
    
    parser.add_argument('--input', '-i', help='Путь к входному файлу')
    parser.add_argument('--output', '-o', help='Путь к выходному файлу')
    
    args = parser.parse_args()
    
    create_directories()
    settings = load_settings()
    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value
    
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return
    
    if args.gen:
        public_path = args.public_key or settings['public_key']
        private_path = args.private_key or settings['private_key']
        symmetric_path = args.symmetric_key or settings['symmetric_key']
        encrypted_symmetric_path = args.encrypted_symmetric_key or settings['encrypted_symmetric_key']
        
        run_key_generation(public_path, private_path, symmetric_path, encrypted_symmetric_path)
        return
    
    if args.enc:
        input_file = args.input or settings['initial_file']
        output_file = args.output or settings['encrypted_file']
        private_path = args.private_key or settings['private_key']
        encrypted_symmetric_path = args.encrypted_symmetric_key or settings['encrypted_symmetric_key']
        
        if not os.path.exists(encrypted_symmetric_path):
            print(f"\n Зашифрованный симметричный ключ не найден: {encrypted_symmetric_path}")
            print("Сначала выполните режим --gen")
            sys.exit(1)
        
        run_encryption(input_file, private_path, encrypted_symmetric_path, output_file)
        return
    
    if args.dec:
        input_file = args.input or settings['encrypted_file']
        output_file = args.output or settings['decrypted_file']
        private_path = args.private_key or settings['private_key']
        encrypted_symmetric_path = args.encrypted_symmetric_key or settings['encrypted_symmetric_key']
        
        if not os.path.exists(encrypted_symmetric_path):
            print(f"\n Зашифрованный симметричный ключ не найден: {encrypted_symmetric_path}")
            print("Сначала выполните режим --gen")
            sys.exit(1)
        
        run_decryption(input_file, private_path, encrypted_symmetric_path, output_file)
        return


if __name__ == '__main__':
    main()