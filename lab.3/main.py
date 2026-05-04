#!/usr/bin/env python3
"""
Гибридная криптосистема с использованием RSA и Camellia
Лабораторная работа №3 "Основы Информационной Безопасности"
"""

import argparse
import os
import sys

from src.config import load_settings, save_settings, HELP_DESCRIPTION, HELP_EPILOG
from src.key_generator import run_key_generation
from src.encryptor import run_encryption
from src.decryptor import run_decryption


def create_directories():
    """Создание необходимых директорий"""
    for d in ['data', 'keys']:
        os.makedirs(d, exist_ok=True)


def configure_paths(settings):
    """Настройка путей к файлам"""
    print("\n Настройка путей ")
    print("Текущие значения (Enter - оставить без изменений):")
    
    for key in settings.keys():
        new_value = input(f"  {key} [{settings[key]}]: ").strip()
        if new_value:
            settings[key] = new_value
    
    save_settings(settings)
    return settings


def print_menu():
    """Вывод меню"""
    print("\n" + "="*60)
    print("Гибридная система (RSA + Camellia)")
    print("Лабораторная работа №3")
    print("="*60)
    print("\nРежимы работы:")
    print("  1 - Генерация ключей ")
    print("  2 - Шифрование данных ")
    print("  3 - Дешифрование данных ")
    print("  4 - Настройка путей")
    print("  0 - Выход")
    print("-"*60)


def interactive_mode():
    """Интерактивный режим """
    create_directories()
    settings = load_settings()
    
    while True:
        print_menu()
        choice = input("\nВаш выбор: ").strip()
        
        match choice:
            case '1':
                print("\n Генерация ключей ")
                run_key_generation(
                    public_key_path=settings['public_key'],
                    private_key_path=settings['private_key'],
                    symmetric_key_path=settings['symmetric_key'],
                    encrypted_symmetric_key_path=settings['encrypted_symmetric_key']
                )
                input("\nНажмите Enter для продолжения...")
            
            case '2':
                print("\n Шифрование данных")
                if not os.path.exists(settings['encrypted_symmetric_key']):
                    print(f"\n Зашифрованный симметричный ключ не найден: {settings['encrypted_symmetric_key']}")
                    print("Сначала выполните режим 1 (Генерация ключей).")
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                run_encryption(
                    input_file=settings['initial_file'],
                    private_key_path=settings['private_key'],
                    encrypted_symmetric_key_path=settings['encrypted_symmetric_key'],
                    output_file=settings['encrypted_file']
                )
                input("\nНажмите Enter для продолжения...")
            
            case '3':
                print("\n Дешифрование данных")
                if not os.path.exists(settings['encrypted_symmetric_key']):
                    print(f"\n Зашифрованный симметричный ключ не найден: {settings['encrypted_symmetric_key']}")
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                if not os.path.exists(settings['encrypted_file']):
                    print(f"\n Зашифрованный файл не найден: {settings['encrypted_file']}")
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                run_decryption(
                    encrypted_file=settings['encrypted_file'],
                    private_key_path=settings['private_key'],
                    encrypted_symmetric_key_path=settings['encrypted_symmetric_key'],
                    output_file=settings['decrypted_file']
                )
                input("\nНажмите Enter для продолжения...")
            
            case '4':
                settings = configure_paths(settings)
            
            case '0':
                print("\nДо свидания!")
                break
            
            case _:
                print("\n Неверный выбор. Пожалуйста, выберите 0-4.")
                input("Нажмите Enter для продолжения...")


def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(
        description=HELP_DESCRIPTION,
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--interactive', action='store_true', help='Интерактивный режим')
    parser.add_argument('--gen', action='store_true', help='Генерация ключей')
    parser.add_argument('--enc', action='store_true', help='Шифрование')
    parser.add_argument('--dec', action='store_true', help='Дешифрование')
    
    parser.add_argument('--public', dest='public_key', help='Открытый ключ RSA')
    parser.add_argument('--private', dest='private_key', help='Закрытый ключ RSA')
    parser.add_argument('--symmetric', dest='symmetric_key', help='Симметричный ключ')
    parser.add_argument('--encrypted-symmetric', dest='encrypted_symmetric_key', help='Зашифрованный симметричный ключ')
    parser.add_argument('--input', '-i', help='Входной файл')
    parser.add_argument('--output', '-o', help='Выходной файл')
    
    args = parser.parse_args()
    
    create_directories()
    settings = load_settings()
    
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return
    
    match True:
        case _ if args.gen:
            public = args.public_key or settings['public_key']
            private = args.private_key or settings['private_key']
            symmetric = args.symmetric_key or settings['symmetric_key']
            encrypted_sym = args.encrypted_symmetric_key or settings['encrypted_symmetric_key']
            run_key_generation(public, private, symmetric, encrypted_sym)
        
        case _ if args.enc:
            input_file = args.input or settings['initial_file']
            output_file = args.output or settings['encrypted_file']
            private = args.private_key or settings['private_key']
            encrypted_sym = args.encrypted_symmetric_key or settings['encrypted_symmetric_key']
            run_encryption(input_file, private, encrypted_sym, output_file)
        
        case _ if args.dec:
            input_file = args.input or settings['encrypted_file']
            output_file = args.output or settings['decrypted_file']
            private = args.private_key or settings['private_key']
            encrypted_sym = args.encrypted_symmetric_key or settings['encrypted_symmetric_key']
            run_decryption(input_file, private, encrypted_sym, output_file)
        
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()